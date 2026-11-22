# Executable Slurm run recipes

Use these for **new submissions**, after checking the [environment and required working paths](REPRODUCIBILITY.md). These examples do not replicate exact historic job IDs or every historic command line. All commands assume you are initially **at the root of the checked-out `Simulation-Workloads` branch** in a Linux Bash shell on the admin node. Use a small run first; large jobs must fit the cluster's current allocations.

## 1. MPI sieve (small sanity check)

```bash
REPO="$(pwd)"
mkdir -p "$HOME/jobs/sieve"
cp "$REPO/Simple Seive of Eratosthenes/Sieve-Results/code/"{sieve_mpi.py,sieve_mpi.sbatch} "$HOME/jobs/sieve/"
cd "$HOME/jobs/sieve"
sbatch -N1 --ntasks-per-node=4 sieve_mpi.sbatch 1e8
```

## 2. MPI Miller–Rabin (known cases)

```bash
REPO="$(git rev-parse --show-toplevel)"
mkdir -p "$HOME/jobs/millerrabin"
cp "$REPO/Miller-Rabin Test For Large Primes/Miller-Rabin-Results/code/"{mr_mpi.py,mr_mpi.sbatch} "$HOME/jobs/millerrabin/"
cd "$HOME/jobs/millerrabin"
sbatch -N1 --ntasks-per-node=4 mr_mpi.sbatch mersenne 16 M4423,M9689
```

## 3. Hydrogen orbital sampling (small)

```bash
REPO="$(git rev-parse --show-toplevel)"
mkdir -p "$HOME/jobs/orbital"
cp "$REPO/Hydrogen Orbiatal Simulations/Hydrogen-Orbital-Results/code/"{orbital2.py,orbital2.sbatch} "$HOME/jobs/orbital/"
cd "$HOME/jobs/orbital"
sbatch -N1 --ntasks-per-node=4 orbital2.sbatch 4 3 -3 1000000 0.001
```

## 4. Single-node Dask benchmark

```bash
REPO="$(git rev-parse --show-toplevel)"
mkdir -p "$HOME/jobs/dask"
cp "$REPO/Dask Primility/Dask-Primility-Results/code/"{dask_local.py,dask1.sbatch} "$HOME/jobs/dask/"
cd "$HOME/jobs/dask"
sbatch dask1.sbatch
```

## 5. Single-core π calculation — newly reconstructed implementation

```bash
REPO="$(git rev-parse --show-toplevel)"
mkdir -p "$HOME/jobs/chud"
cp "$REPO/Chudnovsky's Pi Calculation/chud_fast.py" "$HOME/jobs/chud/"
cd "$HOME/jobs/chud"
python3 chud_fast.py 1000
sbatch -N1 --ntasks=1 --job-name=chud1000 --output=chud-1000-%j.out \
  --wrap='cd "$HOME/jobs/chud" && python3 chud_fast.py 1000'
```

The original binary-splitting program was missing from the archive; the new one is not historically identical and must not be cited as the original source.

## 6. LBM — documented production workflow

The LBM folder already includes carefully maintained scripts with parameters and provenance. Follow [its solver build documentation](<../Lattice Boltzman Fluid Dynamics ( Von Kármán vortex street)/Lattice-Boltzmann-Results/code/README.md>), especially the guidance to test small jobs before production. From the folder `Lattice-Boltzmann-Results/`:

```bash
export PATH=/usr/lib64/openmpi/bin:$PATH
bash code/build.sh
bash code/benchmark.sh
```

`code/benchmark.sh` submits **the large original-format 3072×1024×4000 comparison** across 1/4/16 ranks; do not run it as an initial smoke test. If you only want a smoke test, use the small-case commands provided in the existing LBM `slurm_commands.md` after reading their arguments and verifying the node environment.

## Checking jobs

```bash
squeue -u "$USER"
# Replace 1234 with the numeric Slurm job ID returned by sbatch.
sacct -j 1234 --format=JobID,State,Elapsed,MaxRSS  # only if accounting is enabled
```

No `sudo`, cluster service changes, or Warewulf image modifications are needed for these documentation updates.
