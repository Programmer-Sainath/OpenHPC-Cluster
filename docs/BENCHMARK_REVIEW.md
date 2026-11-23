# What four desktops contributed

Four repurposed Intel Core i5-2400 desktops, connected by Gigabit Ethernet, cut the same cylinder-flow simulation from 322.65 seconds on one fully used desktop to 88.26 seconds across four. Sainath submitted and ran all six project workloads. The i5-4460S administrator coordinated jobs and contributed no compute cores to these timings.

## Fixed-work CFD benchmark

| Job | Compute configuration | Solver time | Speedup over one rank |
|---|---|---:|---:|
| 93 | 1 desktop, 1 MPI rank | 1,059.16 s | 1.00× |
| 94 | 1 desktop, 4 MPI ranks | 322.65 s | 3.28× |
| 95 | 4 desktops, 16 MPI ranks | 88.26 s | 12.00× |

All three jobs used a 3,072 × 1,024 grid, 4,000 steps, cylinder diameter 128 and Reynolds number 120. Frame output was disabled. Across 12,582,912,000 nominal site updates, job 95 reported 142.56 million lattice updates per second (MLUPS). Job start and end timestamps agree with solver timings to the nearest second. Final mass and maximum velocity agree to the precision printed. Each configuration has one recorded timing, so repeatability remains unmeasured.

From one fully used desktop to four, the speedup was 3.66×, about 91% of ideal fourfold scaling. Relative to a single core, speedup was 12.00× and parallel efficiency was 75%. A separate short test recorded identical rendered frames across one and sixteen ranks. The original frames were unavailable for independent comparison. The wake is qualitatively consistent with vortex shedding. Shedding frequency and grid convergence still require measurement.

## Checks on the other five workloads

| Workload | Result and scope |
|---|---|
| Chudnovsky π | An independent MPFR calculation matched every stored digit in all ten files, through one million decimal places. The largest file records 72.3 s on one core. |
| Distributed sieve | Independent prime counts matched both outputs: 455,052,511 through 10 billion and 2,119,654,578 through 50 billion. Job 90 took 68.9 s and distributed 23.28 GiB of arrays across four nodes. |
| Hydrogen orbital | For 25 million samples, compute time fell from 9.1 s to 0.8 s (1 to 16 ranks). In a separate 200-million-sample run, the estimated mean radius was 17.9986 Bohr radii against the theoretical 18.0000. |
| Dask primality | On one desktop, ten trials per configuration gave mean times of 1.73 s with one worker and 0.41 s with four workers. |
| Miller–Rabin | In roughly one minute, one rank found 16 probable primes and sixteen ranks found 246. Random searches measure throughput over a time budget. |

## Comparison with a laptop

The sieve arrays alone exceeded the RAM of a 16 GB laptop. A memory-efficient sieve could solve the same mathematical problem using less memory. For CFD, a modern laptop could be faster or slower. A defensible comparison would run the same double-precision CPU solver with the same inputs and output settings, verify the results, and repeat timings on both systems. The cluster archive contains no such laptop measurement.

For context, a Chalmers study reported 170 MLUPS on one quad-core i5-2500K at 4.0 GHz with 8 GB RAM. It used single precision and a different, optimized data layout. The result shows how much implementation matters and cannot predict that desktop’s runtime for the school solver. See [section 7.5 and Table 1](https://publications.lib.chalmers.se/records/fulltext/161226.pdf).

## Archived evidence

- [CFD job logs and hardware inventories](<../Lattice Boltzman Fluid Dynamics ( Von Kármán vortex street)/Lattice-Boltzmann-Results/logs/>)
- [Sieve timings and memory](<../Simple Seive of Eratosthenes/Sieve-Results/results.md>)
- [Stored π digits](<../Chudnovsky's Pi Calculation/Chudnovsky-Results/digits/>)
- [Orbital measurements](<../Hydrogen Orbiatal Simulations/Hydrogen-Orbital-Results/results.md>)
- [Dask logs](<../Dask Primility/Dask-Primility-Results/logs/>)
- [Miller–Rabin logs](<../Miller-Rabin Test For Large Primes/Miller-Rabin-Results/logs/>)
