# Host call flows

Главная идея native AE development: **After Effects владеет lifecycle и вызывает plug-in через определённые entry points/callbacks**.

Большинство архитектурных ошибок начинается, когда plug-in мысленно превращают в standalone приложение с собственным main loop.

## Effect plug-in

```text
AE scans module / PiPL
→ registration entry point
→ EffectMain(GLOBAL_SETUP)
→ EffectMain(PARAM_SETUP)
→ instance / render / UI selectors
→ GLOBAL_SETDOWN
```

### Global lifecycle

`GLOBAL_SETUP`/`GLOBAL_SETDOWN` — host-level lifetime. Здесь объявляются capabilities и global data, но не frame-specific mutable state.

### Parameter lifecycle

`PARAM_SETUP` определяет parameter model. Persistent parameter identity должна быть deliberate: project compatibility зависит не только от UI index.

### Instance sequence

В зависимости от effect используются `SEQUENCE_SETUP`, `RESETUP`, `FLATTEN`, `SETDOWN`.

Sequence data — host-managed lifecycle, а не arbitrary static global.

### Classic render

```text
FRAME_SETUP
→ RENDER
→ FRAME_SETDOWN
```

### SmartFX

```text
SMART_PRE_RENDER
→ checkout dependencies / calculate result rect
→ SMART_RENDER
→ checkout pixels / render / checkin
```

Pre-render и render имеют разные ownership/lifetime contracts.

### GPU

```text
GPU_DEVICE_SETUP
→ SMART_PRE_RENDER
→ SMART_RENDER_GPU
→ GPU_DEVICE_SETDOWN
```

Global GPU capability не означает, что каждый frame будет GPU-rendered.

### UI

UI selectors вроде `EVENT`, `USER_CHANGED_PARAM`, `UPDATE_PARAMS_UI` не должны становиться hidden source of render truth.

## Effect anti-pattern

Плохо:

```text
background thread loops forever
→ polls AE
→ modifies global effect state
→ render reads it
```

Effect должен работать в host-owned selector lifecycle.

## AEGP flow

```text
AE loads AEGP
→ EntryPointFunc(...)
→ register hooks / commands / services
→ EntryPoint returns
→ AE invokes callbacks later
→ callback acquires/uses suites
→ query/mutate host
```

Entry point — прежде всего registration phase, не application loop.

Сквозной source/design маршрут и таблица partial registration находятся в
[hooks lifecycle](../03-AEGP/01-HOOKS-SUITES.md#12-сквозная-команда-и-частичная-регистрация-сверка-2026-10-07).
MenuTool реализует command/update/death и ping; idle/worker/mutation в этой
композиции — отдельно описанный design, не его скрытые функции.

### Command flow

```text
user action
→ AE command dispatch
→ CommandHook
→ validate current state
→ optional Undo group
→ mutate/query
→ cleanup
→ return A_Err
```

### Update-menu flow

UpdateMenuHook должен быстро обновлять enable/check state. Не сканируйте огромный проект каждый раз при открытии меню.

### Idle flow

Idle hook — возможность выполнить bounded work на host-safe path. Это не гарантия отдельного background worker.

### Death/shutdown

Освобождайте product-owned global resources. Не вызывайте host APIs после их documented lifetime.

## Keyframer flow

```text
menu/UI command
→ resolve selected stream/property
→ validate keyframe capability
→ undo
→ batch keyframe API
→ cleanup
```

См. [Keyframers](06-KEYFRAMERS.md).

## Native panel flow

```text
AE loads/registers panel provider
→ user opens Window-menu panel
→ create callback
→ host owns workspace/docking lifecycle
→ panel events/commands
→ visibility/destroy lifecycle
```

Native panel — не Effect custom UI. View lifetime не должен становиться project-model lifetime.

## AEIO input flow

```text
AE launch
→ AEGP_RegisterIO
→ AE receives function block
→ VerifyFileImportable
→ InitInSpecFromFile
→ metadata/frame/audio callbacks
→ input-spec disposal
```

AEIO importer принадлежит media lifecycle, а не general project automation.

## AEIO output flow

```text
create output spec
→ configure
→ start/add frames/audio
→ finalize
→ dispose output spec
```

Partial output/failure cleanup должен быть explicit.

## Artisan flow

```text
AE launch
→ AEGP_RegisterArtisan
→ renderer selected for comp
→ host creates renderer context
→ frame/render callbacks
→ teardown
```

Artisan заменяет composition 3D renderer path. Это не «GPU API для effects».

## BlitHook flow

```text
Composition panel has display frame
→ display/blit callback
→ consumer receives/copies/processes frame
```

Display-time frame stream не равен Render Queue/Effect render pipeline.

## Shared PICA suite flow

Provider публикует named/versioned function table; consumer делает `AcquireSuite`, использует сервис и делает `ReleaseSuite`.

Suite reference counting не делает service methods thread-safe автоматически.

## Effect ↔ AEGP generic call

```text
AEGP owns effect instance ref
→ AEGP_EffectCallGeneric
→ PF_Cmd_COMPLETELY_GENERAL
→ effect validates message version/size
→ handles command
→ return
```

Подходит для небольших control messages, не для high-volume pixel data.

## Script flow

```text
ExtendScript
→ scripting DOM
→ project/UI mutation
```

Script runtime и native SDK имеют разные object/lifetime models. Raw native handles в script не передаются.

## CEP flow

```text
panel JS
→ evalScript / event
→ ExtendScript dispatcher
→ AE scripting DOM
→ structured result
```

Panel DOM не должен быть authoritative project state.

## Hybrid flow

```text
UI panel
→ semantic command
→ orchestration layer
→ native service/effect/AEGP
→ After Effects
```

Heavy data остаётся native; panel получает control/status.

## Threading boundary

Callback origin не означает, что любые host calls разрешены с любого thread.

Разделяйте worker-safe pure compute и host-facing query/mutation.

## Ownership boundary

Для каждой стрелки flow diagram задайте: borrowed? caller-owned? host-owned? matching dispose/checkin/release? valid until when?

Если диаграмма не может ответить — architecture incomplete.

## Failure boundary

Определите initialization failure, callback failure, partial resource creation, cleanup failure, host-state change и shutdown.

Return path должен сохранять first meaningful error и всё равно выполнять safe cleanup.

## Choosing the flow

| Product need | Primary flow |
|---|---|
| render pixels/audio effect | Effect |
| project automation/native tool | AEGP |
| bulk keyframes | Keyframer |
| native dockable UI | Panel |
| media import/export | AEIO |
| replace 3D renderer | Artisan |
| observe composition display | BlitHook |
| share native service | PICA |
| panel automation | CEP/Script |
| mixed UI + native compute | Hybrid |

## Related chapters

- [Native taxonomy](01-TAXONOMY.md)
- [Effects](04-EFFECTS.md)
- [AEGP tools](05-AEGP-TOOLS.md)
- [Communication architecture](../01-ARCHITECTURE/07-COMMUNICATION-ARCHITECTURE.md)
- [Communication section](../15-COMMUNICATION/README.md)
- [Lifetime/threading cookbook](../17-NATIVE-SUITE-COOKBOOK/14-LIFETIME-THREADING.md)

## Evidence boundary

Flows — architecture summaries derived from documented SDK models/source-reviewed families. Exact selector/function availability остаётся version-sensitive.
