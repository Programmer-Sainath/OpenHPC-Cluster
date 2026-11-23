# Project Timeline — August to November 2026

**Project:** Five-node OpenHPC cluster at DPS–Modern Indian School, Qatar
**Scope:** One administrator and four diskless compute nodes, built from repurposed desktop computers.
**Status at 23 November 2026:** Core infrastructure deployed; Slurm task launch verified across all four compute nodes; six simulation workloads developed and their experimental outputs documented.

> **How to read this timeline:** This is a retrospective account compiled from team recollections, historical troubleshooting notes, repository artifacts and the live verification performed on **23 November 2026**. The month-level sequence is approximate where the original logs do not establish an exact date. In particular, early installation attempts, later reinstallations and configuration changes should not be mistaken for a single uninterrupted deployment. The [troubleshooting log](../troubleshooting.md) retains individual incident notes, and [live configuration](LIVE_CONFIGURATION.md) describes the verified final state.

## August 2026 — Planning, hardware preparation and initial administration

**Focus: establishing the management node and a working networking foundation.**

- **Project design and available hardware.** The team began organizing repurposed school desktop PCs into an administrator-plus-compute-node cluster. Early plans contemplated other node counts and Linux distributions (including RHEL/AlmaLinux), but the deployed project ultimately settled on **one administrator and four compute nodes running a Rocky Linux-based environment**. Hardware and processor expectations changed as the available PCs were inventoried.
- **Administrator storage and Linux installation.** The administrator's operating system was installed on a **Lexar 128 GB nominal SATA SSD** as part of the initial setup. The later observed disk capacity was **119.2 GiB**. The development history includes subsequent OS installation/reinstallation; an October 1 filesystem record should not be interpreted as the date of the very first installation.
- **Initial network and remote access.** The team configured Ethernet connectivity for the private cluster LAN and set up **Tailscale** to reach the administrator remotely for development and troubleshooting. SSH provided the terminal interface. Remote access did not replace the physically connected provisioning network.
- **Internet access for the administrator.** A **TP-Link TG-3468 Gigabit PCIe network adapter** was added to give the administrator a second Ethernet connection. This separated the school/internet connection from the cluster-facing link. The compute nodes were not independently provided with school-network internet access as part of this design.
- **Early service preparation.** Initial work began on the Linux packages, OpenHPC ecosystem, host networking and firewall rules needed for provisioning and distributed computing. These settings were revised during the following months rather than finalized in August.
- **Early platform decisions and troubleshooting.** **Eric Bipin Philip** documented the team's early assessment of RHEL's developer-subscription limitations and the historical proposal to use AlmaLinux. This was an intermediate planning decision, **not** the final Rocky Linux deployment. Eric also contributed to the initial infrastructure setup and diagnosing early installation issues as the project moved toward provisioning.

**Outcome:** A management-machine foundation and a defined direction for building a diskless multi-node Linux cluster. August activities are reconstructed from team recollection; exact installation and purchase dates have not been independently established.

## September 2026 — Network revisions, Warewulf provisioning and overlay work

**Focus: getting compute nodes defined, provisioned and connected to the administrator.**

- **Switch and topology changes.** An earlier Cisco Catalyst switch was replaced during development by the **TP-Link LS1016G 16-port unmanaged Gigabit Ethernet switch** used in the final assembly (reported around late September). The private network and node addressing were also revised from earlier experimental `192.168.1.x` values toward the deployed `192.168.10.0/24` design.
- **Warewulf provisioning.** Work progressed on the `rockylinux-9` compute image, node definitions, profiles, DHCP, TFTP/iPXE and diskless boot configuration. **Eric Bipin Philip** contributed to the initial Warewulf/OpenHPC installation and Linux provisioning setup. The final topology uses administrator `192.168.10.2` and node addresses `192.168.10.10`–`192.168.10.13`; these addresses describe the final design, not necessarily the first September configuration.
- **System and runtime overlays.** The team configured and debugged Warewulf overlays so that compute nodes would receive their required host, networking, account and other runtime settings. The historical troubleshooting log records **invalid Warewulf flags**, **missing runtime overlay assignments** and the need to rebuild overlays after correction. Runtime overlay work was underway by September and continued through integration.
- **Network and image troubleshooting.** Work included investigating unreachable nodes/packet loss, overlay network configuration and kernel-module-path issues when building the image. **Eric helped troubleshoot early Linux infrastructure, Warewulf/OpenHPC setup and provisioning problems alongside the team.** The historical incident log names Aayush and Shanmukha for certain individual fixes; Eric's broader troubleshooting contribution should not be mistaken for sole responsibility for those recorded resolutions. These were iterative investigations across the September–October period, not necessarily resolved in one session.
- **Start of computational workloads.** **Aayush Pal** began developing the team's scientific and mathematical simulations while the cluster infrastructure was still being stabilized. Simulation development continued in parallel with provisioning.

**Outcome:** The main provisioning architecture was established, but network, image and node-configuration problems still required further integration work. See [Provisioning](PROVISIONING.md) and the [historical issue log](../troubleshooting.md).

## October 2026 — Reinstallation, Slurm integration and persistent troubleshooting

**Focus: moving from provisioned machines to a usable, scheduled compute cluster.**

- **Administrator rebuild and configuration.** The admin machine's `/etc/fstab` includes an OS installation record dated **1 October 2026**, supporting a subsequent installation/rebuild during the development period. Historical configuration activity from early October documents the private network, Warewulf image/profile setup, NFS, Munge, firewall rules and Slurm integration.
- **Compute-node registration.** The four node definitions were configured for Warewulf, with their hardware addresses and private IP assignments. Profile and overlay settings were repeatedly checked and corrected so nodes could receive usable configuration at boot.
- **Slurm and Munge setup.** **Shanmukha Sainath Kasireddy** led the Slurm configuration and scheduler integration, including controller/compute-node settings, the `debug` partition, Munge authentication and scheduled task execution. Shared `/home` storage and the environment required for workloads were also integrated.
- **The node-state problem.** For approximately **five days**, Slurm node-state output (the `sinfo` command, rather than CIFS storage) repeatedly showed unresponsive or unavailable states, described by the team as `idle*` or `unknown*`. The team investigated services, networking, provisioning and node communication. The precise single cause and final corrective command are **not firmly established in the surviving record**; the problem should not be attributed to one specific setting without evidence.
- **Continued problem-solving.** **Eric supported ongoing troubleshooting of provisioning and Linux/OpenHPC infrastructure**, while **Shanmukha** concentrated on Slurm configuration, scheduling and node-state issues and **Aayush** contributed to overlay-related fixes. The team worked through the previously recorded Warewulf option/overlay issues, network packet loss, image/kernel-path discrepancies and recurring firewall or service configuration changes. Historical commands remain in the repository as references, **not** an installation script to replay on a live system.
- **Parallel simulation development.** Aayush continued developing the majority of the workloads. Shanmukha developed the remaining workloads and worked on running jobs through Slurm. The team's reported distribution was **four simulations primarily developed by Aayush and two primarily developed by Shanmukha**; this does not imply that every workload was completed in October.

**Outcome:** The provisioning, authentication, storage and job-scheduling components were integrated and progressively debugged. Stable four-node availability is documented definitively in November, not retroactively claimed for every day in October.

## November 2026 — Operational cluster, six workloads, benchmarking and publication

**Focus: demonstrating distributed execution and preserving reproducible results.**

- **Cluster reached a stable scheduled state.** All four compute nodes eventually reported **`idle`**, available for work in the `debug` Slurm partition. The administrator controlled dispatch; the diskless compute nodes ran tasks and used shared storage.
- **Six computational workloads were assembled and documented.** The [Simulation Workloads branch](https://github.com/Programmer-Sainath/OpenHPC-Cluster/tree/Simulation-Workloads) contains **Sieve of Eratosthenes**, **Miller–Rabin primality testing**, **Dask-based primality search**, **Chudnovsky π calculation**, **hydrogen orbital visualization**, and **Lattice Boltzmann fluid dynamics (von Kármán vortex street)**. Some are distributed MPI workloads; Dask's recorded experiments ran on a single node, and the archived Chudnovsky calculations used a serial process. These distinctions matter when describing the project.
- **Execution evidence and results.** The team recorded Slurm submission commands, timings, selected logs, simulation outputs and performance measurements. The fluid-dynamics archive records a **21 November 2026** run set in which the same problem took **1,059.16 seconds with one MPI rank** and **88.26 seconds with sixteen ranks**, a measured **12.00× speedup** on that workload. This is a comparison **within the cluster**, not a controlled benchmark against an ordinary laptop.
- **Scientific and educational objective.** The system demonstrates practical **high-performance and parallel-computing principles**—diskless provisioning, resource allocation, distributed processes and workload scaling—using repurposed school computers. Its results are **not** evidence of a particular supercomputer ranking or of universal speedups over consumer PCs.
- **23 November: final live verification.** On Rocky Linux **9.8**, `sinfo -N -l` showed **node01–node04 idle**, each with **four Slurm CPUs** and **15,000 MB configured memory**. Munge, the Slurm controller and Warewulf services were active. A four-node Slurm test launched one hostname task on **each** compute node; identical `/etc/slurm/slurm.conf` checksums were observed across the administrator and all four nodes.
- **23 November: infrastructure evidence and documentation.** The team captured hardware models, installed package versions, Warewulf image/profile/overlays, NFS exports and mounts, firewall zones, DHCP, Chrony state, and service-account consistency. The **shared `/home` NFSv4.2 mount** was confirmed on every compute node. The [Infrastructure branch](https://github.com/Programmer-Sainath/OpenHPC-Cluster/tree/HPC-Cluster-Infrastructure) and simulation branch were updated with technical references, limitations, troubleshooting notes and photographs of the cluster.

**Outcome:** The project's core build and documentation were completed, with an operational **five-PC educational HPC cluster** and six archived computational workloads. End-to-end Slurm task launch was verified on **23 November 2026**. Fresh post-reboot PXE recovery, independent MPI re-testing after the documentation audit, security hardening and further scientific validation remain separate follow-up work.

## Contributors and responsibilities

| Member | Contributions recorded during the project |
|---|---|
| **Shanmukha Sainath Kasireddy** | Project lead; main cluster setup and administration; Slurm integration and troubleshooting; development of two computational workloads and simulation execution/documentation |
| **Eric Bipin Philip** | Initial Warewulf/OpenHPC setup and Linux provisioning; troubleshooting of installation, configuration and infrastructure problems alongside the team; early OS-platform research |
| **Aayush Pal** | Development of approximately four computational workloads; simulation execution and performance-analysis work; contributions to Warewulf overlay troubleshooting |

This table summarizes the team's reported roles; it is not an assertion that individual tasks were carried out alone. The project maintained work by several contributors throughout the development period.

## Evidence and limits of this reconstruction

- **Live-observed:** [Live Configuration](LIVE_CONFIGURATION.md), [Validation](VALIDATION.md), [Hardware Inventory](HARDWARE_INVENTORY.md), and [Storage](STORAGE.md) record the dated, verified November deployment state.
- **Historical issues:** [`troubleshooting.md`](../troubleshooting.md) records six incidents and their originally attributed resolutions. These should not be assigned exact dates without original timestamped evidence.
- **Computational results:** The [Simulation Workloads branch](https://github.com/Programmer-Sainath/OpenHPC-Cluster/tree/Simulation-Workloads) contains individual results, job scripts and selected logs. Speedup figures are meaningful only with their stated workload and baseline.
- **Retrospective recollection:** August and September activity and much of the October sequence were supplied by team recollection. Precise ordering and dates may be refined if dated commit history or original terminal logs establish them.
