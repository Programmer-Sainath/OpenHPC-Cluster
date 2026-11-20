#!/usr/bin/env bash
#SBATCH --job-name=lbm
#SBATCH --time=02:00:00
#SBATCH --output=logs/lbm-%j.out
set -euo pipefail
cd "$SLURM_SUBMIT_DIR"
export PATH=/usr/lib64/openmpi/bin:$PATH
export LD_LIBRARY_PATH=/usr/lib64/openmpi/lib:${LD_LIBRARY_PATH:-}
export OMP_NUM_THREADS=1
export OMPI_MCA_pml=ob1
export OMPI_MCA_btl=tcp,self,vader
# If the cluster has multiple NICs, set MPI_LAN_CIDR to the dedicated compute-network subnet
# when submitting (e.g. MPI_LAN_CIDR=192.168.x.0/24 sbatch ...).
if [[ -n "${MPI_LAN_CIDR:-}" ]]; then
  export OMPI_MCA_btl_tcp_if_include="$MPI_LAN_CIDR"
fi
TAG=${LBM_TAG:-run}
RUN="runs/${TAG}-${SLURM_JOB_ID}"
mkdir -p "$RUN"
HOSTFILE="hosts.${SLURM_JOB_ID}"
trap 'rm -f "$HOSTFILE"' EXIT
SLOTS="${SLURM_NTASKS_PER_NODE:-4}"
# Reconstruct an OpenMPI hostfile for this specific homogeneous 4-core/node cluster.
# For mixed-node allocations, replace SLOTS with per-node allocations.
scontrol show hostnames "$SLURM_JOB_NODELIST" | awk -v slots="$SLOTS" '{print $1 " slots=" slots}' > "$HOSTFILE"
echo "job: $SLURM_JOB_ID nodes: $SLURM_JOB_NODELIST ntasks: $SLURM_NTASKS tasks/node: $SLOTS tag: $TAG args: $*"
echo "start: $(date '+%F %T')"
/usr/lib64/openmpi/bin/mpirun --hostfile "$HOSTFILE" -np "$SLURM_NTASKS" ./lbm_mpi "$@" --out "$RUN"
echo "end: $(date '+%F %T')"
