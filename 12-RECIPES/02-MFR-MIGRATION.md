# Recipe — migrate an existing effect to MFR

## Rule 0

Keep MFR capability disabled in the shipping build until concurrency evidence exists.

Use a separately identifiable experimental build while migrating.

## Step 1 — inventory mutable state

List every:

- global/static variable;
- singleton;
- sequence/instance object;
- cache;
- lazy initializer;
- third-party library;
- scratch buffer;
- log/profiler object.

For each, classify:

~~~text
immutable shared
per-effect-instance
per-render-frame/thread
host-owned borrowed
product cache with synchronization
unsafe/unknown
~~~

Unknown is a blocker until resolved.

## Step 2 — inspect render writes

Search every render/pre-render callback for writes to shared or sequence state.

Ask:

- can two frames write this simultaneously?;
- can two effect instances collide?;
- is state keyed by all dependencies?;
- can cancel/error leave half-written state?;
- is any pointer borrowed beyond callback lifetime?

## Step 3 — make scratch local

Move temporary render data to:

- stack/local objects;
- frame-local allocation;
- host-supported thread-local render data;
- immutable shared tables.

Do not make scratch safe by placing one giant global mutex around the render.

## Step 4 — caches

A cache needs:

- complete key;
- immutable or safely synchronized values;
- bounded lifetime/size;
- cancellation/error semantics;
- no stale project/parameter dependency.

If using host cache APIs, follow their documented ownership and receipt rules.

## Step 5 — third-party code

Prove thread safety or isolate it.

A library working in multiple applications does not prove concurrent calls are safe.

If it has hidden global state, consider:

- immutable precomputation;
- per-instance context;
- serialized adapter only around the unsafe library;
- replacement library.

Measure serialization cost.

## Step 6 — host calls and locks

Never hold a product mutex across a host callback/suite call unless the API and lock ordering are explicitly proven safe.

This is a deadlock risk.

## Step 7 — create diagnostic stress fixture

Use several instances with intentionally different outputs/parameters.

Run:

- long render;
- 20+ instances;
- multiple comps;
- random seek;
- cancel/restart;
- cache purge;
- repeated 50-100+ loops;
- GPU + MFR if both claimed.

Log lightweight instance/frame/thread identity.

## Step 8 — compare MFR off vs on

Correctness first.

Expected:

- deterministic output;
- no state bleed;
- no crash;
- no hang;
- no unbounded memory growth.

Pixel comparison must use the render-correctness tolerance defined before the migration.

## Step 9 — enable capability only in candidate

After stress passes, enable the MFR declaration in a candidate build.

Then repeat host tests because changing capability flags changes scheduling.

## Step 10 — performance

Measure:

- wall time;
- CPU utilization;
- peak memory;
- lock wait;
- speedup vs MFR off.

A globally serialized MFR-safe effect may be correct but deliver no benefit. That is a performance decision, not a correctness PASS.

## Step 11 — release gate

Ship MFR only when:

- correctness PASS;
- repeated stress PASS;
- cancellation PASS;
- migration/persistence PASS;
- memory bounded;
- performance acceptable;
- every claimed platform/architecture covered.

Otherwise keep the feature flag off and document the limitation.
