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

Concrete synchronous source: [ScriptUI rename command](../20-REFERENCE-IMPLEMENTATIONS/Scripts/ScriptUI-Panel/AEDeveloperBiblePanel.jsx)
returns plain `{ok, changed, total, error, cleanupError}` without widgets/dialogs.
This local result is **not** the CEP wire envelope above; the transport adapter must
normalize/serialize it separately. A setter failure preserves completed count;
Undo-close failure can accompany fully applied edits and makes `ok=false`, not
`changed=0`. No automatic retry or rollback. The standalone rename IIFE and demo
rig are separate lessons, not this shared command or a production RPC dispatcher.

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

<a id="bridgetalk"></a>

## BridgeTalk: другая message-enabled application

**DOCUMENTED / RUNTIME-NOT-CLAIMED.** BridgeTalk относится к ExtendScript
interapplication messaging. Обычно `body` содержит код для DOM target приложения;
по умолчанию принимающий `BridgeTalk.onReceive` вычисляет его. Это иной route,
чем CEP `CSInterface.evalScript()` или native `AEGP_ExecuteScript()`.
[Messaging overview](https://github.com/docsforadobe/javascript-tools-guide/blob/ac6839049e17f4652d301e7d28f8f0d3d5fbb66a/docs/interapplication-communication/communications-overview.md),
[API scope](https://github.com/docsforadobe/javascript-tools-guide/blob/ac6839049e17f4652d301e7d28f8f0d3d5fbb66a/docs/interapplication-communication/messaging-framework-api-reference.md).

### Выбрать target и сохранить его identity

**DOCUMENTED.** `BridgeTalk.getTargets(null, null)` перечисляет известные
message-enabled installations с version/locale; `getSpecifier(appName, version,
locale)` возвращает подходящий полный specifier либо `null`. При version `0` или
без version ищется наиболее новая версия. Major-only выбор может выбрать её
старший minor. `isRunning()` сообщает running state; `getStatus()` также различает
занятость, обработку очереди и недоступность. Modal UI target может означать BUSY.
[BridgeTalk class](https://github.com/docsforadobe/javascript-tools-guide/blob/ac6839049e17f4652d301e7d28f8f0d3d5fbb66a/docs/interapplication-communication/bridgetalk-class.md).

Generic `"aftereffects"` не фиксирует installation: разрешение зависит от
версии/locale/окружения. Application specifier и namespace вызова вроде
`photoshop.open(...)` имеют разные правила. Instance suffix применяется только
к приложениям, которые поддерживают несколько instances; из него не следует
адресация произвольного AE PID.
[Specifiers](https://github.com/docsforadobe/javascript-tools-guide/blob/ac6839049e17f4652d301e7d28f8f0d3d5fbb66a/docs/interapplication-communication/application-and-namespace-specifiers.md).

Практический маршрут: проверить наличие BridgeTalk в данном engine, перечислить
реально найденные targets, выбрать разрешённый продуктом полный specifier и
сохранить его вместе с request. Не собирать marketing-version strings по памяти.
При нескольких установках показать выбор или применить явно записанную policy.
Перед mutation полезен короткий read-only handshake: фактическая identity,
версия собственного dispatcher, capabilities и context token проекта.

~~~jsx
// SOURCE EXAMPLE: только построение read-only probe; отправитель добавляет handlers.
function makeIdentityProbe(fullSpecifier) {
    var message = new BridgeTalk();
    message.target = fullSpecifier;
    message.body = "BridgeTalk.appSpecifier;";
    message.timeout = 15; // seconds, пример policy срока входной очереди
    return message;
}
~~~

Default receive handler нужен для этой формы body. Custom dispatcher может
определить собственный формат. Полученный specifier — данные ответа для проверки,
а не разрешение автоматически запускать следующую destructive command.

### Отправка, callbacks и два разных timeout

**DOCUMENTED.** Перед `send()` настроить target/body/callbacks и сохранить сам
message в объекте, который переживёт ответ; иначе GC может лишить отправителя
callback. Результат транспорта — строка, даже когда target возвращает другое
значение. Старые `toSource()`/`eval()` examples не являются обязательным форматом
product protocol. Передавать plain serialized values, проверять схему; availability
JSON implementation рассмотрена в runtime и CEP главах.
[Message workflow](https://github.com/docsforadobe/javascript-tools-guide/blob/ac6839049e17f4652d301e7d28f8f0d3d5fbb66a/docs/interapplication-communication/communicating-through-messages.md).

| Сигнал / настройка | Документированный смысл |
|---|---|
| `send()` / `send(0)` | Асинхронная отправка; `true` означает возможность немедленной отправки, не completion |
| `send()` вернул `false` | Отправка невозможна **либо** сообщение осталось в очереди; при автозапуске target это предусмотренный результат |
| `message.timeout = seconds` | Срок ожидания извлечения из входной очереди; истёкшее до обработки сообщение отбрасывается, возможен `onTimeout` |
| `send(seconds)` с положительным значением | Синхронно ждать результат до этого срока; это другой параметр |
| `onReceived` | Receipt acknowledgement, не результат command |
| `onResult` | Может быть intermediate либо final result: `sendResult()` допускает несколько ответов |
| `onError` | `body` содержит сообщение; `headers["Error-Code"]` — код ошибки |

[Message contract](https://github.com/docsforadobe/javascript-tools-guide/blob/ac6839049e17f4652d301e7d28f8f0d3d5fbb66a/docs/interapplication-communication/bridgetalk-message-object.md).
Callbacks опциональны и не обещаны всеми message-enabled hosts. Положительный
deadline синхронного `send` не объявлен механизмом отмены выполняемой target
операции.

Практический registry хранит request ID, полный target, phase, message и UI sink.
Создать запись **до** `send`; false-return оставить как `queuedOrUnavailable`,
receipt перевести в `received`. Протокол с progress должен явно различать
`progress` и `done`: первый `onResult` не освобождает запись. Final result/error
сохраняет plain outcome, после чего transport callback owner можно освободить.
Общий UI deadline даёт `outcomeUnknown`; скрытие панели отключает sink и не
доказывает остановку target. Без idempotency/deduplication не повторять mutation
автоматически. Ограничить число pending requests; зависшую запись не держать
бесконечно без политики abandonment и последующей сверки outcome.

Такой route не создаёт поток для вызовов AE DOM. Обработка зависит от message
loop target. `BridgeTalk.pump()` обрабатывает входящие/исходящие сообщения;
не превращать его в tight polling и учитывать возможность callback во время
явного pump. Полноценная отмена требует собственного cooperative protocol.

Коды messaging layer различают script/runtime и transport проблемы, но сами по
себе не сообщают число уже выполненных edits. Логировать code отдельно от body;
product envelope должен сообщать `changed`/partial outcome. В справочнике
отрицательные error codes помечены как unrecoverable; универсальный retry по
любой ошибке этому контракту не соответствует.
[Error codes](https://github.com/docsforadobe/javascript-tools-guide/blob/ac6839049e17f4652d301e7d28f8f0d3d5fbb66a/docs/interapplication-communication/messaging-error-codes.md).

### Cross-DOM wrappers и historical scope

Cross-DOM даёт небольшой набор startup-script wrappers; точный набор зависит от
приложения. У `executeScript`, `open` и `print` нет result, подтверждающего
завершение команды. Неверсионированный namespace выбирает старшую установленную
версию; он не является алиасом текущего AE context.
[Cross-DOM](https://github.com/docsforadobe/javascript-tools-guide/blob/ac6839049e17f4652d301e7d28f8f0d3d5fbb66a/docs/interapplication-communication/cross-dom-functions.md).
Для управляемого automation workflow предпочтительнее явный target и собственный
response contract. Не заменять global `BridgeTalk.onReceive` из небольшой
утилиты: такой handler меняет приём unsolicited messages всего приложения и
требует отдельного ownership/restore решения.

Source review: все 9 interapplication pages JavaScript Tools Guide mirror на
`ac6839049e17f4652d301e7d28f8f0d3d5fbb66a`. Таблицы CS4/CS5 и старые startup paths
оставлены historical evidence. Review не объявляет modern AE/Photoshop/Premiere
support matrix, гарантии каждого callback, единый Undo между приложениями или
сохранение engine после завершения произвольного script invocation.

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
