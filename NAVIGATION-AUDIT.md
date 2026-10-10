# Navigation audit — block 3

> Current reading note — 2026-10-10: the 46-row baseline and subsequent 27-omission result below are historical. The current candidate's omission list is emitted by MkDocs; archive/evidence/generated pages need not all appear in the main menu. Link/anchor validity is checked separately and strictly by [CI](CI-GATES.md). No historical count or browser result is replaced with a new unperformed observation.

## Current edition status — 2026-10-07

Block3 is editorially complete; OPEN/next-step wording below is historical.
Freeze static build checks core/reference HTML, local destinations/anchors, search
index and MASTER exclusion; browser ranking/private-profile findings below are
not rewritten. New block/reconciliation ledgers remain linked from STATUS/tracker;
filled pack from template index; legal/generated records from Home. Omitted menu
entries are evidence/archive/generated/service pages, not missing core chapters.
[Freeze record](EDITION-FREEZE-2026-10-07.md).

Baseline: `7bba4b0`, 46 omissions (41 thematic + 5 root) copied from retained `block2-followup-build.log`. Current local edits are uncommitted; block 3 OPEN. Omission means absent from menu, not unreachable.

## Access keys and scope

- N: [NAVIGATION](NAVIGATION.md), matching direct menu entry.
- S: [SDK Header Tools index](18-SDK-HEADER-TOOLS/README.md), explicit source-review/generated links.
- R: [investigation index](21-BUILTIN-EFFECTS-REVERSE-ENGINEERING/3D-Channel/3D-Channel-Extract/README.md), explicit links to ten research records.
- H: preserved historical alias URL; its HTML links to the matching canonical audit document. No direct menu entry is required.
- Home: [README](README.md), explicit combined-edition/legal links.

HTML PASS means the generated page exists. Links/anchors across six entry pages were checked separately (290 checks); both alias-to-canonical HTML links were checked separately. This is static site evidence, not AE runtime evidence or full browser traversal of every page.

## Baseline decisions

| Path | Category | Menu decision | Entry | Reason | HTML |
|---|---|---|---|---|---|
| GLOSSARY.md | reference | menu | N | direct thematic access | HTML PASS |
| KNOWN-PITFALLS.md | reference | menu | N | direct thematic access | HTML PASS |
| MASTER-AE-DEVELOPER-BIBLE.md | generated | Home link | Home | generated duplicate; search excluded | HTML PASS |
| NAVIGATION.md | core | menu | N | direct thematic access | HTML PASS |
| NOTICE.md | legal/service | Home link | Home | legal/service notice | HTML PASS |
| 02-EFFECT-PLUGINS/08-AUXILIARY-CHANNELS.md | core | menu | N | direct thematic access | HTML PASS |
| 02-EFFECT-PLUGINS/09-CUSTOM-UI-DRAWBOT.md | core | menu | N | direct thematic access | HTML PASS |
| 12-RECIPES/README.md | core | menu | N | direct thematic access | HTML PASS |
| 13-TEMPLATES/README.md | core | menu | N | direct thematic access | HTML PASS |
| 18-SDK-HEADER-TOOLS/05-SUPPLIED-SDK-25.6.md | SDK evidence | index | S | scoped SDK evidence | HTML PASS |
| 18-SDK-HEADER-TOOLS/06-PARAMETERS-PIXELS-SDK25.6.md | SDK evidence | index | S | scoped SDK evidence | HTML PASS |
| 18-SDK-HEADER-TOOLS/07-MEMORY-MFR-SDK25.6.md | SDK evidence | index | S | scoped SDK evidence | HTML PASS |
| 18-SDK-HEADER-TOOLS/08-REGISTRATION-AEGP-SDK25.6.md | SDK evidence | index | S | scoped SDK evidence | HTML PASS |
| 18-SDK-HEADER-TOOLS/09-AEGP-PROJECT-RENDER-SDK25.6.md | SDK evidence | index | S | scoped SDK evidence | HTML PASS |
| 18-SDK-HEADER-TOOLS/10-STREAMS-KEYFRAMES-SDK25.6.md | SDK evidence | index | S | scoped SDK evidence | HTML PASS |
| 18-SDK-HEADER-TOOLS/11-MASK-TEXT-FOOTAGE-SDK25.6.md | SDK evidence | index | S | scoped SDK evidence | HTML PASS |
| 18-SDK-HEADER-TOOLS/12-AEIO-ARTISAN-SDK25.6.md | SDK evidence | index | S | scoped SDK evidence | HTML PASS |
| 18-SDK-HEADER-TOOLS/13-PANELS-BLITHOOK-SDK25.6.md | SDK evidence | index | S | scoped SDK evidence | HTML PASS |
| 18-SDK-HEADER-TOOLS/14-PICA-BRIDGES-LEGACY-SDK25.6.md | SDK evidence | index | S | scoped SDK evidence | HTML PASS |
| 18-SDK-HEADER-TOOLS/15-GPU-AUDIO-CUSTOM-UI-SDK25.6.md | SDK evidence | index | S | scoped SDK evidence | HTML PASS |
| 18-SDK-HEADER-TOOLS/16-GATE4-ACCEPTANCE-RUNBOOK.md | archive/alias | keep alias | H | historical URL; canonical document link | HTML PASS |
| 18-SDK-HEADER-TOOLS/17-GATE4-SDK25.6-RUN-2026-10-01.md | archive/alias | keep alias | H | historical URL; canonical document link | HTML PASS |
| 18-SDK-HEADER-TOOLS/generated/README.md | archive/generated | index | S | fixture/tooling | HTML PASS |
| 18-SDK-HEADER-TOOLS/generated/fixture-inventory.md | archive/generated | index | S | fixture/tooling | HTML PASS |
| 20-REFERENCE-IMPLEMENTATIONS/AEGP/Keyframer/README.md | reference | menu | N | direct thematic access | HTML PASS |
| 20-REFERENCE-IMPLEMENTATIONS/AEGP/MenuTool/README.md | reference | menu | N | direct thematic access | HTML PASS |
| 20-REFERENCE-IMPLEMENTATIONS/AEGP/NativePanel/README.md | reference | menu | N | direct thematic access | HTML PASS |
| 20-REFERENCE-IMPLEMENTATIONS/AEIO/MinimalRegistrar/README.md | reference | menu | N | direct thematic access | HTML PASS |
| 20-REFERENCE-IMPLEMENTATIONS/Artisan/MinimalRegistrar/README.md | reference | menu | N | direct thematic access | HTML PASS |
| 20-REFERENCE-IMPLEMENTATIONS/Bridges/Effect-AEGP/README.md | reference | menu | N | direct thematic access | HTML PASS |
| 20-REFERENCE-IMPLEMENTATIONS/Bridges/PICA-Provider-Consumer/README.md | reference | menu | N | direct thematic access | HTML PASS |
| 20-REFERENCE-IMPLEMENTATIONS/Effect/CustomUI-Drawbot/README.md | reference | menu | N | direct thematic access | HTML PASS |
| 20-REFERENCE-IMPLEMENTATIONS/Effect/SmartFX-MFR/README.md | reference | menu | N | direct thematic access | HTML PASS |
| 20-REFERENCE-IMPLEMENTATIONS/GPU/README.md | reference | menu | N | direct thematic access | HTML PASS |
| 20-REFERENCE-IMPLEMENTATIONS/Scripts/ScriptUI-Panel/README.md | reference | menu | N | direct thematic access | HTML PASS |
| 21-BUILTIN-EFFECTS-REVERSE-ENGINEERING/3D-Channel/3D-Channel-Extract/README.md | research | menu | N | direct thematic access | HTML PASS |
| 21-BUILTIN-EFFECTS-REVERSE-ENGINEERING/3D-Channel/3D-Channel-Extract/AUXILIARY-FIXTURE-CANDIDATE.md | research | index | R | research; preserve evidence status | HTML PASS |
| 21-BUILTIN-EFFECTS-REVERSE-ENGINEERING/3D-Channel/3D-Channel-Extract/BINARY-EVIDENCE-MACOS-AE25.6.md | research | index | R | research; preserve evidence status | HTML PASS |
| 21-BUILTIN-EFFECTS-REVERSE-ENGINEERING/3D-Channel/3D-Channel-Extract/EDGE-AND-RENDER-PROBE.md | research | index | R | research; preserve evidence status | HTML PASS |
| 21-BUILTIN-EFFECTS-REVERSE-ENGINEERING/3D-Channel/3D-Channel-Extract/EVIDENCE-AUDIT-2026-09-30.md | research | index | R | research; preserve evidence status | HTML PASS |
| 21-BUILTIN-EFFECTS-REVERSE-ENGINEERING/3D-Channel/3D-Channel-Extract/FILTERMAIN-FUNCTION-MAP-MACOS-AE25.6.md | research | index | R | research; preserve evidence status | HTML PASS |
| 21-BUILTIN-EFFECTS-REVERSE-ENGINEERING/3D-Channel/3D-Channel-Extract/HOST-CHANNEL-READOUT-CONTRACT.md | research | index | R | research; preserve evidence status | HTML PASS |
| 21-BUILTIN-EFFECTS-REVERSE-ENGINEERING/3D-Channel/3D-Channel-Extract/INPUT-QUALIFICATION-2026-09-30.md | research | index | R | research; preserve evidence status | HTML PASS |
| 21-BUILTIN-EFFECTS-REVERSE-ENGINEERING/3D-Channel/3D-Channel-Extract/MEGA-PROBE.md | research | index | R | withdrawn tool record | HTML PASS |
| 21-BUILTIN-EFFECTS-REVERSE-ENGINEERING/3D-Channel/3D-Channel-Extract/NUMERICAL-OBSERVATIONS-2026-09-30.md | research | index | R | research; preserve evidence status | HTML PASS |
| 21-BUILTIN-EFFECTS-REVERSE-ENGINEERING/3D-Channel/3D-Channel-Extract/RUNTIME-ACCEPTANCE-MACOS-AE25.6.md | research | index | R | research; preserve evidence status | HTML PASS |

## Generation and current omissions

MkDocs 1.6.1 / Material 9.6.23 (`requirements-docs.txt`: `mkdocs-material==9.6.23`). NAVIGATION and menu are source files; build_docs stages docs and regenerates MASTER/MANIFEST. Strict build, generation/check and diff checks PASS for this local iteration. Three route anchors and SDK source-review anchor exist.

27 current omissions, all explained above: MASTER + NOTICE (2), SDK source reviews (11), Gate4 aliases (2), generated tooling (2), research records below the investigation index (10). The original 46 baseline rows are retained. Canonical records, reference guides, Auxiliary Channels and Drawbot have explicit menu/index access. Research/MEGA statuses are unchanged; no collector development or AE run requested.

## MASTER search decision

MASTER remains generated Markdown and HTML, linked from Home. It is excluded from search because it duplicates source chapters. The exclusion is set by scripts/build_docs.py, not by editing generated MASTER. No original chapter metadata, alias/research exclusion, ranking or language settings were changed.

Before exclusion the observed MASTER contribution was 3200 search records. The current probe checks HTML existence, a nonempty index and zero MASTER records. Total remaining records vary after report edits and are not an acceptance constant. Static token matches from the earlier second-part build were not browser ranking evidence.

## Browser search — 2026-10-04

Served built site over HTTP at 127.0.0.1:8000. Auxiliary Channels was initially checked in a new Incognito window. Native-window focus interfered with later input; all eight queries were then reviewed in a fresh dedicated normal Chrome tab. All-private replay remains NOT RUN.

Positions count result-pages, not section hits. Only the first ten loaded result-pages were examined; positions beyond ten are not inferred. Criterion: intended page within first five plus successful target navigation.

| Query | Target position / observation | Click verification | Result |
|---|---|---|---|
| Auxiliary Channels | core chapter absent from first 10 | target NOT RUN | FAIL |
| Drawbot | core 1; reference 3 | core opened; reference click NOT RUN | core PASS; reference partial |
| ScriptUI | reference 1; core 2 | reference opened | PASS |
| AEGP MenuTool | template 3; reference 4 | reference opened | PASS |
| SDK 25.6 | canonical audit / index absent from first 10 | target NOT RUN | FAIL |
| Gate4 | registry 1, SDK overview 2; aliases absent | alias NOT RUN | FAIL for alias target |
| маршрут | NAVIGATION 1 | opened; three headings present | PASS |
| автоматизация | decision tree 1; route/scripting/AEGP absent | target NOT RUN | FAIL for stated target |

All three Home links were clicked without URL entry and reached route-effect, route-automation and route-native. Search returned results without an observed stall. Captured errors originate in installed chrome-extension scripts; a clean console cannot be claimed. MASTER absence is proven by full index inspection, not sampled browser results.

## Remaining work

Block 3 OPEN: search relevance, all-private replay, remaining target/reference clicks and full core/reference reachability need completion/review. No commit or GitHub CI for these local edits. No new AE/CEP/native runtime claims.

## Bilingual search iteration — 2026-10-04

Only search.lang was changed to [en, ru]; no separator, boost, chapter metadata, menu or source chapter changes. Generation/check and strict build PASS; index config.lang is [en, ru]. The preceding browser table remains historical.

Environment: dedicated Codex in-app browser, HTTP localhost. Its observed resource inventory includes search/search_index.json; server traffic includes lunr.ru and lunr.multi assets. No warnings/errors were captured for this tab. A newly reset clean browser profile and inspection of the Network response body were not established; those conditions are NOT VERIFIED. This is a bounded browser repeat, not a claim of meeting every requested environment condition.

Gate4 criterion revised: find the explanation of the old name and reach the current document, not necessarily the alias page. Automation criterion revised: a decision-tree entry with an explicit working route link is acceptable. Historical FAIL labels above are preserved.

| Query | Target position | Transition | Current result |
|---|---|---|---|
| Auxiliary Channels | core absent from first 10 | target NOT RUN | FAIL |
| Drawbot | core 1; reference 3 | reference opened, correct heading | PASS with prior core click evidence |
| ScriptUI | reference 1; core 2 | reference opened, correct heading | PASS |
| AEGP MenuTool | template 1; reference 3 | reference opened, correct heading | PASS |
| SDK 25.6 | compatibility alias 1; canonical/index absent from first 10 | alias transition NOT RUN in this query | PARTIAL useful alias; strict canonical/index criterion FAIL |
| Gate4 | SDK overview 2 | search → overview → canonical record, explanation visible | PASS under revised criterion |
| маршрут | NAVIGATION 2 | opened; three route headings present | PASS |
| автоматизация | decision tree 1 | search → decision tree → NAVIGATION/#route-automation | PASS under revised criterion |

### English query diagnostics

The Auxiliary core is indexed in 11 records. Its main title is Russian, and none of its title/text records contains the exact phrase Auxiliary Channels. This establishes a naming mismatch, not an absent page. Exact-phrase absence alone does not prove all ranking causes.

The SDK overview and canonical record are indexed. The canonical page's main record has an empty text field because its body starts under Scope; the Scope record contains the SDK identity and evidence boundary. Source-review pages and a compatibility alias outrank the canonical/index targets. Ranking failure remains; no boost is applied without review.

First five result-pages (URL paths are relative to http://127.0.0.1:8000):

| Query | Rank | Indexed/display title | URL path |
|---|---:|---|---|
| Auxiliary Channels | 1 | AEIO — media import/export plug-ins | /04-AEIO/ |
| Auxiliary Channels | 2 | Auxiliary input candidate — known data before another AE run | /21-BUILTIN-EFFECTS-REVERSE-ENGINEERING/3D-Channel/3D-Channel-Extract/AUXILIARY-FIXTURE-CANDIDATE/ |
| Auxiliary Channels | 3 | Auxiliary channel readout — contract and offline gate | /21-BUILTIN-EFFECTS-REVERSE-ENGINEERING/3D-Channel/3D-Channel-Extract/HOST-CHANNEL-READOUT-CONTRACT/ |
| Auxiliary Channels | 4 | Auxiliary input qualification — result, 2026-09-30 | /21-BUILTIN-EFFECTS-REVERSE-ENGINEERING/3D-Channel/3D-Channel-Extract/INPUT-QUALIFICATION-2026-09-30/ |
| Auxiliary Channels | 5 | Footage / import: ownership, interpretation, sequences and proxies | /17-NATIVE-SUITE-COOKBOOK/09-FOOTAGE-IMPORT/ |
| SDK 25.6 | 1 | Compatibility alias — SDK 25.6 contract audit record | /18-SDK-HEADER-TOOLS/17-GATE4-SDK25.6-RUN-2026-10-01/ |
| SDK 25.6 | 2 | SDK 25.6: masks, text/markers и footage/import ownership | /18-SDK-HEADER-TOOLS/11-MASK-TEXT-FOOTAGE-SDK25.6/ |
| SDK 25.6 | 3 | SDK 25.6: AEGP streams, properties и keyframes | /18-SDK-HEADER-TOOLS/10-STREAMS-KEYFRAMES-SDK25.6/ |
| SDK 25.6 | 4 | SDK 25.6: AEIO и Artisan | /18-SDK-HEADER-TOOLS/12-AEIO-ARTISAN-SDK25.6/ |
| SDK 25.6 | 5 | SDK 25.6: native panels и BlitHook | /18-SDK-HEADER-TOOLS/13-PANELS-BLITHOOK-SDK25.6/ |

### Indexed main records and Scope excerpt

```json
{
  "location": "02-EFFECT-PLUGINS/08-AUXILIARY-CHANNELS/",
  "title": "Дополнительные каналы: глубина, ID, нормали и сырые данные",
  "text_start": "<p>Основа: заголовки из присланного SDK 25.6 build 61. Это глава о публичном контракте данных, не новый collector и не протокол запуска эксперимента. Идентичность SDK.</p> <p>Главное различие: RGBA изображения и auxiliary-данные источника — не одно и то же. Серое изображение может визуализировать глубину, но наличие серых пикселей само по себе не означает, что источник предоставляет канал <code>DPTH</code>. В SDK получение auxiliary-описаний и buffers оформлено отдельным <code>PF_ChannelSuite1</code>. [C1], [C2]</p>"
}
```

```json
{
  "location": "18-SDK-HEADER-TOOLS/",
  "title": "SDK Header Tools — exact contract audit helpers",
  "text_start": "<p>These tools keep version-sensitive Bible claims aligned with a real Adobe SDK.</p> <p>They are not a requirement to compile the whole Bible.</p>"
}
```

```json
{
  "location": "18-SDK-HEADER-TOOLS/17-SDK25.6-CONTRACT-AUDIT-2026-10-01/",
  "title": "SDK 25.6 required-contract audit — 2026-10-01",
  "text_start": ""
}
```

```json
{
  "location": "18-SDK-HEADER-TOOLS/17-SDK25.6-CONTRACT-AUDIT-2026-10-01/#scope",
  "title": "Scope",
  "text_start": "<p>This record is a real-header SDK contract audit against the user-supplied Adobe After Effects SDK 25.6 build 61.</p> <p>It establishes required contract-table/function coverage and cookbook suite-generation symbol coverage. It does not establish macOS/Windows compilation, linking, PiPL/resource build, After Effects host execution or runtime semantics.</p>"
}
```

Observed browser iteration index SHA-256: `ec8fe9332e7161e32ca302d51df5743d96f33e8e260d3bfd449b6b0b1005f4cc`. Later report regeneration changes the indexed report content; positions above belong to this snapshot, not an unperformed repeat of the final report build.

Block 3 remains OPEN: English relevance, fully verified browser freshness, and full core/reference reachability remain unresolved.

## Final acceptance — 2026-10-04

Block 3 CLOSED in editorial scope. Earlier OPEN/Remaining work paragraphs are historical iteration records, superseded by this acceptance.

User decision: stop search configuration; boosts, separator, clean-profile verification and another ranking pass are not required. SDK 25.6 ranking and prior browser environment limitations remain recorded, without becoming completion blockers. Existing Russian Auxiliary H1 now includes (Auxiliary Channels); its indexed chapter records contain the exact SDK term. Other chapter content is unchanged.

Full inventory: 127 unique core table rows from CHAPTER-COMPLETION-TRACKER, matching the core source inventory after excluding separate evidence/verification appendices; 26 reference pages comprising all Markdown under 16-WORKING-TEMPLATES and 20-REFERENCE-IMPLEMENTATIONS plus GLOSSARY, KNOWN-PITFALLS and SDK Header Tools overview. Total 153 unique pages. Published menu/article-link traversal reaches all 153; all their HTML pages exist. 498 local article targets/anchors checked, zero failures. All 183 menu paths are represented in NAVIGATION; no unexplained menu omissions. This extends, rather than reuses as full coverage, the earlier 290 checks of six entry pages.

Generation/check, strict build and diff checks PASS. Search language config en/ru and MASTER exclusion preserved. No additional browser rank replay or AE/CEP/native runtime run. Final report edits can change search ranking; no unperformed ranking claim applies to the final build. Block 4 not started.

## Block 4 consistency guard handoff — 2026-10-04

Block 3 remains closed. Block 4 is in local review: 127 unique core table rows now guarded against source inventory drift, nested-menu removal and NAVIGATION omissions. CEP examples and scoped evidence-boundary guards are separate checks. Source-content SHA-256 in generated MASTER excludes outputs and uses relative paths; Git source SHA is recorded separately by CI/bot provenance, not mislabeled as the content digest. Local tests PASS; exact-revision GitHub runs NOT RUN. The base for these dirty changes is 9e72ea2828650bda097e5496f2ce7ffc7660e6c8. Full block 3 HTML evidence is not reclassified as a new runtime/CI result.

### GitHub handoff update

Source candidate b6f99db15d0d2b30c5d0e5baa0554eae0198e323 passed Validate on Linux/macOS and both ACX workflows. Draft PR 1 publishes accepted block 3 plus block 4; remote main remains 7bba4b0. Subsequent report/generated commits require separate exact-SHA CI evidence. Main-only bot-regeneration is still NOT RUN; block 4 is not declared closed.


## Block 4 completion — 2026-10-04

PR #1 merged at c64b3032be815803fe743ad10a995725aac2231f. The bounded consistency guards and source/frozen lanes are complete. Actual GitHub PR regeneration produced 1f0b792 from source 24fef6f; final-head Linux/macOS Validate PASS, repeat regeneration changed:false. Full SHA/run provenance and separate main workflow outcome are in VERIFICATION.md. No additional browser/search experiments or AE/CEP/native runtime checks were performed. Block 3 navigation evidence and accepted search limits remain unchanged; block 5 is next, not started.


## Block 5 source entry points — 2026-10-04

Added BLOCK-5-SOURCES.md and BLOCK-5-REVIEW-2026-10-04.md to menu/NAVIGATION and linked from SOURCES. Earlier 183-entry/498-link block 3 results remain historical; this change adds two entries and does not inherit an unperformed full-site rerun. Source table local targets and nine affected rendered content pages were checked separately: 1,913 internal HTML destination/anchor checks PASS. No additional browser ranks, search-profile experiments or AE host runs.


## Block 5 merged — 2026-10-04

PR #2 merged at 8e95a2df24433bfe2f58a1bb42b50f30c9cdf9c8. Source/version table and reviewed JSON are published in main; exact-head PR source/frozen checks passed. Post-merge workflow evidence is recorded in VERIFICATION.md. No additional full-site or browser evidence is inferred from this status update. Block 6 is Effect state/arbitrary data and remains unstarted.
