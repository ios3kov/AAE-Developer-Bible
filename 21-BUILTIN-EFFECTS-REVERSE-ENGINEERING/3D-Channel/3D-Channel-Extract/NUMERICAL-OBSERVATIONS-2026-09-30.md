# 3D Channel Extract — numerical observations, 2026-09-30

Status: **user-executed host collection reviewed; 28/28 records available. Full-effect acceptance remains OPEN.**

This is a descriptive analysis of the returned report, not a claim that 28 independent acceptance tests passed. The collector uses expression `sampleImage`, not a raw renderer-output dump. No native plug-in was modified.

## Evidence identity

- Original artifact: user-supplied `report.json`, conversation attachment `file_000000002f8c81f48754230fbbbc3379`.
- Original byte count: **126559**.
- SHA-256: `b6bd1e918d69f6ae2d6b7f02d3a97e3979cac7edf0af16130488dc5374d66491`.
- Run ID: `ACX-PROBE-20260930-01-1790786999423-396382`.
- Collector build: `ACX-PROBE-20260930-01`.
- Collector source: [ACX_Depth_Probe.jsx at 821b2ff](https://github.com/ios3kov/AAE-Developer-Bible/blob/821b2ff51d081754fa2ee8e3c3152dd988d76acf/scripts/ACX_Depth_Probe.jsx).
- Available collector file SHA-256: `095a533f086d081cbee65f29f4a19ced2d57869e5a2882e43d1e5bb933853a43`; its Git blob matches `2946873fc31665adeb4fd185d159567cd31b4ce4`.

The report identifies its collector by build string; it does **not** hash the executing script or the loaded Adobe binary. Matching the available collector file to Git is not a new runtime identity measurement. The original report remains a supplied evidence artifact; this document records its identity and derived results rather than reproducing all 1260 samples.

## Recorded environment

| Field | Report value |
|---|---|
| AE version / build | `25.6x101` / `101` |
| OS | `Macintosh OS 26.6.2/64` |
| Project | `3dextract.aep` |
| Project dirty at start | `true` |
| Source composition | `DEPTH_SOURCE` |
| Source renderer identifier | `ADBE Advanced 3d` |
| Project GPU setting | `1816` |
| Source resolution factor | `[1, 1]` |
| Initial project depth / Collapse | 8 bpc / OFF |
| Sample time | 0.84 seconds |
| Working space | `None` |
| Linearize working space / linear blending | false / false |
| Expression engine | `javascript-1.0` |
| Sampling | layer space; radius 0.5; postEffect=true |

Renderer and GPU identifiers are preserved literally, without inferring a UI renderer label, effect-level GPU execution or MFR. Because the project was already dirty, the filename does not establish that the live source exactly matched the previously uploaded AEP. The report does not capture complete source geometry or a live-project hash.

## Collection integrity

The full JSON was parsed and compared programmatically:

- All **28 distinct planned cases** are present: nine at each of 8/16/32 bpc, plus the 32-bpc Clamp OFF request.
- All records have status `RECORDED`; top-level status is `COLLECTED`.
- Each record contains the same ordered **45 sample points**, a 9-by-5 grid over 1920-by-1080 layer space: **1260 RGBA tuples** total.
- All returned RGBA components are finite numbers.
- Requested core settings match both before/after parameter readbacks and the recorded Collapse/effect-enabled flags. All 32-bpc clamp writes are reported as applied.
- Parameter readbacks are unchanged across sampling for every case. No case error or cleanup error is recorded.
- Reported collection elapsed time is **7260 ms**. This includes script activity and sampling; it is not a rendering benchmark.

These are report-integrity checks. They do not establish that each sample triggered uncached rendering, nor that every plug-in feature has been tested.

## Numerical findings

### 1. Baseline: three distinct depth levels

Baseline settings: Black 5000, White 0, Invert OFF, AA OFF, Collapse OFF, effect ON, Clamp stored ON.

| Project bpc | Outer sampled region | Middle sampled region | Central sampled region |
|---:|---:|---:|---:|
| 8 | 0.28627452254295 | 0.58823531866074 | 0.78823536634445 |
| 16 | 0.28997802734375 | 0.58999633789062 | 0.78997802734375 |
| 32 | 0.28999999165535 | 0.58999997377396 | 0.79000002145767 |

RGB components are equal. The three levels occur at 30, 12 and 3 grid locations respectively. The effect-disabled control returns colored source values, not these grayscale levels. The outer sampled region therefore must not automatically be described as empty background or an infinity sample.

Maximum baseline RGB difference from the 32-bpc samples is approximately **0.0037254691** at 8 bpc and **0.0000219941** at 16 bpc. These observations are consistent with output quantization, but they do not prove a universal rounding rule or bit-exact equivalence of all render paths.

### 2. Inversion and endpoint reversal

At every sampled point and each tested bpc, these two records have exactly equal serialized RGBA values:

- Black 5000 / White 0 / Invert ON;
- Black 0 / White 5000 / Invert OFF.

The maximum absolute RGB residual of `baseline + invert - 1` is:

| bpc | Maximum absolute residual |
|---:|---:|
| 8 | 0.00392153859139 |
| 16 | 0.00003051757813 |
| 32 | 0.0000000298023201 |

Thus reversal and inversion match exactly **within this recorded grid**, while complementarity has finite-precision differences. Do not describe the integer results as an exact arithmetic complement.

### 3. Equal endpoints

With Black = White = 1000, Invert OFF, Collapse OFF and Clamp stored ON, all 45 locations in each bpc return the same gray:

| bpc | Recorded R = G = B | Recorded alpha |
|---:|---:|---:|
| 8 | 0.50196081399918, approximately 128/255 | 1 |
| 16 | 0.5 | 1 |
| 32 | 0.5 | 1 |

This replaces the earlier screenshot-only estimate with numerical evidence for this specific equal-endpoint case. Other equal values, non-finite inputs and Clamp OFF combinations were not tested.

### 4. Clamp OFF in 32 bpc preserves values above one

Compare `narrow` and `clamp_off_request`: Black 1000, White 2000, Invert OFF, AA OFF, Collapse OFF, effect ON. Parameter 5 reads back 1 and 0 respectively, before and after sampling.

| Region | Clamp OFF, approximate | Clamp ON |
|---|---:|---:|
| Outer | 2.55 | 1 |
| Middle | 1.05 | 1 |
| Central | 0.05 | 0.05000000074506 |

**42/45 sample locations change.** At all sampled RGB components, Clamp ON is exactly equal to clipping the recorded Clamp OFF component into 0–1. The maximum pair difference is about 1.5499999523. No negative sample is present, so lower-bound behavior remains untested.

This is direct numerical evidence that the accepted script request can produce values above 1 in this nested-source run. An earlier blanket interpretation that nested output must always stay within 0–1 cannot be used to override these measurements. Script write acceptance, UI availability, source policy and observed pixels remain separate claims; no UI interaction is established by this batch.

### 5. Repeated baseline

At 8, 16 and 32 bpc, `baseline_repeat` has exactly the same 45 serialized RGBA tuples as the corresponding baseline, after intervening changes to parameters, Collapse and effect enablement.

This establishes repeatability of the sampled observations within one session. Cache invalidation, cold runs, restart behavior, multi-frame rendering and concurrent execution are not established.

### 6. Collapse changes the fixture result

`collapse_on` differs from baseline at **all 45 grid points** in each bpc. At 32 bpc its three gray levels are approximately **0, 0.266666651 and 0.466666639**, versus **0.29, 0.59 and 0.79** with Collapse OFF.

The maximum RGB difference is about 0.3254902065 at 8 bpc, 0.3233337402 at 16 bpc and 0.3233333826 at 32 bpc. ON and OFF observations must remain separate test states. This does not classify either configuration as a plug-in defect.

### 7. Anti-alias: no difference in the sampled grid

`narrow_aa` and `narrow` have identical RGBA samples at all 45 locations, at all three bit depths. The AA parameter reads back 1 and 0 as requested.

This is **not** evidence that anti-aliasing is broken or absent. The grid is not an edge-specific test and the report does not identify DPTH/DPAA callbacks. Edge behavior and channel identity remain OPEN.

### 8. Alpha, selector and parameter bounds

All 1260 returned alpha values are 1. This only establishes opacity at the sampled locations; source-color control is also opaque there. It does not test transparency preservation, partially covered edges or out-of-bounds pixels.

Parameter 1 reads back **1** throughout these Z-Depth cases. This is a scripting-value observation, not a runtime FourCC trace and not a mapping for the other seven channels.

The API reports Black/White bounds **-10000000 through +10000000**, popup bounds 1–8 and checkbox bounds 0–1. These are property metadata, not proof that endpoint writes were tested or that a visible slider spans the same range. Initial values are 5000/0, AA OFF, Clamp ON, Invert OFF; the batch did not perform a clean effect Reset, so these are not newly measured factory defaults.

## Acceptance update

The following scoped claims now have numerical user-run evidence: baseline response at three bpc; equal endpoints at 1000; inversion versus reversal; sampled 32-bpc upper clamping; changed Collapse result; same-session baseline repeatability; and parameter readbacks.

Still OPEN: edge-specific AA and DPTH/DPAA tracing; negative/HDR and non-finite edge inputs; missing-channel and datatype-mismatch behavior; source/bit-depth UI rules; remaining auxiliary channels and ID boundaries; transparency/ROI; raw frame exports and loaded binary identity; CPU/GPU/MFR; independent-implementation equivalence.

**Gate 8 and complete plug-in acceptance are not closed.** The result is a substantial numerical milestone, not a substitute for the remaining gates in [the runtime protocol](RUNTIME-ACCEPTANCE-MACOS-AE25.6.md).

## Reproduce the central comparisons from the original report

Run this Python 3 snippet in the directory containing the original returned `report.json`. Assertions check report integrity and the stated comparisons, not the entire native implementation.

```python
import hashlib
import json
import math
from pathlib import Path

raw = Path('report.json').read_bytes()
assert hashlib.sha256(raw).hexdigest() == 'b6bd1e918d69f6ae2d6b7f02d3a97e3979cac7edf0af16130488dc5374d66491'
r = json.loads(raw)
cases = {(c['bpc'], c['id']): c for c in r['cases']}
assert len(cases) == len(r['cases']) == r['plannedCases'] == 28
assert r['status'] == 'COLLECTED' and not r['cleanupErrors']
for c in cases.values():
    assert c['status'] == 'RECORDED'
    assert c['parametersBefore'] == c['parametersAfter']
    assert [s['point'] for s in c['samples']] == r['grid']['points']
    assert len(c['samples']) == 45
    assert all(len(s['rgba']) == 4 and all(math.isfinite(v) for v in s['rgba']) for s in c['samples'])

def values(bpc, name):
    return [s['rgba'] for s in cases[bpc, name]['samples']]

for bpc in (8, 16, 32):
    assert values(bpc, 'baseline') == values(bpc, 'baseline_repeat')
    assert values(bpc, 'invert') == values(bpc, 'reversed')
    assert values(bpc, 'narrow') == values(bpc, 'narrow_aa')
    print(bpc, 'equal:', sorted({v[0] for v in values(bpc, 'equal')}))
off = values(32, 'clamp_off_request')
on = values(32, 'narrow')
assert all(on[i][k] == min(max(off[i][k], 0), 1) for i in range(45) for k in range(3))
print('Clamp OFF levels:', sorted({v[0] for v in off}))
print('Report comparisons reproduced; full-effect acceptance remains open.')
```
