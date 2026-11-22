#!/usr/bin/env bash
# Compare frames from the newest eq1-* and eq16-* test runs.
# Run from anywhere. Optional first argument: folder containing runs (default: runs/).
set -euo pipefail
HERE="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
RUNS="${1:-$HERE/runs}"
[[ -d "$RUNS" ]] || { echo "ERROR: runs directory not found: $RUNS" >&2; exit 1; }
E1="$(find "$RUNS" -mindepth 1 -maxdepth 1 -type d -name 'eq1-*' | sort -V | tail -n 1)"
E16="$(find "$RUNS" -mindepth 1 -maxdepth 1 -type d -name 'eq16-*' | sort -V | tail -n 1)"
[[ -n "$E1" && -n "$E16" ]] || { echo 'ERROR: Missing eq1-* or eq16-* run directories.' >&2; exit 1; }
shopt -s nullglob
frames=("$E1"/frame_*.ppm)
frames16=("$E16"/frame_*.ppm)
((${#frames[@]} > 0)) || { echo 'ERROR: No frames in 1-rank run.' >&2; exit 1; }
((${#frames16[@]} > 0)) || { echo 'ERROR: No frames in 16-rank run.' >&2; exit 1; }
((${#frames[@]} == ${#frames16[@]})) || {
    echo "ERROR: Unequal frame counts: ${#frames[@]} versus ${#frames16[@]}." >&2
    exit 1
}
for frame in "${frames[@]}"; do
    name="$(basename -- "$frame")"
    other="$E16/$name"
    [[ -f "$other" ]] || { echo "ERROR: Missing 16-rank frame: $name" >&2; exit 1; }
    cmp -s -- "$frame" "$other" || { echo "ERROR: Different frame contents: $name" >&2; exit 1; }
done
printf 'PASS: %s frame(s) are byte-identical between 1 and 16 ranks.\n' "${#frames[@]}"
