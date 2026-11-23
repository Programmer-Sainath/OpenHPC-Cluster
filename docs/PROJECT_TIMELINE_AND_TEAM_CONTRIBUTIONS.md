# Project Timeline and Team Contributions — August to November 2026

**Project:** Student-built OpenHPC / high-performance computing cluster, DPS–Modern Indian School, Qatar
**Development period:** August–November 2026
**Final configuration:** One administrator and four diskless compute nodes (five PCs), running a Rocky Linux-based stack
**Project lead:** **Shanmukha Sainath Kasireddy**
**Team:** **Shanmukha Sainath Kasireddy**, **Eric Bipin Philip**, and **Aayush Pal**

## Team contribution summary

| Member | Role and documented contributions |
|---|---|
| **Shanmukha Sainath Kasireddy** | Led cluster integration and administration, including the admin OS, PCIe network interface, private networking and NFS. Built the four-node runtime overlay with Eric. After that handoff, configured Munge, the firewall and Slurm, verified the cluster, and handled task allocation and job submission for all six workloads. Developed **two** workloads: Lattice Boltzmann fluid dynamics (von Kármán vortex shedding) and the Chudnovsky π calculation. |
| **Eric Bipin Philip** | Set up Tailscale, installed OpenHPC and Open MPI, identified the compute nodes by IP and MAC address, and registered and provisioned them with Warewulf. Built the runtime overlay with Sainath and helped diagnose Linux and node communication issues. |
| **Aayush Pal** | Developed **four** workloads: the distributed Sieve of Eratosthenes, Miller–Rabin primality testing, Dask-based primality search, and hydrogen orbital visualization. Contributed to performance analysis and resolved the Warewulf overlay flag issue. |

**Shared troubleshooting.** Sainath, Eric and Aayush jointly resolved the Slurm node-response issue that appeared as `idle*` and `unknown*` in `sinfo`.

> **Chronology and attribution:** This is a retrospective development history based on the team's account, the [historical troubleshooting log](../troubleshooting.md), repository materials, and the deployment verification performed on **23 November 2026**. Where no dated record exists, activities are attributed to a **month or development phase**, not an invented day. Some tasks overlapped or had to be repeated after reinstallation. Named ownership reflects who primarily worked on each subsystem; it does not imply others never helped. The final configuration is documented in [Live Configuration](LIVE_CONFIGURATION.md).

## August 2026 — Hardware, administrator setup, internet and remote access

**Goal:** Turn available school PCs into a manageable Linux cluster, first establishing a functional administrator machine.

1. **Hardware organization and project leadership — Shanmukha Sainath Kasireddy.** Sainath coordinated the core build of a cluster using repurposed desktop computers. The deployment eventually settled on **one administrator plus four compute nodes**, rather than the larger node counts described in early planning. **Eric Bipin Philip** assisted with initial infrastructure work. Eric also documented an early discussion about RHEL subscription limits and a possible move to AlmaLinux; those were **historical proposals**, not the final Rocky Linux environment.
2. **Administrator operating system and storage — primarily Sainath.** The administrator's Linux installation was prepared using a **Lexar 128 GB SATA SSD**. The eventual disk was observed as approximately **119.2 GiB**. Installation and configuration were revisited later; the October filesystem metadata should not be treated as the date of the first install.
3. **Initial private networking and dual-NIC arrangement — primarily Sainath.** The team established an administrator-facing cluster LAN and obtained a **TP-Link TG-3468 Gigabit PCIe Ethernet adapter**. The extra adapter allowed the administrator to connect to the school/internet network separately from the private compute-node switch. This did **not** give each compute node an independent campus/internet connection. Sainath subsequently maintained and refined the private networking and firewall configuration.
4. **Tailscale remote administration — Eric.** **Eric Bipin Philip installed and configured Tailscale**, enabling the team to access the administrator remotely. Team members used the remote path together with SSH to perform administrative and debugging work when not physically at the cluster.
5. **Initial HPC software installation — Eric.** During the **August–September initial setup phase**, **Eric installed OpenHPC and OpenMPI and set up the initial OpenMPI environment**. These early installations were an essential foundation, while later integration, service configuration and independent MPI runtime validation remained separate work.
6. **Early troubleshooting — Sainath and Eric.** Both worked through initial Linux, interface, connectivity and installation challenges. The team adjusted its plan as actual hardware and software requirements became clearer.

**August outcome:** The project had an administrator-machine foundation, administrator-only upstream connectivity, remote team access and an initial OpenHPC/OpenMPI installation path. Exact purchase and first-installation dates are not independently established.

## September 2026 — Compute-node registration, Warewulf and runtime overlays

**Goal:** Define the compute nodes, provision their Linux environment and make the administrator-to-node network reliable.

1. **Compute-node identification and registration — Eric.** **Eric Bipin Philip identified the compute nodes' IP-address and MAC-address information, registered the compute nodes from the administrator, and contributed to their initial Warewulf definitions.** The final private addressing uses administrator `192.168.10.2` and `node01`–`node04` at `192.168.10.10`–`192.168.10.13`. Earlier experimental addresses in the troubleshooting log were different and must not be confused with this final network.
2. **Initial Warewulf configuration — Eric; continuation and main integration — Sainath.** Eric handled the **early Warewulf setup**, including the initial node-provisioning configuration while Sainath was not always available. **Sainath then took primary responsibility** for the continuing Warewulf image, profile, node, network and provisioning work, with Eric assisting as needed. The final system uses a `rockylinux-9` node image and diskless PXE provisioning.
3. **Network switch and topology revision — team; later network administration — Sainath.** An earlier Cisco switch was replaced by the **TP-Link LS1016G 16-port Gigabit switch**, used in the final hardware assembly. Sainath managed the follow-on cluster network settings, firewall rules, node communications and service integration. The historical `192.168.1.x` addresses were superseded by the final `192.168.10.0/24` cluster LAN.
4. **Four-node runtime overlay build.** After Eric registered and provisioned the compute nodes, **Sainath and Eric** built the runtime overlay together. **Sainath** corrected the system and runtime overlay assignments (Issue 004) and checked the overlay and kernel status of all four nodes with `sudo wwctl node status`. **Aayush** corrected the Warewulf overlay flag syntax (Issue 003).
5. **Provisioning and network fault investigation — mainly Sainath and Eric, with Aayush contributing.** The team investigated compute nodes not responding, packet loss after provisioning, overlay/image setup, service configuration and kernel-module-path problems. The original log attributes the network connectivity recovery and kernel path/symlink correction to **Sainath** (**Issues 005 and 006**). These are documented historical fixes, not evidence that all provisioning problems happened on a single day.
6. **Simulation development begins — primarily Aayush.** **Aayush Pal** started developing computational workloads while **Sainath and Eric** focused on completing the cluster's infrastructure and resolving provisioning issues. This simulation work continued through October and November.

**September outcome:** All four compute nodes were being defined and provisioned, with major progress on Warewulf profiles and runtime overlays. The basic environment existed, but networking and reliable end-to-end scheduling still required troubleshooting.

## October 2026 — Primary infrastructure integration, Slurm and the unresponsive-node issue

**Goal:** Finish the shared Linux cluster services, integrate the job scheduler and resolve compute-node availability problems.

### Infrastructure configurations — Sainath as primary implementer

By this phase, **Shanmukha Sainath Kasireddy was the principal builder and administrator**, building on Eric's early installation and node-registration work. Sainath was primarily responsible for configuring, integrating, revising and troubleshooting the following components:

| Component | Principal responsibility and purpose |
|---|---|
| **Private networking** | **Sainath:** administrator/compute-node connectivity, interface and addressing adjustments, and connectivity checks. **Eric** had handled the earlier Tailscale setup and initial MAC/IP discovery and registration. |
| **Firewall (`firewalld`)** | **Sainath:** configured and revisited firewall rules and network zones so cluster services could communicate across the private network. |
| **Warewulf provisioning** | **Sainath:** continued image/profile, node and overlay integration, then handled provisioning fixes. **Eric** performed initial setup; **Aayush** assisted with overlay-specific issues. |
| **Runtime/system overlays** | Eric and Sainath built the runtime overlay together. Sainath handled overlay assignments and verified all four nodes. Aayush corrected the overlay command syntax. |
| **NFS and shared storage** | **Sainath:** configured the NFS service, exports and the shared `/home` environment needed by compute nodes and scheduled workloads. |
| **Munge authentication** | **Sainath:** configured and integrated Munge authentication between the Slurm controller and compute nodes. |
| **Slurm controller, nodes and partitions** | **Sainath:** **entire primary Slurm setup**—controller and compute-node service integration, node resource definitions, `debug` partition, authentication/scheduling configuration and Slurm testing. |
| **System services and verification** | **Sainath:** checked service status, node communication, Slurm state, shared mounts, system compatibility and readiness for workloads. |
| **OpenMPI availability** | **Eric:** initial OpenMPI installation and environment setup; subsequent cluster-level execution depended on the rest of the infrastructure configured by Sainath. |

These activities were iterative; some had begun earlier or were repeated after the administrator's OS was rebuilt/reconfigured. The `/etc/fstab` metadata records an **October 1** filesystem creation date, but it does not establish the date of every configuration step.

### Major troubleshooting: `idle*` and `unknown*`

- **Problem (approximately five days):** Slurm's `sinfo` output sometimes displayed compute nodes as **`idle*`** or **`unknown*`** instead of a healthy **`idle`** state. The trailing `*` indicates a Slurm node that is **not responding**; `idle` without the marker indicates a node reported available to accept jobs. This was a **Slurm/node-communication issue**, not a CIFS shared-storage status message.
- **Who worked on it:** **Sainath, Eric and Aayush** investigated it as a team. **Sainath** led Slurm configuration and reconfiguration, **Eric** assisted with Linux/infrastructure and provisioning diagnostics, and **Aayush** contributed to relevant node and overlay troubleshooting.
- **Investigation:** Work involved revisiting Slurm controller/daemon settings, node definitions, configuration consistency, services, Munge authentication, provisioning state and network communication. **A Slurm configuration or communication mismatch is a plausible explanation, but the exact root cause and the single decisive fix were not preserved in the available logs.** It would be misleading to record one guessed setting as a confirmed cause.
- **Resolution:** Following joint troubleshooting and further **Slurm reconfiguration led by Sainath**, the compute-node state was eventually restored to **`idle`**. The first fully documented four-node `idle` snapshot was captured in November.

### Simulations in parallel

While infrastructure debugging continued, **Aayush Pal** developed most of the team's simulations. **Sainath** developed his own workloads and began preparing job runs, submissions and result collection on the Slurm-managed cluster. The reported final workload ownership was **four primarily developed by Aayush** and **two primarily developed by Sainath**; both strands of work continued into November.

**October outcome:** The private network, Warewulf provisioning, NFS, Munge and Slurm were integrated into a usable cluster environment. The team overcame a prolonged node-responsiveness problem, with the clearest verified healthy state recorded the following month.

## November 2026 — Four-node operation, six simulations, results and documentation

**Goal:** Demonstrate that the cluster could schedule work, run scientific workloads and preserve verifiable performance results.

1. **Four nodes ready for jobs.** Sainath, Eric and Aayush worked together to resolve the `idle*` and `unknown*` states in `sinfo`. All four compute nodes subsequently reported `idle` in the Slurm `debug` partition.
2. **Workload development.** Sainath developed Lattice Boltzmann fluid dynamics (von Kármán vortex shedding) and the Chudnovsky π calculation. Aayush developed the distributed Sieve of Eratosthenes, Miller–Rabin primality testing, Dask-based primality search, and hydrogen orbital visualization. The [Simulation Workloads branch](https://github.com/Programmer-Sainath/OpenHPC-Cluster/tree/Simulation-Workloads) contains their code and archived results.
3. **Cluster runs and performance analysis.** Sainath allocated resources and submitted all six workloads through Slurm using `sbatch`, setting MPI task counts for the parallel jobs that used MPI. The archived Dask runs used one node and the Chudnovsky jobs used one core. Aayush contributed to the performance analysis.
4. **Measured parallel speedup.** The **21 November** Lattice Boltzmann archive records **1,059.16 s with one MPI rank** and **88.26 s with sixteen ranks** on the tested problem—approximately **12.00× faster for that workload under the recorded cluster configurations**. This is evidence of effective parallel scaling; it is **not a controlled comparison to a gaming PC or laptop**, nor a claim that all six workloads had identical scaling.
5. **23 November: live four-node verification — coordinated by Sainath.** The running cluster reported Rocky Linux **9.8** on the administrator, with `node01` through `node04` **idle**, **4 Slurm CPUs and 15,000 MB Slurm-configured RAM per compute node** (16 compute CPUs / 60,000 MB scheduler-configured memory in total). `munge`, `slurmctld` and `warewulfd` were active on the administrator. A test using `srun --partition=debug --nodes=4 --ntasks=4 --ntasks-per-node=1 --time=00:02:00 /usr/bin/hostname` returned a hostname from **each of the four nodes**, proving Slurm remote task launch at the time tested. NFS `/home` mounts and consistent Slurm configuration checksums were also observed on every compute node.
6. **Publication and documentation — Sainath as project lead, with team contributions.** The team published infrastructure documentation (networking, firewall, Warewulf, overlays, Munge, NFS, Slurm, system verification, troubleshooting), results and photographs. **Eric's early infrastructure contributions and joint troubleshooting** and **Aayush's simulation and overlay work** are explicitly acknowledged in this history; the separate `CONTRIBUTORS.md` file is not required.

### What the project achieved

By **23 November 2026**, the team had built and documented a **working five-node educational HPC cluster** using repurposed school computers. It demonstrated **diskless node provisioning, shared storage, authenticated scheduling, four-node Slurm task launch and measurable parallel speedup** on an actual scientific workload. The team regards the infrastructure build and six-workload project as a success.

This is appropriately described as a **student-built HPC / educational supercomputing project**. Running simulations alone does not establish a formal *supercomputer* designation, and the recorded speedup does **not** prove that the system is faster than any particular modern gaming PC. Such a comparison would require matched workloads and hardware benchmarks. Likewise, full MPI re-testing after the documentation audit, fresh post-reboot provisioning recovery and further security/scientific validation were not all established by the November 23 snapshot.

## Supporting evidence and historical caveats

- [Historical troubleshooting](../troubleshooting.md): incident records, including **Eric** (early OS-platform research), **Aayush** (Warewulf flag correction), and **Sainath** (overlay assignments, packet loss/network fixes, kernel-path fix). Dates for these individual incidents were not independently logged.
- [Live Configuration](LIVE_CONFIGURATION.md) and [Validation](VALIDATION.md): dated November 23 observations of the running five-node cluster, including Slurm, NFS, service states and node task launch.
- [Hardware Inventory](HARDWARE_INVENTORY.md), [Networking and Security](NETWORKING_AND_SECURITY.md), [Provisioning](PROVISIONING.md) and [Storage](STORAGE.md): deployed hardware and configuration references.
- [Simulation Workloads branch](https://github.com/Programmer-Sainath/OpenHPC-Cluster/tree/Simulation-Workloads): archived scripts, workloads, experimental outputs and benchmark evidence. Speedups must be interpreted with the stated MPI-rank baseline and workload.
- **Unverified details:** Precise dates for most August–October steps; the exact single root cause of the October `idle*`/`unknown*` incident; a controlled comparison against a gaming PC; and an official supercomputer performance designation. These are **not** presented as facts.
