# 3D Channel Extract — Runtime Acceptance Protocol

Date: **2026-09-30**. Target observations: **AE 25.6x101, macOS**.

**Status: existing nested-composition Z-Depth evidence retained; complete effect acceptance OPEN. No new user run requested.**

This is the corrected acceptance scope. [The previous protocol](https://github.com/ios3kov/AAE-Developer-Bible/blob/b9db3cd30fabb0c164a6dacf28674af304d5d403/21-BUILTIN-EFFECTS-REVERSE-ENGINEERING/3D-Channel/3D-Channel-Extract/RUNTIME-ACCEPTANCE-MACOS-AE25.6.md) preserves the chronological screenshots and original collection instructions. [The evidence audit](EVIDENCE-AUDIT-2026-09-30.md) is the current source for recomputed results, original hashes and withdrawn interpretations.

## Evidence versus acceptance

Original reports remain unmodified. `COLLECTED`, `RECORDED` and `EXPORTED` are acquisition statuses, not proof that every feature passed. A failed export does not discard earlier valid samples. Conversely, complete acquisition cannot turn placeholder checks into tests.

The offline audit opened the original 28-case report and all six supplied Edge/Mega ZIPs and decoded all 30 images. It did not run After Effects or alter the original AEP. Originals, analysis code and per-file hashes are retained in the private evidence bundle identified in the audit.

## Source classes must remain separate

### A. Nested-composition Z-Depth

The existing fixture supports the observed depth response and parameter comparisons. Adobe documents extraction from nested compositions with the 3D Channel popup disabled. A disabled popup here was not a damaged plug-in. Restart/reset/reinstallation was unnecessary.

The actual collected renderer identifier is `ADBE Advanced 3d`; preserve it literally. Do not retroactively label every run Classic 3D or infer GPU execution from the name. The live project was dirty, so its filename does not establish equivalence to the uploaded AEP.

### B. Imported auxiliary footage

The other channel algorithms need an independently inventoried source containing the relevant identifiers, datatypes, dimensions and known values. Adobe documents RPF/RLA and appropriately tagged OpenEXR. A supported file extension alone is not proof that the required channels exist or are exposed to this effect.

Writing popup values 2–8 on a precomp and getting black RGB does not verify Object ID, UV, normals, coverage, background, unclamped color or Material ID. The Mega v01 selector sweep is retained only as a scripting-write observation, not channel acceptance.

### C. Explicit negative and architecture fixtures

Missing-channel, datatype mismatch, ID boundaries, non-finite depth, transparency, ROI and concurrency require actual test inputs/operations and recorded outcomes. Returning a string saying UNAVAILABLE is not such a test. Fixture limitations remain BLOCKED/NOT RUN, not PASS for the whole effect.

Vendor source, separate from measurement: [Adobe — 3D Channel effects](https://helpx.adobe.com/after-effects/desktop/apply-effects-and-animation-presets/list-of-effects/3d-channel-effects.html), reviewed 2026-09-30. Clamp Output is documented for 32 bpc. UI availability, accepted scripting writes, stored values and observed pixels remain separate claims. The recorded script-controlled Clamp OFF values above one must not be overwritten by a broader reading of documentation.

## Retained observation matrix

| Check | Retained evidence | Remaining boundary |
|---|---|---|
| Initial values and parameter metadata | Black 5000, White 0, AA OFF, Clamp stored ON, Invert OFF; Black/White API bounds ±10000000 | Not a fresh Reset/default/range-endpoint test |
| Invert and endpoint reversal | Identical sampled RGBA for these two cases at all 45 points per bpc | Not universal bit-exact complement; integer residuals recorded |
| Equal endpoints at 1000 | Gray about 128/255 at 8 bpc; 0.5 at 16/32 | Other equal values/non-finite inputs not tested |
| 32-bpc upper clamp | OFF values about 0.05/1.05/2.55; ON clips sampled values into 0–1 | Negative/lower-bound input not tested |
| Same-session repeated baseline | All 45 tuples match at each bpc | Not cold-cache, restart or concurrency proof |
| Collapse ON/OFF | Samples differ; keep states separate | No claim that either is a defect |
| Edge-specific AA | 84/1342 sampled locations change per bpc; real exported AA pairs differ at 3072 pixels per frame | Not a private DPTH/DPAA trace or complete AA specification |
| Exported precision | Actual 8-bit TIFF, 16-bit PNG, float32 PSD, full dimensions decoded | Output pipeline differs from layer sampling; bit-exact equivalence OPEN |
| Multiple output members | 00007/00008 recorded separately and decoded | Not an exactly-one-frame timing PASS |
| Alpha | Full fourth-plane/sample alpha in these opaque observations | Not a transparent/partially covered/ROI fixture |

Detailed numerical scope: [first batch](NUMERICAL-OBSERVATIONS-2026-09-30.md) and [edge/export audit](EDGE-AND-RENDER-PROBE.md). Earlier screenshot observations made before the user switched Collapse OFF retain their user-reported ON state; they are not reused as OFF-baseline acceptance.

## Full-effect gates after the audit

- [x] Preserve and hash existing evidence without changing original report statuses.
- [x] Recompute original 28-case comparisons and scoped depth findings.
- [x] Recompute edge AA pairs and decode all supplied frame files.
- [x] Correct static selector-table byte offset and datatype spellings; withdraw incorrect UNCP formula.
- [x] Withdraw Mega v01 as an all-channel acceptance runner.
- [ ] Establish live source geometry, render time and loaded binary identity for future controlled tests.
- [ ] Verify fresh defaults, actual endpoint writes and source/bpc UI dependencies.
- [ ] Trace AA OFF/ON private channel identity where required; pixel differences do not substitute for it.
- [ ] Isolate output-module/color/precision processing and compare appropriate raw outputs with declared tolerances.
- [ ] Qualify imported auxiliary footage with independently known channel values before all-channel testing.
- [ ] Verify ID boundaries, UV component order, normals, coverage, background and packed unclamped color on suitable inputs.
- [ ] Supply controlled missing-channel and datatype-mismatch cases with actual error/output observations.
- [ ] Verify negative/clipped/non-finite depth and remaining degenerate cases with known inputs.
- [ ] Verify transparent edges, alpha and ROI with a dedicated fixture.
- [ ] Perform actual CPU/GPU comparisons and effect-level path observation where supported.
- [ ] Perform actual serial/MFR, cold-cache and restart comparisons; no placeholder can close this gate.
- [ ] Complete source-backed pseudocode and independent implementation/output comparison.

Public MFR configuration must be researched rather than declared impossible from the old placeholder: see the maintained [Application API](https://ae-scripting.docsforadobe.dev/general/application/#appsetmultiframerenderingconfig) and [Adobe automated rendering](https://helpx.adobe.com/after-effects/using/automated-rendering-network-rendering.html). Availability of a configuration API still does not prove parallel execution in any existing report.

## Gate before requesting another run

First inventory fixture content and identify the unresolved indirect callbacks from existing evidence. Define expected results and tolerances per suite. A single delivery may orchestrate multiple source-specific suites, but not pretend one depth precomp exercises every channel. Implement the test bodies and run applicable portable safety regressions before delivery. Preserve the original Render Queue/project state, avoid overwriting the AEP, and distinguish collection completion from accepted test coverage.

No repetition of already completed depth matrices is requested. **Full-effect acceptance and Gate 8 remain OPEN.**
