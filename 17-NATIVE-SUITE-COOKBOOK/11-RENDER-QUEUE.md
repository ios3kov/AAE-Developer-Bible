# Render Queue recipes

**Primary Bible baseline:** Adobe After Effects SDK **25.6 build 61**.

**Current SDK families:** `AEGP_RenderQueueSuite1`, `AEGP_RQItemSuite4`, `AEGP_OutputModuleSuite4`.

The existing Bible C++ recipe intentionally uses the older-compatible `RQItemSuite3` subset; both Suite3 and current Suite4 use **`AEGP_RenderItemStatusType`**, not `A_Boolean`, for render-item state.

## Queue state vs item state

These are different state machines.

Queue state:

- STOPPED;
- PAUSED;
- RENDERING.

Item state includes values such as:

- NEEDS_OUTPUT;
- UNQUEUED;
- QUEUED;
- USER_STOPPED;
- ERR_STOPPED;
- DONE.

Do not pass queue-state constants to item APIs or vice versa.

## Add composition

```cpp
ERR(suites.RenderQueueSuite1()->AEGP_AddCompToRenderQueue(
    compH,
    initial_path_utf8));
```

Important: changing queue composition/order invalidates existing `AEGP_RQItemRefH` references.

After add/remove/reorder:

```text
drop old RQ refs
→ query count again
→ fetch fresh refs
```

## Find queue items

Current RQItemSuite4 supports item enumeration/state access. A compatibility source recipe may use Suite3 when it needs only older members.

Do not cast Suite3 ↔ Suite4.

## Output modules

Pattern:

```text
RQ item
→ GetNumOutputModulesForRQItem
→ GetOutputModuleByIndex
→ configure path/channels/crop/stretch/etc.
```

Adding/removing/reordering output modules invalidates output-module refs according to the relevant contract.

Re-query after structural changes.

## Output path

`AEGP_SetOutputFilePath` uses UTF-16 path in the current reviewed output-module contract.

`AEGP_GetOutputFilePath` returns Memory Suite handle requiring the matching free path.

Do not retain pointer after unlock/free.

## Queue must be stopped for item state edit

Current RQItemSuite4 header says `AEGP_SetRenderState` errors if Render Queue state is not STOPPED.

Do not silently stop user's render merely because your tool wants to edit an item.

Better:

```text
queue not STOPPED
→ report command unavailable/busy
```

unless product explicitly owns queue operation and user asked for stop/reconfigure.

## Set item to QUEUED correctly

Correct semantic call:

```cpp
ERR(rq_items->AEGP_SetRenderState(
    rq_itemH,
    AEGP_RenderItemStatus_QUEUED));
```

Then read back state when command semantics depend on it.

## Historical TRUE bug

An earlier Bible recipe and Adobe QueueBert sample used:

```cpp
AEGP_SetRenderState(rq_itemH, TRUE)
```

This is wrong for the reviewed enum contract.

In the SDK baseline:

```text
TRUE == 1
AEGP_RenderItemStatus_UNQUEUED == 1
AEGP_RenderItemStatus_QUEUED == 2
```

So `TRUE` requests UNQUEUED, not QUEUED.

The Bible C++ recipe was corrected to named `AEGP_RenderItemStatus_QUEUED` + readback.

## Current Suite4 vs recipe Suite3

Why chapter says Suite4 while code uses Suite3:

- SDK 25.6 current header exposes `AEGP_RQItemSuite4`;
- existing source recipe uses members already present in Suite3;
- Suite3 also has enum-typed SetRenderState;
- recipe remains a compatibility-shaped source example, not current-suite authority.

New product code should choose suite generation deliberately from target host/support policy.

## Output module is more than filename

Output config may include:

- video/audio enabled;
- RGB/RGBA/alpha;
- crop;
- stretch;
- post-render action;
- format/template-specific settings.

File extension alone does not define output module format.

## Post-render actions

Output module may perform project-side actions such as import/replace/proxy workflows.

Treat these as project mutations, not harmless file settings.

## Prepare vs start queue

Separate two commands:

### Prepare our item

```text
validate comp/path
→ add item
→ reacquire refs
→ configure output
→ set QUEUED
→ read back
```

### Start global queue

```text
inspect queue/user intent
→ ensure other queued items are acceptable
→ set queue state RENDERING
```

Starting queue is global. It can render items your tool did not create.

Do not make it an implicit side effect of preview/export preparation.

## Invalidation

Two separate invalidation layers:

| Mutation | Invalidated |
|---|---|
| queue item add/remove/reorder | RQ item refs |
| output module add/remove/reorder | output-module refs for item |

Stored numeric index is also not durable identity after reorder.

## Partial failure

Source limitation: [RenderQueueRecipes.cpp](code/RenderQueueRecipes.cpp) is only
add→fresh last-item ref→first output path→QUEUED→state readback. Caller supplies
STOPPED preflight, allowed path/format, Undo/compensation and protection of existing
queue items. Source does not verify path readback or remove its added item after
failure. Do not call global RENDERING as an implicit continuation of this helper.

Example:

```text
AddCompToRenderQueue succeeds
→ output path configuration fails
```

The queue may already contain a new item.

Returning error does not mean “nothing changed”.

Define product policy:

- leave item and report;
- rollback only the item you created;
- mark unqueued/needs output;
- ask user.

Do not delete unrelated queue items during cleanup.

## Unicode/path conversion

`AddCompToRenderQueue` and output-path APIs do not necessarily use identical string types.

Use deliberate UTF conversion. Do not pointer-cast UTF-8/UTF-16.

## Hybrid scripting

Some template/preset operations may be more practical through scripting (`applyTemplate`) controlled by native/panel orchestration.

Hybrid is acceptable when:

- command boundary documented;
- script errors structured;
- native logic does not depend on localized UI strings.

### Наблюдать render job через Render Queue Monitor

**Public guide, 2026-10-08: DOCUMENTED / RUNTIME-NOT-CLAIMED.**

`AEGP_RenderQueueMonitorSuite1` регистрирует listener с refcon и имеет отдельный
`AEGP_DeregisterListener`. События несут job/item/frame IDs; окончание item
сообщает отдельный finished status. Выходные UTF-16 handles информационных getters
требуют `AEGP_FreeMemHandle`. [Источник](https://github.com/docsforadobe/after-effects-plugin-guide/blob/6d9b285d9755d1fbf8ead7680ba49de24f94b547/docs/aegps/aegp-suites.md#L3813-L3911)

**Рекомендуемый workflow:** создать собственный listener state; зарегистрировать
callback table; в callback связать событие с текущими IDs, получить нужные поля,
скопировать текст в собственную запись и освободить принадлежащие getter ресурсы.
Передавать дальше уже скопированные записи, сохраняя callbacks короткими.

Для журнала различать начало job, начало/обновление/окончание item и сообщения.
`SUCCEEDED`, `ABORTED`, `ERRED` и `UNKNOWN` нельзя сливать в один флаг «готово».
Идентификатор события не заменяет свежий `RQItemRefH`, а завершение job не отменяет
политику частичных результатов отдельных items.

При отключении инструмента прекратить приём новых действий, снять listener и
завершить зависящие от него операции до уничтожения refcon. Страница не задаёт
универсальную гарантию quiescence после deregistration. Также нельзя переносить
правило освобождения **выходного** handle getter на входной `logbuf` callback без
его отдельного контракта. Эти границы сохраняются явными; управление очередью
не становится частью diagnostic callback.

## Product workflow

1. Verify queue is editable.
2. Validate comp/path.
3. Add own item.
4. Drop stale refs.
5. Re-query item/output module.
6. Configure complete output contract.
7. Set named QUEUED enum.
8. Read back state/config if required.
9. Start global queue only on explicit user intent.

## Related chapters

- [Project/render automation](../03-AEGP/02-PROJECT-RENDER-AUTOMATION.md)
- [Rendered frames](10-RENDER-FRAMES.md)
- [Memory/undo](12-MEMORY-UNDO-PERSISTENCE.md)
- [SDK 25.6 project/render review](../18-SDK-HEADER-TOOLS/09-AEGP-PROJECT-RENDER-SDK25.6.md)
- [Corrected C++ recipe](code/RenderQueueRecipes.cpp)

## Evidence boundary

Suite4 baseline and enum/invalidation rules are source-reviewed against SDK 25.6. The corrected source example does not claim a particular queue runtime run.
