# Keyframer batch working pattern

Status: **API recipe / host-test-required**.

Use this inside an AEGP based on the exact SDK sample such as Easy Cheese, with suite generations checked against target headers.

## Goal

For many keyframes, use the Keyframe Suite batch-add transaction rather than independent insert/update work for every key when the batch API matches the operation.

Conceptual flow:

~~~text
validate stream
→ start user undo group
→ StartAddKeyframes(stream)
→ for each desired key:
    AddKeyframes(time → new index)
    SetAddKeyframe(index, value)
    configure interpolation/ease when needed
→ EndAddKeyframes
→ release temporary values/refs
→ end undo group
~~~

## Preconditions

Before opening the batch:

- stream ref is valid;
- stream can accept keyframes;
- value type/dimension is known;
- target times are in the correct timebase;
- expression/separated-dimension behavior is understood;
- desired duplicate-time policy is defined.

## Value ownership

AEGP stream values and keyframe values can have type-specific ownership.

Do not memcpy arbitrary value unions into long-lived storage without understanding the current SDK contract.

Release any host-owned/allocated value data with the matching API.

## Batch error path

A real wrapper must decide what happens when operation N fails after earlier keys were staged.

Keep:

- batch handle/state ownership;
- stream ref cleanup;
- undo end;
- primary error;
- cleanup errors where they matter.

Do not early-return from the loop and leak the batch transaction.

## Existing keyframes

Define whether the command:

- inserts alongside existing keys;
- replaces at matching times;
- clears a range first;
- updates values only.

Do not let the behavior emerge accidentally from host duplicate-time semantics.

## Interpolation/ease

If the product promises interpolation/easing, add explicit host tests for:

- linear;
- hold;
- bezier where supported;
- temporal ease arrays/dimensions;
- spatial tangents for spatial streams;
- roving/continuous flags where relevant.

A key value alone is not the whole keyframe state.

## Undo

The complete user operation should generally be one undo group.

Test Undo and Redo in AE, not only function return codes.

## Stress fixture

Generate a known number of keys, for example hundreds or thousands, then verify:

- final key count;
- times;
- values;
- interpolation;
- performance;
- undo;
- save/reopen.

## Verification boundary

This template documents the transaction shape. Exact KeyframeSuite signatures, value ownership and stream generations must come from the SDK compiled by the product, and host behavior remains pending until tested.
