#!/bin/bash
SSH="ssh -i $HOME/.ssh/id_rsa -o IdentitiesOnly=yes -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o ConnectTimeout=5 -o BatchMode=yes -o LogLevel=ERROR"
echo "# Environment"
echo
echo "Collected: $(date '+%Y-%m-%d %H:%M %Z')"
echo
echo "## Compute nodes"
echo
echo "| Node | CPU | Logical CPUs | RAM | NIC speed | Kernel | Python |"
echo "|:---|:---|---:|---:|---:|:---|:---|"
for n in node01 node02 node03 node04; do
  $SSH root@$n 'bash -s' <<'REMOTE'
cpu=$(grep -m1 'model name' /proc/cpuinfo | cut -d: -f2 | sed 's/^ *//')
mem=$(awk '/MemTotal/{printf "%.1f", $2/1048576}' /proc/meminfo)
spd=$(cat /sys/class/net/enp3s0/speed 2>/dev/null)
echo "| $(hostname -s) | $cpu | $(nproc) | $mem GB | ${spd:-?} Mb/s | $(uname -r) | $(python3 --version 2>&1 | cut -d' ' -f2) |"
REMOTE
done
echo
echo "## Software"
echo
echo "- Scheduler: Slurm $(sinfo --version | awk '{print $2}'), partition debug"
echo "- MPI: $(/usr/lib64/openmpi/bin/mpirun --version 2>&1 | head -1)"
echo "- OS image: Rocky Linux 9, stateless, provisioned with Warewulf 4"
python3 - <<'PY'
import importlib
for m in ["numpy", "scipy", "matplotlib", "mpi4py", "dask", "distributed"]:
    try:
        print("- %s %s" % (m, importlib.import_module(m).__version__))
    except Exception:
        print("- %s: not installed" % m)
PY
echo
echo "## Slurm view of a compute node"
echo
echo '```'
scontrol show node node01 | grep -E "CPUTot|CoresPerSocket|RealMemory"
echo '```'
echo
echo "Interconnect: Ethernet through a Cisco Catalyst switch (negotiated NIC speeds in the table above). Head node: $(hostname -s), $(nproc) logical CPUs; jobs run only on node01-node04."
