# Как пользоваться cookbook

Сквозные [menu/mutation/frame routes](../03-AEGP/02-PROJECT-RENDER-AUTOMATION.md)
связывают отдельные recipes. Начать с user trigger/preflight, выбрать exact suite
source, проследить own/borrow/adopt, mutation invalidation и cleanup до report.
Здесь cookbook call shapes, там orchestration; не считать набор snippets единым plugin.

## 1. Начинать с официального sample

Adobe прямо рекомендует не собирать native plug-in с пустого проекта:

- Effect → `Skeleton`
- project creation / project graph → `Projector`
- keyframe assistant → `Easy Cheese`
- importer → `IO`
- preferences/menu → `Persisto`
- render queue → `QueueBert`
- streams → `Streamie`
- shared PICA suite → `Sweetie`
- native dockable panel → `Panelator`
- renderer → `Artie`
- frame grab / rendering → `Grabba`

Cookbook предполагает, что platform/PiPL plumbing уже взят из подходящего sample.

## 2. Оборачивать mutation в Undo Group

```cpp
AEGP_SuiteHandler suites(SPBasicSuiteP);

ERR(suites.UtilitySuite6()->AEGP_StartUndoGroup("My Operation"));
// mutating calls
ERR2(suites.UtilitySuite6()->AEGP_EndUndoGroup());
```

Для production-кода нужен guard, который вызывает `EndUndoGroup()` даже при раннем выходе.

## 3. Проверять ownership

Типичные пары:

```text
GetNew... / New...          → обычно dispose нужен
Get... (borrowed handle)    → обычно dispose не нужен
RenderAndCheckoutFrame      → CheckinFrame
GetNewStreamValue           → DisposeStreamValue
GetNewLayerStream           → DisposeStream
GetLayerEffectByIndex       → DisposeEffect
GetItemName / GetExpression → MemorySuite FreeMemHandle
```

Смотреть контракт конкретной функции, а не угадывать по имени.

## 4. Handle != стабильный ID

После add/remove/reorder:

- dynamic stream refs могут инвалидироваться;
- RQ item/output module refs могут инвалидироваться;
- project graph handles нельзя считать вечными.

Если действие меняет структуру — **re-query**.

## 5. Не мутировать project state из render worker

MFR/render callbacks и UI/project mutation — разные миры. Состояние проекта меняется из разрешённого host/UI контекста. Render path должен быть thread-safe и не использовать AEGP как скрытый источник render dependency.

## 6. Проверять доступность suite

Если функция нужна только в новом AE:

```text
Acquire newest required suite
    ↓ unavailable?
try older supported suite
    ↓
disable only unsupported feature
```

Не падать всем plug-in из-за одной новой возможности.

## 7. Использовать match name вместо display name

Display name локализуется и может меняться. Для поиска effect/property group используйте documented `match name` там, где API его предоставляет.
