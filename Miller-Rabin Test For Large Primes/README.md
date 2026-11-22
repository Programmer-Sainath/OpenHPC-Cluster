# Miller–Rabin primality testing — MPI

## Objective

Study probabilistic primality testing and parallel computing by splitting **Miller–Rabin witness rounds** across MPI ranks or allowing each rank to independently search for probable primes of a specified bit length.

The **recorded** program is [`Miller-Rabin-Results/code/mr_mpi.py`](Miller-Rabin-Results/code/mr_mpi.py), executed via [`mr_mpi.sbatch`](Miller-Rabin-Results/code/mr_mpi.sbatch). Older files in this directory contain prototypes, trial benchmarks, and notes, which are not necessarily runnable versions of the final MPI workload.

## Two execution modes

1. **`mersenne <rounds> <cases>`:** ranks share witness checks of known Mersenne prime candidates and deliberately composite controls. This measures the parallelization of checking the same integer.
2. **`search <bits> <seconds>`:** each rank searches for random probable primes within a fixed time budget. The natural metric here is total candidate-throughput, not latency for a single fixed integer.

**Probable-prime is not the same as a mathematical primality certificate.** The benchmark uses known truth values for selected Mersenne cases to check its implementation.

## Recorded experiments

- Slurm jobs **74–76** compare 1, 4, and 16 ranks on shared known 4,423-, 9,689-, and 11,213-bit Mersenne examples and composite controls.
- Jobs **77** and **82** cover larger known-number cases, including **M86243**.
- Jobs **78–81** and **83** test 2,048-/4,096-bit probable-prime searches.
- The archive reports **18.38 total core-hours** across these jobs. A separate result table records per-rank timing, memory, and generated candidates.

Sources: [`results.md`](Miller-Rabin-Results/results.md), [`logs/`](Miller-Rabin-Results/logs/), [`primes/`](Miller-Rabin-Results/primes/), and [`environment.md`](Miller-Rabin-Results/environment.md).

## Run a small new experiment

```bash
REPO="$(git rev-parse --show-toplevel)"
mkdir -p "$HOME/jobs/millerrabin"
cp "$REPO/Miller-Rabin Test For Large Primes/Miller-Rabin-Results/code/"{mr_mpi.py,mr_mpi.sbatch} "$HOME/jobs/millerrabin/"
cd "$HOME/jobs/millerrabin"
sbatch -N1 --ntasks-per-node=4 mr_mpi.sbatch mersenne 16 M4423,M9689
# A separate candidate-search experiment:
sbatch -N1 --ntasks-per-node=4 mr_mpi.sbatch search 2048 60
```

The historical submission notes now provide **runnable Linux Bash equivalents** with the intended rank counts. They are reconstructions rather than proof of the exact historical submission syntax or dependency order. See [run recipes](../docs/RUN_RECIPES.md).

The batch file assumes the lab's Open MPI installation and its 192.168.10.0/24 interface. Run only after confirming the MPI environment on the current nodes.

## Limits of evidence

Each configuration was recorded once; randomness affects searches, and composite early exits make witness-splitting timings incomparable to always-prime cases. Core-hour extrapolations are estimates. Keep raw logs linked to any published performance figures. The old mixed draft is preserved as [historical notes](<Miller-Rabin Test For large primes - CODE.md>); the validated benchmark entry point is `mr_mpi.py` above.
