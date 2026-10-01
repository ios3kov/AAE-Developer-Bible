# Native SDK taxonomy

Этот chapter классифицирует **native integration families After Effects** по тому, кто инициирует вызов, каким state владеет host и какой lifecycle получает plug-in.

Taxonomy важнее языка/IDE: неправильный тип расширения создаёт архитектурные проблемы, которые нельзя исправить красивым C++.

## Summary

| Family | Initiator | Primary state | Main use |
|---|---|---|---|
| Effect | AE render graph | effect instance/frame | pixels/audio/parameters |
| AEGP | AE hooks/commands | project/host model | native tools/automation |
| Keyframer | AEGP command flow | streams/keyframes | bulk keyframe tools |
| Native panel | AE workspace | panel/view | native dockable UI |
| AEIO | media pipeline | in/out spec | import/export |
| Artisan | composition renderer | scene/render context | 3D renderer |
| BlitHook | display pipeline | display frame | monitor/display consumer |
| PICA provider | native consumer | shared service | module-to-module API |

## Effect family

### Core image effect

Host вызывает `EffectMain` selectors. Effect получает parameters/input и производит output.

Natural owner: render graph.

### SmartFX

Не отдельный plug-in type.

Добавляет pre-render/dependency/ROI + Smart Render model.

### MFR-aware effect

Не отдельный API family.

Это Effect, чей state/render path безопасен для concurrent frames и корректно объявляет capability.

### GPU effect

Effect с GPU lifecycle/selectors/backend. GPU не меняет ownership эффекта как render-graph component.

### Custom UI effect

Effect event/UI path для effect-local controls/overlays.

Не заменяет полноценный dockable application panel.

### Arbitrary parameter effect

Effect parameter model с custom data type и callbacks для copy/flatten/compare/interpolate/print semantics.

### Audio effect

Effect API с audio selector/sample contract вместо image-world processing.

## AEGP family

AEGP — native host-tool architecture.

### General tool

Menus/commands, project/items/comps/layers, effects, streams, render queue, frames, preferences, scripting bridge.

### Keyframer

AEGP specialization around streams/keyframes and Keyframe Assistant-style workflows.

### Native panel

Workspace panel registration + platform-native UI container.

### PICA suite provider

Publishes versioned function table as native service for other components.

### Specialized registrations

AEGP registration layer also participates in AEIO/Artisan/panel integration.

## AEIO

AEIO belongs to host media lifecycle.

Responsibilities:

- verify/recognize media;
- create input/output specs;
- decode/encode frame/audio;
- options/metadata;
- aux channels;
- color interpretation.

Do not use AEIO for general filesystem helper operations.

## Artisan

Artisan is composition 3D renderer integration.

It receives render/scene context and collaborates with AE through Canvas/scene-related suites.

Do not use Artisan simply because an Effect contains 3D math or GPU code.

## Interactive Artisan

Interactive renderer registration adds viewport/UI interaction concerns on top of Artisan renderer state.

Treat as increased scope, not a checkbox.

## BlitHook

BlitHook belongs to display/preview pipeline.

Useful for external monitor/display consumers.

Not equivalent to:

- Render Queue output;
- Effect render path;
- AEIO encoder;
- Artisan renderer.

## Shared PICA service

Provider publishes a C-shaped/versioned function table; consumer acquires/releases through SPBasic/PICA.

This is a native module API boundary. Define ABI, ownership and threading explicitly.

## Legacy native APIs

Examples:

- Photoshop format/filter integrations;
- Foreign Project Format;
- ADM-era UI.

Legacy presence does not make them preferred for new products.

Keep legacy coverage so maintainers can recognize old code and migration paths.

## What is NOT a native plug-in family

### SmartFX

Effect render model.

### MFR

Effect execution model.

### GPU

Effect backend/lifecycle capability.

### Drawbot

Drawing abstraction used by UI paths.

### CEP / UXP / ExtendScript

JavaScript/extensibility layers, not C++ native module families.

## Multi-module products

Complex product may legitimately use several families:

```text
[CEP/UXP panel]
      ↓ commands
[script/native bridge]
      ↓
[AEGP service] ← PICA → [Effect]
      ↓
project model

[Effect]
      ↑ PF selectors
AE render graph
```

Do not force all responsibilities into one module.

## Selection by owner

| Need | Natural integration |
|---|---|
| pixels/audio parameters | Effect |
| project mutation | AEGP / scripting |
| bulk native keyframes | Keyframer |
| native workspace UI | Panel |
| media format | AEIO |
| composition 3D renderer | Artisan |
| display observer | BlitHook |
| native shared service | PICA |

## Selection by callback owner

Ask: who must initiate?

- render graph → Effect;
- user/menu/host command → AEGP;
- media pipeline → AEIO;
- renderer selection → Artisan;
- workspace lifecycle → Panel;
- display frame → BlitHook;
- native consumer → PICA provider.

## Selection by state lifetime

Wrong API often reveals itself through state mismatch.

Examples:

- trying to keep project model inside Effect global state;
- using panel widgets as render truth;
- using AEIO spec as generic app state;
- using BlitHook buffer as offline render source.

## Migration thinking

Architecture should isolate family-specific adapters.

```text
domain/service core
→ Effect adapter
→ AEGP adapter
→ panel/script adapter
```

This lets UI/runtime evolve without rewriting algorithms.

## Common taxonomy mistakes

- “C++ means AEGP”;
- “GPU means Artisan”;
- “dockable UI means Effect custom UI”;
- “frame callback means final render”;
- “AEIO is just file IO”;
- “Keyframer is a separate render type”;
- “PICA reference counting means service thread-safe”.

## Read order

- [Host call flows](02-HOST-CALL-FLOWS.md)
- [PICA suites](03-PICA-SUITES.md)
- [Effects](04-EFFECTS.md)
- [AEGP tools](05-AEGP-TOOLS.md)
- [Keyframers](06-KEYFRAMERS.md)
- [Native panels](07-NATIVE-PANELS.md)
- [AEIO](08-AEIO.md)
- [Artisan](09-ARTISAN.md)
- [BlitHook](10-BLITHOOK.md)
- [Legacy native](11-LEGACY-NATIVE.md)

## Evidence boundary

Current taxonomy is anchored to the supplied SDK 25.6 source-review baseline. Later-version suites/features are version-gated rather than silently replacing the baseline.
