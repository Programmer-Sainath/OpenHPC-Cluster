# Environment

Collected: 2026-11-19 09:59 +03

## Compute nodes

| Node | CPU | Logical CPUs | RAM | NIC speed | Kernel | Python |
|:---|:---|---:|---:|---:|:---|:---|
| node01 | Intel(R) Core(TM) i5-2400 CPU @ 3.10GHz | 4 | 15.6 GB | 1000 Mb/s | 5.14.0-687.56.1.el9_8.x86_64 | 3.9.25 |
| node02 | Intel(R) Core(TM) i5-2400 CPU @ 3.10GHz | 4 | 15.6 GB | 1000 Mb/s | 5.14.0-687.56.1.el9_8.x86_64 | 3.9.25 |
| node03 | Intel(R) Core(TM) i5-2400 CPU @ 3.10GHz | 4 | 15.6 GB | 1000 Mb/s | 5.14.0-687.56.1.el9_8.x86_64 | 3.9.25 |
| node04 | Intel(R) Core(TM) i5-2400 CPU @ 3.10GHz | 4 | 15.6 GB | 1000 Mb/s | 5.14.0-687.56.1.el9_8.x86_64 | 3.9.25 |

## Software

- Scheduler: Slurm 22.05.11, partition debug
- MPI: mpirun (Open MPI) 4.1.1
- OS image: Rocky Linux 9, stateless, provisioned with Warewulf 4
- numpy 2.0.2
- scipy 1.13.1
- matplotlib 3.9.4
- mpi4py 4.1.2
- dask 2024.8.0
- distributed 2024.8.0

## Slurm view of a compute node

```
NodeName=node01 Arch=x86_64 CoresPerSocket=4 
   CPUAlloc=0 CPUEfctv=4 CPUTot=4 CPULoad=0.00
   RealMemory=15000 AllocMem=0 FreeMem=13086 Sockets=1 Boards=1
```

Interconnect: Ethernet through a Cisco Catalyst switch (negotiated NIC speeds in the table above). Head node: localhost, 4 logical CPUs; jobs run only on node01-node04.
