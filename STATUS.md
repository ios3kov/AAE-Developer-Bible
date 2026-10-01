# Status

**v1.1 — verified SDK syntax baseline and reproducible documentation**

Updated: **2026-10-01**. Previously recorded native compilation baseline: **Adobe SDK 25.6, macOS arm64, C++17**. Historical compiler results are separate from the editorial/source-review milestones below.

## Current work — writing the Bible from the supplied SDK

The supplied `ae25.6_61.64bit.AfterEffectsSDK` is the basis of five source-review records:

1. [Effect anatomy, SmartFX and auxiliary channels](18-SDK-HEADER-TOOLS/05-SUPPLIED-SDK-25.6.md).
2. [Parameters and pixels](18-SDK-HEADER-TOOLS/06-PARAMETERS-PIXELS-SDK25.6.md).
3. [Memory, lifetime and MFR](18-SDK-HEADER-TOOLS/07-MEMORY-MFR-SDK25.6.md).
4. [Registration, PiPL and AEGP lifecycle](18-SDK-HEADER-TOOLS/08-REGISTRATION-AEGP-SDK25.6.md).
5. [AEGP project and render automation](18-SDK-HEADER-TOOLS/09-AEGP-PROJECT-RENDER-SDK25.6.md).
6. [Streams and keyframes](18-SDK-HEADER-TOOLS/10-STREAMS-KEYFRAMES-SDK25.6.md).
7. [Masks, text/markers and footage/import](18-SDK-HEADER-TOOLS/11-MASK-TEXT-FOOTAGE-SDK25.6.md).

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
- [Registration, PiPL and loading](01-ARCHITECTURE/03-PIPL-AND-LOADING.md): separate registration/dispatcher/initializer contracts, resource Kind, symbols, architectures, version domains, outflags and platform resource pipelines.
- [AEGP lifecycle, hooks and suites](03-AEGP/01-HOOKS-SUITES.md): IDs/refcons, suite macros, callbacks and partial initialization; the existing MenuTool is reviewed, not changed or host-verified.
- [AEGP project and render automation](03-AEGP/02-PROJECT-RENDER-AUTOMATION.md): project graph and time, Undo versus rollback, queue states and invalidation, output settings, frame receipts, borrowed worlds, sync/async cancellation and cache boundaries.
- AEGP navigation, recipe warnings and VERIFICATION distinguish source review from compiler/host evidence.

## Latest synchronization and findings

The previously pending STATUS/VERIFICATION registration update was written to main in commits `a5080a132d299b8ef20888e814f3c0513365710c` and `4cd4515e605783f9255edb59cf734d0cabe0f1fd`. It reconciles chapters already present by `859b9c6c816a7cb5a360f61869d1bcf1531aede3`; it is no longer only an unapplied ZIP patch.

The fifth review records six SDK file hashes and reviews three existing cookbook recipes. It identifies a concrete open source finding: `RenderQueueRecipes.cpp` passes TRUE to an enum-status argument; with TRUE=1 that means UNQUEUED, not QUEUED=2. The chapter and [recipe README](17-NATIVE-SUITE-COOKBOOK/code/README.md) now warn about it. The C++ implementation is unchanged; a code correction and behavioral checks remain required. Documentation CI must not be used to close this finding.

Earlier source findings remain in the linked records: ten-file memory/MFR review and three helper inspections; PF handle/register suite-version macro nuances; conditional threading statements; sample/comment discrepancies; 19-file registration/PiPL review and MenuTool partial-initialization limits. No original evidence has been rewritten into a host PASS.

This is documentation and SDK source-review work within the agreed subject matter of [the completion plan](COMPLETION-PLAN.md). It does not complete stages 3–4 or bypass outstanding safety, reuse-audit, compiler and host gates. **Native readout-adapter development remains paused; the deliverable is the Bible, not a separate testing product.** No new user AE run is requested.

**Next editorial block: AEIO and Artisan**, against supplied headers and official samples. This writing order does not close earlier acceptance gates; their criteria remain in [COMPLETION-CHECKLIST.md](COMPLETION-CHECKLIST.md). SDK headers, binaries and complete Adobe sample sources are not published in this repository.

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
