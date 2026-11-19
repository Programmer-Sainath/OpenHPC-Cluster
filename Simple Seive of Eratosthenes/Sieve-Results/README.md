# Sieve of Eratosthenes on the 4-node cluster

## What was run
A distributed version of the simple sieve of Eratosthenes (`code/sieve_mpi.py`, launched by `code/sieve_mpi.sbatch`). The odd numbers up to N are split into contiguous slices, one per MPI rank. Each rank holds its whole slice in RAM (one uint8 flag per odd number), marks the odd multiples of every prime up to sqrt(N), and counts what is left. The total is pi(N), the number of primes up to N.

## Files
- `results.md` - every job (Slurm job, nodes, MPI ranks, tasks per node, arguments), correctness checks, timings per phase, slowest and fastest rank, time per node, per-rank detail, memory and core-hours
- `environment.md` - hardware and software of the cluster when the runs were made
- `slurm_commands.md` - the sbatch commands and the sbatch file
- `code/` - source code
- `logs/` - raw output of each Slurm job
- `outputs/` - per-run files: pi(N), the largest prime up to N, each rank's slice, the last 50 primes

## Scale
The scaling runs use N = 10^10 on 1, 4 and 16 ranks. The large-scale run is N = 5x10^10 on all 16 ranks. One byte per odd number means the flags alone take N/2 bytes, which is 25 GB for N = 5x10^10. That does not fit in the 16 GB of a typical laptop as one process, but spread over the cluster's 4 nodes it does. The `Array exceeds 16 GiB as one process` column and the summed peak memory in `results.md` give the numbers. A segmented, bit-packed sieve would reach this N on a laptop in a few GB of memory, only more slowly in Python; this claim is about the simple whole-array sieve.

## Correctness
- For N = 10^k, pi(N) and the largest prime up to N are compared with published values.
- Every run also spot-checks 20,000 random numbers per rank and the last 2,000 of each slice against deterministic Miller-Rabin (exact below 3.3x10^24). The N = 5x10^10 run has no reference value and relies on this spot-check.

## Notes
- Timestamps in `logs/` are UTC (the node clocks); the head node shows local time (UTC+3).
- Core-hours = MPI ranks x wall time. Each configuration was run once.
