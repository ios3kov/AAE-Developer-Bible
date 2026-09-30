# AE Developer Bible — Completion Checklist

Date: **2026-09-30**
Status: **authoritative acceptance checklist for COMPLETION-PLAN.md**

A checked item requires recorded evidence. Documentation presence alone is not completion.

## Ready means

- required examples build from a clean checkout against the declared Adobe SDK;
- installation is non-destructive and failures fail closed;
- required host scenarios run in a named After Effects build and produce the documented result;
- documentation, code, verification reports, navigation and status agree;
- supported platforms/versions are explicit;
- unknown or untested behavior stays explicitly marked;
- the agreed built-in effects atlas reaches its per-effect Definition of Done.

## Baseline matrix

| Dimension | Required baseline | Current state |
|---|---|---|
| After Effects | 25.6.0.101 | native-effect user-run numerical observations exist; practical reference examples not host-verified |
| Adobe SDK | 25.6 | macOS syntax/type baseline exists |
| macOS | arm64 | native-effect research observations exist; reference-example host acceptance pending |
| Windows | x64 baseline | SDK/host verification pending |
| C++ | C++17 | current native baseline |
| Classic Effect | Minimal Gain 8/16-bpc | host pending |
| SmartFX | copy path 8/16/32-bpc | pixel/ROI/MFR host tests pending |
| AEGP | MenuTool lifecycle | host lifecycle pending |

## Gate 1 — Scope

- [x] Completion plan exists.
- [x] Current coverage gaps are documented.
- [x] Verification boundaries are documented.
- [x] Baseline matrix is explicit.
- [x] Major areas below have acceptance gates.
- [x] Built-in effects atlas remains in final scope.

## Gate 2 — Safe tooling

### host_cycle.py
- [ ] Reject source plugin == destination plugin.
- [ ] Never destroy the only input copy.
- [ ] Back up an existing installed plugin before replacement.
- [ ] Restore the previous plugin after failed install.
- [ ] Non-zero aerender exit fails the command.
- [ ] Support/report timeout.
- [ ] Missing expected render output is failure.
- [ ] Machine-readable report separates install/load/render states.
- [ ] Tests cover success, render failure, timeout, missing output and path collision.

### SDK sample materialization
- [ ] Reject source/destination collision.
- [ ] Replacement cannot destroy source.
- [ ] Missing/partial SDK sample fails closed.
- [ ] Destructive-path tests exist.

**Acceptance:** destructive-path tests pass and false-success render tests are impossible.

## Gate 3 — Documentation consistency

- [ ] Mark superseded hypotheses explicitly.
- [ ] Correct the historical 3D Channel Extract "no physical standalone plug-in" claim wherever it can read as current truth.
- [ ] Current classification matches runtime evidence.
- [ ] Add section 21 to MkDocs navigation.
- [ ] README, STATUS, coverage, verification and checklist use compatible readiness language.
- [ ] MASTER and manifest regenerate cleanly.
- [ ] MkDocs strict build passes.
- [ ] Historical logs remain preserved but separated from current conclusions.

## Gate 3A — Reuse audit: FSTR Line and AE Hot Loader

**Required before creating new examples in Gates 5–6. Status: OPEN.**

Primary extraction and pinned sources: [project case studies](22-PROJECT-CASE-STUDIES/README.md). This audit does not require completion of either product and does not automatically make any Bible example host-verified.

- [x] Pin the reviewed document snapshots: FSTR Line `c69e3663de59dc44cbdef18042891f6dd1ce5ee6`, AE Hot Loader `cf338bcd861504d695c3181767c18bb423575814`.
- [x] Preserve architecture lessons, negative experiments and reported host results with their limitations in section 22.
- [ ] Map each candidate below to actual code files, source commits, related tests and build identity. A documentation snapshot is not necessarily the tested build.
- [ ] Review original test records/artifacts; identify missing raw evidence and separate project-reported results from independently repeated tests.
- [ ] Run applicable portable tests for the selected source snapshot and record commands/results without calling them AE host tests.
- [ ] Record reuse / adapt / do not transfer decisions with reasons for every candidate.
- [ ] Check provenance before copying code; keep licensed third-party headers/binaries outside Bible.
- [ ] Specify Bible-side regression and host acceptance tests for every selected adaptation; actual acceptance remains in Gates 4–7.
- [ ] Link accepted general lessons into their target chapters, keeping private-loader experiments separate from supported SDK recipes.

### Initial candidate register

| ID | Source candidate | Intended Bible destination | Current state / acceptance boundary |
|---|---|---|---|
| FL-01 | UI/Core/Host Adapter separation; normalized snapshots | 07-PANELS, 15-COMMUNICATION | Architecture extracted; code/test mapping open. |
| FL-02 | Stale-command rejection, refresh coalescing and request invalidation | 15-COMMUNICATION, 10-TESTING | Project-reported behavior; implementation audit and portable regression open. |
| FL-03 | FakeHostAdapter and controlled fixtures | 10-TESTING, 16-WORKING-TEMPLATES | Identify reusable tests; no automatic transfer of host readiness. |
| FL-04 | Command-hook negative experiment and probe ABI correction | 03-AEGP, 08-MACOS, section 22 | Source report extracted. Preserve tested ExtendScript-only scope and NOT RUN cases; SYNC-001 remains blocked in the source snapshot. |
| HL-01 | ScriptUI request/response protocol and AEGP Agent | 15-COMMUNICATION, 16-WORKING-TEMPLATES | PoC protocol extracted; inspect file-write behavior, request correlation, lifecycle and tests. |
| HL-02 | Loaded-module lookup, diagnostics and failed callback experiments | 08-MACOS, 01-ARCHITECTURE | Project-reported findings extracted; code/artifact audit open. |
| HL-03 | New-bundle late-loading experiment through internal ML::LoadPlugins | section 22, research cross-reference | Reported live PoC, not general hot replacement. Match experiment branch/build and raw evidence before any readiness promotion. |

**Gate 3A acceptance:** candidate audit is complete; each candidate has source evidence, limitations and a justified transfer decision. For selected code, destinations and Bible-side tests are defined. Completion of SYNC-001 or production Hot Loader is not a prerequisite. After adaptation, the relevant build/host gates must still pass.

Do not infer absence of all AE notification mechanisms from one negative probe. Do not infer unloading or replacing an already-loaded plugin from successful late loading of a new bundle. Internal loader code must not become a hidden dependency of the safe installer or ordinary SDK examples.

## Gate 4 — SDK verification

- [ ] Required SDK 25.6 contract families parse without unresolved required declarations.
- [ ] Parser diagnostics cannot masquerade as ABI/signature validation.
- [ ] Recipes are checked by real compilation against the declared SDK.
- [ ] Native source set compiles with strict warnings.
- [ ] Tests cover malformed/partial/version/signature drift cases.
- [ ] CI distinguishes portable synthetic checks from licensed-SDK checks.
- [ ] Windows SDK validation is reproducible.

## Gate 5 — Three host-verified references

### Minimal Gain
- [ ] Clean build and PiPL/registration validation.
- [ ] Safe install/uninstall.
- [ ] AE loads effect and parameter defaults/ranges match docs.
- [ ] Controlled 8-bpc and 16-bpc pixel tests.
- [ ] Alpha behavior.
- [ ] Save/reopen persistence.
- [ ] Failure/unload behavior.

### SmartFX Copy
- [ ] Clean build/registration and host load.
- [ ] Pre-render checkout/result rectangles.
- [ ] 8/16/32-bpc pixel equivalence.
- [ ] ROI/partial frame.
- [ ] Cancellation/error cleanup.
- [ ] MFR stays disabled until concurrent-frame stress passes.

### AEGP MenuTool
- [ ] Clean build/registration and host load.
- [ ] Menu appears exactly once and command works.
- [ ] Update-menu hook.
- [ ] Safe partial initialization.
- [ ] Death-hook cleanup.
- [ ] Repeated launch/quit without duplicate registration/crash.

## Gate 6 — Remaining integration families

Each requires a minimal complete example, instructions and host report.

- [ ] Custom UI / Drawbot.
- [ ] AEGP keyframer.
- [ ] Native panel.
- [ ] AEIO.
- [ ] Artisan.
- [ ] PICA provider/consumer.
- [ ] Effect ↔ AEGP bridge.
- [ ] GPU CPU/GPU comparison.
- [ ] Audio.
- [ ] JSX / ScriptUI.
- [ ] CEP round trip.
- [ ] Packaging/signing tested against produced artifacts.

## Gate 7 — Host correctness/stress

Where applicable:
- [ ] 8/16/32-bpc.
- [ ] Alpha/premultiplication.
- [ ] ROI/partial render.
- [ ] Odd/tiny/large dimensions and non-zero origins.
- [ ] Cancellation and invalid/missing input.
- [ ] Deterministic repeated output.
- [ ] Save/reopen.
- [ ] MFR concurrency.
- [ ] CPU/GPU equivalence.
- [ ] Repeated lifecycle crash/leak diagnostics.
- [ ] Input/output hashes plus host/build metadata.

## Gate 8 — Built-in effects atlas

### Infrastructure
- [ ] macOS installation scanner + machine-readable inventory.
- [ ] Windows installation scanner + machine-readable inventory.
- [ ] Effect → match name → classification → module map.
- [ ] Evidence level on every nontrivial claim.
- [ ] Runtime addresses never treated as stable offsets.

### 3D Channel Extract pilot
Already captured: physical module, FilterMain, selector table, named function boundaries, RenderX 8/16, FillInAllParams and evidence of inline 32-bpc processing.

Latest milestone: [reviewed numerical observations](21-BUILTIN-EFFECTS-REVERSE-ENGINEERING/3D-Channel/3D-Channel-Extract/NUMERICAL-OBSERVATIONS-2026-09-30.md), user-run collector `ACX-PROBE-20260930-01-1790786999423-396382`. All **28 planned records / 1260 sampleImage RGBA tuples** returned, without logged acquisition or cleanup errors. This is acquisition and scoped numerical evidence, not full-effect PASS.

- [x] Review first numerical batch: baseline/invert/equal/reversed/narrow/AA/Collapse/source control/repeat at 8/16/32 bpc and one Clamp OFF request at 32 bpc.
- [x] Record exact comparisons, original report hash and limitations. Baseline repeats and invert/reversed pairs match at the sampled points; equal-1000 gives approximately 128/255 at 8 bpc and 0.5 at 16/32; Clamp OFF permits values above 1 in this run.
- [ ] Edge-specific AA and DPTH/DPAA evidence. **The coarse AA pair is unchanged; this is not an AA acceptance result.**

Remaining full pilot gates:
- [x] Complete static capture + binary hash (`412a6deefc1d7a710a9019b6a068180556417b0548d0703d34852bcd395dcab8`).
- [x] Decode ACX_Power2 (`2^n` over its signed-char input).
- [ ] Map parameters/defaults/ranges. **Slots and initial values captured; Black/White API bounds ±10000000 observed. Fresh defaults, endpoint writes and UI dependencies remain open.**
- [x] Record static channel branch targets. **Prior static selector interpretation is not a runtime mapping: the returned Z-Depth scripting value is 1. Full UI/stored-value/private-FourCC correspondence still requires reconciliation.**
- [ ] Reconstruct 8/16/32-bpc pseudocode. **Prior all-channel static write-up exists; this Z-Depth-only batch does not validate other channels or establish bit-exact equivalence.**
- [ ] Missing-channel, range reversal/equal-limit, clamp and alpha behavior. **Numerical inversion/reversal/equal-1000 and sampled 32-bpc upper clamping recorded; missing data, lower bound, non-finite inputs and transparent edges remain.**
- [ ] Controlled AE fixtures + raw output hashes. **Report hash recorded; the project was dirty at run start, and neither live geometry nor raw rendered frames were exported.**
- [ ] CPU/GPU/MFR status. **Project identifiers and same-session sample repeatability do not close this gate.**
- [ ] Independent reimplementation recipe and native-output comparison.

The collector reports `sourceRenderer=ADBE Advanced 3d` and `projectGpuSetting=1816`; retain the identifiers literally rather than asserting an effect execution path. Keep Collapse ON and OFF results separate: their samples differ at every grid point in this run.

### Full catalog
For every agreed entry in MASTER-EFFECT-LIST.md:
- [ ] classification, names and implementation module where obtainable;
- [ ] parameters and controlled render behavior;
- [ ] CPU/GPU/MFR status;
- [ ] static evidence;
- [ ] reconstructed pipeline separated from facts;
- [ ] unknowns;
- [ ] independent reimplementation recipe.

## Gate 9 — Release

### Release 1 — verified practical Bible
- [ ] Gates 1–7, including Gate 3A, complete.
- [ ] Clean-machine reproduction.
- [ ] No blocking known defects.
- [ ] Site/navigation/MASTER/manifest agree.
- [ ] Release notes list tested matrix and limits.

### Release 2 — complete Bible + atlas
- [ ] Release 1 remains green.
- [ ] Gate 8 complete.
- [ ] macOS/Windows differences documented.
- [ ] Independent final audit.
- [ ] Version/tag from reproducible commit.

## Required host evidence record

Every host report records: repository commit; exact AE build; SDK; OS; architecture; compiler; build/install/test commands; fixture; expected and observed results; hashes where applicable; PASS/FAIL; known limitations.

For cross-project lessons also record the source repository, pinned document/code commit, tested build identity when known, and whether the result is source-reported or independently reproduced. Preserve missing evidence explicitly.

## Immediate execution order

1. Gate 2: repair host_cycle.py and add destructive/failure tests.
2. Gate 3: resolve documentation contradictions and expose section 21.
3. Gate 3A: audit FSTR Line / AE Hot Loader candidates before creating new examples; preserve accepted lessons and transfer decisions in section 22.
4. Gate 4: strengthen exact-SDK verification.
5. Gate 5: host-verify Minimal Gain, SmartFX Copy and MenuTool using audited reusable components where appropriate.
6. Gates 6–7: complete families and correctness/stress coverage.
7. Gate 8: finish 3D Channel Extract pilot, then catalog. **Current user-directed work is the numerical native-effect research milestone above; other gates are not implicitly complete.**
8. Gate 9: release audits.
