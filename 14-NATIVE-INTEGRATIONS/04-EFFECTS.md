# Effect plug-ins — native capability map

Baseline for source-backed statements: **After Effects SDK 25.6 build 61**. Later-SDK notes must stay version-gated.

## Host contract

After Effects enters an Effect plug-in through `EffectMain` and `PF_Cmd` selectors. `PF_InData`, `PF_OutData`, params, worlds and selector-specific `extra` structures have command-scoped contracts.

The effect family includes pixel/video, audio, SmartFX, GPU, custom UI and parameter supervision. Those are capabilities/paths of the Effect API, not separate plug-in types.

## Registration / metadata

- PiPL and runtime registration;
- display name, match name, category, product version;
- out_flags / out_flags2;
- platform architecture entries;
- flags that must agree between PiPL/global setup unless the documented override mechanism is intentionally used.

Later SDK registration additions are not silently applied to the 25.6 baseline.

## Parameters

Standard parameter families include slider/fixed/float, checkbox, angle, point/3D point, color, popup, layer, button, arbitrary data and topics/groups.

Parameter IDs/order are project compatibility state. UI flags, animation/interpolation and dynamic UI changes are separate concerns; see [Parameters and UI](../02-EFFECT-PLUGINS/02-PARAMETERS-UI.md).

## Classic render

Classic `PF_Cmd_RENDER` is the simple pixel path. Correct code still respects:

- actual dimensions;
- rowbytes;
- origin/extent;
- bit depth;
- alpha/premultiplication;
- cancellation/progress where applicable.

## SmartFX

SmartFX separates dependency declaration from rendering:

```text
SMART_PRE_RENDER
  request inputs/regions
  declare result/max-result
  create pre-render data
      ↓
SMART_RENDER
  checkout pixels
  process
  check in / cleanup
```

See [SmartFX](../02-EFFECT-PLUGINS/03-SMARTFX.md).

## GPU render

SDK 25.6 adds a specific GPU lifecycle:

```text
GPU_DEVICE_SETUP
SMART_PRE_RENDER (+ GPU_RENDER_POSSIBLE for this frame)
SMART_RENDER_GPU
GPU_DEVICE_SETDOWN
```

`PF_OutFlag2_SUPPORTS_GPU_RENDER_F32` is global capability; it does not by itself guarantee a GPU render for every frame.

Per-device state and GPU world/memory ownership are documented in [GPU effects](../02-EFFECT-PLUGINS/05-GPU.md).

## Audio

Audio uses separate selectors:

- AUDIO_SETUP;
- AUDIO_RENDER;
- AUDIO_SETDOWN.

Audio semantics have dedicated flags for audio-only/video+audio, float-only, IIR and synthesis. SoundWorld/sample ranges are separate from pixel worlds.

The supplied 25.6 archive contains the declarations but no bundled effect source that dispatches AUDIO_RENDER; see [Audio effects](../02-EFFECT-PLUGINS/07-AUDIO.md).

## Custom UI / events

Custom effect UI combines:

```text
PF_OutFlag_CUSTOM_UI
+ register_ui(PF_CustomUIInfo)
+ PF_Cmd_EVENT
```

Event contexts include Effect Controls and, when registered, Layer/Comp UI. Drawbot supplies host drawing primitives.

Created Drawbot objects and borrowed drawing/supplier/surface references have different ownership. Modern custom UI needing rendered frames must also account for the async-manager contract.

See [Custom UI / Drawbot](../02-EFFECT-PLUGINS/09-CUSTOM-UI-DRAWBOT.md).

## Lifecycle state

- `global_data`: module/effect global state;
- `sequence_data`: effect-instance state;
- render-thread/flattening rules depend on flags;
- pre-render data: render request state with its own deletion callback;
- GPU data: per-device effect-owned state returned through GPU setup;
- parameters: AE-owned persistent project state.

See [Memory/lifetime/errors](../01-ARCHITECTURE/02-MEMORY-THREADING-ERRORS.md).

## MFR

MFR is an execution model, not a second effect API. Declaring support changes concurrency expectations around render and sequence state.

See [MFR/thread safety](../02-EFFECT-PLUGINS/04-MFR-THREAD-SAFETY.md).

## Data ownership rule

| Data | Typical owner | Safe lifetime |
|---|---|---|
| `PF_InData*` | AE | current selector |
| passed parameter defs | AE | current selector unless API says otherwise |
| host input/output world | AE | command/checkout lifetime |
| plug-in-created GPU world | plug-in | until matching DisposeGPUWorld |
| created Drawbot objects | plug-in | until ReleaseObject |
| Drawbot supplier/surface from DrawRef | host/borrowed | event/context contract |
| locked handle pointer | temporary | while locked |

Exact ownership always comes from the specific suite/selector contract.

## Render determinism

Final pixels/audio must be a deterministic function of declared dependencies. Hidden project state queried through AEGP or native globals can break AE cache invalidation.

Generic native bridge calls are control/service mechanisms, not a license to create invisible render dependencies.

## Minimal production rules

1. match name and released parameter IDs stay stable;
2. exceptions never cross the C ABI;
3. CPU reference correctness precedes GPU optimization;
4. GPU capability is enabled only with correct per-frame fallback;
5. MFR capability follows concurrency testing;
6. custom UI does not block on synchronous frame renders;
7. audio state does not assume strictly forward timeline requests;
8. host/suite calls are made only from contexts where the target API permits them.

Source review for GPU/audio/Custom UI: [15-GPU-AUDIO-CUSTOM-UI-SDK25.6.md](../18-SDK-HEADER-TOOLS/15-GPU-AUDIO-CUSTOM-UI-SDK25.6.md).
