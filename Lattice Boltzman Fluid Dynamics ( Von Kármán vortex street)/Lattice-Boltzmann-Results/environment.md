# HPC environment — captured from the actual cluster

**Source of truth:** `logs/hardware/admin.txt` and `logs/hardware/node01.txt` through `node04.txt` from the uploaded evidence archive, captured on **21 November 2026 at approximately 01:03 Qatar time (UTC+03:00)**. These are actual snapshots from the cluster, not processor models inferred from earlier descriptions.

## 1. Hardware inventory per node

| Node | Role | CPU model (from `lscpu`) | Physical cores | Memory (`free -h`, total) | Active NIC reported speed | Kernel |
|---|---|---|---:|---|---|---|
| **admin** | SSH/admin + submission | Intel(R) Core(TM) i5-4460S CPU @ 2.90GHz | 4 | **15Gi** | enp2s0: 1000 Mbps, enp3s0: 1000 Mbps | `5.14.0-687.53.1.el9_8.x86_64` |
| **node01** | compute | Intel(R) Core(TM) i5-2400 CPU @ 3.10GHz | 4 | **15Gi** | enp3s0: 1000 Mbps | `5.14.0-687.56.1.el9_8.x86_64` |
| **node02** | compute | Intel(R) Core(TM) i5-2400 CPU @ 3.10GHz | 4 | **15Gi** | enp3s0: 1000 Mbps | `5.14.0-687.56.1.el9_8.x86_64` |
| **node03** | compute | Intel(R) Core(TM) i5-2400 CPU @ 3.10GHz | 4 | **15Gi** | enp3s0: 1000 Mbps | `5.14.0-687.56.1.el9_8.x86_64` |
| **node04** | compute | Intel(R) Core(TM) i5-2400 CPU @ 3.10GHz | 4 | **15Gi** | enp3s0: 1000 Mbps | `5.14.0-687.56.1.el9_8.x86_64` |

**Hardware correction:** All four *compute* machines identify as **Intel Core i5-2400 @ 3.10 GHz**, while the separate *admin* machine identifies as **Intel Core i5-4460S @ 2.90 GHz**. Older project descriptions calling all compute nodes i5-4460 were inaccurate; this table is based on the live machines' `lscpu` output. These models have **4 physical cores per node and 1 hardware thread per core** in the captured configuration.

`free -h` reports **15 GiB** Linux-visible RAM per machine, consistent with roughly 16 GB nominal installed RAM; installed DIMM details and DDR generation were **not independently inventoried** by this export. Four compute nodes therefore provide 16 physical cores and approximately 60 GiB of OS-reported RAM in total. The admin's memory is separate and was not allocated to the 16-rank LBM production computation. Values under `Mem: ... available` in the snapshots are *not* peak-memory observations from the simulation.

The interface speed files reported **1000 Mb/s** on each compute node's `enp3s0` NIC and on the admin's `enp2s0` and `enp3s0` NICs. This is reported interface link speed, **not measured MPI network throughput**, and does not prove a 1000 Mb/s sustained application transfer rate. Hardware model-to-ThinkCentre chassis assignments were not recorded.

## 2. Software and execution environment

| Component | Verified version/configuration | Evidence |
|---|---|---|
| Operating system | **Rocky Linux 9.8 (Blue Onyx)** on all 5 machines | `/etc/os-release` in each node snapshot |
| Admin kernel | `5.14.0-687.53.1.el9_8.x86_64` | `admin.txt` |
| Compute-node kernels | `5.14.0-687.56.1.el9_8.x86_64` on nodes 01–04 | `node01.txt`–`node04.txt` |
| Slurm | **22.05.11** (admin output of `sinfo --version`) | `admin.txt` |
| Open MPI | **4.1.1** (`mpirun --version` on admin) | `admin.txt` |
| GNU C compiler | **GCC 11.5.0** | `admin.txt` |
| Python | **3.9.25** | `admin.txt` |
| `imageio-ffmpeg` | **0.6.0** | `admin.txt` |
| Bundled FFmpeg runtime | **7.0.2-static**, H.264 / `libx264` present | `logs/enc-97.out` |
| MPI launch | Open MPI `mpirun --hostfile ... -np $SLURM_NTASKS` from a Slurm allocation | `code/historical/lbm.sbatch` |
| MPI networking | Open MPI `pml=ob1`, `btl=tcp,self,vader` and configured private LAN include | `code/historical/lbm.sbatch` |
| Slurm historical accounting | **Disabled** | `logs/slurm-accounting-status.txt` |

The actual log gives the original batch environment as it ran. Version reports were captured shortly after the run; they are the available evidence, not cryptographic proof that a package was unchanged between job execution and inventory capture.

## 3. Raw per-node outputs

Every report below includes the original kernel/OS/CPU information, RAM snapshot, and NIC link-speed query output:

- [`admin.txt`](logs/hardware/admin.txt) — administrative machine; two 1000 Mb/s interfaces.
- [`node01.txt`](logs/hardware/node01.txt) — compute node 1.
- [`node02.txt`](logs/hardware/node02.txt) — compute node 2.
- [`node03.txt`](logs/hardware/node03.txt) — compute node 3.
- [`node04.txt`](logs/hardware/node04.txt) — compute node 4.

For another snapshot in the future, use `code/environment_snapshot.sh` on the admin or `sbatch code/node-environment.sbatch` for four compute nodes. **Do not treat hardware free-memory snapshots as job maximum resident set size (MaxRSS).** Historical peak RSS is unavailable because Slurm accounting is disabled and no per-rank memory profiler was used.
