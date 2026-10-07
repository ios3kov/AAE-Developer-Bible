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

## Reader verification и sources

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
