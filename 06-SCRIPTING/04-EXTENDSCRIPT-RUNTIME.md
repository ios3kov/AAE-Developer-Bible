# ExtendScript: runtime, данные и отладка

**DOCUMENTED / SOURCE EXAMPLE / RUNTIME-NOT-CLAIMED; review 2026-10-08.**
Полностью прочитаны ещё 34 страницы [JavaScript Tools Guide](https://github.com/docsforadobe/javascript-tools-guide/tree/ac6839049e17f4652d301e7d28f8f0d3d5fbb66a/docs)
на revision `ac6839049e17f4652d301e7d28f8f0d3d5fbb66a`. Это community-maintained
зеркало Adobe guide, включающее исторические CS4/CS5 и ESTK разделы. Современный
маршрут отладки отдельно сверён с официальной документацией Adobe ниже. Ни библиотека,
ни сеть, ни AE в этом обзоре не запускались. Полное чтение страниц не означает
поддержку всех перечисленных возможностей в каждой версии AE.

[File/Folder и базовый runtime](01-OBJECT-MODEL.md#extendscript-files-runtime),
[ScriptUI](02-SCRIPTUI.md), [BridgeTalk](../15-COMMUNICATION/05-SCRIPT-TO-AE.md#bridgetalk)
и [CEP bridge](../15-COMMUNICATION/06-CEP-TO-EXTENDSCRIPT.md)
разбирают соседние операции. Здесь — дополнительные контракты и собственные сценарии.

## 1. Engine, глобальное состояние и диагностика

**DOCUMENTED.** [Startup scripts](https://github.com/docsforadobe/javascript-tools-guide/blob/ac6839049e17f4652d301e7d28f8f0d3d5fbb66a/docs/introduction/scripting-for-specific-applications.md)
могут исполняться разными приложениями; расположение, права и порядок загрузки
зависят от host. Сохранение глобальных переменных в engine не является сохранением
данных проекта. Общий guide направляет за DOM и правилами запуска к документации
конкретного приложения.

**Проектное решение.** Инициализация инструмента проверяет целевое приложение,
занимает один собственный namespace и допускает повторный запуск. Локальные
временные значения держать внутри функции. При перезагрузке явно управлять
callbacks и их поколением: новое определение функции само по себе не отменяет
старую работу. Настройки `$.locale`, `$.localize`, `UnitValue.baseUnit`, XML parser
и поиска библиотек считать общими для соответствующего engine. Предпочитать
параметры экземпляра; временные изменения восстанавливать через `finally`.

### Reflection: описание объекта и фактический доступ

**DOCUMENTED.** [Reflection](https://github.com/docsforadobe/javascript-tools-guide/blob/ac6839049e17f4652d301e7d28f8f0d3d5fbb66a/docs/extendscript-tools-features/extendscript-reflection-interface.md)
даёт `reflect.methods`, `reflect.properties`, `reflect.find(name)`; поиск может
вернуть `null`. Перечень динамических свойств включает уже затронутые свойства.
`dataType` описывает тип значения, `type` — категорию вроде `readonly`, `readwrite`,
`createonly`, `method`. Help, defaults и bounds могут отсутствовать.

**Сценарий диагностики.** Сначала сохранить небольшой список имён и доступных
описаний. Читать значения отдельно, с лимитом элементов и обработкой ошибки
каждого getter. Автоматически вызывать обнаруженные методы или присваивать
значения по `readwrite` нельзя: контекстные условия задаёт API самого объекта.
Reflection snapshot не доказывает полноту DOM, пригодность сохранённой ссылки
или возможность вернуть прежнее состояние. Пример guide с `.type // number`
расходится с его же таблицей `dataType`.

## 2. Единицы, локализация и короткий ввод

**DOCUMENTED.** [UnitValue](https://github.com/docsforadobe/javascript-tools-guide/blob/ac6839049e17f4652d301e7d28f8f0d3d5fbb66a/docs/extendscript-tools-features/specifying-measurement-values.md)
хранит число вместе с единицей. Неизвестная единица даёт `type === "?"`.
`as(unit)` возвращает число, `convert(unit)` меняет объект; conversion failure
нужно обрабатывать. `px` и `%` требуют базы: размер одного пикселя либо величина 100%.
Значение класса `UnitValue.baseUnit` меняет общий default; свойство экземпляра
задаёт его собственную базу.

**SOURCE EXAMPLE / RUNTIME-NOT-CLAIMED.** Собственная функция для физического
размера при явно выбранном DPI; это не преобразование координат композиции AE:

```jsx
function centimetersToPixels(cm, dpi) {
    if (typeof cm !== "number" || !isFinite(cm) || cm < 0 ||
        typeof dpi !== "number" || !isFinite(dpi) || dpi <= 0)
        throw new Error("Expected finite size and positive DPI");
    var length = new UnitValue(cm, "cm");
    length.baseUnit = new UnitValue(1 / dpi, "in");
    var pixels = length.as("px");
    if (!isFinite(pixels)) throw new Error("Conversion overflow");
    return pixels;
}
```

Округление, допустимый размер output и связь с pixel aspect ratio задаёт вызывающая
операция. Арифметическая ошибка guide `4 ft → 36 in` не является ожидаемым результатом:
четыре фута равны 48 дюймам. [Operator overloading](https://github.com/docsforadobe/javascript-tools-guide/blob/ac6839049e17f4652d301e7d28f8f0d3d5fbb66a/docs/extendscript-tools-features/operator-overloading.md)
позволяет менять поведение операторов классов; для некоммутативных операций важен
порядок operands, а `undefined` запрашивает стандартное поведение. Это расширение
ExtendScript; результат удобно явно привести к выбранной единице до сериализации.

**DOCUMENTED.** [localize()](https://github.com/docsforadobe/javascript-tools-guide/blob/ac6839049e17f4652d301e7d28f8f0d3d5fbb66a/docs/extendscript-tools-features/localizing-extendscript-strings.md)
выбирает строку из locale-object и подставляет `%1`, `%2` и следующие аргументы.
Явный вызов не зависит от `$.localize`. Наличие `en` даёт запасной текст;
без подходящего варианта источник допускает возврат самого object.
`$.locale` позволяет тестовую подмену, сброс к locale приложения выполняется
присваиванием `null`. Формат `$$$...` относится к внутренним словарям Adobe.

**Проектное решение.** Локализовать сообщения, оставляя ключи схемы, match names,
идентификаторы и числовое представление транспорта стабильными. Не менять locale
всего engine ради одной подписи. Для [prompt](https://github.com/docsforadobe/javascript-tools-guide/blob/ac6839049e17f4652d301e7d28f8f0d3d5fbb66a/docs/extendscript-tools-features/user-notification-dialogs.md)
сначала различить отмену `null` и принятую пустую строку, затем проверить ввод;
`confirm` возвращает Boolean, `alert` результата не возвращает. Кнопка подтверждения
не заменяет валидацию плана. Проверку ввода завершить до открытия Undo group.

## 3. Socket: ограниченная передача по собственному протоколу

**DOCUMENTED.** [Socket reference](https://github.com/docsforadobe/javascript-tools-guide/blob/ac6839049e17f4652d301e7d28f8f0d3d5fbb66a/docs/external-communication/socket-object-reference.md)
описывает TCP: `open(host:port)` либо `listen(port)`; `poll()` listener возвращает
отдельный Socket или `null`. `read(n)` возвращает до n символов, в том числе короткое
чтение при timeout/закрытии. `eof` означает пустой receive buffer. `timeout` относится
к чтению/записи. `write` и `close` возвращают Boolean; количества частично отправленных
байтов нет. Текстовый режим меняет CR/CRLF, `BINARY` сохраняет их. Закрывать нужно явно;
garbage collection не задаёт момент закрытия.

**Собственный сценарий запроса к локальному helper.** Заранее согласовать ASCII
header с длиной, encoding payload, максимальный header, размер сообщения, correlation
ID и ответ о завершении. В этом сценарии length означает байты payload: выбрать
режим `BINARY`, собрать byte-string до объявленной длины и только затем декодировать
текст согласованным codec. Число UTF-8 bytes нельзя подставлять в `read(n)`
текстового режима как число символов. Получать header ограниченными порциями; проверить формат
длины и предел до накопления payload. Затем дочитывать ровно заявленный объём,
учитывая каждое короткое чтение. Не завершать сообщение по одному `eof`.
Отсутствие прогресса до конца сообщения — отдельный
failure, не успех и не повод бесконечно повторять `read`. Остаток следующего сообщения
сохранять только если протокол допускает несколько сообщений на соединение.

После failure записи результат операции может быть неизвестен: повтор разрешён
лишь протоколом с дедупликацией или проверкой статуса. Успех `write` не заменяет
прикладное подтверждение. Сохранить primary error до cleanup, затем отдельно
зафиксировать ошибку `close`; listener и принятый Socket имеют разных владельцев.
В панели нужен короткий ограниченный шаг работы и отмена между шагами. Общий deadline
не прерывает уже начавшийся блокирующий вызов.

Guide не задаёт TLS, проверку сертификатов, DNS/connect deadline или принудительную
отмену I/O; из номера порта 443 эти свойства не возникают. Для HTTPS и длительного
I/O использовать отдельный сервис с таким контрактом. Его наличие не выдаёт новых
AE DOM возможностей.

[Старые Socket samples](https://github.com/docsforadobe/javascript-tools-guide/blob/ac6839049e17f4652d301e7d28f8f0d3d5fbb66a/docs/external-communication/socket-object.md)
не подходят как шаблон операции: бесконечный `poll` удерживает вызывающий поток,
одно большое `read` не собирает гарантированно целое сообщение, а web-server example
читает request через listener `conn`, хотя общаться нужно через результат `poll`.
Исторический список CS5 в [обзоре](https://github.com/docsforadobe/javascript-tools-guide/blob/ac6839049e17f4652d301e7d28f8f0d3d5fbb66a/docs/external-communication/index.md)
не является сегодняшней матрицей совместимости.

## 4. ExternalObject: библиотека и владельцы ресурсов

**DOCUMENTED.** [Загрузка](https://github.com/docsforadobe/javascript-tools-guide/blob/ac6839049e17f4652d301e7d28f8f0d3d5fbb66a/docs/integrating-external-libraries/loading-and-using-shared-libraries.md)
создаёт wrapper `new ExternalObject("lib:" + filespec)`. Функции библиотеки могут
вызываться через wrapper; indirect interface позволяет библиотеке определять
собственные JS-классы. [Поиск](https://github.com/docsforadobe/javascript-tools-guide/blob/ac6839049e17f4652d301e7d28f8f0d3d5fbb66a/docs/integrating-external-libraries/externalobject-object.md)
использует общие `searchFolders`; относительные варианты привязаны к `Folder.startup`.
`search()` только ищет библиотеку, не загружая её. Это не проверка ABI, её версии
или безопасности выбранного бинарника.

**Контракт владельцев из [direct](https://github.com/docsforadobe/javascript-tools-guide/blob/ac6839049e17f4652d301e7d28f8f0d3d5fbb66a/docs/integrating-external-libraries/defining-entry-points-for-direct-access.md)
и [indirect](https://github.com/docsforadobe/javascript-tools-guide/blob/ac6839049e17f4652d301e7d28f8f0d3d5fbb66a/docs/integrating-external-libraries/defining-entry-points-for-indirect-access.md) guide — DOCUMENTED, без восстановления C ABI:**

| Ресурс/вызов | Существенная обязанность |
|---|---|
| Direct entry points | C exports; имя и преобразование аргументов согласованы с библиотекой |
| Возвращённая строка | UTF-8 с NUL; библиотечный `ESFreeMem` освобождает возвращённую память |
| Tagged data | Инициализация/освобождение через соответствующий server interface; обычный `free` не подставлять |
| Object interface | Обязательные `initialize`/`finalize`; client data живут с объектом |
| Server interface | Сохранить контекст между init и term; после termination не использовать |
| Live object | Теги с release и без release имеют разную передачу владения |
| Script result | `kTypeScript` исполняет возвращённый текст; это путь выполнения кода |

**Проектное решение.** Выбирать известный библиотечный артефакт, фиксировать платформу,
архитектуру и версию протокола. Инициализировать одного владельца библиотеки, затем допускать команды.
Остановить выдачу новых команд → завершить активные callbacks → освободить зависимые
объекты по библиотечному контракту → только после этого выполнять согласованное
завершение библиотеки. Входные данные и ответ использовать как данные; идентификатор
объекта не превращать в сырой C++ pointer. Длительную native работу отдельно
согласовать с правилами вызова AE API.

**Пробел источника.** Примеры зовут `unload()`, справочник описывает `terminate()`;
их взаимозаменяемость не установлена. Direct termination prose ошибочно ссылается
на `ESInitialize`; тот же документ отдельно описывает `ESTerminate`. У indirect
`getClientData` и `taggedDataFree` стоят скопированные декларации `setClientData`.
Поэтому здесь нет универсального unload-helper, объявления `TaggedData` или
придуманных export signatures. [CS4/VS2005/Xcode2.4 sample route](https://github.com/docsforadobe/javascript-tools-guide/blob/ac6839049e17f4652d301e7d28f8f0d3d5fbb66a/docs/integrating-external-libraries/index.md)
не устанавливает ABI современной сборки. Для конкретной библиотеки нужен её
точный SDK/публичный interface; SDK25.6 effect headers не заменяют этот контракт.

## 5. XML/E4X: структура, namespace и сериализация

**DOCUMENTED.** ExtendScript реализует [подмножество E4X](https://github.com/docsforadobe/javascript-tools-guide/blob/ac6839049e17f4652d301e7d28f8f0d3d5fbb66a/docs/integrating-xml/index.md).
[XML/XMLList](https://github.com/docsforadobe/javascript-tools-guide/blob/ac6839049e17f4652d301e7d28f8f0d3d5fbb66a/docs/integrating-xml/the-xml-object.md)
представляют узлы и наборы совпадений. Отсутствие совпадений даёт пустой XMLList;
это отличается от существующего пустого элемента. Присваивание по имени группы
может заменить все одноимённые элементы; индекс адресует один. Namespace выбирается
по URI, а prefix служит его обозначением. `toXMLString()` сохраняет XML-разметку.

[XML reference](https://github.com/docsforadobe/javascript-tools-guide/blob/ac6839049e17f4652d301e7d28f8f0d3d5fbb66a/docs/integrating-xml/xml-object-reference.md)
различает `XML(existing)` как прежний object и `new XML(existing)` как копию.
`XML.settings()`/`setSettings()` читают и восстанавливают общие parser/serialization
options. `children()` включает text nodes; `elements()` выбирает элементы;
`descendants()` проходит глубже. XPath здесь ожидает результат из узлов и может
бросить исключение. `isXMLName()` использует ограниченные правила реализации.

**Сценарий точечной правки.** Ограничить вход → разобрать данные через `new XML(text)`
в `try` → выбрать ожидаемый namespace и набор узлов → проверить его `length()`
и ожидаемую структуру → изменить конкретный узел → сериализовать → повторно
разобрать и сверить нужные значения. Для незнакомой схемы отклонить неоднозначные
совпадения. Если меняются XML settings, сохранить их до операции и восстановить
в `finally`. Присваивание по широкому имени и `delete` всего набора допустимы
только когда удаление всех совпадений входит в план.

Сравнивать ожидаемую структуру и значения, не обещая сохранение исходных пробелов,
порядка attributes или точных байтов. Guide не задаёт лимиты сложности parser;
лимит длины строки не доказывает ограничение памяти/времени для произвольного XML.
Не смешивать XML payload с исполняемым E4X literal, включаемым в строку JSX.
Для JSON нужен совместимый JSON codec и собственная схема; XML/E4X syntax не
переезжает автоматически в CEP, Node или UXP. `eval` не заменяет parser.

## 6. XMP: подготовить metadata packet и отдельно сохранить

**DOCUMENTED.** [AdobeXMPScript](https://github.com/docsforadobe/javascript-tools-guide/blob/ac6839049e17f4652d301e7d28f8f0d3d5fbb66a/docs/scripting-xmp/accessing-the-xmp-scripting-api.md)
загружается через `ExternalObject`; `XMPMeta` работает с metadata packet,
`XMPFile` — с метаданными выбранного файла. Объекты `Thumbnail`/`Metadata` из
Bridge samples не являются объектами AE. [XMPScript reference](https://github.com/docsforadobe/javascript-tools-guide/blob/ac6839049e17f4652d301e7d28f8f0d3d5fbb66a/docs/scripting-xmp/xmpscript-object-reference.md)
задаёт следующие границы:

| Операция | Контракт |
|---|---|
| `getXMP` | Может вернуть `null`; возможна конверсия legacy metadata |
| `getProperty` | Возвращает XMPProperty или `undefined`; значение — `.value` |
| Arrays / localized text | Индексы с 1; языковые альтернативы требуют специальных операций |
| Struct/qualifier paths | Использовать XMPUtils; namespace registration может выбрать другой prefix |
| Iterator | `next()` заканчивается `null`; возможен пропуск поддерева |
| `canPutXMP` → `putXMP` → `closeFile` | Проверка вместимости → отложенные данные → фактическая запись |
| File handler | Smart handler и packet scanner имеют разные возможности |
| Date/serialization | Преобразование в JS Date теряет nanoseconds; формат packet задаётся явно |

**SOURCE EXAMPLE / RUNTIME-NOT-CLAIMED.** Собственная подготовка короткого job-ID
в отдельном namespace. Helper возвращает packet; проекта и внешнего файла он
не сохраняет. Лимит входа — 1,048,576 единиц `String.length`, не байтов. Namespace ниже учебный.

```jsx
function packetWithJobId(packet, jobId) {
    if (typeof packet !== "string" || packet.length > 1024 * 1024 ||
        typeof jobId !== "string" || !/^[A-Za-z0-9._-]{1,64}$/.test(jobId))
        throw new Error("Invalid packet or job ID");
    if (typeof ExternalObject === "undefined")
        throw new Error("ExternalObject is unavailable");
    if (ExternalObject.AdobeXMPScript === undefined)
        ExternalObject.AdobeXMPScript = new ExternalObject("lib:AdobeXMPScript");
    var ns = "urn:example:ae-bible:job:1.0/";
    XMPMeta.registerNamespace(ns, "aeBibleJob");
    var metadata = packet.length ? new XMPMeta(packet) : new XMPMeta();
    metadata.setProperty(ns, "jobId", jobId);
    var updated = metadata.serialize();
    var observed = new XMPMeta(updated).getProperty(ns, "jobId");
    if (!observed || String(observed.value) !== jobId)
        throw new Error("Job ID readback failed");
    return updated;
}
```

**Собственный сценарий сохранения.** Для `app.project.xmpPacket` подготовить результат,
повторно проверить project/job generation и применить через соответствующий
[Project metadata contract](01-OBJECT-MODEL.md); сохранение `.aep` остаётся отдельной
операцией. Для внешнего файла сначала определить формат, политику замены и владельца.
Предпочитать работу с собственной staging-копией, оставляя исходник доступным.
Открыть её с `XMPConst.OPEN_FOR_UPDATE`; режим `OPEN_FOR_READ` не заменяет режим
обновления. Затем `getXMP` → подготовить ограниченный набор изменений разрешённых
полей → `canPutXMP` → `putXMP` → `closeFile`. Пустой результат `getXMP` обработать
по принятой политике создания metadata. [Open/write lifecycle](https://github.com/docsforadobe/javascript-tools-guide/blob/ac6839049e17f4652d301e7d28f8f0d3d5fbb66a/docs/scripting-xmp/xmpscript-object-reference.md#L315-L433).
Невозможность размещения данных является отдельным отказом; не пропускать её молча.
Успех сообщать после завершения записи и независимой проверки результата.

Владелец handle обязан завершить его жизненный цикл и при исключении. Cleanup после
передачи обновлений может записать их: не считать его rollback. Сохранять отдельно
primary failure и failure закрытия; при неизвестном состоянии не повторять запись
в исходник автоматически. Для требуемой crash safety выбрать поддерживаемый
`CLOSE_UPDATE_SAFELY`; это не общий transaction для нескольких файлов/проекта.
Пример не выгружает общую AdobeXMPScript библиотеку после каждого вызова.

**Граница источника.** В batch sample встречается `UNKNOWN`, в таблице — `FILE_UNKNOWN`;
у `appendArrayItem` расходится порядок аргументов, а тип `getLocalizedText` описан
неодинаково. Сложные writer-вызовы по этим образцам не реконструируются.
Наличие file-format constant не доказывает возможности установленного handler.
Общая функция слияния/удаления metadata требует отдельного плана по namespace,
полям и языковым значениям; сериализация одного изменённого поля не подтверждает
сохранение всех остальных семантических свойств packet.

## 7. Отладка: текущий Adobe V2 и исторический ESTK

**DOCUMENTED, официальный [Adobe ExtendScript Debugger V2 README](https://marketplace.visualstudio.com/items?itemName=Adobe.extendscript-debug), проверено 2026-10-08.**
Для разового script использовать `launch`; для ScriptUI/CEP callbacks — `attach`,
затем запускать команду отдельно. Host запускается заранее. Specifier выбирать
из фактического списка; V2 использует `hostAppSpecifier`, `script`, `engineName`
и игнорирует `#target`/`#targetengine`. В `launch`-конфигурации заданный `script`
исполняет сохранённый файл; без него используется содержимое активного редактора.
`attach` сам скрипт не запускает.

**SOURCE EXAMPLE.** Собственная минимальная конфигурация оставляет выбор host/engine
интерфейсу debugger:

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "type": "extendscript-debug",
      "request": "attach",
      "name": "Attach to AE script engine"
    }
  ]
}
```

Adobe отдельно указывает для AE CEP engine `main` и необходимость `$.level = 1`
в отлаживаемом callback. Это источник поведения, не наш наблюдённый результат.
При disconnect вычисление продолжается; оставшиеся `debugger`/`$.bp()` могут
снова остановить его. Использовать одного владельца отладки на host. Не выводить
raw binary в Console: README описывает нарушение debugger protocol.
V2 не включает profiler, OMV viewer и autocomplete; raw OMV dictionary получить
можно. Batch exporter называется `public-scripts/exportToJSXBin.js`.
Windows ARM в README указан как неподдерживаемый.

**Проектное решение.** Воспроизведение хранит версии host/debugger, способ загрузки,
путь фактического JSX и входные данные. Перед остановкой выбирать безопасную копию
проекта; Watch/Console выражения делать без изменений состояния. Логировать краткие
идентификаторы и размеры, а bytes показывать ограниченным текстовым представлением.
Остановка debugger не доказывает откат незавершённой команды.

### Как читать старые ESTK страницы

[Официальный Adobe ESTK Readme](https://github.com/Adobe-CEP/CEP-Resources/blob/ab5e4e3e53a42fad08e1225a22a991bb1ffe73f6/ExtendScript-Toolkit/Readme.md)
описывает ESTK как 32-bit приложение, не работающее на macOS 10.15+; это архивный
маршрут. Полностью прочитанные исторические страницы полезны для понимания механики:

| Раздел guide | Что переносится в практику |
|---|---|
| [Debugging](https://github.com/docsforadobe/javascript-tools-guide/blob/ac6839049e17f4652d301e7d28f8f0d3d5fbb66a/docs/extendscript-toolkit/debugging-in-the-toolkit.md) | Engine ESTK отличается от engine приложения; выбранный stack frame меняет контекст Console/данных |
| [Profiling](https://github.com/docsforadobe/javascript-tools-guide/blob/ac6839049e17f4652d301e7d28f8f0d3d5fbb66a/docs/extendscript-toolkit/code-profiling-for-optimization.md) | Инструментация замедляет выполнение; микросекунды отображения не равны точности таймера |
| [Object models](https://github.com/docsforadobe/javascript-tools-guide/blob/ac6839049e17f4652d301e7d28f8f0d3d5fbb66a/docs/extendscript-toolkit/inspecting-object-models.md) | Dictionary зависит от загруженного приложения и подсистемы |
| [Selecting scripts](https://github.com/docsforadobe/javascript-tools-guide/blob/ac6839049e17f4652d301e7d28f8f0d3d5fbb66a/docs/extendscript-toolkit/selecting-scripts.md) | Double-click может исполнять JSX; Favorites являются настройкой редактора |
| [Workspace](https://github.com/docsforadobe/javascript-tools-guide/blob/ac6839049e17f4652d301e7d28f8f0d3d5fbb66a/docs/extendscript-toolkit/configuring-the-toolkit-window.md) | Сохранённый layout/selection документов не означает сохранение состояния host |
| [Editor](https://github.com/docsforadobe/javascript-tools-guide/blob/ac6839049e17f4652d301e7d28f8f0d3d5fbb66a/docs/extendscript-toolkit/the-script-editor.md) | Syntax check, completion и build comment решают разные задачи; ни один не проверяет результат AE operation |

Общее обещание или субъективная оценка из [mirror debugger overview](https://github.com/docsforadobe/javascript-tools-guide/blob/ac6839049e17f4652d301e7d28f8f0d3d5fbb66a/docs/vscode-debugger/index.md)
не заменяют текущий Adobe README. [Mirror feature page](https://github.com/docsforadobe/javascript-tools-guide/blob/ac6839049e17f4652d301e7d28f8f0d3d5fbb66a/docs/vscode-debugger/vscode-extension-features.md)
сохранила старое имя `exportToJSX.js`; его не копировать в новый build script.
Исторические Flash/Bridge примеры и устаревшие платформенные списки остаются
историей соответствующего источника. Установка debugger не меняет язык JSX,
AE API, доступность библиотеки или правила владения данными.

## Evidence boundary

Новые 34 страницы / 6,859 строк имеют отдельные SHA256 и Git blob в общем runtime
[source ledger](../extendscript-runtime-reviewed-2026-10-08.json). Вместе с8
File/Folder/runtime и31 ScriptUI/BridgeTalk страницами он покрывает все73 страницы
[точного inventory](../extendscript-runtime-inventory-2026-10-08.json).
Индексные страницы описывают навигацию и provenance, а не новые API.
Готовность этой главы — проверенные источники, операции и явно названные пробелы.
Она не заявляет host/network/library execution, современную ABI-совместимость
исторических C interfaces или полную матрицу приложений/операционных систем.
