# Troubleshooting
This is a historical issue log: it preserves early plans, unsuccessful attempts,
intermediate networks, and the resolutions described by the students.
**Do not treat historical node counts, processor models, operating systems, or
IP addresses as descriptions of the final working five-PC Rocky Linux cluster.**
For the 23 November 2026 live-verified setup, see [docs/LIVE_CONFIGURATION.md](docs/LIVE_CONFIGURATION.md).

## This is a document detailing the issues faced by the team during the creation of the cluster.

### Issue 001:

> Historical planning only: the final deployed admin runs Rocky Linux 9.8,
> and the present cluster has one admin PC and four compute PCs, not 10–12 nodes.

Plan to use RHEL pivoted to Alma Linux due to the fact that RHEL (from Free dev subscription) has a limit of 10 images, and we are using ~10-12 nodes, to be on the safe side and not hit a paywall, we chose to move to a enterprise grade yet completely free Linux distribution which is Alma Linux -[Eric Philip Bipin] 

### Issue 002

> Early anticipated/received CPU list. The repository's current hardware inventory
> records i5-4460S (admin) and i5-2400 (compute); CPU hardware identification
> should be independently checked with `lscpu` before treating it as verified.

Expected CPU : i5-7400U  
CPU's Received : i5-4460 & i5-4460U  
This measurably reduces the expected calculations of the performance of this project: pivoting from a High performance cluster, to a learning cluster to prove our in-depth knowledge of bare metal on legacy systems and ability to optimize code/simulations. -[Shanmukha Sainath]

### Issue 003
Warewulf Syntax & Flag Discrepancy

Issue: Flag syntax errors (e.g., unknown flag errors) occurred when attempting to append or modify overlays via the command line using variations like --System-Overlays or --system-overlays+.

Resolution: Corrected the syntax to use sudo wwctl profile set default --system-overlays+=<overlay_name> and subsequently executed sudo wwctl overlay build to apply changes.-[Aayush Pal]

### Issue 004
Missing Overlay Assignments

Issue: Nodes node01 through node04 were initially missing runtime overlay definitions, preventing node-specific configurations from deploying at boot.

Resolution: Assigned default runtime and system overlays explicitly across the profiles and nodes before rebuilding the images (wwctl overlay build).-[Shanmukha Sainath]


### Issue 005

> Historical 192.168.1.x network. The live management network on 2026-11-23
> is 192.168.10.0/24, with controller at 192.168.10.2 and nodes .10–.13.

Network Connectivity & Packet Loss

Issue: Total packet loss (100% loss) occurred when trying to ping nodes (such as 192.168.1.101) post-provisioning.

Resolution: Updated network configurations within system overlays, restarted core management services (dhcpd and warewulfd), and re-provisioned/power-cycled the nodes.-[Shanmukha Sainath]


### Issue 006
Kernel Module Paths & Symbolic Links

Issue: Missing or mismatched kernel module paths during initial image compilation for rockylinux-9 images.
Resolution: Re-created required kernel symbolic links inside the container/chroot image environment prior to image generation.-[Shanmukha Sainath]
