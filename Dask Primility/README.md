# Dask primality — single-node task parallelism

## Objective

Use Dask's local distributed scheduler to run independent random **Miller–Rabin probable-prime searches**, comparing how quickly the first worker finishes when launched with 1, 2, and 4 CPU worker processes.

**Scope:** the archived benchmark uses `dask.distributed.LocalCluster` on **one** Slurm compute node (`node01`, 4 allocated CPUs). It does **not** demonstrate execution across the four physical compute nodes.

## What the code does

Each worker searches randomly generated 1,024-bit odd candidates. An independent Dask task returns a probable prime; the parent process accepts the first completed result, verifies the bit length, performs a Fermat check and an additional probabilistic Miller–Rabin check, then cancels remaining tasks. `pure=False` is an important experiment setting: identical calls to `submit()` can otherwise be deduplicated when Dask assumes a pure function.

The benchmark script is [`Dask-Primility-Results/code/dask_local.py`](Dask-Primility-Results/code/dask_local.py). The older [`Dask Primility.py`](<Dask Primility.py>) is a development prototype, **not** the Slurm-recorded entry point; in its current archived form it defines `main()` without calling it.

## Recorded benchmark

| Workers | Trials | Mode | Mean time |
|---:|---:|---|---:|
| 1 | 10 | `pure=False` | 1.73 s |
| 2 | 10 | `pure=False` | 1.08 s |
| 4 | 10 | `pure=False` | 0.41 s |
| 4 | 10 | default `pure=True` | 1.31 s |

Times are the recorded means of 10 stochastic trials each, not controlled end-to-end speedups for a fixed computational problem. Full min/median/max values: [`results.md`](Dask-Primility-Results/results.md). Original Slurm stdout: [`logs/dask1-56.out`](Dask-Primility-Results/logs/dask1-56.out).

## Run new benchmarks

```bash
REPO="$(git rev-parse --show-toplevel)"
mkdir -p "$HOME/jobs/dask"
cp "$REPO/Dask Primility/Dask-Primility-Results/code/"{dask_local.py,dask1.sbatch} "$HOME/jobs/dask/"
cd "$HOME/jobs/dask"
sbatch dask1.sbatch
```

Requires a working `dask.distributed` installation on the allocated compute node. The batch script requests one node, one task, and four CPUs per task. Each trial writes its winning candidate to a `winners_w*_pure*.txt` output file. Run from the job work directory rather than committing volatile trial outputs to Git.

## Interpretation and limitations

- Miller–Rabin is **probabilistic** for arbitrary large numbers. The local `verified=True` field reports further probabilistic checks, **not** a certificate of primality.
- Stochastic search times vary; multiple independent batch runs and statistical uncertainty would be needed for strong scaling conclusions.
- The `pure=True` condition can reuse/deduplicate identical work: this is a useful scheduling experiment but not the same amount of independent work.
- A future multi-node Dask study would require an actual distributed scheduler/worker deployment and network-aware Slurm script.
