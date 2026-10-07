# Performance architecture

## Сквозной profiling contract

Сначала установить actual render entry/plane route instrumented build, затем
измерять unchanged baseline и candidate с одинаковыми source/toolchain/inputs.
Instrumentation attribution и ordinary release timing — разные режимы.
Pure native benchmark исключает host scheduling/output encoding; export timing
включает их; Preview cache-fill и displayed playback — ещё две отдельные метрики.
Нельзя переносить ускорение generic CPU renderer на реально вызываемый plane path.

State inventory → immutable parameter snapshot → request-local scratch → complete
cache key + receipt → actual route observation → output parity → repeated timings.
Сначала correctness, затем speed. Для N simultaneous requests budget включает
N×scratch; MFR requested не measured concurrency. Для этого нужны overlapping
callback observations именно нужного effect, а не общий CPU graph.

Performance is an architecture property before it is a compiler flag.

The order matters: remove unnecessary work before trying to execute unnecessary work faster.

## Optimization ladder

1. **Semantics/algorithm** — calculate only what the effect actually needs.
2. **Region/extent** — avoid work outside requested/meaningful pixels.
3. **Data layout/memory** — remove per-pixel allocation and improve locality.
4. **Host interaction** — reduce unnecessary checkout/suite traffic.
5. **Reuse/cache** — reuse expensive results only with correct dependency identity.
6. **MFR/threading** — allow useful concurrent work without global serialization.
7. **GPU** — move workloads only when transfer/sync overhead is justified.
8. **Micro-optimization** — SIMD/intrinsics after profiling proves the hotspot.

Do not start at step 8.

## Algorithm budget

For every expensive operation ask:

~~~text
does output really depend on this?
can it be precomputed?
can it be shared safely?
can requested ROI reduce it?
can a cheaper representation preserve semantics?
~~~

An O(N²) algorithm does not become a good architecture because it runs on a GPU.

## Region of interest

SmartFX/pre-render capable effects should express only the input region needed for the requested output where the algorithm permits it.

Wrong dependency rectangles can cause two opposite defects:

- too large: correct but slower;
- too small: fast but incorrect/missing pixels.

ROI optimization therefore needs golden edge/origin fixtures, not only timing.

## Memory architecture

Hot render paths should avoid:

- allocation per pixel;
- allocation per scanline when reusable scratch is possible;
- repeated format conversion;
- giant temporary full-frame buffers for local algorithms;
- unbounded caches;
- false sharing on mutable cross-thread state.

Define scratch ownership explicitly:

~~~text
frame-local
thread-local
instance-owned immutable/read-only
host compute-cache owned
~~~

Never reuse one mutable buffer across concurrent MFR frames without a safe ownership model.

## Host calls

Suite calls/checkouts may be cheap enough individually and still dominate when placed inside a pixel loop.

Prefer:

~~~text
acquire/checkout once at the required scope
→ normalize inputs
→ pure inner compute
→ checkin/release
~~~

Do not cache host-owned pointers beyond their legal lifetime merely to remove a call.

Correct ownership beats a speculative micro-optimization.

## Cache architecture

A cache key must include every input that can change the cached result.

Typical identity dimensions:

- algorithm/schema version;
- parameter values;
- time/frame dependency;
- source identity/revision;
- pixel format;
- dimensions/ROI where relevant;
- backend/device capability where output differs.

A fast stale cache is a correctness bug.

Separate:

- persistent project truth;
- rebuildable runtime cache.

Never make a volatile singleton cache the only source of render-affecting state.

## MFR scaling

Thread safety is gate zero.

Then measure scaling.

Look for:

- one global mutex;
- serialized third-party library;
- mutable singleton;
- shared scratch;
- cache lock held during expensive compute;
- lock held across AE host calls.

More threads with the same wall time and higher memory use is not automatically a win.

## GPU decision

GPU is useful when:

~~~text
compute saved
> upload/preparation + dispatch + synchronization + download/conversion
~~~

Measure small, typical and large frames.

A GPU path can lose on tiny frames and win on 4K/8K. Define the target workload.

Keep a CPU oracle for correctness.

## Interactive tools

For scripts/panels/AEGP tools, performance can be dominated by host interaction rather than pixels.

Measure:

- panel startup;
- selection/state refresh;
- command → host response;
- project traversal;
- evalScript calls;
- file/network/helper latency.

Avoid dozens of tiny evalScript/project reads per UI frame. Batch semantically related work.

## Golden benchmark set

Maintain at least:

### tiny

Overhead-sensitive. Finds startup/dispatch/bridge costs.

### typical

Representative production project. Primary regression gate.

### stress

Large/long composition, many instances, high resolution and extreme parameter values.

Record:

- render wall time;
- frame median/p95;
- CPU utilization;
- peak/retained memory;
- MFR scaling;
- lock wait;
- GPU stage timings;
- cache hit/miss;
- correctness result.

## Benchmark identity

Every result needs:

- plug-in hash;
- baseline hash;
- AE build;
- OS;
- CPU/GPU/driver;
- fixture hash;
- MFR/GPU state;
- sample count;
- warmup policy.

Otherwise a percentage cannot be reproduced.

## Optimization acceptance

An optimization is accepted only if:

1. the target user metric measurably improves;
2. golden output remains within tolerance;
3. MFR/stability tests still pass;
4. memory remains bounded;
5. no unsupported platform assumption was introduced.

Performance never overrides correctness, deterministic state or host stability.

See [performance testing](../10-TESTING/04-PERFORMANCE.md) and [profiling recipe](../12-RECIPES/06-PROFILING.md).
