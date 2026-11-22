# OpenHPC Cluster — Simulation Workloads

**Scientific computing on a student-built, four-compute-node HPC cluster.** This branch contains six workloads in computational fluid dynamics, quantum-mechanical visualization, number theory, and distributed task scheduling. It preserves runnable source, Slurm job definitions, measurements, raw job output, and selected generated artifacts.

> **Separate branches:** this is the **`Simulation-Workloads`** branch. Deployment and cluster configuration live in the [HPC Cluster Infrastructure branch](https://github.com/Programmer-Sainath/OpenHPC-Cluster/tree/HPC-Cluster-Infrastructure). These workloads are not an installer for the infrastructure.

## Simulation index

| Workload | Method and parallel model | Representative archived result | Documentation |
|---|---|---|---|
| Lattice Boltzmann fluid dynamics | 2D D2Q9 BGK solver in C + MPI across four nodes | 12.00× measured speedup at 16 versus 1 MPI ranks (identical workload) | [Read](<Lattice Boltzman Fluid Dynamics ( Von Kármán vortex street)/README.md>) |
| Distributed sieve of Eratosthenes | Python/NumPy + MPI; partitioned odd-integer arrays | Prime count through 50,000,000,000 with 16 MPI ranks | [Read](<Simple Seive of Eratosthenes/README.md>) |
| Miller–Rabin primality | Python + MPI; split witness rounds or independent candidate search | 2,048-/4,096-bit candidate searches and known Mersenne cases | [Read](<Miller-Rabin Test For Large Primes/README.md>) |
| Hydrogen orbital visualization | Monte Carlo importance sampling + mpi4py | 200 million samples across 16 MPI ranks | [Read](<Hydrogen Orbiatal Simulations/README.md>) |
| Dask primality | Single-node Dask LocalCluster; independent worker tasks | 1/2/4 worker benchmark series | [Read](<Dask Primility/README.md>) |
| Chudnovsky π calculation | Single-core binary splitting (original run); not distributed MPI | Archived digits up to one million after the decimal point | [Read](<Chudnovsky's Pi Calculation/README.md>) |

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
2. Choose a workload above. For executable **new-run** commands, use [run recipes](docs/RUN_RECIPES.md); historic command notes may include explanatory annotations rather than literal shell commands.
3. Read the original `results.md` and logs before making performance claims. **Do not conflate archived timings with results of new runs.**

The accompanying [`requirements.txt`](requirements.txt) records the major Python dependencies from the cluster environment as documented in the archived November 2026 inventory. It is not a full lockfile for OS packages, MPI, compilers, or every historical prototype.

## Interpretation and scientific limitations

These demonstrations have different validation standards. For example, LBM qualitatively shows a vortex street but has **not** established Strouhal number or grid-convergence validation; Miller–Rabin returns *probable-prime* verdicts, not general proofs; the large sieve result relies on spot checks where a reference value was unavailable. See [known limitations](docs/KNOWN_LIMITATIONS.md) for provenance and missing materials.

## Contributions, acknowledgements, and license

This work was conducted as part of the **DPS–Modern Indian School HPC Cluster project**. See the [infrastructure branch](https://github.com/Programmer-Sainath/OpenHPC-Cluster/tree/HPC-Cluster-Infrastructure) for the documented project team and responsibilities. Workload-level authorship is not inferred solely from file names; contributions should be credited explicitly in a future `CONTRIBUTORS.md` after checking with the team.

The project acknowledges the school for access to its robotics-lab hardware and the open-source communities behind Rocky Linux, Warewulf, OpenHPC, Slurm, Open MPI, Python, NumPy, SciPy, and Dask. See the branch [`LICENSE`](LICENSE) for licensing terms.
