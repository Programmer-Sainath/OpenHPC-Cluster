# Lattice Boltzman Fluid Dynamics ( Von Kármán vortex street)

This repository folder records a **parallel two-dimensional D2Q9 BGK Lattice Boltzmann** simulation of flow past a cylinder, executed on a **4-compute-node Rocky Linux 9.8 Slurm cluster (16 MPI ranks)**. All documentation and outputs are inside the standard [`Lattice-Boltzmann-Results/`](Lattice-Boltzmann-Results/README.md) directory.

![Final signed-vorticity image](Lattice-Boltzmann-Results/images/final-frame.png)

**[Watch the actual HPC MP4](Lattice-Boltzmann-Results/video/vortex.mp4)** · **[Open the standardized Results folder](Lattice-Boltzmann-Results/README.md)**

## Verified performance

| Job | MPI ranks | Compute nodes | Solver wall time | MLUPS | Scaling |
|---:|---:|---:|---:|---:|---:|
| 93 | 1 | 1 | 1059.16 s | 11.88 | 1.00× |
| 94 | 4 | 1 | 322.65 s | 39.00 | 3.28× |
| 95 | 16 | 4 | 88.26 s | 142.56 | **12.00×** |

Production job **96** completed **80,000 steps** on a **2048×768** grid in **897.84 s** (**140.15 MLUPS**) and recorded **289 frames**. Encoder job **97** produced the included 1024×384 H.264 MP4.

**Hardware correction from archived `lscpu` evidence:** each *compute* node has an **Intel Core i5-2400**, not i5-4460; the *admin* node has an **Intel Core i5-4460S**. Four nodes have 16 physical cores total. [See hardware inventory](Lattice-Boltzmann-Results/environment.md).

**Scientific caveat:** the animation shows a visually alternating wake consistent with von Kármán shedding. Strouhal number, drag/lift and resolution convergence were not measured. Historical per-rank timings and peak process memory are unavailable because the initial jobs did not instrument them and Slurm accounting is disabled.

## Standard documentation index

- [`results.md`](Lattice-Boltzmann-Results/results.md): jobs 91–97, arguments, measured overall timings, fastest/slowest rank and memory availability.
- [`environment.md`](Lattice-Boltzmann-Results/environment.md): actual CPU/RAM/NIC and kernel on **every node**, Slurm/MPI/Python/FFmpeg versions.
- [`slurm_commands.md`](Lattice-Boltzmann-Results/slurm_commands.md): exact historical submissions and batch scripts, plus rerun instructions.
- [`code/`](Lattice-Boltzmann-Results/code/): original solver, build/Slurm scripts, preserved historical scripts, optional profiling utilities.
- [`logs/`](Lattice-Boltzmann-Results/logs/README.md): **complete raw Slurm output** for jobs 91–97 plus original five-node hardware reports.
- [`images/`](Lattice-Boltzmann-Results/images/README.md): documented signed-vorticity stills and performance chart.
- [`video/vortex.mp4`](Lattice-Boltzmann-Results/video/vortex.mp4): original encoded production result.
- [`data/`](Lattice-Boltzmann-Results/data/): structured CSV and JSON measurement records.
