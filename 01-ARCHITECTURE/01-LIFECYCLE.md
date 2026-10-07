# Native plug-in lifecycle

After Effects native development начинается не с классов и не с UI. Начинайте с вопроса:

> **кто вызывает кого, сколько живёт state и кто его освобождает?**

Host владеет основным lifecycle. Plug-in предоставляет entry points/callbacks и отвечает только в разрешённые фазы.

## Effect mental model

```text
AE loads/reads PiPL
→ registration
→ GLOBAL_SETUP
→ PARAM_SETUP
→ instance / render / UI selectors
→ GLOBAL_SETDOWN
```

Не существует одного «Effect object lifetime». Есть несколько scopes.

## Global scope

Живёт на уровне загруженного effect module.

Подходит для:

- immutable tables;
- process-wide product resources;
- capability data;
- carefully owned shared services.

Не подходит для:

- current frame state;
- current instance parameters;
- mutable render scratch shared without synchronization.

## Parameter setup scope

`PARAM_SETUP` определяет public parameter model.

Параметры имеют как минимум два вида identity:

- UI/index position;
- persistent parameter ID/match semantics.

Не путайте их при evolution plug-in version.

## Sequence/instance scope

Sequence lifecycle относится к конкретному effect instance.

Типичные selectors:

- `SEQUENCE_SETUP`;
- `SEQUENCE_RESETUP`;
- `SEQUENCE_FLATTEN`;
- `SEQUENCE_SETDOWN`.

State должен быть:

- versioned, если сохраняется;
- relocatable/serializable, если host требует flatten;
- thread-safe/read-only where MFR requires it;
- independent between effect instances.

## Frame/render scope

### Recovery сохраняемого Effect state

```text
flat bytes → size/schema validation → migrate known schema
          → allocate live state → initialize transient cache → publish
          ↘ failure: clean partial allocation; retain primary error
```

RESETUP не предполагает существование прежнего живого объекта. Copy/duplicate
не переносит mutex, decoder pointer или callback-local world. Legacy FLATTEN и
GET_FLATTENED_SEQUENCE_DATA имеют разные ownership transitions; смотреть точный
selector, а не общий метод «save». Unknown future schema не превращать в defaults
без явной product policy. Parameter Reset и восстановление sequence — разные
операции. Практическая [таблица хранилищ и migration](../02-EFFECT-PLUGINS/02-PARAMETERS-UI.md#13-сохраняемое-состояние-и-arbitrary-data)
согласована с source codec; render использует валидированный snapshot и не зависит
от того, открывалась ли UI-панель.

Classic render:

```text
FRAME_SETUP
→ RENDER
→ FRAME_SETDOWN
```

SmartFX:

```text
SMART_PRE_RENDER
→ SMART_RENDER
```

Frame-local scratch не должен переживать frame lifecycle без явного ownership transfer.

## GPU device scope

GPU effect добавляет per-device lifetime:

```text
GPU_DEVICE_SETUP
→ many GPU renders
→ GPU_DEVICE_SETDOWN
```

Per-device state и per-frame state — разные уровни.

## UI/event scope

`EVENT`, `USER_CHANGED_PARAM`, `UPDATE_PARAMS_UI` и related callbacks принадлежат UI/event path.

UI callback не должен становиться скрытым render dependency.

## AEGP mental model

AEGP lifecycle:

```text
EntryPointFunc
→ register hooks/commands/services
→ return
→ AE invokes callbacks later
→ callbacks acquire/use suites
→ death/shutdown cleanup
```

Главная ошибка — считать `EntryPointFunc` аналогом `main()`.

## AEGP callback state

Разделяйте:

- plug-in-global refcon;
- per-command temporary state;
- per-panel refcon;
- host refs/handles;
- external/helper process state.

Opaque host refs нельзя автоматически хранить между callbacks.

## AEIO lifecycle

Importer/exporter state принадлежит InSpec/OutSpec/media lifecycle:

```text
register IO
→ create/init spec
→ metadata/frame/audio callbacks
→ flatten/options where applicable
→ dispose spec/options
```

File decoder object не должен жить дольше соответствующего spec без собственного ownership contract.

## Artisan lifecycle

Artisan имеет уровни:

- global renderer state;
- instance/comp state;
- render/frame state;
- temporary textures/worlds/receipts.

Нельзя объединять их в один global singleton.

## Native panel lifecycle

Panel имеет как минимум:

```text
plug-in global
→ panel registration
→ panel instance/view
→ panel callbacks
→ close/destroy
→ plug-in shutdown
```

View lifetime не равен project lifetime.

## Script/panel lifecycle

CEP/ScriptUI/ExtendScript объекты живут по другим правилам, чем native handles.

Panel reload, document navigation или script completion могут уничтожить JS state, пока project state остаётся.

Поэтому panel DOM не authoritative project store.

## State scope checklist

Для каждого state object запишите:

| Question | Why |
|---|---|
| кто создаёт? | ownership start |
| кто уничтожает? | cleanup |
| scope? | global/instance/frame/view/request |
| serialized? | project/reload compatibility |
| mutable concurrently? | MFR/threading |
| host-owned? | no accidental free |
| invalidation trigger? | stale refs |

Если этого нет в design doc, lifecycle bug уже заложен.

## Host boundary

Entry points/callbacks — ABI boundary.

На boundary:

- не выпускать C++ exceptions наружу;
- не возвращать dangling pointers;
- переводить errors в host-compatible result;
- cleanup выполнять даже при partial failure;
- не держать invalid host refs;
- логировать enough identity for diagnostics.

## Error before cleanup

Правило:

```text
primary operation error
→ cleanup all owned resources
→ preserve/report primary error
→ record cleanup failure separately if useful
```

Cleanup error не должен случайно скрывать реальную причину failure.

## Partial initialization

Init может упасть после того, как часть state уже создана.

Планируйте:

- какие resources уже owned;
- какие hooks уже registered;
- какой cleanup ещё legal;
- можно ли оставить feature disabled instead of failing entire module.

## Versioned suites

Suite acquisition — capability check.

```text
AcquireSuite(name, version)
  ├─ success → use
  └─ unavailable → fallback / disable feature / explicit error
→ ReleaseSuite
```

Header compilation не означает runtime availability.

## What not to cache blindly

- stream/effect/RQ refs without documented lifetime;
- frame-local worlds;
- callback-local pointers;
- temporary locked-memory pointers;
- platform view pointers beyond view lifetime;
- request-specific objects across async generations.

## Invalidation

Host structural mutation может инвалидировать refs/indices.

Типичный safe pattern:

```text
store stable product identity
→ resolve host ref late
→ validate
→ use
→ dispose/drop
```

## Threading

State lifetime и thread safety — разные свойства.

Объект может жить global lifetime и всё равно быть unsafe for concurrent access.

Для MFR/GPU/worker architecture отдельно определите:

- immutable shared;
- locked shared;
- per-thread;
- per-frame;
- per-device.

## Unload/shutdown

Shutdown должен:

1. stop accepting new work;
2. signal workers/helpers;
3. complete/drop queued product work deliberately;
4. release product-owned resources;
5. avoid host calls after host contract expired.

Не делайте unbounded wait inside host shutdown.

## Lifecycle anti-patterns

- one giant global singleton for all state;
- raw host refs in long-lived UI model;
- lazy init without synchronization;
- cleanup only on success path;
- assuming host always calls selectors in the one order seen during testing;
- treating UI close as product/model destruction;
- using render callback to initialize unrelated services.

## Design workflow

Before implementation:

1. draw lifecycle diagram;
2. list state scopes;
3. list ownership pairs;
4. list invalidation events;
5. list thread access;
6. list serialization needs;
7. list partial-failure cleanup;
8. only then write code.

## Related chapters

- [Memory/threading/errors](02-MEMORY-THREADING-ERRORS.md)
- [PiPL/loading](03-PIPL-AND-LOADING.md)
- [Communication architecture](07-COMMUNICATION-ARCHITECTURE.md)
- [Host call flows](../14-NATIVE-INTEGRATIONS/02-HOST-CALL-FLOWS.md)
- [Lifetime/threading cookbook](../17-NATIVE-SUITE-COOKBOOK/14-LIFETIME-THREADING.md)
- [Host call boundary](../19-NATIVE-CODE-FOUNDATION/04-HOST-CALL-BOUNDARY.md)

## Evidence boundary

Lifecycle models above summarize documented/source-reviewed API families. Exact selector/function details remain version-specific to the relevant SDK/source-review chapter.
