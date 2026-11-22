# Known limitations and follow-up work

This checklist distinguishes **documented facts**, **unrecovered source/evidence**, and **new improvements**. It is based on the simulation archive reviewed on 23 November 2026; the live branch may have changed afterward.

## High priority — historical reproducibility

- [ ] **Recover original π binary-splitting program.** Historical `slurm_commands.md` executes `chud_fast.py`, but that original program was missing from the supplied snapshot. A newly written program now exists under that name for **new work only**; it cannot establish historic byte-for-byte source provenance.
- [ ] **Recover original Chudnovsky Slurm stdout.** Digit files include job metadata, but the original `chud-*.out` logs were not supplied.
- [ ] **Preserve historical submission provenance.** Sieve and Miller–Rabin `slurm_commands.md` now give runnable *equivalent* allocations (`-N1/-N4` etc.) rather than invalid parenthetical shell annotations. Original `--dependency=afterany` chains were not independently recovered; do not treat the reconstructed command text as an exact terminal transcript.
- [ ] **Validate site-specific launchers.** Multiple `.sbatch` scripts hardcode `/usr/lib64/openmpi/`, `~/jobs/<name>`, and the `192.168.10.0/24` MPI NIC selector. Confirm these are correct for current nodes before rerunning.

## Code cleanup separate from documented benchmark

- [x] **Preserve mixed theory/code drafts as documentation.** The two invalid historical `.py` drafts have been converted into fenced-text `.md` archival documents with their contents retained. Run the actual programs in the corresponding `*-Results/code/` directories.
- [x] **Remove misleading orbital `SystemError` claim.** Referencing built-in `SystemError` alone was harmless, not a raised exception. The line was removed for clarity. Three orbital prototypes now support the recorded SciPy 1.13 environment and save plots instead of requiring a GUI. They have not been rerun across MPI nodes.
- [x] **Review Dask development prototype.** `Dask Primility.py` now calls `main()` when executed and uses `pure=False` for independent tasks; it remains unbenchmarked. The benchmark `dask_local.py` now stops on failed candidate verification.
- [ ] **Document Python/C package versions for each independent run.** The current `requirements.txt` reflects only versions actually listed in archived snapshots and is not a full transitive lockfile.

## Existing-code fixes applied (new code, not historical reruns)

- [x] LBM frame-equivalence script now rejects missing/empty/mismatched frame sets before issuing a PASS.
- [x] Sieve and Miller–Rabin Slurm recipes now contain executable Linux Bash allocations.
- [x] Miller–Rabin new-run batch time limit increased to allow overhead above 2,400-second search budgets.
- [x] LBM Windows-only transfer example removed; hardware descriptions now separate observed link speeds from reported switch model.
- [ ] **Still unverified on real cluster:** runtime behavior of repaired prototypes and new-run Slurm scripts. Historical logs and figures are unchanged.

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
