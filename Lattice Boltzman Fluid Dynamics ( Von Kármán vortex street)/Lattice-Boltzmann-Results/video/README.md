# Original production MP4 — job 96 + encoder job 97

**Simulation sample times:** 289 frames from lattice steps **8,000 through 80,000**, every 250 simulation steps. **MPI configuration:** 16 ranks across four compute nodes (`node01–04`, four ranks/node). **Solver wall time:** 897.84 s. **Job 97's encoder wall time:** not logged.

**Result:** [`vortex.mp4`](vortex.mp4) — original H.264 clip, resolution **1024×384**, **24 FPS**, **12.04 seconds** of presentation time (not physical time). The original video was preserved byte-for-byte, with SHA-256 documented in `data/asset-checksums.sha256`.

The visualization colors represent opposite signs of vorticity. Quantitative vortex shedding rate and grid-independence have not yet been validated. This is a genuine four-node simulation output, **not** footage of the optional unexecuted larger workload.
