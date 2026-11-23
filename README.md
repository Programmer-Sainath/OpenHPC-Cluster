# OpenHPC Cluster — Simulation Workloads

**Scientific computing on a student-built, four-compute-node HPC cluster.** This branch contains six workloads in computational fluid dynamics, quantum-mechanical visualization, number theory, and distributed task scheduling. It preserves runnable source, Slurm job definitions, measurements, raw job output, and selected generated artifacts.

> **Separate branches:** this is the **`Simulation-Workloads`** branch. Deployment and cluster configuration live in the [HPC Cluster Infrastructure branch](https://github.com/Programmer-Sainath/OpenHPC-Cluster/tree/HPC-Cluster-Infrastructure). These workloads are not an installer for the infrastructure.

## Workload contributions

| Developer | Workloads developed |
|---|---|
| **Aayush Pal** | Distributed Sieve of Eratosthenes, Miller-Rabin primality testing, Dask-based primality search, and hydrogen orbital visualization |
| **Shanmukha Sainath Kasireddy** | Lattice Boltzmann fluid dynamics (von Karman vortex shedding) and Chudnovsky pi calculation |

**Cluster execution.** Sainath ran all six workloads on the HPC cluster. He configured Slurm, submitted the jobs with `sbatch`, and allocated MPI tasks for the workloads that used MPI. Eric Bipin Philip installed OpenHPC and Open MPI.

## Simulation index

| Workload | Method and parallel model | Representative archived result | Documentation |
|---|---|---|---|
| Lattice Boltzmann fluid dynamics | 2D D2Q9 BGK solver in C + MPI across four nodes | 12.00× measured speedup at 16 versus 1 MPI ranks (identical workload) | [Read](<Lattice Boltzman Fluid Dynamics ( Von Kármán vortex street)/README.md>) |
| Distributed sieve of Eratosthenes | Python/NumPy + MPI; partitioned odd-integer arrays | Prime count through 50,000,000,000 with 16 MPI ranks | [Read](<Simple Seive of Eratosthenes/README.md>) |
| Miller–Rabin primality | Python + MPI; split witness rounds or independent candidate search | 2,048-/4,096-bit candidate searches and known Mersenne cases | [Read](<Miller-Rabin Test For Large Primes/README.md>) |
| Hydrogen orbital visualization | Monte Carlo importance sampling + mpi4py | 200 million samples across 16 MPI ranks | [Read](<Hydrogen Orbiatal Simulations/README.md>) |
| Dask primality | Single-node Dask LocalCluster; independent worker tasks | 1/2/4 worker benchmark series | [Read](<Dask Primility/README.md>) |
| Chudnovsky π calculation | Single-core binary splitting (original run); not distributed MPI | Archived digits up to one million after the decimal point | [Read](<Chudnovsky's Pi Calculation/README.md>) |

## Benchmark review

[Open the dedicated benchmark review folder](benchmark-review/).

Four repurposed Intel Core i5-2400 desktops, connected by Gigabit Ethernet, cut the same cylinder-flow simulation from 322.65 seconds on one fully used desktop to 88.26 seconds across four. Sainath submitted and ran all six project workloads. The i5-4460S administrator coordinated jobs and contributed no compute cores to these timings.

### Fixed-work CFD benchmark

| Job | Compute configuration | Solver time | Speedup over one rank |
|---|---|---:|---:|
| 93 | 1 desktop, 1 MPI rank | 1,059.16 s | 1.00× |
| 94 | 1 desktop, 4 MPI ranks | 322.65 s | 3.28× |
| 95 | 4 desktops, 16 MPI ranks | 88.26 s | 12.00× |

All three jobs used a 3,072 × 1,024 grid, 4,000 steps, cylinder diameter 128 and Reynolds number 120. Frame output was disabled. Across 12,582,912,000 nominal site updates, job 95 reported 142.56 million lattice updates per second (MLUPS). Job start and end timestamps agree with solver timings to the nearest second. Final mass and maximum velocity agree to the precision printed. Each configuration has one recorded timing, so repeatability remains unmeasured.

From one fully used desktop to four, the speedup was 3.66×, about 91% of ideal fourfold scaling. Relative to a single core, speedup was 12.00× and parallel efficiency was 75%. A separate short test recorded identical rendered frames across one and sixteen ranks. The original frames were unavailable for independent comparison. The wake is qualitatively consistent with vortex shedding. Shedding frequency and grid convergence still require measurement.

### Checks on the other five workloads

| Workload | Result and scope |
|---|---|
| Chudnovsky π | An independent MPFR calculation matched every stored digit in all ten files, through one million decimal places. The largest file records 72.3 s on one core. |
| Distributed sieve | Independent prime counts matched both outputs: 455,052,511 through 10 billion and 2,119,654,578 through 50 billion. Job 90 took 68.9 s and distributed 23.28 GiB of arrays across four nodes. |
| Hydrogen orbital | For 25 million samples, compute time fell from 9.1 s to 0.8 s (1 to 16 ranks). In a separate 200-million-sample run, the estimated mean radius was 17.9986 Bohr radii against the theoretical 18.0000. |
| Dask primality | On one desktop, ten trials per configuration gave mean times of 1.73 s with one worker and 0.41 s with four workers. |
| Miller–Rabin | In roughly one minute, one rank found 16 probable primes and sixteen ranks found 246. Random searches measure throughput over a time budget. |

### Comparison with a laptop

The sieve arrays alone exceeded the RAM of a 16 GB laptop. A memory-efficient sieve could solve the same mathematical problem using less memory. For CFD, a modern laptop could be faster or slower. A defensible comparison would run the same double-precision CPU solver with the same inputs and output settings, verify the results, and repeat timings on both systems. The cluster archive contains no such laptop measurement.

For context, a Chalmers study reported 170 MLUPS on one quad-core i5-2500K at 4.0 GHz with 8 GB RAM. It used single precision and a different, optimized data layout. The result shows how much implementation matters and cannot predict that desktop’s runtime for the school solver. See [section 7.5 and Table 1](https://publications.lib.chalmers.se/records/fulltext/161226.pdf).

### Archived evidence

- [CFD job logs and hardware inventories](<Lattice Boltzman Fluid Dynamics ( Von Kármán vortex street)/Lattice-Boltzmann-Results/logs/>)
- [Sieve timings and memory](<Simple Seive of Eratosthenes/Sieve-Results/results.md>)
- [Stored π digits](<Chudnovsky's Pi Calculation/Chudnovsky-Results/digits/>)
- [Orbital measurements](<Hydrogen Orbiatal Simulations/Hydrogen-Orbital-Results/results.md>)
- [Dask logs](<Dask Primility/Dask-Primility-Results/logs/>)
- [Miller–Rabin logs](<Miller-Rabin Test For Large Primes/Miller-Rabin-Results/logs/>)

## Cluster used for measurements

The recorded experiments used **four Rocky Linux 9 compute nodes (`node01`–`node04`)**, each with an **Intel Core i5-2400 (4 physical cores)** and approximately **15 GiB Linux-visible RAM**. The separate admin node has an Intel Core i5-4460S. This means 16 physical compute cores across four compute nodes, managed using Slurm and Open MPI. The [original inventory](<Lattice Boltzman Fluid Dynamics ( Von Kármán vortex street)/Lattice-Boltzmann-Results/environment.md>) is based on captured `lscpu`, network, and OS diagnostics.

**Be precise about parallelism:** LBM, the sieve, Miller–Rabin, and the orbital benchmark used MPI; Dask's recorded workload uses a *single-node* `LocalCluster`; the π jobs were *serial*, even though Slurm scheduled them.

## Results and evidence

Each workload contains or links to its recorded results. Most benchmark folders use this layout:

```text
<Workload>/
  README.md                 # Context, method, reproduction notes
  <Workload>-Results/
    results.md              # Recorded numerical measurements
    slurm_commands.md       # Historic submissions and scripts
    code/                   # Actual runnable benchmark version
    logs/                   # Original Slurm stdout where available
    images/, video/, ...    # Outputs, where available
```

The LBM folder contains particularly extensive records: source snapshots, full job logs, hardware inventories, checksum manifest, measured throughput, and a video. Other experiments have differing levels of archival completeness; refer to the workload READMEs and [known limitations](docs/KNOWN_LIMITATIONS.md).

## Shell and operating system

**Linux only:** the cluster is built on **Rocky Linux**. All terminal commands and Slurm recipes in this branch are written for **GNU/Linux Bash**, to be run on the admin node (or, for compute workloads, through Slurm). If connecting from a Windows laptop using SSH/Tailscale, enter the Linux SSH session before running them. Windows CMD, PowerShell, and `.bat` instructions are not used.

## Getting started

1. Read [setup and reproduction](docs/REPRODUCIBILITY.md) before submitting jobs. The included scripts contain paths and MPI network settings from the school's cluster that must be checked on a different environment.
2. Choose a workload above. For executable **new-run** commands, use [run recipes](docs/RUN_RECIPES.md); historical Slurm command notes now include executable **equivalents** where original dependency syntax was not preserved; they are not verbatim shell-history transcripts.
3. Read the original `results.md` and logs before making performance claims. **Do not conflate archived timings with results of new runs.**

The accompanying [`requirements.txt`](requirements.txt) records the major Python dependencies from the cluster environment as documented in the archived November 2026 inventory. It is not a full lockfile for OS packages, MPI, compilers, or every historical prototype.

## Interpretation and scientific limitations

These demonstrations have different validation standards. For example, LBM qualitatively shows a vortex street but has **not** established Strouhal number or grid-convergence validation; Miller–Rabin returns *probable-prime* verdicts, not general proofs; the large sieve result relies on spot checks where a reference value was unavailable. See [known limitations](docs/KNOWN_LIMITATIONS.md) for provenance and missing materials.

## Acknowledgements, and license

This work was conducted as part of the **DPS–Modern Indian School HPC Cluster project**. See the [infrastructure branch](https://github.com/Programmer-Sainath/OpenHPC-Cluster/tree/HPC-Cluster-Infrastructure) for the documented project team and responsibilities.

The project acknowledges the school for access to its robotics-lab hardware and the open-source communities behind Rocky Linux, Warewulf, OpenHPC, Slurm, Open MPI, Python, NumPy, SciPy, and Dask. See the branch [`LICENSE`](LICENSE) for licensing terms.
