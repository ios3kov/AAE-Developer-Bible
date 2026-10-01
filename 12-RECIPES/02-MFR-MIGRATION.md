# Recipe — migrate an existing effect to MFR

## Goal

Enable Multi-Frame Rendering only after the effect is actually safe under concurrent render selectors.

The public AE SDK guidance requires an effect to be thread-safe before it sets PF_OutFlag2_SUPPORTS_THREADED_RENDERING.

## Phase 1 — keep the shipping flag off

Start with the effect behaving as non-MFR capable.

Create a separate migration branch/build. Do not set the support flag first and use crashes as the discovery method.

## Phase 2 — inventory mutable state

List every:

- global/static variable;
- global_data write;
- sequence_data read/write;
- singleton;
- lazy initialization path;
- scratch buffer;
- cache;
- third-party library global;
- random-number generator;
- log sink;
- GPU/device state;
- lock.

Classify each:

~~~text
immutable shared
instance-owned
frame-local
thread-local
host-owned
unsafe/unknown
~~~

Unknown is not thread-safe.

## Phase 3 — inspect render-time sequence state

For modern MFR behavior, treat render-time sequence data as read-only unless using the SDK mechanisms intended for mutable render state.

Prefer:

- read-only sequence data where possible;
- Compute Cache for expensive shareable computed state;
- frame-local scratch for transient mutation.

The compatibility flag for mutable render sequence data is not a substitute for architecture review; it can carry a performance cost.

## Phase 4 — remove hidden serialization

A single global mutex can make the effect technically race-free while destroying MFR scaling.

Check every lock:

- what state it protects;
- maximum hold time;
- whether independent instances contend;
- whether a host suite/checkout is called while held.

Do not hold blocking product locks across host calls; SDK MFR guidance warns this can deadlock.

## Phase 5 — make callbacks re-entrant

Render-related callbacks must not depend on a global current frame/current instance.

Good pattern:

~~~text
callback inputs
→ acquire immutable/shared resources
→ frame-local context
→ render
→ release/checkin
~~~

Every failure path must still release/checkin resources.

## Phase 6 — third-party dependencies

For each library used during render, obtain evidence for concurrent use.

If thread safety is unknown:

- isolate calls behind a deliberately serialized boundary and measure the cost;
- move work outside concurrent render if semantics permit;
- replace the dependency;
- keep MFR disabled.

Do not infer thread safety from the fact that the library is popular.

## Phase 7 — static/global analysis

Use symbol/static analysis as a discovery aid, not as proof.

A scan can find suspicious globals but cannot prove:

- correct ownership;
- no stale pointer;
- no race inside a third-party library;
- no deadlock;
- correct render output.

## Phase 8 — create diagnostic fixtures

At minimum:

- many instances with different parameter values;
- long composition;
- mixed frame complexity;
- multiple compositions;
- cancel/restart;
- cache purge;
- MFR off/on comparison.

Use visually distinctive instance outputs so state bleed is obvious.

## Phase 9 — repeated stress

Run enough repeated renders to expose rare scheduling bugs.

Record:

- output hash/diff;
- crash/hang;
- memory trend;
- thread/instance/frame identity in diagnostic logs;
- timeout/thread dump on hang.

One successful render is not acceptance.

## Phase 10 — enable the flag in the candidate

Only after the review and stress harness exist, set the MFR support flag in the candidate build.

Repeat:

~~~text
MFR off reference
→ MFR on
→ repeated render
→ cancel
→ save/reopen
→ CPU/GPU combinations if GPU is claimed
~~~

Output must remain within the predefined correctness tolerance.

## Phase 11 — performance

After correctness:

- measure wall time;
- CPU utilization;
- lock wait;
- peak memory;
- cache behavior.

MFR support that serializes on one global lock may be correct but not useful.

## Acceptance gate

Ship MFR support only if:

- mutable state inventory has no unresolved item;
- concurrency stress passes repeatedly;
- MFR off/on pixels match expected tolerance;
- cancellation and error cleanup pass;
- no deadlock/hang;
- memory is bounded;
- third-party dependencies have a safe policy;
- performance does not reveal accidental global serialization.

If not, keep PF_OutFlag2_SUPPORTS_THREADED_RENDERING disabled.

See [MFR stress tests](../10-TESTING/03-MFR-STRESS.md).
