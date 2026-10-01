# Communication architecture

Коммуникация в After Effects — это не просто вопрос «как передать данные». Правильный bridge должен сохранять:

- **host lifecycle**;
- **threading rules**;
- **ownership/lifetime**;
- **dependency visibility**;
- **version compatibility**;
- **failure semantics**.

Если канал обходит эти правила, он может работать в простом тесте и всё равно ломать cache, MFR, undo, project state или shutdown.

## Сначала определить владельца состояния

Перед выбором транспорта ответьте:

1. Кто источник истины?
2. Кто имеет право изменять состояние?
3. Кто инициирует команду?
4. На каком thread разрешён host API?
5. Нужно ли состояние видеть render/cache dependency model?
6. Нужно ли переживать reload/restart?
7. Может ли ответ устареть до доставки?

Плохая архитектура часто начинается с двух компонентов, которые оба считают себя владельцем одного state.

## Host-owned channels

### Effect plug-in

~~~text
After Effects
→ PF_Cmd selector
→ EffectMain
→ output / out_data / host callbacks
~~~

Effect должен получать render-affecting state через host-visible parameters, sequence/frame data и documented APIs.

Не прячьте render dependency в:

- global singleton;
- panel DOM;
- temp JSON file;
- undocumented process memory;
- external service without explicit cache invalidation strategy.

### AEGP

~~~text
After Effects
→ registered hook/callback
→ AEGP code
→ host suites
~~~

AEGP хорошо подходит для project/control-plane operations: commands, project/items/layers, render queue, idle/update hooks и native integration.

### AEIO

Host вызывает зарегистрированный function block. AEIO callbacks — часть host-driven import/export lifecycle, а не произвольный RPC surface.

### Artisan

Host вызывает renderer entry points и предоставляет suite/context state. Renderer не должен превращаться в общий application service только потому, что он native.

### ExtendScript

~~~text
script
→ scripting DOM
→ After Effects project/UI state
~~~

Подходит для orchestration и project automation. Не подходит как heavy binary data path.

### CEP / panel

~~~text
HTML/JS panel
→ evalScript / event bridge
→ ExtendScript / host-facing layer
→ AE
~~~

Panel — control surface. DOM panel-а не должен быть persistent source of truth для project/render state.

## Cross-component channels

### AEGP → Effect

Для scoped native command к конкретному effect instance:

- `AEGP_EffectCallGeneric`;
- `PF_Cmd_COMPLETELY_GENERAL`.

Использовать для небольших versioned control messages. Не передавать long-lived host pointers между независимыми lifetimes.

### Native → Native through PICA

Published suite подходит, когда один native module предоставляет сервис другому.

Contract должен включать:

- suite name;
- public version;
- function-table ABI;
- ownership;
- thread assumptions;
- provider lifetime;
- failure if suite unavailable.

### Native → scripting

`AEGP_ExecuteScript` полезен, когда нужная операция доступна только scripting layer или когда продукт осознанно использует script as orchestration.

Это не причина переносить heavy native workflow в строки.

### CEP → ExtendScript

`CSInterface.evalScript` — control-plane bridge.

Хорошие payloads:

- command;
- IDs;
- small state snapshots;
- options;
- progress;
- structured errors.

Плохие payloads:

- pixels;
- audio buffers;
- huge project dumps every frame;
- ML tensors;
- binary archives encoded as strings.

### External helper / process

Если нужен отдельный process, используйте IPC, которым владеет продукт:

- local socket;
- named pipe;
- loopback protocol;
- file handoff;
- shared memory;
- process-specific RPC.

Document:

- discovery;
- authentication/trust boundary;
- message version;
- retry rules;
- process lifetime;
- shutdown;
- stale requests;
- large-payload ownership.

Не используйте undocumented AE internal IPC как production contract.

## Control plane vs data plane

### Control plane

Небольшие сообщения:

- commands;
- IDs;
- configuration;
- state summaries;
- progress;
- errors.

### Data plane

Большие/частые данные:

- pixels;
- audio;
- large binary buffers;
- tensors;
- cached frames.

Правило:

> control plane можно сериализовать; data plane должен оставаться там, где его не приходится постоянно превращать в текст.

## Synchronous vs asynchronous

### Synchronous

Используйте, когда:

- операция быстрая;
- caller должен немедленно получить результат;
- host contract сам synchronous;
- нельзя безопасно продолжить без ответа.

Опасность: blocking main thread.

### Asynchronous

Используйте, когда:

- helper/process выполняет долгую работу;
- panel ждёт background task;
- ответ может прийти позже.

Нужны:

- request ID;
- generation/revision;
- timeout;
- cancellation policy;
- stale-response rejection;
- explicit completion/error state.

Async callback не делает host API thread-safe автоматически.

## Request identity

Минимальный versioned request:

~~~json
{
  "protocol": 1,
  "requestId": "panel-42",
  "command": "refreshProject",
  "payload": {}
}
~~~

Response:

~~~json
{
  "protocol": 1,
  "requestId": "panel-42",
  "ok": true,
  "result": {}
}
~~~

Error:

~~~json
{
  "protocol": 1,
  "requestId": "panel-42",
  "ok": false,
  "error": {
    "code": "NO_ACTIVE_COMP",
    "message": "No active composition"
  }
}
~~~

Transport error и domain error — разные вещи.

## Ownership across a bridge

Через bridge лучше передавать:

- values;
- immutable IDs;
- copied strings;
- serialized state;
- file/resource handles with explicit ownership contract.

Не передавать как long-lived opaque state:

- raw AE handles;
- borrowed worlds;
- suite pointers;
- stack pointers;
- callback-local references.

Если host ref нужен позже, документированный API должен позволять безопасно получить его заново.

## Dependency visibility

Самая опасная ошибка — скрытое состояние, влияющее на render.

Пример плохого дизайна:

~~~text
panel changes global native variable
→ render code reads global variable
→ AE parameter/dependency graph ничего не знает
~~~

Возможные последствия:

- stale cache;
- разные результаты MFR;
- render queue отличается от UI preview;
- project reopen не восстанавливает state.

Render-affecting persistent state должен находиться в host-visible model либо иметь документированную invalidation/dependency strategy.

## Undo and project mutation

Bridge не должен автоматически означать «одна UI команда = много независимых host mutations».

Для project-changing command определите:

- кто открывает undo group;
- кто закрывает;
- что происходит при partial failure;
- нужен ли refresh после mutation;
- что возвращает command — old state, new state или только operation ID.

Undo не является database rollback. Если операция частично выполнена и затем упала, это нужно документировать отдельно.

## Threading

Главное правило:

> host API не считается thread-safe, пока конкретный API явно этого не обещает.

Panel/helper/background thread может:

- парсить JSON;
- считать pure data;
- делать network/file IO;
- готовить command payload.

Host mutation обычно должна быть marshalled в documented host/main-thread path.

Подробнее: [Threading boundaries](../15-COMMUNICATION/08-THREADING-BOUNDARIES.md).

## Failure model

Продумайте минимум:

- transport unavailable;
- malformed payload;
- version mismatch;
- timeout;
- stale response;
- duplicate request;
- command unsupported;
- host state changed meanwhile;
- partial mutation;
- helper process died;
- component unloaded.

Failure должен быть machine-readable там, где это нужно логике продукта.

## Channel selection table

| Need | Recommended channel |
|---|---|
| effect parameter/render dependency | Effect parameters / stream / host-visible state |
| project mutation | AEGP or scripting DOM |
| native command to effect instance | generic effect call |
| shared native service | PICA suite |
| panel project command | panel → script/native command bridge |
| scripting-only operation from native | ExecuteScript, deliberately |
| heavy pixels/audio | native/GPU/shared memory/file/data-plane path |
| cross-process helper | explicit owned IPC |
| UI notification | panel event/state channel |
| persistent product configuration | owned config storage with version/migration |

## Anti-patterns

### One giant bridge

Один `execute("anything", json)` без schema/version/ownership быстро превращается в скрытый internal API.

### eval of arbitrary script strings

Предпочтительнее dispatcher с известными commands.

### Polling everything continuously

Polling допустим как explicit fallback, но нужно учитывать cost, visibility и staleness.

### Shared mutable global state

Особенно опасно для render/MFR.

### “Fire and forget” project mutation

Без request ID/result невозможно отличить success от lost command.

### Treating process path as module identity

Фактически загруженный module может отличаться от installer expectation. Проверяйте real loaded image при debugging.

## Production workflow

1. Определить source of truth.
2. Разделить control/data plane.
3. Выбрать documented channel.
4. Описать request/response version.
5. Описать ownership.
6. Описать threading/marshalling.
7. Описать timeout/stale/failure.
8. Описать undo/project mutation semantics.
9. Описать shutdown/reload.
10. Только после этого оптимизировать transport.

## Related chapters

- [Communication section](../15-COMMUNICATION/README.md)
- [Threading boundaries](../15-COMMUNICATION/08-THREADING-BOUNDARIES.md)
- [Data ownership](../15-COMMUNICATION/09-DATA-OWNERSHIP.md)
- [CEP → ExtendScript](../15-COMMUNICATION/06-CEP-TO-EXTENDSCRIPT.md)
- [Native ↔ script/panel](../15-COMMUNICATION/07-NATIVE-TO-SCRIPT-PANEL.md)
- [PICA suites](../14-NATIVE-INTEGRATIONS/03-PICA-SUITES.md)

## Evidence boundary

Native generic-call/PICA contracts are SDK-contract-reviewed against the SDK 25.6 source material. Panel/script/IPC guidance is architecture and public-documentation guidance unless a specific runtime observation is explicitly cited.
