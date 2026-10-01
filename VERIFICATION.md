# Verification — v1.1

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
4. Recipes: disposable project operations, undo, stream/keyframe ownership and render receipt cleanup. Correct and test the queue-status argument noted above; a syntax-only check is insufficient.
5. Record AE build, SDK, OS/architecture, sample base and actual observed result before upgrading a status to host-verified.
