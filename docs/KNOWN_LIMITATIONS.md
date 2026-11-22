# Known limitations and follow-up work

This checklist distinguishes **documented facts**, **unrecovered source/evidence**, and **new improvements**. It is based on the simulation archive reviewed on 23 November 2026; the live branch may have changed afterward.

## High priority — historical reproducibility

- [ ] **Recover original π binary-splitting program.** Historical `slurm_commands.md` executes `chud_fast.py`, but that original program was missing from the supplied snapshot. A newly written program now exists under that name for **new work only**; it cannot establish historic byte-for-byte source provenance.
- [ ] **Recover original Chudnovsky Slurm stdout.** Digit files include job metadata, but the original `chud-*.out` logs were not supplied.
- [ ] **Retain exact command provenance.** Historical `slurm_commands.md` in the sieve and Miller–Rabin folders embeds `(total ranks ...)` as text on shell command lines. The actual executable form must use `-N1/-N4` plus `--ntasks-per-node` (see [`RUN_RECIPES.md`](RUN_RECIPES.md)). Do not silently rewrite history without documenting the correction.
- [ ] **Validate site-specific launchers.** Multiple `.sbatch` scripts hardcode `/usr/lib64/openmpi/`, `~/jobs/<name>`, and the `192.168.10.0/24` MPI NIC selector. Confirm these are correct for current nodes before rerunning.

## Code cleanup separate from documented benchmark

- [ ] **Archive mixed code/theory prototype correctly.** `Miller-Rabin Test For large primes - CODE.py` and `Simple sieve of Eratosthenes in python-Theory and Code.py` contain non-executable note text. Keep the historical content, but consider renaming or splitting into `.md` and clean `.py` versions. The working benchmark programs are in each `*-Results/code/` directory.
- [ ] **Repair unbenchmarked orbital prototype.** `or_mpi4py_vertices.py` contains an accidental standalone `SystemError` name near the top. Do not count it as a working benchmark until edited and tested.
- [ ] **Review Dask development prototype.** `Dask Primility.py` defines `main()` but does not call it; the archived workload was run from `dask_local.py`, not that prototype.
- [ ] **Document Python/C package versions for each independent run.** The current `requirements.txt` reflects only versions actually listed in archived snapshots and is not a full transitive lockfile.

## Stronger science and benchmarking

- [ ] **LBM:** estimate shedding frequency/Strouhal number, validate against an appropriate reference case, and measure grid/time-step convergence. Video is qualitative evidence, not quantitative validation.
- [ ] **MPI scaling:** repeat each configuration multiple times; state noise and variability, allocation, and the exact problem held fixed.
- [ ] **Hydrogen orbitals:** provide derivation of the importance-sampling estimator and uncertainty estimates; compare additional quantum numbers against analytic normalization/radial expectation.
- [ ] **Miller–Rabin and Dask:** explicitly distinguish *probable-prime* outputs from proven primes; re-run randomized throughput trials to quantify uncertainty.
- [ ] **Sieve:** independently validate the 50-billion prime count if a trusted reference becomes available; existing source records 352k spot checks but no independent reference.
- [ ] **Chudnovsky:** independently validate generated digits rather than comparing only shared prefixes of files from the same code path.

## Presentation and maintenance

- [ ] Agree with the project team on **workload-specific authorship credits** instead of inferring them from filenames. The project-wide roles are documented on the infrastructure branch.
- [ ] Consider correcting historical folder spellings in a separate `git mv` commit after updating all relative links; this patch intentionally preserves folder paths to avoid broken links.
- [ ] Keep new logs, huge generated images, and binary artifacts out of routine commits unless explicitly selected as evidence.
- [ ] Add tests and CI checks once the archived notebook-like `.py` prototypes are separated from runnable benchmark code.
