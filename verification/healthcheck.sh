#!/usr/bin/env bash
# Read-only HPC health summary, intended for the Rocky Linux admin node.
# --slurm-smoke optionally launches one short Slurm task per compute node.
set -uo pipefail

header() { printf '\n=== %s ===\n' "$1"; }
run_check() { "$@" || printf 'WARNING: command failed: %s\n' "$1" >&2; }

header 'OS / hostname'
run_check cat /etc/rocky-release
run_check hostname -s
header 'Slurm node status'
run_check sinfo -N -l
header 'Admin service health'
for service in warewulfd munge slurmctld dhcpd nfs-server firewalld chronyd; do
  printf '%-14s ' "$service"
  systemctl is-active "$service" || true
done
header 'Admin /home backing filesystem'
run_check findmnt -T /home -o TARGET,SOURCE,FSTYPE
header 'Admin time synchronization'
run_check timedatectl show -p NTPSynchronized
header 'Slurm config hash'
run_check sha256sum /etc/slurm/slurm.conf
header 'Warewulf version and image list'
if command -v wwctl >/dev/null 2>&1; then
  run_check wwctl version
  # Image inventory can require root on some installations; don't auto-sudo.
else
  echo 'wwctl unavailable'
fi
header 'Firewall zoning'
if command -v firewall-cmd >/dev/null 2>&1; then
  run_check firewall-cmd --get-active-zones
fi
case "${1:-}" in
  '') echo 'No jobs submitted. Use --slurm-smoke for a four-node Slurm task.' ;;
  --slurm-smoke)
    header 'Four-node Slurm smoke job (allocates scheduler resources)'
    run_check srun --partition=debug --nodes=4 --ntasks=4 --ntasks-per-node=1 --time=00:02:00 /usr/bin/hostname
    ;;
  *) echo 'Usage: bash verification/healthcheck.sh [--slurm-smoke]' >&2; exit 2 ;;
esac
