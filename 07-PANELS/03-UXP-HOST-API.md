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
