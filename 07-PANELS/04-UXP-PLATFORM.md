# UXP platform: lifecycle, UI, файлы, сеть и доставка

Область этого раздела — **DOCUMENTED shared UXP / RUNTIME-NOT-CLAIMED**.
Сверка 2026-10-08: AdobeDocs/uxp-hub `ea508323293acd250a2058c92410e0df7a3a50b0`;
AE-specific docs `7d1cd01b4c69a9e02b77d48b3f919a6145a90841`.
Оба commit оставались последними в default branch при проверке.
Операции проекта, Undo и DeferredCall описаны в [AE host API](03-UXP-HOST-API.md);
здесь они не превращаются в обычные browser/Promise APIs.

[Source ledger](../uxp-platform-reviewed-2026-10-08.json):47 полных Hub страниц
и5 AE setup/site файлов; повторные manifest/localStorage/changelog записи объединены.
Покрыты выбранные операции, не весь UXP Hub. Пример экспорта ниже проверяется
[переносимыми failure-path cases](../scripts/test_document_file_examples.js)
с doubles; это не выполнение picker, UXP I/O или AE.

## Что известно об AE setup

AE [Get Started][ae-start] прямо оставлен под будущую инструкцию команды AE,
а [Quickstart на landing][ae-landing] ведёт на общую developer.adobe.com.
В полном дереве закреплённого AE repo нет отдельного tutorial, plugin manifest,
starter или host changelog. README этого repo объясняет запуск сайта документации,
а не загрузку плагина в AE. Это конкретный пробел опубликованных источников.
[AE source tree][ae-tree], [README][ae-readme].

Shared [HostDefinition][manifest] перечисляет `PS`, `ID`, `premierepro`, `ame`.
[Первый плагин][first-plugin] предлагает starters этих четырёх hosts.
[Таблица host ↔ UXP][runtime-versions] содержит Photoshop, Premiere и InDesign,
но не AE. Поэтому `MinVersion 27.0` в AE API не определяет `host.app`, версию UXP,
минимальный UDT, включение Developer Mode в AE или Marketplace eligibility.
Устанавливаемый AE manifest и фактическая beta/GA здесь не заявлены;
даты rollout остаются в [отдельном обзоре перехода](02-UXP-TRANSITION.md).

Практическая рекомендация: хранить раздельно AE build, UXP runtime, manifest schema,
UDT, версию плагина и выбранный канал доставки. Shared API предоставляет
`require("uxp").host.name/version/uiLocale` и
`require("uxp").versions.uxp/plugin` для диагностики в уже поддерживаемом host;
прочитанное имя host не является документированным значением `manifest.host.app`.
[Host info][host-info], [Versions][versions].

## Entrypoints: регистрация и время жизни

Command — отдельное действие без постоянной панели; panel — сохраняющийся UI.
Оба могут открывать modal dialog, который блокирует взаимодействие с host.
Один plugin может объявить несколько entrypoints обоих типов.
[Panels and Commands][components].

Manifest объявляет `entrypoints`; ключи `commands` и `panels` в
`require("uxp").entrypoints.setup(...)` должны совпасть с их IDs.
`setup` вызывается один раз: повтор или некорректные данные вызывают exception.
Если задан `plugin` object, reference требует `create`; объект panel должен
определить `create` или `show`, объект command — `run`.
`getPanel(id)` и `getCommand(id)` возвращают `null` для неизвестного ID.
[Entrypoints reference][entry-api].

| Hook | Значение в shared guide | Рекомендуемая ответственность продукта |
|---|---|---|
| `plugin.create()` | Создание plugin container | Инициализировать общие сервисы один раз |
| `plugin.destroy()` | Завершение container | Прекратить новые задачи, быстро освободить оставшиеся собственные ресурсы |
| `panel.create(rootNode)` | Создание panel | Создать принадлежащий этой панели DOM/container |
| `panel.show(rootNode, data)` | Показ panel | Идемпотентно подключить UI и обновить отображаемое состояние |
| `panel.hide(rootNode, data)` | Скрытие panel | Приостановить необязательные обновления, если callback поступил |
| `panel.destroy(rootNode)` | Уничтожение panel | Отсоединить собственные listeners/container, если callback поступил |

В manifest v5 guide разрешает Promise из `plugin.destroy` и panel
`create/show/hide/destroy`, указывает timeout **300 ms** и текущую связь
`show` с `create`, `hide` с `destroy`. Формула «destroy всегда synchronous» неверна.
Но это также не разрешение ждать неопределённо долго: поддержка Promise не отменяет
лимит и host-specific поведение. `plugin.create` в этом перечне async hooks нет.
[Entrypoints guide][entry-guide].

Shared how-to предупреждает: `hide/destroy` ненадёжны в некоторых hosts;
для нескольких panels callbacks могут приходить всем панелям без различения
инициатора. Поэтому гарантированное завершение работы нельзя строить на одном
событии закрытия. Пример проблемы назван для Premiere; поведение AE из него
не выводится. [Lifecycle limitations][hooks].

Есть и несогласованность command contract: guide показывает `uxpcommand` event,
а reference для v5 описывает `run(executionContext, ...arguments)`.
Reference оставляет `commands.cancel` для будущего использования, хотя
[migration guide][migration] описывает cancel callback как действующий.
Не объявлять этот callback рабочим механизмом отмены AE и не переносить payload
из другого host; использовать конкретный подтверждённый command contract.

## Ownership: собственные ресурсы и сохранение состояния

В [multi-panel guide][panels] панели одного HTML document разделяют JavaScript
context; DOM wrapper ID и manifest entrypoint ID — разные идентификаторы.
Обмен данными внутри этого context не требует IPC. Показ другой панели через
Plugin Manager в примере требует IPC permission; API закрытия панели эта страница
не предоставляет. Возможность открыть panel не доказывает полный window manager API.

**Авторская схема ownership:** общий controller владеет общими сервисами,
каждый panel controller — своим container, подписками и отложенными UI-задачами.
Один panel callback не должен освобождать ресурс, которым ещё пользуется другой UI.
Не сохранять runtime rootNode/host object в состояние, переживающее reload.

| Ресурс продукта | Что хранить у владельца | Как завершать |
|---|---|---|
| DOM listener | Target, event name, исходный callback, capture | Явно снять тот же callback |
| Таймер/планировщик | Handle и соответствующую функцию отмены runtime-адаптера | Отменить следующее выполнение; callback проверяет актуальность владельца |
| Собственная подписка | Полученный от конкретного API способ отписки | Выполнить его один раз; не выдумывать универсальный `dispose` для host objects |
| Async UI request | Generation владельца и идентичность запроса | Запретить устаревшему результату менять UI; обработать поздний reject |
| Общий сервис | Явных потребителей и владельца завершения | Завершить после освобождения зависимых ресурсов |

Shared `EventTarget` документирует `addEventListener/removeEventListener`;
из options object заявлен только `capture`. Browser-паттерны `once`, `passive`
или автоматическая отписка через `signal` отсюда не следуют.
[EventTarget][event-target].

**Авторский workflow:** сначала отметить controller неактивным и увеличить generation,
потом снять listeners/таймеры, затем отсоединить принадлежащий ему DOM. Все операции
завершения повторяемы и допустимы после частичной инициализации. Ошибка снятия одной
подписки не должна мешать попытке снять остальные; первичную ошибку операции сохранять
отдельно от ошибки очистки. Этот путь вызывается и при управляемой остановке/ошибке,
а lifecycle callbacks дополнительно используют его, когда host их доставляет.
Ресурсы одной операции освобождать в её собственном `finally`, не держать их до
закрытия панели. Быструю синхронную часть очистки выполнять сразу; длительную запись
на диск или сетевой запрос завершения не делать единственной копией важного состояния.

Сохранять настройки по мере подтверждения пользователем, а не впервые в `destroy`.
Разделять plain UI preferences, временное состояние запроса и истину AE project.
Для сериализации задать schemaVersion, разрешённые поля и defaults; после загрузки
проверять JSON и мигрировать поддерживаемые версии. При повреждении UI preferences
показать defaults, сохранив объяснимый статус; неизвестная будущая schema не должна
молча перезаписываться старой. Не возобновлять мутацию только потому, что на диске
осталось `busy: true`. Повторно прочитать host state и применить обычную проверку цели.

Выбор localStorage/sessionStorage/SecureStorage, форматы и ошибки описаны в
разделе о файлах и хранилищах ниже. Сохранение настроек и завершение UI имеют
разные обязанности; одно не гарантирует другое.

## UI: события, клавиатура, тема и размеры

Shared guide разделяет встроенные **Spectrum UXP Widgets**, устанавливаемые
**Spectrum Web Components** и поддерживаемые HTML elements. Для SWC нужны установка,
imports, bundling и `enableSWCSupport`; пример pin `0.37.0` прямо относится к Premiere.
UXP реализует часть browser APIs. Это не основание переносить любой компонент или
версию framework в AE. [UI guide][ui].

`addEventListener` в JS позволяет обойтись без inline HTML handlers; для последних
источник требует `allowCodeGenerationFromStrings`. `input/change`, `focus/blur` и
`keydown/keyup` входят в shared event guide. [HTML events][events].
KeyboardEvent reference перечисляет `key`, `code`, modifiers, `repeat`,
`preventDefault/stopPropagation`. Это локальное событие; оно не документирует
перехват глобальных AE shortcuts. [KeyboardEvent][keyboard].

Manifest shortcuts зависят от host; конфликтующее сочетание игнорируется с warning.
Желаемые panel sizes host может не соблюсти. [Manifest][manifest].
CSS recipe использует `document.theme.getCurrent()` / `onUpdated` **для Premiere**,
а наличие `--uxp-host-*` variables предлагает проверять отдельно. Его тема/событие
не являются AE API. [CSS recipe][css].

**Рекомендации для UI продукта:** оставлять путь к действию через видимые controls,
сохранять предсказуемый Tab/focus порядок и не отправлять повторную мутацию от
удерживаемой клавиши. Перехватывать только действительно обработанное сочетание
в принадлежащем панели UI. Отображать busy/error/empty как разные состояния;
после async операции возвращать focus логически, если прежний control ещё существует.
Проверять исходную тему и её изменение в документированном host-адаптере;
при отсутствии данных использовать читаемую собственную палитру. Размеры layout
должны выдерживать узкую docked panel, локализованные подписи и масштабирование.

## Manifest и developer workflow

`manifest.json` находится в корне bundle. Stable plugin ID, версия `major.minor.patch`,
host range и entrypoint IDs — независимые данные. В таблице `manifestVersion`
указан string, в примере — число `5`; расхождение сохраняем, AE schema не угадываем.
Не смешивать product version с UXP runtime или API member MinVersion.
[Manifest][manifest].

Для поддерживаемого host shared tutorial описывает: установить UDT, включить
Developer Mode, создать project, запустить host, выбрать Load & Watch.
Изменение manifest требует **Unload → Load**, обычный source reload его не обновляет.
[Tools][dev-tools], [First plugin][first-plugin].

При bundler-based сборке UDT может хранить ссылку на source manifest и отдельно путь
к generated directory; это помогает, если сборка удаляет и создаёт output заново.
Нужны два наблюдателя: build watcher создаёт bundle, UDT загружает его изменения.
UDT сам не устанавливает npm dependencies. [UDT workflows][udt-workflow].

**Рекомендация:** завершать модульную регистрацию один раз за plugin context;
повторный show запускает refresh, а не новый `entrypoints.setup`. Проектировать
reload как восстановление из plain preferences и нового host snapshot. Для AE
следующий source-dependent шаг — опубликованная инструкция с host ID, build/UDT
совместимостью и активацией; наличия API reference для него недостаточно.

## CCX, каналы обновления и installed state

Shared packaging использует UDT **Actions → Package**, `.ccx` и один host object.
При development host array UDT выбирает первый host при упаковке. Package-level
CEP signature/timestamp для CCX не нужны; это не снимает требований с native addons.
ID остаётся стабильным при обновлении в одном канале. При одновременной Marketplace
и внешней доставке нужны разные IDs: Marketplace entitlement может иначе блокировать
внешнюю установку. [Package][package].

| Канал | Опубликованный общий путь | Кто управляет продолжением |
|---|---|---|
| Marketplace | Portal listing, CCX, Adobe review; новая версия добавляется к listing | Creative Cloud Desktop доставляет версии; публикация после review бывает автоматической или ручной |
| Independent | Раздача CCX через собственный сайт/release/store | Издатель управляет доступностью, обновлениями и поддержкой |
| Enterprise | Admin Console/managed package/UPIA | Администратор задаёт политику установки и обновлений |

[Marketplace][marketplace], [Listing][listing], [Outside Marketplace][outside],
[Enterprise][enterprise]. Успешная установка managed package в целом не гарантирует
установку каждого plugin: enterprise guide прямо допускает отдельный plugin failure.
Его status и activation после требуемого restart учитывать отдельно.

CC Desktop устанавливает внешний CCX по double-click и показывает permissions.
End-user install не требует developer workflow. `Disable` сохраняет установку,
`Uninstall` удаляет package. Marketplace listing может остаться в Manage Plugins
из-за права переустановки; это не доказательство наличия установленной версии.
[Install][install].

**Авторская политика обновления:** связывать package hash, ID, host target, версию,
канал и settings schema в release record. Разные IDs могут означать разные context
и storage; перенос пользовательских настроек должен быть явной процедурой продукта,
а не обещанием CCX. Сохранять прежний package и описывать границу downgrade settings.
Отдельно обозначать состояние «скачан», «установлен», «включён», «доступен в host».
Упаковка не доказывает ни AE discovery, ни Marketplace eligibility.
Общая политика артефактов — [Distribution](../11-DISTRIBUTION/05-RELEASE-ARTIFACTS-UPDATES.md).

## Версионные расхождения shared docs

Shared changelog не совпадает с универсальной manifest-таблицей во всех версиях:
в UXP 9.0 `webview.domains` стал optional, в 9.1 поле `allow` перестало использоваться;
manifest reference продолжает перечислять оба как required. Changelog 8.1 также
говорит о default `enableFillAsCustomAttribute: true`, тогда как manifest даёт false.
Выбирать конфигурацию по реально целевой версии UXP и её host constraints;
не превращать старую таблицу или newest changelog в контракт любого AE build.
[Changelog][changelog], [Manifest][manifest].

Этот раздел закрывает выбранные опубликованные shared lifecycle/UI/workflow contracts.
AE-specific setup, распределение конкретного AE build по UXP versions и host-only
ограничения остаются явно обозначенными границами источников. Выполнение внутри AE,
установка и публикация продукта здесь не заявлены.

## Файлы, сохранённый доступ и сеть — shared UXP review 2026-10-08

Основание: полностью прочитанные страницы официального
[AdobeDocs/uxp-hub](https://github.com/AdobeDocs/uxp-hub/tree/ea508323293acd250a2058c92410e0df7a3a50b0),
pin `ea508323293acd250a2058c92410e0df7a3a50b0`. Это **общая платформа UXP**;
поддержка конкретной AE-установкой и преобразование Entry в аргумент AE DOM здесь
не проверены. Evidence: DOCUMENTED / SOURCE EXAMPLE / RUNTIME-NOT-CLAIMED.

Общие [prerequisites](https://github.com/AdobeDocs/uxp-hub/blob/ea508323293acd250a2058c92410e0df7a3a50b0/src/pages/guides/how-to/recipes/_shared/prerequisites.md)
называют UDT2.2, manifest5 и Premiere25.6; для остальных hosts требуют собственной
проверки. Это не основание назначить такой же minimum After Effects.

### Выбрать место хранения и permission

По [filesystem recipe](https://github.com/AdobeDocs/uxp-hub/blob/ea508323293acd250a2058c92410e0df7a3a50b0/src/pages/guides/how-to/recipes/filesystem-operations/index.md):

| Область | Доступ и назначение |
|---|---|
| Plugin folder, `plugin:/` | Read-only: упакованные ресурсы |
| Data folder, `plugin-data:/` | Сохраняется при обновлении приложения; удаление плагина/очистка данных могут её удалить |
| Temporary folder, `plugin-temp:/` | Временные данные; не место для единственной копии результата |
| Выбранный пользователем File/Folder | Entry для согласованного внешнего места |
| Произвольный `file:/...` | Требуется `fullAccess`; ограничения ОС всё равно действуют |

`getPluginFolder/getDataFolder/getTemporaryFolder` возвращают соответствующие
Folder. Не записывать project assets в plugin folder и не считать data folder
резервной копией пользователя. `require("fs")` опубликован как отдельный path API,
похожий на Node, но это не полная Node-совместимость и не `localFileSystem`.
Здесь операции используют Entry API; полный `fs` contract не объявлен проверенным.

[Manifest][manifest]: `localFileSystem` по умолчанию `"plugin"`; внешний выбор
требует `"request"`, доступ без выбора — `"fullAccess"`. Сеть задаётся отдельно
в `requiredPermissions.network.domains`. Строка пути не заменяет permissions.

Для примера экспорта ниже достаточно **фрагмента** manifest:

```json
{
  "requiredPermissions": {
    "localFileSystem": "request"
  }
}
```

Это не полный installable manifest: host ID, entrypoint и поддерживаемая версия
задаются отдельным подтверждённым setup конкретного приложения.

### Получение Entry и восстановление доступа

Источник: [FileSystemProvider](https://github.com/AdobeDocs/uxp-hub/blob/ea508323293acd250a2058c92410e0df7a3a50b0/src/pages/uxp-api/reference-js/modules/uxp/persistent-file-storage/file-system-provider.md).
Получать provider через `require("uxp").storage.localFileSystem`, не через новый класс.

`getFileForOpening` даёт read-only File; при `allowMultiple:true` — массив.
Отмена означает пустой результат, для множественного выбора — пустой массив.
`getFileForSaving` даёт read-write File или null; picker отдельно подтверждает
перезапись. `getFolder` возвращает Folder/null, дети выбранной папки доступны
для read-write. `initialLocation` перекрывает `initialDomain`.

| Токен | Создание | Восстановление | Граница |
|---|---|---|---|
| Session | `createSessionToken(entry)` → string | `getEntryForSessionToken(token)` → Entry | Только текущая сессия плагина |
| Persistent | `await createPersistentToken(entry)` | `await getEntryForPersistentToken(token)` | Может перестать работать после перемещения, смены прав и ограничений ОС |

Успешное восстановление Entry не гарантирует успешное чтение/запись. Рекомендуемая
операция: восстановить → проверить роль File/Folder → выполнить чтение → проверить
схему. При отказе предложить новый выбор; отмена завершает команду. Новый токен
сохранить под **тем же ключом** только после проверки выбранного файла. Не запускать
цикл навязчивых picker-повторов.

`getNativePath/getFsUrl` возвращают разные строковые представления. Session token,
persistent token, Entry, URL и native path нельзя взаимозаменять. Photoshop-пример
`batchPlay` не определяет формат аргумента AE. Получение через `getEntryWithUrl`
не создаёт файл и не обходит permissions; `createEntryWithUrl` требует существующего
родителя, а file-entry становится файлом на диске только при записи.

### Entry, Folder и операция над содержимым

[Entry](https://github.com/AdobeDocs/uxp-hub/blob/ea508323293acd250a2058c92410e0df7a3a50b0/src/pages/uxp-api/reference-js/modules/uxp/persistent-file-storage/entry.md)
публикует read-only имя, provider, URL и nativePath. `copyTo` возвращает новый
File/Folder; `moveTo` — Promise<void>. По умолчанию они не разрешают overwrite;
копирование папки требует отдельного `allowFolderCopy`. Это действия над диском,
не project Undo. `delete()` успешен с результатом **0**, а не true; папка должна
быть пустой. Источник отдельно предупреждает об отказе удаления папки, выбранной
picker или drag-and-drop. Не строить rollback через удаление такой папки.

[Folder](https://github.com/AdobeDocs/uxp-hub/blob/ea508323293acd250a2058c92410e0df7a3a50b0/src/pages/uxp-api/reference-js/modules/uxp/persistent-file-storage/folder.md):
`getEntries()` — Promise массива непосредственных детей; `getEntry(path)` получает
File/Folder. `createFile` создаёт Entry, реальная запись выполняется `write`.
`createFolder` создаёт папку; `renameEntry` возвращает Promise<void>. Source-example
ошибочно вызывает `.rename()`, поэтому использовать имя из заголовка метода.
Для folders предпочесть `createFolder`: описание `createEntry` смешивает Symbol
и класс Folder, хотя пример использует `types.folder`.

Рекомендуемый batch-export: согласовать папку и политику конфликтов имён →
подготовить весь список → создавать и записывать файлы по одному → вести перечень
проверенных, частичных и не начатых результатов. При ошибке не удалять папку целиком.
`overwrite:true` — явное разрешение замены, а не исправление любой ошибки доступа.
Эти страницы не обещают атомарность rename/replace, flush/fsync или восстановление
после отключения питания; такую гарантию нельзя получить добавлением `await`.

### Форматы чтения и записи

[File](https://github.com/AdobeDocs/uxp-hub/blob/ea508323293acd250a2058c92410e0df7a3a50b0/src/pages/uxp-api/reference-js/modules/uxp/persistent-file-storage/file.md)
получают через provider/folder, не `new File(...)`. `isFile` и `mode` помогают
проверить роль и read-only состояние. `read` возвращает Promise<string|ArrayBuffer>,
`write` — Promise<number> с длиной записанного содержимого. Это не boolean-методы.
Не сравнивать результат UTF-8 записи с JavaScript `string.length` как универсальным
числом байтов: единица возвращаемой длины здесь не уточнена.

[formats](https://github.com/AdobeDocs/uxp-hub/blob/ea508323293acd250a2058c92410e0df7a3a50b0/src/pages/uxp-api/reference-js/modules/uxp/persistent-file-storage/formats.md)
содержит Symbols `utf8` и `binary`. Передавать `format:formats.utf8` для текста,
`format:formats.binary` для ArrayBuffer; по умолчанию UTF-8. `append` по умолчанию
false. Типизированное представление части буфера не равно всему его `.buffer`:
если исходные bytes занимают лишь срез, перед записью выделить ровно этот диапазон.
Read-only и нехватка места/квоты дают ошибки.

[EntryMetadata](https://github.com/AdobeDocs/uxp-hub/blob/ea508323293acd250a2058c92410e0df7a3a50b0/src/pages/uxp-api/reference-js/modules/uxp/persistent-file-storage/entry-metadata.md)
получать через `await entry.getMetadata()`: имя, size, даты, тип. У папки size=0;
это не размер дерева. Метаданные — предварительная проверка, не блокировка файла
и не подтверждение, что содержимое осталось прежним. `File.read()` читает целиком;
проверка `ArrayBuffer.byteLength` после чтения ограничивает принимаемый результат,
но не предотвращает уже выполненную загрузку большого файла.

### SOURCE EXAMPLE: экспорт небольшого JSON с проверкой прочитанного

Ниже собственная схема preset: label до 80 JavaScript code units и strength0..1.
Это ограничения примера, не диапазоны AE API. Вызывать из обработчика осознанной
команды в поддерживаемом plugin runtime; UI должен исключать параллельные запуски.

```javascript
const { localFileSystem, formats } = require("uxp").storage;

async function exportPreset(label, strength) {
  if (typeof label !== "string" || label.length > 80 ||
      !Number.isFinite(strength) || strength < 0 || strength > 1) {
    throw new TypeError("Invalid preset fields");
  }
  const text = JSON.stringify({ schema: 1, label, strength });
  let phase = "selecting";
  try {
    const file = await localFileSystem.getFileForSaving("preset.json", {
      types: ["json"]
    });
    if (!file) return { status: "cancelled" };

    phase = "write_attempted";
    await file.write(text, { format: formats.utf8, append: false });
    phase = "written";
    const actual = await file.read({ format: formats.utf8 });
    if (actual !== text) throw new Error("Readback mismatch");
    return { status: "verified", name: file.name };
  } catch (error) {
    const status = phase === "selecting" ? "acquire_failed" :
      phase === "write_attempted" ? "write_outcome_unknown" :
      "written_unverified";
    return { status, error: String(error) };
  }
}
```

`verified` здесь означает совпадение немедленно прочитанного текста. Это не
crash-safe commit, импорт preset в AE или гарантия будущей сохранности. При
неизвестном результате записи файл мог измениться; пример не удаляет его и не
повторяет overwrite автоматически. Picker-cancel, acquisition failure и ошибка
после записи различимы. В Bible этот код не запускался в host.

### Локальные настройки, session state и SecureStorage

[localStorage](https://github.com/AdobeDocs/uxp-hub/blob/ea508323293acd250a2058c92410e0df7a3a50b0/src/pages/uxp-api/reference-js/global-members/data-storage/local-storage.md)
синхронен: `getItem` даёт string/null, `setItem` принимает string и может бросить
ошибку. `removeItem` допускает отсутствующий ключ; `clear` очищает весь store.
Сохранять версионированные данные под собственными ключами, проверять JSON-схему
при чтении, не сбрасывать все настройки из-за одного повреждённого значения.
Store может быть очищен, поэтому это восстановимые настройки, не единственная
копия проекта. Пароли туда не помещать.

[sessionStorage](https://github.com/AdobeDocs/uxp-hub/blob/ea508323293acd250a2058c92410e0df7a3a50b0/src/pages/uxp-api/reference-js/global-members/data-storage/session-storage.md)
использует API localStorage, но только на текущую сессию плагина. Его сохранение
не превращает Session token в Persistent token и не обеспечивает resume после
unload.

[SecureStorage](https://github.com/AdobeDocs/uxp-hub/blob/ea508323293acd250a2058c92410e0df7a3a50b0/src/pages/uxp-api/reference-js/modules/uxp/key-value-storage/secure-storage.md)
шифрует **значения, не имена ключей**, под учётной записью текущего пользователя.
Это не защита секрета от самого пользователя и не бессрочное хранилище.
Содержимое может быть потеряно; приложение должно уметь восстановить авторизацию.

`await setItem(key,value)` принимает string/ArrayBuffer/TypedArray и возвращает
void; `await getItem(key)` возвращает **Uint8Array**, не исходную строку.
Использовать явный проверенный codec; `.toString()` массива не является UTF-8
декодированием. Не переносить туда предположение о глобальном TextDecoder.
Удалять только собственный ключ через `removeItem`, а не `clear` всех секретов.
`key(index)` в таблице объявлен number, хотя остальные методы используют string:
для операции с известным ключом enumeration не нужна.

Есть версионное расхождение: страница обещает rejection при отсутствии удаляемого
ключа/пустом clear, а [changelog UXP9.0](https://github.com/AdobeDocs/uxp-hub/blob/ea508323293acd250a2058c92410e0df7a3a50b0/src/pages/uxp-api/changelog.md#L77-L87)
сообщает переход error handling к Web Storage spec. Не определять «ключ отсутствует»
по произвольному catch или тексту ошибки; отдельно квалифицировать выбранный runtime.

### HTTP: permission, cookies, результат и тело

Источник [fetch](https://github.com/AdobeDocs/uxp-hub/blob/ea508323293acd250a2058c92410e0df7a3a50b0/src/pages/uxp-api/reference-js/global-members/data-transfers/fetch.md):
глобальная функция возвращает Promise<Response>. GET/HEAD с body недопустимы.
Network/timeout и проблемы чтения FormData могут дать TypeError: он не доказывает
одну конкретную причину. `credentials` по умолчанию **include**; для публичного
каталога явно выбирать `omit`. Токены авторизации и пользовательские данные не
передавать endpoint, выбранному произвольным ответом сервера.

Пример permission в fetch-page использует старое поле `permissions`; текущий
manifest и [network recipe](https://github.com/AdobeDocs/uxp-hub/blob/ea508323293acd250a2058c92410e0df7a3a50b0/src/pages/guides/how-to/recipes/network/index.md)
используют **requiredPermissions**. Нужны точные HTTPS origins, а не `domains:"all"`.
С UXP7.4 wildcard в top-level domain запрещён. Network permission также относится
к удалённым изображениям, но не заменяет самостоятельные permissions webview.

[Headers](https://github.com/AdobeDocs/uxp-hub/blob/ea508323293acd250a2058c92410e0df7a3a50b0/src/pages/uxp-api/reference-js/global-members/data-transfers/headers.md)
принимает Object со строковыми значениями, пары или другой Headers; `get` даёт
string/null, хотя таблица возврата не отражает null. `set` заменяет значение,
`append` добавляет; не дублировать Authorization через append. Заголовок страницы
`windows.Headers` — опечатка, не отдельный объект windows.

[Request](https://github.com/AdobeDocs/uxp-hub/blob/ea508323293acd250a2058c92410e0df7a3a50b0/src/pages/uxp-api/reference-js/global-members/data-transfers/request.md)
документирует `new Request(url,{method,headers,credentials,signal})`, а fetch принимает
такой Request. Таблица fetch-init сама не перечисляет signal; его демонстрирует
общий recipe. Request/Response/Headers помечены UXP7.3.0, не AE27.0.

[Response](https://github.com/AdobeDocs/uxp-hub/blob/ea508323293acd250a2058c92410e0df7a3a50b0/src/pages/uxp-api/reference-js/global-members/data-transfers/response.md):
`ok` означает HTTP200..299, `status/statusText` — протокольный результат.
Успешный fetch ещё не означает успешный HTTP-ответ или правильный JSON.
`json/text/arrayBuffer/blob/formData` читают body до конца; `text` декодирует UTF-8.
`bodyUsed` показывает факт чтения, `body` может быть null. Для одной команды
выбирать одного потребителя тела, затем проверять собственную схему результата.
Не пытаться повторно читать body для журнала ошибки; не журналировать credentials
и полное потенциально приватное содержимое. `response.url` отражает URL ответа,
но его поздняя проверка не предотвращает уже выполненную отправку запроса.

Рекомендуемый каталог preset: фиксированный разрешённый endpoint → GET без cookies
→ HTTP-status → ожидаемый Content-Type → ограниченное тело → JSON.parse/схема/version
→ только разрешённые поля в UI. Ответ сети остаётся данными, не JS/HTML для исполнения.
HTTP401, HTTP500, transport failure, parse failure и устаревший UI-result — разные
исходы. Повтор POST после timeout не становится безопасным из-за catch; нужен
самостоятельный серверный контракт идемпотентности.

### Отмена, timeout и размер: три разных ограничения

[AbortController](https://github.com/AdobeDocs/uxp-hub/blob/ea508323293acd250a2058c92410e0df7a3a50b0/src/pages/uxp-api/reference-js/global-members/html-dom/abort-controller.md)
предоставляет signal и `abort(reason)`; без reason используется AbortError.
[AbortSignal](https://github.com/AdobeDocs/uxp-hub/blob/ea508323293acd250a2058c92410e0df7a3a50b0/src/pages/uxp-api/reference-js/global-members/html-dom/abort-signal.md)
публикует `aborted/reason/throwIfAborted` и отдельно ограничивает поддержку web streams.
Request и network-recipe показывают fetch с signal: это документированный pattern,
но не гарантия универсальной отмены любых UXP calls. Не переносить abort на
`File.write`, AE mutations или DeferredCall.

Собственный design команды: отдельный controller на запрос; timeout активен до
окончания чтения body, а не только до headers; в finally убрать timer. Кнопка Cancel
запрашивает abort и помечает результат ненужным для UI. Смена UI-generation запрещает
применять поздний результат, но не отменяет уже выполненную запись/серверное действие.
`Promise.race` с таймером сам по себе не останавливает сеть. Фактическое завершение
и точность deadline требуют отдельной квалификации версии.

Для размера `Content-Length` служит только предварительным фильтром: заголовка
может не быть, а значение не является лимитом памяти. Проверять длину после
`arrayBuffer()` полезно для принятия результата, но всё тело к этому моменту уже
прочитано. Для больших/непредсказуемых ответов нужен streaming adapter и лимит
агрегируемых bytes; лимит одного ответа не равен лимиту внутренних buffers host.

[ReadableStream](https://github.com/AdobeDocs/uxp-hub/blob/ea508323293acd250a2058c92410e0df7a3a50b0/src/pages/uxp-api/reference-js/global-members/streams/readable-stream.md)
публикует `getReader`, который блокирует поток на reader; BYOB не поддержан.
`stream.cancel` отвергает locked stream. `pipeTo/pipeThrough` имеют собственные
signal и preventClose/preventAbort/preventCancel: эти флаги меняют cleanup,
поэтому их нельзя копировать случайно из browser snippet.

[ReadableStreamDefaultReader](https://github.com/AdobeDocs/uxp-hub/blob/ea508323293acd250a2058c92410e0df7a3a50b0/src/pages/uxp-api/reference-js/global-members/streams/readable-stream-default-reader.md)
возвращает из `read()` объект `{value,done}`; closed/error различаются. Рекомендуемый
adapter принимает только ожидаемые byte-chunks, проверяет лимит перед добавлением
каждого chunk, а при отказе запрашивает cancel и отдельно фиксирует cleanup error.
`releaseLock()` не удаляет непрочитанные chunks; pending reads могут получить TypeError.
В описании `reader.cancel` есть несогласованность: reader держит lock по назначению,
но текст обещает отказ при locked stream; возвращаемый тип также указан string.
Не подменять эту границу обещанием безошибочного cleanup.

Network-recipe прямо предупреждает, что TextDecoder отсутствует в описываемом UXP.
Не копировать browser decoder по наличию ReadableStream. Для small JSON использовать
документированный Response.text/json; для streaming-текста нужен отдельно выбранный
совместимый UTF-8 decoder с обработкой разрыва многобайтовой последовательности
между chunks. HTTP/download-progress и AE render-progress — разные процессы.

### Версии, ошибки источников и evidence

[Changelog](https://github.com/AdobeDocs/uxp-hub/blob/ea508323293acd250a2058c92410e0df7a3a50b0/src/pages/uxp-api/changelog.md)
отдельно фиксирует UXP8.2 `fs.createReadStream` и UXP8.4 исправление удаления
Authorization при redirect на другой origin. Это важные границы reader-product;
наличие метода в latest source не переносит исправление на старый host.
Поддержка upload-stream не превращает `File.read` в потоковый метод.

Описания Entry.isFile/isFolder сформулированы через «not», тогда как специализированные
File/Folder и recipe показывают положительные type-флаги. В операциях выбирать
конкретный возвращённый тип, не превращать эти опечатки в новый контракт.

Для продукта, обещающего сохранение preset, нужны сценарии отмены picker, ошибки
доступа, нехватки места, частичной записи и несовпадения readback. Для remembered
access — исчезнувший файл/просроченный token; для авторизации — потерянный store;
для загрузки — HTTP error, неправильная схема, превышение размера и отмена до/во
время чтения body. Это границы продуктовых обещаний, не обязательный host-test
каждого примера Bible. Ни чтение source, ни syntax-check не подтверждают исполнение
в AE или реальную сетевую/файловую операцию.

[ae-start]: https://github.com/AdobeDocs/uxp-after-effects/blob/7d1cd01b4c69a9e02b77d48b3f919a6145a90841/src/pages/get-started/index.md
[ae-landing]: https://github.com/AdobeDocs/uxp-after-effects/blob/7d1cd01b4c69a9e02b77d48b3f919a6145a90841/src/pages/index.md
[ae-tree]: https://github.com/AdobeDocs/uxp-after-effects/tree/7d1cd01b4c69a9e02b77d48b3f919a6145a90841
[ae-readme]: https://github.com/AdobeDocs/uxp-after-effects/blob/7d1cd01b4c69a9e02b77d48b3f919a6145a90841/README.md
[manifest]: https://github.com/AdobeDocs/uxp-hub/blob/ea508323293acd250a2058c92410e0df7a3a50b0/src/pages/guides/explanation/concepts/manifest/index.md
[first-plugin]: https://github.com/AdobeDocs/uxp-hub/blob/ea508323293acd250a2058c92410e0df7a3a50b0/src/pages/guides/tutorials/build-your-first-plugin/index.md
[runtime-versions]: https://github.com/AdobeDocs/uxp-hub/blob/ea508323293acd250a2058c92410e0df7a3a50b0/src/pages/uxp-api/versions.md
[host-info]: https://github.com/AdobeDocs/uxp-hub/blob/ea508323293acd250a2058c92410e0df7a3a50b0/src/pages/uxp-api/reference-js/modules/uxp/host-information/host.md
[versions]: https://github.com/AdobeDocs/uxp-hub/blob/ea508323293acd250a2058c92410e0df7a3a50b0/src/pages/uxp-api/reference-js/modules/uxp/versions/versions.md
[components]: https://github.com/AdobeDocs/uxp-hub/blob/ea508323293acd250a2058c92410e0df7a3a50b0/src/pages/guides/explanation/concepts/panels-and-commands/index.md
[entry-api]: https://github.com/AdobeDocs/uxp-hub/blob/ea508323293acd250a2058c92410e0df7a3a50b0/src/pages/uxp-api/reference-js/modules/uxp/entry-points/entry-points.md
[entry-guide]: https://github.com/AdobeDocs/uxp-hub/blob/ea508323293acd250a2058c92410e0df7a3a50b0/src/pages/guides/explanation/concepts/entrypoints/index.md
[hooks]: https://github.com/AdobeDocs/uxp-hub/blob/ea508323293acd250a2058c92410e0df7a3a50b0/src/pages/guides/how-to/add-lifecycle-hooks/index.md
[migration]: https://github.com/AdobeDocs/uxp-hub/blob/ea508323293acd250a2058c92410e0df7a3a50b0/src/pages/migration-center/uxp-for-cep-devs/technical-migration-guide/index.md
[panels]: https://github.com/AdobeDocs/uxp-hub/blob/ea508323293acd250a2058c92410e0df7a3a50b0/src/pages/guides/how-to/add-panels/index.md
[event-target]: https://github.com/AdobeDocs/uxp-hub/blob/ea508323293acd250a2058c92410e0df7a3a50b0/src/pages/uxp-api/reference-js/global-members/html-events/event-target.md
[local-storage]: https://github.com/AdobeDocs/uxp-hub/blob/ea508323293acd250a2058c92410e0df7a3a50b0/src/pages/uxp-api/reference-js/global-members/data-storage/local-storage.md
[ui]: https://github.com/AdobeDocs/uxp-hub/blob/ea508323293acd250a2058c92410e0df7a3a50b0/src/pages/guides/explanation/fundamentals/user-interfaces/index.md
[events]: https://github.com/AdobeDocs/uxp-hub/blob/ea508323293acd250a2058c92410e0df7a3a50b0/src/pages/guides/how-to/recipes/html-events/index.md
[keyboard]: https://github.com/AdobeDocs/uxp-hub/blob/ea508323293acd250a2058c92410e0df7a3a50b0/src/pages/uxp-api/reference-js/global-members/html-events/keyboard-event.md
[css]: https://github.com/AdobeDocs/uxp-hub/blob/ea508323293acd250a2058c92410e0df7a3a50b0/src/pages/guides/how-to/recipes/css-styling/index.md
[dev-tools]: https://github.com/AdobeDocs/uxp-hub/blob/ea508323293acd250a2058c92410e0df7a3a50b0/src/pages/guides/how-to/developer-tools/index.md
[udt-workflow]: https://github.com/AdobeDocs/uxp-hub/blob/ea508323293acd250a2058c92410e0df7a3a50b0/src/pages/guides/how-to/udt-deep-dive/plugin-workflows.md
[package]: https://github.com/AdobeDocs/uxp-hub/blob/ea508323293acd250a2058c92410e0df7a3a50b0/src/pages/guides/how-to/distribution/package/index.md
[marketplace]: https://github.com/AdobeDocs/uxp-hub/blob/ea508323293acd250a2058c92410e0df7a3a50b0/src/pages/guides/how-to/distribution/adobe-marketplace/index.md
[listing]: https://github.com/AdobeDocs/uxp-hub/blob/ea508323293acd250a2058c92410e0df7a3a50b0/src/pages/guides/how-to/distribution/listing/index.md
[outside]: https://github.com/AdobeDocs/uxp-hub/blob/ea508323293acd250a2058c92410e0df7a3a50b0/src/pages/guides/how-to/distribution/outside-marketplace/index.md
[enterprise]: https://github.com/AdobeDocs/uxp-hub/blob/ea508323293acd250a2058c92410e0df7a3a50b0/src/pages/guides/how-to/distribution/enterprise-distribution/index.md
[install]: https://github.com/AdobeDocs/uxp-hub/blob/ea508323293acd250a2058c92410e0df7a3a50b0/src/pages/guides/how-to/distribution/install/index.md
[changelog]: https://github.com/AdobeDocs/uxp-hub/blob/ea508323293acd250a2058c92410e0df7a3a50b0/src/pages/uxp-api/changelog.md
