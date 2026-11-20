# C/MPI code and Slurm scripts

## Verified original files from the Rocky Linux admin node

The historical files in [`historical/`](historical/) were copied directly from `/home/hpc/jobs/lbm/lbm_mpi_vortex` in the evidence archive. Those are the **exact original-run** scripts and source:

- `historical/lbm_mpi.c` — the solver used for jobs 91–96.
- `historical/lbm.sbatch` — MPI/Slurm launcher used for these jobs; retains its site-specific MPI network selector.
- `historical/encode.sbatch` — encoder used for job 97.
- `historical/build.sh` — original build instructions.

The top-level `lbm_mpi.c` is byte-for-byte identical to the historical source. Top-level `lbm.sbatch`/`encode.sbatch`/`build.sh` are **adapted for the nested GitHub results-folder layout** and may need site-specific configuration. Do not represent them as identical to the original cluster scripts.

## Reproduction (new jobs, not historic jobs)

From the parent `Lattice-Boltzmann-Results/` directory:

```bash
mkdir -p logs runs
export PATH=/usr/lib64/openmpi/bin:$PATH
bash code/build.sh
bash code/benchmark.sh
bash code/run-production.sh
```

Additional utilities:

- `environment_snapshot.sh`, `node-environment.sbatch`: fresh node inventories.
- `collect_evidence.sh`: refreshes old logs, if desired; complete logs from 91–97 are **already archived**.
- `check-frame-equivalence.sh`: compares images for new small parallel equivalence tests.
- `lbm-profiled.sbatch`, `profile_rank.sh`, `summarize_profile.py`: produce per-rank execution time and per-process maximum RSS for **new, separately identified profiling jobs** only. These values were not recorded in the original jobs.

`/usr/bin/time` must exist on compute nodes for the optional profiler. Verify first if needed. The profiling scripts use MPI over a Slurm node allocation and shared storage. Do not treat sums of separate processes' peak RSS values as a measured simultaneous node-level memory peak.
