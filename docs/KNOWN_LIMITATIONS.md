# Known limitations and follow-up verification

The 2026-11-23 audit corrected historical reference files against available live observations. The following are **not necessarily malfunctions**, but must not be represented as completed validation:

1. **Provisioning resilience not tested:** no supervised reboot/PXE re-provisioning demonstration during this audit.
2. **Munge distribution unverified:** services were active, but actual secret transfer mechanism was not inspected; credentials must never be shared to public Git.
3. **Warewulf runtime overlay policy:** `secure: false`; `rootkey` is assigned. Requires administrator-led risk review; not proof of compromise.
4. **Campus-facing firewall exposure:** `public` zone lists DHCP/TFTP/NFS/Cockpit/Slurm/Warewulf; upstream filtering not tested. Needs school IT review.
5. **No cgroup CPU/RAM containment:** live `ConstrainCores=no`, `ConstrainRAMSpace=no`. Scheduling works but does not establish strict CPU/memory isolation under misuse.
6. **NFS `/opt` policy:** `ro,no_root_squash` on server; client `noauto`, so it was not mounted during the survey.
7. **Compute NTP accuracy unknown:** `chronyd` is active; individual NTP synchronization and offsets were not queried.
8. **MPI fresh smoke test unknown:** prior simulation archive has MPI jobs, but audit's current four-node test only launched hostnames through Slurm.
9. **Single controller and shared storage:** no observed high-availability backup controller or redundant NFS infrastructure.
10. **Full install reproducibility not guaranteed:** archived command notes came from historical work and are intentionally not an executable setup script; incompatible versions, service unit differences, NIC names and school network policies may differ.
11. **Permanent vs runtime firewalld zone mapping:** runtime has campus NIC in `public`; permanent `public` has no explicit interface and could still inherit zone from NetworkManager. Reboot persistence not tested.
12. **Public data minimization:** current repository may contain node MAC addresses from the original inventory. Do not add serial numbers, credentials, campus uplink addresses, or unsanitized network dumps.
13. **Software security updates:** deployed Slurm 22.05 is an older release; a planned compatibility/security review is advisable. No upgrade was performed.

Outstanding items are hypotheses or improvement opportunities, not observed failures. The system passed its observed Slurm task-launch and NFS mount checks.
