# ExtendScript scripting

After Effects scripting API отображает project/UI hierarchy в объектную модель:

```text
app
→ project
→ items/compositions
→ layers
→ properties/keyframes
→ render queue / import options
```

Это лучший слой для **project automation и artist tools**, когда native render path не нужен.

## Best use cases

- batch project construction;
- repetitive layer/property operations;
- render queue setup;
- pipeline glue;
- asset relinking/import;
- one-click artist tools;
- project cleanup;
- prototype logic before native implementation.

## Not for

- heavy per-pixel processing;
- realtime frame algorithms;
- low-level GPU work;
- long-lived binary services;
- assumptions about modern browser/Node runtime.

## Script vs expression

Script:

- запускается как command/tool;
- может менять project structure;
- работает через scripting DOM.

Expression:

- вычисляет property value;
- живёт в evaluation context;
- не является general project automation API.

См. [Expressions vs scripts](03-EXPRESSIONS-VS-SCRIPTS.md).

## Object model discipline

Не храните произвольную UI selection как eternal identity.

Перед operation валидируйте:

- `app.project` exists;
- active item type;
- layer still exists;
- property/effect present;
- selection not stale;
- file path still valid.

## Match names vs display names

Localized display name может меняться.

Для effects/properties там, где API даёт stable match name, используйте match name для program logic, а display name — для UI.

## Undo

Для user-visible batch mutation:

```javascript
app.beginUndoGroup("My Tool");
try {
    // project mutations
} finally {
    app.endUndoGroup();
}
```

Undo group не исправляет partial failure автоматически; validate inputs before destructive work.

## User state

Если script временно меняет:

- active item;
- selection;
- current time;
- viewer state;
- render settings;

решите явно, нужно ли восстановить состояние.

Не оставляйте UI в неожиданном состоянии только потому, что script закончил задачу.

## Long operations

Для длинной batch operation:

- оцените количество work;
- давайте progress только если он полезен;
- делайте cancel path;
- проверяйте cancel between bounded units;
- не открывайте тысячи modal alerts;
- логируйте failed items отдельно.

## File paths

Планируйте:

- Unicode;
- network/removable paths;
- missing files;
- permission denied;
- path normalization;
- user cancel from file dialogs.

Не склеивайте platform paths вручную, если scripting API предоставляет File/Folder abstractions.

## Error model

Разделяйте:

- invalid user context;
- unsupported object type;
- missing asset/effect/font;
- filesystem error;
- host operation error;
- script bug.

Пользователю нужен contextual message, а не raw exception dump.

## Idempotence

Pipeline scripts выигрывают от idempotent design.

Example:

```text
ensure folder exists
ensure comp exists
ensure named control exists
update only if needed
```

Вместо «каждый запуск добавляет ещё один объект».

## Performance

Типичные traps:

- full project scan внутри inner loop;
- repeated property lookup by string;
- UI refresh-heavy operations;
- one tiny host mutation per iteration.

Сначала уменьшите количество host/DOM calls, потом оптимизируйте JS.

## ScriptUI

ScriptUI подходит для небольших native-looking tools/dialogs/panels.

Не переносите весь domain model в widget callbacks.

Схема:

```text
UI
→ command/controller
→ scripting service
→ AE DOM
```

См. [ScriptUI](02-SCRIPTUI.md).

## CEP bridge

Если UI — CEP, централизуйте `evalScript()` через dispatcher/adapter.

Не разбрасывайте arbitrary script strings по React/UI components.

Передавайте small control payloads, а не huge data.

## Native bridge

Если native code делает heavy compute, script может быть orchestration layer, но raw pointers/handles между JS и C++ не являются контрактом.

Use versioned commands/IDs.

## Production workflow

1. Define semantic command.
2. Validate active context.
3. Resolve stable target names/IDs.
4. Open undo group if mutating.
5. Perform bounded operation.
6. Handle cancel/errors.
7. Restore user state if promised.
8. Return/report structured result.

## Script quality rules

- begin/end undo where appropriate;
- validate every assumed object type;
- use match names where stability/localization requires it;
- handle cancel cleanly;
- preserve user state deliberately;
- keep domain logic separate from UI;
- do not hide failures with blanket `catch {}`.

## Related chapters

- [Object model](01-OBJECT-MODEL.md)
- [ScriptUI](02-SCRIPTUI.md)
- [Expressions vs scripts](03-EXPRESSIONS-VS-SCRIPTS.md)
- [Script → AE communication](../15-COMMUNICATION/05-SCRIPT-TO-AE.md)
- [CEP → ExtendScript](../15-COMMUNICATION/06-CEP-TO-EXTENDSCRIPT.md)
- [Panels](../07-PANELS/README.md)

## Evidence boundary

This chapter describes scripting architecture and public object-model practice. Version-specific object/property availability should be checked against the target AE scripting documentation.
