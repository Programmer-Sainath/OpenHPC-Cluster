#!/usr/bin/env bash
# Optional future profiling ONLY. This was not active during historical jobs 93-97.
set -euo pipefail
RUN=${1:?Missing output directory}; shift
rank=${OMPI_COMM_WORLD_RANK:?Requires mpirun}
node=$(hostname)
printf '%s\n' "$node" > "$RUN/rank_${rank}.host"
if [[ ! -x /usr/bin/time ]]; then echo '/usr/bin/time (GNU time) is required for profiling' >&2; exit 1; fi
exec /usr/bin/time -f 'wall_s=%e\nuser_s=%U\nsystem_s=%S\npeak_rss_kb=%M' -o "$RUN/rank_${rank}.time" "$@"
