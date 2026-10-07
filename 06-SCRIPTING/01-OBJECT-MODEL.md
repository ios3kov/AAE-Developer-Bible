# After Effects scripting object model

## Current scripting delta — review 2026-10-07

Source snapshot: [scripting changelog](https://github.com/docsforadobe/after-effects-scripting-guide/blob/7137a990db4bd8dc9f5869b8ca431c7dfed52bdc/docs/introduction/changelog.md).
These are **ExtendScript DOM introduction versions**, not native SDK generations
or UXP availability. DOCUMENTED/source designs; no new host runtime observed.

| Introduced | Operation and contract | Safe workflow |
|---|---|---|
| 26.0 | Property.propertyParameters / valueText: dropdown strings / selected text, read-only | Use numeric value for selection and strings for display; labels are not durable/localization-independent IDs |
| 26.0 | PropertyGroup.addVariableFontAxis(axisTag) on ADBE Text Animator Properties only | Discover actual font designAxesData; add valid 4-character axis; reacquire invalidated indexed-group properties; use actual font bounds, not universal wght100–900 |
| 26.3 | LayerCollection.addParametricMesh(name, meshType); ParametricMeshLayer and mesh/bevel options | Validate comp/type before Undo; create, read back layer type/mesh, report partial result; do not replace unavailable mesh with solid as equivalent |
| 26.3 | Camera FocusAreaWidth/NearFarBlurMultiplier | Advanced3D-only; property presence does not prove active renderer supports desired image |
| 26.5 | GuideOptions, typed enums, getGuideAsObject and object overloads | Full-state readback and explicit units; never persist raw guide enum integers across versions |
| 26.5 | layerInputStage/inputLayerAndStage, setters and cycle-safe query | Require LAYER_INDEX property; revalidate source/index/stage after structural mutation |

### Guide edit: partial update without destroying units

Preconditions: selected intended Item/Layer; valid current guide index; AE26.5+
API actually available. Read `getGuideAsObject(index)` to show current state.
Create `new GuideOptions()`, set only `color = [0,0,1]`, then call
`target.setGuide(index, options)` within an Undo group. Read back full state; verify
color and unchanged orientation/positionType/position/pinned. Older positional
form is **setGuide(position, index)**, reversed arguments! Do not turn a percentage
guide into pixels accidentally. Structural insertion/removal invalidates index
selection; re-list before mutation. Undo grouping is not transactional rollback.

Scripting guide warns orientationType/positionType integer values differ between
AE versions: compare `GuideOrientationType` / `GuidePositionType` constants, not0/1.
If constants or object getters unavailable, refuse fidelity-preserving edit or offer
explicit lossy pixel-only operation; never assert identical semantics.

### Layer input stage: source pair, not just property.value

[Property reference](https://github.com/docsforadobe/after-effects-scripting-guide/blob/7137a990db4bd8dc9f5869b8ca431c7dfed52bdc/docs/property/property.md)
documents `inputLayerAndStage` as `[layerIndex, stageIndex]`;0 means no source layer.
`setInputLayerAndStage(layerIndex, stageIndex)` changes both in one Undo step;
returns nothing, so do not impose UXP Application boolean-success behavior.
`setLayerInputStage(stage)` changes stage only. Non-LAYER_INDEX property throws.

Concrete conservative command: late resolve target property and source layer in
its comp → validate integer index0..numLayers and LAYER_INDEX → snapshot old pair
→ use documented SOURCE constant and combined setter → read back both. SOURCE
is documented always cycle-safe. For richer stages re-query
`getInputStageCycleSafeLimit()` with the relevant current source; do not compare
sentinel integers using a guessed numeric ordering. An old-source safe limit does
not certify a proposed different-source pair. If allowed-stage policy is unclear,
do not offer that mutation. Readback failure leaves possible mutation; no blind retry.

### Variable font axis: discovery before creation

Set the actual installed variable font on a copied TextDocument and write it back.
Inspect `FontObject.designAxesData`; validate requested tag/range. Resolve Text →
Animators → intended animator → `ADBE Text Animator Properties`; addVariableFontAxis
only here. Save necessary indices, reacquire group/property after indexed additions,
set bounded value/keyframes, verify keys and render-font availability separately.
`ADBE Text Variable Font Spacing` appears only after an active axis; its dropdown
affects character spacing compensation, not a generic font substitution fix.
Missing font/axis: stop without silently selecting another font. Source:
[PropertyGroup](https://github.com/docsforadobe/after-effects-scripting-guide/blob/7137a990db4bd8dc9f5869b8ca431c7dfed52bdc/docs/property/propertygroup.md).

This closes the scoped26.x changelog delta, not a full historical scripting/expression
member audit. Mesh shape/options source:
[ParametricMeshLayer](https://github.com/docsforadobe/after-effects-scripting-guide/blob/7137a990db4bd8dc9f5869b8ca431c7dfed52bdc/docs/layer/parametricmeshlayer.md).

## Сквозные automation операции

### Property animation: typed plan before mutation

Reviewed2026-10-07 against pinned scripting source
`7137a990db4bd8dc9f5869b8ca431c7dfed52bdc`,
[Property](https://github.com/docsforadobe/after-effects-scripting-guide/blob/7137a990db4bd8dc9f5869b8ca431c7dfed52bdc/docs/property/property.md),
[PropertyGroup](https://github.com/docsforadobe/after-effects-scripting-guide/blob/7137a990db4bd8dc9f5869b8ca431c7dfed52bdc/docs/property/propertygroup.md),
[PropertyBase](https://github.com/docsforadobe/after-effects-scripting-guide/blob/7137a990db4bd8dc9f5869b8ca431c7dfed52bdc/docs/property/propertybase.md).
DOCUMENTED/source operation design, not executed AE animation.

Concrete authoring command: resolve intended layer/property → validate
propertyValueType/canVaryOverTime and existing keys/expression policy → build
finite times and correctly shaped values → show overwrite scope → begin Undo
→ set values → resolve keys by time and verify keyTime → set supported interpolation
→ verify keys/values/interpolation → end Undo with independent cleanup error.
Product policy here requires strictly increasing times (reject duplicates), equal
array lengths and bounded batch size; not an undocumented Adobe uniqueness rule.
For opacity, request times[0,1] and values[0,100], LINEAR. Preserve unrelated keys;
if replacing an interval, explicitly list/removal-confirm only that interval.

Property.setValue only sets a static no-key property; it throws when keys exist.
Property.setValueAtTime creates or updates the key at the requested time;
Property.setValueAtKey requires an existing valid key index.
Property.setValuesAtTimes creates/updates each requested time and requires equal
length arrays; no whole-call transactional rollback is documented. An exception
can leave a partial outcome: refresh keys and report, never blind retry.
These setters return nothing, not boolean success.

Property.nearestKeyIndex is not proof a key exists **at** your time. Check numKeys,
then keyTime with an explicitly chosen numerical tolerance appropriate to product
time representation. Do not round times to frame boundaries unless that is requested
policy. Property.removeKey shifts indices; delete selected keys highest-to-lowest.
Stored key indices do not survive insertion/removal as stable identity.

Check Property.isInterpolationTypeValid before Property.setInterpolationTypeAtKey.
Omitted outType uses inType. For Property.setTemporalEaseAtKey, ease array length
is2 for TwoD,3 for ThreeD, **1 for all other types including spatial vectors**;
do not derive it from value.length. Construct KeyframeEase with valid product values.
Property.setSpatialTangentsAtKey accepts only TwoD_SPATIAL/ThreeD_SPATIAL, matching
2/3-component tangent vectors; temporal easing is not a spatial tangent operation.
Auto-Bezier/continuous/roving policies require their own member checks, not implied
by this scoped LINEAR operation.

### Structural mutation and expression evaluation

PropertyGroup.canAddProperty guards intended matchName before PropertyGroup.addProperty.
Adding to an indexed group recreates it and invalidates existing property references;
save propertyIndex where appropriate and reacquire after subsequent additions.
Text animator is the documented named-group exception. PropertyBase.matchName avoids
localized display names but is a **type identifier**, not a unique instance ID when
the same effect occurs more than once. Resolve intended occurrence/parent and verify
its matchName after index lookup; stale index alone is not identity.

Property.expression assignment evaluates the expression: invalid string generates
error and disables expression; empty string disables without error. Validate
canSetExpression, preserve old string/enabled state for diagnostics, assign, inspect
Property.expressionError and expressionEnabled. A successful initial evaluation
does not establish correctness for all times/assets. Property.valueAtTime(time,true)
reads pre-expression value; false requests evaluated value and can wait for expensive
expressions such as sampleImage. Bound diagnostic samples; don't run full-frame
expression sampling in a UI repaint loop. The Source Text layer-time exception is
described in font usage preflight below.

Property.dimensionsSeparated applies to a separation leader. Before editing Position,
inspect isSeparationLeader/dimensionsSeparated; when already separated use
Property.getSeparationFollower(dim) with0-based dimension and author scalar keys.
Do not toggle separation merely to fit a generic vector setter; separation can
change animation representation and needs explicit product migration policy.

### Font preflight: identity, substitutes and project usage

Reviewed2026-10-07 at scripting source `7137a990db4bd8dc9f5869b8ca431c7dfed52bdc`:
[FontsObject](https://github.com/docsforadobe/after-effects-scripting-guide/blob/7137a990db4bd8dc9f5869b8ca431c7dfed52bdc/docs/text/fontsobject.md),
[FontObject](https://github.com/docsforadobe/after-effects-scripting-guide/blob/7137a990db4bd8dc9f5869b8ca431c7dfed52bdc/docs/text/fontobject.md),
[Project](https://github.com/docsforadobe/after-effects-scripting-guide/blob/7137a990db4bd8dc9f5869b8ca431c7dfed52bdc/docs/general/project.md).
DOCUMENTED/source workflow, no host result claimed.

Concrete read-only preflight: validate project and font API → record
FontsObject.fontServerRevision → flatten FontsObject.allFonts family arrays for
display → read FontsObject.missingOrSubstitutedFonts and Project.usedFonts → report
source font identity and each usedAt.layerID/layerTimeD → recheck revision and mark
stale if it changed. Do not mutate sync policy or activate fonts as a hidden side
effect of a report. Resolve layers by Project.layerByID; skip/report deleted targets.

Critical time-domain exception: **Source Text.valueAtTime expects layer time** in
the usedFonts example, unlike other properties' comp-time usage. Preserve supplied
layerTimeD; don't substitute comp.time or subtract startTime again blindly.

FontObject.fontID is stable only within this application session, may change after
restart. FontsObject.getFontByID can return undefined after removal. Persist font
descriptors, not fontID as cross-launch identity; re-resolve and handle ambiguity.
FontsObject.allFonts groups are not uniquely keyed by family name; duplicate
PostScript names are allowed across technology/writing-script tuples. Never pick
array[0] automatically for a release-critical replacement. Display technology,
writing scripts, designVector and substitute status for user selection.

FontsObject.fontServerRevision changes on installation/removal, substituted-project
open/close, variable instances and English-name sort preference. Cache by this
revision only within the session; a matching revision is not render/image proof.
FontObject.designAxesData gives name/tag/min/max/default; designVector order follows
axes, not alphabetical tag order. Both can be undefined for non-variable fonts.
FontObject.hasSameDict tests variable-font dictionary identity, not equal appearance.
FontObject.postScriptNameForDesignVector returns a name, not installed availability.
FontObject.hasGlyphsFor (25.1+) answers whether **all** characters have glyphs;
false doesn't identify which character, true doesn't prove shaping/layout correctness.

### Project-wide font replacement is not Undo-safe

Project.usedFonts / Project.replaceFont introduced24.5. Plan: fresh usage report →
explicit from/to font choice and backup/save policy → re-resolve both font instances
and project → user confirmation of non-undoable mutation → replaceFont → refresh
usage and text/layout diagnostics. No automatic retry if an exception leaves unknown
outcome. The return is boolean **at least one layer changed**, not a changed-count,
complete glyph-success result or saved-project confirmation.

Project.replaceFont preserves mixed-style ranges but is **not undoable**; wrapping
it in beginUndoGroup cannot provide rollback. Optional noFontLocking=false allows
glyph fallback; true can yield missing glyphs without a complete detection/report
API. For substituted fromFont with identical target properties, documentation says
fallback is suppressed and the option treated as true. A successful replacement
does not establish final glyph coverage. Preflight sampled text with hasGlyphsFor
where available and qualify relevant frames/layout separately.

FontsObject.freezeSyncSubstitutedFonts (24.6) controls automatic Adobe Fonts sync;
FontsObject.substitutedFontReplacementMatchPolicy selects POSTSCRIPT_NAME,
CTFI_EQUAL or DISABLED replacement matching. These are application-environment
policies, not per-layer edits. If a tool deliberately changes them, save old values,
restore in finally, report restoration error separately and don't promise restoration
undoes already completed font activation/replacement.

### Text ranges: detached edit, explicit commit, fresh composition

Source: [TextDocument](https://github.com/docsforadobe/after-effects-scripting-guide/blob/7137a990db4bd8dc9f5869b8ca431c7dfed52bdc/docs/text/textdocument.md),
[CharacterRange](https://github.com/docsforadobe/after-effects-scripting-guide/blob/7137a990db4bd8dc9f5869b8ca431c7dfed52bdc/docs/text/characterrange.md).
TextDocument.characterRange / paragraphRange / composedLineRange introduced24.3.
Character indices start0; explicit end is exclusive, optional end selects one
character; -1 follows current text end. Cannot span final carriage return. Paragraph
and composed-line ranges use their respective indices, not character offsets.

Concrete styling edit: resolve intended Source Text and time/key policy → obtain
TextDocument value → validate start/end against that value → obtain characterRange
→ edit chosen styling fields only → commit with setValue for static property or
explicit key/time route → reacquire TextDocument → verify target styling and text.
Do not overwrite animated Source Text through a generic static setter; do not treat
first-character aggregate style as proof all mixed-style characters match.

CharacterRange.isRangeValid must be checked after edits changing length.
CharacterRange.pasteFrom (25.1) deletes target text then pastes source text/style;
original range bounds stay fixed and a shorter paste can invalidate the target.
Recreate accessors after structural text changes. Validation before paste is not
permission to reuse the old accessor afterward.

TextDocument.composedLineCount is a snapshot from initial composed state; editing
the detached TextDocument does **not** recompose it. It may be zero for all-overset
text. Commit and reacquire before using composedLineRange or reporting line layout.
TextDocument.boxOverflow (24.6) reports some text didn't compose into the box;
don't hide overflow by claiming successful text assignment proves full visibility.
Absent versioned APIs require an explicit older-host path or unsupported report,
not interpreting undefined as no missing fonts/no overflow.

[Import/queue source](../16-WORKING-TEMPLATES/jsx-tool/import-and-queue.jsx): диалоги
input/output диалоги до Undo → canImportAs → import → comp/layer → disabled queue item → exact template
prompt внутри Undo → reacquire → output path readback. Не запускает render и не включает чужие
items. Extension/sequence-pattern согласовать с template вручную; path selection
не доказывает format compatibility. Компенсация касается только созданных objects;
при failed dependent cleanup footage сохраняется для диагностики.

Начать с [demo rig](../16-WORKING-TEMPLATES/jsx-tool/build-demo-rig.jsx): validated
project → create comp/layers → resolve matchNames → set keys/interpolation →
write TextDocument/Shape/MarkerValue → expression resolution → explicit cleanup.
Host runtime не заявлен; syntax ES3 и guide objects не равны support matrix.

Demo expression uses animated `value` plus slider with clamp, so keys are not
silently overridden: slider50 yields expected opacity50 at t=0 and100 at t=1.
`valueAtTime(0,false)` requests post-expression evaluation; expressionEnabled/error
checks establish script-level resolving only, not a complete pixel correctness test.
The script currently creates linear keys; it is not an ease/Bezier authoring example.

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

## Source composition and remaining operation limits — 2026-10-07

| Operation | Actual source | Design / failure boundary |
|---|---|---|
| Bulk rename | [ScriptUI command](../20-REFERENCE-IMPLEMENTATIONS/Scripts/ScriptUI-Panel/AEDeveloperBiblePanel.jsx) snapshots selected layer refs and proposed names, returns changed/total/error/cleanupError | Synchronous, current selection only; not scheduled stable-ID resolution; no rollback or collision-free naming promise |
| Standalone rename | [Small IIFE](../16-WORKING-TEMPLATES/jsx-tool/rename-selected-layers.jsx) prefixes current names and returns count on success | Repeat adds prefix; failure alerts but does not report partial count; not the reusable command above |
| Import + queue | Existing import-and-queue IIFE creates owned objects and disabled queue item | Template prompt occurs after creation inside Undo, not all dialogs before Undo; path readback only, not settings/format verification |
| Rig | Existing build-demo-rig IIFE creates new comp and checks expression resolution | Linear keys; new-comp compensation, no reusable rig command or render proof |
| Replace | Workflow below | Design only: no replacement script shipped |

**Replace workflow.** Snapshot the intended FootageItem and original file/source
interpretation for diagnostics. Choose media before mutation, then revalidate the
same project and target after the dialog; reject a removed/replaced/non-file target
or newly busy queue. `canImportAs` is import preflight, not a guarantee that `replace`
will decode or preserve every media characteristic. Inside one successful Undo
scope call the documented `FootageItem.replace(File)`, re-query the new source and
check intended dimensions/duration/interpretation and dependent layer expectations.
Failure after replacement is partial/unknown until readback, not automatically
restored by Undo or a cached old path. Do not remove the pre-existing footage item
as compensation. This is a worked command design, not executed source.
Source: [pinned FootageItem reference](https://github.com/docsforadobe/after-effects-scripting-guide/blob/7137a990db4bd8dc9f5869b8ca431c7dfed52bdc/docs/item/footageitem.md).
That reference states `replace` creates a new FileSource, updates media-derived
name/dimensions/frameDuration/duration, preserves prior interpretation parameters,
and estimates alpha interpretation for unlabeled alpha. Re-query rather than retain
the old `mainSource` object. Sequence replacement is a separate `replaceWithSequence`
operation, not this single-file workflow.

Import lesson chooses input/output before Undo but prompts for an exact template
after queue creation. User must inspect format, range and output settings before
enabling; code only compares `om.file.fsName`. A new path is not an exclusive
filesystem reservation. The two-second/25fps comp is fixed, not matched to imported
media duration/framerate. If queue removal fails, do not infer all dependent
cleanup succeeded: the source still attempts comp removal and retains footage
when earlier cleanup failures were recorded. These limits are not host observations.

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

### OneD temporal ease: самостоятельная операция

Prerequisite: caller passes an already resolved, tool-owned OneD property in a
disposable comp, with no enabled expression and no keys. Caller opens/closes Undo
and compensates only its newly created comp on failure; this helper does not remove
user keys to force eligibility. Source example / AE NOT_RUN:

```jsx
function addEasedOneD(prop) {
    if (!prop || prop.propertyValueType !== PropertyValueType.OneD ||
        !prop.canVaryOverTime || prop.expressionEnabled || prop.numKeys !== 0 ||
        !prop.isInterpolationTypeValid(KeyframeInterpolationType.BEZIER))
        throw new Error("Need unkeyed expression-free OneD property");
    prop.setValuesAtTimes([0, 1], [0, 100]);
    for (var k = 1; k <= 2; k++) {
        prop.setInterpolationTypeAtKey(k, KeyframeInterpolationType.BEZIER,
            KeyframeInterpolationType.BEZIER);
        prop.setTemporalAutoBezierAtKey(k, false);
        prop.setTemporalEaseAtKey(k, [new KeyframeEase(0, 33.333)],
            [new KeyframeEase(0, 33.333)]);
    }
    return {keys: prop.numKeys, firstTime: prop.keyTime(1), lastTime: prop.keyTime(2),
        firstOutSpeed: prop.keyOutTemporalEase(1)[0].speed};
}
```

Expected: keys at0/1s with values0/100, Bezier interpolation, zero endpoint speeds;
inspect readback interpolation/ease before treating it as accepted. Failure after
the first setter can leave partial keys; caller compensation is necessary. OneD
uses one ease object per direction. TwoD/ThreeD quantitative properties need
dimension-matched arrays; spatial properties have separate temporal/spatial
semantics. Do not copy this helper into a Position leader/follower by cast.
Source: [pinned Property guide](https://github.com/docsforadobe/after-effects-scripting-guide/blob/7137a990db4bd8dc9f5869b8ca431c7dfed52bdc/docs/property/property.md),
setValuesAtTimes, setInterpolationTypeAtKey, setTemporalAutoBezierAtKey,
setTemporalEaseAtKey and keyOutTemporalEase. This is separate from the linear rig.

Source-quality caveat: that guide's setTemporalAutoBezierAtKey paragraph refers
to keySpatialContinuous even though its keyTemporalAutoBezier attribute paragraph
describes Bezier temporal interpolation; setTemporalContinuousAtKey's newVal text
also calls continuity auto-Bezier. Treat these as documentation inconsistencies,
not authority to invoke spatial APIs on OneD. The fragment explicitly disables
temporal auto-Bezier and declares manual ease; verify actual readback in target AE.

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

### File/Folder и preferences: bounded сценарии

**UTF-8 text export (SOURCE EXAMPLE / AE NOT_RUN).** Включённые scripting file
permissions — prerequisite, не обещание helper. Dialog до mutation, новый filename,
проверка parent Folder и возвращаемых I/O statuses. Здесь нет project edits и Undo:

```jsx
function writeNewUtf8(file, text) {
    if (!file || file.exists || !file.parent.exists)
        throw new Error("Choose a new file in an existing folder");
    file.encoding = "UTF-8";
    var opened = false, primary = null, closeProblem = null;
    try {
        if (!file.open("w")) throw new Error(file.error || "Open failed");
        opened = true;
        if (!file.write(text)) throw new Error(file.error || "Write failed");
    } catch (e) { primary = e; }
    finally {
        if (opened) {
            try { if (!file.close()) closeProblem = "Close failed: " + file.error; }
            catch (c) { closeProblem = c.toString(); }
        }
    }
    if (primary || closeProblem)
        throw new Error((primary ? primary.toString() : "") + "\n" + (closeProblem || ""));
    return file.fsName;
}
```

Expected: Unicode text roundtrips through an independent UTF-8 reader, output
path returned only after successful close. Failure can leave partial own file;
do not report complete export. `exists` check is **not exclusive creation**: race
can create a file before open("w"). Use a product-owned staging directory under
controlled access; if collision-free publication against concurrent writers is
required, use an external service with exclusive-create/atomic-publish semantics,
not this helper. Never delete user files as automatic error cleanup.

**Preferences.** A tool can save a short non-secret mode string under its own
`app.settings` section; this does not mutate project and needs no Undo. Example:

```jsx
function saveMode(mode) {
    if (mode !== "preview" && mode !== "final") throw new Error("Invalid mode");
    app.settings.saveSetting("BibleDemo", "mode", mode);
    if (app.settings.getSetting("BibleDemo", "mode") !== mode)
        throw new Error("Preference readback mismatch");
}
function readMode() {
    if (!app.settings.haveSetting("BibleDemo", "mode")) return "preview";
    var value = app.settings.getSetting("BibleDemo", "mode");
    return value === "final" ? "final" : "preview";
}
```

Expected current preference readback, not proof of persistence across process exit.
Test restart separately in target AE. Settings I/O can fail; caller reports the
error instead of marking saved. Unknown values use declared safe default; no secret
or binary blob, no attempt to override host's preference storage location.
The guide documents values as strings, per-version preferences (not automatically
migrated across AE installs), and a reported1999-byte failure limit in AE15.0.1;
keep tiny preferences rather than interpreting that observation as a universal
modern capacity guarantee.
Exact
File/Folder APIs follow [ExtendScript File reference](https://extendscript.docsforadobe.dev/file-system-access/file-object/)
(open/write/close returns reviewed2026-10-07), not browser File APIs; Settings follows
[pinned guide](https://github.com/docsforadobe/after-effects-scripting-guide/blob/7137a990db4bd8dc9f5869b8ca431c7dfed52bdc/docs/other/settings.md).

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
