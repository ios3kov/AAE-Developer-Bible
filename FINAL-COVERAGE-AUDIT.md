# Coverage matrix

Edition: **1.1 editorial freeze**, updated 2026-10-07.

This matrix describes **documentation coverage, reference material and evidence boundaries**. It is not a product QA scoreboard.

[Поглавный трекер завершения](CHAPTER-COMPLETION-TRACKER.md) дополняет эту обзорную матрицу конкретными задачами для всех 127 core pages. Он не объявляет полную готовность направлений по одной обзорной оценке «strong/source reviewed».

| Area | Documentation coverage | Reference material | Evidence / limit |
|---|---|---|---|
| Extension selection / architecture | strong | decision tree, communication maps | editorial/source reviewed |
| Classic Effect | lifecycle, parameters, pixels, color | Minimal Gain source example | SDK-contract reviewed; no shipping-binary claim |
| SmartFX / MFR | ROI, checkout, state, thread safety | pass-through/source examples | contract guidance; historical compiler record lacks exact tested source identity |
| GPU | backend lifecycle, device/world ownership, testing guidance | SDK sample path | source reviewed; no universal runtime claim |
| Custom UI / Drawbot | event model, drawing references, async boundary | acquisition skeleton | source reviewed; skeleton intentionally partial |
| Audio effects | selectors, sound world, checkout/checkin | guidance | supplied SDK has no bundled AUDIO_RENDER implementation |
| AEGP | hooks, suites, project/render automation | MenuTool/cookbook source | SDK-contract reviewed |
| Streams / keyframes | hierarchy, values, expressions, batching | cookbook source | SDK 25.6 generations source reviewed |
| Masks / text / markers / footage | ownership and operations | cookbook | SDK 25.6 source reviewed |
| Native panels | PanelSuite/Panelator architecture | registration/reference guidance | source reviewed |
| AEIO | import/export architecture and callback tables | sample path / registrar guidance | source reviewed |
| Artisan | renderer lifecycle / Canvas / entry points | sample path / registrar guidance | source reviewed |
| PICA / Effect↔AEGP | provider/consumer and generic-call protocols | bridge source patterns | SDK-contract reviewed |
| ExtendScript / ScriptUI | object model, UI, automation boundaries | scripts/source examples | documentation/source guidance |
| CEP / UXP transition | CEP architecture, bridge patterns, dated migration notes | CEP bridge source | dated public-source review |
| macOS | build/debug/sign/notarize/package workflows | platform recipes | guidance, not a claim Bible shipped binaries |
| Windows | Visual Studio/arch/debug/sign/package workflows | platform recipes | guidance, not a claim Bible shipped binaries |
| Testing | correctness, MFR, perf, crash diagnostics, evidence design | templates/checklists | guidance for reader products |
| Distribution | versioning, installers, release artifacts, licensing/security | release checklist/templates | platform/public-source review |
| SDK contract tooling | inventory, required tables/functions, suite-generation checks | tools + records | real SDK 25.6: 35/35 required, 39/39 calls |
| C++ foundation | suite lifetime, owners, undo, callback boundary | reusable headers | source-reviewed + portable helper tests |
| Working templates | source-shaped integration patterns | C++/JSX/CEP snippets | examples illustrate contracts, not release artifacts |
| Reference implementations | maps architecture to source/sample paths | reference directories | implementation aid, not completion gate |
| Built-in effect atlas | evidence/reconstruction methodology | 3D Channel Extract pilot | ongoing research appendix |
| Project case studies | FSTR Line / AE Hot Loader lessons | evidence-backed case studies | scoped project evidence |

## Evidence vocabulary

- **DOCUMENTED** — public/canonical documentation.
- **SDK-CONTRACT-REVIEWED** — checked against exact SDK header/sample material.
- **SOURCE EXAMPLE** — demonstrates an implementation pattern without asserting runtime outcome.
- **PROJECT-REPORTED / RUNTIME-OBSERVED** — concrete scoped execution evidence exists.
- **RECONSTRUCTED** — evidence-backed reverse engineering/inference.

Older labels such as `host-test-required` described a missing runtime claim. They are **not completion tasks for the Bible**.

## Editorial readiness rule

A section can be editorially complete without a Bible-owned host run when:

- the documented contract is sourced correctly;
- the example scope is stated honestly;
- runtime-specific claims are not invented;
- known limitations are explicit.

Compilation or host execution matters only when the text makes a claim that depends on that execution.

Block1 scoped legacy labels and historical compiler evidence. All127 core rows
are now individually reconciled C/explicit L; [freeze](EDITION-FREEZE-2026-10-07.md)
records completion, reproducibility and intentional limits. Existing SDK/compiler
results belong to their snapshots; no new whole-repository native/host result.

See [COMPLETION-CHECKLIST.md](COMPLETION-CHECKLIST.md).
