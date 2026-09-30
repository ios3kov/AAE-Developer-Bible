# 3D Channel Extract — Runtime Acceptance Protocol

Target: **After Effects 25.6.0.101 / macOS arm64**  
Previously captured binary SHA-256: `412a6deefc1d7a710a9019b6a068180556417b0548d0703d34852bcd395dcab8`  
Current status: **qualitative user-run observations exist; numerical batch collection is prepared, not yet host-verified. Gate 8 remains open.**

## Current source constraints — corrections, not new runtime results

Adobe documents that the **3D Channel popup is disabled on a nested composition**. A disabled popup on DEPTH_SOURCE inside DEPTH_TEST is expected behavior, not evidence of a damaged plug-in. Resetting, reinstalling, duplicating the layer or restarting AE is not a remedy for this documented restriction.

Adobe describes **Clamp Output as a 32-bpc-only control** and separately states that nested-composition depth is clamped to 0–1 at 32 bpc. Do not infer from a grey checkbox at another bit depth that Classic 3D never supports the control. A stored checkbox value, a script accepting a write, UI availability and an observable pixel change are four different observations.

Source: [Adobe — 3D Channel effects, Anti-alias and Extract a depth pass](https://helpx.adobe.com/after-effects/desktop/apply-effects-and-animation-presets/list-of-effects/3d-channel-effects.html), reviewed 2026-09-30. These statements are **vendor documentation**, not additional measurements of the supplied fixture.

The user confirmed that **Anti-alias can be clicked** in the nested-depth fixture. Earlier conclusions based only on its grey appearance must not override that interaction evidence. A screenshot cannot establish that a particular private FourCC, such as DPAA, was requested.

## Existing observations and their limits

The chronological record before this correction remains available at [the pinned pre-correction revision](https://github.com/ios3kov/AAE-Developer-Bible/blob/c240edf6e59f8fb6305a3547f2b79301e1795353/21-BUILTIN-EFFECTS-REVERSE-ENGINEERING/3D-Channel/3D-Channel-Extract/RUNTIME-ACCEPTANCE-MACOS-AE25.6.md). The table below preserves the observations while correcting overly broad interpretations.

| Observation on 2026-09-30 | Evidence scope | Current interpretation |
|---|---|---|
| Popup on a plain Black Solid listed Z-Depth, Object ID, Texture UV, Surface Normals, Coverage, Background RGB, Unclamped RGB, Material ID | User screenshots | UI order observed. No proof of the underlying selector/FourCC mapping or availability of those channels. |
| Initial visible values: Black 5000, White 0, AA OFF, Clamp stored ON, Invert OFF | User screenshots | Values observed. Not a complete allowed-range or enablement test. |
| Several subordinate controls appeared grey while cycling non-depth items on the solid | Appearance only | Do not promote visual styling into a universal source-dependent enablement rule. |
| Nested source with a camera and three 3D solids produced distinct grayscale areas | User-built fixture and screenshot | Qualitative depth response observed; geometry and exact sample values were not independently captured. |
| Invert ON with Black 5000 / White 0 changed depth-ramp orientation | Screenshot at 17:47 | Qualitative inversion observed. Exact numerical complement remains open. |
| Black = White = 1000 produced a uniform mid-grey field, without a visible error dialog | Screenshot at 17:48 | Degenerate-range response observed. Screenshot does not establish an exact scalar or general absence of errors. |
| Black 0 / White 5000 with Invert OFF reversed the previous ramp orientation | Screenshot at 17:48 | Qualitative endpoint reversal observed. |
| User subsequently reported Collapse Transformations had been ON during earlier runs | User report | Earlier inversion/equal/reversal observations must be labelled Collapse ON, user-reported; not reused as OFF-baseline acceptance. |
| Collapse was then switched OFF and a new depth image supplied at 17:51 | User action and screenshot | Separate OFF fixture state. Do not pool ON/OFF images as identical test inputs. |
| Black 1000 / White 2000 was displayed with Clamp stored ON | User screenshot | A single setting cannot establish an ON/OFF clamp difference. The earlier claim that this completed the clamp test was too strong. |
| Anti-alias was reported clickable and an enabled-state image supplied at 17:57 | User interaction and screenshot | Checkbox interaction observed. DPTH/DPAA identity and numerical edge differences remain open. |
| Popup stayed disabled after resets and restarts on the precomp | User report plus Adobe documentation | Expected nested-composition restriction, not a reproduced state/UI bug. |

Screen captures are qualitative evidence. Their display-managed RGB is not raw effect output. No new runtime test is marked PASS merely because this document or a script has been created.

## Next: one numerical observation batch

Use [ACX_Depth_Probe.jsx](../../../scripts/ACX_Depth_Probe.jsx) with the existing open project. `DEPTH_TEST` must contain one **2D precomp layer**, with only `3D Channel Extract` on that layer. The script validates this instead of guessing which layer to modify.

Run **File > Scripts > Run Script File** and select the JSX. It creates a unique `AE_Depth_...` folder on Desktop containing `report.json`. If file writing is denied, it stops before duplicating the composition and explains the scripting permission needed. It never changes that preference itself.

### Batch matrix

Each of the following is requested at **8, 16 and 32 project bpc**, at one recorded time and 45 layer-space sample locations:

| Case | Black / White | Invert | AA | Collapse | Effect |
|---|---|---|---|---|---|
| baseline | 5000 / 0 | OFF | OFF | OFF | ON |
| invert | 5000 / 0 | ON | OFF | OFF | ON |
| equal | 1000 / 1000 | OFF | OFF | OFF | ON |
| reversed | 0 / 5000 | OFF | OFF | OFF | ON |
| narrow | 1000 / 2000 | OFF | OFF | OFF | ON |
| narrow_aa | 1000 / 2000 | OFF | ON | OFF | ON |
| collapse_on | 5000 / 0 | OFF | OFF | ON | ON |
| source_color_control | 5000 / 0 | OFF | OFF | OFF | OFF |
| baseline_repeat | 5000 / 0 | OFF | OFF | OFF | ON |

One additional **32-bpc-only** case requests Clamp OFF with Black 1000 / White 2000. Total: **28 planned records**. Accepted writes and parameter readbacks are logged separately from image samples. The popup is not forced to another channel. The script does not manufacture infinity, ID or datatype-mismatch fixtures.

### Measurement contract

The sampler uses a temporary Source Text expression and `sampleImage(point, [0.5,0.5], true, time)`, read through `valueAtTime(time, false)`. It records RGBA, parameter names/match names/values/available numeric bounds, project bit depth, renderer, color-management settings and run identity.

This is **alpha-weighted expression sampling after the layer's effects**, not a raw output-file render, frame hash or final-composition screenshot. The 45-point grid can miss anti-aliased edges or small objects. Lack of a difference in this grid does not prove lack of an effect. A warm repeated sample does not prove cold-cache behavior or MFR safety.

Sources: [Adobe expression-language reference](https://helpx.adobe.com/after-effects/desktop/work-with-expressions/expression-language-reference/expression-language-reference.html) and the maintained [After Effects Scripting Guide — Property.valueAtTime](https://ae-scripting.docsforadobe.dev/property/property/#propertyvalueattime).

### Safety and failure behavior

Only a disposable duplicate of the outer composition is edited. The nested source is referenced read-only; its layers are not rebuilt. The script does not save or overwrite the input AEP, alter preferences, purge caches, touch the Render Queue or patch a binary. It restores project bpc and removes its temporary composition in `finally`. A cleanup failure is an error. The project can remain marked dirty due to temporary edits; the original disk file remains unchanged by the script.

A checkpoint is written before each host sampling call. A crash/hang can leave `RUNNING`, never an invented PASS. The 180-second budget is checked **between** host calls and cannot interrupt a hung AE. The collector stops on a failed core setting or malformed sample rather than repeating a broken operation. Retain any partial report.

`COLLECTED`/`RECORDED` are acquisition states, **not test acceptance statuses**. Review the returned report and define supported numerical comparisons before closing gates. The report does not export the live AEP or prove the identity of the loaded native binary.

## Remaining full-effect acceptance gates

- [ ] UI menu item / stored integer / private FourCC mapping, using appropriate source and evidence.
- [ ] Parameter defaults, allowed ranges and source/bit-depth-dependent UI availability.
- [ ] AA OFF/ON channel identity and edge-specific numerical samples.
- [ ] Clamp behavior, separating general 32-bpc control from nested-source policy.
- [ ] Invert, equal endpoints and reversed endpoints: numerical comparison with known Collapse state.
- [ ] Controlled positive/negative infinity input, or an explicit fixture limitation.
- [ ] Missing-channel behavior, visible output and return/error reporting.
- [ ] Controlled datatype mismatch, or an explicit fixture limitation.
- [ ] Raw 8/16/32-bpc renders, input/output identities and applicable tolerance checks.
- [ ] Object ID boundary values and Material ID samples from a suitable auxiliary source.
- [ ] UV, normals, coverage, background and unclamped color from suitable auxiliary sources.
- [ ] Alpha and out-of-bounds behavior, including edge coverage.
- [ ] Effect-level CPU/GPU evidence, not merely the project's renderer setting.
- [ ] Real MFR/concurrent-render determinism and repeat/cold-cache checks.
- [ ] Independent implementation compared against controlled native-effect outputs.

A fixture limitation is BLOCKED or N/A with a reason, not PASS for the whole plug-in. Scope exclusion requires an explicit decision. Numerical collection does not by itself close bit-exact reconstruction or the complete atlas pilot.

## Collector validation record

Build: `ACX-PROBE-20260930-01`. Source: script introduced at `76dfdbbc18f7a1586aadea2a90dcb3e92d15eebd`; portable tests at `f23163ec54bd614d0ae34c1de7004192d9697eb8`.

Local Node 22.16: **13 portable control-flow/safety tests PASS** via `node scripts/test_acx_depth_probe.js`. ECMAScript 3 syntax parsed successfully with Node's bundled Acorn 8.14.1 after removing the Adobe `#target` directive. These checks cover run count, source isolation, restoration, filesystem failure, malformed observations, ignored clamp requests and interrupted runs. They do not emulate Adobe's effect algorithm.

**Collector execution inside After Effects: NOT RUN by the assistant.** The user's first returned `report.json` is the next evidence to review; it is not pre-labelled as a successful host run.
