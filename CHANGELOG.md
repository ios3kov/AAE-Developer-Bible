# Changelog

## Editorial progress — 2026-10-01

- Expanded the full testing section with explicit build/host/release evidence layers, richer matrices, render/ROI correctness, MFR stress, performance and crash diagnostics.
- Added an evidence/acceptance chapter with PASS/FAIL/BLOCKED/NOT_RUN vocabulary tied to exact artifact and environment identity.
- Expanded practical recipes and bug/compatibility/performance/spec/release templates.
- Reconciled the CEP working template with the communication protocol field and corrected ScriptUI/JSX verification wording.
- Serialized/retried generated-doc updates to prevent non-fast-forward failures during rapid documentation pushes.

- Expanded ExtendScript object-model and ScriptUI chapters with reference invalidation, stable targeting, command boundaries and long-operation rules.
- Expanded CEP communication into a versioned request/response protocol with main-thread scheduling, stale-response, path, large-data and security boundaries.
- Added a dated After Effects UXP migration plan based on Adobe's 2026-09-24 transition announcement without treating the future beta as a verified API.
- Expanded macOS Xcode/Universal/signing/notarization/install/CI chapters and Windows Visual Studio/x64-ARM64/AuthentiCode/install/CI chapters.
- Expanded distribution versioning, licensing/security, install-location policy and release acceptance checklist.
- Added a dated source-review record; no native build, signing, notarization, installer or host-test status was upgraded by this editorial pass.


## Unreleased — 2026-10-01

- Expanded CEP/ExtendScript and native/script-panel communication into versioned production bridge protocols with batching, undo, stale-response, failure, IPC and ownership guidance.
- Added end-to-end macOS and Windows production build pipeline chapters.
- Added release artifact identity, installer ownership, upgrade/rollback and staged update guidance.
- Updated STATUS and VERIFICATION without claiming new host/build verification.
- Added explicit host-verification evidence ladder, durable test-record format and clean-machine release acceptance chapters.

## v1.1 — 2026-09-30

- Fixed Minimal Gain registration macro, About callback context, selector spelling and suite includes.
- Implemented SmartFX host-copy pass-through; corrected checkout context/time fields; disabled unverified MFR capability.
- Added exception guards and error propagation to MenuTool; retained callback state safely after partial registration.
- Corrected cookbook suite generations and keyframe value ABI for SDK 25.6; added missing macro includes and cleanup error handling.
- Added real-SDK syntax/type driver; 13 checks pass on macOS arm64.
- Made symbol checks reject absent/empty inputs; added partial-parse diagnostics, bounded declaration parsing and field-order diffs.
- Added regression/ownership tests, docs CI, generated MASTER/manifest and explicit verification matrix.
- Replaced duplicated implementation files with canonical-source forwarding files.

## v0.4 — 2026-09-30

- Added `18-SDK-HEADER-TOOLS/`: exact native contract inventory generated from local SDK headers.
- Added recipe symbol verification and SDK inventory diff tooling.
- Added macOS and Windows validation launchers and platform-specific validation docs.
- Added `19-NATIVE-CODE-FOUNDATION/`: PICA suite lifetime helper, AEGP resource owners, undo scope, and host callback exception guard.
- Added unit tests for the inventory parser and C++17 stub compile test for foundation headers.
- Regenerated navigation and MASTER edition; preserved v0.3 as a separate release.

## v0.3 — 2026-09-30

- Added `17-NATIVE-SUITE-COOKBOOK/`.
- Added recipes for Project/Item, Composition, Layer, Effect, Stream/Dynamic Stream, Keyframe, Mask, Text/Marker, Footage, frame rendering, Render Queue, memory/undo/persistence, Guide/ItemView/selection.
- Added AEGP suite function capability index.
- Added C++ drop-ins: project traversal, comp/layer, effect/stream, keyframes, render frame, render queue.
- Added public SDK docs errata and header-first verification policy.
- Re-verified high-risk signatures; corrected frame-rate type for `AEGP_CreateComp`, mask calls, `AEGP_SetRenderState`, and `AEGP_LayerIDVal`.
- Added verification labels so examples distinguish published-contract verification from host execution.

## v0.2 — 2026-09-30

- Added complete native integration taxonomy: Effect, AEGP, Keyframer, native panel, AEIO, Artisan, Interactive Artisan, BlitHook, shared PICA suites and legacy paths.
- Added AE 26.5 AEGP suite catalog.
- Added communication architecture: AE↔Effect, AE↔AEGP, AEGP↔Effect, PICA suite bridge, scripting and CEP bridges, threading and ownership.
- Added working/drop-in templates for native effect, AEGP menu tool, generic bridge, shared suite ABI, native panel registration, keyframer batch pattern, AEIO/Artisan registration, JSX and CEP JSON dispatcher.
- Updated status/sources/navigation/master edition.

## v0.1 — 2026-09-30

- Initial developer bible structure with macOS and Windows branches, effect/AEGP/AEIO/Artisan fundamentals, testing, distribution, recipes and templates.
