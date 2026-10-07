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
| Native guides | dated reviewed source | Guide2, ItemView2, Comp13, Stream7 changes need full topic/source reconciliation |
| Effect metadata | reviewed PiPL baseline | Search_Keywords/Description/EXT3 and preview media are PProBeta27-only per current guide |
| ExtendScript | reviewed ES3 lessons/DOM | Full current scripting object/member inventory OPEN |
| AE UXP | migration chapter | First practical host-API guide added; full published object/member/platform/packaging coverage OPEN |
| Host/OS support | retained dated matrix | Fresh readable release/requirements source OPEN; HTTP403 is not verification |

Native guide lists `AEGP_CreateParametricMeshLayerInComp` in CompSuite13 and
`AEGP_ObjectType_3D_PARAMETRIC_MESH` from GetLayerObjectType; StreamSuite7 exposes
layer-parameter render-stage sampling. Exact signatures/macros/layouts require
the current SDK, not guessed declarations copied from overview prose.

## Обязательная очередь новой актуальной редакции

- [ ] Obtain lawful current SDK archive/version/build; record hash and full
  headers/utilities/sample/tool/resource diff against25.6. Do not distribute SDK.
- [ ] Reconcile all published native families/members, including new26.5 APIs and
  cross-host-only additions. Map topic → authoritative source → version → actual recipe.
- [ ] Cover published AE UXP objects and shared-platform contracts with AE host
  setup/manifest/permissions/UI/file/network/storage/lifecycle/packaging workflow.
- [ ] Review current scripting/expression object/member changes and missing operation
  recipes; distinguish ExtendScript, expression JS and UXP rather than porting by name.
- [ ] Read current host/platform requirements/release notes from a verifiable official
  route; close dated-snapshot gaps or explicitly report blocked assertions.
- [ ] Audit source/recipe completeness against current API inventory, not just the
  historical127 core menu entries. Overview L does not excuse a missing promised operation.
- [ ] Final source/date/link/provenance sweep, tests/generated outputs and new freeze.

First result: [AE UXP host operations](07-PANELS/03-UXP-HOST-API.md) now documents
actual published entry/version/identity/Undo/creation/readback boundaries. It closes
the roadmap-only gap for this bounded operation, **not this whole queue**.

## Native26.5 public-contract reconciliation

### Reproducible scripting inventory

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
