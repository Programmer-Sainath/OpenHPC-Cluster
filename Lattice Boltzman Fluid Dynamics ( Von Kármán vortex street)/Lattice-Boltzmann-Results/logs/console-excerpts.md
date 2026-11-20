# Original operator transcript — supplemental only

The full historical Slurm logs for jobs 91–97 are now available directly in this `logs/` directory. This short file records the operator's additional **outside-of-job** frame comparison, which is not printed in the Slurm stdout:

```text
$ diff <(cd "$E1" && md5sum frame_*.ppm) <(cd "$E16" && md5sum frame_*.ppm) && echo "PASS: FRAMES IDENTICAL"
PASS: FRAMES IDENTICAL
```

The source frame images and checksums from that comparison were not part of the evidence archive. See the real `lbm-91.out` and `lbm-92.out` logs for execution parameters and completion times.
