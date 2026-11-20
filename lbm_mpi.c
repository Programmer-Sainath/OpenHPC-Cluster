/*
 * Parallel D2Q9 BGK lattice-Boltzmann simulation of flow past a cylinder.
 * MPI decomposition: contiguous slabs in x, periodic in y.
 * Boundaries: Zou/He velocity inlet; zero-gradient population outlet;
 *             half-way bounce-back at stationary cylinder.
 * Outputs: MPI-gathered, spatially downsampled vorticity PPM frames.
 *
 * This is a 2-D weakly compressible educational/research demonstrator,
 * NOT a validated engineering CFD solver. Stability and convergence depend
 * on discretization, boundary conditions, Reynolds number, and runtime.
 */
#include <mpi.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <errno.h>

static const int ex[9]  = {0, 1, 0,-1, 0, 1,-1,-1, 1};
static const int ey[9]  = {0, 0, 1, 0,-1, 1, 1,-1,-1};
static const int opp[9] = {0, 3, 4, 1, 2, 7, 8, 5, 6};
static const double w[9] = {4.0/9.0,1.0/9.0,1.0/9.0,1.0/9.0,1.0/9.0,
                             1.0/36.0,1.0/36.0,1.0/36.0,1.0/36.0};

typedef struct {
    int nx, ny, steps, diameter, snapshot_every, start_snapshot, stride, log_every;
    double uin, re;
    char outdir[512];
} Params;

typedef struct {
    int rank, size, nxloc, xstart;
    Params p;
    double tau, nu, omega;
    double *f, *post, *next, *ux, *uy;
    unsigned char *solid;
    int nxsamples, nysamples;
    int *counts, *offsets;
    unsigned char *pixels, *allpixels, *rowbuf;
} Sim;

static void fatal(const char *why, int rank) {
    fprintf(stderr, "[rank %d] ERROR: %s\n", rank, why);
    MPI_Abort(MPI_COMM_WORLD, 1);
}
static size_t cell(const Sim *s, int x, int y) {
    return (size_t)x * (size_t)s->p.ny + (size_t)y;
}
static size_t pop(const Sim *s, int x, int y, int i) {
    return cell(s,x,y)*9u+(size_t)i;
}
static void *checked_calloc(size_t n, size_t size, int rank) {
    if (size && n > SIZE_MAX/size) fatal("allocation size overflow",rank);
    void *v=calloc(n,size);
    if (!v) fatal("out of memory while allocating fields",rank);
    return v;
}
static void usage(void) {
    puts("Usage: ./lbm_mpi [--nx N] [--ny N] [--steps N] [--diameter N]"
         " [--re R] [--uin U] [--snapshot-every N] [--start-snapshot N]"
         " [--stride N] [--log-every N] [--out DIRECTORY]\n"
         "Example: srun ./lbm_mpi --nx 2048 --ny 768 --diameter 96"
         " --re 120 --steps 80000 --snapshot-every 1000 --stride 2"
         " --start-snapshot 12000 --out runs/test");
}
static int parse_int(const char *str, int *dest) {
    char *end=NULL; errno=0;
    long v=strtol(str,&end,10);
    if (errno||!end||*end||v<0||v>2147483647L) return 0;
    *dest=(int)v; return 1;
}
static int parse_double(const char *str, double *dest) {
    char *end=NULL; errno=0;
    double v=strtod(str,&end);
    if (errno||!end||*end||!isfinite(v)) return 0;
    *dest=v; return 1;
}
static void parse_args(Params *p, int argc, char **argv, int rank) {
    *p=(Params){.nx=2048,.ny=768,.steps=80000,.diameter=96,
                .snapshot_every=1000,.start_snapshot=12000,.stride=2,
                .log_every=1000,.uin=0.06,.re=120.0};
    snprintf(p->outdir,sizeof(p->outdir),"frames");
    for(int a=1;a<argc;a++) {
        if (!strcmp(argv[a],"--help") || !strcmp(argv[a],"-h")) {
            if(!rank) usage();
            MPI_Finalize();
            exit(0);
        }
        if(a+1>=argc) fatal("option is missing a value",rank);
        const char *k=argv[a++], *v=argv[a];
        int ok=1;
        if (!strcmp(k,"--nx")) ok=parse_int(v,&p->nx);
        else if (!strcmp(k,"--ny")) ok=parse_int(v,&p->ny);
        else if (!strcmp(k,"--steps")) ok=parse_int(v,&p->steps);
        else if (!strcmp(k,"--diameter")) ok=parse_int(v,&p->diameter);
        else if (!strcmp(k,"--snapshot-every")) ok=parse_int(v,&p->snapshot_every);
        else if (!strcmp(k,"--start-snapshot")) ok=parse_int(v,&p->start_snapshot);
        else if (!strcmp(k,"--stride")) ok=parse_int(v,&p->stride);
        else if (!strcmp(k,"--log-every")) ok=parse_int(v,&p->log_every);
        else if (!strcmp(k,"--uin")) ok=parse_double(v,&p->uin);
        else if (!strcmp(k,"--re")) ok=parse_double(v,&p->re);
        else if (!strcmp(k,"--out")) {
            if (strlen(v)>=sizeof(p->outdir)) fatal("output directory path too long",rank);
            snprintf(p->outdir,sizeof(p->outdir),"%s",v);
        }
        else fatal("unknown option (run --help)",rank);
        if(!ok) fatal("invalid numeric option",rank);
    }
    if(p->nx<80||p->ny<48||p->steps<1||p->diameter<8||
       p->diameter>p->ny/3||p->diameter>p->nx/8||
       p->snapshot_every<1||p->stride<1||p->log_every<1||
       p->start_snapshot<0||p->re<20.0||p->re>220.0||
       p->uin<=0.0||p->uin>0.12||!strlen(p->outdir))
        fatal("invalid simulation parameters; Re must be 20-220, Uin <=0.12, cylinder sufficiently small",rank);
}
static void equilibrium(double *f, double rho, double ux, double uy) {
    double u2=ux*ux+uy*uy;
    for(int i=0;i<9;i++) {
        double cu=ex[i]*ux+ey[i]*uy;
        f[i]=w[i]*rho*(1.0+3.0*cu+4.5*cu*cu-1.5*u2);
    }
}
static int is_cylinder(const Sim *s, int gx, int y) {
    if(gx<0||gx>=s->p.nx) return 0;
    double dx=(double)gx-0.20*(double)s->p.nx;
    double dy=(double)y-0.5*(double)s->p.ny;
    double r=0.5*(double)s->p.diameter;
    return dx*dx+dy*dy<=r*r;
}
static void init(Sim *s) {
    Params *p=&s->p;
    s->nxloc=p->nx/s->size+(s->rank<p->nx%s->size?1:0);
    s->xstart=(p->nx/s->size)*s->rank+(s->rank<p->nx%s->size?s->rank:p->nx%s->size);
    if(s->nxloc<2) fatal("each rank requires at least 2 x-columns; decrease MPI ranks",s->rank);
    s->nu=p->uin*p->diameter/p->re;
    s->tau=0.5+3.0*s->nu;
    s->omega=1.0/s->tau;
    if (s->tau<=0.505 || s->tau>2.0) fatal("relaxation time tau outside safe range",s->rank);
    size_t n=(size_t)(s->nxloc+2)*(size_t)p->ny;
    s->f=checked_calloc(n*9, sizeof(double),s->rank);
    s->post=checked_calloc(n*9,sizeof(double),s->rank);
    s->next=checked_calloc(n*9,sizeof(double),s->rank);
    s->ux=checked_calloc(n,sizeof(double),s->rank);
    s->uy=checked_calloc(n,sizeof(double),s->rank);
    s->solid=checked_calloc(n,sizeof(unsigned char),s->rank);
    for(int x=0;x<s->nxloc+2;x++) {
        int gx=s->xstart+x-1;
        for(int y=0;y<p->ny;y++) {
            s->solid[cell(s,x,y)]=(unsigned char)is_cylinder(s,gx,y);
            double ux=p->uin, uy=0.;
            if (s->solid[cell(s,x,y)]) ux=0.;
            else {
                /* Tiny initial asymmetric perturbation seeds physical shedding. */
                double dx=((double)gx-(0.2*p->nx+1.5*p->diameter))/p->diameter;
                double dy=((double)y-(0.5*p->ny+0.6*p->diameter))/p->diameter;
                uy=0.03*p->uin*exp(-2.0*dx*dx-2.0*dy*dy);
            }
            equilibrium(&s->f[pop(s,x,y,0)],1.0,ux,uy);
        }
    }
    s->nysamples=(p->ny+p->stride-1)/p->stride;
    s->nxsamples=0;
    for(int x=0;x<s->nxloc;x++)
        if((s->xstart+x)%p->stride==0) s->nxsamples++;
    size_t localbytes=(size_t)s->nxsamples*s->nysamples*3;
    if(localbytes>2147483647u) fatal("per-rank frame too big for MPI_Gatherv",s->rank);
    s->pixels=checked_calloc(localbytes?localbytes:1,1,s->rank);
    s->counts=checked_calloc((size_t)s->size,sizeof(int),s->rank);
    s->offsets=checked_calloc((size_t)s->size,sizeof(int),s->rank);
    int nbytes=(int)localbytes;
    MPI_Gather(&nbytes,1,MPI_INT,s->counts,1,MPI_INT,0,MPI_COMM_WORLD);
    if(s->rank==0) {
        int sum=0;
        for(int i=0;i<s->size;i++) {
            s->offsets[i]=sum;
            if(s->counts[i]>2147483647-sum) fatal("gathered frame too big",s->rank);
            sum+=s->counts[i];
        }
        int expectedx=(p->nx+p->stride-1)/p->stride;
        if(sum!=(int)((size_t)expectedx*s->nysamples*3)) fatal("sampled frame partition mismatch",s->rank);
        s->allpixels=checked_calloc((size_t)sum,1,s->rank);
        s->rowbuf=checked_calloc((size_t)expectedx*3,1,s->rank);
    }
}
static void exchange_distribution(Sim *s) {
    int prev=(s->rank>0?s->rank-1:MPI_PROC_NULL);
    int next=(s->rank+1<s->size?s->rank+1:MPI_PROC_NULL);
    int count=s->p.ny*9;
    /* Send first owned column left, receive last neighbor to right halo. */
    MPI_Sendrecv(&s->post[pop(s,1,0,0)],count,MPI_DOUBLE,prev,100,
                 &s->post[pop(s,s->nxloc+1,0,0)],count,MPI_DOUBLE,next,100,
                 MPI_COMM_WORLD,MPI_STATUS_IGNORE);
    /* Send last owned column right, receive first neighbor to left halo. */
    MPI_Sendrecv(&s->post[pop(s,s->nxloc,0,0)],count,MPI_DOUBLE,next,101,
                 &s->post[pop(s,0,0,0)],count,MPI_DOUBLE,prev,101,
                 MPI_COMM_WORLD,MPI_STATUS_IGNORE);
}
static void collide(Sim *s, int step, double *localmass, double *localmax) {
    int do_stats=(step%s->p.log_every==0||step==s->p.steps);
    *localmass=0; *localmax=0;
    for(int x=1;x<=s->nxloc;x++) for(int y=0;y<s->p.ny;y++) {
        size_t c=cell(s,x,y);
        if(s->solid[c]) continue;
        size_t at=c*9u;
        const double *f=&s->f[at];
        double rho=0.;
        for(int i=0;i<9;i++) rho+=f[i];
        if(!(rho>0.01) || !isfinite(rho)) fatal("non-positive/non-finite density: numerical instability",s->rank);
        double ux=(f[1]+f[5]+f[8]-f[3]-f[6]-f[7])/rho;
        double uy=(f[2]+f[5]+f[6]-f[4]-f[7]-f[8])/rho;
        double u2=ux*ux+uy*uy;
        if(!isfinite(u2)||u2>0.16) fatal("excessive speed/non-finite velocity: numerical instability",s->rank);
        for(int i=0;i<9;i++) {
            double cu=ex[i]*ux+ey[i]*uy;
            double feq=w[i]*rho*(1.0+3.0*cu+4.5*cu*cu-1.5*u2);
            s->post[at+(size_t)i]=f[i]+s->omega*(feq-f[i]);
        }
        if(do_stats) {
            *localmass+=rho;
            double speed=sqrt(u2);
            if(speed>*localmax) *localmax=speed;
        }
    }
}
static void stream_and_boundaries(Sim *s) {
    Params *p=&s->p;
    for(int x=1;x<=s->nxloc;x++) {
        int gx=s->xstart+x-1;
        for(int y=0;y<p->ny;y++) {
            size_t at=pop(s,x,y,0);
            if(s->solid[cell(s,x,y)]) {
                for(int i=0;i<9;i++) s->next[at+i]=0.;
                continue;
            }
            for(int i=0;i<9;i++) {
                int upstream_x=x-ex[i], upstream_gx=gx-ex[i];
                if(upstream_gx<0||upstream_gx>=p->nx) {
                    s->next[at+i]=0.; /* overwritten by inlet/outlet */
                    continue;
                }
                int upstream_y=y-ey[i];
                if(upstream_y<0) upstream_y+=p->ny;
                if(upstream_y>=p->ny) upstream_y-=p->ny;
                if(s->solid[cell(s,upstream_x,upstream_y)])
                    s->next[at+i]=s->post[at+opp[i]]; /* halfway bounceback */
                else
                    s->next[at+i]=s->post[pop(s,upstream_x,upstream_y,i)];
            }
            if(gx==0) {
                double *f=&s->next[at];
                double rho=(f[0]+f[2]+f[4]+2.0*(f[3]+f[6]+f[7]))/(1.0-p->uin);
                f[1]=f[3]+(2.0/3.0)*rho*p->uin;
                f[5]=f[7]+0.5*(f[4]-f[2])+(1.0/6.0)*rho*p->uin;
                f[8]=f[6]+0.5*(f[2]-f[4])+(1.0/6.0)*rho*p->uin;
            }
        }
    }
    if(s->rank==s->size-1) {
        /* Extrapolation of populations at outlet; do not reflect via periodic x. */
        int x=s->nxloc;
        for(int y=0;y<p->ny;y++)
            memcpy(&s->next[pop(s,x,y,0)],&s->next[pop(s,x-1,y,0)],9*sizeof(double));
    }
    double *tmp=s->f; s->f=s->next; s->next=tmp;
}
static void exchange_velocity(Sim *s) {
    int prev=(s->rank>0?s->rank-1:MPI_PROC_NULL);
    int next=(s->rank+1<s->size?s->rank+1:MPI_PROC_NULL);
    int ny=s->p.ny;
    double *fields[2]={s->ux,s->uy};
    for(int field=0;field<2;field++) {
        double *u=fields[field];
        MPI_Sendrecv(&u[ny],ny,MPI_DOUBLE,prev,200+field*2,
                     &u[(size_t)(s->nxloc+1)*ny],ny,MPI_DOUBLE,next,200+field*2,
                     MPI_COMM_WORLD,MPI_STATUS_IGNORE);
        MPI_Sendrecv(&u[(size_t)s->nxloc*ny],ny,MPI_DOUBLE,next,201+field*2,
                     &u[0],ny,MPI_DOUBLE,prev,201+field*2,
                     MPI_COMM_WORLD,MPI_STATUS_IGNORE);
        if(s->rank==0) memcpy(&u[0],&u[ny],(size_t)ny*sizeof(double));
        if(s->rank==s->size-1)
            memcpy(&u[(size_t)(s->nxloc+1)*ny],&u[(size_t)s->nxloc*ny],(size_t)ny*sizeof(double));
    }
}
static void blend(unsigned char *rgb, double vorticity, const Sim *s, int issolid) {
    if(issolid) {rgb[0]=225;rgb[1]=228;rgb[2]=232;return;}
    /* Dimensionless vorticity scale ~ omega_z * D / U; signed warm/cool. */
    double z=tanh(fabs(vorticity)*(double)s->p.diameter/(s->p.uin*6.0));
    double r=vorticity>=0.?244.:32.;
    double g=vorticity>=0.?84.:192.;
    double b=vorticity>=0.?56.:245.;
    rgb[0]=(unsigned char)(12.+z*(r-12.));
    rgb[1]=(unsigned char)(18.+z*(g-18.));
    rgb[2]=(unsigned char)(33.+z*(b-33.));
}
static void frame(Sim *s, int step, int frameid) {
    int ny=s->p.ny;
    for(int x=1;x<=s->nxloc;x++) for(int y=0;y<ny;y++) {
        size_t c=cell(s,x,y);
        if(s->solid[c]) {s->ux[c]=0.;s->uy[c]=0.;continue;}
        const double *f=&s->f[c*9u];
        double rho=0.; for(int i=0;i<9;i++) rho+=f[i];
        s->ux[c]=(f[1]+f[5]+f[8]-f[3]-f[6]-f[7])/rho;
        s->uy[c]=(f[2]+f[5]+f[6]-f[4]-f[7]-f[8])/rho;
    }
    exchange_velocity(s);
    size_t px=0;
    for(int x=1;x<=s->nxloc;x++) {
        int gx=s->xstart+x-1;
        if(gx%s->p.stride) continue;
        for(int y=0;y<ny;y+=s->p.stride) {
            int yp=(y+1<ny?y+1:0);
            int ym=(y>0?y-1:ny-1);
            size_t c=cell(s,x,y);
            double vort=0.;
            if(!s->solid[c])
                vort=0.5*(s->uy[cell(s,x+1,y)]-s->uy[cell(s,x-1,y)]
                          -s->ux[cell(s,x,yp)]+s->ux[cell(s,x,ym)]);
            blend(&s->pixels[px],vort,s,s->solid[c]);
            px+=3;
        }
    }
    MPI_Gatherv(s->pixels,(int)px,MPI_UNSIGNED_CHAR,
                s->allpixels,s->counts,s->offsets,MPI_UNSIGNED_CHAR,0,MPI_COMM_WORLD);
    if(s->rank==0) {
        char path[1024];
        snprintf(path,sizeof(path),"%s/frame_%06d.ppm",s->p.outdir,frameid);
        FILE *fp=fopen(path,"wb");
        if(!fp) fatal("cannot create frame; ensure output directory exists and is writable",0);
        int width=(s->p.nx+s->p.stride-1)/s->p.stride;
        fprintf(fp,"P6\n%d %d\n255\n",width,s->nysamples);
        for(int y=s->nysamples-1;y>=0;y--) {
            for(int x=0;x<width;x++) {
                size_t src=((size_t)x*s->nysamples+(size_t)y)*3;
                memcpy(&s->rowbuf[(size_t)x*3],&s->allpixels[src],3);
            }
            if(fwrite(s->rowbuf,3,(size_t)width,fp)!=(size_t)width) fatal("error writing frame",0);
        }
        if(fclose(fp)!=0) fatal("error closing frame",0);
        printf("Frame %d saved (step %d, %dx%d)\n",frameid,step,width,s->nysamples);
        fflush(stdout);
    }
}
static void release(Sim *s) {
    free(s->f);free(s->post);free(s->next);free(s->ux);free(s->uy);
    free(s->solid);free(s->pixels);free(s->counts);free(s->offsets);
    free(s->allpixels);free(s->rowbuf);
}
int main(int argc, char **argv) {
    MPI_Init(&argc,&argv);
    Sim s={0};
    MPI_Comm_rank(MPI_COMM_WORLD,&s.rank);
    MPI_Comm_size(MPI_COMM_WORLD,&s.size);
    parse_args(&s.p,argc,argv,s.rank);
    init(&s);
    if(s.rank==0) {
        double gib=(double)s.p.nx*s.p.ny*9.0*8.0*3.0/(1024.*1024.*1024.);
        printf("D2Q9 MPI LBM | %d ranks | grid %dx%d | steps %d | cylinder D %d\n",s.size,s.p.nx,s.p.ny,s.p.steps,s.p.diameter);
        printf("Re=%.4f, U=%.5f, nu=%.7f, tau=%.6f, periodic y, zero-gradient outlet\n",s.p.re,s.p.uin,s.nu,s.tau);
        printf("Global population buffers ~%.2f GiB (3x 9 doubles/site), plus auxiliary fields\n",gib);
        printf("Frames: stride=%d every=%d after step=%d, output=%s\n",s.p.stride,s.p.snapshot_every,s.p.start_snapshot,s.p.outdir);
        fflush(stdout);
    }
    MPI_Barrier(MPI_COMM_WORLD);
    double t0=MPI_Wtime();
    int frameid=0;
    for(int step=1;step<=s.p.steps;step++) {
        double lm, lv;
        collide(&s,step,&lm,&lv);
        exchange_distribution(&s);
        stream_and_boundaries(&s);
        if(step%s.p.log_every==0 || step==s.p.steps) {
            double gm, gv;
            MPI_Reduce(&lm,&gm,1,MPI_DOUBLE,MPI_SUM,0,MPI_COMM_WORLD);
            MPI_Reduce(&lv,&gv,1,MPI_DOUBLE,MPI_MAX,0,MPI_COMM_WORLD);
            if(s.rank==0) {
                double secs=MPI_Wtime()-t0;
                double mlups=secs>0? (double)s.p.nx*s.p.ny*(double)step/(secs*1.0e6):0.;
                printf("Step %d/%d | mass %.5g | max(u) %.5f | elapsed %.1f s | avg %.2f MLUPS\n",
                    step,s.p.steps,gm,gv,secs,mlups);
                fflush(stdout);
            }
        }
        if(step>=s.p.start_snapshot && step%s.p.snapshot_every==0) frame(&s,step,frameid++);
    }
    MPI_Barrier(MPI_COMM_WORLD);
    if(s.rank==0) {
        double wall=MPI_Wtime()-t0;
        printf("Finished: %d frames, wall time %.2f s, average %.2f million lattice updates/sec\n",
               frameid,wall,(double)s.p.nx*s.p.ny*s.p.steps/wall/1e6);
    }
    release(&s);
    MPI_Finalize();
    return 0;
}
