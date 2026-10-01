# SDK 25.6: GPU, audio and Custom UI / Drawbot

Date: **2026-10-01**. Source: user-supplied `ae25.6_61.64bit.AfterEffectsSDK`.

**Scope: SDK source review and Bible editing.** No new GPU render, audio effect, custom-UI host run or platform performance test was executed.

The accepted SDK TAR SHA-256 remains:

`eee39a787ab09226a5a08c27496335faf79cbe52dd96f19cf795e48af09e2df6`

## GPU contracts

### Capability is a multi-step contract

`AE_Effect.h:1007–1011` declares:

- `PF_OutFlag2_SUPPORTS_GPU_RENDER_F32`;
- `PF_OutFlag2_SUPPORTS_DIRECTX_RENDERING`.

The GPU flag alone is not enough for an individual frame. The header explicitly requires `PF_RenderOutputFlag_GPU_RENDER_POSSIBLE` from pre-render when GPU rendering is possible for the current parameters/context.

`AE_Effect.h:1245,1255–1257` defines Smart Render plus GPU setup/setdown/render selectors.

`AE_Effect.h:2476–2482` lists the framework values present in this SDK: NONE, OPENCL, METAL, CUDA and DIRECTX.

### Per-device state

`AE_Effect.h:2598–2631` gives GPU setup/setdown extras. Setup output contains `gpu_data`; the setdown input comment says the effect must dispose it.

Bundled `SDK_Invert_ProcAmp.cpp:270–423` creates framework-specific device state during `PF_Cmd_GPU_DEVICE_SETUP`, and its dispatcher routes setup, setdown, pre-render, Smart Render and Smart Render GPU separately.

This sample is useful lifecycle evidence, but not a universal backend implementation.

### GPU Device Suite ownership

`AE_EffectGPUSuites.h:50–219` defines frozen `PF_GPUDeviceSuite1`. Source-backed rules include:

- device count/info enumeration;
- exclusive-device access functions for applicable paths;
- device and pinned host memory allocate/free pairs;
- `CreateGPUWorld` paired with `DisposeGPUWorld`;
- only plug-in-created GPU worlds may be disposed by that plug-in;
- GPU world data/size/device-index queries.

The comments say all device memory should be allocated through the suite and reserve purge for emergency cases.

### Sample behavior

`SDK_Invert_ProcAmp.cpp:650–660` sets `GPU_RENDER_POSSIBLE` in pre-render.

`SDK_Invert_ProcAmp.cpp:835–1100` requires `PF_PixelFormat_GPU_BGRA128`, creates an intermediate GPU world, gets GPU buffer addresses, dispatches framework-specific work and disposes the intermediate world.

The sample uses CUDA/OpenCL/DirectX/Metal branches conditionally. Its presence in source does not prove every backend is buildable or available on every target machine.

## Audio contracts

### Audio selectors and flags

`AE_Effect.h:1238–1240` defines:

- `PF_Cmd_AUDIO_RENDER`;
- `PF_Cmd_AUDIO_SETUP`;
- `PF_Cmd_AUDIO_SETDOWN`.

`AE_Effect.h:784–813,971–976` documents audio flags:

- FLOAT_ONLY requires AUDIO_EFFECT_TOO or AUDIO_EFFECT_ONLY;
- AUDIO_IIR marks output dependent on previous output times;
- I_SYNTHESIZE_AUDIO means output can be generated from silence;
- AUDIO_EFFECT_TOO means video effect also filters audio;
- AUDIO_EFFECT_ONLY means audio-only filtering.

These flags are semantics/capabilities, not proof that a particular implementation correctly handles seeking/history.

### Sound format

`AE_Effect.h:1644–1679` defines PCM/float formats, sample sizes, mono/stereo channels, `PF_SoundFormatInfo` and `PF_SoundWorld`.

A SoundWorld carries format info, number of samples and a data pointer. The declaration does not by itself define a production DSP buffering strategy.

### Audio checkout

`AE_Effect.h:2739–2765` exposes layer-audio checkout/checkin and data access. Checkout specifies start/duration/time scale plus requested rate/sample size/channels/signedness; checkin is a separate paired operation.

`PF_InData` and `PF_OutData` contain audio-command-only sample ranges/worlds at `AE_Effect.h:3104–3106,3147–3150`.

### Missing bundled implementation

A source search of the supplied `Examples` tree found the audio selectors/flags only in `AE_Effect.h`; no bundled C/C++ effect implementation in this archive dispatches `PF_Cmd_AUDIO_RENDER`.

Therefore the Bible can document the declared contract, tests and design requirements, but this review does **not** claim an Adobe sample validates a full audio processing lifecycle.

## Custom UI and Drawbot

### Event model

`AE_EffectUI.h:103–117` defines events including NEW_CONTEXT, ACTIVATE, DO_CLICK, DRAG, DRAW, DEACTIVATE, CLOSE_CONTEXT, IDLE, ADJUST_CURSOR, KEYDOWN and MOUSE_EXITED.

`AE_EffectUI.h:539–551` places event type, type-specific union, window/context data, callbacks, input flags and output flags into `PF_EventExtra`.

`AE_Effect.h:701–724,958,1006` requires `PF_OutFlag_CUSTOM_UI` for custom effect UI and documents the async-manager flag for UI frame requests.

### Registering custom UI

`AE_EffectUI.h:558–579` defines `PF_CustomUIInfo` and event targets for comp/layer/effect/preview contexts.

The custom-UI flag, registering UI areas and handling `PF_Cmd_EVENT` are distinct steps.

### Drawing reference and Drawbot lifetime

`AE_EffectSuites.h:653–665` defines the current custom-UI suite call for obtaining a drawing reference from an event context.

`DrawbotSuite.h:113–204` defines Draw/Supplier/Surface suites. The source comments make a key ownership distinction:

- supplier/surface references obtained from a draw reference are borrowed and must not be released as newly-created objects;
- pens, brushes, fonts and other objects created through the supplier are released through `ReleaseObject`.

### Bundled UI samples

`Custom_ECW_UI.cpp:95–110,340–360` enables custom UI and dispatches `PF_Cmd_EVENT`.

`Custom_ECW_UIUI.cpp:87–208` acquires Drawbot suites, obtains drawing reference/supplier/surface, creates path/brush/font resources, releases created resources, releases acquired suites and marks a handled draw event.

`Custom_ECW_UIUI.cpp:299–325` dispatches click, drag, draw and cursor adjustment.

`CCU.cpp/CCU_UI.cpp` provides a larger second sample using the same event/Drawbot family. It is useful cross-checking, not a host acceptance run.

## Async custom-UI boundary

The 25.6 header explicitly says that after the UI/render thread split, custom UI frames should no longer be synchronously rendered and describes `PF_OutFlag2_CUSTOM_UI_ASYNC_MANAGER`.

This is a source contract, not evidence that the current Bible has an async-manager implementation. New custom UI that needs rendered frames must treat async lifetime/cancellation as a first-class design problem.

## Source identity

| File | SHA-256 |
|---|---|
| `Examples/Headers/AE_Effect.h` | `5432df9bb447cefce2f96c1477d6beccd4686b7236d460c803beab76dae1d537` |
| `Examples/Headers/AE_EffectGPUSuites.h` | `55fb5dddbb0c33dfc218f9cb9ff77589803f6a6c3080fe889d87bccef242a321` |
| `Examples/Headers/AE_EffectUI.h` | `ffec9e25ac13a278f3ef0889bb33968fb338f41942ad16d13b3b53f03a235075` |
| `Examples/Headers/AE_EffectSuites.h` | reviewed current custom-UI suite declaration; hash retained in local source audit |
| `Examples/Headers/adobesdk/DrawbotSuite.h` | `c5c4f294b6c7f4628654172bca75c7b256ddfe302ce5f0dbaf08a0cd2156f2ad` |
| `Examples/Effect/SDK_Invert_ProcAmp/SDK_Invert_ProcAmp.cpp` | `d345bd2923f0c3c88907b1164de1c9096145f7a7f58ab7425ba5bd20cf85702a` |
| `Examples/Effect/SDK_Invert_ProcAmp/SDK_Invert_ProcAmp.h` | `0f6a6d909187b271c047d64be994696db067966e6fcdc525475d07464c98b77b` |
| `Examples/Effect/SDK_Invert_ProcAmp/SDK_Invert_ProcAmpPiPL.r` | `a68ea229981ab613028fa1a63af22f4c74e0a7255f249941004bb8b7e747b5dc` |
| `Examples/UI/Custom_ECW_UI/Custom_ECW_UI.cpp` | `55b0079b4319d83ded86fa6a1e302e0e77e543188cf76c7f28bbfa6bb851375c` |
| `Examples/UI/Custom_ECW_UI/Custom_ECW_UIUI.cpp` | `ebd69d9ce67f0271bf0d52c278739131e82a7007fccdeca28d2f9df4ba19112a` |
| `Examples/UI/CCU/CCU.cpp` | `1fe303cfa03327d79bf57568924b9a9c695af0e3b776db948a7e4a06ec53dd59` |
| `Examples/UI/CCU/CCU_UI.cpp` | `ed437ced4a200704f38fb0f63b2649441198910d7720b62133cf6ecfd4559181` |

## Verification boundary

NOT RUN in this editorial iteration:

- GPU build for each framework;
- device setup/setdown in AE;
- GPU world allocation failure injection;
- CPU↔GPU pixel comparison;
- audio effect build/render;
- seek/IIR/synthesis audio tests;
- custom UI click/drag/draw in AE;
- Retina/HiDPI and theme tests;
- async custom-UI frame request/cancel lifecycle;
- leak checks for Drawbot resources;
- Windows host verification.

These remain Gate 4/6/7 work.
