# Effect ↔ AEGP generic bridge

Status: **protocol/source template; SDK 25.6 contract-reviewed; runtime result not claimed**.

Use this only for a pair of plug-ins you control. See [AEGP → Effect](../../15-COMMUNICATION/03-AEGP-TO-EFFECT.md).

## Current AEGP call shape

In SDK 25.6 current `AEGP_EffectSuite5::AEGP_EffectCallGeneric` takes:

```text
plugin id
effect ref
time in the target layer timebase
PF_Cmd
void* extra
```

For the historical generic behavior pass `PF_Cmd_COMPLETELY_GENERAL`.

Do **not** copy the old ProjDumper EffectSuite2 call shape literally; that bundled sample predates the explicit command argument.

## Effect side

Handle `PF_Cmd_COMPLETELY_GENERAL` and validate payload size/version before reading it. `Protocol.h` also pins standard-layout/trivially-copyable requirements, 32-bit opcode width, total size and field offsets so accidental compiler-visible ABI drift fails at build time.

```cpp
case PF_Cmd_COMPLETELY_GENERAL: {
    auto* msg = static_cast<bible_bridge::MessageV1*>(extra);
    if (!msg || msg->size < sizeof(*msg) || msg->version != bible_bridge::kVersion)
        return PF_Err_BAD_CALLBACK_PARAM;

    switch (msg->op) {
        case bible_bridge::Op::Ping:
            msg->result_code = 0;
            return PF_Err_NONE;
        case bible_bridge::Op::ReloadResources:
            // This protocol lesson has no resource reload implementation.
            msg->result_code = -1;
            return PF_Err_NONE;
        default:
            msg->result_code = -1;
            return PF_Err_NONE;
    }
}
```

This example assumes the effect command is already on the correct SDK callback path. It does not permit storing `extra` after return.

Ping is the only implemented illustrative operation. ReloadResources refuses the
domain command until a concrete service/dependency invalidation is implemented.
Size is a declaration, not proof of arbitrary pointer readability; the same-product
caller must allocate the complete shared struct.

## AEGP side

1. resolve the target `AEGP_EffectRefH`;
2. convert time to the target layer timebase when needed;
3. build a versioned payload;
   set a product-defined non-success result sentinel explicitly (`Protocol.h`
   defaults to zero); `AEGP_ConvertCompToLayerTime` is the host conversion API;
4. call `AEGP_EffectCallGeneric(..., PF_Cmd_COMPLETELY_GENERAL, &payload)`;
5. distinguish the returned `A_Err` from `payload.result_code`;
6. dispose the effect ref according to its ownership contract.

This is a caller design, not a shipped AEGP resolver/caller implementation. Recheck
effect identity after resolving the current layer; a remembered index alone is not
stable across reorder/removal. Preserve delivery error first and cleanup separately.

## Do not

- send STL types;
- send a temporary pointer that the effect stores for later use;
- assume struct packing/layout without explicit compile-time checks on every binary that participates;
- use hidden mutable state as a render dependency;
- treat old EffectSuite2/legacy syntax as current EffectSuite5 syntax;
- swallow host-call error because the protocol field looks successful.

## Product validation cases

- missing target;
- short/wrong-version payload;
- unknown opcode;
- correct response;
- correct layer time;
- target removal/reorder;
- repeated calls;
- cache invalidation behavior for any render-affecting state.
