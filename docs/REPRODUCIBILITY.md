# Setup and reproducibility

This document explains **new runs** from a checked-out `Simulation-Workloads` branch. The archived `results.md` and `logs/` describe **historical results**, not promises of identical speed or output on another cluster.

## Shell compatibility

All `bash` code blocks and command examples in this repository target **Rocky Linux / GNU Bash**, not Windows CMD or PowerShell. SSH into the admin node before executing them. Job submissions use Slurm commands such as `sbatch`, `srun`, `squeue`, and `sacct` provided by the cluster.

## Expected environment

The November 2026 archived snapshots report Rocky Linux 9.8, Python 3.9.25, Slurm 22.05.11, Open MPI 4.1.1, and four 4-core compute nodes. See the `environment.md` files for original versions and CPU inventories. Reproduction on other clusters requires validating these dependencies rather than blindly copying machine-specific paths.

## Check first (read-only)

```bash
hostname
sinfo
squeue -u "$USER"
python3 --version
command -v mpirun && mpirun --version | head -n 1
command -v mpicc
python3 -c 'import numpy, scipy, mpi4py; print(numpy.__version__, scipy.__version__, mpi4py.__version__)'
python3 -c 'import dask, distributed; print(dask.__version__, distributed.__version__)'
```

Some jobs do not need all dependencies. The original MPI/Slurm scripts hardcode `/usr/lib64/openmpi/bin`, MPI library paths, and/or the `192.168.10.0/24` network. Verify that these settings still match your installation. Do not assume that installing `mpi4py` from PyPI automatically uses the same MPI library as the nodes.

## Python dependencies

[`../requirements.txt`](../requirements.txt) captures the versions listed in the historical MPI workload inventory for **NumPy, SciPy, Matplotlib, mpi4py, and Dask**. It also lists `scikit-image` only for the older isosurface prototype (its exact historical version was not recorded). Python packages are separate from Open MPI, compiler, Slurm, FFmpeg, and operating-system packages. Avoid installing packages globally on the lab admin node without authorization; consult the cluster environment maintainer and use compatible modules/virtual environments.

## Use the job working directories expected by the scripts

Several archived `.sbatch` files run `cd ~/jobs/<name>` before calling relative program paths. The [run recipes](RUN_RECIPES.md) copy the program and batch file to that specific location before submitting. Directly submitting an `.sbatch` file from inside a cloned repository **without** preparing its expected `~/jobs` directory may fail or run the wrong version of a script.

Keep a record with each run: `git rev-parse HEAD`, date/time and timezone, Slurm job ID, requested nodes/ranks/CPUs, stdout/stderr, Python package versions, `mpirun --version`, command arguments, and actual measured wall time. Put new experimental results in a **new, clearly named results folder**, not over the 2026 historic outputs.

## Accuracy and provenance

- **Strong scaling** compares the same computational problem across rank counts; changing problem size turns it into a different experiment.
- **Speedup** alone does not establish numerical validity. Check correctness against reference results, conservation or normalization, or explicit regression tests appropriate to each workload.
- **Probable prime** is a statistical algorithm verdict, not a primality proof.
- A video or a point-cloud plot can illustrate simulation output without providing numerical validation.
- Historical files must remain traceable to their original scripts and logs. The newly reconstructed `chud_fast.py` is intentionally labeled as a **new implementation**, not as recovered source.
