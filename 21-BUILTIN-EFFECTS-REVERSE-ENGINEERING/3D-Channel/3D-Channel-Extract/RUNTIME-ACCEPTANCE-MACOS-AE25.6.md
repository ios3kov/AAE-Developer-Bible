# 3D Channel Extract — Runtime Acceptance Protocol

Target: **After Effects 25.6.0.101 / macOS arm64**  
Previously captured binary SHA-256: `412a6deefc1d7a710a9019b6a068180556417b0548d0703d34852bcd395dcab8`  
Current status: **first user-executed numerical batch reviewed: 28/28 records and 1260 sampleImage observations. Full-effect acceptance and Gate 8 remain open.**

## Latest numerical evidence

See [Numerical observations, 2026-09-30](NUMERICAL-OBSERVATIONS-2026-09-30.md) for the exact report identity, environment, measurements, comparisons and reproduction snippet.

Run: `ACX-PROBE-20260930-01-1790786999423-396382`. Original report SHA-256: `b6bd1e918d69f6ae2d6b7f02d3a97e3979cac7edf0af16130488dc5374d66491`.

The returned JSON records all 28 planned cases as `RECORDED`, with `COLLECTED` at the top level and no logged case or cleanup errors. Those labels describe acquisition, not 28 acceptance PASS results. Parameter readbacks are stable; requested core settings and all 32-bpc clamp requests are reflected in the records.

| Scoped observation | Result in this batch | Limit |
|---|---|---|
| Baseline at 8/16/32 project bpc | Three grayscale levels at each bit depth | sampleImage, not raw frame equivalence |
| Invert versus reversed endpoints | Exactly identical recorded RGBA at all 45 points for each bpc | Not exact complementarity after integer conversion |
| Black = White = 1000 | Gray approximately 128/255 at 8 bpc; exactly 0.5 at 16/32 bpc | No claim for all degenerate/non-finite inputs |
| Clamp OFF versus ON at 32 bpc, 1000/2000 | OFF approximately 0.05/1.05/2.55; ON approximately 0.05/1/1; 42/45 points change | No negative inputs or UI availability test |
| Baseline repeat | Same 45 serialized RGBA values at every tested bpc | No cold-cache, restart or MFR test |
| Collapse ON versus OFF | All 45 points differ at every tested bpc | Distinct source-processing states, not evidence of damage |
| AA ON versus OFF | Same 45 sampled values | Edge-specific AA and DPTH/DPAA identity remain open |
| Alpha | All recorded values are 1 | Sampled source-color control is also opaque; transparency is untested |
| Parameter 1 and numeric bounds | Selector 1 throughout; Black/White API bounds ±10000000 | Not a full popup/FourCC map, slider-range test or fresh-default test |

The report records renderer identifier `ADBE Advanced 3d`, GPU setting `1816`, AE `25.6x101`, and source time 0.84 seconds. Keep those identifiers literal rather than inferring effect-level GPU/MFR execution. `projectDirtyAtStart=true`: the live source was not proven identical to the previously uploaded AEP. The loaded Adobe binary hash was not measured by the collector.

## Current source constraints — corrections, not new runtime results

Adobe documents that the **3D Channel popup is disabled on a nested composition**. A disabled popup on DEPTH_SOURCE inside DEPTH_TEST is expected behavior, not evidence of a damaged plug-in. Resetting, reinstalling, duplicating the layer or restarting AE is not a remedy for this documented restriction.

Adobe describes **Clamp Output as a 32-bpc-only control** and separately states that nested-composition depth is clamped to 0–1 at 32 bpc. The returned numerical batch, however, records values above 1 after an accepted scripted Clamp OFF request. Preserve that difference between the documentation statement and this measured scenario; do not discard either or claim the UI toggle was tested. A stored checkbox value, script write acceptance, UI availability and observable output are separate observations.

Source: [Adobe — 3D Channel effects, Anti-alias and Extract a depth pass](https://helpx.adobe.com/after-effects/desktop/apply-effects-and-animation-presets/list-of-effects/3d-channel-effects.html), reviewed 2026-09-30. Vendor statements are not additional measurements of the supplied fixture.

The user confirmed that **Anti-alias can be clicked** in the nested-depth fixture. Earlier conclusions based only on its grey appearance must not override that interaction evidence. Neither a screenshot nor an unchanged coarse sample grid identifies which private FourCC was requested.

## Existing observations and their limits

The chronological record before the earlier correction remains available at [the pinned pre-correction revision](https://github.com/ios3kov/AAE-Developer-Bible/blob/c240edf6e59f8fb6305a3547f2b79301e1795353/21-BUILTIN-EFFECTS-REVERSE-ENGINEERING/3D-Channel/3D-Channel-Extract/RUNTIME-ACCEPTANCE-MACOS-AE25.6.md).

| Earlier observation on 2026-09-30 | Evidence scope | Current interpretation |
|---|---|---|
| Popup on a plain Black Solid listed all eight channels | User screenshots | UI order observed, not proof of channel availability or private FourCC mapping |
| Visible values: Black 5000, White 0, AA OFF, Clamp ON, Invert OFF | User screenshots | Initial values, not a complete factory-default or allowed-range test |
| Some controls appeared grey on non-depth selections | Appearance only | Not a universal source-dependent enablement rule |
| Nested source produced distinct grayscale regions | User-built fixture and screenshot | Qualitative depth response; numerical data now recorded separately |
| Invert ON changed ramp orientation at 17:47 | Screenshot | Qualitative; numerical OFF-Collapse comparison now exists in the batch |
| Equal endpoints produced uniform mid-grey at 17:48 | Screenshot | Numerical equal-1000 result now exists in the batch |
| Swapped endpoints reversed ramp orientation at 17:48 | Screenshot | Numerical comparison now exists in the batch |
| User reported Collapse had been ON during earlier runs | User report | Earlier images remain labelled Collapse ON, not pooled with the later OFF baseline |
| Collapse switched OFF at 17:51 | User action and screenshot | Separate fixture state; the batch confirms ON/OFF sample differences |
| Narrow range with Clamp stored ON | Single screenshot | Not an ON/OFF clamp comparison; superseded for that question by the 32-bpc pair |
| AA reported clickable at 17:57 | User interaction | Valid interaction evidence; not DPTH/DPAA identity |
| Popup stayed disabled after reset/restart on the precomp | User report plus vendor documentation | Expected nested-composition restriction, not a reproduced state/UI bug |

Screen captures are qualitative evidence. Display-managed screenshot RGB is not raw effect output. The numerical batch does not retrospectively turn those screenshots into pixel-level tests.

## Numerical collector and batch matrix

Use [ACX_Depth_Probe.jsx](../../../scripts/ACX_Depth_Probe.jsx) with the existing open project. `DEPTH_TEST` must contain one **2D precomp layer**, with only `3D Channel Extract` on that layer. The script validates this instead of guessing which layer to modify.

Run **File > Scripts > Run Script File**. It creates a unique `AE_Depth_...` Desktop folder containing `report.json`. If file writing is denied, it stops before duplicating the composition; it never changes the scripting permission itself.

The first returned batch is already recorded. Do not ask the user to repeat these cases without a new question or a changed test condition.

Each case below is requested at **8, 16 and 32 project bpc**, at one recorded time and 45 layer-space locations:

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

One additional **32-bpc-only** case requests Clamp OFF with Black 1000 / White 2000: **28 records total**. Writes and parameter readbacks are separate from image samples. The popup is not forced to another channel. No infinity, ID or datatype-mismatch fixture is manufactured.

### Measurement contract

A temporary Source Text expression calls `sampleImage(point, [0.5,0.5], true, time)`, read through `valueAtTime(time, false)`. The report includes RGBA, parameter names/match names/values/numeric bounds, project bpc, renderer, color settings and run identity.

This is **alpha-weighted expression sampling after the layer's effects**, not a raw output-file render, frame hash or final-composition screenshot. The grid can miss edges or small objects. A warm repeat does not prove cold-cache behavior or MFR safety.

Sources: [Adobe expression-language reference](https://helpx.adobe.com/after-effects/desktop/work-with-expressions/expression-language-reference/expression-language-reference.html) and [After Effects Scripting Guide — Property.valueAtTime](https://ae-scripting.docsforadobe.dev/property/property/#propertyvalueattime).

### Safety and failure behavior

Only a disposable duplicate of the outer composition is edited. The nested source is referenced read-only. The script does not save the input AEP, alter preferences, purge caches, touch the Render Queue or patch a binary. In `finally` it restores project bpc and removes its temporary composition; a cleanup failure is an error. The live project can remain dirty after temporary edits.

A checkpoint precedes each host sampling call. A crash/hang can leave `RUNNING`, never an invented PASS. The 180-second budget is checked **between** host calls and cannot interrupt a hung AE. Core-setting or malformed-sample failures stop the collector. Retain partial reports.

`COLLECTED`/`RECORDED` are acquisition states, **not acceptance statuses**. The report does not export the live AEP or identify the loaded native binary. No logged cleanup error is not an independent filesystem or leak audit.

## Remaining full-effect acceptance gates

- [ ] Full UI menu / stored integer / private FourCC mapping. **Z-Depth scripting value 1 observed; other values and private callbacks untraced.**
- [ ] Parameter defaults, allowed ranges and UI availability. **API bounds and initial values captured; Reset and endpoint writes still untested.**
- [ ] AA OFF/ON channel identity and edge-specific samples. **Coarse-grid samples equal; not an AA acceptance result.**
- [ ] Complete Clamp behavior. **32-bpc upper clamping and accepted OFF request observed; lower bound, UI and other source cases remain.**
- [x] Invert, equal-1000 and reversed endpoints: numerical comparison at known Collapse OFF, **restricted to this grid and run**.
- [ ] Controlled positive/negative infinity input, or explicit fixture limitation.
- [ ] Missing-channel behavior, output and error reporting.
- [ ] Controlled datatype mismatch, or explicit fixture limitation.
- [ ] Raw 8/16/32-bpc renders, input/output identities and tolerance checks. **SampleImage observations exist but do not replace this gate.**
- [ ] Object ID boundaries, Material ID, UV, normals, coverage, background and unclamped color on suitable sources.
- [ ] Alpha/transparency and out-of-bounds behavior, including edge coverage.
- [ ] Effect-level CPU/GPU evidence, not merely a project setting.
- [ ] Real MFR/concurrent-render determinism and cold/restart checks. **Same-session sample repeatability observed only.**
- [ ] Independent implementation compared with controlled native-effect outputs.

A fixture limitation is BLOCKED or N/A with a reason, not PASS for the whole plug-in. Scope exclusion requires an explicit decision. Numerical collection does not close bit-exact reconstruction or the complete atlas pilot.

## Collector validation record

Build: `ACX-PROBE-20260930-01`. Script introduced at `76dfdbbc18f7a1586aadea2a90dcb3e92d15eebd`; portable tests at `f23163ec54bd614d0ae34c1de7004192d9697eb8`.

Previously recorded: Node 22.16 **13 portable control-flow/safety tests PASS** via `node scripts/test_acx_depth_probe.js`; ECMAScript 3 syntax parsed with Acorn 8.14.1 after removing `#target`. These tests do not emulate Adobe's algorithm.

**First user-executed host collection: returned and reviewed.** All 28 records are available with no logged acquisition/cleanup errors. The assistant analysed the submitted data, not a local AE execution. Detailed numerical results and limitations are in [the observation report](NUMERICAL-OBSERVATIONS-2026-09-30.md).
