#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
if ! command -v mpicc >/dev/null 2>&1; then
  echo "ERROR: mpicc not on PATH. Load your cluster's OpenMPI module first (module avail; module load <name>)." >&2
  exit 1
fi
mpicc -O3 -std=c11 -Wall -Wextra -pedantic -o lbm_mpi lbm_mpi.c -lm
printf 'Built %s/lbm_mpi with %s\n' "$PWD" "$(command -v mpicc)"
