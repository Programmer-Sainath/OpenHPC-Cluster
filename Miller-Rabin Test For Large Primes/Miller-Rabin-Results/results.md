# Results

## Jobs

| Slurm job | Nodes | MPI ranks (--ntasks) | Tasks per node | Arguments |
|---:|:---|---:|---:|:---|
| 66 | node01 | 1 | 1 | `mersenne 16 M4423,M9689,M11213,C4253x4423` |
| 67 | node01 | 4 | 4 | `mersenne 16 M4423,M9689,M11213,C4253x4423` |
| 68 | node[01-04] | 16 | 4 | `mersenne 16 M4423,M9689,M11213,C4253x4423` |
| 69 | node[01-04] | 16 | 4 | `mersenne 16 M19937,M21701,M23209,C9941x11213` |
| 70 | node01 | 1 | 1 | `search 2048 60` |
| 71 | node01 | 4 | 4 | `search 2048 60` |
| 72 | node[01-04] | 16 | 4 | `search 2048 60` |
| 73 | node[01-04] | 16 | 4 | `search 4096 120` |

## 1. Witness-split primality tests: the same numbers on 1, 4 and 16 MPI ranks

16 Miller-Rabin rounds in total per number, split evenly across the ranks.

**Job 66**

| Number | Bits | Truth | Verdict | Correct | Ranks | Nodes | Rounds requested | Wall (s) | Slowest rank (s) | Fastest rank (s) | Slowest rank per node (s) |
|:---|---:|:---|:---|:---|---:|---:|---:|---:|---:|---:|:---|
| M4423 | 4423 | prime | probably prime | yes | 1 | 1 | 16 | 3.97 | 3.97 | 3.97 | node01 4.0 |
| M9689 | 9689 | prime | probably prime | yes | 1 | 1 | 16 | 36.85 | 36.85 | 36.85 | node01 36.9 |
| M11213 | 11213 | prime | probably prime | yes | 1 | 1 | 16 | 56.32 | 56.32 | 56.32 | node01 56.3 |
| C4253x4423 | 8676 | composite | composite | yes | 1 | 1 | 16 | 1.57 | 1.57 | 1.57 | node01 1.6 |

**Job 67**

| Number | Bits | Truth | Verdict | Correct | Ranks | Nodes | Rounds requested | Wall (s) | Slowest rank (s) | Fastest rank (s) | Slowest rank per node (s) |
|:---|---:|:---|:---|:---|---:|---:|---:|---:|---:|---:|:---|
| M4423 | 4423 | prime | probably prime | yes | 4 | 1 | 16 | 1.05 | 1.05 | 1.05 | node01 1.0 |
| M9689 | 9689 | prime | probably prime | yes | 4 | 1 | 16 | 9.78 | 9.78 | 9.77 | node01 9.8 |
| M11213 | 11213 | prime | probably prime | yes | 4 | 1 | 16 | 14.95 | 14.95 | 14.91 | node01 14.9 |
| C4253x4423 | 8676 | composite | composite | yes | 4 | 1 | 16 | 1.66 | 1.66 | 1.66 | node01 1.7 |

**Job 68**

| Number | Bits | Truth | Verdict | Correct | Ranks | Nodes | Rounds requested | Wall (s) | Slowest rank (s) | Fastest rank (s) | Slowest rank per node (s) |
|:---|---:|:---|:---|:---|---:|---:|---:|---:|---:|---:|:---|
| M4423 | 4423 | prime | probably prime | yes | 16 | 4 | 16 | 0.26 | 0.26 | 0.26 | node01 0.3, node02 0.3, node03 0.3, node04 0.3 |
| M9689 | 9689 | prime | probably prime | yes | 16 | 4 | 16 | 2.45 | 2.45 | 2.44 | node01 2.4, node02 2.4, node03 2.4, node04 2.4 |
| M11213 | 11213 | prime | probably prime | yes | 16 | 4 | 16 | 3.73 | 3.73 | 3.73 | node01 3.7, node02 3.7, node03 3.7, node04 3.7 |
| C4253x4423 | 8676 | composite | composite | yes | 16 | 4 | 16 | 1.66 | 1.66 | 1.66 | node01 1.7, node02 1.7, node03 1.7, node04 1.7 |

## 2. Very large numbers on 16 ranks (4 nodes)

**Job 69**

| Number | Bits | Truth | Verdict | Correct | Ranks | Nodes | Rounds requested | Wall (s) | Slowest rank (s) | Fastest rank (s) | Slowest rank per node (s) |
|:---|---:|:---|:---|:---|---:|---:|---:|---:|---:|---:|:---|
| M19937 | 19937 | prime | probably prime | yes | 16 | 4 | 16 | 19.60 | 19.60 | 19.54 | node01 19.6, node02 19.6, node03 19.6, node04 19.6 |
| M21701 | 21701 | prime | probably prime | yes | 16 | 4 | 16 | 25.13 | 25.13 | 25.05 | node01 25.1, node02 25.1, node03 25.1, node04 25.1 |
| M23209 | 23209 | prime | probably prime | yes | 16 | 4 | 16 | 30.61 | 30.61 | 30.50 | node01 30.6, node02 30.6, node03 30.6, node04 30.6 |
| C9941x11213 | 21154 | composite | composite | yes | 16 | 4 | 16 | 21.67 | 21.67 | 21.60 | node01 21.7, node02 21.6, node03 21.6, node04 21.6 |

## 3. Prime search throughput (fixed time budget per run)

| Run | Time budget | Ranks | Nodes | Candidates tested (after sieve) | Primes found (verified) | Wall (s) | Primes per minute | Primes found per node |
|:---|:---|---:|---:|---:|:---|---:|---:|:---|
| search 2048-bit | 60 s budget | 1 | 1 | 1742 | 16 (16 verified) | 60.0 | 16.0 | node01 16 |
| search 2048-bit | 60 s budget | 4 | 1 | 6535 | 62 (62 verified) | 60.0 | 62.0 | node01 62 |
| search 2048-bit | 60 s budget | 16 | 4 | 26181 | 246 (246 verified) | 60.4 | 244.6 | node01 62, node02 57, node03 62, node04 65 |
| search 4096-bit | 120 s budget | 16 | 4 | 8061 | 39 (39 verified) | 122.1 | 19.2 | node01 12, node02 5, node03 8, node04 14 |

### Per-rank detail

| Run | Ranks | MPI rank | Node | Busy time (s) | Candidates tested | Primes found |
|:---|:---|---:|:---|---:|---:|---:|
| 2048-bit search | 1 ranks | 0 | node01 | 60.0 | 1742 | 16 |
| 2048-bit search | 4 ranks | 0 | node01 | 60.0 | 1626 | 16 |
| 2048-bit search | 4 ranks | 1 | node01 | 60.0 | 1659 | 14 |
| 2048-bit search | 4 ranks | 2 | node01 | 60.0 | 1683 | 13 |
| 2048-bit search | 4 ranks | 3 | node01 | 60.0 | 1567 | 19 |
| 2048-bit search | 16 ranks | 0 | node01 | 60.0 | 1624 | 16 |
| 2048-bit search | 16 ranks | 1 | node01 | 60.0 | 1659 | 14 |
| 2048-bit search | 16 ranks | 2 | node01 | 60.0 | 1684 | 13 |
| 2048-bit search | 16 ranks | 3 | node01 | 60.0 | 1568 | 19 |
| 2048-bit search | 16 ranks | 4 | node02 | 60.0 | 1698 | 12 |
| 2048-bit search | 16 ranks | 5 | node02 | 60.1 | 1718 | 11 |
| 2048-bit search | 16 ranks | 6 | node02 | 60.0 | 1623 | 16 |
| 2048-bit search | 16 ranks | 7 | node02 | 60.0 | 1587 | 18 |
| 2048-bit search | 16 ranks | 8 | node03 | 60.0 | 1605 | 17 |
| 2048-bit search | 16 ranks | 9 | node03 | 60.0 | 1571 | 19 |
| 2048-bit search | 16 ranks | 10 | node03 | 60.0 | 1662 | 14 |
| 2048-bit search | 16 ranks | 11 | node03 | 60.0 | 1698 | 12 |
| 2048-bit search | 16 ranks | 12 | node04 | 60.4 | 1672 | 14 |
| 2048-bit search | 16 ranks | 13 | node04 | 60.0 | 1699 | 12 |
| 2048-bit search | 16 ranks | 14 | node04 | 60.0 | 1473 | 24 |
| 2048-bit search | 16 ranks | 15 | node04 | 60.0 | 1640 | 15 |
| 4096-bit search | 16 ranks | 0 | node01 | 120.1 | 531 | 1 |
| 4096-bit search | 16 ranks | 1 | node01 | 120.1 | 531 | 1 |
| 4096-bit search | 16 ranks | 2 | node01 | 120.2 | 455 | 5 |
| 4096-bit search | 16 ranks | 3 | node01 | 122.1 | 464 | 5 |
| 4096-bit search | 16 ranks | 4 | node02 | 120.2 | 549 | 0 |
| 4096-bit search | 16 ranks | 5 | node02 | 120.0 | 511 | 2 |
| 4096-bit search | 16 ranks | 6 | node02 | 120.0 | 511 | 2 |
| 4096-bit search | 16 ranks | 7 | node02 | 120.1 | 530 | 1 |
| 4096-bit search | 16 ranks | 8 | node03 | 120.1 | 474 | 4 |
| 4096-bit search | 16 ranks | 9 | node03 | 120.2 | 549 | 0 |
| 4096-bit search | 16 ranks | 10 | node03 | 120.2 | 549 | 0 |
| 4096-bit search | 16 ranks | 11 | node03 | 120.0 | 473 | 4 |
| 4096-bit search | 16 ranks | 12 | node04 | 120.2 | 475 | 4 |
| 4096-bit search | 16 ranks | 13 | node04 | 120.2 | 512 | 2 |
| 4096-bit search | 16 ranks | 14 | node04 | 120.1 | 473 | 4 |
| 4096-bit search | 16 ranks | 15 | node04 | 120.1 | 474 | 4 |

### Peak memory per rank

- job 66: largest per-rank resident memory: 25 MB
- job 67: largest per-rank resident memory: 26 MB
- job 68: largest per-rank resident memory: 25 MB
- job 69: largest per-rank resident memory: 27 MB
- job 70: largest per-rank resident memory: 25 MB
- job 71: largest per-rank resident memory: 25 MB
- job 72: largest per-rank resident memory: 27 MB
- job 73: largest per-rank resident memory: 27 MB

Each configuration was run once, so treat small differences in wall time as noise.
