# Extension types

Выбор extension type — главное архитектурное решение в After Effects development.

Не начинайте с языка:

> «хочу C++» или «хочу React».

Начинайте с:

> **каким state владеет feature, кто должен инициировать работу и где находится hot path?**

## Quick comparison

| Type | Главная задача | Кто инициирует | Heavy compute | Rich UI | Project access | Typical complexity |
|---|---|---|---:|---:|---:|---:|
| Effect | pixel/audio processing | AE render graph | high | limited/local | limited/indirect | high |
| AEGP | deep project/native tool | hooks/commands | medium/high | native/bridge | high | high |
| AEIO | media import/export | host media pipeline | high | options/dialogs | specialized | very high |
| Artisan | composition 3D renderer | host renderer | very high | specialized | scene/render context | very high |
| ExtendScript | project automation | user/script | low/medium | ScriptUI | high DOM access | low/medium |
| CEP | dockable HTML UI | user/UI | UI-side only | high | through bridge | medium |
| UXP | future/new Adobe panel model | user/UI | UI-side only | high | target API dependent | evolving |
| Hybrid | UI + native core | mixed | high | high | through adapters | high but scalable |

## Effect plug-in

Choose Effect when output is fundamentally a function of:

```text
input frames
+ effect parameters
+ time
+ declared dependencies
→ output frame/audio
```

### Strong sides

- realtime/render path;
- Effect Controls parameters;
- SmartFX/ROI;
- MFR;
- GPU selectors/backends;
- color/pixel formats;
- effect-local custom UI.

### Weak sides

- C/C++ ABI/lifecycle;
- host-managed memory;
- strict render dependency model;
- harder testing;
- not general project automation.

### Do not use Effect for

- global project manager;
- full dockable application UI;
- arbitrary background service;
- file format import/export.

## AEGP

Choose AEGP when product needs native access to the host/project model:

- project/items/comps/layers;
- effects/streams/keyframes;
- render queue;
- menus/hooks;
- native panel registration;
- frame/render services;
- PICA services.

### Strong sides

- deep host access;
- native performance;
- extensible suite model;
- good foundation for hybrid products.

### Weak sides

- opaque ref lifetime/invalidation;
- main-thread/host callback discipline;
- partial initialization complexity;
- more version-sensitive than scripting.

### Do not use AEGP for

- ordinary per-frame pixel effect where Effect API is natural;
- simple batch script that scripting DOM already solves.

## Keyframer

Keyframer is not a fundamentally separate host architecture; it is an AEGP-oriented specialization around streams/keyframes and user-facing keyframe workflows.

Choose it for native high-volume/property-aware keyframe tools.

## Native panel

Native Workspace Panel is useful when tight native UI integration justifies platform-specific NSView/HWND work.

Do not choose it only because «native must be faster». Browser-style panels are usually cheaper for rich cross-platform product UI.

## AEIO

Choose AEIO when product must participate in After Effects media input/output lifecycle.

Typical responsibilities:

- file recognition;
- decode/encode;
- metadata;
- frame/audio delivery;
- options;
- aux channels;
- color metadata.

### Strong sides

- real importer/exporter integration;
- host-controlled frame/audio requests;
- format-specific interpretation.

### Weak sides

- broad callback surface;
- codec/container complexity;
- sparse/random access;
- cancellation/I/O errors;
- metadata/color/audio correctness.

Do not use AEIO as a generic file helper or project automation API.

## Artisan

Choose Artisan only when product must become a **composition 3D renderer implementation**.

### Strong sides

- scene-level renderer integration;
- camera/light/3D layer context;
- interactive renderer possibilities.

### Weak sides

- huge scope;
- complex state/lifecycle;
- scene extraction/render semantics;
- heavy platform/performance burden.

Do not use Artisan because an effect contains a 3D mesh or GPU code.

## BlitHook

BlitHook is a display-pipeline observer/integration path.

Good for external monitor/display consumer scenarios.

Not for:

- deterministic offline output;
- importer/exporter;
- effect processing;
- composition 3D renderer.

## ExtendScript

Choose scripting when feature is primarily project automation.

### Strong sides

- fast iteration;
- easy deployment;
- project/layer/property/render-queue DOM;
- excellent pipeline glue;
- ScriptUI for smaller tools.

### Weak sides

- legacy JS runtime;
- slow for heavy compute;
- string/object bridge overhead;
- not a pixel/GPU API.

## ScriptUI

ScriptUI is suitable for small/medium scripting tools where HTML/CSS application UI is unnecessary.

Do not let widget callbacks become the entire domain architecture.

## CEP

Choose CEP when current product needs rich dockable HTML UI and target AE still uses CEP.

### Strong sides

- HTML/CSS/JS;
- mature ecosystem;
- rich UI;
- external/native bridge possibilities.

### Weak sides

- legacy runtime;
- two-engine bridge complexity;
- migration pressure toward UXP;
- easy to accidentally put business logic into CEF/DOM.

## UXP

UXP is Adobe's newer extensibility direction.

Because After Effects UXP support is version/time-sensitive, use the dated [UXP transition chapter](../07-PANELS/02-UXP-TRANSITION.md) rather than treating one roadmap snapshot as permanent truth.

Architect today so UI shell can change without rewriting core domain logic.

## Hybrid

Many serious products should be hybrid:

```text
Panel / Script UI
      ↓ semantic commands
Application services
      ↓
Native AEGP / Effect / helper
      ↓
After Effects
```

Typical split:

- panel: presentation, user workflow;
- script/adapter: orchestration where appropriate;
- native: heavy compute and deep host integration;
- protocol: small, versioned, testable.

## Decision by state ownership

| State | Natural owner |
|---|---|
| effect parameters/render dependencies | Effect/host parameter model |
| project graph | AE project model via AEGP/script |
| importer decoder state | AEIO InSpec + product decoder |
| renderer scene state | Artisan render/instance contexts |
| panel visual state | panel UI |
| persistent product settings | explicit product config |
| heavy compute cache | native product cache with correct invalidation |

## Decision by latency

### Per-pixel/per-frame hot path

Use native Effect/GPU/core.

### Interactive project command

AEGP or scripting depending on capability/performance.

### UI refresh

Panel/script with small snapshots.

### Long background job

Worker/helper + explicit progress/cancel; commit to AE through safe host path.

## Decision by deployment cost

From lowest to highest typical maintenance burden:

```text
simple script
→ ScriptUI tool
→ CEP panel
→ native Effect
→ AEGP/native panel/hybrid
→ AEIO/Artisan
```

This is not a value ranking. Choose the least complex architecture that satisfies the product.

## Common wrong choices

### «Сделаем всё ExtendScript»

Fails when feature is pixel/GPU heavy.

### «Сделаем всё C++»

Creates unnecessary build/deployment/UI complexity.

### «AEGP мощнее, значит Effect не нужен»

Wrong: Effect owns normal per-frame effect rendering.

### «Native panel вместо CEP потому что быстрее»

UI performance is rarely the only cost; platform-specific UI maintenance can dominate.

### «Artisan — это просто GPU renderer»

Wrong: it is composition 3D renderer integration.

### «BlitHook даст final render frames»

Wrong abstraction: display pipeline is not final render/export pipeline.

## Product architecture examples

### Color effect

Effect + optional GPU backend.

### Project organizer panel

CEP/UXP UI + script/AEGP adapter.

### Batch keyframe assistant

ExtendScript for simple version; AEGP Keyframer when native capability/performance justifies it.

### Proprietary camera format importer

AEIO + decoder core.

### External preview monitor

BlitHook/display consumer path.

### Complex commercial suite

Panel shell + versioned services + native core + Effect/AEGP adapters.

## Architecture checklist

Before committing to a type:

1. What data does the feature own?
2. Who should call whom?
3. Is there a per-frame hot path?
4. Does project state need mutation?
5. Is rich dockable UI required?
6. Does operation need media import/export lifecycle?
7. Does feature replace composition 3D renderer?
8. What must survive UI reload/project reopen?
9. What platform/build burden is acceptable?
10. Can simpler scripting solve it?

## Related chapters

- [Decision tree](00-DECISION-TREE.md)
- [Environment matrix](02-ENVIRONMENT-MATRIX.md)
- [Native integrations taxonomy](../14-NATIVE-INTEGRATIONS/README.md)
- [Communication architecture](../01-ARCHITECTURE/07-COMMUNICATION-ARCHITECTURE.md)
- [Panels](../07-PANELS/README.md)

## Evidence boundary

Native category definitions are tied to the SDK/source-reviewed taxonomy. CEP/UXP platform status is dated and maintained separately because Adobe's extensibility roadmap changes over time.
