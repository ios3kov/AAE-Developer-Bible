# AEGP keyframer reference

Status: **sample-derived source reference / runtime not claimed**.

KeyframeRecipes.cpp forwards to the canonical cookbook implementation in 17-NATIVE-SUITE-COOKBOOK/code. Compile the forwarding file or canonical implementation, not both.

## Purpose

This reference demonstrates the operation layer for changing a property stream and its keyframes without duplicating a second AEGP registration lifecycle.

Recommended composition:

~~~text
MenuTool lifecycle
→ validate target item/layer/property
→ acquire stream ref
→ start undo group
→ keyframe batch operation
→ dispose stream
→ end undo group
~~~

Use the MenuTool reference for initialization/hooks and KeyframeRecipes for property/keyframe work.

## Stream identity

A display name is not a stable property API contract.

Prefer the documented stream/property identity path appropriate to the operation and reacquire references after structural mutation when the API can invalidate them.

Never cache a stream ref as an eternal project-object ID.

## Keyframe batch lifecycle

The current SDK review covers StreamSuite6, DynamicStreamSuite4 and KeyframeSuite5 in the supplied 25.6 baseline.

A batch operation should make ownership visible:

~~~text
new stream ref
→ begin batch/add keyframes
→ write keyframe values/interpolation/ease
→ finalize batch
→ dispose temporary refs
~~~

Use the exact suite generation and call signatures from the target SDK headers.

The diagram describes product composition, not all functions in the forwarded
source: the actual helper writes OneD values in CompTime, borrows the stream and
does not set interpolation/ease, Undo or cancellation. See the [scalar recipe and
handoff comparison](../../../14-NATIVE-INTEGRATIONS/06-KEYFRAMERS.md#actual-scalar-recipe-and-async-command-composition-2026-10-07).

## Time/value rules

Before writing a keyframe define:

- stream timebase;
- target time;
- property value type;
- dimensionality;
- separated-dimension behavior;
- interpolation;
- temporal/spatial ease where supported.

Do not reinterpret raw property values without checking the stream type.

## Undo

A user action that creates or edits multiple keyframes should normally appear as one coherent undo operation.

Undo does not repair a partially completed algorithm by itself. Validate target stream and value shapes first.

## Error cleanup

Test failure after:

- stream acquisition;
- first keyframe insertion;
- batch creation;
- value write;
- interpolation write.

Every owned stream/batch/resource still needs its matching cleanup path.

## Product validation cases

If a concrete product claims these operations, useful cases include:

- empty project/no target;
- valid scalar property;
- multidimensional property;
- animated property with existing keys;
- insert before/between/after existing keys;
- separated dimensions if claimed;
- undo/redo;
- save/reopen;
- repeated operation;
- malformed/unsupported target type.

## Verification boundary

The recipe shape has been checked against the supplied SDK source contracts. Bible does not claim a runtime result for this reference. A developer may validate it in the target product/environment as needed.
