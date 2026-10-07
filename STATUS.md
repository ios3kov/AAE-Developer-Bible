# Status

Updated: **2026-10-04**

## Continuous completion — 2026-10-07

Fresh real-SDK syntax/type check: 13/13 PASS at clean source
`ef4e90b1c96c6a9a1cb34b5c2260b2561b20e7eb`, supplied SDK25.6build61,
Apple Clang21 arm64. [Exact evidence](VERIFICATION.md). Not link/host evidence.

Latest review: MenuTool ping versus recommended mutation chain, queue helper
missing preflight/path-readback/rollback, fixed comp and truncated LayerID source
limits are now explicit. Local portable regression sweep recorded against exact
source `429ea45f5d16e5135cc930e0fc7e230cf0ebcf97`; no host result implied.

Chapter-level follow-up: five Effect-state rows now C with
[explicit source reconciliation](CHAPTER-RECONCILIATION-2026-10-07.md), not automatic
closure from build PASS. Corrected payload-field versus new-parameter migration IDs.
Remaining chapter rows retain their actual open status; final freeze not yet claimed.

Owner authorized continuing between checked blocks without approval pauses.
Block 6 content implemented: arbitrary data/state migration, SDK ownership map,
portable codec and Minimal Gain identity table. [Review](BLOCK-6-REVIEW-2026-10-07.md).
Next: block 7 spatial/temporal SmartFX. No new AE runtime claim.

Blocks 7–10 additions now in progress: numeric ROI/temporal dependencies, cache
receipt and GPU failure routes, bounded Drawbot/audio, scripting demo rig. These
additions are not a claim that all tracker reconciliation/freeze tasks are closed.

Blocks 11–15 practical additions implemented: AEGP operation chains, copied SDK
Skeleton platform routes, exact IO/Artie maps, worked evidence pack and scoped
ElasticGridFX case study. Chapter tracker remains the outstanding queue; license
decision and full per-page reconciliation are not silently closed. Next: cross-page
source/recipe review and final checks, not a new product QA requirement.

## Canonical editorial policy

All writing/editing rules are now consolidated in [EDITORIAL-GUIDE.md](EDITORIAL-GUIDE.md). The mandatory workflow is: finish one logical block → commit/validate → report status to the user → stop before the next block.

## План завершения после аудита — 2026-10-02

**Блоки 2–5 выполнены 2026-10-04 в редакционной области.** Навигация: 153 core/reference страницы, 498 ссылок/якорей PASS. Блок 4: exact-head PR bot regeneration и Validate Linux/macOS PASS; PR #1 слит в main на `c64b303`. Детальные SHA и post-merge проверки — в [VERIFICATION](VERIFICATION.md). Блок 5 слит через PR #2 на `8e95a2d`: 27 source/claim records, platform rereview и practical-depth comparison; лицензия по решению владельца пока неопределённа. Блок 6 ещё не начат.

Зафиксирован [аудит текущей редакции](EDITORIAL-AUDIT-2026-10-02.md) и [план из 16 логических блоков](COMPLETION-PLAN.md). **Блок 1 — единая редакционная готовность и evidence: выполнен.** Блок 2 согласовал protocol/envelopes, `renameSelected({prefix})`, bootstrap и unknown-outcome policy. Добавлены portable regression tests в Validate; follow-up изолировал Unicode fixture и повторно проверил отдельный INTERNAL_ERROR: 14/14 portable scenarios PASS, host execution не заявляется. [Результаты и ограничения](VERIFICATION.md#block-2-cep-protocol-and-failure-paths-2026-10-04).

Результат блока 1:

- В active chapters/source guides убраны устаревшие этапы обязательной build/host приёмки Bible; product-validation scenarios сохранены с правильной областью.
- Исторический compiler PASS от 2026-09-30 больше не присваивается нынешним recipes/reference sources: exact tested source identity в старой записи отсутствует.
- SDK-review records и evidence ledger объясняют исторические Gates; результаты, хэши и NOT RUN своей итерации сохранены.
- Case-study overview исправлен: independent FSTR portable rerun уже выполнен для pinned snapshot.
- [Поглавный трекер](CHAPTER-COMPLETION-TRACKER.md) охватывает 127 core pages, пять осей готовности и конкретные результаты следующих блоков.

Локальные документационные проверки **PASS**; результаты GitHub CI читаются отдельно по опубликованному source SHA. Проверки и ограничения фиксируются в [ledger](VERIFICATION.md#block-1-editorial-readiness-and-evidence-2026-10-02). Новая native-компиляция и AE execution не заявляются.

[ElasticGridFX transfer plan](22-PROJECT-CASE-STUDIES/ELASTICGRIDFX-TRANSFER-PLAN-2026-10-02.md) добавляет scoped performance/release lessons в существующие блоки. Source snapshot закреплён; перенос в core главы и адаптация tools пока не выполнены. Новые SDK/native/AE результаты не заявляются.

## Внешние источники — завершённый targeted review

[Отчёт от 2026-10-02](EXTERNAL-SOURCES-REVIEW-2026-10-02.md) закрепляет четыре source snapshots и выводы выбранных проверок. У secondary KB current-25.6 matrix выявлены расхождения; web guides также требуют per-member/version чтения. Полная построчная валидация внешних коллекций не заявляется.

В core добавлены import preflight и provenance/invalidation уточнения, CEP manifest/library/bootstrap diagnostic chain, native source comparison и актуальная граница published UXP docs versus actual host proof. Синтаксис собственного import helper проверен; ошибочный upstream example воспроизведён syntax-only проверкой. Новые native/AE/CEP/UXP runtime результаты — NOT RUN. В этом external review блоки 2, 5 и 10 были закрыты лишь в отдельных пунктах. Блок 2 завершён отдельной итерацией 2026-10-04; задачи блоков 5/10 остаются открыты.

## Current mission

AE Developer Bible — **research-backed practical documentation for After Effects developers**.

Текущая работа: **писать, расширять, сверять и согласовывать Bible**. Репозиторий не должен превращаться в отдельный проект по обязательной сборке и host-QA всех демонстрационных plug-ins.

## Current editorial state

Core structure covers:

- architecture and extension selection;
- Effect / SmartFX / MFR / GPU / Custom UI / audio;
- AEGP;
- AEIO;
- Artisan;
- scripting / ScriptUI / CEP / UXP transition;
- native panels / PICA / bridges;
- macOS and Windows development;
- testing / debugging / diagnostics;
- distribution / signing / packaging;
- recipes and templates;
- native suite cookbook;
- SDK header/source review;
- reference source examples;
- reverse-engineering atlas;
- real-project case studies.

The current priority is a **section-by-section editorial completeness and consistency sweep**.

## SDK 25.6 baseline

The supplied Adobe After Effects SDK **25.6 build 61** anchors the native source review.

Eleven source-review records cover the high-risk native areas from Effect anatomy through GPU/audio/Custom UI.

The real-header audit on 2026-10-01 records:

- **35/35 required SDK contracts present**;
- **39/39 cookbook call-sites resolved** to expected suite generations;
- **0 required parser diagnostics**;
- four unrelated partial parser diagnostics retained explicitly.

This establishes the **contract baseline used by the documentation**. It does not create a requirement to compile the whole repository.

See [SDK tools](18-SDK-HEADER-TOOLS/README.md), [SDK source record](18-SDK-HEADER-TOOLS/05-SUPPLIED-SDK-25.6.md) and [real-header audit](18-SDK-HEADER-TOOLS/17-SDK25.6-CONTRACT-AUDIT-2026-10-01.md).

Historical filenames containing “Gate 4” are retained for stable links/history; the old build-gate completion model is superseded.

## Major editorial work completed

- Effect lifecycle, parameter, pixel, color and SmartFX explanations.
- Memory/ownership/threading/MFR source review.
- AEGP lifecycle, project graph, render queue and frame-render contracts.
- Streams/keyframes/masks/text/marker/footage cookbook alignment.
- AEIO and Artisan architecture.
- Native panels, PICA bridges and legacy boundaries.
- GPU/audio/Custom UI source-review chapters.
- Scripting/ScriptUI/CEP communication architecture.
- macOS/Windows build, debugging, signing and packaging guidance.
- Test/evidence/release methodology.
- Historical CEP field-name reconciliation; remaining envelope/error-path defects are scheduled in block 2.
- Render-queue enum correction.
- 3D Channel Extract historical classification correction.
- FSTR Line / AE Hot Loader reuse audit.
- Safe repository tooling where destructive behavior was possible.

## Evidence boundary

The Bible uses runtime evidence when it exists, but **runtime evidence is not mandatory for every source example**.

“Source-reviewed, runtime not claimed” is a complete and valid editorial state when the text makes no runtime assertion.

Historical compiler/runtime results remain useful evidence about their snapshots, not release requirements for the documentation.

## Editorial completeness sweep — wave 1

Expanded entry/architecture/platform/native chapters now include consistent coverage of selection criteria, lifecycle, ownership, threading, failure modes, production workflow, related chapters and evidence boundaries.

Wave 1 covered:

- extension selection and environment matrix;
- native lifecycle, version compatibility and communication architecture;
- scripting and panel entry architecture;
- macOS/Windows platform entry pages;
- macOS/Windows GPU guidance;
- Windows debugging;
- native taxonomy, host-call flows and AEGP tools;
- Keyframers;
- guides/views/selection;
- documentation errata;
- header-first and SDK-diff methodology.

Strict-link failures introduced during expansion were corrected; the documentation tree returned to green strict validation.

### Memory / lifetime / threading

Completed as a single cookbook/foundation block:

- `12-MEMORY-UNDO-PERSISTENCE.md`;
- `14-LIFETIME-THREADING.md`;
- Native C++ foundation suite acquisition / RAII / undo / host callback boundary docs.

The block now uses one consistent model for ownership, cleanup, invalidation, thread permission, persistence, partial failure and shutdown.

### Effects / streams / keyframes

Completed as one source/cookbook/reference block:

- `EffectSuite5` current baseline reconciled across cookbook, canonical recipe, ownership helper and Effect↔AEGP bridge docs;
- `StreamSuite6` / `DynamicStreamSuite4` retained as SDK 25.6 stream baseline;
- `KeyframeSuite5` retained as SDK 25.6 keyframe baseline;
- source examples, Keyframer references and product-validation language aligned with `EDITORIAL-GUIDE.md`.

### Masks / text / markers / footage

Completed as one ownership/import block:

- MaskRef/outline stream/value ownership and structural invalidation reconciled;
- TextDocument and UTF-16 MemorySuite lifetimes clarified;
- Marker stream timing, payload ownership and standalone marker ownership separated;
- Footage caller-owned → project-adopted transition and failure rollback made explicit;
- Footage Suite versus AEIO responsibility boundary made explicit;
- product validation wording aligned with `EDITORIAL-GUIDE.md`.

### AEIO import / export lifecycle

Completed as one SDK/source/reference block:

- `AEIO_FunctionBlock4` lifecycle mapped to current `IOInSuite7` / `IOOutSuite6`;
- spec/options ownership and flat/live persistence separated;
- random/sparse frame, audio, metadata, auxiliary-channel and output-finalization guidance expanded;
- cancellation, untrusted-media validation and partial-failure cleanup made explicit;
- Footage Suite versus AEIO responsibility boundary reconciled;
- reference/template evidence wording aligned with `EDITORIAL-GUIDE.md`.

### Artisan renderer lifecycle

Completed as one renderer-architecture/source-reference block:

- current `PR_ArtisanEntryPoints + CanvasSuite8 + ArtisanUtilSuite1` baseline reconciled;
- Global/Instance/Render state and versioned persistence separated;
- scene extraction, context ownership, textures/worlds/receipts and cache identity documented;
- bins/track mattes, camera/light/time, motion blur, ROI/downsample and unsupported-scene policy expanded;
- interactive/final state, cancellation, failure cleanup and threading boundaries clarified;
- Artie historical suite generations retained only as sample pattern evidence;
- template/reference wording aligned with `EDITORIAL-GUIDE.md`.

### Native Panels / BlitHook

Completed as one workspace/display-lifecycle block:

- Native Panel registration, stable identity, host-container vs product-child ownership, recreation and shutdown clarified;
- panel model/project model and worker handoff boundaries documented;
- BlitHook borrowed-buffer lifetime, row-aware staging, blank frames, view metadata, backpressure and display-color semantics expanded;
- asynchronous BlitHook behavior remains deliberately unclaimed beyond verified source contract;
- template/reference/source-review and communication evidence language aligned with `EDITORIAL-GUIDE.md`.

### PICA / Effect↔AEGP / legacy boundaries

Completed as one native-service/bridge/migration block:

- PICA ABI identity, provider/consumer lifetime, version adapters, shutdown and suite-name ownership clarified;
- Effect↔AEGP generic bridge aligned to current `EffectSuite5`, late target resolution and size/versioned synchronous payload semantics;
- render dependency and persistent-state boundaries clarified;
- legacy current-generation typo fixed and migration guidance split into source modernization versus behavior/project compatibility;
- templates/references/source-review evidence wording aligned with `EDITORIAL-GUIDE.md`.

## Current editorial TODO

1. Start block 6: Effect state and arbitrary data.
2. Resolve the owner-deferred license decision before block 16 edition freeze.
3. Follow blocks 7–15 and update each affected row in the chapter tracker.
4. Complete block 16: source/link/provenance sweep and edition freeze.

## Research tracks

The built-in effects atlas and project case studies remain valuable ongoing tracks.

They are **appendices, not blockers**. Full reverse engineering of every bundled effect is not required before the core Bible can be editorially complete.

## References

- [Evidence ledger](VERIFICATION.md)
- [Coverage matrix](FINAL-COVERAGE-AUDIT.md)
- [Chapter completion tracker](CHAPTER-COMPLETION-TRACKER.md)
- [Editorial completion plan](COMPLETION-PLAN.md)
- [Editorial checklist](COMPLETION-CHECKLIST.md)

No user AE action is required for the current editorial work.
