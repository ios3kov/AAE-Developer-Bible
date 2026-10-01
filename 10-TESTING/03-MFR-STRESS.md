# MFR stress tests

Multi-Frame Rendering changes a plug-in from "one frame at a time in my preview" into a concurrent execution problem.

The purpose of stress tests is to expose races, deadlocks, state bleed and lifetime defects that normal preview rarely reproduces.

## Preconditions

Do not enable an MFR capability flag simply because code compiles.

Before stress:

- identify global mutable state;
- identify sequence/instance state;
- identify caches;
- identify third-party libraries with unknown thread safety;
- identify locks held near host calls;
- identify lazy initialization.

Write down what is expected to be shared vs per-instance vs per-render-thread.

## Core scenarios

1. One effect instance, long composition.
2. 20+ instances of the same effect.
3. Several comps queued together.
4. Different parameter values per instance.
5. Rapid cancel/restart.
6. Cache purge between runs.
7. MFR off -> on -> off.
8. GPU backend with MFR.
9. Old project after sequence-data migration.
10. Repeated render 50-100+ times for flaky races.
11. Multiple output resolutions/sizes.
12. Same source reused by many comps.
13. Failure injection during allocation/cache creation if possible.

## State-bleed fixture

Create several instances with intentionally distinctive output:

~~~text
instance A -> red / parameter 1
instance B -> green / parameter 2
instance C -> blue / parameter 3
~~~

Concurrent output must never contain state from another instance/frame.

This is more diagnostic than using nearly identical parameters.

## Randomized scheduling pressure

Host scheduling is not under the test's full control, but increase variety:

- long/short frames;
- random parameter animation;
- mixed layer sizes;
- CPU/GPU combinations;
- repeated cancel;
- memory pressure.

Do not write a test that passes only because every frame has identical work duration.

## Observability

Debug/stress logging should include enough identity to correlate concurrency:

- plug-in build;
- instance ID/refcon identity;
- frame/time;
- thread ID;
- backend;
- sequence/global state revision;
- cache key/hit/miss;
- request start/end;
- cancellation.

Avoid logging every pixel or creating so much I/O that the logging serializes the render.

## Determinism

Run the same fixture repeatedly and compare output.

Look for:

- different hash/diff between runs;
- rare corrupted tile/row;
- one-frame parameter leak;
- wrong cache reuse;
- output that changes only under high concurrency.

A race that appears 1 in 100 runs is still a release blocker.

## Deadlock/hang detection

Stress harness needs a timeout with useful diagnostics.

On timeout preserve:

- process/thread dump or sample;
- last plug-in log events;
- frame/request IDs in flight;
- AE version/OS;
- MFR state.

Do not kill and discard all evidence.

## Memory trend

Track memory across repeated renders.

Distinguish:

- one-time host/cache warmup;
- bounded reusable cache;
- unbounded growth.

A useful stress run includes purge/restart checkpoints so retained caches are not automatically mislabeled leaks.

## Lock review

A lock can make races disappear by serializing everything and still be a performance defect.

Measure:

- lock wait time;
- critical-section duration;
- whether lock is held across AE suite/host callbacks;
- whether one global lock serializes independent instances.

Correctness first, then remove unnecessary serialization with evidence.

## Third-party libraries

If an external library uses hidden global state, MFR safety may fail even when your own code is clean.

Test each integration under actual concurrent calls or isolate it behind a safe architecture.

Do not infer thread safety from "works in multiple applications".

## Failure symptoms

Release blocker:

- nondeterministic pixels;
- sporadic crash;
- hang/deadlock;
- cross-instance state;
- corrupted cache;
- increasing memory without bound;
- project corruption after save/reopen;
- cancellation leaving persistent broken state.

## MFR claim rule

Until the stress matrix passes, keep MFR disabled in the shipping capability declaration and use a separately identified test build for experiments.
