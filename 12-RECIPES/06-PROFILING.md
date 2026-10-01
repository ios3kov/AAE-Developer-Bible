# Recipe — profiling a slow effect

## Rule

Profile a fixed reproducible workload. Never optimize from a vague report that "the effect feels slow".

## 1 — freeze environment

Record:

- product build/hash;
- AE exact build;
- OS;
- CPU;
- GPU/driver;
- project fixture;
- resolution/duration/BPC;
- MFR state;
- GPU state.

Run the baseline more than once to estimate noise.

## 2 — measure whole operation

Start from user-visible wall time:

- first frame;
- warm frame;
- full comp render;
- panel command latency if relevant.

If the total problem is 200 ms, optimizing a 1 ms function cannot solve it.

## 3 — isolate feature switches

Compare:

- CPU vs GPU;
- MFR off vs on;
- cache cold vs warm;
- preview vs render queue if relevant.

Change one dimension at a time.

## 4 — instrument high-level stages

Example:

~~~text
checkout/input prep
→ conversion
→ algorithm
→ output conversion
→ host checkin
~~~

For SmartFX include pre-render/checkouts.

For GPU include upload/kernel/sync/download.

## 5 — allocations

Measure:

- allocations per frame;
- large transient buffers;
- reallocations caused by size changes;
- memory peak;
- retained cache.

A fast algorithm can be dominated by allocation churn.

## 6 — locks

Measure:

- lock wait;
- hold duration;
- contention across instances;
- whether lock spans host calls.

MFR often exposes hidden global serialization.

## 7 — host interaction

Count expensive host calls/checkouts.

Ask whether the same immutable data is repeatedly requested or converted.

Do not cache host-owned pointers beyond their valid lifetime to save a call.

## 8 — GPU

Separate:

~~~text
world/buffer acquisition
upload
kernel
synchronization
download/conversion
~~~

Profile small and large frames because crossover points differ.

## 9 — optimize one bottleneck

Make one focused change.

Then rerun:

1. correctness;
2. MFR stress if affected;
3. memory;
4. benchmark.

Do not combine five optimizations and lose the cause of a regression.

## 10 — report

Store:

| Metric | Baseline | Candidate | Delta |
|---|---:|---:|---:|
| first frame | | | |
| warm median | | | |
| p95 | | | |
| full render | | | |
| peak memory | | | |
| lock wait | | | |

Attach environment/artifact identity.

## Reject an "optimization" when

- output leaves tolerance;
- memory becomes unbounded;
- cancellation worsens;
- MFR races appear;
- improvement is within measurement noise;
- improvement only exists on an unsupported machine/project.

Performance evidence belongs beside correctness evidence, not instead of it.
