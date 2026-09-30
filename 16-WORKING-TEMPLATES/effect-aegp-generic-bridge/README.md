# Effect <-> AEGP generic bridge

Use this only for a pair of plug-ins you control.

## Effect side

Handle `PF_Cmd_COMPLETELY_GENERAL`. Validate payload size/version before reading it.

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
            // Update NON-render-dependent resource/control state here.
            msg->result_code = 0;
            return PF_Err_NONE;
        default:
            msg->result_code = -1;
            return PF_Err_NONE;
    }
}
```

## AEGP side

Resolve the target effect reference, then use `AEGP_EffectCallGeneric()` from the current Effect Suite version. Pass a `MessageV1` pointer as the generic payload according to the exact signature in the SDK header you compile against.

## Do not

- send STL types;
- send pointer to temporary object that dies before call returns;
- use this as hidden render dependency;
- assume struct packing without static assertions/platform checks.
