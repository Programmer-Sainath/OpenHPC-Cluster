#!/usr/bin/env bash
# Run from the Lattice-Boltzmann-Results/ directory.
set -euo pipefail
cd "$(dirname "$0")/.."
if ! command -v mpicc >/dev/null 2>&1; then
    echo 'mpicc not found; load the Open MPI environment first' >&2
    exit 1
fi
mpicc -O3 -std=c11 -Wall -Wextra -pedantic -o lbm_mpi code/lbm_mpi.c -lm
echo "Built $PWD/lbm_mpi with $(command -v mpicc)"
