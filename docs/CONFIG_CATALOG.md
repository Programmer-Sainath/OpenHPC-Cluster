# Configuration catalog and provenance

**IMPORTANT:** An extension `.conf` does not necessarily mean a file is a native daemon configuration. Several files in this repository are historical human-readable command logs. Do not `source`, execute, or copy them to `/etc` without version-specific and administrative review.

| Repository file | Source and status | Usage |
|---|---|---|
| [`warewulf/warewulf.conf`](../warewulf/warewulf.conf) | Observed live Warewulf config, 2026-11-23 | Read-only reference; security caveats |
| [`warewulf/dhcpd.conf.reference`](../warewulf/dhcpd.conf.reference) | Observed generated DHCP configuration | Read-only generated output; not hand-editable authority |
| [`warewulf/image-and-profile.conf`](../warewulf/image-and-profile.conf) | Historical image/profile commands | Historical record, **not** executable runbook |
| [`warewulf/node-setup.conf`](../warewulf/node-setup.conf) | Historical node add commands | Do not replay against existing nodes |
| [`warewulf/overlay-setup.conf`](../warewulf/overlay-setup.conf) | Historical overlay manipulation | Do not replay; overlays may hold secrets |
| [`slurm/slurm.conf`](../slurm/slurm.conf) | Observed live Slurm config | Reference, identical checksum on five hosts |
| [`slurm/cgroup.conf`](../slurm/cgroup.conf) | Observed live 3-setting excerpt | Reference, not resource constraint policy advice |
| [`slurm/controller-setup.conf`](../slurm/controller-setup.conf) | Historical package/UID/service steps | No replay on existing controller |
| [`slurm/compute-node-setup.conf`](../slurm/compute-node-setup.conf) | Historical image preparation | Verify image version before reuse |
| [`munge/munge.conf`](../munge/munge.conf) | Historical command notes | Never regenerate/copy active key blindly |
| [`munge/munge.key.example`](../munge/munge.key.example) | Warning-only placeholder | Not a usable key |
| [`nfs/exports`](../nfs/exports) | Live generated `/etc/exports` excerpt | Effective flags also documented separately |
| [`nfs/setup.conf`](../nfs/setup.conf) | Historical setup steps | No automatic execution |
| [`firewall/firewalld.conf`](../firewall/firewalld.conf) | Live inspection and risk notes | Read-only Bash checks only |
| [`networking/cluster-layout.conf`](../networking/cluster-layout.conf) | Historical/static node map + confirmed IPs | Data record, not shell syntax |
| [`system/packages.conf`](../system/packages.conf) | Historical image package commands | Unpinned, not a version-lock manifest |
| [`system/services.conf`](../system/services.conf) | Historical service enablement | Do not replay automatically |
| [`system/chrony.conf.reference`](../system/chrony.conf.reference) | Observed selected Chrony directives | Partial reference |
| [`verification/commands.conf`](../verification/commands.conf) | Linux Bash checks and a small Slurm job | Review each line; not full installer |
| [`verification/healthcheck.sh`](../verification/healthcheck.sh) | Auditable helper script | Inspects system; opt-in small Slurm job |

See [Live Configuration](LIVE_CONFIGURATION.md) for values, [Build Guide](CLUSTER_BUILD_GUIDE.md) for safe sequencing, and [Known Limitations](KNOWN_LIMITATIONS.md) for unverified or risky behaviors.
