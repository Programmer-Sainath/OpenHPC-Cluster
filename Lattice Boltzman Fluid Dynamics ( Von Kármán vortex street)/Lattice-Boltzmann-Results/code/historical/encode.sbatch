#!/bin/bash
#SBATCH --job-name=lbm-video
#SBATCH --ntasks=1
#SBATCH --time=00:30:00
#SBATCH --output=logs/enc-%j.out

set -e
cd "$SLURM_SUBMIT_DIR"

FF=$(command -v ffmpeg || python3 -c \
'import imageio_ffmpeg; print(imageio_ffmpeg.get_ffmpeg_exe())')

DIR="$1"

"$FF" -y -framerate 24 \
  -i "$DIR/frame_%06d.ppm" \
  -c:v libx264 -pix_fmt yuv420p \
  -crf 20 -movflags +faststart \
  "$DIR/vortex.mp4"

ls -lh "$DIR/vortex.mp4"
