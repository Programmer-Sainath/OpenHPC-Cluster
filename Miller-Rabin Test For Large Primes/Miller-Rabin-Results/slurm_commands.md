# Slurm commands used

Ten jobs, chained with --dependency=afterany so they never ran at the same time.

```bash
# job 74
sbatch --ntasks-per-node=1 (total ranks 1) mr_mpi.sbatch mersenne 16 M4423,M9689,M11213,C4253x4423
# job 75
sbatch --ntasks-per-node=4 (total ranks 4) mr_mpi.sbatch mersenne 16 M4423,M9689,M11213,C4253x4423
# job 76
sbatch --ntasks-per-node=4 (total ranks 16) mr_mpi.sbatch mersenne 16 M4423,M9689,M11213,C4253x4423
# job 77
sbatch --ntasks-per-node=4 (total ranks 16) mr_mpi.sbatch mersenne 16 M19937,M21701,M23209,C9941x11213
# job 78
sbatch --ntasks-per-node=1 (total ranks 1) mr_mpi.sbatch search 2048 60
# job 79
sbatch --ntasks-per-node=4 (total ranks 4) mr_mpi.sbatch search 2048 60
# job 80
sbatch --ntasks-per-node=4 (total ranks 16) mr_mpi.sbatch search 2048 60
# job 81
sbatch --ntasks-per-node=4 (total ranks 16) mr_mpi.sbatch search 4096 120
# job 82
sbatch --ntasks-per-node=4 (total ranks 16) mr_mpi.sbatch mersenne 16 M86243
# job 83
sbatch --ntasks-per-node=4 (total ranks 16) mr_mpi.sbatch search 4096 2400
```

Contents of mr_mpi.sbatch:

```bash
#!/bin/bash
#SBATCH --job-name=mrmpi
#SBATCH --time=00:40:00
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
```
