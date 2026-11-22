#!/usr/bin/env python3
"""New binary-splitting Chudnovsky π implementation (not original 2026 run source).

Usage: python3 chud_fast.py 1000 [--output path]
Calculates the requested number of digits AFTER the decimal point.
"""
import argparse
from decimal import Decimal, localcontext
import os
from pathlib import Path
import socket
import textwrap
import time

C3_OVER_24 = 640320 ** 3 // 24
KNOWN_PREFIX = "3.14159265358979323846264338327950288419716939937510"


def binary_split(a, b):
    """Compute P,Q,T products for Chudnovsky terms [a,b)."""
    if b - a == 1:
        if a == 0:
            p = q = 1
        else:
            p = (6 * a - 5) * (2 * a - 1) * (6 * a - 1)
            q = a * a * a * C3_OVER_24
        t = p * (13591409 + 545140134 * a)
        if a & 1:
            t = -t
        return p, q, t
    mid = (a + b) // 2
    p1, q1, t1 = binary_split(a, mid)
    p2, q2, t2 = binary_split(mid, b)
    return p1 * p2, q1 * q2, t1 * q2 + p1 * t2


def pi_string(digits):
    if digits < 1:
        raise ValueError("digits must be a positive integer")
    terms = digits // 14 + 2  # conservative; Chudnovsky converges ~14.18 decimal digits/term
    _, q, t = binary_split(0, terms)
    with localcontext() as ctx:
        ctx.prec = digits + 30
        pi = (Decimal(426880) * Decimal(10005).sqrt() * Decimal(q)) / Decimal(t)
        s = format(pi, "f")
    result = s[:digits + 2]
    if len(result) != digits + 2 or not result.startswith(KNOWN_PREFIX[:min(len(result), len(KNOWN_PREFIX))]):
        raise ArithmeticError("unexpected digit count or incorrect known prefix")
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("digits", type=int, help="number of digits after decimal point")
    parser.add_argument("--output", type=Path, default=None)
    args = parser.parse_args()
    if not 1 <= args.digits <= 2_000_000:
        parser.error("digits must be between 1 and 2,000,000")
    t0 = time.perf_counter()
    value = pi_string(args.digits)
    duration = time.perf_counter() - t0
    output = args.output or Path("pi_%d_digits.txt" % args.digits)
    if output.exists():
        parser.error("output already exists: %s (use --output with a fresh path)" % output)
    job_id = os.environ.get("SLURM_JOB_ID", "not under Slurm")
    header = [
        "Chudnovsky algorithm (new reconstructed binary-splitting implementation)",
        "Digits after decimal: %d" % args.digits,
        "Time taken (seconds): %.6f" % duration,
        "Node: %s   Slurm job: %s" % (socket.gethostname(), job_id),
        "Digits below are wrapped at 100 characters per line.",
        "----------------------------------------------------------------",
    ]
    output.write_text("\n".join(header) + "\n" + "\n".join(textwrap.wrap(value, 100)) + "\n", encoding="ascii")
    print("digits=%d seconds=%.6f prefix_check=PASS file=%s" % (args.digits, duration, output), flush=True)


if __name__ == "__main__":
    main()
