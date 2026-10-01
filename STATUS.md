# Status

**v1.1 — verified SDK syntax baseline and reproducible documentation**

Updated: **2026-10-01**. Previously recorded native compilation baseline: **Adobe SDK 25.6, macOS arm64, C++17**. Historical compiler results are separate from the editorial/source-review milestones below.

## Current work — writing the Bible from the supplied SDK

The supplied `ae25.6_61.64bit.AfterEffectsSDK` is the basis of eleven source-review records:

1. [Effect anatomy, SmartFX and auxiliary channels](18-SDK-HEADER-TOOLS/05-SUPPLIED-SDK-25.6.md).
2. [Parameters and pixels](18-SDK-HEADER-TOOLS/06-PARAMETERS-PIXELS-SDK25.6.md).
3. [Memory, lifetime and MFR](18-SDK-HEADER-TOOLS/07-MEMORY-MFR-SDK25.6.md).
4. [Registration, PiPL and AEGP lifecycle](18-SDK-HEADER-TOOLS/08-REGISTRATION-AEGP-SDK25.6.md).
5. [AEGP project and render automation](18-SDK-HEADER-TOOLS/09-AEGP-PROJECT-RENDER-SDK25.6.md).
6. [Streams and keyframes](18-SDK-HEADER-TOOLS/10-STREAMS-KEYFRAMES-SDK25.6.md).
7. [Masks, text/markers and footage/import](18-SDK-HEADER-TOOLS/11-MASK-TEXT-FOOTAGE-SDK25.6.md).
8. [AEIO and Artisan](18-SDK-HEADER-TOOLS/12-AEIO-ARTISAN-SDK25.6.md).
9. [Native panels and BlitHook](18-SDK-HEADER-TOOLS/13-PANELS-BLITHOOK-SDK25.6.md).
10. [PICA providers, Effect↔AEGP and legacy boundaries](18-SDK-HEADER-TOOLS/14-PICA-BRIDGES-LEGACY-SDK25.6.md).
11. [GPU, audio and Custom UI / Drawbot](18-SDK-HEADER-TOOLS/15-GPU-AUDIO-CUSTOM-UI-SDK25.6.md).

Completed editorial changes:

- [Effect anatomy](02-EFFECT-PLUGINS/01-ANATOMY.md): handler declaration, registration, lifecycle and Skeleton source.
- [Parameters and UI](02-EFFECT-PLUGINS/02-PARAMETERS-UI.md): indexes/IDs, setup macros, animation versus interpolation, changed-param versus UI-update callbacks, controls and source discrepancies.
- [SmartFX](02-EFFECT-PLUGINS/03-SMARTFX.md): dependency/rectangle/checkout-ID explanations, pre-render state and distinct cleanup contracts.
- [Pixels, color and alpha](02-EFFECT-PLUGINS/06-COLOR-PIXELS.md): ARGB formats, 16-bpc range, typed access, rowbytes/origin, HDR, alpha and export boundaries.
- [Auxiliary channels](02-EFFECT-PLUGINS/08-AUXILIARY-CHANNELS.md): semantic types, descriptors, requested/returned datatype, raw layout and mandatory checkin.
- [Memory, lifetime and errors](01-ARCHITECTURE/02-MEMORY-THREADING-ERRORS.md): resource ownership, paired release APIs, host-managed state locks, both flatten operations, pre-render deletion, error-preserving cleanup and limits of existing helpers.
- [MFR and thread safety](02-EFFECT-PLUGINS/04-MFR-THREAD-SAFETY.md): exact flags and selector constraints, read-only sequence access, mutable thread-local copies, Compute Cache keys/values/receipts and waiting modes.
- [AEGP project/render automation](03-AEGP/02-PROJECT-RENDER-AUTOMATION.md): project/item/comp/layer handles, Undo, render queue, frame receipts, async lifetime and an open render-state recipe mismatch.
- **Streams/properties and keyframes:** Cookbook chapters 05/06 are now aligned to SDK 25.6 `StreamSuite6` / `DynamicStreamSuite4` / `KeyframeSuite5`; expressions, dynamic hierarchy, separated dimensions, interpolation/ease and batch-keyframe ownership are documented with source limits.
- **Masks, text/markers and footage/import:** Cookbook chapters 07–09 now use SDK 25.6 generations (`MaskSuite6`, `MaskOutlineSuite3`, `TextDocumentSuite1`, `MarkerSuite3`, `FootageSuite5`, `ItemSuite9`, `CompSuite12`, `LayerSuite9`) and document MaskRef cleanup, UTF-16 handle lifetimes, marker payload/cue-point ownership and FootageH adoption/failure cleanup.
- **AEIO and Artisan:** import/export and custom-renderer chapters now document `AEIO_ModuleInfo`, frozen `AEIO_FunctionBlock4`, current IOIn7/IOOut6, aux-channel producer callbacks, output state, color metadata, `PR_ArtisanEntryPoints`, CanvasSuite8, PR global/instance/frame state and Artie sample-generation limits.
- **Native panels and BlitHook:** workspace-panel identity/create/flyout/visibility contracts are now sourced from `AEGP_PanelSuite1`/Panelator; BlitHook is separated as `AEGeneral` hook protocol 3.0 with 32/64/128 pixel-buffer metadata, view coordinates and explicitly unqualified async lifetime.
- **PICA providers and native bridges:** `SPBasicSuite` acquire/release, `SPSuitesSuite::AddSuite`, Sweetie/Checkout provider-consumer patterns, current `AEGP_EffectCallGeneric` command/time contract and historical sample/version boundaries are documented. Legacy samples are no longer treated as current ABI signatures by default.
- **GPU, audio and Custom UI/Drawbot:** GPU capability/setup/pre-render/render/setdown and GPU-world ownership are sourced from `AE_Effect.h`, `AE_EffectGPUSuites.h` and SDK_Invert_ProcAmp; audio selectors/flags/SoundWorld/checkout are documented with the explicit limitation that the supplied archive has no bundled AUDIO_RENDER implementation; custom UI now has a dedicated event/Drawbot/async-manager chapter using Custom_ECW_UI and CCU.
- **Scripting, panels and platform distribution:** object-model/ScriptUI chapters, CEP/UXP bridge architecture, hybrid native communication, macOS/Windows build-sign-package workflows and release/distribution gates were expanded from the public Adobe CEP/SDK guidance plus current Apple and Microsoft platform documentation. See [the dated platform source-review record](11-DISTRIBUTION/05-PLATFORM-SOURCE-REVIEW-2026-10-01.md).
- **Testing, recipes and templates:** test evidence is now separated into unit/build/host/release layers; matrix, render correctness, MFR stress, performance and crash chapters were expanded; a new evidence/acceptance chapter defines PASS/FAIL/BLOCKED/NOT_RUN; practical recipes and reusable report/spec/release templates were aligned to the same evidence model. The CEP working template protocol field was also reconciled with the communication chapter.
- [Registration, PiPL and loading](01-ARCHITECTURE/03-PIPL-AND-LOADING.md): separate registration/dispatcher/initializer contracts, resource Kind, symbols, architectures, version domains, outflags and platform resource pipelines.
- [AEGP lifecycle, hooks and suites](03-AEGP/01-HOOKS-SUITES.md): IDs/refcons, suite macros, callbacks and partial initialization; the existing MenuTool is reviewed, not changed or host-verified.
- [AEGP project and render automation](03-AEGP/02-PROJECT-RENDER-AUTOMATION.md): project graph and time, Undo versus rollback, queue states and invalidation, output settings, frame receipts, borrowed worlds, sync/async cancellation and cache boundaries.
- AEGP navigation, recipe warnings and VERIFICATION distinguish source review from compiler/host evidence.

## Latest synchronization and findings

The platform/distribution source review records the public CEP main-thread bridge contract, Adobe's dated UXP/CEP transition milestones, sample-first native build guidance, installer paths, Apple Developer ID/notarization requirements and Microsoft Authenticode tooling. It expands documentation only; no signing/notarization/installer/host result is promoted to PASS.


The previously pending STATUS/VERIFICATION registration update was written to main in commits `a5080a132d299b8ef20888e814f3c0513365710c` and `4cd4515e605783f9255edb59cf734d0cabe0f1fd`. It reconciles chapters already present by `859b9c6c816a7cb5a360f61869d1bcf1531aede3`; it is no longer only an unapplied ZIP patch.

The fifth review recorded the original render-queue defect: `RenderQueueRecipes.cpp` passed TRUE to an enum-status argument; TRUE=1 means UNQUEUED while QUEUED=2. The recipe has since been corrected at source level to use `AEGP_RenderItemStatus_QUEUED` and verify the state with `AEGP_GetRenderState`. Runtime queue behavior is still host-test-required; documentation CI does not turn the corrected source into an AE PASS.

The eleventh review records GPU/audio/custom-UI contracts and an important absence boundary: the supplied Examples tree declares audio selectors/flags but contains no bundled C/C++ effect implementation dispatching PF_Cmd_AUDIO_RENDER. It also documents the custom-UI async-manager requirement and Drawbot borrowed-vs-created resource ownership without claiming a host run.

The tenth review records 13 SDK source hashes and clarifies two important version boundaries: old ProjDumper generic-call syntax is not the current EffectSuite4 call shape, and bundled Commando uses an initializer signature that differs from the current AEGP prototype. Sweetie/Checkout establish provider/optional-consumer patterns but do not establish generic suite hot replacement. The existing Bible SharedSuite header is documented as C++-oriented C-shaped ABI, not directly C-source-compatible.

Earlier source findings remain in the linked records: ten-file memory/MFR review and three helper inspections; PF handle/register suite-version macro nuances; conditional threading statements; sample/comment discrepancies; 19-file registration/PiPL review and MenuTool partial-initialization limits. No original evidence has been rewritten into a host PASS.

This work remains within the agreed subject matter of [the completion plan](COMPLETION-PLAN.md). Safe-tooling Gate 2 is now closed by portable regression evidence; stages 3–4, the reuse audit, native compiler expansion and AE host gates remain open. **Native readout-adapter development remains paused; the deliverable is the Bible, not a separate testing product.** No new user AE run is requested.

**The scripting/panels communication → macOS/Windows build → distribution and testing/release-evidence blocks are written. Cross-checking reconciled the CEP command schema, corrected the render-queue enum recipe, strengthened the native generic-bridge ABI checks, and Gates 2–3 are closed with CI evidence. Gate 3A reuse audit is closed with an independent FSTR portable rerun. Gate 4 portable tooling now enforces inventory schema, parser diagnostics, required SDK 25.6 tables/functions, exact SuiteHandler generations, compiler-report identity and macOS/Windows runner syntax. Gate 4 remains open until the current revision is rerun against the licensed SDK 25.6 and MSVC/Windows evidence exists**, while preserving the exact-SDK baseline. This writing order does not close earlier acceptance gates; their criteria remain in [COMPLETION-CHECKLIST.md](COMPLETION-CHECKLIST.md). SDK headers, binaries and complete Adobe sample sources are not published in this repository.

## Earlier baseline evidence

- Native translation units and foundation headers passed strict syntax/type checks against a locally installed Adobe SDK 25.6 in the previously recorded baseline.
- Python tests cover incomplete parsing, missing inputs, ignored comments, conflicting tables and function-field reordering.
- Foundation tests cover resource release, moves, acquisition failure, undo balance and callback exceptions.
- MASTER, checksum manifest and MkDocs staging are generated by `scripts/build_docs.py`; CI validates generated documentation and builds the site.
- The header indexer fails closed on unsupported declarations. Full real SDK indexing remains **incomplete**, not a successful SDK validation. The streams/keyframes revision corrected a documentation-version leak: `StreamSuite7` belongs to a later SDK note, while supplied 25.6 exposes `StreamSuite6`. The masks/text/footage revision similarly corrected the earlier `CompSuite13` baseline to supplied 25.6 `CompSuite12`.

## Verification boundaries

Source review is not compilation. Authored Markdown fragments illustrate isolated operations or design patterns; target-platform compilation, linking and host execution of new snippets are NOT RUN. Syntax compilation does not establish PiPL correctness, host loading, pixels, operation semantics or MFR safety. No native reference binary in this edition is labelled host-verified. Windows compilation and reference-example AE host tests remain pending.

Previously collected native-effect research remains separately scoped in the [evidence audit](21-BUILTIN-EFFECTS-REVERSE-ENGINEERING/3D-Channel/3D-Channel-Extract/EVIDENCE-AUDIT-2026-09-30.md); it is not full-effect acceptance.

See [verification commands and results](VERIFICATION.md) and [coverage matrix](FINAL-COVERAGE-AUDIT.md). Six families have reproducible exact-SDK sample workspaces; none is called host-verified until the full cycle is recorded.
