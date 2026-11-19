# Miller-Rabin primality tests on the 4-node cluster

## What was run
- The repo's `miller_rabin(n, k)` function, unchanged, wrapped in an MPI program (`code/mr_mpi.py`, launched by `code/mr_mpi.sbatch`).
- **mersenne mode:** tests very large numbers whose answer is known. Mersenne primes must come out "probably prime"; products of two Mersenne primes are composite. The 16 Miller-Rabin rounds for each number are split evenly across the MPI ranks, so all ranks work on the same number at once.
- **search mode:** every rank independently searches for random probable primes of a given bit size for a fixed time budget. Each prime is re-checked afterwards. Primes found per minute measures throughput at 1, 4 and 16 ranks.

## Files
- `results.md` - every job (Slurm job, nodes, MPI ranks, tasks per node, arguments) and every result, with wall time, slowest and fastest rank, time per node, per-rank detail and peak memory
- `environment.md` - hardware and software of the cluster when the runs were made
- `slurm_commands.md` - the exact sbatch commands and the sbatch file
- `code/` - source code (`mr_mpi.py`, `mr_mpi.sbatch`, `collect_env.sh`)
- `logs/` - raw output of each Slurm job
- `primes/` - the primes found, with the time, ranks and nodes in a header above them

## Notes
- A "composite" verdict is certain. A "probably prime" verdict from k rounds is wrong with probability at most 4^-k (16 rounds in the witness-split tests, 20 per candidate in the search). Because the Mersenne numbers have known answers, every verdict in section 1 and 2 is checked against the truth (the `Correct` column).
- For composite numbers one failing round is enough, so they do not speed up with more ranks. For primes all rounds must run, so they split well.
- This workload is CPU-bound. Peak memory per rank is listed in `results.md` and is small, so the cluster helps here through cores, not memory.
- Random seeds are fixed per rank (1000003 x (rank + 1)). Each configuration was run once.
