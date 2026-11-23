# Verification matrix and observed evidence

**Snapshot:** 2026-11-23. Source: administrative terminal captures and four-node Slurm `srun` outputs. Tests labeled **passed** were observed in supplied output; tests labeled **not tested** are not claims of failure.

| Component | Test | Result | Evidence |
|---|---|---|---|
| Admin OS | `/etc/rocky-release` | PASS | Rocky Linux 9.8 |
| Core services | `systemctl is-active` | PASS | `warewulfd`, `munge`, `slurmctld`, `dhcpd`, `nfs-server`, `firewalld`, `chronyd` active |
| Scheduler | `sinfo -N -l` | PASS | `node01`–`node04` idle, 4 CPUs and 15,000 MB each |
| Four-node execution | `srun ... /usr/bin/hostname` | PASS | Four distinct hostnames returned |
| Slurm consistency | `sha256sum /etc/slurm/slurm.conf` | PASS | Identical SHA-256 on admin and all four nodes |
| Compute processes | `systemctl is-active` on four nodes | PASS | `slurmd`, `munge`, `chronyd` active |
| User identity | `id slurm` on five hosts | PASS | UID 977, GID 976 everywhere |
| Compute packages | `rpm -q` on four nodes | PASS | Slurm daemon, Munge, OpenMPI and NFS utils match versions |
| Shared `/home` | `findmnt` on four nodes | PASS | NFSv4.2 `rw` from admin across all nodes |
| `/opt` auto-mount | `findmnt -T /opt` | NOT MOUNTED | Expected with `noauto` profile setting, not a failure |
| NFS effective policy | `exportfs -v` | OBSERVED | `/home root_squash`, `/opt ro,no_root_squash` |
| Admin clock | `timedatectl`, `chronyc tracking` | PASS | Synchronized; stratum 4 and ~0.218ms slow at observation |
| Compute clock offset | Per-node `chronyc tracking` | NOT TESTED | `chronyd` active only, offset unmeasured |
| Fresh PXE reboot | Power-cycle boot validation | NOT TESTED | No controlled reboot experiment in this audit |
| MPI smoke test after audit | Compiled 4-node MPI application | NOT TESTED | Slurm hostname test is not an MPI communication test |
| cgroup resource enforcement | CPU/RAM containment | NOT ENABLED | `ConstrainCores=no`, `ConstrainRAMSpace=no` |
| Network exposure | Upstream access tests | NOT TESTED | Firewall declarations alone don't establish reachability |

## A reproducible lightweight allocation test

```bash
srun --partition=debug --nodes=4 --ntasks=4 --ntasks-per-node=1 \
  --time=00:02:00 /usr/bin/hostname
```

Expected outcome is one distinct hostname per compute node, in **any** order. This command allocates four tasks and therefore does use scheduler resources, but makes no configuration changes.

## Configuration-consistency test

```bash
sha256sum /etc/slurm/slurm.conf
srun --nodes=4 --ntasks=4 --ntasks-per-node=1 --time=00:02:00 \
  sha256sum /etc/slurm/slurm.conf
```

Historical digest across all five hosts: `e6286b92556619ddabc2038a47a60d17f9d2affc838a5f380428e544eeeed914`. A changed checksum in the future isn't necessarily wrong; investigate versioned deployments before declaring drift or reverting anything.

The full outcomes and caveats live in [Live Configuration](LIVE_CONFIGURATION.md). For human-friendly current-state inspections, see [Operations](OPERATIONS.md).
