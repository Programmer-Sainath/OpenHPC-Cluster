#!/usr/bin/env bash
# Read-only environment snapshot; run locally or once per compute node through Slurm.
set -u
echo '========== NODE ENVIRONMENT =========='
echo "timestamp: $(date -Is)"
echo "hostname: $(hostname)"
echo "kernel: $(uname -r)"
echo '--- os-release ---'
cat /etc/os-release 2>/dev/null || true
echo '--- CPU ---'
if command -v lscpu >/dev/null; then lscpu | grep -E '^(Architecture|CPU\(s\)|Model name|Socket\(s\)|Core\(s\) per socket|Thread\(s\) per core):'; else grep -m1 'model name' /proc/cpuinfo; fi
echo '--- memory ---'
free -h 2>/dev/null || cat /proc/meminfo | head -4
echo '--- NICs and negotiated link speeds ---'
command -v ip >/dev/null && ip -br link || true
for net in /sys/class/net/*; do
  name=${net##*/}
  [[ "$name" == 'lo' ]] && continue
  printf 'NIC %s: ' "$name"
  speed=$(cat "$net/speed" 2>/dev/null || true)
  printf 'speed_Mbps=%s operstate=%s\n' "${speed:-unavailable}" "$(cat "$net/operstate" 2>/dev/null || echo unavailable)"
done
echo '--- Slurm ---'
command -v sinfo >/dev/null && sinfo --version || true
command -v slurmd >/dev/null && slurmd -V || true
echo '--- MPI ---'
command -v mpirun >/dev/null && mpirun --version | head -2 || true
command -v mpicc >/dev/null && mpicc --showme:version 2>/dev/null || true
echo '--- Python and video libraries ---'
command -v python3 >/dev/null && python3 --version || true
python3 -c 'import importlib.metadata as m; print("imageio-ffmpeg:",m.version("imageio-ffmpeg"))' 2>/dev/null || echo 'imageio-ffmpeg: unavailable'
command -v ffmpeg >/dev/null && ffmpeg -version | head -1 || true
