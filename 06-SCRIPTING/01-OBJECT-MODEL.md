# After Effects scripting object model

## Сквозные automation операции

Начать с [demo rig](../16-WORKING-TEMPLATES/jsx-tool/build-demo-rig.jsx): validated
project → create comp/layers → resolve matchNames → set keys/interpolation →
write TextDocument/Shape/MarkerValue → expression resolution → explicit cleanup.
Host runtime не заявлен; syntax ES3 и guide objects не равны support matrix.

Bulk rename: snapshot selected layer objects/old names перед изменением, validate
все proposed names, открыть один Undo group, менять последовательно и сообщать
changed count + failure. Имя не stable identity; не resolve заново по уже изменённому
имени. Partial failure не скрывать return=0 после успешно переименованных слоёв.

Import: выбрать существующий File, проверить `ImportOptions.canImportAs`, задать
importAs/sequence явно, импортировать, настроить interpretation только для подходящего
source, добавить Layer в validated comp. На failure удалять лишь созданные tool-owned
items, если policy это допускает, не чужой project. Replace: validate target FootageItem
и new media до `replace`; сохранить old path/interpretation для diagnostic, но не
обещать восстановление missing media простым Undo. Structural changes в indexed
groups инвалидируют property references: сохранить index и re-query после addProperty.

Queue route: add validated comp → acquire outputModule(1) → проверить доступные
template names → applyTemplate → вновь получить outputModule → установить новый
owned output File → readback path/settings → queue status. Нельзя render в существующий
неизвестный output или считать exit0 доказательством полного набора decoded frames.

File/Folder: permissions на script filesystem/network не предполагать включёнными.
Для UTF-8 text установить encoding до open, проверить return/status, close в finally;
не переписывать существующий file без explicit policy. `app.settings` — preferences,
не project persistence или secret vault. Scheduled chunks хранят generation/job ID,
обрабатывают bounded batch и revalidate target; cancelTask прекращает будущие
invocations, не откатывает уже совершённые изменения. Не держать Undo group
открытым через произвольные scheduled callbacks.

After Effects scripting exposes the host through an ExtendScript object graph. It is a high-level automation API for project structure, timeline state, properties, import and render queue. It is not the same API surface as Effect or AEGP suites.

## Mental map

~~~text
app
└── project
    ├── items
    │   ├── CompItem
    │   │   └── layers
    │   │       └── PropertyGroup / Property
    │   │           ├── transforms
    │   │           ├── effects
    │   │           ├── masks
    │   │           ├── text animators
    │   │           └── markers / keyframes
    │   ├── FootageItem
    │   └── FolderItem
    └── renderQueue
        └── RenderQueueItem
            └── OutputModule(s)
~~~

## Collections are 1-based

AE scripting collections are not normal JavaScript arrays. Items, layers, render-queue entries and many property groups use indices starting at 1.

~~~jsx
var firstItem = app.project.item(1);
var firstLayer = comp.layer(1);
~~~

Make conversion explicit when code moves between zero-based JavaScript arrays and one-based AE collections.

## Validate type before use

An active item can be absent, a composition, footage or a folder. Never cast by assumption.

~~~jsx
var item = app.project.activeItem;

if (!(item instanceof CompItem)) {
    throw new Error("Open or select a composition first.");
}
~~~

Apply the same rule to layers, footage, output modules and optional properties.

## Stable targeting

Display names may be localized, changed by Adobe or renamed by the user. For effects and properties, prefer stable match-name identifiers where the scripting API exposes them.

~~~jsx
var effects = layer.property("ADBE Effect Parade");
var slider = effects.property("ADBE Slider Control");
~~~

Use visible names for presentation. Do not make them the only machine identity in a production tool.

For product-owned layers or objects, keep your own stable identifier in deliberate project metadata instead of relying only on a layer name such as "Controller".

## Structural mutation can invalidate references

Indexed property groups are a classic scripting trap. Adding, moving or removing children can rebuild a group and invalidate object references saved earlier.

Risky:

~~~jsx
var fx = layer.property("ADBE Effect Parade");
var a = fx.addProperty("ADBE Slider Control");
fx.addProperty("ADBE Color Control");
// saved reference a may no longer be valid
~~~

Safer:

~~~jsx
var fx = layer.property("ADBE Effect Parade");
var a = fx.addProperty("ADBE Slider Control");
var aIndex = a.propertyIndex;

fx.addProperty("ADBE Color Control");

a = fx.property(aIndex); // reacquire after structural mutation
~~~

Treat host objects as host-owned references, not immortal JavaScript objects.

`numProperties` описывает indexed children, а не все доступные свойства слоя. Часть свойств доступна по имени/match name. Поэтому обычный цикл `1..numProperties` не является полным обозревателем всего layer API: сначала определите нужные roots и область обхода. Источник: [PropertyGroup в закреплённом Scripting Guide](https://github.com/docsforadobe/after-effects-scripting-guide/blob/7137a990db4bd8dc9f5869b8ca431c7dfed52bdc/docs/property/propertygroup.md).

## Undo groups are not database transactions

For user-triggered mutations, group related operations:

~~~jsx
app.beginUndoGroup("Build Rig");

try {
    // validate, then mutate
} finally {
    app.endUndoGroup();
}
~~~

This gives the user coherent undo history. It does not mean an exception automatically rolls the project back.

If partial mutation is unacceptable:

1. validate prerequisites before the first edit;
2. collect errors before running a batch;
3. create resources in a controlled order;
4. explicitly clean up product-owned resources on failure where possible.

Put undo ownership at the command boundary instead of opening nested undo groups in low-level helpers.

## Defensive scripting checklist

Before a destructive or cast-like assumption, verify:

- app.project exists;
- active item exists and is the expected type;
- layer/property index is in range;
- property/effect exists;
- canSetExpression, canVaryOverTime, canAddProperty or another capability is true when relevant;
- input file exists before import/read;
- project has a path before code depends on project.file;
- output directory exists and is writable;
- render-queue references are reacquired after structural changes when required;
- cancel leaves the project in a deliberate state.

For batch tools, validate as much as possible before the first project mutation.

## Import preflight: один файл как footage

Сначала проверьте входной File и допустимый тип импорта. Только затем меняйте проект. Авторский helper ниже получает уже выбранный File; он не открывает диалог и не создаёт проект.

~~~jsx
function importFootageFile(inputFile) {
    if (!app.project) {
        throw new Error("Open a project first.");
    }
    if (!(inputFile instanceof File) || !inputFile.exists) {
        throw new Error("Select an existing file.");
    }

    var options = new ImportOptions(inputFile);
    if (!options.canImportAs(ImportAsType.FOOTAGE)) {
        throw new Error("This file cannot be imported as footage.");
    }
    options.importAs = ImportAsType.FOOTAGE;
    options.sequence = false;

    app.beginUndoGroup("Import footage file");
    try {
        return app.project.importFile(options);
    } finally {
        app.endUndoGroup();
    }
}
~~~

Контракт: [ImportOptions](https://github.com/docsforadobe/after-effects-scripting-guide/blob/7137a990db4bd8dc9f5869b8ca431c7dfed52bdc/docs/other/importoptions.md) и [Project.importFile](https://github.com/docsforadobe/after-effects-scripting-guide/blob/7137a990db4bd8dc9f5869b8ca431c7dfed52bdc/docs/general/project.md). Проверка `canImportAs` не гарантирует успешного чтения: импорт всё равно может завершиться ошибкой. `finally` закрывает undo group, а не выполняет rollback.

Ожидаемые сценарии продукта: отсутствующий файл и недопустимый тип отказывают до mutation; допустимый файл добавляется как отдельный item; повторный вызов не обещает deduplication. Для sequence нужен отдельный сценарий. Уровень примера — **SOURCE EXAMPLE / RUNTIME-NOT-CLAIMED**; выполнение в AE здесь не записано.

## Command layer instead of UI-driven scripting

Do not bury the entire product in a button callback.

Prefer:

~~~text
UI event
  -> validate plain command
  -> command/service function
  -> AE scripting DOM
  -> normalize plain result
  -> UI renders result
~~~

The command function should remain callable from ScriptUI, CEP, a JSX harness or a future UXP adapter without rewriting the operation.

## Long operations

Host-side ExtendScript can block interactive work. Avoid one giant call that performs expensive file parsing, networking or computation and then mutates the project.

Split work into:

1. pure/external computation where practical;
2. short host mutations;
3. explicit progress and cancellation checkpoints for genuinely long jobs.

When CEP invokes ExtendScript through evalScript, the host-side script runs on the host main thread. A long script call can starve both AE interaction and CEP event scheduling.

## Version gates

New scripting methods arrive in specific AE versions. Prefer feature detection where possible.

~~~jsx
if (typeof someObject.someNewMethod === "function") {
    someObject.someNewMethod();
} else {
    // supported fallback or clear compatibility error
}
~~~

Use app.version only when behavior cannot be detected directly.

A compatibility statement should name AE versions actually tested, not merely versions whose API documentation contains the method.

Проверяйте также provenance самого member. В [ImportOptions reference](https://github.com/docsforadobe/after-effects-scripting-guide/blob/7137a990db4bd8dc9f5869b8ca431c7dfed52bdc/docs/other/importoptions.md) `rangeStart`, `rangeEnd`, `isFileNameNumbered()` явно отмечены как officially undocumented. Feature detection показывает наличие member, а не устойчивый поддерживаемый контракт. Исследовательские API требуют отдельной opt-in policy и ограничения версий продукта.

Актуальный Scripting Guide включает более поздние API, включая 26.5. Используйте его per-member version notes; native SDK baseline 25.6 не является общей версией всех scripting возможностей. Дата этого source review: **2026-10-02**, [область проверки](../EXTERNAL-SOURCES-REVIEW-2026-10-02.md).

## Boundary with expressions

Scripts mutate project state and perform automation. Expressions are evaluated as part of property evaluation and should not be used as a substitute for project orchestration.

See:

- 03-EXPRESSIONS-VS-SCRIPTS.md
- ../15-COMMUNICATION/05-SCRIPT-TO-AE.md

## Verification boundary

This chapter documents the scripting model, provenance limits and architecture patterns. It does not claim that its fragments have been executed in every supported AE version. Product-specific runtime assertions need separately identified host evidence.
