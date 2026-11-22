#!/bin/bash
#SBATCH --job-name=mrmpi
#SBATCH --time=01:10:00
#SBATCH --output=mrmpi-%j.out
cd ~/jobs/millerrabin
export PATH=/usr/lib64/openmpi/bin:$PATH
export LD_LIBRARY_PATH=/usr/lib64/openmpi/lib:$LD_LIBRARY_PATH
export OMPI_MCA_pml=ob1 OMPI_MCA_btl=tcp,self,vader OMPI_MCA_btl_tcp_if_include=192.168.10.0/24
scontrol show hostnames "$SLURM_JOB_NODELIST" | sed "s/\$/ slots=$SLURM_NTASKS_PER_NODE/" > hosts.$SLURM_JOB_ID
echo "job: $SLURM_JOB_ID  nodes: $SLURM_JOB_NODELIST  ntasks: $SLURM_NTASKS  tasks/node: $SLURM_NTASKS_PER_NODE  cpus/task: ${SLURM_CPUS_PER_TASK:-1}  args: $@"
echo "start: $(date '+%F %T')"
/usr/lib64/openmpi/bin/mpirun --hostfile hosts.$SLURM_JOB_ID -np $SLURM_NTASKS python3 mr_mpi.py "$@"
echo "end: $(date '+%F %T')"
rm -f hosts.$SLURM_JOB_ID
