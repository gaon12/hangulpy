"""Microbenchmark the particle-selection hot paths used by es-hangul comparisons."""

import argparse
from timeit import Timer
from typing import List, Optional

BENCHMARKS = (
    ("josa", "josa('사과', '은/는')"),
    ("josa_pick", "josa_pick('사과', '은/는')"),
    ("has_batchim", "has_batchim('사과')"),
)
SETUP = "from hangulpy import has_batchim, josa, josa_pick"


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--number", type=int, default=1_000_000, help="calls per sample")
    parser.add_argument("--repeat", type=int, default=5, help="number of samples")
    args = parser.parse_args(argv)

    if args.number < 1 or args.repeat < 1:
        parser.error("--number and --repeat must be positive")

    for name, statement in BENCHMARKS:
        best = min(Timer(statement, setup=SETUP).repeat(args.repeat, args.number))
        rate = args.number / best
        print(f"{name:12} {rate:>12,.0f} ops/s  {best / args.number * 1e6:>8.3f} us/op")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
