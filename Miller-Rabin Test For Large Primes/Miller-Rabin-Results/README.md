# Miller-Rabin primality tests on the 4-node cluster

## What was run
- The repo's `miller_rabin(n, k)` function, unchanged, wrapped in an MPI program (`code/mr_mpi.py`, launched by `code/mr_mpi.sbatch`).
- **mersenne mode:** tests very large numbers whose answer is known. Mersenne primes must come out "probably prime"; products of two Mersenne primes are composite. The 16 Miller-Rabin rounds for each number are split evenly across the MPI ranks, so all ranks work on the same number at once.
- **search mode:** every rank independently searches for random probable primes of a given bit size for a fixed time budget. Each prime is re-checked afterwards. Primes found per minute measures throughput.

## Files
- `results.md` - every job (Slurm job, nodes, MPI ranks, tasks per node, arguments) and every result, with wall time, slowest and fastest rank, time per node, per-rank detail, core-hours and peak memory
- `environment.md` - hardware and software of the cluster when the runs were made
- `slurm_commands.md` - the sbatch commands and the sbatch file
- `code/` - source code
- `logs/` - raw output of each Slurm job
- `primes/` - the primes found, with the time, ranks and nodes in a header above them

## Scale
Sections 1-3 of `results.md` are small runs that measure speedup at 1, 4 and 16 ranks. Section 4 is the large-scale tier, run on all 16 ranks. This workload is CPU-bound, so scale is measured in core-hours, not memory (peak memory per rank is small and listed in `results.md`). The "Est. hours on 8 cores" column assumes perfect scaling and the same per-core speed as these nodes; a modern laptop core may be faster, so treat it as an order-of-magnitude comparison. Core-hours are the measured quantity.

## Notes
- A "composite" verdict is certain. A "probably prime" verdict from k rounds is wrong with probability at most 4^-k. Known Mersenne primes are used so every verdict is checked against the truth (the `Correct` column).
- For composite numbers one failing round is enough, so they do not speed up with more ranks. For primes all rounds must run, so they split well.
- Random seeds are fixed per rank (1000003 x (rank + 1)). Each configuration was run once.
- Timestamps in `logs/` are UTC (the node clocks); the head node shows local time (UTC+3).
- Core-hours = MPI ranks x wall time of the job, an upper bound when ranks finish at different times.
- Scale note: this workload is CPU-bound, so the large runs take hours on a laptop's cores rather than being impossible there. For example, testing M86243 takes 16 Miller-Rabin rounds of about 1413 s each (one per rank here), about 6.3 core-hours in total, which took 23.6 minutes of wall time on 16 ranks. Peak memory was 27 MB per rank.
