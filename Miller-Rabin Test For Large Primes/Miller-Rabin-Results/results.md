# Results

## Jobs

| Slurm job | Nodes | MPI ranks (--ntasks) | Tasks per node | Arguments |
|---:|:---|---:|---:|:---|
| 74 | node01 | 1 | 1 | `mersenne 16 M4423,M9689,M11213,C4253x4423` |
| 75 | node01 | 4 | 4 | `mersenne 16 M4423,M9689,M11213,C4253x4423` |
| 76 | node[01-04] | 16 | 4 | `mersenne 16 M4423,M9689,M11213,C4253x4423` |
| 77 | node[01-04] | 16 | 4 | `mersenne 16 M19937,M21701,M23209,C9941x11213` |
| 78 | node01 | 1 | 1 | `search 2048 60` |
| 79 | node01 | 4 | 4 | `search 2048 60` |
| 80 | node[01-04] | 16 | 4 | `search 2048 60` |
| 81 | node[01-04] | 16 | 4 | `search 4096 120` |
| 82 | node[01-04] | 16 | 4 | `mersenne 16 M86243` |
| 83 | node[01-04] | 16 | 4 | `search 4096 2400` |

Total compute across all runs: 18.38 core-hours.

## 1. Witness-split primality tests: the same numbers on 1, 4 and 16 MPI ranks

16 Miller-Rabin rounds in total per number, split evenly across the ranks.

**Job 74**

| Number | Bits | Truth | Verdict | Correct | Ranks | Nodes | Rounds requested | Wall (s) | Slowest rank (s) | Fastest rank (s) | Slowest rank per node (s) | Core-hours | Est. hours on 8 cores |
|:---|---:|:---|:---|:---|---:|---:|---:|---:|---:|---:|:---|---:|---:|
| M4423 | 4423 | prime | probably prime | yes | 1 | 1 | 16 | 3.96 | 3.96 | 3.96 | node01 4.0 | 0.001 | 0.00 |
| M9689 | 9689 | prime | probably prime | yes | 1 | 1 | 16 | 36.87 | 36.87 | 36.87 | node01 36.9 | 0.010 | 0.00 |
| M11213 | 11213 | prime | probably prime | yes | 1 | 1 | 16 | 56.35 | 56.35 | 56.35 | node01 56.4 | 0.016 | 0.00 |
| C4253x4423 | 8676 | composite | composite | yes | 1 | 1 | 16 | 1.57 | 1.57 | 1.57 | node01 1.6 | 0.000 | 0.00 |

**Job 75**

| Number | Bits | Truth | Verdict | Correct | Ranks | Nodes | Rounds requested | Wall (s) | Slowest rank (s) | Fastest rank (s) | Slowest rank per node (s) | Core-hours | Est. hours on 8 cores |
|:---|---:|:---|:---|:---|---:|---:|---:|---:|---:|---:|:---|---:|---:|
| M4423 | 4423 | prime | probably prime | yes | 4 | 1 | 16 | 1.05 | 1.05 | 1.05 | node01 1.0 | 0.001 | 0.00 |
| M9689 | 9689 | prime | probably prime | yes | 4 | 1 | 16 | 9.78 | 9.78 | 9.77 | node01 9.8 | 0.011 | 0.00 |
| M11213 | 11213 | prime | probably prime | yes | 4 | 1 | 16 | 14.96 | 14.96 | 14.91 | node01 15.0 | 0.017 | 0.00 |
| C4253x4423 | 8676 | composite | composite | yes | 4 | 1 | 16 | 1.66 | 1.66 | 1.66 | node01 1.7 | 0.002 | 0.00 |

**Job 76**

| Number | Bits | Truth | Verdict | Correct | Ranks | Nodes | Rounds requested | Wall (s) | Slowest rank (s) | Fastest rank (s) | Slowest rank per node (s) | Core-hours | Est. hours on 8 cores |
|:---|---:|:---|:---|:---|---:|---:|---:|---:|---:|---:|:---|---:|---:|
| M4423 | 4423 | prime | probably prime | yes | 16 | 4 | 16 | 0.26 | 0.26 | 0.26 | node01 0.3, node02 0.3, node03 0.3, node04 0.3 | 0.001 | 0.00 |
| M9689 | 9689 | prime | probably prime | yes | 16 | 4 | 16 | 2.45 | 2.45 | 2.44 | node01 2.4, node02 2.4, node03 2.4, node04 2.4 | 0.011 | 0.00 |
| M11213 | 11213 | prime | probably prime | yes | 16 | 4 | 16 | 3.74 | 3.74 | 3.73 | node01 3.7, node02 3.7, node03 3.7, node04 3.7 | 0.017 | 0.00 |
| C4253x4423 | 8676 | composite | composite | yes | 16 | 4 | 16 | 1.66 | 1.66 | 1.66 | node01 1.7, node02 1.7, node03 1.7, node04 1.7 | 0.007 | 0.00 |

## 2. Very large numbers on 16 ranks (4 nodes)

**Job 77**

| Number | Bits | Truth | Verdict | Correct | Ranks | Nodes | Rounds requested | Wall (s) | Slowest rank (s) | Fastest rank (s) | Slowest rank per node (s) | Core-hours | Est. hours on 8 cores |
|:---|---:|:---|:---|:---|---:|---:|---:|---:|---:|---:|:---|---:|---:|
| M19937 | 19937 | prime | probably prime | yes | 16 | 4 | 16 | 19.60 | 19.60 | 19.55 | node01 19.6, node02 19.6, node03 19.6, node04 19.6 | 0.087 | 0.01 |
| M21701 | 21701 | prime | probably prime | yes | 16 | 4 | 16 | 25.14 | 25.13 | 25.06 | node01 25.1, node02 25.1, node03 25.1, node04 25.1 | 0.112 | 0.01 |
| M23209 | 23209 | prime | probably prime | yes | 16 | 4 | 16 | 30.58 | 30.57 | 30.52 | node01 30.6, node02 30.6, node03 30.6, node04 30.6 | 0.136 | 0.02 |
| C9941x11213 | 21154 | composite | composite | yes | 16 | 4 | 16 | 21.65 | 21.65 | 21.58 | node01 21.6, node02 21.6, node03 21.6, node04 21.6 | 0.096 | 0.01 |

## 3. Prime search throughput (fixed time budget per run)

| Run | Time budget | Ranks | Nodes | Candidates tested (after sieve) | Primes found (verified) | Wall (s) | Primes per minute | Primes found per node | Core-hours | Est. hours on 8 cores |
|:---|:---|---:|---:|---:|:---|---:|---:|:---|---:|---:|
| search 2048-bit | 60 s budget | 1 | 1 | 1744 | 16 (16 verified) | 60.0 | 16.0 | node01 16 | 0.017 | 0.00 |
| search 2048-bit | 60 s budget | 4 | 1 | 6538 | 62 (62 verified) | 60.0 | 62.0 | node01 62 | 0.067 | 0.01 |
| search 2048-bit | 60 s budget | 16 | 4 | 26182 | 246 (246 verified) | 60.4 | 244.4 | node01 62, node02 57, node03 62, node04 65 | 0.268 | 0.03 |
| search 4096-bit | 120 s budget | 16 | 4 | 8058 | 39 (39 verified) | 122.2 | 19.1 | node01 12, node02 5, node03 8, node04 14 | 0.543 | 0.07 |

## 4. Large-scale tier: long runs on all 16 ranks

**Job 82: the largest Mersenne number that fit the time budget**

| Number | Bits | Truth | Verdict | Correct | Ranks | Nodes | Rounds requested | Wall (s) | Slowest rank (s) | Fastest rank (s) | Slowest rank per node (s) | Core-hours | Est. hours on 8 cores |
|:---|---:|:---|:---|:---|---:|---:|---:|---:|---:|---:|:---|---:|---:|
| M86243 | 86243 | prime | probably prime | yes | 16 | 4 | 16 | 1413.34 | 1413.34 | 1411.89 | node01 1413.3, node02 1412.5, node03 1413.3, node04 1413.3 | 6.282 | 0.79 |

**Job 83: 4096-bit prime search**

| Run | Time budget | Ranks | Nodes | Candidates tested (after sieve) | Primes found (verified) | Wall (s) | Primes per minute | Primes found per node | Core-hours | Est. hours on 8 cores |
|:---|:---|---:|---:|---:|:---|---:|---:|:---|---:|---:|
| search 4096-bit | 2400 s budget | 16 | 4 | 161074 | 768 (768 verified) | 2402.6 | 19.2 | node01 191, node02 191, node03 209, node04 177 | 10.678 | 1.33 |

## Per-rank detail (search runs)

| Run | Ranks | MPI rank | Node | Busy time (s) | Candidates tested | Primes found |
|:---|:---|---:|:---|---:|---:|---:|
| 2048-bit search | 1 ranks | 0 | node01 | 60.0 | 1744 | 16 |
| 2048-bit search | 4 ranks | 0 | node01 | 60.0 | 1627 | 16 |
| 2048-bit search | 4 ranks | 1 | node01 | 60.0 | 1659 | 14 |
| 2048-bit search | 4 ranks | 2 | node01 | 60.0 | 1684 | 13 |
| 2048-bit search | 4 ranks | 3 | node01 | 60.0 | 1568 | 19 |
| 2048-bit search | 16 ranks | 0 | node01 | 60.0 | 1625 | 16 |
| 2048-bit search | 16 ranks | 1 | node01 | 60.0 | 1664 | 14 |
| 2048-bit search | 16 ranks | 2 | node01 | 60.0 | 1682 | 13 |
| 2048-bit search | 16 ranks | 3 | node01 | 60.0 | 1568 | 19 |
| 2048-bit search | 16 ranks | 4 | node02 | 60.0 | 1697 | 12 |
| 2048-bit search | 16 ranks | 5 | node02 | 60.0 | 1718 | 11 |
| 2048-bit search | 16 ranks | 6 | node02 | 60.0 | 1623 | 16 |
| 2048-bit search | 16 ranks | 7 | node02 | 60.0 | 1588 | 18 |
| 2048-bit search | 16 ranks | 8 | node03 | 60.0 | 1604 | 17 |
| 2048-bit search | 16 ranks | 9 | node03 | 60.0 | 1569 | 19 |
| 2048-bit search | 16 ranks | 10 | node03 | 60.0 | 1661 | 14 |
| 2048-bit search | 16 ranks | 11 | node03 | 60.0 | 1700 | 12 |
| 2048-bit search | 16 ranks | 12 | node04 | 60.4 | 1672 | 14 |
| 2048-bit search | 16 ranks | 13 | node04 | 60.0 | 1697 | 12 |
| 2048-bit search | 16 ranks | 14 | node04 | 60.0 | 1472 | 24 |
| 2048-bit search | 16 ranks | 15 | node04 | 60.0 | 1642 | 15 |
| 4096-bit search | 16 ranks | 0 | node01 | 120.0 | 529 | 1 |
| 4096-bit search | 16 ranks | 1 | node01 | 120.1 | 531 | 1 |
| 4096-bit search | 16 ranks | 2 | node01 | 120.0 | 453 | 5 |
| 4096-bit search | 16 ranks | 3 | node01 | 122.2 | 464 | 5 |
| 4096-bit search | 16 ranks | 4 | node02 | 120.1 | 549 | 0 |
| 4096-bit search | 16 ranks | 5 | node02 | 120.1 | 512 | 2 |
| 4096-bit search | 16 ranks | 6 | node02 | 120.2 | 512 | 2 |
| 4096-bit search | 16 ranks | 7 | node02 | 120.2 | 531 | 1 |
| 4096-bit search | 16 ranks | 8 | node03 | 120.0 | 473 | 4 |
| 4096-bit search | 16 ranks | 9 | node03 | 120.1 | 550 | 0 |
| 4096-bit search | 16 ranks | 10 | node03 | 120.0 | 548 | 0 |
| 4096-bit search | 16 ranks | 11 | node03 | 120.0 | 473 | 4 |
| 4096-bit search | 16 ranks | 12 | node04 | 120.2 | 474 | 4 |
| 4096-bit search | 16 ranks | 13 | node04 | 120.0 | 511 | 2 |
| 4096-bit search | 16 ranks | 14 | node04 | 120.0 | 474 | 4 |
| 4096-bit search | 16 ranks | 15 | node04 | 120.2 | 474 | 4 |
| 4096-bit search | 16 ranks | 0 | node01 | 2400.1 | 10041 | 50 |
| 4096-bit search | 16 ranks | 1 | node01 | 2400.1 | 10166 | 43 |
| 4096-bit search | 16 ranks | 2 | node01 | 2400.0 | 10019 | 52 |
| 4096-bit search | 16 ranks | 3 | node01 | 2400.1 | 10077 | 46 |
| 4096-bit search | 16 ranks | 4 | node02 | 2400.1 | 9985 | 52 |
| 4096-bit search | 16 ranks | 5 | node02 | 2400.1 | 10013 | 51 |
| 4096-bit search | 16 ranks | 6 | node02 | 2400.2 | 10155 | 43 |
| 4096-bit search | 16 ranks | 7 | node02 | 2402.0 | 10126 | 45 |
| 4096-bit search | 16 ranks | 8 | node03 | 2400.2 | 9877 | 58 |
| 4096-bit search | 16 ranks | 9 | node03 | 2402.6 | 10137 | 45 |
| 4096-bit search | 16 ranks | 10 | node03 | 2400.2 | 10019 | 51 |
| 4096-bit search | 16 ranks | 11 | node03 | 2400.2 | 9921 | 55 |
| 4096-bit search | 16 ranks | 12 | node04 | 2400.0 | 10009 | 51 |
| 4096-bit search | 16 ranks | 13 | node04 | 2400.1 | 10163 | 43 |
| 4096-bit search | 16 ranks | 14 | node04 | 2400.1 | 10237 | 39 |
| 4096-bit search | 16 ranks | 15 | node04 | 2400.0 | 10129 | 44 |

## Peak memory per rank

- job 74: largest per-rank resident memory: 26 MB
- job 75: largest per-rank resident memory: 26 MB
- job 76: largest per-rank resident memory: 26 MB
- job 77: largest per-rank resident memory: 27 MB
- job 78: largest per-rank resident memory: 25 MB
- job 79: largest per-rank resident memory: 26 MB
- job 80: largest per-rank resident memory: 26 MB
- job 81: largest per-rank resident memory: 26 MB
- job 82: largest per-rank resident memory: 27 MB
- job 83: largest per-rank resident memory: 28 MB

Each configuration was run once, so treat small differences in wall time as noise.
