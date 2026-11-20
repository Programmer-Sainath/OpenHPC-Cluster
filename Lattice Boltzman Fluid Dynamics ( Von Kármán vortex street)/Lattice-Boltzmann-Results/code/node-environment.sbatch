#!/usr/bin/env bash
#SBATCH --job-name=lbm-node-env
#SBATCH --nodes=4
#SBATCH --ntasks-per-node=1
#SBATCH --time=00:10:00
#SBATCH --output=logs/node-env-%j.out
set -euo pipefail
cd "$SLURM_SUBMIT_DIR"
# Run ordinary shell commands on all four allocated nodes; MPI integration is not required.
srun --mpi=none --label bash code/environment_snapshot.sh
