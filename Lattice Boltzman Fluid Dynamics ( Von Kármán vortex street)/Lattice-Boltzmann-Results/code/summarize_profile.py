#!/usr/bin/env python3
"""Summarize optional future MPI rank profiles from lbm-profiled.sbatch.
This does not retroactively provide rank metrics for historical jobs.
"""
import csv, pathlib, sys, collections
if len(sys.argv) != 2:
    raise SystemExit('Usage: python3 code/summarize_profile.py runs/profile-JOBID')
folder = pathlib.Path(sys.argv[1]); rows=[]
for path in folder.glob('rank_*.time'):
    try:
        rank=int(path.stem.split('_')[1]); metrics=dict(line.split('=',1) for line in path.read_text().splitlines() if '=' in line)
        host=(folder/f'rank_{rank}.host').read_text().strip()
        rows.append({'rank':rank,'hostname':host,'wall_s':float(metrics['wall_s']),
                     'user_s':float(metrics['user_s']),'system_s':float(metrics['system_s']),
                     'peak_rss_kb':int(metrics['peak_rss_kb'])})
    except (ValueError, KeyError, FileNotFoundError) as exc:
        print(f'Unusable profile {path}: {exc}',file=sys.stderr)
rows.sort(key=lambda r:r['rank'])
if not rows: raise SystemExit('No readable per-rank timing files found')
with (folder/'per_rank_metrics.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
byhost=collections.defaultdict(list)
for r in rows: byhost[r['hostname']].append(r)
with (folder/'per_node_metrics.csv').open('w',newline='') as f:
    w=csv.writer(f);w.writerow(['hostname','ranks','node_elapsed_max_rank_s','node_elapsed_min_rank_s','sum_rss_peak_kb_not_simultaneous'])
    for host,rr in sorted(byhost.items()):
        w.writerow([host,len(rr),max(x['wall_s'] for x in rr),min(x['wall_s'] for x in rr),sum(x['peak_rss_kb'] for x in rr)])
fast=min(rows,key=lambda r:r['wall_s']);slow=max(rows,key=lambda r:r['wall_s'])
print(f"Ranks profiled: {len(rows)} | fastest rank {fast['rank']} ({fast['hostname']}): {fast['wall_s']:.2f} s | slowest rank {slow['rank']} ({slow['hostname']}): {slow['wall_s']:.2f} s")
print(f"Largest recorded per-process peak RSS: {max(r['peak_rss_kb'] for r in rows)/1024:.2f} MiB")
print('Note: summed process peak RSS values are NOT a synchronized total-memory measurement.')
