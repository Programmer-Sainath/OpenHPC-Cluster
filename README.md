# HPC Simulation & Computational Workloads

This branch contains mathematical and scientific computing workloads developed, executed, and tested using our **five-machine High-Performance Computing (HPC) cluster**.

The objective is to explore how computationally intensive problems can be implemented, executed, and evaluated in an HPC environment. These workloads also serve as practical tests of the cluster's computational capabilities, software infrastructure, and job execution workflow.

## Cluster Environment

The workloads in this branch are associated with the following cluster:

- **5 physical machines:** 1 administration node and 4 compute nodes
- **Operating System:** Rocky Linux 9
- **CPU:** Intel Core i5-4460
- **Memory:** 16 GB RAM per machine
- **Workload Management:** Slurm
- **Cluster Provisioning:** Warewulf
- **Authentication:** Munge
- **Networking:** Gigabit Ethernet

## Computational Workloads

The following projects explore different mathematical and computational problems.

### 1. Chudnovsky's Pi Calculation
Implementation of the Chudnovsky algorithm for high-precision calculation of π.

- Focus: Arbitrary-precision arithmetic and computational mathematics.
- Demonstrated result: Calculation of **1,000,000 digits of π in 72 seconds** on the HPC cluster.
- Further work: Benchmarking execution time at different precision levels and documenting performance.

### 2. Dask Primality
Exploration of distributed computing using Dask for computational number theory.

- Focus: Parallel and distributed task execution.
- Objective: Explore how computational workloads can be divided and processed across available resources.

### 3. Miller–Rabin Test for Large Primes
Implementation and testing of the Miller–Rabin probabilistic primality test.

- Focus: Large-integer arithmetic and primality testing.
- Objective: Evaluate the computational cost of testing large numbers for probable primality.

### 4. Sieve of Eratosthenes
Implementation of the Sieve of Eratosthenes for generating prime numbers.

- Focus: Algorithmic efficiency and computational number theory.
- Objective: Examine execution time and performance as the input range increases.

## Repository Structure

Each workload is maintained as an independent project, with its own code, documentation, results, and troubleshooting notes where applicable.

```text
Simulation-Workloads/
│
├── Chudnovsky's Pi Calculation/
├── Dask Primility/
├── Miller-Rabin Test For Large Primes/
└── Simple Seive of Eratosthenes/
```

## Performance Evaluation

Where applicable, workloads are evaluated using:

- Execution time
- Input size and computational complexity
- Resource utilization
- Scalability and parallel execution behaviour
- Comparison between different implementations

Benchmark results and observations will be documented alongside their respective workloads. Results will be reported with their execution conditions so that measurements can be interpreted accurately.

## Project Scope

This branch is an ongoing collection of computational workloads used to explore mathematical computing, parallel processing, and scientific computing through our school-built HPC cluster.

Future work will focus on expanding the workload collection, improving implementations, conducting repeatable benchmarks, and exploring more computationally demanding problems, including physics-based simulations and concepts related to Computational Fluid Dynamics (CFD).

---

**Part of the OpenHPC-Cluster project.**
