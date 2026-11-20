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
