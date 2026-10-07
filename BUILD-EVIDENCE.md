# Historical native link evidence — reconciled 2026-10-07

Original record: [audit commit 31fba783df86cb2eff4eba86a897591123857ca3](https://github.com/ios3kov/AAE-Developer-Bible/blob/31fba783df86cb2eff4eba86a897591123857ca3/BUILD-EVIDENCE.md).
This preserves that dated result, not a new build or current-main build driver.

## Original executed scope

SDK25.6 build61, Xcode27.0 (27A266a), C++17, macOS arm64 Debug,
deployment target12.0, signing disabled. Target12.0 is not a tested minimum OS.
Untouched Skeleton built, then canonical Gain/SmartFX Copy grafted into a local
licensed Skeleton project with resources; Xcode build/link succeeded.

| Source | Source SHA-256 | Historical binary SHA-256 |
|---|---|---|
| Minimal Gain | `ccdc036222b41ab06995bc23dd0151a5462e271c17a93285fa6794a8f06d9e4f` | `714c62736cec8d25aef58ca663637394b23921fa8ece83a321c5f029acd31891` |
| SmartFX Copy | `ed5f2e7245aa5dc6846ddccc585878aad4361f654453a5b933595f143dd1c288` | `6069cb480a635ee9d4322b0098c41e2cf04249998ea014c71ba02e22d87b4561` |

Original inspection recorded EffectMain/PluginDataEntryFunction exports,
Contents/Resources/Skeleton.rsrc, Gain flags33554432/0 and SmartFX33554432/5120;
MFR unset. Resource presence was not exhaustive PiPL validation. Both bundles were
Skeleton.plugin; do not install together as independently identified products.

## Rechecked now

At main source `3bf1985`, read original record and compared old/current canonical
`.cpp` bytes with SHA-256: both identical to table. Source continuity is **not**
identity of a new artifact, project settings, installed image or host behavior.
Original local logs/private licensed workspace were not re-inspected here.
Audit build driver exists at its immutable commit; current command routes:
[macOS](08-MACOS/09-PRODUCTION-BUILD-PIPELINE.md),
[Windows](09-WINDOWS/09-PRODUCTION-BUILD-PIPELINE.md).

## Not established

No AE discovery/load/render, ROI/cancel/MFR, Universal/Intel/Windows/GPU execution,
signing/notarization or release packaging. New syntax/type evidence is separate in
[VERIFICATION](VERIFICATION.md). Do not replace NOT_RUN host cells in illustrative
release plans with this historical link success.
