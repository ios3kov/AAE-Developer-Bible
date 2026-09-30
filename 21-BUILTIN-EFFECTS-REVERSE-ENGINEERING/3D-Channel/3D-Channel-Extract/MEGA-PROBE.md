# ACX Mega Probe — v01 withdrawn

Date: **2026-09-30**. Original build: `ACX-MEGA-20260930-01`.

**Do not run v01 as an all-channel acceptance test. No replacement host run is requested.** The current script entry point is a non-mutating withdrawal notice. Original code and documentation are retained in [the pinned historical revision](https://github.com/ios3kov/AAE-Developer-Bible/tree/b9db3cd30fabb0c164a6dacf28674af304d5d403).

## Why withdrawn

The nested-composition fixture supported the collected Z-Depth observations, not verification of every auxiliary channel. `selectorSweep` forced values 1–8 through scripting despite the restricted precomp UI. Readback success and one black center sample for selectors 2–8 do not establish valid source data, channel availability, absence, datatype or rendering correctness.

The missing-channel, datatype-mismatch, ID-boundary, alpha/ROI, MFR and GPU capability functions were mostly explanatory placeholders, wrapped in acquisition statuses. They were not implemented acceptance tests. `UNAVAILABLE_PUBLIC_SCRIPT_API` is not evidence that no public MFR control exists. No concurrent-render or effect-level GPU comparison was performed.

The description of v01 as a complete final Mega Probe was incorrect. The general claim that every unavailable check would be safely isolated also exceeded the code: core sample/export errors still aborted the collection.

## What remains useful

The returned run `ACX-MEGA-20260930-01-1790791818056-853739` retains six Z-Depth edge records and twelve exported images. Recomputed same-format AA pairs change 3072 RGB pixels per frame; all twelve corresponding decoded images match Edge v04. These are scoped observations, not full-plug-in PASS.

Original evidence is preserved without rewriting its statuses. The [evidence audit](EVIDENCE-AUDIT-2026-09-30.md) records hashes, file precision, numerical comparisons, source constraints and all withdrawn claims. The original on-disk AEP was not rewritten by this audit.

## Gate before another collector

Use separately inventoried auxiliary footage with known channels and values, plus a separate missing-channel control. Define expected outputs and tolerances before execution. Keep nested Z-Depth, imported auxiliary footage, output processing, transparency/ROI and concurrency as separate test suites even when delivered in one package. A placeholder or unsupported input stays NOT RUN/BLOCKED and cannot become acceptance PASS merely because collection completes.

Existing depth measurements must not be discarded or rerun just to rename a tool. **Full-effect acceptance and Gate 8 remain OPEN.**
