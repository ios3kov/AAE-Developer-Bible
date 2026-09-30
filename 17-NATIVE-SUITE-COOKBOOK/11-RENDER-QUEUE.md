# Render Queue recipes

**Suites:** `AEGP_RenderQueueSuite1`, `AEGP_RQItemSuite4`, `AEGP_OutputModuleSuite4`  
**Confidence:** SDK-verified + `QueueBert` sample-derived.

## Добавить comp в queue

```cpp
ERR(suites.RenderQueueSuite1()->AEGP_AddCompToRenderQueue(
    compH,
    output_path_utf8_or_host_expected_path));
```

После add **старые Render Queue references могут стать invalid**. Re-query queue.

---

## Получить queue items

```text
GetNumRQItems
→ GetRQItemByIndex / GetNextRQItem
→ GetCompFromRQItem
→ GetRenderState / SetRenderState
```

Используйте именно indexing semantics вашей версии/sample; не переносите undocumented community assumptions между версиями.

---

## Output modules

```text
RQItem
→ GetNumOutputModulesForRQItem
→ GetOutputModuleByIndex
→ SetOutputFilePath
→ configure enabled outputs / channels / crop / stretch / sound
```

После add/remove output module re-query references/indices.

---

## Установить output path

```cpp
ERR(suites.OutputModuleSuite4()->AEGP_SetOutputFilePath(
    rq_item_refH,
    output_module_refH,
    utf16_pathZ));
```

`AEGP_SetOutputFilePath` принимает NULL-terminated UTF-16 path (`A_UTF16Char*`). `AEGP_GetOutputFilePath` возвращает `AEGP_MemHandle`, который надо освободить через Memory Suite.

---

## Запустить queue

Сначала item должен иметь допустимый output path и быть включён для рендера:

```cpp
ERR(suites.RQItemSuite4()->AEGP_SetRenderState(
    rq_itemH,
    TRUE));

ERR(suites.RenderQueueSuite1()->AEGP_SetRenderQueueState(
    AEGP_RenderQueueState_RENDERING));
```

`AEGP_SetRenderState` принимает `A_Boolean`, а не enum статуса render item.

Host может передать управление render pipeline и UI; команда не должна ожидать «обычный синхронный цикл» после старта.

---

## Invalidation rule

Официальный SDK guide отдельно предупреждает:

- `AddCompToRenderQueue` или пользовательский add/remove инвалидирует RQ item references;
- add/remove output module инвалидирует output-module references для item.

Production code:

```text
mutation
→ drop old refs
→ query count again
→ fetch fresh refs
```

---

## Для сложных preset/template операций

Некоторые render settings/output module template actions проще/надёжнее делаются через scripting (`applyTemplate`) поверх native controller. Hybrid допустим, если:
- boundary документирован;
- script failure возвращается как structured error;
- native core не зависит от UI language strings.
