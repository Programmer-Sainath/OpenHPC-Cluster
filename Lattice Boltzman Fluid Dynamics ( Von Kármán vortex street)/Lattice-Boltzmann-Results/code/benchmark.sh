#!/usr/bin/env bash
# Three sequential, identical-workload comparisons: 1, 4, 16 MPI ranks.
set -euo pipefail
mkdir -p logs runs
BM=(--nx 3072 --ny 1024 --diameter 128 --re 120 --steps 4000 \
    --start-snapshot 4001 --snapshot-every 1000 --stride 4 --log-every 1000)
: > bench.list
prev=''
for spec in 'bench1 1 1' 'bench4 1 4' 'bench16 4 4'; do
  read -r tag nodes per_node <<< "$spec"
  dep=()
  [[ -n "$prev" ]] && dep=(--dependency="afterany:$prev")
  prev=$(LBM_TAG="$tag" sbatch --parsable "${dep[@]}" -N"$nodes" \
    --ntasks-per-node="$per_node" code/lbm.sbatch "${BM[@]}")
  printf '%s %s\n' "$tag" "$prev" >> bench.list
  echo "Submitted $tag as $prev"
done
