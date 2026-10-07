# Performance testing

Filled [illustrative report](../13-TEMPLATES/examples/WORKED-EXAMPLE.md) и
[primary-record comparison](../22-PROJECT-CASE-STUDIES/ELASTICGRIDFX-PERFORMANCE-SCOPE-2026-10-07.md):
preparation throughput, actual native render, ordinary export wall-time, Preview
cache-fill и displayed playback — пять scopes. Warmups/repeats/order/cache policy
и frame coverage входят в report. Неполный набор outputs исключается из принятого
timing aggregate, но остаётся в failure history. Screenshot-bracketed interval не
точная latency и не observer-free performance.

Performance work needs a fixed workload, fixed environment and defined regression threshold. "Feels faster" is not a benchmark.

## Metrics

Measure what matters for the product:

- cold first frame;
- warm frame;
- full composition render time;
- per-frame median/p95/p99;
- peak RSS/working set;
- allocations per frame;
- MFR scaling;
- CPU utilization;
- lock wait time;
- GPU kernel time;
- CPU<->GPU transfer/synchronization time;
- cache hit rate;
- panel command latency for interactive tools.

## Baseline

Compare each candidate to a known baseline:

~~~text
same machine
same AE build
same OS
same project
same output settings
same MFR/GPU mode
last shipped plug-in vs candidate
~~~

Changing hardware/driver/AE invalidates a direct regression percentage unless the baseline is rerun there too.

## Example gates

Product-specific thresholds should be chosen before measuring the candidate.

~~~text
Typical project:
  median render regression <= 5% unless approved

Stress:
  no OOM or unbounded growth

MFR:
  no accidental global serialization

GPU:
  must meet target workload benefit or have an explicit non-speed reason
~~~

Do not blindly copy 5% into every product; noise level and workload determine a meaningful threshold.

## Warmup

Separate:

- process cold start;
- first plug-in initialization;
- first GPU pipeline/kernel setup;
- first cache fill;
- steady state.

A benchmark that mixes all five into one average is hard to interpret.

## Repetitions

Run enough repetitions to understand noise.

Record:

- sample count;
- median;
- p95;
- min/max if useful;
- environment thermal/power mode.

Discarding "slow outliers" without a predeclared rule can hide the exact stalls users care about.

## MFR scaling

Measure relative to MFR-off or single-concurrency baseline.

Useful output:

~~~text
threads/host mode
frames
wall time
CPU utilization
speedup
peak memory
~~~

More CPU utilization is not itself success. It must produce useful throughput without unacceptable memory growth.

## GPU

Break GPU time into:

~~~text
upload / world preparation
kernel/compute
synchronization
download / conversion
host overhead
~~~

Optimizing a 1 ms kernel does not matter if transfers cost 12 ms.

Test small and large frames; GPU crossover points vary.

## Memory

Track:

- peak memory;
- steady-state retained memory;
- per-frame allocation count;
- cache size;
- memory after purge;
- memory after project close if relevant.

Performance fixes that create unbounded caches are regressions.

## Interactive UI/panel

For interactive tools, render throughput is not enough.

Measure:

- click/command -> host response latency;
- selection refresh;
- panel startup;
- large-project state snapshot;
- cancellation response.

Avoid high-frequency evalScript polling that makes UI benchmarks look like host performance problems.

## Profiling order

1. measure whole user operation;
2. locate slow selector/backend/component;
3. profile algorithm;
4. inspect allocations;
5. inspect lock contention;
6. inspect GPU transfer/sync;
7. inspect host callbacks/checkouts;
8. optimize;
9. rerun correctness first;
10. rerun benchmark.

Do not optimize from intuition alone.

## Performance evidence

Store benchmark report with:

- product/build hashes;
- baseline version;
- AE/OS;
- CPU/GPU/RAM;
- driver;
- project fixture hash;
- MFR/GPU settings;
- raw samples or machine-readable summary.

Without that, a chart cannot be reproduced.

## Correctness remains gate 0

A faster output outside pixel tolerance, a cache that returns stale data, or an MFR lock removal that introduces races is not a performance win.
