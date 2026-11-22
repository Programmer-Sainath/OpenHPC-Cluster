# Slurm jobs — reproducible Linux Bash submission equivalents

The four archived jobs were run sequentially using `--dependency=afterany`. The commands below reconstruct their allocations and arguments in executable Bash; their historical dependency job IDs were not retained here. **Do not submit all large jobs indiscriminately.**

```bash
# job 87
sbatch -N1 --ntasks-per-node=1 sieve_mpi.sbatch 1e10
# job 88
sbatch -N1 --ntasks-per-node=4 sieve_mpi.sbatch 1e10
# job 89
sbatch -N4 --ntasks-per-node=4 sieve_mpi.sbatch 1e10
# job 90
sbatch -N4 --ntasks-per-node=4 sieve_mpi.sbatch 5e10
```

Current new-run launcher (`sieve_mpi.sbatch`):

```bash
#!/bin/bash
#SBATCH --job-name=sieve
#SBATCH --time=01:00:00
#SBATCH --output=sieve-%j.out
cd ~/jobs/sieve
export PATH=/usr/lib64/openmpi/bin:$PATH
export LD_LIBRARY_PATH=/usr/lib64/openmpi/lib:$LD_LIBRARY_PATH
export OMPI_MCA_pml=ob1 OMPI_MCA_btl=tcp,self,vader OMPI_MCA_btl_tcp_if_include=192.168.10.0/24
scontrol show hostnames "$SLURM_JOB_NODELIST" | sed "s/\$/ slots=$SLURM_NTASKS_PER_NODE/" > hosts.$SLURM_JOB_ID
echo "job: $SLURM_JOB_ID  nodes: $SLURM_JOB_NODELIST  ntasks: $SLURM_NTASKS  tasks/node: $SLURM_NTASKS_PER_NODE  cpus/task: ${SLURM_CPUS_PER_TASK:-1}  args: $@"
echo "start: $(date '+%F %T')"
/usr/lib64/openmpi/bin/mpirun --hostfile hosts.$SLURM_JOB_ID -np $SLURM_NTASKS python3 sieve_mpi.py "$@"
echo "end: $(date '+%F %T')"
rm -f hosts.$SLURM_JOB_ID
```
