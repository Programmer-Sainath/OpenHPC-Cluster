#!/bin/bash
#SBATCH --job-name=dask1
#SBATCH -N1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --time=00:30:00
#SBATCH --output=dask1-%j.out
cd ~/jobs/dask
echo "node: $(hostname)"
for W in 1 2 4; do python3 dask_local.py $W 10 0; done
python3 dask_local.py 4 10 1
