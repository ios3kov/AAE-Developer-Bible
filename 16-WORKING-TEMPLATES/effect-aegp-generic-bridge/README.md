# Effect ↔ AEGP generic bridge

Status: **protocol template; source-reviewed against SDK 25.6, not host-verified**.

Use this only for a pair of plug-ins you control. See [AEGP → Effect](../../15-COMMUNICATION/03-AEGP-TO-EFFECT.md).

## Current AEGP call shape

In SDK 25.6 `AEGP_EffectSuite4::AEGP_EffectCallGeneric` takes:

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

Handle `PF_Cmd_COMPLETELY_GENERAL` and validate payload size/version before reading it.

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
            msg->result_code = 0;
            return PF_Err_NONE;
        default:
            msg->result_code = -1;
            return PF_Err_NONE;
    }
}
```

This example assumes the effect command is already on the correct SDK callback path. It does not permit storing `extra` after return.

## AEGP side

1. resolve the target `AEGP_EffectRefH`;
2. convert time to the target layer timebase when needed;
3. build a versioned payload;
4. call `AEGP_EffectCallGeneric(..., PF_Cmd_COMPLETELY_GENERAL, &payload)`;
5. distinguish the returned `A_Err` from `payload.result_code`;
6. dispose the effect ref according to its ownership contract.

## Do not

- send STL types;
- send a temporary pointer that the effect stores for later use;
- assume struct packing without explicit checks;
- use hidden mutable state as a render dependency;
- treat old EffectSuite2 sample syntax as current EffectSuite4 syntax;
- swallow host-call error because the protocol field looks successful.

## Required acceptance

- missing target;
- short/wrong-version payload;
- unknown opcode;
- correct response;
- correct layer time;
- target removal/reorder;
- repeated calls;
- cache invalidation behavior for any render-affecting state.
