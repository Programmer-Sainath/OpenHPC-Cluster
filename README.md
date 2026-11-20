# Lattice Boltzmann Fluid Dynamics — von Kármán Vortex Street

**MPI-accelerated D2Q9 computational fluid dynamics simulation on a four-node school HPC cluster.**  
**Status:** Completed production visualization and three parallel-scaling benchmarks; quantitative fluid-physics validation remains future work.

![Final vortex street visualization](media/final-frame.png)

**[Watch the actual four-node simulation (MP4)](media/vortex.mp4)** · [Simulation contact sheet](media/vortex_contactsheet.jpg) · [Measured HPC benchmark graph](results/benchmark-throughput.png)

## Overview

This project models **2-D, weakly compressible flow past a stationary circular cylinder** with a D2Q9 Bhatnagar–Gross–Krook (BGK) lattice Boltzmann solver written in **C and MPI**. At Reynolds number 120, the downstream wake transitions from a near-symmetric pattern to a visibly alternating wake consistent with **von Kármán vortex shedding**. Output frames show **signed vorticity** (cyan and orange/red, opposite senses of rotation), **not tracer particles**.

The solver partitions the domain among independent MPI ranks, exchanges neighbor halo columns, renders PPM snapshots, and produces an H.264 MP4. The actual production video and measured cluster benchmarks are included in this directory.

## Hardware and software

| Component | Configuration |
|---|---|
| Compute | **4 Lenovo ThinkCentre nodes**, Intel Core i5-4460, 4 physical cores and 16 GB DDR3 each |
| Available compute total | **16 physical cores, 64 GB DDR3** |
| Admin | 1 separate node (16 GB DDR3), used for SSH, build, scheduling, files |
| Network | Ethernet cluster interconnect; MPI network interface should be selected per site |
| OS / batch system | **Rocky Linux 9**, OpenHPC / Slurm |
| Parallel library | **Open MPI**, 16 MPI ranks for production |
| Implementation | C11, MPI, D2Q9 BGK lattice Boltzmann |
| Animation | FFmpeg / imageio-ffmpeg, H.264 MP4 |

*The same grid can run on a single workstation: the HPC contribution is the measured **parallel speedup**, not merely the existence of a simulation.*

## Final production run

| Setting | Value |
|---|---:|
| Slurm compute job | **96** (video encoder job **97**) |
| Grid | **2048 × 768** = 1,572,864 sites |
| Time steps | **80,000** |
| Nominal lattice-site updates | **125,829,120,000** (~125.8 billion) |
| Reynolds number | **120** |
| Cylinder diameter | **96 lattice cells** |
| Inlet speed | **0.06 lattice units/step** |
| Kinematic viscosity / BGK relaxation time | **0.048 / 0.644** |
| Compute allocation | **4 nodes × 4 MPI ranks = 16 ranks** |
| Snapshots | Steps 8000–80000, every 250; **289 frames** |
| MP4 video | **1024 × 384**, 24 fps, **12.04 seconds**, H.264 |

![Selected stages from the recorded video](media/vortex_contactsheet.jpg)

### What the video demonstrates

The cylinder generates a wake that evolves visibly from an approximately symmetric shape into an alternating, wavy pattern. The generated movie captures a developed visual vortex street. A video alone does **not** prove quantitative CFD accuracy or the shedding-frequency prediction; see [Validation and limitations](docs/VALIDATION.md).

## Measured performance: same workload on 1, 4 and 16 ranks

All three benchmarks used **3072 × 1024 cells for 4000 steps**, with frame output disabled. These are **actual user-supplied Slurm results**, not estimates.

| Configuration | Job | Wall time | Throughput | Speedup vs 1 rank | Parallel efficiency |
|---|---:|---:|---:|---:|---:|
| 1 MPI rank / 1 node | 93 | 1059.16 s | 11.88 MLUPS | 1.00× | 100% |
| 4 MPI ranks / 1 node | 94 | 322.65 s | 39.00 MLUPS | 3.28× | 82.1% |
| 16 MPI ranks / 4 nodes | 95 | 88.26 s | 142.56 MLUPS | **12.00×** | **75.0%** |

![Benchmark throughput](results/benchmark-throughput.png)

Relative to four ranks on one node, the 16-rank run has **3.66×** the throughput. Scaling is good for an older networked CPU cluster, but nonideal due to communication, memory/cache behavior and other overhead.

## Folder guide

```text
Lattice Boltzman Fluid Dynamics ( Von Kármán vortex street)/
├── README.md                  # Project landing page for GitHub
├── lbm_mpi.c                  # Original C/MPI solver used for the experiment
├── build.sh                   # Build with mpicc
├── lbm.sbatch                 # Reproduced cluster-compatible mpirun job script
├── encode.sbatch              # Dependent video encoding job
├── run-production.sh          # Reproduce the successful production configuration
├── benchmark.sh               # Re-run the 1/4/16-rank benchmark sequence
├── check-frame-equivalence.sh # Compare output frames from validation cases
├── docs/
│   ├── METHODS.md             # Physics, LBM method, MPI algorithm
│   ├── RESULTS.md             # Interpretation of actual metrics and video
│   ├── VALIDATION.md          # What is validated and what is not
│   ├── REPRODUCE.md           # Rocky Linux, Slurm, video, and Windows download
│   └── EXPERIMENT_LOG.md      # Dated summary of jobs and terminal evidence
├── results/
│   ├── benchmarks.csv
│   ├── benchmark-throughput.png
│   └── production-run.json
├── media/
│   ├── vortex.mp4             # Actual output from production jobs 96/97
│   ├── final-frame.png
│   └── vortex_contactsheet.jpg
├── tests/                    # Developer-only one-rank test shim
└── examples/                 # Separate small local demonstration, not the HPC video
```

## Running it

The tested Open MPI installation did not support the direct `srun ./lbm_mpi` launch method. The jobs used **`mpirun` inside a Slurm allocation**, with a hostfile constructed from Slurm's allocated nodes. This repository includes that approach rather than the unmodified `srun` templates from the original starter ZIP.

```bash
# In an SSH terminal on the Rocky Linux admin node:
mkdir -p logs runs
export PATH=/usr/lib64/openmpi/bin:$PATH
bash build.sh

# Only after checking the MPI settings and scheduling limits:
bash run-production.sh
cat prod.jobs
squeue -u "$USER"
```

The runner submits the production job plus a second job that encodes the video **only when the simulation finishes successfully**. Downloading `vortex.mp4` before both are done returns a “No such file” error because the video has not yet been created. For benchmark instructions, scientific caveats, and copying the final MP4 to Windows, read [Reproduction guide](docs/REPRODUCE.md).

## Scientific scope and integrity

- **Demonstrated:** parallel D2Q9 computation, 1/4/16-rank scaling, matching validation-case frame output between 1 and 16 ranks, completed cylinder-flow animation.
- **Not yet demonstrated:** mesh-independence, domain-independence, physical dimensional units, lift/drag coefficients, measured shedding frequency/Strouhal number, comparison with accepted experimental/numerical references, or quantified conservation error.
- **Heavy-workload idea, not claimed as completed:** 6144 × 2048 for 160,000 steps (~2.01 trillion updates). It has not been included in the measured results.
- Open boundaries use a basic zero-gradient treatment; transverse boundaries are periodic. Interpret quantitative results cautiously.

## Credits and provenance

Prepared for the school **HPC Project Team**. The solver and starter materials were developed with AI coding assistance (ChatGPT); subsequent Slurm launcher troubleshooting, benchmarks and production execution were carried out with additional Claude assistance. The recorded benchmark outputs and video are artifacts supplied from the actual four-node cluster. The documentation distinguishes measured evidence from inference and planned tests. Contributors should add or confirm names and roles before publication.

This directory is a project folder for inclusion in an existing HPC repository, rather than a separate Git repository. Any licensing terms should follow the destination repository's policy.
