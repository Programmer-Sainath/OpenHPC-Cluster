# Original Slurm output and node inventories

**These are actual files exported from the cluster**, not reconstructed excerpts. They correspond to the complete recorded stdout of the Slurm jobs used in this experiment:

| File | Meaning |
|---|---|
| `lbm-91.out` | 1-rank correctness test, 800 steps, 8 frames |
| `lbm-92.out` | 16-rank correctness test, 800 steps, 8 frames |
| `lbm-93.out` | 1-rank benchmark, 4,000 steps |
| `lbm-94.out` | 4-rank benchmark, 4,000 steps |
| `lbm-95.out` | 16-rank benchmark, 4,000 steps |
| `lbm-96.out` | 16-rank production run, 80,000 steps, 289 frames, completed |
| `enc-97.out` | FFmpeg output that produced the H.264 MP4 |
| `slurm-accounting-status.txt` | Actual response: `Slurm accounting storage is disabled` |
| `hardware/*.txt` | Five actual hardware/OS/network inventory snapshots |
| `source-lists/bench.list`, `source-lists/prod.jobs` | Historical job ID mappings |

**What the logs cannot show:** per-rank elapsed times, per-rank peak RSS, per-node execution-time breakdowns, historical `MaxRSS` and encoder wall time. These values were not recorded at runtime; they are not zero. Optional scripts under `code/` can instrument *future* jobs and save separately named results.

**GitHub hygiene:** before making the repository public, inspect exported logs and inventories for any information you do not want to disclose (internal hostnames, private network configuration, account names or paths). The `code/historical/lbm.sbatch` file retains the actual historical MPI LAN selector for reproducibility.
