#!/bin/bash
#SBATCH --job-name=orb2
#SBATCH --time=00:30:00
#SBATCH --output=orb2-%j.out
cd ~/jobs/orbital
export PATH=/usr/lib64/openmpi/bin:$PATH
export LD_LIBRARY_PATH=/usr/lib64/openmpi/lib:$LD_LIBRARY_PATH
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
export OMPI_MCA_pml=ob1 OMPI_MCA_btl=tcp,self,vader OMPI_MCA_btl_tcp_if_include=192.168.10.0/24
scontrol show hostnames "$SLURM_JOB_NODELIST" | sed "s/\$/ slots=$SLURM_NTASKS_PER_NODE/" > hosts.$SLURM_JOB_ID
echo "nodes: $SLURM_JOB_NODELIST  ranks: $SLURM_NTASKS  args: $@"
/usr/lib64/openmpi/bin/mpirun --hostfile hosts.$SLURM_JOB_ID -np $SLURM_NTASKS python3 orbital2.py "$@"
rm -f hosts.$SLURM_JOB_ID
