# Historical Slurm commands, original `.sbatch` files, and reproduction

This is the **original configuration** executed from `~/jobs/lbm/lbm_mpi_vortex` on Rocky Linux 9.8. The historical source, launcher, encoder and build files were included in your evidence archive and are preserved **unchanged** in [`code/historical/`](code/historical/). The scripts at the top of `code/` are adapted for this nested GitHub results-folder structure.

## 1. Frame-equivalence correctness tests (jobs 91–92)

```bash
SM="--nx 640 --ny 256 --diameter 32 --re 100 --steps 800 --snapshot-every 100 --start-snapshot 100 --stride 1 --log-every 100"
J1=$(LBM_TAG=eq1 sbatch --parsable -N1 --ntasks-per-node=1 lbm.sbatch $SM)
J2=$(LBM_TAG=eq16 sbatch --parsable -N4 --ntasks-per-node=4 --dependency=afterany:$J1 lbm.sbatch $SM)
# Original returned IDs: 91, 92
# Operator later ran a frame md5sum/diff and got PASS: FRAMES IDENTICAL
```

## 2. Identical-workload benchmarks (jobs 93–95)

```bash
BM="--nx 3072 --ny 1024 --diameter 128 --re 120 --steps 4000 --start-snapshot 4001 --snapshot-every 1000 --stride 4 --log-every 1000"
rm -f bench.list; prev=""
b() { dep=""; [ -n "$prev" ] && dep="--dependency=afterany:$prev"; prev=$(LBM_TAG=$1 sbatch --parsable $dep -N$2 --ntasks-per-node=$3 lbm.sbatch $BM); echo "$1 $prev" >> bench.list; }
b bench1 1 1  # job 93
b bench4 1 4  # job 94
b bench16 4 4 # job 95
```

`logs/source-lists/bench.list` contains the original mapping `bench1 93`, `bench4 94`, `bench16 95`. All three logs include exact solver times and rates, copied to [`results.md`](results.md).

## 3. Production (job 96) and dependent video encoder (job 97)

```bash
PJ=$(LBM_TAG=prod sbatch --parsable \
  --time=02:00:00 \
  -N4 --ntasks-per-node=4 \
  lbm.sbatch \
  --nx 2048 --ny 768 --diameter 96 --re 120 --steps 80000 --snapshot-every 250 --start-snapshot 8000 --stride 2 --log-every 1000)
EJ=$(sbatch --parsable --dependency=afterok:$PJ encode.sbatch runs/prod-$PJ)
echo "$PJ $EJ" > prod.jobs
# Original returned IDs: 96, 97
```

Historical `prod.jobs` contained `96 97`. Job 96 completed 289 frames in 897.84 seconds; job 97 encoded `vortex.mp4`. The encoder log contains actual FFmpeg output but **does not contain elapsed wall time**.

## 4. Original historical Slurm launcher — saved file `code/historical/lbm.sbatch`

The following content was **read from the actual cluster evidence archive** (not reconstructed):

```bash
#!/bin/bash
#SBATCH --job-name=lbm
#SBATCH --time=02:00:00
#SBATCH --output=logs/lbm-%j.out
cd "$SLURM_SUBMIT_DIR"
export PATH=/usr/lib64/openmpi/bin:$PATH
export LD_LIBRARY_PATH=/usr/lib64/openmpi/lib:$LD_LIBRARY_PATH
export OMP_NUM_THREADS=1
export OMPI_MCA_pml=ob1 OMPI_MCA_btl=tcp,self,vader OMPI_MCA_btl_tcp_if_include=192.168.10.0/24
TAG=${LBM_TAG:-run}
RUN="runs/${TAG}-${SLURM_JOB_ID}"
mkdir -p "$RUN"
scontrol show hostnames "$SLURM_JOB_NODELIST" | sed "s/\$/ slots=$SLURM_NTASKS_PER_NODE/" > hosts.$SLURM_JOB_ID
echo "job: $SLURM_JOB_ID  nodes: $SLURM_JOB_NODELIST  ntasks: $SLURM_NTASKS  tasks/node: $SLURM_NTASKS_PER_NODE  cpus/task: ${SLURM_CPUS_PER_TASK:-1}  tag: $TAG  args: $@"
echo "start: $(date '+%F %T')"
/usr/lib64/openmpi/bin/mpirun --hostfile hosts.$SLURM_JOB_ID -np $SLURM_NTASKS ./lbm_mpi "$@" --out "$RUN"
echo "end: $(date '+%F %T')"
rm -f hosts.$SLURM_JOB_ID
```

**Site note:** this preserves an internal compute-network CIDR from the real deployment. Review it before publication. It may not work on other networks; top-level [`code/lbm.sbatch`](code/lbm.sbatch) is a configurable variant for reproduction.

## 5. Original video encoder — saved file `code/historical/encode.sbatch`

```bash
#!/bin/bash
#SBATCH --job-name=lbm-video
#SBATCH --ntasks=1
#SBATCH --time=00:30:00
#SBATCH --output=logs/enc-%j.out

set -e
cd "$SLURM_SUBMIT_DIR"

FF=$(command -v ffmpeg || python3 -c \
'import imageio_ffmpeg; print(imageio_ffmpeg.get_ffmpeg_exe())')

DIR="$1"

"$FF" -y -framerate 24 \
  -i "$DIR/frame_%06d.ppm" \
  -c:v libx264 -pix_fmt yuv420p \
  -crf 20 -movflags +faststart \
  "$DIR/vortex.mp4"

ls -lh "$DIR/vortex.mp4"
```

## 6. Rerunning from this GitHub layout

The top-level batch scripts use `code/` paths and include environment-variable configuration for MPI link selection:

```bash
cd 'Lattice-Boltzmann-Results'
mkdir -p logs runs
export PATH=/usr/lib64/openmpi/bin:$PATH
bash code/build.sh
bash code/benchmark.sh
bash code/run-production.sh
cat prod.jobs
```

The resulting job IDs will differ from 91–97. `code/lbm.sbatch` and `code/encode.sbatch` are the **adapted** scripts, not the identical historical scripts. To collect new per-rank and peak-process-RSS metrics, see `code/lbm-profiled.sbatch`; **the existing historical job accounting is disabled**, as documented in `logs/slurm-accounting-status.txt`.
