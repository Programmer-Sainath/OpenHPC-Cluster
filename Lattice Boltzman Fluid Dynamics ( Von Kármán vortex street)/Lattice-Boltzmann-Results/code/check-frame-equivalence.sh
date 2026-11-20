#!/usr/bin/env bash
# Requires two finished validation runs stored as runs/eq1-ID and runs/eq16-ID.
set -euo pipefail
E1=$(find runs -maxdepth 1 -type d -name 'eq1-*' | sort -V | tail -1)
E16=$(find runs -maxdepth 1 -type d -name 'eq16-*' | sort -V | tail -1)
[[ -n "$E1" && -n "$E16" ]] || { echo 'Missing eq1 or eq16 directories' >&2; exit 1; }
diff <(cd "$E1" && md5sum frame_*.ppm) <(cd "$E16" && md5sum frame_*.ppm)
echo 'PASS: Generated PPM frames are byte-identical between 1 and 16 ranks.'
