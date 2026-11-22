# Distributed sieve of Eratosthenes — MPI

## Objective

Count primes \(\pi(N)\) up to a specified bound using a **distributed odd-number sieve of Eratosthenes**. Each rank stores and marks a contiguous subset of the odd-number flags in a NumPy `uint8` array, allowing a whole-array sieve larger than the memory of a single compute node.

The recorded implementation is [`Sieve-Results/code/sieve_mpi.py`](Sieve-Results/code/sieve_mpi.py), with launcher [`sieve_mpi.sbatch`](Sieve-Results/code/sieve_mpi.sbatch).

## Archived results

| Search bound | MPI ranks | Nodes | Reported π(N) | Recorded compute wall time |
|---:|---:|---:|---:|---:|
| 10,000,000,000 | 1 | 1 | 455,052,511 | 55.8 s |
| 10,000,000,000 | 4 | 1 | 455,052,511 | 50.9 s |
| 10,000,000,000 | 16 | 4 | 455,052,511 | 13.1 s |
| 50,000,000,000 | 16 | 4 | 2,119,654,578 | 68.9 s |

The 10-billion bound matches the published reference value. The 50-billion bound was recorded with **352,000 randomized/boundary spot-checks** and zero mismatches, but the archived report lists *no independent published reference* for that result. Do not label it independently reference-verified.

At 50 billion, the boolean flag storage alone was about **23.28 GiB total**, distributed across 16 ranks; the archived sum of per-process peak resident memory is **23.97 GiB**. The memory comparison is specifically for this whole-array **one-byte-per-odd-number** implementation, **not** a claim that a memory-efficient segmented/bit-packed sieve cannot run on one machine.

## Run a smaller new experiment

```bash
REPO="$(git rev-parse --show-toplevel)"
mkdir -p "$HOME/jobs/sieve"
cp "$REPO/Simple Seive of Eratosthenes/Sieve-Results/code/"{sieve_mpi.py,sieve_mpi.sbatch} "$HOME/jobs/sieve/"
cd "$HOME/jobs/sieve"
sbatch -N1 --ntasks-per-node=4 sieve_mpi.sbatch 1e8
# Original 10-billion comparison once resources are available:
# sbatch -N4 --ntasks-per-node=4 sieve_mpi.sbatch 1e10
```

The historical [`slurm_commands.md`](Sieve-Results/slurm_commands.md) embeds `(total ranks ...)` explanatory annotations in its sample commands; those annotations are **not executable**. The corrected recipes in [docs/RUN_RECIPES.md](../docs/RUN_RECIPES.md) show proper `-N` and `--ntasks-per-node` options.

## Evidence and limitations

[Results and per-rank profiles](Sieve-Results/results.md) · [Environment](Sieve-Results/environment.md) · [Raw Slurm logs](Sieve-Results/logs/) · [Output summaries](Sieve-Results/outputs/)

Performance varied between a one-node four-rank allocation and a four-node sixteen-rank allocation. Each original configuration was run **once**, so these are measurements, not confidence intervals. The scripts use a lab-specific Open MPI path and network selector; review those settings before applying them elsewhere.
