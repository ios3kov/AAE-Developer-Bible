# AEGP tools — native automation and deep AE integration

AEGP — основной native C++ путь для инструментов, работающих с **After Effects project/host model**, а не только с пикселями одного Effect instance.

Думайте об AEGP как о сочетании registered callbacks + versioned host suites, а не как о втором scripting DOM.

## Когда AEGP подходит

- native project/item/layer access;
- menu commands/hooks;
- render queue integration;
- streams/keyframes;
- footage operations;
- rendered-frame services;
- native panels;
- shared PICA services;
- AEIO/Artisan registration;
- native performance around project operations.

## Когда scripting проще

ExtendScript лучше, если операция небольшая/редкая, нужный API уже удобно доступен в DOM и deployment simplicity важнее native throughput.

Hybrid часто оптимален:

```text
panel/script UI
→ semantic command
→ native AEGP service
→ AE
```

## Lifecycle

```text
EntryPointFunc
→ obtain plugin context/ID
→ register hooks/commands/services
→ return
→ AE invokes callbacks later
→ callbacks use suites
→ shutdown cleanup
```

Entry point — registration phase, не main loop.

## Capability map

### Project/items

Proj + Item suites: project traversal, root, items, project-level state.

### Compositions/layers

Comp + Layer suites: composition creation/access, layer enumeration и identity.

### Effects

Effect suite: installed effects, apply/remove instances, match names, generic-call bridge.

### Streams/properties

Stream + DynamicStream: properties, expressions, effect parameters и property hierarchy.

### Keyframes

Keyframe suite: bulk keyframe operations и interpolation/ease metadata.

### Masks/text/markers/footage

Dedicated suites + Stream/Memory ownership rules.

### Render queue

RenderQueue + RQItem + OutputModule. Queue-wide state и item state — разные вещи.

### Frame rendering

Render/RenderOptions/World paths дают rendered-frame workflow с receipt/checkin ownership.

### Utility

Reporting, undo, script execution и host utilities.

## Commands

Typical menu-tool setup:

```text
GetUniqueCommand
→ InsertMenuCommand
→ RegisterCommandHook
→ RegisterUpdateMenuHook
```

CommandHook делает actual operation. UpdateMenuHook — только cheap UI state.

## Idle hook

Хорошо: consume queued lightweight commands, bounded maintenance, host-safe commit.

Плохо: full project scan every idle, heavy network IO, unbounded work, render logic.

## Death hook

Освобождайте product-owned global resources. Shutdown order может ограничивать доступность host services.

## Undo

Для user-visible mutation:

```text
StartUndoGroup
→ changes
→ EndUndoGroup
```

Undo не равен transaction rollback. Mid-operation failure может оставить partial state, поэтому validate before mutate.

## Handles and refs

Classify each ref as borrowed/newly-owned/host-managed/disposable/checkin-required/stable ID vs ephemeral ref.

Не храните `AEGP_StreamRefH`/effect refs в long-lived app state без documented guarantee.

Лучше хранить stable product identity и re-resolve host ref at execution time.

## Strings

APIs могут возвращать UTF-8, UTF-16 или MemHandle-backed strings. Encoding и ownership — отдельные контракты.

## Time domains

Документируйте, где comp/layer/stream/render time. Не делайте helper `GetTime()` без domain.

## Threading

AEGP — не general thread-safe API.

```text
worker: pure compute / IO / parsing
host callback: re-resolve handles + query/mutate AE
```

Opaque AE handles не должны путешествовать на worker только потому, что computation background.

## State freshness

Project state может измениться между panel request, background compute и commit.

Используйте generation/revision, stable IDs и revalidation.

## ExecuteScript

`AEGP_ExecuteScript` полезен для scripting-only capability, но не должен превращать native product в генератор arbitrary script strings на каждый action.

## Render Queue tools

Разделяйте queue-wide state, item state, output module, output path и execution. Structural changes могут инвалидировать refs.

## Rendered frames

```text
configure render options
→ render/checkout receipt
→ access borrowed world
→ consume/copy
→ checkin receipt
```

Borrowed world нельзя сохранять beyond receipt lifetime.

## Native service pattern

Если нескольким компонентам нужен один service — versioned PICA suite предпочтительнее raw global symbol lookup как public module API.

## Native panel pattern

```text
panel view
↕ controller/model
↕ AEGP host adapter
```

UI widget lifetime не должен быть project model lifetime.

## Error strategy

Обогащайте host errors контекстом. Вместо `error 4` полезнее `rename failed: layer no longer exists; host error 4`.

## Partial initialization

Registration может упасть после успешной регистрации части hooks. Планируйте, что остаётся alive, что disable-ится и какой cleanup legal.

Не предполагайте, что failed EntryPoint автоматически unregister-ит всё.

Практическая [таблица initializer → update/command/idle → shutdown](../03-AEGP/01-HOOKS-SUITES.md#12-сквозная-команда-и-частичная-регистрация-сверка-2026-10-07)
различает локальное владение до регистрации и resident/degraded state после неё.
MenuTool не разрешает цели и не делает mutation: для настоящей операции подключите
[cookbook operation route](../17-NATIVE-SUITE-COOKBOOK/15-RECIPE-INDEX.md), повторную
проверку целей, successful-Start-only Undo и отдельный partial-result report.

## Performance

Типичные traps: repeated full-project traversal, one-key-per-transaction, repeated string conversion, script bridge per tiny operation.

Batch semantic work, когда host API предлагает batch/transaction model.

## Product architecture examples

### Layer batch tool

```text
UI command
→ normalize LayerIDs
→ host callback
→ revalidate
→ undo
→ mutate
→ fresh result
```

### Keyframe generator

```text
worker computes times/values
→ host callback resolves stream
→ batch keyframe API
→ cleanup
```

### Render queue manager

```text
read queue snapshot
→ UI edits desired config
→ command applies current refs
→ re-query after structural mutation
```

## Anti-patterns

- cache opaque refs globally;
- call host from arbitrary thread;
- use menu/idle hook as application loop;
- mix UI state with project source of truth;
- ignore cleanup;
- copy obsolete sample suite generation as current API.

## Production workflow

1. Choose minimum suites.
2. Pin target SDK baseline.
3. Define stable product-level model.
4. Register only needed hooks.
5. Resolve refs late.
6. Validate before mutate.
7. Group undo appropriately.
8. Cleanup owned resources.
9. Report contextual errors.
10. Gate version/platform differences explicitly.

## Related chapters

- [AEGP hooks/suites](../03-AEGP/01-HOOKS-SUITES.md)
- [Project/render automation](../03-AEGP/02-PROJECT-RENDER-AUTOMATION.md)
- [Native suite cookbook](../17-NATIVE-SUITE-COOKBOOK/README.md)
- [Communication architecture](../01-ARCHITECTURE/07-COMMUNICATION-ARCHITECTURE.md)
- [Keyframers](06-KEYFRAMERS.md)
- [Native panels](07-NATIVE-PANELS.md)

## Evidence boundary

Suite generations/key ownership for current baseline are source-reviewed against SDK 25.6 records. Эта глава описывает architecture, а не runtime claim конкретного binary.
