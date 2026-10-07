# After Effects → Effect plug-in

Сквозной [state/arbitrary walkthrough](../02-EFFECT-PLUGINS/02-PARAMETERS-UI.md#13-сохраняемое-состояние-и-arbitrary-data)
связывает command dispatch, borrowed input, owned callback output и wire schema.
Не читать arbitrary union до проверки команды/type ID; обычный render не передаёт
плагину владение parameter value. Copy/flatten не является отправкой runtime cache
между процессами.

An Effect plug-in is primarily reactive: After Effects calls the exported effect dispatcher with selector commands and selector-specific data.

## Dispatcher boundary

Conceptual current shape:

~~~cpp
PF_Err EffectMain(
    PF_Cmd cmd,
    PF_InData* in_data,
    PF_OutData* out_data,
    PF_ParamDef* params[],
    PF_LayerDef* output,
    void* extra);
~~~

The exact declaration/export macros come from the target SDK.

The meaning and validity of every other argument depends on cmd.

Do not assume params, output or extra carry the same data for every selector.

## Input channels

### PF_InData

Host/context data such as:

- current time/time scale;
- effect reference;
- project/render context;
- quality/field information;
- PICA suite access;
- callbacks.

Fields are selector/version-sensitive.

### Parameter array

Current parameter values for selectors where parameter data is supplied.

The parameter index contract must agree with ParamsSetup and persistent parameter IDs.

### Output world

Only meaningful for selectors/render paths that provide it.

SmartFX uses its own checkout/output callback flow rather than treating the classic output argument as universal.

### extra

Selector-specific payload.

Examples include:

- Smart pre-render/render structures;
- custom UI events;
- parameter supervision data;
- generic Effect/AEGP communication payload.

Always cast extra according to the current selector only after null/contract validation.

## Output channels

The effect communicates back through:

- returned PF_Err;
- PF_OutData flags/version/message/state;
- rendered output;
- selector-specific structures;
- suite/callback calls to the host.

Return errors should preserve the primary failure while still performing mandatory cleanup/checkin.

## Lifecycle classes

A useful mental map:

~~~text
registration/export
→ GLOBAL_SETUP
→ PARAMS_SETUP
→ sequence/instance selectors
→ render/pre-render/events many times
→ sequence teardown
→ GLOBAL_SETDOWN
~~~

Do not infer one fixed call order for every selector beyond documented guarantees.

Render/event calls can occur many times and under concurrency rules such as MFR.

## State layers

Separate:

- process/global immutable configuration;
- host-owned global_data;
- per-effect sequence/instance state;
- per-render/frame scratch;
- GPU device state;
- external cache/service state.

Render-affecting state must be visible to the host dependency/cache model.

A hidden mutable singleton is dangerous both for MFR and caching.

## Threading

When an effect declares threaded rendering, relevant render/sequence selectors can execute concurrently according to the SDK MFR contract.

Do not set the flag until every render dependency is thread-safe.

UI selectors remain a different threading class; do not solve a render-to-UI communication problem with arbitrary cross-thread host calls.

## Ownership

Callback pointers/worlds/structures are host-owned unless the API explicitly transfers ownership.

Never retain a callback-scoped raw pointer because it appears stable in one run.

Every checkout has its matching checkin; every created host resource follows its exact release API.

## Effect should not become project automation

A render effect is not the right layer for arbitrary ongoing project mutation.

If the product needs:

- menus;
- project graph edits;
- import/render automation;
- persistent panel controller;

use AEGP, scripting/panel or another documented host integration.

Keep the Effect responsible for effect-instance semantics/render/UI selectors.

## Generic calls

An AEGP can synchronously call a specific effect instance through the documented generic-call path.

That is a control bridge, not a hidden render dependency system.

See [AEGP → Effect](03-AEGP-TO-EFFECT.md).

## Failure tests

For every implemented selector test:

- null/invalid optional input where contract permits;
- host call failure;
- allocation failure policy;
- checkout then later failure;
- cancellation;
- repeated invocation;
- project save/reopen for persistent state;
- MFR concurrency if claimed;
- shutdown.

## Verification boundary

The dispatcher model is defined by the target Effect SDK. Illustrative selector flows in this Bible do not replace exact header signatures or host execution.
