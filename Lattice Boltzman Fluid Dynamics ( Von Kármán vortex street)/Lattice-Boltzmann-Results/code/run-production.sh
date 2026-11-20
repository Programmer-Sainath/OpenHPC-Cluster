#!/usr/bin/env bash
# Run from the project root after building and confirming the correctness test.
set -euo pipefail
mkdir -p logs runs
# Set MPI_LAN_CIDR if your OpenMPI installation needs explicit NIC selection.
PJ=$(LBM_TAG=prod sbatch --parsable --time=02:00:00 -N4 --ntasks-per-node=4 code/lbm.sbatch \
  --nx 2048 --ny 768 --diameter 96 --re 120 --steps 80000 \
  --snapshot-every 250 --start-snapshot 8000 --stride 2 --log-every 1000)
EJ=$(sbatch --parsable --dependency=afterok:"$PJ" code/encode.sbatch "runs/prod-$PJ" 24)
echo "$PJ $EJ" > prod.jobs
echo "Production job: $PJ; encoder job: $EJ"
echo "Check: squeue -j $PJ,$EJ"
echo "Video path after successful completion: runs/prod-$PJ/vortex.mp4"
