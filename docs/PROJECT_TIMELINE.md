# Project timeline and configuration changes

This document keeps the students' early decisions distinct from the **verified 2026-11-23 deployed system**. Exact project milestone dates are included only when established in records; undated events remain undated.

| Phase | What happened | Status |
|---|---|---|
| Initial proposals (historical) | RHEL/AlmaLinux ideas and a 10–12-node target appeared in early notes | Plans, **not** final hardware |
| Hardware acquisition | Repurposed Lenovo desktops supplied; CPU availability differed from early expectations | Historical issue log |
| Network revision | Earlier Cisco Catalyst switch was replaced by a TP-Link LS1016G unmanaged 16-port Gigabit switch | Team inventory; final layout |
| Deployment | Rocky Linux 9 with Warewulf, diskless compute nodes, NFS, Munge, Slurm and OpenMPI | Actual running deployment |
| **2026-11-23** | Admin confirmed Rocky Linux 9.8; Warewulf 4.7; four compute nodes idle; task launch on all four | **Live verified** |
| **2026-11-23** | Captured DHCP, Slurm, Warewulf profiles, firewall, NFS mounts, RPM versions, NTP and Slurm checksums | **Live verified** |
| Future | Supervisor-approved security hardening, MPI smoke test, PXE recovery and scientific accuracy validation | Proposed, **not implemented** |

All six numbered historical incidents and individual attribution remain in [`../troubleshooting.md`](../troubleshooting.md) as originally recorded, with explicit chronology warnings. Avoid rewriting the project's history to look like everything worked on the first attempt.
