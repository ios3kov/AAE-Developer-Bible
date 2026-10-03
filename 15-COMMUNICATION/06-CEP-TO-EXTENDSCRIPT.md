# CEP panel <-> ExtendScript

CEP JavaScript и ExtendScript — разные runtimes. `CSInterface.evalScript(source, callback)` передаёт код в scripting engine хоста; сериализация, схема, очередь и timeout принадлежат продукту. По [Adobe CEP 12 Cookbook](https://github.com/Adobe-CEP/CEP-Resources/blob/ab5e4e3e53a42fad08e1225a22a991bb1ffe73f6/CEP_12.x/Documentation/CEP%2012%20HTML%20Extension%20Cookbook.md) этот код и manifest `ScriptPath` исполняются на main thread хоста. Callback не превращает длительный script в background compute.

## Один учебный контракт

[Шаблон](../16-WORKING-TEMPLATES/cep-panel-bridge/README.md) использует namespace `$._aeBible`, команды `ping` и `renameSelected`. Последняя добавляет префикс **всем слоям, выбранным в активной композиции на момент исполнения**, а не на момент клика. Повтор добавляет префикс ещё раз: команда не идемпотентна.

```json
{"protocol":1,"requestId":"session:1","command":"renameSelected","payload":{"prefix":"Bible_"}}
```

```json
{"protocol":1,"requestId":"session:1","ok":true,"result":{"changed":2}}
```

```json
{"protocol":1,"requestId":"session:1","ok":false,"error":{"code":"NO_ACTIVE_COMP","message":"No active composition.","outcome":"notApplied"}}
```

`ping` принимает `{}` и возвращает `result: {ready:true, protocol:1, commands:["ping","renameSelected"]}`. Это readiness handshake текущего dispatcher, не подтверждение исхода предыдущих команд и не proof всей AE/CEP compatibility matrix.

Запрос — JSON object с собственными полями: `protocol` number, `requestId` непустая строка до 128 UTF-16 code units, `command` непустая строка, `payload` object (не array/null). Только protocol 1 и две перечисленные команды поддерживаются. `prefix` — собственное строковое поле до 256 code units; произвольные значения не преобразуются в строку. Пустой префикс возвращает `changed:0` без Undo-группы после проверки композиции и selection.

Запрос и ответ ограничены 65536 UTF-16 code units; ожидание — 15000 ms. Это политики примера, **не опубликованные лимиты CEP**. Success имеет только `result`, failure — только `error`; в обоих есть `protocol:1`, `requestId` и boolean `ok`. `changed` — целое неотрицательное число.

## Контролируемые границы ошибок

Host проверяет наличие `JSON.parse/stringify` до обработки запроса. Parsing находится внутри `try/catch`; после parsing проверяются object/type/required fields, protocol, allowlist и payload. Точные реализации находятся в source-файлах [template](../16-WORKING-TEMPLATES/cep-panel-bridge/README.md), чтобы второй сокращённый dispatcher не расходился с первым.

| Отказ | Корреляция | Outcome |
|---|---|---|
| `BOOTSTRAP_FAILED`, `JSON_UNAVAILABLE` | `null`: запрос ещё не разобран | `notApplied` |
| `INVALID_JSON`, `INVALID_REQUEST` | `null` или валидный прочитанный ID для invalid fields | `notApplied` |
| `UNSUPPORTED_PROTOCOL`, `UNKNOWN_COMMAND`, `INVALID_PAYLOAD` | ID запроса | `notApplied` |
| `NO_ACTIVE_COMP`, `NO_SELECTED_LAYERS`, `TARGET_READ_FAILED` | ID запроса | `notApplied` |
| `COMMAND_FAILED` | ID запроса | `notApplied` до первого присваивания; иначе `mayHaveApplied` |
| `UNDO_CLOSE_FAILED` | ID запроса | `mayHaveApplied` после попытки изменения |
| `INTERNAL_ERROR`, `RESPONSE_SERIALIZATION_FAILED` | консервативный аварийный `null` | `mayHaveApplied` |

`notApplied` означает, что обработчик не начал изменения имён слоёв. Это не утверждение об отсутствии любых побочных эффектов, например открытия Undo-группы. `mayHaveApplied` запрещает автоматический повтор в этом примере. Фиксированный JSON fallback для отсутствующего JSON не зависит от JSON runtime.

Клиент проверяет тип/размер ответа, JSON parsing, protocol, форму success/error, результат и request ID. `null` разрешён только для перечисленных pre-correlation/аварийных ошибок с соответствующим outcome. Поэтому `JSON_UNAVAILABLE` отображается, а не теряется в stale-response filter. `EvalScript error.`, чужой ID и malformed envelope оставляют UI заблокированным.

## Строки и security

Не собирайте вызов конкатенацией пользовательского `prefix`. Сначала сериализуйте object в JSON, затем JSON-строку в строковый literal; дополнительно экранируйте U+2028/U+2029 для older JavaScript parsers. Это защищает кавычки, backslash и переводы строк при embedding. JSON parser должен быть проверенной ES3-compatible реализацией, а не обработкой untrusted input через `eval`.

Команда выбирается по allowlist. В host нет протокольного «execute arbitrary script». Namespace должен быть уникальным для продукта: глобальные scripting engines могут быть разделяемыми. Schema validation не является аутентификацией других установленных extensions.

## Correlation, порядок и повтор

Request ID связывает ответ с запросом; он не даёт дедупликацию, exactly-once execution, isolation или rollback. Stale display rejection полезен для superseded **read-only** snapshots. Отбрасывание ответа mutating command не отменяет уже исполненное изменение.

У минимальной панели один outstanding вызов, включая startup ping. Кнопка отключена до результата. После подтверждённого `notApplied` mutation error можно исправить selection и повторить вручную. После timeout, bridge exception, malformed response или `mayHaveApplied` панель блокирует новые изменения; late callback не снимает блокировку. Пользователь проверяет проект и только затем перезагружает панель. Reload не отменяет старую команду и не устанавливает её исход.

Это локальная политика одной панели. Пользователь, другие панели и scripts могут менять selection/project. Для deterministic targeting продукту нужны IDs/generation, повторное разрешение целей на host и отдельная политика deduplication. Session ID примера не идентифицирует проект. Для нескольких writers нужен явный порядок выполнения, а не только latest-request filtering.

## Undo и частичные изменения

Host заранее читает selection и готовит имена без присваиваний. После успешного `beginUndoGroup()` выполняет изменения; `finally` пытается закрыть только открытую группу. Primary error сохраняется отдельно от cleanup error. `details.changedBeforeError` считает присваивания, вернувшиеся без исключения; setter, который бросил исключение, тоже мог изменить состояние.

[Undo API](https://ae-scripting.docsforadobe.dev/general/application/#appbeginundogroup) группирует действия для Undo/Redo. Он не предоставляет транзакционный rollback. При частичном отказе требуется проверка проекта, а не слепой retry.

## Bootstrap walkthrough

1. Подготовьте `CSXS/manifest.xml` для **проверяемых** AEFT host range, RequiredRuntime/CSXS и schema version; не выводите одну версию из другой. [CEP chapter](../07-PANELS/01-CEP.md) разделяет эти поля.
2. В `Resources` задайте `<MainPath>./index.html</MainPath>` и `<ScriptPath>./host/bootstrap.jsx</ScriptPath>` относительно корня extension. Это фрагмент конфигурации, не полный валидный manifest.
3. Добавьте matching Adobe `CSInterface.js` рядом с HTML. `index.html` загружает его до `index.js`; HTML сам не загружает JSX.
4. Создайте `host/bootstrap.jsx`, который сначала загружает закреплённую JSON dependency, затем `host/index.jsx`. Например:

```jsx
// SOURCE EXAMPLE: requires separately supplied, reviewed vendor/json2.jsx.
var bridgeDirectory = File($.fileName).parent;
$.evalFile(File(bridgeDirectory.fsName + "/vendor/json2.jsx"));
$.evalFile(File(bridgeDirectory.fsName + "/index.jsx"));
```

5. У dependency сохраните repository/version/hash/license и проверки ES3 parser/stringifier; тестируйте именно packaged copy на целевом AE. [JSON-js](https://github.com/douglascrockford/JSON-js) — кандидат для review, не автоматически одобренный bundled polyfill. Наличие JSON после открытия другой панели не заменяет bootstrap.
6. Startup `ping` либо разблокирует кнопку, либо показывает явную bootstrap/protocol ошибку. Диагностируйте отдельно manifest visibility, HTML/CSInterface, загрузку JSX, JSON dependency и dispatcher.

Skeleton не содержит manifest, vendor library, polyfill или signing config и не считается установленной extension. Альтернативный panel-startup loader обязан завершить и проверить загрузку до ping; нельзя одновременно запускать loader и рабочие команды.

## Большие данные, события и cancellation

Bridge — control channel: передавайте параметры/path/token, а тяжёлые pixels/audio/model data оставляйте native/helper/file transport с явным ownership. CEP events подходят для invalidation: событие → отбросить snapshot → запросить новое состояние. Длительные host scripts препятствуют main-thread scheduling; разбивайте работу на ограниченные части, если API и операция это допускают.

Timeout — срок ожидания UI, не host deadline. Закрытие панели не отменяет отправленный script. Для cooperative cancellation нужны отдельный protocol, safe checkpoints и partial-completion semantics; этот template их не реализует.

## Проверки и evidence

`node scripts/test_cep_bridge.js` исполняет реальные source-файлы в Node VM с fake DOM, timers и AE objects: routing, malformed input/envelopes, bootstrap/JSON failure, Unicode/escaping, one-outstanding-call, timeout/late reply, execution-time selection, partial mutation и cleanup failure. Это portable logic evidence, а не запуск CEP или ExtendScript.

Для продукта отдельно проверьте packaged manifest, выбранный JSON implementation, actual engine syntax, selection/Undo/partial failure, reload и AE/CEP support matrix. В Bible: **SOURCE EXAMPLE / RUNTIME-NOT-CLAIMED**. Source review: 2026-10-04, CEP snapshot `ab5e4e3e53a42fad08e1225a22a991bb1ffe73f6`; scripting guide snapshot `7137a990db4bd8dc9f5869b8ca431c7dfed52bdc`. [Ledger](../VERIFICATION.md#block-2-cep-protocol-and-failure-paths-2026-10-04).

Связанные главы: [Script → AE](05-SCRIPT-TO-AE.md), [Native ↔ script/panel](07-NATIVE-TO-SCRIPT-PANEL.md), [Threading](08-THREADING-BOUNDARIES.md), [Data ownership](09-DATA-OWNERSHIP.md).
