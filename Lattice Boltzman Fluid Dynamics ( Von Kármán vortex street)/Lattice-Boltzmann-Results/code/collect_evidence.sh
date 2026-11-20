#!/usr/bin/env bash
# Run on the cluster from Lattice-Boltzmann-Results/, after copying this package there.
# Usage: bash code/collect_evidence.sh ~/jobs/lbm/lbm_mpi_vortex
# Copies actual raw job logs (if present) and Slurm accounting; never fabricates records.
set -euo pipefail
cd "$(dirname "$0")/.."
SRC=${1:-$HOME/jobs/lbm/lbm_mpi_vortex}
if [[ ! -d "$SRC" ]]; then echo "Source directory not found: $SRC" >&2; exit 1; fi
mkdir -p logs
for id in 91 92 93 94 95 96; do
    file="$SRC/logs/lbm-$id.out"
    if [[ -f "$file" ]]; then cp -p "$file" "logs/lbm-$id.out"; echo "Copied $file"; else echo "Missing $file (not invented)"; fi
done
file="$SRC/logs/enc-97.out"
if [[ -f "$file" ]]; then cp -p "$file" logs/enc-97.out; echo "Copied $file"; else echo "Missing $file"; fi
for pattern in 'logs/eq*.out' 'logs/lbm-*.err'; do
    : # Include additional files manually after reviewing for secrets.
done
if command -v sacct >/dev/null; then
    sacct -P -j 93,94,95,96,97 \
       --format=JobID,JobName,Partition,AllocNodes,NTasks,Elapsed,CPUTime,TotalCPU,MaxRSS,MaxVMSize,State,ExitCode \
       > logs/slurm_accounting_93-97.psv 2> logs/slurm_accounting_error.txt || true
    echo 'Saved accounting output; fields may be empty if accounting is disabled or records expired.'
else echo 'sacct unavailable'; fi
bash code/environment_snapshot.sh > logs/admin_environment.txt 2>&1 || true
printf '\nReview logs before uploading to a public GitHub repository for sensitive hostnames, IPs, accounts or paths.\n'
