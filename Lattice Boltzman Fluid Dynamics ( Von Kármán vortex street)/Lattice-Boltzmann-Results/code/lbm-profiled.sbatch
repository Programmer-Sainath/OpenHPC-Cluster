#!/usr/bin/env bash
#SBATCH --job-name=lbm-profile
#SBATCH --time=02:00:00
#SBATCH --output=logs/lbm-profile-%j.out
# Run ONLY for a new experiment; cannot add missing metrics to old jobs.
set -euo pipefail
cd "$SLURM_SUBMIT_DIR"
export PATH=/usr/lib64/openmpi/bin:$PATH
export LD_LIBRARY_PATH=/usr/lib64/openmpi/lib:${LD_LIBRARY_PATH:-}
export OMP_NUM_THREADS=1
export OMPI_MCA_pml=ob1 OMPI_MCA_btl=tcp,self,vader
if [[ -n "${MPI_LAN_CIDR:-}" ]]; then export OMPI_MCA_btl_tcp_if_include="$MPI_LAN_CIDR"; fi
RUN="runs/profile-${SLURM_JOB_ID}"
mkdir -p "$RUN"
HOSTFILE="hosts.${SLURM_JOB_ID}"
trap 'rm -f "$HOSTFILE"' EXIT
slots=${SLURM_NTASKS_PER_NODE:-4}
scontrol show hostnames "$SLURM_JOB_NODELIST" | awk -v slots="$slots" '{print $1 " slots=" slots}' > "$HOSTFILE"
/usr/lib64/openmpi/bin/mpirun --hostfile "$HOSTFILE" -np "$SLURM_NTASKS" \
    bash "$SLURM_SUBMIT_DIR/code/profile_rank.sh" "$RUN" ./lbm_mpi "$@" --out "$RUN"
python3 code/summarize_profile.py "$RUN"
