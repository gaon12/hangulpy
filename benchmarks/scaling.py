"""Run size, cache, Unicode and collection benchmarks without competitors.

Run from the repository root: python -m benchmarks.scaling --output result.json
"""

from __future__ import annotations

import argparse
import gc
import json
import platform
import statistics
import time
import tracemalloc
import unicodedata
from collections.abc import Callable
from functools import partial
from pathlib import Path

from hangulpy import HangulIndex, find_hangul_spans, hangul_contains


def measure(fn: Callable[[], object], samples: int = 5) -> dict[str, object]:
    elapsed = []
    for _ in range(samples):
        started = time.perf_counter_ns()
        fn()
        elapsed.append((time.perf_counter_ns() - started) / 1_000_000)
    return {"median_ms": statistics.median(elapsed), "samples_ms": elapsed}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    rows = []
    for form, unit in [
        ("NFC", "과"),
        ("NFD", unicodedata.normalize("NFD", "과")),
        ("HCJ", "ㄱㅗㅏ"),
    ]:
        for count in [128, 512, 2048]:
            text = unit * count
            sequence = iter(range(1_000_000))
            for operation, function in [
                ("contains", hangul_contains),
                ("spans", find_hangul_spans),
            ]:
                for query in ["과", "없는말"]:
                    # Unique suffixes avoid shared-cache hits without private cache APIs.
                    cold = measure(
                        lambda function=function, text=text, sequence=sequence, query=query: function(
                            text + str(next(sequence)), query
                        )
                    )
                    function(text, query)
                    warm = measure(partial(function, text, query))
                    rows.append(
                        {
                            "operation": operation,
                            "form": form,
                            "chars": len(text),
                            "query": query,
                            "cold": cold,
                            "warm": warm,
                        }
                    )
    for count in [1024, 1025, 10000]:
        items = [f"한글문서{i:05d}" for i in range(count)]
        build = measure(partial(HangulIndex, items))
        index = HangulIndex(items)
        for query in ["ㅎㄱ", "없는말"]:
            for threshold in [0.0, 1.0]:
                rows.append(
                    {
                        "operation": "index",
                        "items": count,
                        "query": query,
                        "min_score": threshold,
                        "build": build,
                        "search": measure(partial(index.search, query, min_score=threshold)),
                    }
                )
    gc.collect()
    tracemalloc.start()
    for i in range(128):
        hangul_contains("한글" * 500 + str(i), "없는말")
    gc.collect()
    retained, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    result = {
        "runtime": {
            "python": platform.python_version(),
            "platform": platform.platform(),
            "processor": platform.processor(),
        },
        "results": rows,
        "large_text_cache_bytes": {"retained": retained, "peak": peak},
    }
    output = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(output, encoding="utf-8")
    else:
        print(output)


if __name__ == "__main__":
    main()
