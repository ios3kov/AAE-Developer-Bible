# Status

Updated: **2026-10-01**

## Canonical editorial policy

All writing/editing rules are now consolidated in [EDITORIAL-GUIDE.md](EDITORIAL-GUIDE.md). The mandatory workflow is: finish one logical block → commit/validate → report status to the user → stop before the next block.

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
- CEP protocol reconciliation.
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

## Current editorial TODO

1. Sweep every main chapter for completeness against the editorial checklist.
2. Find underdeveloped/too-short sections and expand them.
3. Reconcile recipes/source examples with the latest explanatory chapters.
4. Review dated public facts before edition freeze.
5. Complete cross-link/provenance audit.
6. Freeze and publish the next coherent documentation edition.

## Research tracks

The built-in effects atlas and project case studies remain valuable ongoing tracks.

They are **appendices, not blockers**. Full reverse engineering of every bundled effect is not required before the core Bible can be editorially complete.

## References

- [Evidence ledger](VERIFICATION.md)
- [Coverage matrix](FINAL-COVERAGE-AUDIT.md)
- [Editorial completion plan](COMPLETION-PLAN.md)
- [Editorial checklist](COMPLETION-CHECKLIST.md)

No user AE action is required for the current editorial work.
