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
