# Safe day-to-day operations

These commands are written for **Rocky Linux Bash on the administrator node**. Their examples inspect state unless stated otherwise. They never replace or regenerate Munge credentials, firewall rules, DHCP tables, or node images.

## Quick health check

```bash
cat /etc/rocky-release
hostname -s
sinfo -N -l
squeue
systemctl is-active munge slurmctld warewulfd dhcpd nfs-server chronyd
sudo wwctl image list
sudo wwctl profile list -a
sudo exportfs -v
sudo firewall-cmd --get-active-zones
```

A reusable script is included at [`../verification/healthcheck.sh`](../verification/healthcheck.sh); run it from the admin node with `bash verification/healthcheck.sh`. It has a separate opt-in `--slurm-smoke` flag for submitting a lightweight Slurm task.

## Read-only diagnostics

```bash
scontrol show node node01
scontrol show partition debug
systemctl --no-pager status slurmctld
chronyc tracking
findmnt -T /home -o TARGET,SOURCE,FSTYPE,OPTIONS
```

For four-node NFS and service inspections, run a short, supervised Slurm allocation. The following creates a Slurm job allocation but makes no persistent changes:

```bash
srun --label --nodes=4 --ntasks=4 --ntasks-per-node=1 \
  --time=00:02:00 bash -c 'hostname; findmnt -n -T /home -o TARGET,SOURCE,FSTYPE'
```

## Operations and rollback policy

- Avoid running `dnf update`, `wwctl overlay build`, `wwctl configure --all`, `systemctl restart`, `exportfs -ra`, `firewall-cmd --reload`, account creation, `mungekey` regeneration, or image imports as **health checks**. These can mutate the live system.
- Before any planned modification, record a change request, sanitized state snapshot, affected services, window approved by school supervisor, and rollback steps. Do not publish sensitive material in Git.
- The root filesystem is memory-backed on compute nodes; repeated configuration may require changing the Warewulf image/overlays rather than writing directly to a live compute node.
- Treat `/home` as a shared failure domain; file changes may affect all nodes immediately.

## Interpreting results

Four `idle` nodes indicate Slurm sees them as available. That does not alone establish MPI communication correctness, clock offsets, absence of disk issues, or successful PXE recovery. Always record what was actually tested and when.
