# Effect plug-ins — полный native map

## Host contract

After Effects инициирует всё через `EffectMain` и `PF_Cmd` selectors. `PF_InData` — входной host context; `PF_OutData` — capabilities/state обратно в AE; `PF_ParamDef[]` — parameters; `PF_LayerDef` / `PF_EffectWorld` — image buffers.

## Категории поведения

### Registration / metadata
- PiPL / runtime registration
- display name, match name, category, version
- out flags / out flags 2
- current SDK 26.5 adds effect search keywords/description support in the current registration/PiPL model; exact macro/version сверять с current SDK.

### Parameters
- sliders/fixed/float
- checkbox
- angle
- point / 3D point
- color
- popup
- layer
- button
- arbitrary data
- groups/topics

### Render
- classic `PF_Cmd_RENDER`
- SmartFX pre-render/render
- output resizing
- layer checkout at arbitrary time
- ROI/extent hints
- iteration suites
- 8/16/32-bpc paths
- premultiplication / color management

### Lifecycle state
- global data: module-wide
- sequence data: effect-instance state
- frame data: render-local
- parameters: AE-owned persistent project state

### UI/events
- Effect Controls custom control
- Composition/Layer overlay controls
- Drawbot drawing
- parameter supervision

### Performance
- MFR
- host iterate suites
- GPU render
- async frame acquisition for passive custom UI in newer SDKs

## Data ownership rule

| Data | Owner | Safe lifetime |
|---|---|---|
| `PF_InData*` | AE | current selector only |
| `PF_ParamDef*` passed in | AE | current selector only |
| `PF_EffectWorld` | AE | callback scope unless documented otherwise |
| global/sequence handles allocated through AE | plug-in + AE handle system | documented lifecycle |
| raw pointer inside locked handle | temporary | only while handle locked |

## Render determinism

Effect output must be a deterministic function of declared dependencies. If render depends on hidden project state queried via AEGP, AE cache invalidation may be wrong. Do not use AEGP queries as invisible render inputs.

## Minimal production rule

1. parameter IDs stable forever after release;
2. match name stable forever;
3. catch all C++ exceptions before `extern "C"` return;
4. CPU path correct before GPU optimization;
5. MFR declared only after stress test;
6. suite calls from render thread only when explicitly safe.
