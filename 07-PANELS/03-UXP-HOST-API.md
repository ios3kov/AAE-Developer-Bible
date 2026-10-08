# AE UXP: host module, project operations и migration contracts

Проверено по официальной AE-specific reference **2026-10-08**: все **44 страницы**
закреплённого source snapshot (43 объекта + index) полностью прочитаны; SHA256
сверены с inventory. Evidence: DOCUMENTED / SOURCE EXAMPLE; runtime **NOT_RUN**.
Это полнота чтения данного набора страниц, не обещание всех overloads, типов,
конструкторов, shared-platform API или установленной поддержки AE UXP.
[Переход на UXP](02-UXP-TRANSITION.md) описывает rollout; ниже — практические
операции и конкретные пробелы опубликованных контрактов.

## Доступ и целевая версия

Официальный [API index](https://developer.adobe.com/after-effects/uxp/after-effects-api/)
показывает **`const app = require("aftereffects")`**: модуль — сам Application,
не `{app}` из Photoshop и не глобальный ExtendScript `app`. Проверенные страницы
Application/Project/ItemCollection/CompItem имеют Min Version/Since **27.0**.
Эта минимальная версия не является подтверждением GA или доступности конкретного
beta build. Нужен AE с UXP host module; обычный Node/CEP/ExtendScript его не предоставляет.

Сначала в поддерживающей development-среде записать `app.version`, `buildNumber`,
`buildName`, `appName`, `isBeta`. Не выводить совместимость из похожего DOM или
успеха `require("uxp")` в другом Adobe host. Manifest/UDT/installation workflow
должен соответствовать AE-specific host setup; этот source example не устанавливает
панель и не предлагает выдуманный host ID/minVersion manifest.

## Когда использовать

Для UXP UI/application tool, которому нужно создавать/организовывать project items,
изменять layers/properties, импортировать и управлять render queue через опубликованный
AE DOM. Pixel hot path остаётся Effect/native API. UI не владеет persistent render truth.
UXP Application доступ не даёт permission вызывать host API из произвольного worker.
Не переносить Photoshop `executeAsModal`, CEP `evalScript` или Node filesystem
автоматически: опубликованный host contract и shared UXP platform — разные слои.

## Что действительно опубликовано

AE API index включает:

| Domain | Objects / где искать контракт |
|---|---|
| App/project | Application, Project, Preferences, Settings, ItemCollection, FolderItem |
| Comps/layers | CompItem, LayerCollection, Layer, AVLayer, CameraLayer, LightLayer, ShapeLayer, TextLayer, ThreeDModelLayer, ParametricMeshLayer |
| Properties/animation | Property, PropertyGroup, MaskPropertyGroup, Shape, KeyframeEase, MarkerValue |
| Text/fonts | TextDocument, CharacterRange, ParagraphRange, ComposedLineRange, Font, Fonts |
| Media/import | ImportOptions, FootageItem, FileSource, PlaceholderSource, SolidSource |
| Queue/output | RenderQueue, RenderQueueItem, RQItemCollection, OutputModule, OMCollection |
| Views/guides | Viewer, View, ViewOptions, GuideOptions |
| Deferred work | DeferredCall |

Все перечисленные страницы прочитаны на одном pin; точные пути и хэши находятся
в [review ledger](../uxp-api-reviewed-2026-10-08.json). Отдельные таблицы содержат
наследуемые повторы и противоречия: полная page review не устраняет их автоматически.
Не обещать полную parity с ExtendScript из одинаковых object names.

## Конкретная операция: создать comp без замены проекта

Preconditions: module доступен; user инициирует command; открытый disposable project;
ни параллельной mutation command, ни pending uncertain outcome. Команда добавляет
один item, не вызывает newProject/open/close/save, не меняет rendering/preferences.
Чистую validation делать до Undo и mutation. Рекомендованные dimensions here:
1920×1080, PAR1, duration2s, frameRate24 — не универсальные SDK limits.

```javascript
const app = require("aftereffects");

function createLessonComp() {
  const project = app.project;
  if (!project || !project.items ||
      typeof project.items.addComp !== "function") {
    throw new Error("AE UXP project/addComp unavailable");
  }
  const result = {
    host: {version: app.version, build: app.buildNumber, beta: app.isBeta},
    mutation: "not_started", itemId: null,
    primaryError: null, cleanupError: null
  };
  let undoOpen = false;
  try {
    if (app.beginUndoGroup("Bible UXP: create comp") !== true) {
      throw new Error("beginUndoGroup did not confirm success");
    }
    undoOpen = true;
    result.mutation = "unknown";
    const comp = project.items.addComp("Bible UXP Lesson", 1920, 1080, 1, 2, 24);
    if (!comp) throw new Error("addComp returned no item");
    result.itemId = comp.id;
    result.mutation = "created";
    if (comp.width !== 1920 || comp.height !== 1080 ||
        comp.pixelAspect !== 1 || comp.duration !== 2 || comp.frameRate !== 24) {
      throw new Error("Created comp settings did not match requested values");
    }
  } catch (error) {
    result.primaryError = String(error);
  } finally {
    if (undoOpen) {
      try {
        if (app.endUndoGroup() !== true) throw new Error("endUndoGroup failed");
      } catch (error) {
        result.cleanupError = String(error);
      }
    }
  }
  return result;
}
```

Call from the host-supported command entry, not at module import. The stricter
boolean-success gate follows the published Application return type; if the chosen
build disagrees, retain version/outcome and resolve docs/build conflict before
shipping, not weaken the condition to accept undefined silently.

Expected reader observation: **one** new comp with specified dimensions/PAR/time/fps;
normal completion has mutation created, itemId and no errors; one Undo group.
The code does not perform host-test observations, project save/reopen or screenshot.
`beginUndoGroup` throw/false: no mutation attempted, no unmatched end. Mutation
throw: unknown outcome (may have created something). Readback failure: created item
may remain. End failure: created item can remain with uncertain history state.
No automatic retry, no deletion compensation, no assertion that Undo is atomic rollback.

## Official-source inventory and media/output workflows — 2026-10-08

Published page HTML links to official repository `AdobeDocs/uxp-after-effects`.
Pinned source `7d1cd01b4c69a9e02b77d48b3f919a6145a90841` now inventoried by
`scripts/audit_uxp_inventory.py`:44 pages (43 objects + index),1448 property rows/
method headings. Repeated inherited members are counted per page, **not1448 unique
API symbols or all overloads**. `uxp-api-reviewed-2026-10-08.json` lists only actual
full-page reviews at this revision; prior live reviews aren't automatically promoted.
Текущий ledger охватывает44/44 страницы и1448/1448 таких строк/заголовков.
История отдельных блоков сохранена в currentness review, а предметные разделы
ниже показывают результат согласования. MinVersion27.0 — опубликованный контракт,
не установленная доступность. MaterialPropertyGroup, упомянутый модельным API,
не имеет собственной страницы в этом наборе; такой пробел не считается закрытым.

### Import and source interpretation

ImportOptions file **string**, sequence/forceAlphabetical booleans, importAs numeric
enum: establish host-provided construction/enum exports before generating installer
code. Page mentions constructor without documenting full signature/export location;
don't invent `new app.ImportOptions(...)` or copy ExtendScript constructor. With
supported options instance/file, canImportAs(type) gates assigning importAs; a number
in filename isn't proof contiguous valid sequence. isFileNameNumbered returns object
{isNumbered,num}, not tuple. UXP official rangeStart/rangeEnd are **documented here**,
unlike pinned ExtendScript research exclusions: keep language-specific status.

For explicit sequence clipping, forceAlphabetical must be false and rangeEnd nonzero
before rangeStart; ordering still depends valid initial endpoints, so inspect them
and validate finite intended start<=end. Invalid setter can reset entire range to all
files before throwing; catch isn't rollback. Out-of-sequence end creates missing
frames, not safe clamp. Reject unsupported/ambiguous initial state and read both
endpoints before importing; never retry mutated options blindly. No sequence index
base/frame filename mapping or complete constructor contract inferred from prose.

FileSource.file read-only path; replace via owner FootageItem main-source methods or
owner AVItem proxy methods. reload boolean, **mainSource only**. missingFootagePath
diagnostic doesn't authorize file access; still/missing/audio/video gates distinct.
Interpretation workflow snapshots fields only where meaningful: hasAlpha gates
alphaMode/invertAlpha/premulColor; invert ignored when alpha ignored. premulColor
table uses lowercase alphaMode.PREMULTIPLIED (source enum spelling discrepancy),
don't invent export from that typo. No full component range/color-management contract.

Non-still timing: conformFrameRate0 selects native only with pulldown OFF; enabling
pulldown from0 sets conform to native. Field separation OFF forbidden while pulldown
on; highQualityFieldSeparation requires non-still and fields enabled; loop disallowed
for still. Safe requested reset: snapshot → pulldown OFF → fields OFF → conform0,
checking readback at each step; enabling fields/pulldown follows explicit supported
enum policy. displayFrameRate conform/native without pulldown, conform*0.8 otherwise.
guessAlphaMode/guessPulldown are **mutations**, boolean results and best estimates,
not analysis-only ground truth or universal decoded-pixel validation.

### Relink/proxy operation: fresh owner, not cached source

Concrete controlled relink design: user approves owned item ID and destination path;
resolve item in current project → verify expected source role/type/not stale → snapshot
interpretation/reference metadata → Undo under published app contract → replace(path)
boolean gate → re-read item.mainSource and dimensions/duration/path → report primary/
cleanup errors independently. Replacement creates new FileSource, preserving previous
interpretation but estimating unlabeled alpha; cached mainSource isn't assumed current.
No auto-delete/retry on uncertain mutation, and no claim all pixels unchanged.

replaceWithSequence first-path + alphabetical flag; replaceWithPlaceholder name/
width/height/fps/duration; replaceWithSolid color/name/width/height/PAR. Validate typed
inputs/product bounds instead of fabricate missing parameter ranges. Proxy setters
create proxySource/useProxy true and often use user preferences rather than preserve
main interpretation; setProxyToNone clears proxy/null and useProxy false, not disk file.
Re-resolve source and reapply intentional interpretation only after valid source gates.

Footage metadata: duration/frameRate/frameDuration table RW conflicts with description
read-only linked mainSource; use conformFrameRate for timing, not direct setters.
width/height mutable only SolidSource. file table string but description **null** for
non-FileSource: branch actual value before string operations. typeName localized,
ID save/reload persistent but changes on import, usedIn copied; name changes don't
rename file. selected is selection mutation, not command permission; label preset
indices0..16, comment max15999 bytes after encoding. frameTime frames/time seconds
direct preview state, not comp time-remap; still time setter error. parentFolder
organization separate from source path; dynamicLinkGUID not render/content hash.
isMediaReplacementCompatible includes cycle/media restrictions, not exported MOGRT PASS.

openInViewer can open missing/placeholder footage but not successful decode evidence.
Guide overloads retain opposite argument order as above; getRenderGUID returns
DeferredCall, no guessed Promise/cancel integration. remove deletes project item only,
never disk content; users of source can be affected, so not automatic relink rollback.

### Output module configuration, not completed render

Owned RenderQueueItem/output-module path first, not project-wide collection. Inspect
templates locally → select explicit available name → applyTemplate boolean → read
getSettings format intentionally (settable subset versus display/numeric) → validate
requested keys → setSetting(key,String) or setSettings(Object) boolean → fresh readback.
Don't port arbitrary numeric value into setSetting String signature or use display
strings as locale-independent stable IDs. Templates belong current installation;
saveAsTemplate changes local persistent configuration, not project-only Undo.

normalizeSettings accepts returned-shape object and collapses Output File Info Base
Path/Subfolder/File Name to tokenized File Template. It isn't filesystem path
authorization, token expansion evidence or universal codec compatibility validator.
OutputModule.file table **string** contradicts prose ExtendScript File object;
retain mismatch, don't emit `.fsName` without target evidence. Assign path only under
qualified UXP string contract and inspect normalized settings/path after template edits.
includeSourceXMP deliberately opted-in metadata leakage policy, postRenderAction
numeric enum not documented map here; no magic IDs or unintended reimport default.

remove throws for last module, otherwise boolean; update collection ownership/freshness
after mutation. Name read-only, templates copied/local list not license entitlement.
Prepared settings/true return/output path isn't successful render: completion status,
decoded files/time/frame coverage and requested color/audio settings require actual
render evidence. No media import/relink/proxy/output/UXP host execution in this review.

### Render queue preparation and lifecycle — full pinned review2026-10-08

RenderQueue/RenderQueueItem/RQItemCollection/OMCollection full pages at official pin
read; общий coverage приведён в начале главы. All reviewed
members27.0. Queue contains **all** user items: render() isn't scoped to newly added
item, so don't trigger unattended queue-wide side effects as part of import/setup.

Concrete prepare-only command, from validated current CompItem and idle queue:
queue.items.add(comp) → keep returned owned item, not stale index → choose available
Render Settings template/applyTemplate boolean → explicitly set valid timeSpanStart/
timeSpanDuration seconds and skipFrames0 → configure owned outputModule(1) under
previous section → verify settings/path/time → set item.render=false until user
separately approves queue launch. Setting render false unqueues item, true queues;
status itself read-only. Validation occurs before mutation; failure can leave created
item, report it, don't silently delete existing user queue entries or retry add.
New output modules via item.outputModules.add(), refresh length and1-based
getByIndex, never append array or confuse project collection. Last module removal
throws. remove RenderQueueItem removes queue entry, not composition/file; changing
comp requires explicit delete/new item, not assignment to read-only comp.

Render item inspector covers comp/comment/logType/numOutputModules/outputModules/
queueItemNotify/skipFrames/startTime/status/templates/timeSpan/render. startTime
table Number versus description day/time or null isn't documented JS Date schema:
preserve raw diagnostic, no invented epoch conversion. elapsedSeconds render cost,
not frame coverage. skipFrames0..99 changes frame sampling (1 every other frame),
not output duration. Notification flags at item/queue level external user policy,
not output success. getSettings(format) selects STRING/NUMBER and SETTABLE subset;
setSetting signature String contradicts prose string-or-number: prefer declared String
or explicit setSettings object and qualify target. setSettings boolean isn't atomic
all-fields rollback; read actual affected values. saveAsTemplate persistent local
change separate from project-only edits. duplicate DONE becomes QUEUED: immediately
review/unqueue owned duplicate to prevent accidental extra render.

Launch policy: user sees **every queued item**, requested frame ranges, outputs,
overwrite/missing-media concerns before explicit approval. queue.rendering true means
in-progress **or paused**, not terminal failure. render(skipCheck=false) synchronous
void until complete; no boolean-success gate. renderAsync(skipCheck=false) boolean
launch result, **not Promise/completed file evidence**. Default false retains missing-
source check; true intentional degraded missing-footage render, not recovery repair.
pauseRendering(true/false) and stopRendering boolean commands don't instantly prove
all files finalized or interrupted output cleaned. showWindow boolean only UI action.

RenderQueueItem.onStatus/onComplete/onReorder are callback registration methods,
not ExtendScript string onstatus field. Varargs callback contract doesn't describe
payload, order, exactly-once, thread, unsubscribe/removal, or plugin-reload lifetime.
Don't invent event listener return disposer or null-unregister. Before shipping
interactive observer, resolve these gaps. With qualified registration, use generation
gate and re-read actual item status; stale UI suppression never cancels host render.
Blocking render doc suggests pause/stop from status/app.onError callback, but absence
of full reentrancy contract means no arbitrary project mutation during callbacks.
No mandatory all-example host testing added; missing delivery contract remains visible.

Terminal status must inspect actual enum (DONE/ERR_STOPPED/USER_STOPPED versus
QUEUED/UNQUEUED/NEEDS_OUTPUT/RENDERING/WILL_CONTINUE), then validate decoded output
files/requested coverage. onComplete invocation alone not DONE guarantee. lastError
session-only most recent failed render, can be stale relative requested operation;
empty string isn't positive success evidence. Record before/after context without
clearing undocumented field. canQueueInAME means queued AE items exist, not AME
installed/reachable/licensed. queueInAME(false) queues, true also starts processing;
boolean enqueue isn't AME terminal render or exported file PASS. No queue/AME/output/
callback/runtime observations executed in this source review.

### Preferences/settings and live views — full pinned review2026-10-08

Six full pages Preferences/Settings/Viewer/View/ViewOptions/GuideOptions read at
official pin; общий coverage приведён в начале главы.
Host-side preference stores differ from shared UXP plugin storage and AEP project.

Concrete plugin-only small UI setting: app.settings.haveSetting(ownedSection,key)
→ getSetting String or explicit default → bounded schema/version/enum validation
→ on deliberate user change saveSetting(ownedSection,key,String) boolean → readback.
No arbitrary eval of stored text, password/token/private project snapshots, or assumed
inter-plugin privacy. prefType optional file selector; specify intended host-provided
enum when needed, not hardcode integer. Settings has **no deletion method documented**;
no invented removeSetting or automatic Preferences-key deletion for another namespace.
No copied ExtendScript byte limit/default-section-prefix guarantee at this pin.
Persisted true/readback doesn't prove survive restart or portable across AE versions.

Preferences typed access: havePref before getPrefAsBool/Float/Long/String; validate
finite number, integer for Long and intended bounds/type. Explicit owned section/key/
prefType; default machine-specific file is not project preference. savePrefAsBool/
Float/Long/String and deletePref return boolean: snapshot **existence and typed value**
before changing, restore value if existed or delete only newly created owned key.
Missing isn't false/zero/default. Never change hidden security/GPU/cache prefs by
guessing key names or treat preference change as Undo-able project mutation.
saveToDisk/reload affect host preference-file state globally; source wording says
restart otherwise needed, not a guarantee every host subsystem immediately reacts
to reload. Obtain consent for global flush/reload and avoid overwriting concurrent
user changes on restore; unknown outcome/error remains reported, not blind retry.

Viewer active/focus and maximized are UI state, type numeric viewer role; views Array/
numViews, activeViewIndex **index base unspecified in this UXP page**. Don't port
ExtendScript1-based viewer index or general JS0-based assumption into setter wrapper.
Retain object from deliberate supported openInViewer operation where possible, refresh
after project/view close/reload and verify type. setActive boolean changes focus; not
activeComp selection authority or render camera. View.options read-only reference to
mutable ViewOptions, View.setActive boolean and stopPlayback boolean UI operations,
not render-queue stop. No playback start or automatic camera selection API invented.

Concrete qualified view command: use caller-resolved live View from validated viewer
→ snapshot options.zoom/checkerboards/rulers/guidesVisibility/guidesLocked/guidesSnap
→ set intended zoom1.0 (100%) and requested UI flags → readback → report changed
view; restore only with explicit user policy and if same valid view still owned.
zoom range0.01..16 normalized, not percent100; exposure changes display not exported
pixel truth. channels numeric enum requires actual enum contract, not guessed RGBA
IDs. fastPreview access throws in Layer/Footage viewer; draft prose specifically
ray-traced and Classic3D error, not modern Advanced3D capability matrix. Retain dated
renderer wording rather than claim universal draft support. No screenshot/color/
render equality inferred from UI options or checkerboard visibility.

GuideOptions color exactly3 finite0..1 RGB; orientation horizontal/vertical, position
PIXEL/PERCENTAGE with finite constraints (host clamps ±100000px/±300%). Validate
product bounds before setter instead of rely silent clamp. pinned anchors opposite
edge (bottom/right), not frozen position/locked guide; guidesLocked view option
different scope. Read getGuideAsObject before partial update and preserve other
fields/units; positional overload moves pixel position while object form interprets
positionType, opposite index argument order remains. No constructor/export signature
for GuideOptions from this page: use returned supported object, not invented class.
Expected guide UI state not rendered artifact. No preference/disk/reload/view/guide/
UXP host runtime executed; index/enum/renderer gaps remain unresolved contracts.

### Font picker and typed animation values — full pinned review2026-10-08

Full Font/Fonts/Shape/KeyframeEase/MarkerValue pages read. No classes/constructors/export locations
invented from matching ExtendScript names; obtain supported returned values and
review target Property write-back contract separately.

Concrete font picker: capture fontServerRevision → allFonts family arrays → exclude/
flag substitutes deliberately → show nativeFamily/Style/FullName for non-Latin UI,
keep internal postScriptName/technology/type/version/fontID for disambiguation →
before apply recheck revision/getFontByID and validate requested glyph String.
fontID stable **current session**, not persistent installed-font identity; unknown/
removed ID gives undefined despite table Font return. Empty location valid, no
guaranteed disk path or license to bundle font. familyName/fullName/styleName ASCII
versus native Unicode fields; isFromAdobeFonts doesn't prove current entitlement.
Duplicate PostScript/family+style lookup arrays may contain several; index0 primary
for TextDocument.fontObject route but not user-intended face identity. Explicitly
present substitution/duplicate policy, don't silently choose first for exact typography.

findFirstFontByFamilyNameAndStyleNameWithFallback always returns {font,matched}:
nonempty font isn't exact match. hasGlyphsFor returns support for **every character**,
no failing-character list or shaping/ligature/visual equivalence guarantee.
writingScripts/getCTScriptForString return script metadata/counts, empty String gives
empty list; not complete glyph coverage or grapheme count. getDefaultFontForCTScript
has **no guarantee even one mapped glyph exists**. Default change accepts non-variable
Font, returns true changed/false already equal; null resets launch default, not previous
custom mapping. Snapshot previous actual Font for intended restore and avoid concurrent
global edits; favorite/mru family lists and sync-freeze/replacement policy are global
UI/font behavior, not AEP-only project settings. otvLookupTable marked internal naming
table, don't build required public font resolver on its undocumented stability.

Variable fonts: hasDesignAxes first; designAxesData ordered {min,max,default,name,tag},
designVector same-length ordered values; non-variable design fields undefined despite
some primitive types. Validate finite values per axis bounds before
postScriptNameForDesignVector(vector), read-only Font.designVector isn't setter.
familyPrefix/designVectorIsDefault/otherFontsWithSameDict/hasSameDict distinguish
dictionary/instances, not all same-name files; hasSameDict true only variable pair.
Lookup-generated PS name alone isn't proof instantiated/installed/resolved design
vector; actual lookup/TextDocument readback remains required. Folder poll returns true
**scheduled asynchronous update**, not completed new-font availability. Refresh via
revision/user-driven bounded UI, no aggressive polling or fabricated Promise await.
freezeSyncSubstitutedFonts disables auto AdobeFonts sync attempt, not removes installed
fonts or grants access. No download/install/cloud/runtime observations performed.

KeyframeEase influence finite0.1..100, speed units depend property/key type; do not
normalize spatial px/sec and scalar degrees/sec identically or assume zero valid
influence. Value fields mutable, applying ease belongs Property per-dimensional arrays;
no `new app.KeyframeEase` signature promised here. Snapshot matching typed easing
through supported Property and re-read actual interpolation separately.

Shape path edit design: valid returned Shape → preserve closed/vertices/inTangents/
outTangents and feather metadata → validate finite2D pairs/equal tangent lengths →
modify requested points → supported Property setter and readback. RotoBezier ignores
stored tangent edits; closed connects endpoints but isn't duplicate final vertex.
No expression createPath/points syntax in UXP Shape. Feather arrays one record per
feather point with segment number **zero-based**, relative location0..1, tensions0..1,
types0 outer/1 inner, interps0 non-Hold/1 Hold; inner radii negative, corner-angle
relative **percentage** not world degrees. Topology insertion/removal can invalidate
segments/feather mapping: preserve under compatible edit or explicit remap policy,
don't blindly copy old feather indices to new topology. Page lacks complete topology/
degenerate/empty-path/coordinate contract, no invented minimum vertex/ABI rule.

MarkerValue comment/chapter/cuePointName/frameTarget/url String, eventCuePoint bool,
duration seconds, label0..16 presets (not custom RGB), protectedRegion comp/nested-
comp protected markers, not ordinary layer marker universal flag. Marker metadata
stays inert/untrusted; validate bounds/types, no eval/open URL during rig evaluation.
getParameters returns **object string-key/value map**, setParameters Object boolean:
not ExtendScript flat alternating pair array or expression MarkerKey.parameters
write operation. Copy owned bounded plain fields, reject unexpected inherited/schema
keys and preserve unrelated user parameters intentionally. UI three-param limit not
API limit, but impose product size bound. Changing detached value not proven host
marker write until Property set/readback; duration bar isn't automatic playback/retime.
No font/ease/path/marker/UXP host runtime or full animation contract PASS.

### Project folders and generated sources — full pinned review2026-10-08

Полностью прочитаны FolderItem/ItemCollection/SolidSource/PlaceholderSource/
DeferredCall/index. Index содержит43 object links и подтверждает модуль
require("aftereffects"), но не задаёт constructor/enum exports или shared-platform
setup contract. Общий актуальный coverage указан в начале главы.

Owned project-folder organization: known supported collection.addFolder(name) returns
folder under that collection's owner (project/root→root, nested folder→that folder).
addComp follows same parent policy, so create directly in intended collection when
supported. Existing items move by item.parentFolder assignment after checking current
project, target owner and cycle prevention under product policy; no OS folder creation.
Folder.item(1..numItems) enumerates **direct children**, numItems/items.length not
recursive descendants. Snapshot approved target IDs before reorder/move and re-resolve
within actual owner; collection.itemByID **throws absent**. Project.layerByID has
an explicitly nullable missing-result contract; Project.itemByID does not specify
the absent-result behavior. Moving item out of folder can make owner-scoped ID lookup fail
without deleting it. Do not call private_itemAtIndex (explicit internal helper);
no public getByIndex method invented on this ItemCollection page.

Folder name/comment/label/selected metadata and inherited IDs/typeName/GUID obey
earlier item rules: locale typeName not stable type test, encoded comment limit,
selection not command authorization. remove **recursively deletes project contents**,
not disk; never use as automatic compensation for partially failed folder command
when user items might have been moved into it. Guides/setGuide inherited rows are
published on FolderItem but meaningful viewer behavior not independently specified:
don't infer real folder video viewer/guide rendering from duplicated table.

SolidSource color RGB0..1 exactly3 components: user-approved owned solid's mainSource
→ validate role/current owner → snapshot RGB → write finite intended color → readback.
Shared source used by many layers/comps means edit affects every consumer; duplicate/
replace only with explicit ownership policy, no silent global brand-color update.
Inherited alphaMode/invertAlpha/premulColor only meaningful when hasAlpha/appropriate
mode; normal solid isStill, so loop/conform/field/pulldown settings aren't universally
usable just because rows RW. Reuse FileSource interpretation dependency rules where
non-still supported, not assume SolidSource gains file/reload from similar base.

PlaceholderSource has no file-path/reload or new creation methods; replacement belongs
FootageItem.replaceWithPlaceholder/replace and proxy owner methods. isStill true
duration0 placeholder, nonzero placeholder timed per description; inspect actual
value before conform/loop/field/pulldown writes. Display/native/conform rates aren't
decoded media or filled missing frames. guessAlpha/Pulldown mutate estimates with
no-change hasAlpha/isStill gates as above. No missingFootagePath field fabricated for
all placeholders from FileSource contract. Full inherited source-row review doesn't
promise actual footage import/replacement success, dimensions/ranges or visual output.

Собственная pinned страница DeferredCall перечисляет только **duration** —
read-only elapsed seconds. Однако описания layer `getRenderGUID` прямо упоминают
получение результата через **`.wait()`**. Это межстраничный пробел полноты: нельзя
говорить, что способ получения результата вообще не упомянут, или считать duration
индикатором завершения. Полный контракт ожидания и ошибок разобран в разделе
[Deferred render](#deferred-render-promisecancel-api). Runtime в этом обзоре NOT_RUN.

### Application, Project и CompItem — полный pinned review, 2026-10-08

Три полные страницы прочитаны на общем official pin; их SHA256 совпали с inventory.
Здесь дополнены операции, которых не хватало в начальном примере создания comp.
Общие правила identity, selection, import, queue и DeferredCall описаны ниже и выше
в этой главе; повторённые строки не означают новый независимый контракт.

#### Application: жизненный цикл и глобальные настройки

[Application](https://github.com/AdobeDocs/uxp-after-effects/blob/7d1cd01b4c69a9e02b77d48b3f919a6145a90841/src/pages/after-effects-api/application.md)
публикует `openFast`: в UXP это документированный метод, хотя ExtendScript review
оставляет одноимённый API в research scope. Он пропускает часть проверок открытия;
обычный сценарий открытия не нуждается в такой оптимизации. `newProject` может
вернуть null после отмены. Перед переключением документа сохраните решение
пользователя о текущем проекте; отсутствие нового объекта не разрешает повторять
команду или отбрасывать изменения.

`beginSuppressDialogs`/`endSuppressDialogs` балансируются только после успешного
начала. `getAppTheme`, `getUseReducedContrast`, `getAllowedAppThemes` — **read-only
свойства**, несмотря на имена; не вызывайте их как функции. Поиск menu command ID
зависит от локализации и не заменяет прямой опубликованный метод.

`scheduleTask` принимает строку JavaScript и возвращает ID. На этой pinned странице
**нет `cancelTask`** и полного контракта context/lifecycle. Рекомендуется одноразовая
задача с фиксированным кодом, проверкой актуальности проекта и ограниченным сроком
действия; не интерполируйте входные данные в исполняемую строку. Бесконечный repeat
без подтверждённой остановки не подходит панели с reload/unload.

`setMultiFrameRenderingConfig` описан для следующего render с восстановлением после
script; срок такого scope у постоянной UXP панели не уточнён. Исторические пределы
памяти в `setMemoryUsageLimits` не являются актуальной моделью RAM. Purge, Watch
Folder, quit/restart и отключение rendering — отдельные глобальные действия.

#### Project: настройки, сохранение и совместная работа

[Project](https://github.com/AdobeDocs/uxp-after-effects/blob/7d1cd01b4c69a9e02b77d48b3f919a6145a90841/src/pages/after-effects-api/project.md)
документирует `dirty` как read-only UXP свойство; ExtendScript research-статус сюда
не переносится. `textSelection` также read-only: layer ID, время слоя и диапазон
символов описывают выбор, но не setter выделения. Получайте слой заново перед правкой.

Для команды настройки проекта сначала соберите профиль и изменяйте только явно
запрошенные поля. `gpuAccelType` выбирается из `app.availableGPUAccelTypes`.
`workingGamma` игнорируется при заданном `workingSpace`; `linearBlending` и
`linearizeWorkingSpace` — разные настройки. Смена frame-count policy может менять
`displayStartFrame`. Проверяйте зависимые значения после записи; не называйте
прочитанные числа доказательством одинакового изображения.

`save`/`saveWithDialog` возвращают boolean; false не подтверждает сохранение.
`replaceFont` возвращает **void** и не поддерживает Undo. `reduceProject`,
`removeUnusedFootage` и `consolidateFootage` возвращают количество удалённых элементов,
поэтому ноль может быть успешным результатом. Общий helper «все методы дают true»
неверен. У `setDefaultImportFolder` prose допускает сброс без аргумента, а таблица
не помечает path optional; эту неоднозначность нельзя скрывать wrapper-ом.

Team Projects требуют проверки доступности и отдельного намерения пользователя
для share/sync/conflict resolution. Application.openTeamProject описывает identifier,
Project.openTeamProject — name; не объединяйте их по названию. Доступность команды
не выбирает сторону конфликта за автора проекта.

#### CompItem: время, presets и экспорт

[CompItem](https://github.com/AdobeDocs/uxp-after-effects/blob/7d1cd01b4c69a9e02b77d48b3f919a6145a90841/src/pages/after-effects-api/compitem.md)
разделяет `frameTime` в кадрах и `time` в секундах; для начального номера кадра
есть `displayStartFrame`, позволяющий избежать float-деления. Выбирайте `renderer`
из `renderers`, а не из названия GPU. `activeCamera` может быть null.

`applyPreset(path)` затрагивает **выделенные слои**, а при пустом выделении создаёт
solid. Получатель вызова не является единственной целью. Команда должна явно
зафиксировать разрешённое выделение и обработать его изменение до запуска.
`duplicate()` создаёт CompItem, но не обещает рекурсивную независимую копию всех
вложенных источников. `remove()` удаляет project item, не файл на диске.

Для MOGRT: выбрать comp → явно решить сохранение dirty проекта → задать имя
template и разрешённый output path → отдельно согласовать overwrite → вызвать
`exportAsMotionGraphicsTemplate` → проверить boolean и фактический результат.
У controller name get/set отсутствует index-base contract; не придумывайте цикл
переименования от 0 или 1. Deferred frame/GUID results рассмотрены отдельно.

`markerProperty` имеет тип Property в таблице и PropertyGroup в описании — конфликт
сохранён, без неподтверждённого type cast. `counters` здесь опубликован, но описан
как общий для приложения no-op: на нём нельзя строить полезную функцию или метрику.

#### Общий шаблон команды

Рекомендуемый SOURCE EXAMPLE design: проверить запрос → заново получить владельца
и цель → сохранить необходимые исходные значения → открыть предусмотренную Undo
group → выполнить одну операцию → прочитать результат → завершить group → вернуть
primary/cleanup ошибки раздельно. Конкретный return contract выбирается по методу.
После частичной записи сообщайте, что осталось изменённым; автоматический retry
может создать дубликат, повторить экспорт или потерять пользовательскую правку.
Сохранение, облачная синхронизация, изменение глобальных настроек и non-undoable
операции требуют собственного пользовательского сценария, а не обещания общего
rollback. Это описание команды для разработчика; AE UXP runtime **NOT_RUN**.

### Слои: создание, редактирование и повторное чтение — review 2026-10-08

Полностью прочитаны Layer, LayerCollection, AVLayer, ShapeLayer и TextLayer на
официальном pin `7d1cd01b4c69a9e02b77d48b3f919a6145a90841`; SHA256 совпадают
с inventory. Это 371 повторяемая строка/заголовок, не 371 уникальный контракт.
**DOCUMENTED** — опубликованные условия, Min Version 27.0; **SOURCE EXAMPLE** —
последовательности ниже; **RUNTIME-NOT-CLAIMED** — выполнение в AE не заявлено.

При создании учитывать отдельно слой и созданные project items; при изменении
существующего объекта — зависимости других слоёв и композиций. Общая схема команды
описана в блоке Application/Project выше. `locked` рекомендуется учитывать как
намерение пользователя; `remove()` изменяет документ, не освобождает JS wrapper.
Ошибки основной операции, восстановления selection и закрытия Undo сообщать отдельно.

#### LayerCollection: выбирать способ создания

[Официальный контракт](https://github.com/AdobeDocs/uxp-after-effects/blob/7d1cd01b4c69a9e02b77d48b3f919a6145a90841/src/pages/after-effects-api/layercollection.md).

`byIndex` использует 1..length; `relativeTo` прибавляет смещение к индексу слоя
этой композиции; `byName` возвращает верхнее совпадение или null. Перед структурной
операцией переводить сохранённые идентичности в свежие индексы.

| Создание | Особенность UXP |
|---|---|
| `add(item, duration)` | duration действует на still; старт зависит от preferences |
| `addSolid` | Создаёт SolidSource, project FootageItem и AVLayer; RGB 0..1, размеры **1..30000**, PAR 0.01..100 |
| `addNull` | Возвращает AVLayer; optional duration |
| `addShape` | Пустой ShapeLayer; содержимое добавляется отдельно |
| `addText / addVerticalText` | String либо TextDocument; в Returns AVLayer, в описании TextLayer |
| `addBoxText / addVerticalBoxText` | Размеры массива + необязательный String, возвращают TextLayer |
| `addCamera / addLight` | Имя и centerPoint; у камеры это XY Point of Interest, z=0 |
| `addParametricMesh` | Имя и числовой тип; экспорт enum здесь не раскрыт |

Вертикальные text-методы задают VERTICAL_RIGHT_TO_LEFT, обычные — HORIZONTAL.
`precompose(indices, name, flag)` возвращает CompItem, переносит слои; false разрешён
для единственного индекса, default true. Рекомендуется после вызова перечитать обе
композиции, timing, parenting и зависимости. Не выводить сохранение всех выражений
из самого возврата CompItem. Границы размеров UXP не подменять ExtendScript-границами.

#### Layer: идентичность, структура, presets

[Официальный контракт](https://github.com/AdobeDocs/uxp-after-effects/blob/7d1cd01b4c69a9e02b77d48b3f919a6145a90841/src/pages/after-effects-api/layer.md).

ID сохраняется при save/reload, меняется при импорте проекта; `index` — позиция,
`propertyIndex` у Layer undefined. `isNameSet` — явное имя, не владение инструментом.
`startTime/inPoint/outPoint/time` используют composition seconds; stretch — проценты,
100 без изменения, ненулевые величины между −1 и 1 ограничиваются до ±1.

Для reparent выбрать: `parent = target` компенсирует transforms; `setParentWithJump(target)`
сохраняет локальные числа, возможен скачок. **Аргумент обязателен**: вызов без него
не является UXP-командой удаления parent. `parent = null` описан отдельно.
Рекомендуется отклонять циклы и проверять нужные моменты анимации.

`duplicate()` возвращает Layer, не меняя selection. `copyToComp` добавляет копию сверху;
`moveBefore/moveAfter/moveToBeginning/moveToEnd`, copy и remove возвращают boolean. Проверять
фактический порядок; `moveTo` относится к indexed properties, не универсальной
перестановке слоёв.

`applyPreset(stringPath)` действует на selection композиции; пустая selection создаёт
solid. Рекомендуется сохранить selection, выделить точные цели, вызвать один раз,
проверить изменения и восстановить доступные цели. `savePreset(stringPath)` сохраняет
выделенные свойства в .ffx, false возможен при пустом выборе. Файловое действие
требует отдельной политики пути/перезаписи, не Undo-обещания.

#### AVLayer: источник, matte и capability gates

[Официальный контракт](https://github.com/AdobeDocs/uxp-after-effects/blob/7d1cd01b4c69a9e02b77d48b3f919a6145a90841/src/pages/after-effects-api/avlayer.md).

`source` read-only; `replaceSource(item, fixExpressions)` возвращает boolean.
Рекомендуемый сценарий: проверить новый источник/циклы → сохранить source/timing/
expression policy → заменить → перечитать source и затронутые значения; такая
операция не равна замене общего FootageItem.

`setTrackMatte(layer, type)` возвращает boolean; null отсоединяет matte.
`removeTrackMatte()` сохраняет тип, `trackMatteType = NO_TRACK_MATTE` удаляет и
сбрасывает тип. Считать вместе `trackMatteLayer/hasTrackMatte/type`, затем проверять
результат композитинга. Capability gates для remap/collapse проверять перед setter;
после смены структуры заново получать свойства.

`hasAudio`, `audioEnabled`, `audioActiveAtTime` различают наличие компонента,
переключатель и временную активность. `frameBlending` read-only; тип, quality,
sampling, blur, effects и blending — отдельные настройки. Их значения не являются
доказательством готового аудио/изображения. Числовые enum-поля не раскрывают место
экспорта констант.

Для Media Replacement сначала `canAddToMotionGraphicsTemplate(comp)`. У
`addToMotionGraphicsTemplate` Returns boolean противоречит описанию **undefined**
при отказе; вариант As описан true/false. Не считать `result !== false` успехом:
только true подтверждает добавление, далее нужен readback. Регистрация контроллера
не экспортирует MOGRT. Scene detection запрещена для non-video/remapped video;
NONE анализирует, другие режимы изменяют структуру — после них обновить цели.

#### ShapeLayer: содержимое и неоднозначная геометрия

[Официальный контракт](https://github.com/AdobeDocs/uxp-after-effects/blob/7d1cd01b4c69a9e02b77d48b3f919a6145a90841/src/pages/after-effects-api/shapelayer.md).

Рекомендуемый сценарий после `addShape()`: найти подтверждённую vector-группу →
выбрать path/fill/stroke → проверить возможность добавления → выполнить структурный
шаг → заново получить свойства → записать значения по отдельным контрактам
Property/Shape → перечитать topology, цвет и порядок. Пустой слой и true от команды
не доказывают видимый контур. Не придумывать vector matchNames или constructor
Shape из этой страницы.

Повторяемые AVLayer-поля не гарантируют применимость: `lightType` прямо запрещён
для non-light; строки source/audio/remap/font-axis не превращают shape в media/text.
Сокращённое описание подкласса не отменяет более подробные условия операции.

Документация геометрии требует разбирательства:

| Member | Пробел между страницами |
|---|---|
| `calculateTransformFromPoints` | ShapeLayer: третий угол **bottom-left**; AVLayer/TextLayer: **bottom-right** |
| `compPointToSource / sourcePointToComp` | ShapeLayer явно требует [x,y,z]; AVLayer/TextLayer пишут только number[] |
| `sourceRectAtTime(..., true)` | ShapeLayer обещает blur/shadow extents; AVLayer/TextLayer описывают расширение shape bounds |
| `openInViewer` | ShapeLayer обещает Layer panel; TextLayer говорит, что text и shape там не открываются |

Рекомендация: не выпускать общий wrapper геометрии/автообрезки, пока нужная трактовка
не подтверждена для целевого build; UI-инспекцию строить без обязательного Layer panel.
Это ограничение конкретных продуктовых обещаний, не требование host-test всей Библии.

#### TextLayer: текстовая операция, а не замена media source

[Официальный контракт](https://github.com/AdobeDocs/uxp-after-effects/blob/7d1cd01b4c69a9e02b77d48b3f919a6145a90841/src/pages/after-effects-api/textlayer.md).

`source` у TextLayer null. Содержимое редактировать через проверенный Source Text
property-path и отдельный контракт TextDocument/Property, не `replaceSource`.
Рекомендуемый сценарий: после typed creation получить текущий текст → определить
static/key/time policy → изменить нужные поля → записать → получить свежие значения
и проверить текст/шрифт/компоновку. Наличие TextLayer не доказывает доступность шрифта
или отсутствие overflow.

`threeDPerChar` относится к per-character 3D. `addVariableFontAxis(tag)` применяется
только на `ADBE Text Animator Properties`, возвращая Property; tag четырёхсимвольный.
После `addProperty` indexed group пересоздаётся, старые ссылки недействительны;
перечитывать группу после каждого добавления. В описании canAddProperty mask-пример
сужен до «only legal», хотя addProperty перечисляет text/effects: не превращать
пример в общий запрет.

`openInViewer()` по TextLayer возвращает null вопреки Returns Viewer.
Координатные преобразования отражают первый символ в текущий момент, не весь
per-character rig. Обе EGP add-формы здесь описывают undefined при отказе; это
не регистрация обычного текстового контрола и не наследуемая true/false-гарантия.

**Уточнение DeferredCall:** Layer/AVLayer/TextLayer `getRenderGUID` прямо упоминают
`.wait()` для получения GUID. Это документированное описание вызова, отсутствующее
в собственной таблице DeferredCall; неверно утверждать полное отсутствие способа
получения результата. Блокирующее поведение, cancellation, errors и общий lifecycle
не раскрыты. Не выдумывать Promise/await API, thread permission или гарантию файла.

### Свойства, ключи, маски и текст — полный pinned-review 2026-10-08

Полностью прочитаны семь официальных страниц: Property/PropertyGroup/
MaskPropertyGroup/TextDocument/CharacterRange/ParagraphRange/ComposedLineRange,
283 строки свойств и заголовка методов с учётом наследуемых повторов. SHA256
совпадают с inventory для `7d1cd01b4c69a9e02b77d48b3f919a6145a90841`.
Их опубликованная граница — **27.0**, отдельно от версий ExtendScript и наличия
поддержки в конкретной установке. Evidence: DOCUMENTED; операции ниже —
SOURCE EXAMPLE / RUNTIME-NOT-CLAIMED.

Общая схема команды приведена в блоке Application/Project. Для этих операций
дополнительно выбрать static/key/time policy и сохраняемые части значения.
Обычный JSON-снимок не является универсальным клоном типизированных host-значений
или смешанного оформления. Проверять именно запрошенные поля и заново получать
свойства после структурной правки; старый диапазон не гарантирует актуальный layout.

#### Property: выбрать правильную запись и проверить результат

Источник: [Property](https://github.com/AdobeDocs/uxp-after-effects/blob/7d1cd01b4c69a9e02b77d48b3f919a6145a90841/src/pages/after-effects-api/property.md).

`propertyType/propertyValueType` read-only; `hasMin/hasMax` защищают бросающие
`minValue/maxValue`. `value` включает expression; исходное значение:
`valueAtTime(time,true)`. `numKeys=0` не исключает expression.

| Намерение | Контракт записи |
|---|---|
| Статическое значение | `setValue` только без ключей |
| Существующий ключ | `setValueAtKey`; отсутствующий ключ — ошибка |
| Значение в момент | `setValueAtTime` создаёт ключ при необходимости |
| Несколько моментов | `setValuesAtTimes`: одинаковая длина массивов |

Все четыре метода возвращают **void**: проверка `===true` ошибочна. Expression:
`canSetExpression` → источник, `expressionEnabled/expressionError`
и выбранные моменты; пустая ошибка не доказывает корректность всей анимации.

Снимок ключа включает время/значение, interpolation/ease, пространственные параметры,
label/selection. Spatial-операции требуют spatial-свойства; крайние ключи не rove.
Удалять ключи с конца. Разделённые dimensions имеют followers с нулевой нумерацией.
Не смешивать scalar follower и vector leader.

Неясности source: размер temporal-ease массива обобщён через размерность;
`setSpatialTangentsAtKey` дублирует `inTan`, но поясняет второй аргумент как
`outTan`; `setPropertyParameters` возвращает Property без полного контракта строк.
У `LayerInputStageType` документирован accessor экземпляра, числовая карта не дана;
фраза «raw effect index, 0-5» не задаёт универсальный порядок стадий.
Перед wiring заново получить `getInputStageCycleSafeLimit`, после — читать
`inputLayerAndStage`. Числовое `<=` и числа из ExtendScript не обоснованы.

Media replacement требует обеих capabilities. Для dropdown заранее спланировать
миграцию keys/values; перечитать возвращённую Property. EGP-add и source-swap
не подтверждают render.

#### PropertyGroup: структура и ссылки после изменения

Источник: [PropertyGroup](https://github.com/AdobeDocs/uxp-after-effects/blob/7d1cd01b4c69a9e02b77d48b3f919a6145a90841/src/pages/after-effects-api/propertygroup.md).

`numProperties` считает indexed children; остальные roots нужно искать по имени.
`property(indexOrName)` проходит один уровень, indexed range — `1..numProperties`.
`matchName` не локализован, но одинаковый эффект может встречаться несколько раз:
для редактора нужен конкретный owner и occurrence. Display name/selection не
подтверждают принадлежность инструменту; `canSetEnabled` проверяется отдельно.

Добавление в indexed group пересоздаёт её и инвалидирует существующие ссылки;
`moveTo` инвалидирует siblings. Поэтому после add/reorder повторно получать группу,
соседей и нужные дочерние свойства. Сохранённый индекс помогает найти добавленное
свойство в неизменённом порядке, но не служит постоянным ID. `duplicate` возвращает
объект, `moveTo/remove` — boolean; удаление включает детей. Named-group исключение
для добавления касается text animator.

В source `addProperty` заявляет возврат PropertyGroup, а описание — PropertyBase;
после вызова проверять фактический `propertyType`. `canAddProperty` одновременно
описан общим методом и ограничен формулировкой про mask: не превращать эту фразу
в глобальный whitelist. `propertyGroup()` наверху возвращает Layer вопреки узкой
таблице возврата. Для отсутствующего child полный null/throw-контракт не указан.

`addVariableFontAxis` допустим только на `ADBE Text Animator Properties`; четыре
символа axisTag не доказывают наличие оси, а пример `wght 100–900` не заменяет
границы выбранного шрифта. Наследуемая EGP capability не делает любую группу
допустимым контроллером.

#### MaskPropertyGroup: геометрия, режим и UI — разные изменения

Источник: [MaskPropertyGroup](https://github.com/AdobeDocs/uxp-after-effects/blob/7d1cd01b4c69a9e02b77d48b3f919a6145a90841/src/pages/after-effects-api/maskpropertygroup.md).

Для изменения существующей маски повторно получить её в текущем слое, проверить
`isMask`, сохранить выбранные поля и отдельно определить static/key/time-политику
её path-свойства. Геометрию писать как поддерживаемый Shape через Property;
не конструировать неописанный UXP-класс по образцу ExtendScript.

`color` — RGB `0..1` для контура **в интерфейсе**, `locked` ограничивает UI-editing.
Ни цвет, ни lock не заменяют проверку результата маскирования или разрешение
менять пользовательскую маску. `maskMode`, `inverted`, `rotoBezier`,
`maskFeatherFalloff`, `maskMotionBlur` — самостоятельные настройки;
mode/feather/blur требуют соответствующих enum, не придуманных числовых ID.
RotoBezier-политику согласовать с сохранением tangents из раздела Shape.

`duplicate` возвращает MaskPropertyGroup; после `moveTo/remove` обновить owner и
список масок, проверить порядок и запрошенные поля. Наследуемое перечисление
`addVariableFontAxis` не разрешает добавлять ось прямо в маску: его собственный
receiver contract остаётся текстовым. Повторы `addProperty/canAddProperty` сохраняют
описанные выше неоднозначности. Проверка readback подтверждает настройки;
видимая рамка или boolean-ответ не доказывают итоговые pixels/blur/feather.

#### TextDocument: область стиля и устаревшая раскладка

Источник: [TextDocument](https://github.com/AdobeDocs/uxp-after-effects/blob/7d1cd01b4c69a9e02b77d48b3f919a6145a90841/src/pages/after-effects-api/textdocument.md).

Многие character-getters отражают первый символ, setters меняют весь текст;
paragraph-settings затрагивают все абзацы. Для локальной правки нужен range.
`fauxBold/fauxItalic` здесь **read-only**, в CharacterRange — RW.
`fontObject` имеет тип Font; фраза о PostScript name не документирует string-setter.
`font` может создать substitute. `resetCharStyle/resetParagraphStyle` возвращают
boolean и берут defaults панелей, не восстанавливают прежнее смешанное оформление.

RGB fill допускает overbright; чтение отключённого fill/stroke бросает исключение,
запись цвета включает соответствующий paint. `fontSize`: `0.1..1296`; нулевой
`strokeWidth` клипуется до `0.01`. `MULTIPLE_JUSTIFICATIONS` при записи превращается
в CENTER; composerEngine нельзя вернуть в LATIN_CJK.

Box-операции требуют `boxText`; autofit растёт вниз и отключён вне TOP.
Ненулевой first-baseline minimum перекрывает alignment. `composedLineCount` —
снимок, при полном overset может быть нулём; после записи заново получить документ.

Неясности: `leading` якобы включает `autoLeading=true`; `boxTextPos` описан
одновременно координатами и width/height; scale назван pixels. Не выводить из
этих формулировок недокументированные преобразования единиц.

Range-starts нулевые: character start допускает длину текста, line/paragraph start
должен быть меньше count. Default end=start+1, `-1` динамический конец; для вставки
явно задать одинаковые границы. `*CharacterIndexesAt` принимает индекс **символа**,
не номер строки/абзаца. Индекс не объявлен grapheme/glyph identity.

#### CharacterRange: локальная правка и tagged ranges

Источник: [CharacterRange](https://github.com/AdobeDocs/uxp-after-effects/blob/7d1cd01b4c69a9e02b77d48b3f919a6145a90841/src/pages/after-effects-api/characterrange.md).

`isRangeValid` проверять до чтения границ и после изменения текста. Замена `text`
меняет содержимое диапазона; пустая строка удаляет, нулевая ширина вставляет.
`pasteFrom` проверяет обе стороны, удаляет target и вставляет source text/style,
не меняя параметры диапазона; сокращение текста способно инвалидировать target.
Получить новые ranges перед следующей правкой и затем записать весь TextDocument
через выбранный Property setter.

Для полей с описанным mixed-результатом `undefined` означает неопределённость,
а не default. RGB fill/stroke допускает HDR; запись включает paint, чтение
отключённого paint здесь не бросает исключение, в отличие от TextDocument.
`kerning` возвращает ручное значение, а при auto/mixed — undefined;
запись выбирает NO_AUTO_KERN. Paragraph-параметры диапазона могут затронуть
абзацы, поэтому выделение нескольких символов не гарантирует узкую область
paragraph-правки. Reset берёт defaults, не предыдущие стили.

UXP дополнительно публикует `taggedRanges` с `{start,end,tag}`,
`createTaggedRange(string)` и `deleteTaggedRanges()`: создание на пустом диапазоне
возвращает false, удаление охватывает все пересекающиеся tags. Параметр `url`
описан как строковая метка; это не инструкция открыть сеть.
При общей области чужие tags могут пересекаться: перед удалением показать
затрагиваемые записи. Стабильность меток после редактирования, сериализация и
селективное удаление по tag не определены. `toString()` безопасен на invalid range,
но возвращает параметры, не текст или persistent ID.

#### ParagraphRange: границы абзаца и отдельный CharacterRange

Источник: [ParagraphRange](https://github.com/AdobeDocs/uxp-after-effects/blob/7d1cd01b4c69a9e02b77d48b3f919a6145a90841/src/pages/after-effects-api/paragraphrange.md).

На этой странице только read-only `characterStart/characterEnd/isRangeValid`,
`characterRange()` и `toString()`. Не добавлять воображаемый setter
`paragraphRange.justification` из назначения класса.

Операция: получить paragraph range из актуального TextDocument → проверить
валидность → один раз получить CharacterRange → изменить нужное оформление →
записать TextDocument → заново проверить абзац. Возвращённый CharacterRange
независим от последующих изменений родительского диапазона; он не следит за
перемещением выбранного абзаца. На невалидном диапазоне чтение границ или
`characterRange()` может бросить исключение; `toString()` остаётся диагностикой.
После вставки переноса заново определить смысловую цель, а не только проверить
старый числовой интервал. Текстовый индекс, номер абзаца и номер перенесённой
строки нельзя считать взаимозаменяемыми.

#### ComposedLineRange: строка требует свежего layout

Источник: [ComposedLineRange](https://github.com/AdobeDocs/uxp-after-effects/blob/7d1cd01b4c69a9e02b77d48b3f919a6145a90841/src/pages/after-effects-api/composedlinerange.md).

Опубликованы те же три read-only поля и два метода. `characterRange()` строит
независимый CharacterRange по текущим границам; invalid range вызывает ошибку.
`toString()` безопасен для диагностики invalid объекта, не сериализует layout.

Для оформления строки использовать свежий документ и composed-line mapping,
затем его CharacterRange; после commit получить новый документ и диапазоны.
`isRangeValid` означает допустимость границ, не подтверждение актуального переноса
после изменения шрифта, текста или box. Нулевая раскладка не даёт строку с
индексом 0. Иначе редактор может успешно применить стиль уже к другим символам.
Страница называет single line, а фабрика TextDocument допускает диапазон линий:
не ограничивать её одним номером и не объявлять прямой setter стилей на
ComposedLineRange. Host-layout, сохранение и render в этом review не выполнялись.

### Камеры, свет и 3D-слои — полный обзор pinned UXP source, 2026-10-08

Полностью прочитаны CameraLayer, LightLayer, ParametricMeshLayer и ThreeDModelLayer
на общем official pin; SHA256 совпали с inventory. Это 325 повторённых строк свойств
и заголовков методов, не 325 уникальных API. Все members помечены **27.0**.
Evidence: DOCUMENTED / SOURCE EXAMPLE / RUNTIME-NOT-CLAIMED.

#### Выбор операции и типа слоя

Создание и редактирование — разные команды. Для создания используйте документированный
метод `LayerCollection`; для изменения сначала установите ожидаемую специализацию
цели. Общая строка в таблице API, имя слоя или `threeDLayer` не заменяют такую проверку.
Эти четыре страницы не задают универсального классификатора произвольного выделения
или экспорта классов для `instanceof`: неподтверждённую цель лучше отклонить, чем
проверять её тип изменяющим setter. Не придумывайте конструкторы на `app`.

#### CameraLayer

[Страница CameraLayer](https://github.com/AdobeDocs/uxp-after-effects/blob/7d1cd01b4c69a9e02b77d48b3f919a6145a90841/src/pages/after-effects-api/cameralayer.md)
описывает обычную иерархию свойств. Для настройки камеры находите именованные
`position`/`zoom` через `property()` и проверяйте полученный объект перед изменением.
Одного обхода `1..numProperties` недостаточно: он охватывает индексируемые группы.
`active`/`activeAtTime` учитывают включение, solo и время; они не определяют
окончательный выбор камеры рендерером.

Скопированные строки `lightType`/`lightSource` не делают камеру источником света:
описание прямо запрещает setter `lightType` у non-light слоя. Аналогично,
`addVariableFontAxis` ограничен группой текстового animator. `duplicate()` возвращает
новую CameraLayer; это создание объекта, а не получение ещё одной ссылки на прежний.

#### LightLayer: назначение environment source

[LightLayer](https://github.com/AdobeDocs/uxp-after-effects/blob/7d1cd01b4c69a9e02b77d48b3f919a6145a90841/src/pages/after-effects-api/lightlayer.md)
связывает `lightSource` с режимом `LightType.ENVIRONMENT`. Источником служит
**2D video/still/precomp слой той же композиции**; 3D-слой отвергается.
Это ссылка на слой, а не путь к файлу. Числовые значения enum и место его экспорта
здесь не определены; не подставляйте предполагаемые числа.

Рекомендуемая команда: заново разрешить light и source → проверить владельца,
специализацию и 2D-роль → сохранить текущую пару type/source → установить
поддерживаемый environment type → назначить source → прочитать оба значения.
Ошибка второго шага записи может оставить уже изменённый type; сообщите частичный
результат. Не переводите пользовательский источник в 2D автоматически.
Старое описание `environmentLayer` относится к Ray-traced 3D и не устанавливает
эквивалентность этому light-source маршруту.

#### ParametricMeshLayer: изменение существующей формы

[ParametricMeshLayer](https://github.com/AdobeDocs/uxp-after-effects/blob/7d1cd01b4c69a9e02b77d48b3f919a6145a90841/src/pages/after-effects-api/parametricmeshlayer.md)
разрешает изменение `parametricMeshType` только у mesh-слоя; setter не превращает
произвольный слой в mesh. `parametricMeshOptions` и `parametricBevelOptions` имеют
тип **PropertyGroup, access R**, хотя описание говорит о редактировании параметров.
Это не документированный setter всего объекта. Bevel описан только для
**CUBE/CONE/CYLINDER**.

После согласованной смены типа заново получите подходящие группы, найдите
документированные дочерние свойства и запишите лишь выбранные параметры через их
контракт. Не переносите сюда объектный формат mesh-options из ExtendScript.
Точные поля, диапазоны, enum exports и сохранение прежних параметров при смене типа
этой страницей не заданы. Отсутствующий bevel не заменяйте выдуманной пустой группой.
`sourceRectAtTime` описан как прямоугольник слоя с text/shape оговорками;
это не контракт 3D bounding box или получения вершин/топологии.

#### ThreeDModelLayer: материалы и пределы общего API

[ThreeDModelLayer](https://github.com/AdobeDocs/uxp-after-effects/blob/7d1cd01b4c69a9e02b77d48b3f919a6145a90841/src/pages/after-effects-api/threedmodellayer.md)
публикует `material(indexOrName)` только при включённой beta feature
`AE.SubstanceMaterialScripting`; иначе сам member **undefined**. Индекс начинается
с 1, имя сравнивается точно с учётом регистра; отсутствующий материал вызывает
ошибку. Возвращаемый `MaterialPropertyGroup` не описан отдельной страницей данного
inventory. Поэтому можно объяснить квалифицированный поиск, но нельзя обещать
перечисление всех материалов, их поля или редактирование геометрии.

Сначала проверьте доступность метода у свежей цели; используйте явно выбранное
имя/известный допустимый индекс, не перебирайте до исключения. `source` read-only,
изменение отнесено к `replaceSource`; список допустимых модельных форматов и
гарантии сохранения материалов при замене здесь отсутствуют.

Особые расхождения: `calculateTransformFromPoints` называет третий угол
bottom-right, тогда как mesh-страница — bottom-left; общий wrapper требует
разрешения конфликта. `addToMotionGraphicsTemplate` объявляет boolean, но описывает
warning и **undefined** при отказе. Общие text/audio/matte строки не доказывают
поддержку каждого сценария конкретной моделью или render engine.

#### Владение, ошибки и версии

Общая схема команды Application/Project применяется с проверкой специализации
слоя. `remove()` удаляет слой из композиции; эти страницы не задают `dispose()`
или permission для произвольного worker.

Существующие общие разделы о Property, parenting, preset selection, guides, matte
и DeferredCall применяйте с их ограничениями; не выводите полную совместимость
из повторённой строки таблицы. Упоминание `.wait()` в layer `getRenderGUID`
сверяйте с разделом **Deferred render**; Promise/cancel API из него не следует.

**UXP 27.0, ExtendScript feature versions и native SDK — отдельные основания.**
Primary native baseline остаётся SDK25.6build61/CompSuite12;
CompSuite13/parametric mesh относится к отдельно помеченному public-guide26.5
исследованию. Ни создание слоя, ни readback не подтверждают конкретный renderer,
экспорт модели или изображение. В этом обзоре AE не запускался.

## Identity, selection и invalidation

[Project](https://developer.adobe.com/after-effects/uxp/after-effects-api/project)
documents activeItem null for absent/ambiguous selection, `itemByID`, `layerByID`
and `revision`; invalid layer IDs throw, absent valid IDs can return null. ID is
not permission or proof object still exists. CompItem item ID survives save/reload,
but importing the project assigns new IDs. Re-resolve target at command execution,
not when UI was painted. Collection index is 1-based, selectedLayers is 0-based.
Do not call `private_itemAtIndex`: reference explicitly marks it internal.

`Project.revision` increments on user actions; useful freshness signal, not a
cryptographic render identity or universal mutation lock. After project switch,
structural mutation, async wait or UI reload, refresh and validate target. Serialize
mutating commands; rejecting a stale response does not undo executed work.

## Не переносить ExtendScript contracts по похожему имени

| Published AE UXP fact | Migration consequence |
|---|---|
| Application.open/openFast/openTemplate take **string** paths | Do not pass ExtendScript File or UXP Entry object without documented conversion |
| Project.file is string, empty when unsaved | Do not access `.fsName`; handle unsaved project explicitly |
| Project.save accepts optional string; returns boolean | false/cancel is not saved-project success |
| Project.importFile takes options object | Read ImportOptions shape before porting `new ImportOptions(new File(...))` |
| Project.replaceFont is explicitly **not undoable** | Undo group cannot provide rollback; separate consent/backup policy |
| Application.themeColor always throws deprecated error | Use documented getAppTheme/getUseReducedContrast/getAllowedAppThemes |
| CompItem.usedIn is a copied array | Refresh after project mutation, not live membership cache |

Shared UXP file access/network/storage require their own permissions and host
integration. OS path accepted by one host method does not authorize arbitrary
filesystem access or imply Entry/nativePath conversion for another method.

## Guides: overloads и версии

[CompItem](https://developer.adobe.com/after-effects/uxp/after-effects-api/compitem)
documents legacy-style `setGuide(position, guideIndex)` and object-style
`setGuide(guideIndex, guideOptions)` — **opposite argument order**. Never generalize
one positional wrapper across both forms. getGuideAsObject yields orientation,
positionType, position, color, pinned; object partial-update form is described as
AE Beta26.5+, while UXP member table says Since27.0. Keep these layers separate:
host feature introduction versus UXP module/member availability. Do not lower
UXP MinVersion to26.5 because text mentions an older host feature.

## Deferred render: не выдумывать Promise/cancel API

CompItem documents `getRenderGUID(seconds, thread, trace)`, `saveFrameToPng(seconds,
path, max_abort_interval?)` and draft variant returning **DeferredCall**, described
as resolving when computation/write finishes. Собственная страница DeferredCall
перечисляет duration seconds, а Layer/AVLayer/TextLayer и3D pages у `getRenderGUID`
прямо описывают `.wait()` для получения GUID. Это упоминание результата не раскрывает
блокирующее поведение, допустимый context, timeout, cancellation или полный error
contract. Оно также не документирует `.then`, Promise identity или безопасный await.
Не переносить частичное описание GUID ожидания на frame export автоматически.
Resolve exact async integration before implementing an export command. Requested
path/returned handle are not output evidence: require decoded files, full requested
frame coverage, identity and explicit status. Avoid arbitrary polling or workers
calling host methods without a documented permission.

## Shared platform и AE setup

[Отдельная platform-глава](04-UXP-PLATFORM.md) описывает официальные shared UXP
lifecycle/UI, manifest/UDT, file/storage/network и distribution contracts.
AE Get Started остаётся заглушкой; host ID, соответствие AE build ↔ UXP runtime
и устанавливаемый AE starter не выводятся из MinVersion27.0. Entry/nativePath,
Promise и AbortController подчиняются своим контрактам и не расширяют автоматически
возможности AE host module или DeferredCall.

Use [evidence records](../10-TESTING/07-TEST-EVIDENCE.md): exact host version/build/beta,
plugin/package source identity, entry/manifest/runtime, project preconditions,
requested operation, readback, error and cleanup outcomes. Test no-project/missing
API, begin failure, mutation/readback failure and cleanup-only failure separately.
No docs build or fake-host test is rendered/runtime success.

Reviewed sources: [API index](https://developer.adobe.com/after-effects/uxp/after-effects-api/),
[Application](https://developer.adobe.com/after-effects/uxp/after-effects-api/application),
[Project](https://developer.adobe.com/after-effects/uxp/after-effects-api/project),
[ItemCollection](https://developer.adobe.com/after-effects/uxp/after-effects-api/itemcollection),
[CompItem](https://developer.adobe.com/after-effects/uxp/after-effects-api/compitem),
[DeferredCall](https://developer.adobe.com/after-effects/uxp/after-effects-api/deferredcall).
Полное чтение44 pinned host pages завершено. Оставшиеся constructor/enum/type/
async gaps, AE setup, shared-platform и distribution coverage учитываются отдельно
в [currentness review](../CURRENTNESS-REVIEW-2026-10-07.md); они не закрыты количеством
прочитанных страниц.
