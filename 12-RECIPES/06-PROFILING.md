# Recipe — profiling a slow effect

## Goal

Find the actual bottleneck of a reproducible user operation, change one cause, then prove both performance improvement and unchanged correctness.

## 1. Freeze the workload

Record:

- project/fixture hash;
- AE exact version/build;
- OS;
- CPU/GPU/RAM;
- driver;
- plug-in hash;
- bit depth;
- resolution;
- MFR state;
- GPU state;
- render path.

Do not compare measurements from different environments without rerunning the baseline there.

## 2. Define the user-level metric

Choose the metric that matters:

- first preview frame;
- warm frame;
- N-frame render;
- render queue wall time;
- panel command latency;
- project-open operation;
- memory peak.

Start from end-to-end time, not a guessed function.

## 3. Warmup policy

Measure separately:

~~~text
cold process/plugin startup
first GPU/device setup
first cache fill
steady state
~~~

Do not average them together unless the product question actually concerns that combined experience.

## 4. Establish baseline distribution

Run enough repetitions to see noise.

Record at least:

- sample count;
- median;
- p95 when meaningful;
- min/max or raw samples;
- thermal/power condition.

A single stopwatch result is not a performance baseline.

## 5. Split by execution path

First toggles:

~~~text
GPU on vs CPU
MFR on vs off
cache cold vs warm
small vs large frame
~~~

This identifies which subsystem deserves deeper profiling.

## 6. Time major stages

For a render effect:

~~~text
host checkout
→ input conversion/preparation
→ core algorithm
→ cache work
→ GPU upload
→ kernel
→ synchronization
→ download/conversion
→ checkin/return
~~~

Do not optimize a 1 ms kernel if 15 ms is spent waiting/copying.

## 7. Inspect allocation pressure

Measure:

- allocations per frame;
- transient buffer sizes;
- peak memory;
- retained cache;
- memory after purge/project close.

Common improvement is reusing correctly owned scratch, but never reuse a buffer across concurrent renders without a safe ownership model.

## 8. Inspect locks

For each hot lock:

- wait time;
- hold time;
- contention count;
- which instances contend;
- whether host calls occur while held.

A global lock can erase MFR benefit.

## 9. Inspect host API frequency

Repeated tiny suite/checkouts or evalScript calls can dominate interactive workflows.

Batch work only when semantics remain correct.

Do not hide necessary dependency declarations to make profiling numbers smaller.

## 10. GPU-specific profiling

Separate:

- preparation/upload;
- dispatch;
- kernel;
- synchronization;
- download/readback.

Test multiple resolutions because GPU crossover varies with workload size.

## 11. Make one change

Examples:

- remove redundant conversion;
- change cache key/data structure;
- batch host reads;
- reduce allocations;
- shorten lock;
- optimize kernel;
- avoid unnecessary readback.

One isolated change gives interpretable evidence.

## 12. Correctness gate before celebrating

Immediately rerun:

- golden pixels;
- alpha;
- required bit depths;
- ROI/origins if relevant;
- MFR stress;
- GPU equivalence if touched.

A faster stale/wrong frame is not an optimization.

## 13. Rerun the exact baseline

Compare candidate vs baseline in the same environment.

Report both absolute and relative change.

If improvement is within noise, do not market it as a performance win.

## 14. Keep regression evidence

Store the benchmark definition and machine-readable result beside the release/test evidence so later versions can detect regression.

## Acceptance gate

Keep the optimization only if:

- end-user metric improves measurably;
- correctness remains inside existing tolerances;
- memory does not become unbounded;
- MFR scaling is not harmed;
- no unsupported environment-specific assumption was introduced.

See [Performance testing](../10-TESTING/04-PERFORMANCE.md).
