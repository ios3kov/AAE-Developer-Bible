# Полнота и актуальность — новая приёмка после edition1.1

Дата: **2026-10-07**. Parent: `227a0ac81f3313bd589c8a2e5a7dea80851249ba`.

По новому требованию владельца frozen edition1.1 не считается доказательством
исчерпывающей полноты и актуальности. Её исторический результат сохраняется;
ни tracker C/L, ни strict build не закрывают новую сверку текущего API surface.

## Источники и наблюдения первой итерации

| Источник | Что фактически прочитано | Вывод / предел |
|---|---|---|
| [Adobe AE portal](https://developer.adobe.com/after-effects/) | SDK download link | Console route — официальный путь, не полученная SDK поставка |
| [SDK Console](https://developer.adobe.com/console/servicesandapis/ae) | webfetch и browser | Loading/progressbar; SDK version/build/archive bytes не получены |
| [AE release notes](https://helpx.adobe.com/after-effects/desktop/what-s-new/release-notes-after-effects.html) | fetch HTTP403; search result сообщает September2026/version26.5 | Search snippet — discovery, не прочитанный vendor release contract |
| [C++ What's New](https://ae-plugins.docsforadobe.dev/intro/whats-new/) | 26.5 additions и host-only warning | Guide-level changes; не exact proprietary header review |
| [Preview media source](https://raw.githubusercontent.com/docsforadobe/after-effects-plugin-guide/master/docs/effect-details/effect-preview-media.md) | paths/formats/host note | Premiere Pro Beta27.0-only; не AE discovery feature |
| [AE UXP landing](https://developer.adobe.com/after-effects/uxp/) | beta wording и host API link | Documentation publication, не установленный beta/GA |
| [AE UXP API index](https://developer.adobe.com/after-effects/uxp/after-effects-api/) | host module/access и object index | Уже возможен отдельный AE-specific API guide, а не только roadmap |
| [Application](https://developer.adobe.com/after-effects/uxp/after-effects-api/application) | properties/methods, MinVersion27.0 | Undo returns boolean, identity, path strings; themeColor throws |
| [Project](https://developer.adobe.com/after-effects/uxp/after-effects-api/project) | full page | selection/IDs/import/path strings, non-undoable replaceFont |
| [ItemCollection](https://developer.adobe.com/after-effects/uxp/after-effects-api/itemcollection) | full page | addComp/addFolder, ID lookup, private helper not for callers |
| [CompItem](https://developer.adobe.com/after-effects/uxp/after-effects-api/compitem) | full page | creation/readback, guide overload reversal, DeferredCall frame APIs |
| [DeferredCall](https://developer.adobe.com/after-effects/uxp/after-effects-api/deferredcall) | full page | Only duration documented; no independently described await/cancel contract |

Public-page review dates apply to these observations only. No beta/GA availability,
full UXP/runtime/SDK26.5 audit or new installed AE observation inferred.

## Новый version map

| Layer | Retained exact baseline | Current published surface / gap |
|---|---|---|
| Native headers/samples | supplied SDK25.6build61 | 26.5 guide additions; actual archive/header/toolset diff OPEN |
| Native guides | dated reviewed source | All89 pinned public-guide pages read and reconciled; mixed suite generations and source gaps retained, not an exact SDK26.5 header inventory |
| Effect metadata | reviewed PiPL baseline | Search_Keywords/Description/EXT3 and preview media are PProBeta27-only per current guide |
| ExtendScript / expressions | retained lessons and dated evidence | Pinned DOM648 headings classified,32 expression pages and8 match-name pages reviewed;8 File/Folder/runtime pages added, broader runtime and source-contract gaps explicit |
| AE UXP | official source pin7d1cd01 | 44/44 full host pages;47 selected Hub pages plus5 AE setup/site files reviewed. Constructor/enum/type/async and AE setup/runtime-map gaps retained |
| Host/OS support | historical matrix retained | Four official pages read2026-10-08; dated release26.5/requirements and known issues transferred, previous HTTP403 access gap closed |

Native guide lists `AEGP_CreateParametricMeshLayerInComp` in CompSuite13 and
`AEGP_ObjectType_3D_PARAMETRIC_MESH` from GetLayerObjectType; StreamSuite7 exposes
layer-parameter render-stage sampling. Exact signatures/macros/layouts require
the current SDK, not guessed declarations copied from overview prose.

## Обязательная очередь новой актуальной редакции

**Native public-guide closure — 2026-10-08:** [обзор](NATIVE-PUBLIC-GUIDE-REVIEW-2026-10-08.md)
фиксирует89/89 полностью прочитанных Markdown страниц,2 953 983 bytes/12 918 строк,
exact tree/blob/SHA256 inventory и соответствие профильным главам. В частности,
AEGP suites page прочитана полностью;88 headings/596 повторяемых именованных строк
включают структуры, legacy и source typos, а не596 современных SDK функций.
Public guide дополняет SDK25.6build61 и сохраняет текущий26.5 archive/header gap.

**Platform/runtime дополнение — 2026-10-08:** новая
[UXP platform глава](07-PANELS/04-UXP-PLATFORM.md) закрывает выбранные lifecycle/UI,
file/network/storage и packaging workflows по47 полным Hub страницам и5 AE setup/
site файлам. Общие страницы дедуплицированы в [52-file ledger](uxp-platform-reviewed-2026-10-08.json).
AE setup остаётся опубликованной заглушкой; shared manifest/version table не дают
AE host ID, minimum UDT или UXP↔AE mapping. Эти данные не придуманы.

Все8 pinned match-name страниц/757 повторяемых строк прочитаны и сопоставлены
с property-tree операциями. Отдельно прочитаны8 runtime/File/Folder страниц,
2790 строк, с исходными hashes. Добавлены собственные bounded binary reader,
new-file UTF-8 export и UXP JSON export;16 source-extracted portable cases проверяют
отмену, пределы, частичный outcome и cleanup, без настоящего I/O или AE.
ScriptUI/BridgeTalk/Socket/ExternalObject/E4X и остальные runtime references не
объявляются полностью пересмотренными из-за чтения этих8 страниц.

[Host/platform review](HOST-PLATFORM-REVIEW-2026-10-08.md) закрывает доступ к текущим
официальным release notes и requirements, добавляет Advanced3D/known-issues scope.
Сохранённые даты различаются; более старый renderer minimum не понижает текущий
host minimum. Exact SDK25.6build61 baseline и отсутствие нового26.5 archive
не изменились. Текущий core inventory129 не заменяет source API inventory.

**Актуальный UXP результат — 2026-10-08:** полное чтение44/44 pinned страниц
завершено; 1448/1448 повторяемых property rows/method headings охвачены page review.
Последние19 страниц: Application/Project/CompItem, Layer/LayerCollection/AVLayer/
ShapeLayer/TextLayer, Property/PropertyGroup/MaskPropertyGroup, TextDocument и3 ranges,
CameraLayer/LightLayer/ParametricMeshLayer/ThreeDModelLayer. Все SHA256 сверены.
Практические операции и расхождения внесены в host chapter; regression требует
точного совпадения inventory/ledger, включая index без member headings.

Это не1448 уникальных API, полный overload/constructor/enum reference, все типы
или shared-platform coverage. MaterialPropertyGroup не имеет страницы в данном
index. Layer `.wait()` mention уточняет прежнюю only-duration формулировку:
собственная DeferredCall table неполна, точные wait/error/cancel semantics остаются
неизвестными. Native SDK и AE UXP runtime в этом блоке не выполнялись.

Следующие датированные записи сохраняют промежуточный coverage своих итераций;
числа «remain» в них не являются текущим итогом.

2026-10-08 official UXP folders/generated sources/index block:6 full pages;
ledger25/44 pages,281/1448 repeated rows/headings,19 remain. Owner-specific creation/
throwing ID lookup/recursive-delete consent, solid/placeholder interpretation gates
and DeferredCall only-duration integration gap reconciled. No host/runtime PASS.

2026-10-08 official UXP font/animation-value block:5 full pages; ledger19/44,
229/1448 repeated rows/headings,25 remain. Font picker/revision/fallback/variable axes,
typed ease/path/feather and marker-object parameters documented. Global defaults,
constructor/write-back/shaping/topology gaps retained; no typography/runtime PASS.

2026-10-08 official UXP prefs/settings/views block:6 full pages, ledger14/44 pages,
164/1448 repeated rows/headings,30 remain. Namespaced typed settings/preference
ownership and explicit live preview/guide operations; activeViewIndex base/enum/
constructor/global persistence/renderer gaps retained, no runtime or image PASS.

2026-10-08 official UXP queue block:4 full pages reviewed; ledger8/44 pages,
124/1448 repeated rows/headings,36 pages remain. Prepare-only owned queue command,
render versus renderAsync return contracts, global queue consent, status/lastError/
AME and callback lifecycle gaps documented. No render/AME/output/runtime PASS.

2026-10-08 official AE UXP source pinned at7d1cd01b4c69a9e02b77d48b3f919a6145a90841
(AdobeDocs/uxp-after-effects, linked from published HTML). Inventory44 pages (43
objects + index)/1448 repeated property rows and method headings, not unique symbols.
Initial4 full pinned reviews/79 rows: import/media interpretation/relink/proxy/output
workflows. Official UXP range APIs distinguished from ExtendScript research exclusions;
constructor/enum exports, RW/prose and string/File discrepancies retained.40 pages
unreviewed at this pin; no automatic promotion of earlier live reviews or host PASS.

2026-10-08 scripting zero-heading closure:7/7 such inventory pages read/hash checked
and independently reconciled, including8 unqualified globals, Collection table,
Camera26.3 Advanced3D options and typed inheritance.648 DOM heading denominator
unchanged. Text matte/camera inheritance/source-owner discrepancies retained; exact
match names/ranges and runtime/File/Folder still separate. No host runtime PASS.

2026-10-08 pinned expression page-review closure:32/32 pages,295/295 third-level
headings reconciled by explicit full-page reviews; includes3 zero-heading pages,
non-callable Text.Font menu and Chaining overview. Added uniform/range text styles,
paragraph ordering and owned variable-axis remap; retained None/chaining, manual
kerning and Tsume source gaps. Exhaustive page-set regression added. This is pinned
source/design classification, not all signatures/engine language/current official
contracts or AE runtime PASS. Expanded whole-Bible acceptance remains OPEN; native/
UXP current inventories, runtime/File/Folder and final provenance queues remain.

2026-10-08 expression global/layer/camera/light block:9 full pages including2
zero-heading navigation pages read/hash checked; ledger28/32 (213/295 headings),
4 text pages remain. Context/cadence, transforms/audio/source-time/bounds/sampling,
materials and camera/light policies supplied; source hasVideo/singular option routes,
optical-depth and sample-stage limitations retained. No pixel/lighting/runtime PASS.

2026-10-08 expression context/data/marker block:10 full pages read/hash checked,
ledger19/32 pages (136/295 headings),13 remain. Comp/footage metadata and lookup,
no-eval JSON/MGJSON, effects/menu/hierarchy, masks, keys and inert marker metadata
operations supplied. [1][0] scalar/path example error, dated mask limitation and
comp-marker numeric-name/index distinction retained. No host/data decode/render PASS.

2026-10-08 expression math/color block:4 full pages read/hash checked; ledger9/32
pages (75/295 headings),23 pages remain. Bounded remap, vector shape/zero-length,
world orientation and normalized color/hex policies supplied. Malformed rgbToHsl
and mismatched clamp example preserved as source discrepancies; no runtime PASS.

2026-10-08 expression property/path block: independent inventory32 pages/295 headings
(overloads retained),5 explicitly full-page reviews/52 headings,27 pages unreviewed.
Added marker trigger/count/pre-first gates, versioned next/previousKey, qualified
loops/sampling/smoothing and path rebuild/arc follow. Source loop default/temporal
wiggle units ambiguities retained. No expression/key/path runtime or complete coverage.

2026-10-08 expression continuation: pinned reference revision
`a5c5c5066d0395239d524510ace060963f5c0d33`; full transforms/time/random pages read.
Practical3D parent-space follow, point/vector/surface distinctions, time offset/
rounding and random lifetime policies added to expressions chapter. Source example
toWorldVec/toWorld discrepancy retained. This is3-page scoped review, not complete
expression member inventory or runtime PASS.

- [ ] Obtain lawful current SDK archive/version/build; record hash and full
  headers/utilities/sample/tool/resource diff against25.6. Do not distribute SDK.
- [x] Read and reconcile all89 pinned native public-guide pages, including26.5
  additions and cross-host-only topics. Map source → version boundary → practical
  chapter; preserve malformed/legacy rows. Exact SDK symbol closure remains part
  of the separate archive/header task above.
- [x] Read all44 pinned published AE UXP host pages and reconcile practical operations;
  retain contradictory/incomplete contracts without inventing API parity.
- [x] Review selected shared-platform setup/manifest/permissions/UI/file/network/
  storage/lifecycle/packaging workflows; explicitly preserve unpublished AE-specific
  setup/runtime mapping. This is scoped operation coverage, not all UXP Hub APIs.
- [ ] Review current scripting/expression object/member changes and missing operation
  recipes; distinguish ExtendScript, expression JS and UXP rather than porting by name.
- [x] Read current host/platform requirements/release notes from a verifiable official
  route; close the previous access gap and retain separate dates/runtime limits.
- [ ] Audit source/recipe completeness against current API inventory, not just the
  historical127 core menu entries. Overview L does not excuse a missing promised operation.
- [ ] Final source/date/link/provenance sweep, tests/generated outputs and new freeze.

First result: [AE UXP host operations](07-PANELS/03-UXP-HOST-API.md) now documents
actual published entry/version/identity/Undo/creation/readback boundaries. It closes
the roadmap-only gap for this bounded operation, **not this whole queue**.

## Native26.5 public-contract reconciliation

### Reproducible scripting inventory

#### Text range full-page reconciliation — 2026-10-08
Final ImportOptions full-page read/hash match confirms remaining3 members are research.
Pinned DOM partition complete:642 documented +6 explicit research exclusions =648.
No unclassified headings remain; test checks disjoint/exhaustive source membership.
This scoped closure does not close expressions/matchnames, zero-heading pages,
runtime/File/Folder, signature/overload gaps, native/UXP or full/current acceptance.

Full TextDocument page subsequently read/hash matched:63 remaining headings mapped
to scoped styling, irreversible composer migration, box fitting and fresh composition
diagnostics. Leading setter/autoLeading prose, scale units and empty-line mapping
ambiguities retained. Ledger642/648;6 headings remain (3 research-only,3 ImportOptions).
This is DOM-heading reconciliation, not expression/native/UXP or full acceptance PASS.

Full Property page subsequently reconciled:59 remaining headings, ledger579/648,
69 without documented reconciliation. Typed inspection/key snapshots/restoration,
dropdown semantic migration, EGP/alternate media and26.5 layer-input stages supplied.
Temporal auto-Bezier setter/getter conflict preserved; prospective-source cycle limit
not invented. No key/dropdown/media/stage runtime or exact26.5 header evidence.


Full CharacterRange/ParagraphRange/ComposedLineRange pages read/hash matched.
Remaining18 headings mapped to mixed-style edit, insertion/replacement, detached
validity, paragraph/line conversion and fresh composition workflows. Undefined
mixed values, color/kerning side effects and independent derived accessors documented.
Ledger520/648;128 without documented reconciliation, not128 proven absent operations.
No text/layout/runtime performed; full TextDocument/Property remains next.

#### Font ecosystem full-page reconciliation — 2026-10-08

Full FontObject/FontsObject pages read/hash checked. Remaining26 headings reconciled
into font-picker disambiguation, soft proxy lifetime, variable-instance discovery,
default-font/UI policy and asynchronous folder-update workflows. Lookup can create
variable instance; default mapping doesn't guarantee even one glyph; null resets
launch default, not prior mapping. Ledger502/648;146 headings without documented
reconciliation. No font install/cloud sync/default mutation/runtime performed.

#### Light/mesh/value objects and heading correction — 2026-10-08

Full LightLayer/ParametricMeshLayer/GuideOptions/KeyframeEase pages read, hashes match
inventory. Extractor missed lightSource heading with trailing colon; fixed/tested,
denominator now648 headings/49 pages.12 members transferred into actual operation
guidance; ledger476/648,172 without documented reconciliation. MeshType versus
ParametricMeshType and absent mesh-options constructor/bounds contracts retained;
lightSource24.3 HDR/EXR versus25.2 any2D source separated. No geometry/light runtime.

#### PropertyBase/PropertyGroup full-page reconciliation — 2026-10-08

Full pages read, hashes match pinned inventory. Remaining18 headings transferred to
bounded tree inspector and indexed-stack mutation/readback. Indexed numProperties
doesn't enumerate named layer roots; propertyType listed writable isn't described
as a type-conversion operation. Source naming discrepancy retained. Ledger464/647,
183 without documented reconciliation. No property-stack mutation runtime executed.

#### AVLayer reconciliation — 2026-10-08

Full pinned AVLayer page read, SHA256 matches inventory.40 headings transferred to
matte/source/retime/render policies, coordinate/bounds and Media Replacement registration.
NO_TRACK_MATTE null/example conflict, transform bottom-right/example bl and legacy
Ray-traced description preserved; no guessed enum/coordinate/effect-bounds contract.
Ledger446/647,201 headings without documented reconciliation. No render/coordinate/
matte/MOGRT/retime host result inferred.

#### Layer/LayerCollection reconciliation — 2026-10-08

Full pinned pages read, SHA256 matches inventory.49 documented members transferred
to typed creation, source ownership, timing/parenting/reordering, copy/duplicate,
precompose/preset/detection and layer-view guide recipes. Dated copy/Undo crash warning
retained without inventing a current-host result. Ledger406/647;241 headings remain
without explicit documented reconciliation. No layer creation/copy/precompose/runtime
performed; coordinate conversion/AVLayer contracts remain separate next review.

#### Application/Project reconciliation — 2026-10-08

Full pinned Application/Project pages read; downloaded SHA256 checked against
inventory.96 additional documented headings transferred to lifecycle/save/settings,
bounded scheduled jobs, external-script outcomes, destructive maintenance, explicit
Team Projects collaboration and Watch Folder operation guidance. Research openFast/
dirty excluded. Source type/enum/example conflicts and missing prior-policy getters
retained explicitly; historical memory-limit prose not promoted to modern RAM model.
Ledger357/647,290 headings without documented-member reconciliation (includes research
exceptions). No AE/save/cloud/watch/render runtime or release matrix observed.

#### Item/CompItem reconciliation

Full Item/CompItem pages read at pinned revision; downloaded bytes match inventory
SHA256. Added49 documented headings covering project-scoped identity, organization/
deletion, guides, composition preset/readback/selection and explicit MOGRT save/export.
CompItem.counters reviewed as research-only and excluded. Controller index base is
absent from pinned page; bulk rename implementation remains a concrete contract gap,
not invented1-based behavior. Ledger261/647;386 headings lack explicit documented
reconciliation (includes research exceptions), not386 proven missing Bible members.
No comp/EGP/export/consumer runtime executed; expanded acceptance remains IN PROGRESS.

#### Persistence/viewer/system reconciliation

Full Preferences/Settings/View/Viewer/ViewOptions/System pages actually read.
Transferred38 headings into namespaced persistence, typed store/restoration,
view-scoped UI diagnostic preset and trusted external-helper protocol designs.
Preserved historical Settings size observation and fastPreview limitations;
no current OS support or process exit-code API invented. Ledger212/647,
435 headings without explicit reconciliation (includes research exceptions).

#### Proxy/mask/shape/marker reconciliation

Full AVItem/Shape/MaskPropertyGroup/MarkerValue source pages read at pinned revision.
Transferred49 headings into concrete operation/readback guidance: proxy interpretation
vs source replacement, AVItem undefined constructor, source-specific writable fields,
geometry/tangent/feather/UI boundaries and marker metadata commit/preservation.
Ledger grows to174 members,473 headings not explicitly ledger-reconciled. These
counts remain source-review coverage, not host/image/runtime tests.

#### Import/relink/source reconciliation and inventory correction

Found extractor scope omission: docs/sources wasn't included. Added source folder,
retaining pinned revision; report now49 pages/647 headings, not45/629. Four source
pages read in full along with ImportOptions/FootageItem/FolderItem/ItemCollection.
Added import/relink/interpretation/bin recipes and source dependency ordering;
undocumented rangeStart/rangeEnd/isFileNameNumbered explicitly research-only.
No research member promoted to public contract. Semantic ledger records documented
members only for this block; source enumeration does not establish host runtime.

Ledger totals after this block:125 named members;522 inventory headings without
explicit documented-member reconciliation. Three research helpers reviewed as
unsupported public-contract dependencies stay outside that documented ledger.

#### Render queue DOM reconciliation — 2026-10-07

All5 pinned renderqueue pages read in full (48 headings): prepare/disarm/arm/run,
local template/settings capability, module invalidation, multiple outputs, foreign
queue protection, callbacks/range/skip diagnostics and AME handoff transferred to
object-model chapter. Documented source inconsistencies retained (item index0 vs1;
callback string vs example function); no invented resolution through unrun host code.
Semantic ledger grows to90 members;539 extracted headings remain without explicit
ledger reconciliation. No AE/AME render or decoded-output claim.

#### Properties/keyframes operation review — 2026-10-07

Selected Property/PropertyGroup/PropertyBase sections read at pinned revision:
static/key/time/batch setters, nearest-key vs exact-time identity, removal ordering,
interpolation/ease/tangent shape, expression evaluation and separated followers,
indexed-group invalidation and matchName/index limits. Transferred to scripting
chapter as bounded authoring recipe. No full74-member Property audit inferred.
Semantic review ledger added separately from the machine mention inventory.

Initial `scripting-api-reviewed-2026-10-07.json` recorded42 explicitly reviewed members in
8 source pages with covered operation and Bible chapter. It is not inferred from
matching text, does not change source extractor's UNASSESSED entries and does not
assert whole-object/runtime coverage. At that block587 extracted headings lacked
this explicit reconciliation record (not necessarily absent from historical Bible).

#### Fonts/text operational reconciliation — 2026-10-07

Reviewed selected Project/FontsObject/FontObject/TextDocument/CharacterRange sections
at pinned revision. Transferred identity/revision/substitute/glyph policies,
non-undoable project replacement, layer-time usage exception and range/composition
invalidation to scripting chapter. Review scope is the named members in these
sections; not all45 pages/629 members. Machine report retains UNASSESSED because
literal extraction isn't a semantic review ledger. This block closes previously
missing operational guidance for those workflows; full text/member inventory stays OPEN.

`scripts/audit_scripting_inventory.py` obtained all45 DOM pages at pinned scripting
revision and extracted629 unique member headings within their pages. Report:
`scripting-api-inventory-2026-10-07.json` (per-page SHA256, member names, literal
mentions in scripting/templates and explicit UNASSESSED status). No upstream prose
copied. Source tree truncation fails closed. This is a machine inventory, not629
human-reviewed contracts; mentions are not practical coverage, overload signatures
and expressions/matchnames are outside this extractor's scope. Reproduce:

```sh
.venv/bin/python scripts/audit_scripting_inventory.py \
  --output scripting-api-inventory-2026-10-07.json
```

This supplies a concrete review denominator instead of assuming128 chapters cover
the current API. Per-member/topic reconciliation remains OPEN and visible.

### BlitHook limitation disposition — synchronous operation supplied

Full local25.6 AE_Hook.h/EMP.cpp reread: no async lifetime/thread/cancel ordering
contract found. Async remains blocked on vendor details rather than invented timing.
Added concrete synchronous-copy callback/worker separation plus original portable
row-copy helper/tests. Valid source extent is caller precondition; no SDK source
redistributed or ABI shim invented. Native guide inventory and remaining API coverage
are still independent OPEN tasks. This closes the lack of a concrete safe copy
operation, not the undocumented async path.

### Third block: scripting delta and shared UXP workflow

Scripting source pinned `7137a990db4bd8dc9f5869b8ca431c7dfed52bdc`: changelog,
GuideOptions, ParametricMeshLayer, selected Item/Property/PropertyGroup/LayerCollection
sections actually read. Scoped26.0/26.3/26.5 change mapping and operational designs
added to scripting chapter. Whole scripting/expression inventory remains OPEN.

Adobe UXP first-plugin/manifest/package/install pages read2026-10-07. Shared lifecycle,
least privilege, distribution ID/CCX and install workflow added to host API chapter.
Manifest HostDefinition lists PS/ID/Premiere/AME only; no AE host ID validated.
Shared workflow is covered; AE-specific setup/availability and detailed platform
API review remain OPEN, not erased by copying a Photoshop manifest.
Repeated official release/system-requirement routes still HTTP403. No new matrix
verification or installed product observation. Full queue above remains active.

User-supplied local SDK checked at
`/Users/os3kov/Downloads/AfterEffectsSDK_25.6_61_mac/ae25.6_61.64bit.AfterEffectsSDK/Examples`.
It is25.6build61, not26.5. Fresh SHA256 of `Headers/AE_GeneralPlug.h`:
`30d12ec3eb5af1a902c7414053b1be1da0204b226e0b1cdc71272be1e137000c`;
`Util/AEGP_SuiteHandler.h`:
`2eeec0827ca13f039eb87c961c8c41e77f046379457930d4bb2700c756b40b13`.
Headers/Util symbol search found ItemViewSuite1 (playback only), not GuideSuite,
ItemViewSuite2/CompSuite13/StreamSuite7/CreateParametricMesh/EXT3 declarations.
Negative declaration search is scoped to this tree, not proof about installed hosts.

Public C++ source snapshot pinned to `6d9b285d9755d1fbf8ead7680ba49de24f94b547`;
reviewed `docs/aegps/aegp-suites.md` SHA256
`c27d64011443b983b379d1c6c2279d29fc35fb0a50bd6eed5436cf0f872be0c7`.
Selected exact sections actually read: Guides, ItemView2, Comp13 mesh, Stream7 stage.
Other suite rows are not declared fully reviewed in this iteration.

### Mesh command, not renderer implementation

Published Comp13 `AEGP_CreateParametricMeshLayerInComp(parent_compH, mesh_type,
new_layerPH)` adds a project-owned layer; listed shapes are cube/sphere/plane/torus/
cone/cylinder. Do not dispose returned LayerH as allocated memory. Recommended
command: late comp resolution → required Comp13 acquisition → validated mesh choice
→ successful Undo begin → create → object-type readback via LayerSuite9 → end Undo
→ release suites. No26.5 declaration compiled; acquisition macros/types must come
from actual26.5 headers. A created layer can remain after readback/Undo-end failure;
return created identity plus both errors, not pretend rollback. Mesh creation does
not implement Artisan, guarantee a renderer or prove scene/output compatibility.
If Comp13 unavailable, disabling mesh command is preferable to creating a solid
and calling it equivalent. Generic LayerSuite9 callers must handle a new enum
value without silently treating it as AV/text/model.

### Layer-parameter stage: two independent values

Stream7 published stage symbols: SOURCE(0), ONLY_MASKS(-2), ALL_EFFECTS(-1),
positive1..N means through effect indexN. LayerID alone no longer describes sampling
intent. Reviewed calls: Get/SetStreamLayerParamStageValue, Get/SetStreamLayerParamAndStageValue,
GetStreamInputStageCycleSafeLimit. Combined getter returns StreamValue2 requiring
DisposeStreamValue; scalar stage requires no disposal. Calls require PF_Param_LAYER,
otherwise Err_PARAMETER per guide. Re-query cycle-safe limit before applying after
source/effect add/remove/reorder; don't cache effect-index stage as durable identity.

Concrete design: request sourceLayerID plus stage ALL_EFFECTS → acquire Stream7
→ resolve layer-param stream/type → query current pair and cycle-safe limit
→ validate exact documented allowed-stage contract → choose combined setter when
both change → read back pair → dispose temporary value/stream → release suite.
Guide says combined setter is atomic single Undo step; this applies to that call,
**not a batch transaction or compensating subsequent errors**. Unsupported stage
must not silently downgrade to SOURCE or reuse25.6 SetStreamValue as equivalent.
Self/dependency cycle policy uses documented query, not numeric guess. No runtime,
compiled adapter or portable stub of invented26.5 tables added.

### Concrete chapter transfer

Guide preset/units/readback/per-view partial outcome now in
[guides chapter](17-NATIVE-SUITE-COOKBOOK/13-GUIDES-VIEWS-SELECTION.md).
PiPL/preview PProBeta-only scope in [PiPL chapter](01-ARCHITECTURE/03-PIPL-AND-LOADING.md).
Migration map linked from compatibility. Exact archive/header diff remains OPEN;
this block improves current public-contract coverage without pretending a baseline upgrade.
