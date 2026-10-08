# ScriptUI

Практическая standalone operation: [demo rig](../16-WORKING-TEMPLATES/jsx-tool/build-demo-rig.jsx).
Его IIFE ещё не reusable command layer: для UI вынести operation в отдельную
function с plain input/result, оставив alert и dialogs в adapter. Рекомендация:
UI вызывает reusable operation, а не копирует host mutations в каждый handler.
Для long batch progress обновляется между bounded chunks; Cancel запрещает новые
chunks, не обещает rollback. Каждая chunk повторно проверяет project/target и
generation; закрытая Panel не получает late update. Dockable Panel и floating
Window имеют разные show/layout пути; scripted command не должен зависеть от них.

ScriptUI is the ExtendScript UI toolkit used for dialogs, palettes and classic script panels. It remains useful when the product is mainly AE automation and does not require a modern web-style application shell.

## Use when

- UI is small or medium;
- the tool is mostly scripting automation;
- minimal packaging matters;
- a dialog, palette or simple dockable panel is enough;
- classic controls and layout are acceptable.

## Avoid when

- complex virtualized lists or grids;
- account, browser or web workflows;
- modern responsive UI;
- large application state;
- heavy asynchronous networking;
- a product is already structured as a full panel application.

For those cases use a panel runtime and keep ScriptUI for small utilities.

## Dialog, palette and dockable panel

Common standalone windows:

~~~jsx
var dlg = new Window("dialog", "My Tool");
~~~

~~~jsx
var win = new Window("palette", "My Tool", undefined, { resizeable: true });
~~~

A reusable dockable ScriptUI panel should allow the same builder to receive either a host-provided Panel or create a Window.

~~~jsx
function buildUI(thisObj) {
    var root = (thisObj instanceof Panel)
        ? thisObj
        : new Window("palette", "My Tool", undefined, { resizeable: true });

    // create controls on root
    return root;
}
~~~

Keep UI construction separate from After Effects operations.

### Жизненный цикл формы

**DOCUMENTED / RUNTIME-NOT-CLAIMED.** `new Window()` и `add()` могут вернуть
`null`. Новое окно скрыто. У modal dialog `show()` ожидает закрытия и возвращает
число из `close(result)`; `hide()` завершает такой dialog с `0`. `onClose` вызывается
до закрытия и может вернуть `false`; `onShow` выполняется после initial layout,
но до показа. Эти window callbacks не являются общим lifecycle API для `Panel`.
[Window reference](https://github.com/docsforadobe/javascript-tools-guide/blob/ac6839049e17f4652d301e7d28f8f0d3d5fbb66a/docs/user-interface-tools/window-object.md#window-event-handling-callbacks).

Для стандартных кнопок задать creation names `ok` и `cancel`, сохранив свободно
переводимый текст. Без собственного `onClick` default/cancel button закрывает
dialog с `1`/`2`; при собственном handler закрытие становится его обязанностью.
[Modal dialogs](https://github.com/docsforadobe/javascript-tools-guide/blob/ac6839049e17f4652d301e7d28f8f0d3d5fbb66a/docs/user-interface-tools/types-of-controls.md#modal-dialogs).

Практический маршрут: controls редактируют черновик plain model; OK валидирует
весь черновик и закрывает форму; вызывающий код запускает AE command только при
явном успешном результате. Cancel, системное закрытие и `hide()` не коммитят
черновик. Проверку обязательных полей удобнее держать в OK handler: безусловный
запрет в `onClose` может одновременно запретить пользователю отмену. Borrowed
dockable Panel получает controls и layout от builder; owner приложения управляет
его жизнью. Отмена фонового job и отключение UI sink остаются отдельными действиями,
описанными ниже в `Long-running work`.

Для однострочного ввода `Window.prompt()` возвращает `null` при Cancel; пустая
строка — другой результат. `Window.find()` поддерживается не всеми реализациями,
поэтому registry собственного окна надёжнее поиска по локализованному заголовку.
[Window class](https://github.com/docsforadobe/javascript-tools-guide/blob/ac6839049e17f4652d301e7d28f8f0d3d5fbb66a/docs/user-interface-tools/window-class.md).

## Layout discipline

Prefer ScriptUI layout managers to hard-coded pixel coordinates.

Typical hierarchy:

~~~text
root
└── group(column)
    ├── group(row): inputs
    ├── status / progress
    └── group(row): actions
~~~

For resizable panels, use layout resize handling rather than manually repositioning every control.

Do not assume fonts, DPI, control metrics or platform rendering are identical on macOS and Windows.

### Initial layout и последующее изменение

**DOCUMENTED.** Default auto layout пропускает контейнер с явно заданным `bounds`.
При построении оставить bounds неопределённым, задать `orientation`, `margins`,
`spacing` и при необходимости `preferredSize`; `-1` сохраняет автоматический
расчёт соответствующего измерения. `alignChildren` — правило контейнера,
`alignment` ребёнка его переопределяет; двухэлементный массив задаёт горизонталь,
затем вертикаль. `stack` рассчитывается по крупнейшему ребёнку: это полезно для
смены страниц без прыжка общего размера.
[Automatic layout](https://github.com/docsforadobe/javascript-tools-guide/blob/ac6839049e17f4652d301e7d28f8f0d3d5fbb66a/docs/user-interface-tools/automatic-layout.md).

`layout.layout(true)` пересчитывает размеры контейнера и вложенных контейнеров
после изменения состава/контента. `layout.resize()` размещает детей после
изменения размера уже существующего контейнера по alignment. После первого показа
изменения не запускают полный layout автоматически.
[LayoutManager](https://github.com/docsforadobe/javascript-tools-guide/blob/ac6839049e17f4652d301e7d28f8f0d3d5fbb66a/docs/user-interface-tools/layoutmanager-object.md).

~~~jsx
// Собственный Window; builder уже добавил controls без фиксированных bounds.
win.onResizing = win.onResize = function () {
    this.layout.resize();
};
win.layout.layout(true);
win.show();

// После отдельного изменения структуры формы:
// updateModelAndControls();
// win.layout.layout(true);
// win.layout.resize();
~~~

Это **SOURCE EXAMPLE**, составленный для Bible; runtime run не заявлен. Не
вызывать полный rebuild внутри каждого события drag/resize. Сначала обновить модель
и нужные controls, затем сделать один layout. Для группы переключаемых страниц
выбирать `visible`, а удалять children только при реальном изменении структуры.

`bounds = [left, top, right, bottom]` не означает `[x, y, width, height]`.
Геометрические объекты создаются присваиванием соответствующей property, а не
через придуманный `new Bounds()`. Вложенные coordinates относятся к своему
контейнеру; frame окна и content area — разные области.
[Size/location objects](https://github.com/docsforadobe/javascript-tools-guide/blob/ac6839049e17f4652d301e7d28f8f0d3d5fbb66a/docs/user-interface-tools/size-and-location-objects.md).

## Controls: модель, events и перестроение

**DOCUMENTED.** Creation properties выбираются при создании, включая режимы
контролов. `children` контейнера и `items` списка индексируются с нуля; это другой
контракт, чем 1-based AE collections. После `remove()` обращение к удалённому
control не определено. Ссылки на старые widgets не переживают rebuild.
[Programming model](https://github.com/docsforadobe/javascript-tools-guide/blob/ac6839049e17f4652d301e7d28f8f0d3d5fbb66a/docs/user-interface-tools/scriptui-programming-model.md).

### Событие не является отдельной командой

**DOCUMENTED.** `onChanging` пригоден для промежуточного ввода, `onChange` — для
завершённого изменения; у EditText граница зависит от `enterKeySignalsOnChange`.
Присваивание `selection` списка или удаление выбранного item тоже вызывает
`onChange`. У multiselect ListBox чтение selection даёт массив либо `null`;
при добавлении одного item к selection прежний выбор может сохраниться. Для
замены сначала очистить selection. Read-only `items` менять через API списка.
[Control reference](https://github.com/docsforadobe/javascript-tools-guide/blob/ac6839049e17f4652d301e7d28f8f0d3d5fbb66a/docs/user-interface-tools/control-objects.md#selection).

**DOCUMENTED.** Прямой callback (`onClick`) и зарегистрированный listener
(`addEventListener("click", fn, false)`) — разные интерфейсы. Listener получает
event; для удаления нужны те же name/function/capture arguments. `notify()`
симулирует действие: checkbox/radiobutton изменяет свой `value`. Поэтому
`notify()` не подходит в качестве безусловного «перерисуй из модели».
[Callbacks/listeners](https://github.com/docsforadobe/javascript-tools-guide/blob/ac6839049e17f4652d301e7d28f8f0d3d5fbb66a/docs/user-interface-tools/defining-behavior-with-event-callbacks-and-listeners.md).

Практический pattern — один command handler и отдельный `renderForm(model)`.
Во время программного восстановления формы установить собственный флаг `syncing`;
обработчики проверяют его до вызова command. Завершать флаг в `finally`, даже если
не удалось создать item. Не подключать один mutation command одновременно к
`onClick` и к всплывающему `click` того же элемента. Промежуточный ввод обновляет
предпросмотр/черновик; тяжёлый AE edit выполняется на осмысленной границе принятия.

`event.target` — исходный control, `currentTarget` — место регистрации listener.
`stopPropagation()` останавливает дальнейшее распространение, а
`preventDefault()` отменяет default action только cancelable event. Эти действия
не взаимозаменяемы. Для mouse coordinates различать `clientX/Y` и `screenX/Y`.
[Event objects](https://github.com/docsforadobe/javascript-tools-guide/blob/ac6839049e17f4652d301e7d28f8f0d3d5fbb66a/docs/user-interface-tools/event-handling.md).

Для модификатора, прочитанного прямо внутри command callback, используется
`ScriptUI.environment.keyboardState`; это текущее состояние клавиатуры, а не
снимок старого события. `keyName` описывает одну клавишу; modifier flags читаются
отдельно. [Environment](https://github.com/docsforadobe/javascript-tools-guide/blob/ac6839049e17f4652d301e7d28f8f0d3d5fbb66a/docs/user-interface-tools/environment.md).

### Списки и дерево

**DOCUMENTED.** DropDownList и TreeView возвращают выбранный ListItem либо `null`.
У нескольких колонок ListBox один ListItem представляет строку: `text/image` —
первая колонка, `subitems[0]` — вторая. Display labels и текущие индексы не
становятся стабильными IDs модели. `onExpand(node)`/`onCollapse(node)` получают
ListItem; `onDraw(drawState)` — DrawState. Общее утверждение справочника, будто
все callbacks без аргументов, к ним неприменимо.
[Lists](https://github.com/docsforadobe/javascript-tools-guide/blob/ac6839049e17f4652d301e7d28f8f0d3d5fbb66a/docs/user-interface-tools/types-of-controls.md#creating-multi-column-lists),
[callbacks](https://github.com/docsforadobe/javascript-tools-guide/blob/ac6839049e17f4652d301e7d28f8f0d3d5fbb66a/docs/user-interface-tools/control-objects.md#control-event-handling-callbacks).

При refresh сохранить stable selected ID в plain model; подготовить новый
ограниченный набор строк; под `syncing` перестроить items и сопоставление
`item ↔ record ID`; восстановить выбор только среди новых объектов. На failure
показать, что view неполон, и запретить действие по неподтверждённому выбору.
Удалённые widgets не использовать для rollback. В TreeView отдельно хранить
expanded IDs и признак загрузки children; повторное раскрытие не должно
дублировать данные. Длинный список выдавать страницами по принятому лимиту
продукта: ScriptUI не предоставляет здесь документированную виртуализацию.

**SOURCE EXAMPLE.** Официальный Adobe
[SnpCreateTreeView.jsx](https://github.com/Adobe-CEP/CEP-Resources/blob/ab5e4e3e53a42fad08e1225a22a991bb1ffe73f6/ExtendScript-Toolkit/Samples/javascript/SnpCreateTreeView.jsx)
показывает отдельный owner дочерних items:

~~~jsx
// root — уже созданный container; это минимальный illustration, не AE command.
var tree = root.add("treeview");
if (!tree) { throw new Error("UI_CREATE_FAILED"); }
var branch = tree.add("node", "Композиции");
if (!branch) { throw new Error("UI_CREATE_FAILED"); }
var leaf = branch.add("item", "Главная композиция");
if (!leaf) { throw new Error("UI_CREATE_FAILED"); }
branch.expanded = true;
tree.selection = leaf;
// После подтверждённого изменения модели: branch.removeAll(); затем новые children.
~~~

Остальная логика этого старого filesystem example — учебная. В продукте путь или
AE target получать из записи модели, а не собирать из `node.text`: подпись может
быть локализована, сокращена или повторяться. Не вкладывать долго живущие AE DOM
references в дерево; хранить описания/IDs и разрешать их перед command.

### Текст, ресурсы и custom drawing

**DOCUMENTED.** Resource string описывает иерархию controls; вложенный `properties`
задаёт creation properties. Это собственный формат ScriptUI, а не JSON и не DOM
HTML. Для пользовательских названий проще обычный `add()` с отдельным text
argument, чем сборка resource string конкатенацией.
[Resource specifications](https://github.com/docsforadobe/javascript-tools-guide/blob/ac6839049e17f4652d301e7d28f8f0d3d5fbb66a/docs/user-interface-tools/resource-specifications.md).

Локализовать display text через `localize({en: "…", ru: "…"})` до layout.
Явный вызов не требует изменения глобального `$.localize`; автоматическая
подстановка localization objects требует `$.localize = true` по
[объекту `$`](https://github.com/docsforadobe/javascript-tools-guide/blob/ac6839049e17f4652d301e7d28f8f0d3d5fbb66a/docs/extendscript-tools-features/dollar-object.md#localize).
Написание `$.localization` в одном абзаце ScriptUI guide — конфликт источника,
не подтверждённый alias. Изменение
общего флага чужой панелью — ещё одна причина предпочесть явную функцию.
[Localization](https://github.com/docsforadobe/javascript-tools-guide/blob/ac6839049e17f4652d301e7d28f8f0d3d5fbb66a/docs/user-interface-tools/localization-in-scriptui-objects.md).

`titleLayout` размещает подпись относительно поддерживающего её control, отдельно
от общей компоновки. Его alignment не допускает `fill`; `characters` резервирует
ширину, `truncate` определяет обрезку. Для полного имени файла рядом с сокращённой
подписью можно дать helpTip; хранить полный путь в модели.
[Control titles](https://github.com/docsforadobe/javascript-tools-guide/blob/ac6839049e17f4652d301e7d28f8f0d3d5fbb66a/docs/user-interface-tools/managing-control-titles.md).

Custom drawing выполнять в `onDraw` через `control.graphics`, отдельно от AE
mutations. [Drawing objects](https://github.com/docsforadobe/javascript-tools-guide/blob/ac6839049e17f4652d301e7d28f8f0d3d5fbb66a/docs/user-interface-tools/drawing-objects.md).
У обычного image control размер области сам по себе не масштабирует картинку;
`graphics.drawImage(image, x, y, width, height)` явно масштабирует её.
`measureString()` возвращает необходимые размеры текста, а `newPath()` заменяет
текущий path. Custom element class отдельно обусловлен поддержкой host.
[Graphics reference](https://github.com/docsforadobe/javascript-tools-guide/blob/ac6839049e17f4652d301e7d28f8f0d3d5fbb66a/docs/user-interface-tools/graphic-customization-objects.md),
[images](https://github.com/docsforadobe/javascript-tools-guide/blob/ac6839049e17f4652d301e7d28f8f0d3d5fbb66a/docs/user-interface-tools/types-of-controls.md#displaying-images).

`ScriptUI.newImage()` позволяет подготовить разные изображения для состояний
normal/disabled/pressed/rollover. Default fonts и named host resources зависят от
приложения; пример имени ресурса Photoshop не объявляет такой ресурс в AE.
Версия toolkit читается из `ScriptUI.version/coreVersion/frameworkName` и не
подменяет версию AE. [ScriptUI class](https://github.com/docsforadobe/javascript-tools-guide/blob/ac6839049e17f4652d301e7d28f8f0d3d5fbb66a/docs/user-interface-tools/scriptui-class.md).

## Architecture

Even a small script should separate:

~~~text
ScriptUI callbacks
    ↓
commands
    ↓
validation + AE scripting DOM
    ↓
plain result object
    ↓
render status in UI
~~~

Bad architecture is a 300-line button callback containing project traversal, file I/O, mutation, error dialogs and UI updates.

Better:

~~~jsx
button.onClick = function () {
    var result = Commands.buildRig(readForm());
    renderResult(result);
};
~~~

This separation lets a CEP dispatcher reuse the ExtendScript command and makes a
port to another runtime easier to define. UXP still needs its own host adapter;
similar method names do not make ExtendScript code directly compatible.

## Long-running work

### Concrete synchronous command and deferred-job design

The [panel source](../20-REFERENCE-IMPLEMENTATIONS/Scripts/ScriptUI-Panel/AEDeveloperBiblePanel.jsx)
now contains widget-independent `renameSelectedLayers(prefix)`: validate prefix,
project/queue/comp/selection → snapshot targets and proposed names → recheck context
→ open Undo → rename → plain result with changed/total/error/cleanupError. The
adapter disables/re-enables the button and displays partial count, even if Undo
close fails. No collision resolution or rollback is promised. Names are not
identity; this immediate non-structural operation does not retain refs across tasks.
Docked and floating roots both receive initial layout; only Window uses center/show.

For a **long deferred job**, use an explicit product registry resolvable by the
scheduled script string, not a closure that disappears when this IIFE exits.
Capture project epoch + target IDs/descriptions + job/UI generation; each bounded
callback re-resolves and validates targets, opens/closes its own Undo scope, applies
one bounded unit and reports completed/failed count. One coherent global Undo across
arbitrary scheduled callbacks is not promised. Cancel marks the job, cancels a known
pending task ID, and prevents rescheduling; it cannot interrupt a running synchronous
DOM call or reverse committed chunks. On panel recreation, old callbacks must not
touch old controls or whichever targets are currently selected. Detach UI sinks and
invalidate generation even if task cancellation fails. This registry/progress/cancel
route is design only, not implemented in the small synchronous panel.

ScriptUI does not turn ExtendScript into a worker-thread environment. A long synchronous loop freezes the tool and can make AE appear hung.

**DOCUMENTED.** `Window.update()` синхронно выполняет redraw и обрабатывает часть
mouse/keyboard events; окно должно быть visible. На это время применяется modal
state. Это не worker и не прерывание выполняемого DOM call.
[update()](https://github.com/docsforadobe/javascript-tools-guide/blob/ac6839049e17f4652d301e7d28f8f0d3d5fbb66a/docs/user-interface-tools/window-object.md#update).
Если progress loop использует этот путь, считать update точкой входа callback:
запретить повторный Start, после возврата повторно проверить Cancel/generation,
затем начинать следующую bounded unit. Не вызывать window-only update на borrowed
Panel по одному лишь сходству свойств.

For long jobs:

- validate before starting;
- update progress at sensible intervals;
- expose a cancel flag where the workflow allows it;
- chunk work instead of repainting on every item;
- move CPU-heavy independent work outside ExtendScript when that fits the product architecture.

app.scheduleTask can help defer or chunk script work, but it is a scheduling primitive, not a general concurrency model. It also introduces lifecycle and global-state concerns because scheduled code must remain resolvable later.

## Errors and cleanup

UI callbacks must not leave controls permanently disabled after an exception.

~~~jsx
button.enabled = false;

try {
    var result = Commands.run();
    status.text = result.message;
} catch (e) {
    status.text = "Error: " + e.toString();
} finally {
    button.enabled = true;
}
~~~

For batch tools, prefer a status area or aggregated error report over an alert for every recoverable validation issue.

## Persistence

Do not make transient widget state the only source of truth for important product state.

Separate:

- UI state: selected tab, temporary text, expanded sections;
- project state: data that legitimately belongs in the AE project;
- user preferences: explicit settings layer;
- secrets or licensing credentials: never embedded in JSX source.

## Migration rule

A ScriptUI tool is migration-ready when its AE operations can run without ScriptUI objects being present.

If command functions accept plain input and return plain output, the same
ExtendScript command layer can sit behind a CEP evalScript dispatcher or a JSX
test harness.

A UXP port keeps the semantic command and data model, but implements its host
adapter against the [separate UXP contracts](../07-PANELS/03-UXP-HOST-API.md).
File/path types, return values, async behavior and availability must be reconciled
per operation; this is not an automatic JSX execution path in UXP.

## Source и граница применимости

**DOCUMENTED / SOURCE EXAMPLE / RUNTIME-NOT-CLAIMED.** Review покрывает полностью
22 ScriptUI pages закреплённого JavaScript Tools Guide mirror `ac6839049e17f4652d301e7d28f8f0d3d5fbb66a`
и один отдельный Adobe tree sample. Это review текста, а не заявление, что каждый
control из generic guide поддержан каждой версией AE.

Исторические FlashPlayer/SWF/ActionScript instructions описывают прежний bridge
через `ExternalInterface` и `invokePlayerFunction`; они не являются современным
AE panel route. В этом проходе Flash support текущего AE не заявлен.
[Flash communication](https://github.com/docsforadobe/javascript-tools-guide/blob/ac6839049e17f4652d301e7d28f8f0d3d5fbb66a/docs/user-interface-tools/communicating-with-the-flash-application.md).
`EditNumber` помечен как Photoshop 20.0 addition; переносимый AE workflow может
использовать собственный разбор и проверку числа в EditText. `topDivider` и `onEnterKey` прямо отмечены
maintainers как undocumented discoveries. Не делать их обязательными для command
workflow. Наличие пункта в общей таблице свойств не перекрывает более точный
контракт control: например, её строка `characters` расходится с reference
StaticText/EditText.
[Common properties](https://github.com/docsforadobe/javascript-tools-guide/blob/ac6839049e17f4652d301e7d28f8f0d3d5fbb66a/docs/user-interface-tools/common-properties.md),
[control details](https://github.com/docsforadobe/javascript-tools-guide/blob/ac6839049e17f4652d301e7d28f8f0d3d5fbb66a/docs/user-interface-tools/control-objects.md).

Список [Adobe examples](https://github.com/docsforadobe/javascript-tools-guide/blob/ac6839049e17f4652d301e7d28f8f0d3d5fbb66a/docs/user-interface-tools/code-examples-for-scriptui.md)
— навигация: полный review страницы ссылок не означает review всех файлов samples.
Точный support matrix и visual observations относятся к продукту, который их
заявляет; отсутствие такого host run не блокирует этот source-level раздел Bible.

Полный [постраничный ledger](../extendscript-runtime-reviewed-2026-10-08.json)
и [runtime/tooling глава](04-EXTENDSCRIPT-RUNTIME.md) сохраняют source scope.
