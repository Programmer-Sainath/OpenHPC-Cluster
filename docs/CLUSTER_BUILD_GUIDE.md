# Cluster build and recovery guide (documented architecture)

> **Not a turnkey installer.** This is a reproducibility-oriented walkthrough of the *observed architecture*, not a full replay of original installation. Historical shell transcripts are not fully validated for current software versions. Follow school IT approval and have console access/backups before making live changes.

## Prerequisites and design decisions

- Five compatible x86_64 PCs; one dual-homed administrator and four diskless compute machines.
- Rocky Linux 9-family administrator, compatible OS image, managed package repositories, static cluster-interface address on a **physically isolated** provisioning LAN.
- PXE-capable BIOS/UEFI configuration, a switched Gigabit LAN, a known IP/MAC inventory, reliable time, and a secure way to administer the controller.
- Confirm authority over the school network: running another DHCP server on the wrong interface can disrupt unrelated devices.

## Deployment sequence (for a **new** environment only)

1. **Record hardware.** Check CPU, memory, NIC names, firmware PXE support, BIOS boot mode, switch connectivity. See [Hardware Inventory](HARDWARE_INVENTORY.md).
2. **Install the administrator OS.** Install Rocky Linux and update packages in a controlled change window. Arrange disks and partitions to suit capacity; this system has 70 GiB `/`, 39.8 GiB `/home` and 7.8 GiB swap in LVM. Do not copy UUIDs or partition commands from another host.
3. **Configure two interfaces and firewall zones.** Keep private `enp3s0` on `192.168.10.2/24` and the campus `enp2s0` separate. Apply only approved service exposure rules. See [Network Security](NETWORKING_AND_SECURITY.md).
4. **Install compatible Warewulf/OpenHPC components.** Verify the specific release matrix. Import/build the OS image, define the default profile and nodes, and configure DHCP/PXE on the **private** NIC. The current observed image name is `rockylinux-9`. Follow Warewulf **4.7-specific** documentation rather than executing historical `.conf` command notes as scripts.
5. **Provision system and runtime overlays.** Configure network, hostnames, fstab, and secure identity/account synchronization; secret-bearing overlays should be handled only by authorized administrators. Avoid publishing `rootkey` or Munge key contents.
6. **Set up time synchronization.** The admin currently uses Chrony with private subnet clients allowed; verify peers and actual per-node offsets, not just service status.
7. **Configure shared storage.** Export `/home` using NFS, provision compute mounts through Warewulf profile fstab, confirm `root_squash` and permissions. `/opt` is exported but has a `noauto` client mount policy.
8. **Set up authentication and scheduling.** Install Munge/Slurm controller and compatible compute image components, create matching service identities, use shared `slurm.conf`, and verify `slurmd` and `slurmctld` services. Do not regenerate the active Munge key on a running installation.
9. **Validate in stages.** Confirm services and names, all four `idle` nodes, NFSv4.2 `/home` mounts, same Slurm checksum, a four-node hostname task and—separately—a fresh MPI program test.
10. **Snapshot, document, and plan rollback.** Record versions and sanitized configurations with a date. Any future change to node boot, firewall, Slurm, Warewulf, Munge, storage or SSH policy requires a planned maintenance window.

## Ready-to-run inspections (read-only)

```bash
cat /etc/rocky-release
ip -br addr
sudo wwctl image list
sudo wwctl profile list -a
sinfo -N -l
scontrol show config | grep -E 'SlurmctldHost|SelectType|TaskPlugin'
sudo exportfs -v
sudo firewall-cmd --get-active-zones
```

The first six stages above are **design guidance**, not an assertion that the exact original procedural steps are fully recoverable from the repository. Do not use this README to overwrite any currently running `warewulf.conf`, Slurm, NFS, firewall or Munge configuration.
