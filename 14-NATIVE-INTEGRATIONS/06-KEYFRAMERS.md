# Keyframers

Keyframer — AEGP-oriented tool that reads and changes property streams/keyframes. Historically such tools often appear under **Animation → Keyframe Assistant**, but product UI can be elsewhere if the architecture requires it.

The important part is not the menu location. The important part is the property/keyframe contract.

## When to use

Use a native Keyframer/AEGP path when the tool needs:

- large keyframe batches;
- access to stream/keyframe metadata not convenient in scripting;
- native performance;
- integration with AEGP commands/hooks;
- shared native logic with another plug-in component.

For ordinary project automation, ExtendScript may be simpler.

## When not to use

Do not choose a native keyframer only because “C++ is faster”.

Avoid it when:

- operation is small and scripting already exposes the needed property;
- UI/pipeline iteration speed matters more than native throughput;
- product would become dependent on opaque handles for no practical benefit.

## Core model

~~~text
find target property/stream
→ validate property type/capability
→ decide value-time vs keyframe-index operation
→ open undo scope if mutating
→ perform single or batch keyframe operation
→ dispose owned refs/values
→ refresh/report result
~~~

## Streams first, keyframes second

AEGP keyframe API operates on streams/properties.

Before changing keys, determine:

- which stream is targeted;
- stream type;
- value dimensionality;
- temporal dimensionality;
- whether it is time-varying;
- number of keyframes;
- whether dimensions are separated;
- whether the passed ref is a leader or follower where relevant.

Do not treat “property has zero keys” as equivalent to “property is constant”: an expression may still drive the property.

## SDK 25.6 baseline

Current Bible baseline uses:

- `AEGP_StreamSuite6`;
- `AEGP_DynamicStreamSuite4`;
- `AEGP_KeyframeSuite5`.

Older Adobe samples may use earlier suite generations. They are useful for patterns, not as current signature authority.

See the [SDK 25.6 stream/keyframe source review](../18-SDK-HEADER-TOOLS/10-STREAMS-KEYFRAMES-SDK25.6.md).

## Ownership

### Stream refs

APIs returning a **new** `AEGP_StreamRefH` generally create caller-owned refs that must be disposed with the matching Stream Suite function.

Do not keep a stream ref forever.

Structural project/property changes can invalidate assumptions about:

- index;
- hierarchy;
- parent;
- selection;
- stream identity.

If long-lived product state needs to refer to a property, store a stable product-level description/ID where possible and re-resolve the host ref at operation time.

### Stream values

Functions returning `AEGP_StreamValue2` via “GetNew...” create values that require the documented dispose path.

Set-functions do not imply transfer of ownership unless documented.

### Strings/memory handles

Expression/name APIs may return Memory Suite handles rather than C++ strings. Lock/copy/unlock/free according to the memory contract.

## Time models

Do not casually mix:

- layer time;
- composition time;
- stream time;
- keyframe index.

A keyframe API may use `A_Time` plus an AEGP time mode; another API may address a key by index.

Keep conversions explicit at the boundary.

## Value dimensionality vs temporal dimensionality

These are different questions.

Examples:

- spatial value may have multiple value dimensions;
- temporal ease array is indexed by temporal dimensionality;
- separated dimensions can change which stream is legal for keyframe-index operations.

Do not size ease/tangent data by guessing from UI appearance.

## Separated dimensions

For separated properties, value access and keyframe-index access do not necessarily have the same legal target.

Practical rule:

1. inspect separation state;
2. resolve the correct follower stream where keyframe-index API requires it;
3. perform operation on that stream;
4. dispose the resolved ref.

Do not assume leader key indexes map 1:1 to follower keys.

## Reading keyframes

Typical questions:

- number of keys;
- key time;
- key value;
- interpolation type;
- temporal ease;
- spatial tangents;
- flags;
- label color.

Read only what the feature needs. A “dump everything” helper quickly becomes slow on large projects.

## Single-key mutation

Typical sequence:

~~~text
resolve stream
→ validate stream supports keys
→ find/insert target key
→ set value/interpolation/ease/flags
→ release temporary values/refs
~~~

`InsertKeyframe` may return an existing key index when a key already exists at that time; do not automatically interpret that as a newly-created key.

## Batch mutation

For many keys use the batch family instead of repeated independent insertion:

~~~text
AEGP_StartAddKeyframes
→ AEGP_AddKeyframes
→ AEGP_SetAddKeyframe
→ ...
→ AEGP_EndAddKeyframes
~~~

Benefits:

- clearer transaction boundary;
- less repeated host bookkeeping;
- easier error/cleanup reasoning;
- better fit for bulk generation.

Do not forget to close the batch if a middle operation fails. Use structured cleanup/RAII around host transactions where practical.

### Actual scalar recipe and async command composition — 2026-10-07

[`Bible_AddOneDKeyframes`](../17-NATIVE-SUITE-COOKBOOK/code/KeyframeRecipes.cpp)
borrows its stream and times/values arrays, validates OneD and uses **CompTime** for
both sampling and insertion. It acquires/disposes each StreamValue and calls
`EndAddKeyframes(FALSE, addH)` on ordinary error, TRUE on success. If End itself
fails, commit outcome is not proved; it preserves an earlier error but does not
log the secondary error. No interpolation/ease, Undo, cancellation token, target
resolver or exception-safe batch owner is implemented by this helper.

Worked command design: capture project epoch + layer/property identity and desired
scalar keys; worker computes only owned finite times/values; host callback checks
cancel/freshness, resolves the current stream and separated follower if required,
validates type/expression/duplicate-time policy, successfully starts Undo, calls
the scalar helper, disposes caller-owned refs and ends the opened Undo scope.
Configure interpolation/ease only in a separate legal step after successful batch
finalization and fresh key-index resolution, not through a guessed staged index.
This links the [Animate route](../17-NATIVE-SUITE-COOKBOOK/06-KEYFRAMES.md) without
attributing the command layer to the helper.

The helper has no mid-loop cancellation support. Check cancel before calling it;
after return report committed/failed/uncertain work honestly. A product needing
interruptible batches must implement explicit safe-point/End(FALSE) handling and
preserve partial-result and cleanup diagnostics; dropping a response is not rollback.

## Undo

Wrap user-visible mutation in an appropriate undo group.

Undo is not identical to database rollback:

- an operation can partially mutate before an error;
- cleanup can also fail;
- nested/host-owned undo behavior has its own contract.

Document product behavior for partial failure.

## Interpolation and ease

Treat separately:

- temporal interpolation;
- spatial interpolation;
- temporal ease;
- spatial tangents;
- key flags.

Changing one does not imply the others.

Preserve existing properties the tool is not intentionally changing.

## Expressions

A property can have:

- keyframes;
- expression;
- both.

A keyframer should define whether it:

- preserves expression;
- disables expression;
- refuses the operation;
- edits keys underneath the expression.

Do not silently change expression state unless that is the feature.

## Selection

If the tool starts from UI selection, treat selection only as an **input snapshot**.

Before committing mutation:

- validate active comp;
- validate selected properties;
- validate expected layer/property identity;
- reject stale/unsupported targets.

Avoid storing selection-derived refs across unrelated user actions.

## Threading

Project/property mutation belongs on a documented host-safe execution path.

Do not mutate AEGP streams from an arbitrary worker thread because the computation that produced the key values happened in background.

Safe pattern:

~~~text
worker: compute pure values/times
→ main/host-safe callback: resolve streams + mutate keys
~~~

## Failure model

Handle at least:

- no active comp;
- no target property;
- unsupported stream type;
- stale/invalid stream;
- expression policy conflict;
- separated-dimension mismatch;
- invalid time/value;
- failure to start batch/undo;
- partial batch failure;
- cleanup/dispose error.

User-facing errors should identify the property/operation, not just an opaque numeric host code.

## Production workflow

1. Define exact target-property rules.
2. Build pure representation of desired keys.
3. Resolve host property immediately before mutation.
4. Validate stream/keyframe capabilities.
5. Open undo scope.
6. Use batch API for bulk keys.
7. Preserve unrelated interpolation/expression state.
8. Dispose every owned ref/value.
9. Refresh/report result.
10. Re-resolve on next command rather than caching opaque refs indefinitely.

## Reference samples

### Easy Cheese

Useful for:

- expression/value inspection;
- stream info;
- interpolation/ease patterns.

It uses historical suite generations; do not copy those generations as the current SDK baseline.

### Streamie

Useful for:

- stream hierarchy;
- structural stream operations;
- cleanup patterns.

It also contains historical API shapes.

### Mangler

Historically demonstrates more elaborate keyframer UI concepts, but old ADM-era UI architecture is not a recommended new-product UI stack.

## Related Bible material

- [Streams/properties cookbook](../17-NATIVE-SUITE-COOKBOOK/05-STREAMS-PROPERTIES.md)
- [Keyframes cookbook](../17-NATIVE-SUITE-COOKBOOK/06-KEYFRAMES.md)
- [Keyframer batch template](../16-WORKING-TEMPLATES/keyframer-batch/README.md)
- [Undo transactions](../19-NATIVE-CODE-FOUNDATION/03-UNDO-TRANSACTIONS.md)
- [Lifetime/threading](../17-NATIVE-SUITE-COOKBOOK/14-LIFETIME-THREADING.md)

## Evidence boundary

The suite generations and lifecycle rules above are SDK-contract-reviewed against the supplied SDK 25.6 source material. Bible does not claim a universal runtime result for a particular Keyframer binary.
