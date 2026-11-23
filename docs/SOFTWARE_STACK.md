# Software stack and compatibility inventory

Admin system observed on **2026-11-23**: Rocky Linux **9.8 (Blue Onyx)**. Exact installed RPM versions, not just upstream major releases:

| Component | Installed RPM/version | Function |
|---|---|---|
| Warewulf | `wwctl 4.7.0-1`, `warewulf-ohpc-4.7.0-350.ohpc.2.1` | Image, profiles, DHCP/PXE, overlays |
| Slurm | `slurm-22.05.11-2.el9` | Workload scheduler and controller |
| Munge | `munge-0.5.13-14.el9_7` | Slurm authentication |
| OpenMPI | `openmpi-4.1.1-7.el9` | MPI applications |
| NFS | `nfs-utils-2.5.4-42.el9` | Shared `/home` |
| Chrony | `chrony-4.8-1.el9` | Clock synchronization |
| HWLOC | `hwloc-libs-2.4.1-6.el9_7` | Hardware locality libraries |

Each compute node reported the same RPM versions of `slurm-slurmd`, `munge`, `openmpi`, and `nfs-utils`; `chronyd` was active on each. A full `rpm -qa` dump of images was not collected. The exact OpenHPC release bundle/metapackage was not independently determined; **do not substitute the Warewulf RPM version as the OpenHPC distribution version**.

Slurm controller is `/etc/slurm/slurm.conf` and matching copies exist on the four compute nodes. Slurm cgroup settings are documented under [`slurm/cgroup.conf`](../slurm/cgroup.conf). The sampled files reflect the installed versions and are **not generally portable** to a newer Slurm or Warewulf without reviewing changes and migration notes.

Useful read-only Linux Bash checks:

```bash
cat /etc/rocky-release
rpm -q warewulf-ohpc slurm munge openmpi nfs-utils chrony
sudo wwctl version
sinfo -N -l
```

**Documentation references:** [Warewulf 4.7 notes](https://warewulf.org/docs/v4.7.x/release/v4.7.0.html), [Warewulf security](https://warewulf.org/docs/main/server/security.html), [Slurm cgroup config](https://slurm.schedmd.com/cgroup.conf.html). Consult documentation corresponding to the deployed version before executing upgrades.
