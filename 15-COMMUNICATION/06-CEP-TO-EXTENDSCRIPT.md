# CEP panel ↔ ExtendScript

Обновлено **2026-10-01**. CEP panel и ExtendScript — два разных JavaScript runtime. Panel не получает scripting DOM напрямую: доступ к AE идёт через host bridge.

Связанные главы:

- [CEP development](../07-PANELS/01-CEP.md)
- [UXP transition](../07-PANELS/02-UXP-TRANSITION.md)
- [Script → AE](05-SCRIPT-TO-AE.md)

## 1. Runtime model

~~~text
CEP HTML/JS runtime
      |
      | CSInterface.evalScript(...)
      v
After Effects ExtendScript engine
      |
      v
AE scripting DOM
~~~

Официальный CEP cookbook разделяет HTML DOM и host Application/ExtendScript DOM.

evalScript запускает script в host ExtendScript engine. Cookbook также указывает, что host script и CEP event dispatch зависят от host main-thread scheduling.

Asynchronous callback в panel API не делает host-side script background worker.

## 2. One bridge, not evalScript everywhere

Плохо:

~~~text
ButtonA -> evalScript
ButtonB -> evalScript
component -> evalScript
timer -> evalScript
~~~

Хорошо:

~~~text
UI
 ↓
Bridge.request(command, payload)
 ↓
one evalScript dispatcher
 ↓
$._myTool.dispatch(...)
 ↓
AE scripting service
~~~

Так protocol можно тестировать отдельно от UI.

## 3. Namespace and bootstrap

~~~jsx
$._myTool = $._myTool || {};

$._myTool.dispatch = function(jsonText) {
    // parse → validate → route → stringify response
};
~~~

Не полагайтесь на то, что много JSX-файлов безопасно определяют одинаковые globals: последняя загрузка может перезаписать предыдущую.

## 4. Request protocol

~~~json
{
  "protocol": 1,
  "requestId": "42",
  "command": "renameSelected",
  "payload": {
    "name": "Hero"
  }
}
~~~

Dispatcher:

1. parse JSON;
2. validate protocol;
3. allowlist command;
4. validate payload shape/range;
5. execute;
6. return normalized JSON envelope.

## 5. User data is data, not script source

Нельзя:

~~~js
cs.evalScript('rename("' + userText + '")');
~~~

Один практический pattern:

~~~js
const wire = JSON.stringify(message);
const jsxArg = JSON.stringify(wire);
cs.evalScript('$._myTool.dispatch(' + jsxArg + ')', onResult);
~~~

В ExtendScript:

~~~jsx
var message = JSON.parse(jsonText);
~~~

Quoting/escaping централизуется на transport layer.

## 6. Response envelope

Success:

~~~json
{
  "ok": true,
  "requestId": "42",
  "result": {"changed": 3}
}
~~~

Failure:

~~~json
{
  "ok": false,
  "requestId": "42",
  "error": {
    "code": "NO_COMP",
    "message": "No active composition"
  }
}
~~~

Human-readable строка не должна быть единственным machine contract.

## 7. Transport error ≠ application error

Различайте:

~~~text
CEP/evalScript transport failed
script failed before envelope
protocol rejected
domain command failed
command succeeded
~~~

Panel должен показывать diagnostic, не превращая всё в Unknown error.

## 8. Request IDs and stale responses

Каждый запрос имеет requestId. Для snapshots полезен generation/revision.

~~~text
request generation 12
→ UI moved to 13
→ old response arrives
→ ignore as stale
~~~

Старый callback не должен перетирать новое состояние.

## 9. Backpressure

Не запускать десятки evalScript calls на каждый mousemove.

Для high-frequency UI:

- debounce/coalesce reads;
- batch related writes;
- latest-wins для transient preview, если semantic допускает;
- serial queue для order-sensitive mutations;
- explicit Apply для дорогой операции.

## 10. AE/ExtendScript → panel

ExtendScript не может напрямую менять CEP HTML DOM. Для notification используется CEP/CSXS event path.

~~~text
host state changed
→ small state-invalidated event
→ panel receives event
→ panel requests fresh normalized snapshot
~~~

Для большого state лучше invalidation + pull, чем сотни mutation events.

## 11. Event payload

Event payload должен быть versioned, small, serializable, без raw pointers/handles и не единственным source of truth.

## 12. Idempotency and retry

Не retry автоматически destructive command, если неизвестно, выполнился ли первый вызов.

Для reconnect/reload:

- request/operation IDs;
- idempotent commands где возможно;
- duplicate detection, если это важно.

## 13. Reload / extension restart

~~~text
panel boot
→ protocol handshake
→ query host snapshot
→ reconstruct UI state
→ resume interaction
~~~

DOM state после reload не authoritative.

## 14. Payload size

String bridge подходит для control data и small snapshots.

Не гоняйте через evalScript:

- pixel buffers;
- audio blocks;
- large binary models;
- huge Base64 blobs;
- frequent telemetry streams.

## 15. Security boundary

- allowlist commands;
- validate paths/enums/ranges;
- never eval downloaded code;
- не вставлять remote/user text в script source;
- не хранить secrets в panel bundle;
- downloaded code и downloaded data — разные trust classes.

## 16. Acceptance checklist

Проверить:

- malformed JSON;
- unknown protocol/command;
- quotes/newlines/unicode;
- long allowed string;
- rapid requests;
- stale callback;
- panel reload;
- project change while panel open;
- script exception;
- event during long host call;
- missing JSX bootstrap;
- clean AE restart.

## Verification boundary

CEP bridge rules сверены с Adobe CEP cookbook/CEP resources, включая разделение HTML и host DOM и main-thread scheduling evalScript/events. Этот editorial pass не является новым AE host test.
