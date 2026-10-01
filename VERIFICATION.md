## Gate 3 post-close consistency correction — 3D Channel Extract (2026-10-01)

A follow-up consistency scan after the recorded Gate 3 closure found two stale planning statements, not new runtime evidence. The master effect list still defaulted every entry to TO VERIFY, and the execution plan still placed 3D Channel Extract under the original HOST-BUILTIN-first pilot wording.

Both were reconciled with the already-retained binary evidence: macOS AE 25.6 contains the physical `Aux_Channel_Extract.plugin` module, so the current pilot classification is SHIPPED-PLUGIN. The earlier absent/HOST-BUILTIN interpretation remains preserved only as a superseded historical hypothesis. FLT evidence remains host-dispatch/subsystem evidence.

**Verification level: documentation consistency correction using existing evidence.** No new AE execution, binary capture or algorithm acceptance was performed.

# Verification — v1.1

## Testing, recipes and templates editorial review (2026-10-01)

Expanded the complete 10-TESTING section and added [Evidence and acceptance](10-TESTING/06-EVIDENCE-AND-ACCEPTANCE.md). The matrix now distinguishes PR/nightly/pre-release lanes; render correctness covers exact/tolerance comparisons, alpha, ROI/origins and golden-update policy; MFR stress now has state-bleed, repeatability, hang and memory evidence; performance requires fixed baselines; crash diagnostics now ties exact symbols to artifact identity.

The practical recipes and templates were aligned to the same evidence vocabulary. During that cross-check one concrete documentation/template mismatch was found and corrected: the CEP bridge chapter standardized the request field as `protocol`, while the working template still used `version`. The CEP README, panel JavaScript and host dispatcher now use the same `protocol` field. ScriptUI/JSX example status wording was also corrected so source that is intended to run is not mislabeled as host-verified.

The regeneration workflow was hardened after several simultaneous documentation pushes produced non-fast-forward failures in the generated-doc commit step. The workflow now serializes main-branch regeneration and retries from the latest main before generating/pushing MASTER and MANIFEST.

**Verification level: documentation/template review.** No new AE host execution, native SDK compile, render, installer, signing or performance run was performed by this pass. The CEP/JSX/ScriptUI changes are source-level alignment until an actual host result is recorded.


## Scripting, panels and platform distribution chapter review (2026-10-01)

Expanded the ExtendScript object model and ScriptUI chapters, CEP/UXP panel guidance, Script/CEP/native communication chapters, macOS and Windows build/sign/package/CI chapters, and the distribution compatibility/security/release checklist. The [dated source-review record](11-DISTRIBUTION/05-PLATFORM-SOURCE-REVIEW-2026-10-01.md) lists the public Adobe CEP/SDK, Adobe UXP-transition, Apple Developer ID/notarization and Microsoft SignTool sources used for this pass.

The review records the CEP two-engine boundary and host-main-thread evalScript/event scheduling; treats the November 2026 AE UXP beta as a future dated milestone rather than an available API; distinguishes development plug-in paths from installer policy; preserves Windows PiPL resource-generation and architecture declarations; separates macOS ad-hoc development signing from Developer ID/notarized release distribution; and expands Authenticode, installer ownership, upgrade, provenance, symbol and release-evidence rules.

**Verification level: public-source review and documentation.** No new exact-SDK compilation, native link, CEP host run, UXP host run, Developer ID signature, notarization submission, Authenticode signature, installer run, clean-machine load or Windows x64/ARM64 host test was performed. Existing completion gates are unchanged by this editorial work.


## GPU, audio and Custom UI / Drawbot chapter review (2026-10-01)

Expanded [GPU effects](02-EFFECT-PLUGINS/05-GPU.md), [Audio effects](02-EFFECT-PLUGINS/07-AUDIO.md), added [Custom UI / Drawbot](02-EFFECT-PLUGINS/09-CUSTOM-UI-DRAWBOT.md), and aligned the Effect capability map to the supplied SDK 25.6 build 61. The [source-review record](18-SDK-HEADER-TOOLS/15-GPU-AUDIO-CUSTOM-UI-SDK25.6.md) records relevant header/sample hashes and line ranges.

GPU review distinguishes global capability from per-frame GPU_RENDER_POSSIBLE, per-device setup/setdown state, GPU framework/device identity, GPUDeviceSuite allocation/world ownership and the bundled SDK_Invert_ProcAmp lifecycle. Source presence is not treated as proof every CUDA/OpenCL/DirectX/Metal branch is buildable or available on every target.

Audio review records AUDIO_SETUP/RENDER/SETDOWN, audio capability flags, PF_SoundWorld, sample formats and checkout/checkin. A source search of the supplied Examples tree found no bundled C/C++ effect implementation dispatching PF_Cmd_AUDIO_RENDER; therefore the chapter does not invent a sample-backed DSP lifecycle or scheduling guarantee.

Custom UI review records PF_Cmd_EVENT, event contexts, PF_CustomUIInfo, PF_EffectCustomUISuite, Drawbot supplier/surface borrowed ownership versus created-object ReleaseObject, Custom_ECW_UI/CCU patterns and the documented async-manager requirement for rendered UI frames after the UI/render-thread split.

**Verification level: SDK source review and documentation.** No new GPU binary, device setup/render, CPU↔GPU comparison, audio processing host run, custom UI interaction, async-manager lifecycle, Drawbot leak test, HiDPI/theme test or Windows host run was performed. Gate 4/6/7 remain open.

## PICA providers, Effect↔AEGP and legacy-boundary chapter review (2026-10-01)

Expanded [PICA suites](14-NATIVE-INTEGRATIONS/03-PICA-SUITES.md), [AEGP → Effect](15-COMMUNICATION/03-AEGP-TO-EFFECT.md), [Plug-in → Plug-in PICA](15-COMMUNICATION/04-PLUGIN-TO-PLUGIN-PICA.md), [legacy/native boundaries](14-NATIVE-INTEGRATIONS/11-LEGACY-NATIVE.md) and the two existing bridge-template READMEs from the supplied SDK 25.6 build 61. The [source-review record](18-SDK-HEADER-TOOLS/14-PICA-BRIDGES-LEGACY-SDK25.6.md) records 13 SDK/source hashes and exact ranges.

Reviewed contracts include SPBasic public-version acquire/release reference counting; SPSuites public/internal version separation and AddSuite publication; Sweetie’s static DuckSuite provider; Checkout’s optional acquire/use/release consumer; current EffectSuite4 generic-call command/time arguments; PF_Cmd_COMPLETELY_GENERAL dispatch; and the old ProjDumper/Shifter workflow. The review also records that bundled Commando’s initializer signature differs from the current AEGP_PluginInitFuncPrototype and therefore must not be copied as the 25.6 reference signature.

Source limits are explicit: Sweetie does not demonstrate generic suite unpublish/hot replacement; suite refcount does not prove thread safety; the current Bible SharedSuite header is C++-oriented despite its C-shaped ABI; old bundled sample suite generations remain pattern evidence rather than current signatures.

**Verification level: SDK source review and documentation.** The SDK TAR SHA-256 was recalculated and matched the accepted archive. No new provider/consumer host load, wrong-version acquisition run, suite unload/reload test, generic call, layer-time host test, concurrency stress, exact-SDK compile of the Bible bridge templates or Windows host run was performed. Gate 4/6/7 remain open.

## Native panels and BlitHook chapter review (2026-10-01)

Rewrote [native dockable panels](14-NATIVE-INTEGRATIONS/07-NATIVE-PANELS.md) and [BlitHook](14-NATIVE-INTEGRATIONS/10-BLITHOOK.md) from the supplied SDK 25.6 build 61. The [source-review record](18-SDK-HEADER-TOOLS/13-PANELS-BLITHOOK-SDK25.6.md) records ten source hashes and the reviewed Panelator/EMP contracts.

Panel review establishes `AEGP_PanelSuite1`, non-localized UTF-8 match-name identity, CreatePanelHook/per-panel refcon/function-table separation, NSView*/HWND platform containers, snap/flyout callbacks, title/visibility state and explicit UnRegisterCreatePanelHook. Panelator remains a useful Window-menu/platform UI skeleton but its reviewed source does not show a complete global teardown/unregister path; this is source evidence only, not a measured leak.

BlitHook review separates the `AEGeneral` PiPL/plugin entry contract from AEGP. `AE_Hook.h` protocol 3.0 describes 32/64/128-bit AE_PixBuffer metadata, ARGB/BGRA format, non-tight row bytes, view origin/visible rectangle, nullable blank frame and receipt/completion/async fields. Bundled EMP does not process pixels or exercise asynchronous completion, so the Bible does not invent pixel-pointer lifetime or async timing beyond the header.

**Verification level: SDK source review and documentation.** No new native panel binary, dock/reopen/workspace/shutdown run, BlitHook display callback, async completion test, preview-latency benchmark or macOS/Windows host matrix was performed. Gate 6/7 remain open.
## AEIO and Artisan chapter review (2026-10-01)

Rewrote [AEIO](04-AEIO/README.md), [AEIO native integration](14-NATIVE-INTEGRATIONS/08-AEIO.md), [Artisan](05-ARTISAN/README.md) and [Artisan native integration](14-NATIVE-INTEGRATIONS/09-ARTISAN.md) from the supplied SDK 25.6 build 61. The [source-review record](18-SDK-HEADER-TOOLS/12-AEIO-ARTISAN-SDK25.6.md) records nine source hashes and exact header/sample ranges.

AEIO review distinguishes the frozen 49-slot `AEIO_FunctionBlock4` from current host suites `AEGP_IOInSuite7`/`AEGP_IOOutSuite6`; ModuleInfo capability flags from actual callback behavior; options flatten/inflate and MemorySuite lifetimes; sparse-region drawing; importer-side auxiliary-channel producer callbacks; output Start/Add/End state; audio; ICC/CICP metadata; and semantic `AEIO_Err_USE_DFLT_CALLBACK`. The bundled IO/FBIO examples remain fake-format skeletons, not codec correctness evidence.

Artisan review records PR API 1.0, `PR_ArtisanEntryPoints` global/instance/frame/query lifecycle, plugin-owned private data, registration and match-name identity, current `AEGP_CanvasSuite8`/`ArtisanUtilSuite1`, texture/world/render-receipt cleanup families and the relation between render context and scene evaluation. Bundled Artie uses older Canvas/Layer/Item/Stream suite generations and is treated as renderer-flow evidence, not current-signature or production-quality renderer evidence.

Source caveats are preserved rather than silently fixed: IO's legacy comment about not freeing a replaced old InSpec options handle during sync; Artie's mostly-empty global/instance/frame/query lifecycle callbacks; Artie's old suite generations and helper that does not handle text-layer source dimensions; Artie registration sets both artisan version major/minor from `Artie_MAJOR_VERSION`. None is promoted to a measured AE defect without host reproduction.

**Verification level: SDK source review and documentation.** No new exact-SDK compile, AEIO registration/import/export run, decoder/encoder output comparison, aux-channel import test, Artisan registration/selectability/render, interactive viewport test, persistence test, leak/cancel/error injection run or Windows host test was performed. Gate 6/7 remain open.
## Masks, text/markers and footage/import chapter review (2026-10-01)

Rewrote [Masks](17-NATIVE-SUITE-COOKBOOK/07-MASKS.md), [Text + markers](17-NATIVE-SUITE-COOKBOOK/08-TEXT-MARKERS.md) and [Footage / import](17-NATIVE-SUITE-COOKBOOK/09-FOOTAGE-IMPORT.md) against the supplied SDK 25.6 build 61. The [source-review record](18-SDK-HEADER-TOOLS/11-MASK-TEXT-FOOTAGE-SDK25.6.md) records six SDK/source hashes, current suite generations, sample ranges and ownership findings.

The review corrects later-SDK leakage from the previous Cookbook: mask/text chapters now use `StreamSuite6`, and the footage baseline uses `CompSuite12` rather than later `CompSuite13`. Current reviewed families include MaskSuite6/MaskOutlineSuite3, TextDocumentSuite1, MarkerSuite3 and FootageSuite5.

Reviewed contracts include MaskRef disposal even after deleting a mask; outline StreamValue lifetime; closed-mask vertex/tangent semantics and variable feather points; UTF-16 TextDocument MemHandle ownership and character counts; marker strings/cue-point handles, duration/flags/labels and the distinction between standalone marker allocation and a marker carried by StreamValue; FootageH caller ownership before adoption, project ownership after Add/Proxy/Replace, path MemHandle cleanup, sequence/layer keys, interpretation enum and proxy/placeholder/solid workflows.

Official samples remain pattern evidence, not production ownership proof. `Projector` creates a mask in the reviewed function without an explicit DisposeMask even though the current header gives MaskRef a dispose contract; this is a source-level finding, not a measured host leak. `Projector`/`ProjDumper` pass `FALSE` where FootageSuite5 declares `AEGP_InterpretationStyle`; numerically that selects `NO_DIALOG_GUESS=0`, but new code should use the enum. Reviewed import sample error paths do not constitute complete RAII rollback proof for every NewFootage/adoption failure.

**Verification level: SDK source review and documentation.** No new exact-SDK compilation, linked native binary, mask/text/marker mutation, actual footage import/proxy/relink, leak test, failure rollback run or Windows host verification was performed. Any green documentation CI for the resulting commit remains documentation/portable evidence only.
## Streams/properties and keyframes chapter review (2026-10-01)

Expanded [Streams / properties / expressions](17-NATIVE-SUITE-COOKBOOK/05-STREAMS-PROPERTIES.md) and [Keyframes](17-NATIVE-SUITE-COOKBOOK/06-KEYFRAMES.md) from the supplied SDK 25.6 build 61. The [source-review record](18-SDK-HEADER-TOOLS/10-STREAMS-KEYFRAMES-SDK25.6.md) records seven SDK file hashes, exact header/sample ranges and the reviewed Cookbook recipe blobs.

The review corrected a version-mixing error in the previous Cookbook: supplied SDK 25.6 exposes `AEGP_StreamSuite6`, `AEGP_DynamicStreamSuite4` and `AEGP_KeyframeSuite5`; a later `StreamSuite7` note is not the 25.6 baseline. It also records that suite struct suffixes are not numeric AcquireSuite versions (`StreamSuite6` uses version macro 11).

Reviewed contracts include owned StreamRef and StreamValue lifetimes, expression MemHandle cleanup, effect parameter index 0 as the input layer, pre/post-expression sampling, expression-aware time-varying status, dynamic group/match-name operations, delete/reorder ownership, separated leader/follower behavior, keyframe count/time/value ownership, interpolation/ease/tangents/flags, batch-add transactions and Suite5 label metadata.

`Easy_Cheese` and `Streamie` remain useful Adobe samples but use older suite generations (`StreamSuite2`, `KeyframeSuite3`, `DynamicStreamSuite2`). The documentation now treats them as pattern evidence rather than current-signature evidence. A concrete compatibility example is `GetStreamName`: the current StreamSuite6 returns a UTF-16 MemorySuite handle, while the old Streamie call shape used a character buffer.

The existing `EffectStreamRecipes.cpp` and `KeyframeRecipes.cpp` were reviewed but not edited. Their source blobs remain `8b473f10c872aec992eb728c91444b629041c0a1` and `19d798ddd0aba617cf98a41ebd6271ddd1315624`. The static OneD recipe is intentionally more conservative than the raw `SetStreamValue` header rule because it refuses expression-driven time-varying streams. The keyframe recipe requires callers to provide a stream on which index-based keyframe APIs are legal; separated leaders need follower resolution first.

**Verification level: SDK source review and documentation.** No new exact-SDK compile, loaded AEGP binary, expression/keyframe host mutation, separated-dimension test, save/reopen test, undo test or Windows host run was performed. Green documentation CI, when recorded for the resulting commit, does not upgrade these chapters to host-verified.
## AEGP project and render automation chapter review (2026-10-01)

Expanded [AEGP project and render automation](03-AEGP/02-PROJECT-RENDER-AUTOMATION.md) from the supplied SDK 25.6 build 61. The [fifth source-review record](18-SDK-HEADER-TOOLS/09-AEGP-PROJECT-RENDER-SDK25.6.md) records six SDK file hashes, reviewed ranges and three existing cookbook Git blobs. The source TAR SHA-256 was recalculated and matched the previously accepted archive.

The chapter distinguishes project/item/comp/layer handles, temporal spaces, owned strings, dangerous New/Open operations, Undo grouping versus rollback, queue versus item status, ref invalidation, output configuration, render options, borrowed receipt worlds, sync/async lifetime and cache submission. QueueBert and Projector excerpts are treated as historical sample code, not automatically safe or executed workflows. The frame/cache explanations do not claim a new independent AE renderer.

A concrete source finding remains OPEN: `RenderQueueRecipes.cpp` passes TRUE to `AEGP_SetRenderState`, whose RQItemSuite3 argument is an enum. With TRUE=1 this requests UNQUEUED rather than QUEUED=2. Exact declarations and the matching sample occurrence are recorded. The recipe README now withdraws its earlier “enable render” description; the native source is unchanged. Fixing and testing that behavior is still required even when documentation CI passes.

The previously prepared registration STATUS/VERIFICATION patch was actually written to main through `a5080a132d299b8ef20888e814f3c0513365710c` and `4cd4515e605783f9255edb59cf734d0cabe0f1fd`. No SDK files or raw user project evidence were published with these documentation updates.

**Verification level: source review and documentation.** No new exact-SDK compile, linked native binary, project mutation, undo/rollback test, queue execution, image export, cancellation, async shutdown or MFR test was performed. GitHub Validate and documentation-regeneration results belong to their actual committed revisions. Source hash checks and successful Markdown generation are not native-effect acceptance. The next editorial topic is streams/keyframes; general plan gates are not closed by this writing milestone.

## Registration/PiPL and AEGP lifecycle chapter review (2026-10-01)

Expanded [registration, PiPL and loading](01-ARCHITECTURE/03-PIPL-AND-LOADING.md) and [AEGP hooks and suites](03-AEGP/01-HOOKS-SUITES.md). The [fourth source-review record](18-SDK-HEADER-TOOLS/08-REGISTRATION-AEGP-SDK25.6.md) identifies 19 files from SDK 25.6 build 61, exact ranges and the unchanged Bible MenuTool source. The chapters, review record and AEGP reading route are present by commit `859b9c6c816a7cb5a360f61869d1bcf1531aede3`; this status reconciliation does not create a new native implementation.

The recorded review distinguishes Effect registration, EffectMain and AEGP initialization; resource Kind, exports and architecture entries; independent version fields; PiPL/global outflags and the documented override exception; Windows/macOS resource build descriptions; suite acquisition, hook refcons and command/update/idle/death lifetimes. The historical source observations include RegisterSuite5's version macro evaluating to 6, the wrong decimal comment beside Skeleton's PiPL outflags and unequal Reserved Info values whose runtime priority remains unestablished.

MenuTool's later initialization errors deliberately retain state after hook registration and may return A_Err_NONE with the command disabled. That is not complete functional success. The source review also records discarded DisableCommand/ReportInfo errors and absent UI-suppression handling. The implementation was not silently changed; partial-initialization, exception and shutdown paths still require actual host verification.

**Verification level: existing SDK-source review and documentation.** No new exact-SDK compiler run, resource compilation, linking, loaded-module test, MenuTool execution, installer test or failure-injection run is established by this editorial update. Runtime compatibility and the full plan gates remain open. Any CI result must be tied to its actual commit/run; this paragraph is not itself an assertion that a new CI run passed.

## Memory/lifetime and MFR chapter review (2026-10-01)

Expanded [memory, resource lifetime and errors](01-ARCHITECTURE/02-MEMORY-THREADING-ERRORS.md) and [MFR/thread safety](02-EFFECT-PLUGINS/04-MFR-THREAD-SAFETY.md) from the supplied SDK 25.6 build 61. The [third source-review record](18-SDK-HEADER-TOOLS/07-MEMORY-MFR-SDK25.6.md) identifies ten source files by SHA-256 and records exact declaration/comment/sample ranges.

Reviewed contracts include PF versus AEGP memory families, borrowed versus owned worlds, suite references, host-managed sequence handle locks, the two flatten selectors, pre-render deletion, auxiliary versus SmartFX checkin, error-preserving cleanup, read-only MFR sequence access, mutable per-render-thread copies, and Compute Cache key/value/receipt lifetime. The non-waiting compute option is explicitly distinguished from cached-only lookup.

Source discrepancies are retained: general versus conditional sequence-setup threading descriptions, PF_HandleSuite1's version macro evaluating to 2, the bool error variables in a schematic Compute Cache comment, and PathMaster's cross-platform warning. Architectural recommendations are labelled separately from SDK guarantees.

Also reviewed the existing PicaSuiteRef, AegpOwners and HostCallbackGuard at snapshot `fcfb0e32c14916b55c2bcdbe414d3d1b3f524eeb`. Their borrowed suite dependencies, discarded cleanup errors and scope limits are documented; their implementation is unchanged. This is not the cross-project reuse audit required by stage 3A.

**Verification level: source review and documentation only.** The source TAR hash was recomputed and matched the previously recorded value. No new native implementation, exact-SDK compiler run, loaded binary, leak test, MFR stress, GPU comparison or AE render was performed. Existing portable regression and strict documentation results must be read from the committed revision's Validate run, not inferred from this paragraph. Full plan gates remain open as recorded in COMPLETION-CHECKLIST.

## Parameter/UI and color/pixel chapter review (2026-09-30)

Expanded [parameters and UI](02-EFFECT-PLUGINS/02-PARAMETERS-UI.md) and [pixels, color and alpha](02-EFFECT-PLUGINS/06-COLOR-PIXELS.md) from the supplied SDK 25.6 build 61. The [second source-review record](18-SDK-HEADER-TOOLS/06-PARAMETERS-PIXELS-SDK25.6.md) records hashes for 15 source files, exact declaration/sample line ranges and unresolved source discrepancies.

Reviewed contracts include non-animatable versus non-interpolated parameters; setup macro clearing; USER_CHANGED_PARAM versus UPDATE_PARAMS_UI; UI-only/disabled/hidden states; Point/default units; ARGB32/64/128; the 0..32768 integer 16-bpc range; typed pixel access; rowbytes/origin; alpha-conversion signatures; floating color parameters in the effect working space; and possible multithreading of iterate callbacks.

Source discrepancies are retained explicitly: two numeric typos beside 16-bit constants, Paramarama enum/setup ordering, Supervisor popup changes beyond the documented PF_UpdateParamUI field list, and differing macro initialization behavior. No SDK source was edited to hide them. They are source observations, not newly reproduced host defects.

**Verification level: documentation and SDK source review, not new native compilation.** Authored C++ fragments illustrate setup, UI flags and floating color lookup; they are not linked or host-tested plug-ins. Numeric normalization/alpha examples are mathematical explanations, not native-effect measurements. The TAR identity was rechecked against the previous recorded SHA-256; the prior compressed/decompressed byte comparison is not claimed as a new successful run.

GitHub Validate remains responsible for the documentation build and existing portable regressions on the committed revision. It does not compile these Markdown fragments against the licensed SDK. Native readout development remains paused; no new user AE run, map installation, output conversion experiment or GPU/MFR comparison was performed. Plan gates 2, 3A and 4–9 are not silently closed by editorial work.

## First supplied-SDK chapter review (2026-09-30)

The user supplied `ae25.6_61.64bit.AfterEffectsSDK`. In the first review, the uploaded Zstandard stream was decompressed and compared byte-for-byte with the separately uploaded TAR; they matched. Source hashes and exact file/line references are recorded in [the supplied-SDK review](18-SDK-HEADER-TOOLS/05-SUPPLIED-SDK-25.6.md).

That iteration expanded Effect anatomy and SmartFX and added an auxiliary-channel chapter. It checked declarations, ownership rules and relevant Skeleton/SmartyPants source behavior. In particular, auxiliary-channel checkin and SmartFX world checkin have different documented contracts.

**Scope: SDK source review and documentation.** No new native reader, compiled plug-in, AE render, importer qualification or concurrency run was claimed. The historical compiler baseline below was not repeated and is not automatically attributed to the new upload. GitHub documentation validation is separate from native compilation and host execution.

## Recorded baseline (2026-09-30)

- Adobe After Effects SDK **25.6 build 61**, locally supplied; proprietary headers are not redistributed.
- macOS arm64, Apple Clang, C++17: **13 translation-unit checks passed**.
- Python: **7 tests passed**.
- Foundation: strict C++17 build and behavioral assertions passed against synthetic stubs.
- Full SDK index: 70 headers, 230 recognized tables, 3537 parsed functions. **Incomplete**: unsupported declarations produce diagnostics and a nonzero exit code. These counts are exploratory, not coverage claims.
- Native linking, PiPL packaging, AE loading/rendering, MFR stress and Windows compilation: **not verified**.

The 13 recorded translation-unit checks include two forwarding entry files and a foundation-header probe. These historical results are not repeated by the editorial reviews above.

`scripts/materialize_sdk_examples.py` provides exact local sample shells for all six gaps. `scripts/host_cycle.py` installs a built bundle and optionally invokes `aerender`, but intentionally reports UI load/unload and MFR stress as pending.

## Reproduce portable checks

```bash
python3 -m unittest discover -s 18-SDK-HEADER-TOOLS/tests -v
mkdir -p .build
c++ -std=c++17 -Wall -Wextra -Werror \
  -I19-NATIVE-CODE-FOUNDATION/tests/stubs \
  -I19-NATIVE-CODE-FOUNDATION/code \
  19-NATIVE-CODE-FOUNDATION/tests/test_foundation.cpp -o .build/foundation-test
.build/foundation-test
python3 -m pip install -r requirements-docs.txt
python3 scripts/build_docs.py --check
python3 scripts/build_docs.py
mkdocs build --strict
```

## Check with the actual SDK (macOS / Clang)

```bash
python3 scripts/check_native.py "/path/to/Adobe-SDK/Examples"
```

This is a **syntax/type** check. It deliberately does not call it a plugin build. Keep Adobe sample utilities, PiPL resources, exported entry points and platform settings when integrating. Compile canonical sources or section-20 forwarding files, never both into the same binary. Copy the foundation headers alongside MenuTool or adjust its relative include.

## Required next host checks

1. Minimal Gain: load, parameter UI, gain 0/1/4, 8/16-bpc and transparent pixels.
2. SmartFX Copy: compare input/output at 8/16/32-bpc, partial/empty ROI, odd sizes, nonzero origins and cancellation. Keep MFR off in the delivery build until concurrent-frame tests pass; use a separately identified enabled test build for those tests.
3. MenuTool: successful command execution, menu updates, failed initialization and shutdown.
4. Recipes: disposable project operations, undo, stream/keyframe ownership and render receipt cleanup. The render-queue Boolean/enum source defect is corrected to named `QUEUED` plus readback; actual queue behavior remains host-test-required.
5. Record AE build, SDK, OS/architecture, sample base and actual observed result before upgrading a status to host-verified.


## Scripting/panels communication and platform distribution review (2026-10-01)

Expanded the production bridge guidance in [CEP panel <-> ExtendScript](15-COMMUNICATION/06-CEP-TO-EXTENDSCRIPT.md) and [Native <-> script/panel](15-COMMUNICATION/07-NATIVE-TO-SCRIPT-PANEL.md). The bridge now has an explicit versioned request/response envelope, centralized dispatcher, undo ownership, batching guidance, stale-response handling, cancellation limits, large-payload transport boundaries, state ownership, IPC versioning, failure behavior and security checks.

Added end-to-end release-flow chapters for [macOS](08-MACOS/09-PRODUCTION-BUILD-PIPELINE.md) and [Windows](09-WINDOWS/09-PRODUCTION-BUILD-PIPELINE.md). They connect clean checkout, pinned toolchains, architecture/resource checks, signing, packaging, clean-machine installation, AE load tests, symbols and artifact manifests without changing the verification level of existing examples.

Added [release artifacts, installers and update strategy](11-DISTRIBUTION/05-RELEASE-ARTIFACTS-UPDATES.md), covering release-set identity, installer ownership, upgrade/rollback, staged auto-update, download integrity and compatibility/support metadata.

**Verification level: documentation/architecture review only.** No new CEP panel was executed in AE, no ExtendScript dispatcher was host-tested, no macOS release binary was signed/notarized in this update, no Windows binary was Authenticode-signed, no installer was built, and no clean-machine AE load cycle was performed. These chapters define the required production process; they do not close completion-plan host/build gates.


## Host-verification and release-evidence guidance (2026-10-01)

Added [After Effects host verification](10-TESTING/06-HOST-VERIFICATION.md), [test evidence and acceptance records](10-TESTING/07-TEST-EVIDENCE.md), and [clean-machine release acceptance](10-TESTING/08-CLEAN-MACHINE-ACCEPTANCE.md). The chapters establish a strict evidence ladder from documented/compiled/linked through load-, behavior-, stress- and release-verified states, require exact artifact/environment identity, define PASS/FAIL/BLOCKED/NOT RUN semantics, and make package-level clean-machine installation the final release boundary.

These chapters deliberately prevent compiler checks, screenshots, manual developer-folder installs or one-platform results from being promoted into broader compatibility claims.

**Verification level: documentation/process definition only.** No new AE host run, release-candidate install, upgrade/uninstall, signing/notarization, Authenticode verification, MFR stress or cross-platform execution was performed by this editorial update. Existing completion-plan gates remain open until the named evidence is actually collected.


## Safe tooling Gate 2 verification (2026-10-01)

`scripts/host_cycle.py` was changed from destructive replace-and-report behavior to a fail-closed transaction:

- source/destination collision is rejected;
- an existing installed plug-in is moved to a temporary backup before replacement;
- copy/install failure restores the previous installation;
- render failure, timeout or missing expected output rolls the installation back;
- non-zero `aerender` exit is a command failure;
- render timeout is explicit and reported;
- machine-readable output separates build/install/load/render/MFR states.

`scripts/materialize_sdk_examples.py` now validates the complete requested materialization plan before mutation, rejects source/destination overlap, checks expected sample source identity, stages copies transactionally and preserves the licensed source tree.

Portable regression coverage lives in `scripts/test_safe_tools.py`. It covers successful replacement, forced install-copy failure and restoration, non-zero render, timeout, missing output, path collision, materializer overlap, source preservation and partial-sample rejection.

**Evidence:** GitHub Actions Validate run `36839553520` on commit `22095cd86a7460f241215f5252de65327824a892` completed successfully. The safe-tool step, SDK-header parser tests, C++ foundation test, generated-documentation check and `mkdocs build --strict` all passed.

This closes Completion Gate 2 only. It does not establish AE host loading, render correctness, signing, installer acceptance or Windows native compilation.


## Gate 3A reuse-audit verification (2026-10-01)

The code-level audit is recorded in [22-PROJECT-CASE-STUDIES/REUSE-AUDIT-2026-10-01.md](22-PROJECT-CASE-STUDIES/REUSE-AUDIT-2026-10-01.md).

FSTR Line was independently rerun from the pinned snapshot `c69e3663de59dc44cbdef18042891f6dd1ce5ee6` using audit branch `audit/bible-reuse-2026-10-01`. Audit commit `165bfac15ef9401ba8f2aaec747d2a6bc487a0b1` differs from the pinned snapshot by exactly one added workflow file. GitHub Actions run `36841872858` passed locked dependency installation, `npm run check`, `npm run check:cep` and `git diff --check`.

AE Hot Loader retained CI evidence was reviewed, including successful macOS PoC runs `36309949069` and `36337979733`, plus earlier failed run `36308472947` whose Static checks failed and whose later steps were skipped. The audit preserves that failure.

Transfer decisions are explicit: FSTR snapshot/guard/coalescing/fake-host patterns are adapted conceptually; the FSTR command-hook probe remains evidence-only; AE Hot Loader request-correlation ideas may inform bridge design; its private `ML::LoadPlugins` path remains research-only and its destructive installer pattern is explicitly rejected.

**Gate 3A is closed.** None of these results are Bible AE host verification.
