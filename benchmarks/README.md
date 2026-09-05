# Benchmarks

Run `python -m benchmarks.scaling --output benchmarks/results/scaling.json` from
the repository root for NFC/NFD/HCJ sizes, successful/unsuccessful searches,
unique-input and repeated-input calls, index construction, the 1024/1025 cache
boundary, score thresholds, and retained allocations. Each row stores all five
samples, not just the median. Unique-input timing includes appending a short
numeric suffix; retained allocations are measured with tracemalloc, not RSS.

The cross-language workflow pins competitor versions and runs Python 3.14 and
Node.js 24 sequentially. Reproduce its dependency installation locally, then run
`python benchmarks/cross_language/python_bench.py`,
`node benchmarks/cross_language/node_bench.mjs` and
`python benchmarks/cross_language/aggregate.py`.

Every measurement hashes the full output outside the timed region. The report
omits ranks and ratios when output hashes or units differ. This deliberately
exposes the numeric-format and initial-search policy differences in the original
corpus instead of claiming that all implementations do identical work. Shared
output is a comparability check, not an independent linguistic correctness oracle.
Raw timing samples and environment metadata remain in the JSON artifacts.

The main cross-language corpus measures warmed repeated input at fixed lengths.
Its per-character ratios must not be generalized to every input size, import
latency, table initialization, cache-miss workload or memory footprint. Use the
scaling runner alongside it. A complete cold-import measurement requires fresh
processes; it is not represented by the unique-input rows.
