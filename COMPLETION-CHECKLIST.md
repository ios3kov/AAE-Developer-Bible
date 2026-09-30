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
| After Effects | 25.6.0.101 | available for current macOS investigation; practical examples not host-verified |
| Adobe SDK | 25.6 | macOS syntax/type baseline exists |
| macOS | arm64 | host verification pending |
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

Remaining:
- [ ] Complete static capture + binary hash.
- [ ] Decode ACX_Power2.
- [ ] Map parameters/defaults/ranges.
- [ ] Map channel cases with evidence.
- [ ] Reconstruct 8/16/32-bpc pseudocode.
- [ ] Missing-channel, range reversal/equal-limit, clamp and alpha behavior.
- [ ] Controlled AE fixtures + output hashes.
- [ ] CPU/GPU/MFR status.
- [ ] Independent reimplementation recipe.

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
- [ ] Gates 1–7 complete.
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

## Immediate execution order

1. Gate 2: repair host_cycle.py and add destructive/failure tests.
2. Gate 3: resolve documentation contradictions and expose section 21.
3. Gate 4: strengthen exact-SDK verification.
4. Gate 5: host-verify Minimal Gain, SmartFX Copy and MenuTool.
5. Gates 6–7: complete families and correctness/stress coverage.
6. Gate 8: finish 3D Channel Extract pilot, then catalog.
7. Gate 9: release audits.
