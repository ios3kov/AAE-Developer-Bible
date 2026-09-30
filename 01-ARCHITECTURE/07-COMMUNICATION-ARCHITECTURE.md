# Communication architecture — one-page rulebook

## Host-owned channels

- Effect: AE -> `PF_Cmd` -> `EffectMain`.
- AEGP: AE -> registered hooks; AEGP -> AE via suites.
- AEIO: AE -> registered function block.
- Artisan: AE -> renderer entry points.
- Script: JS -> AE scripting DOM.
- CEP: panel JS -> `evalScript` -> ExtendScript -> AE.

## Cross-component channels

1. **AEGP -> Effect**: `AEGP_EffectCallGeneric` / `PF_Cmd_COMPLETELY_GENERAL`.
2. **Native -> Native**: published PICA suite.
3. **AEGP -> Script**: `AEGP_ExecuteScript`.
4. **CEP -> Script**: `CSInterface.evalScript`.
5. **CEP events**: event bus for UI/event notification, not bulk binary transfer.
6. **External service**: explicit IPC you own; do not depend on undocumented AE internals.

## Choose by payload

| Payload | Best channel |
|---|---|
| effect parameter / render dependency | AE parameter stream / Effect API |
| project mutation | AEGP or scripting DOM |
| native control message | generic effect call or published suite |
| UI command | CEP/UXP -> script/native command bridge |
| large pixels/binary | native memory/GPU/file/IPC; not ExtendScript JSON |
| cross-process batch metadata | JSON/protobuf over owned IPC |

## Absolute rule

The communication path must preserve **dependency visibility, thread rules and ownership**. Fast but hidden state is not an optimization; in AE it is a future cache/crash bug.
