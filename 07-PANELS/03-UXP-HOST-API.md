# AE UXP: host module, project operations и migration contracts

Reviewed **2026-10-07** against Adobe AE-specific reference. Evidence: DOCUMENTED /
SOURCE EXAMPLE, runtime NOT_RUN. Read [transition](02-UXP-TRANSITION.md) for rollout;
this page covers published API rather than treating UXP as only a future roadmap.

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

Это inventory опубликованных object links, не построчная валидация всех members.
Каждый member требует своей MinVersion/access/return/error проверки. Не обещать
полную parity с ExtendScript из одинаковых object names.

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
Four full pages reviewed initially: ImportOptions/FileSource/FootageItem/OutputModule,
79 rows/headings. MinVersion27.0 is published contract, not installed availability.

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
read; ledger now8/44 pages,124/1448 rows/headings,36 pages remain. All reviewed
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
official pin; ledger14/44 pages,164/1448 repeated rows/headings,30 pages remain.
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

Full Font/Fonts/Shape/KeyframeEase/MarkerValue pages read; ledger19/44 pages,
229/1448 repeated rows/headings,25 remain. No classes/constructors/export locations
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
as resolving when computation/write finishes. Reviewed DeferredCall page only
exposes duration seconds; it does not specify `.then`, Promise identity, cancellation
or complete error semantics. No invented await wrapper/cancel method here.
Resolve exact async integration before implementing an export command. Requested
path/returned handle are not output evidence: require decoded files, full requested
frame coverage, identity and explicit status. Avoid arbitrary polling or workers
calling host methods without a documented permission.

## Shared platform setup, permissions and packaging — 2026-10-07

Reviewed Adobe [first plugin](https://developer.adobe.com/uxp/guides/tutorials/build-your-first-plugin/),
[manifest](https://developer.adobe.com/uxp/guides/explanation/concepts/manifest/),
[package](https://developer.adobe.com/uxp/guides/how-to/distribution/package/) and
[install](https://developer.adobe.com/uxp/guides/how-to/distribution/install/).
The common tutorial and manifest HostDefinition list PS/ID/Premiere/AME, **not AE**.
Consequently this is a shared-platform workflow with an AE-specific setup gap,
not a validated AE starter. Do not invent app:"AE" or copy another host's ID.

1. Obtain AE-specific supported host/build/UDT template and host ID from its actual
   setup documentation/distribution. Confirm connected host in UDT, not merely a
   page saying API27.0. Until then no installable AE manifest is claimed here.
2. Keep manifest.json at bundle root; current common schema example uses
   manifestVersion5 (number), stable id/name/semver, host minVersion and command/panel
   entrypoint IDs. Bind code to those exact IDs. Reference table calls schema version
   string while example uses number: follow host's validated schema, record conflicts.
3. Enable development mode in UDT and supporting host, Load & Watch, debug in host.
   HTML/JS reload loses in-memory state; stop listeners/timers and invalidate pending
   UI generations. Manifest changes require Unload then Load, not hot reload.
4. Default deny optional capabilities. For user-selected files prefer
   localFileSystem:"request", plugin-only storage needs no fullAccess. Network allowlist
   exact needed domains; avoid domains:"all". Clipboard/webview/process/addon permissions
   are separate, not granted by network or a host path parameter.
5. Handle picker cancellation, stale persistent tokens, revoked/missing paths and
   failed writes. Plugin folder is not project persistence or a credential store.
   Remote content is data; validate bridge origin/message schema, never evaluate code
   from response strings. Leave allowCodeGenerationFromStrings false unless justified.
6. UI uses shared UXP HTML/CSS/Spectrum, not full Chrome/CEP behavior. Bundle needed
   components; resize/theme/keyboard/focus and repeated show/hide need dedicated checks.
   Disable mutation controls while a host command is active; stale UI suppression
   does not cancel already executed host work.
7. Package with UDT Actions → Package into .ccx, inspect logs. Single host object for
   distribution; multi-host arrays are development convenience and packaging selects
   first host. Packaging success does not establish installed AE compatibility.
8. Stable Marketplace ID comes from distribution portal; independent/enterprise use
   separate stable ID to avoid Marketplace entitlement failure. CCX needs no CEP
   package signature/timestamp; this does **not** waive native addon signing/notary.
9. Test user install via CC Desktop (.ccx double-click), consent, installed listing,
   host discovery, update, disable and uninstall with actual artifact hash recorded.
   Do not require end users to enable developer mode. No AE Marketplace eligibility
   inferred from common packaging docs.

Hybrid .uxpaddon is not an AE Effect/AEGP binary renamed. Common package guide
specifies mac/arm64, mac/x64, win/x64 layouts and native signing/notary; support in
the chosen AE UXP build still needs host-specific confirmation. Developer loading,
CCX packaging and installed-product evidence remain separate lanes (NOT_RUN here).

The remaining AE host ID/setup and file/network/lifecycle member details are open
source contracts, not hidden under a claim that common UXP documentation guarantees
every host API or installation channel.

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
Full remaining object/member, manifest, shared-platform and distribution coverage
is tracked in [currentness review](../CURRENTNESS-REVIEW-2026-10-07.md), not silently complete.
