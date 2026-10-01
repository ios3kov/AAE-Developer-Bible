# ExtendScript → After Effects

Обновлено **2026-10-01**. ExtendScript работает внутри scripting engine After Effects и управляет host через high-level scripting DOM. Это control/automation API, а не render API и не low-level native ABI.

Связанные главы:

- [After Effects scripting object model](../06-SCRIPTING/01-OBJECT-MODEL.md)
- [CEP ↔ ExtendScript](06-CEP-TO-EXTENDSCRIPT.md)
- [Threading boundaries](08-THREADING-BOUNDARIES.md)

## 1. Execution path

~~~text
script / JSX command
        ↓
After Effects ExtendScript engine
        ↓
app → project → items/comps → layers → properties
        ↓
host-owned project state
~~~

Script получает host objects, а не копию проекта. Structural mutation, selection changes и удаление объектов могут менять валидность ранее сохранённых ссылок.

## 2. Validate before mutate

~~~jsx
function renameFirstLayer(newName) {
    if (!app.project) {
        throw new Error("NO_PROJECT");
    }

    var comp = app.project.activeItem;
    if (!(comp instanceof CompItem)) {
        throw new Error("NO_ACTIVE_COMP");
    }

    if (comp.numLayers < 1) {
        throw new Error("NO_LAYER");
    }

    comp.layer(1).name = newName;
}
~~~

До первого изменения проверяйте:

- тип active item;
- существование слоя/property/effect;
- диапазоны 1-based индексов;
- наличие файла/папки;
- capability flags вроде canAddProperty/canSetExpression;
- support/version gate.

## 3. Undo group — история, не transaction

~~~jsx
app.beginUndoGroup("My Tool");

try {
    // validate and mutate
} finally {
    app.endUndoGroup();
}
~~~

Undo group объединяет изменения в историю Undo, но exception сам по себе не откатывает уже выполненную половину команды.

Если partial mutation недопустим:

1. проверить prerequisites до первого edit;
2. только потом менять проект;
3. явно чистить product-owned temporary objects на failure path;
4. держать undo ownership на command boundary.

## 4. Reacquire after structural mutation

Indexed property groups могут перестраиваться после add/remove/move.

~~~jsx
var effects = layer.property("ADBE Effect Parade");
var slider = effects.addProperty("ADBE Slider Control");
var sliderIndex = slider.propertyIndex;

effects.addProperty("ADBE Color Control");
slider = effects.property(sliderIndex);
~~~

Не считать host object reference бессрочной.

## 5. Stable identity

Display name — UI label, не всегда machine identity.

Для effects/properties предпочитайте match names там, где API их предоставляет. Для product-owned объектов храните собственный stable ID, а не полагайтесь только на имя слоя.

## 6. Command layer

~~~text
UI / panel / test harness
        ↓
plain command + validated payload
        ↓
scripting service
        ↓
AE scripting DOM
        ↓
plain result
~~~

Одна операция должна быть вызываема из ScriptUI, CEP, JSX harness, native AEGP через ExecuteScript и будущего panel adapter без переписывания business logic.

## 7. Native → script через AEGP Utility Suite

Public AEGP Utility Suite предоставляет AEGP_IsScriptingAvailable и AEGP_ExecuteScript.

AEGP_ExecuteScript принимает script string и может вернуть result последней строки и error string как AEGP_MemHandle.

~~~text
check scripting available
→ ExecuteScript
→ inspect returned result/error handles
→ release owned memory handles with matching Memory Suite API
~~~

Не теряйте result/error handles на early return.

Bridge подходит для редких host automation calls, но не для high-frequency IPC и больших данных.

Источник публичного контракта: AEGP_UtilitySuite6 в After Effects C++ SDK Guide. Shipping code всё равно сверяется с headers целевого SDK.

## 8. app.executeCommand boundary

app.executeCommand(id) может вызвать host menu command, но numeric command ID не является хорошим стабильным product protocol.

Использовать только если:

- нет лучшего public DOM/API;
- ID подтверждён на поддерживаемых версиях;
- behavior покрыт host test;
- есть clear failure/fallback.

## 9. Error contract

~~~json
{
  "ok": false,
  "requestId": "42",
  "error": {
    "code": "NO_ACTIVE_COMP",
    "message": "Open a composition first"
  }
}
~~~

Разделяйте:

1. script parse/runtime failure;
2. command validation failure;
3. AE operation failure;
4. transport failure, если script вызван через CEP/native bridge.

Machine code должен быть стабильнее human text.

## 10. Long work

ExtendScript — плохое место для heavy CPU, больших binary transforms и tight polling.

~~~text
external/pure compute
→ compact result
→ short host mutation
→ normalized response
~~~

Для длинной операции добавляйте осмысленные chunks и cancellation/progress boundary.

## 11. Project persistence

Runtime JavaScript object не является надёжным persistent storage.

Если state должен пережить reopen/restart, заранее выберите owner:

- project objects/properties;
- deliberate serialized metadata;
- external product state, если он не обязан ехать вместе с project.

## 12. Acceptance checklist

Проверить:

- no project;
- wrong active item;
- empty comp;
- missing effect/property;
- localized UI;
- cancel path;
- partial failure;
- save/reopen;
- repeated invocation;
- supported AE versions;
- ExecuteScript result/error cleanup, если bridge используется.

## Verification boundary

Глава описывает public scripting model и production architecture pattern. Текущий editorial pass не является новым host run. Native AEGP_ExecuteScript и scripting workflows проверяются отдельно на заявленной версии SDK/AE.
