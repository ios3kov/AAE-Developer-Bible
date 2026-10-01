# 3D Channel Extract — edge sampling and frame export

Date: **2026-09-30**. **Collection reviewed; full-effect research remains incomplete; this is an ongoing atlas track and does not block core Bible editorial readiness. No new run requested.**

This page supersedes stale v01 NOT RUN statements, the failed half-frame proposal and the exactly-one-file assertion in [the historical version](https://github.com/ios3kov/AAE-Developer-Bible/blob/b9db3cd30fabb0c164a6dacf28674af304d5d403/21-BUILTIN-EFFECTS-REVERSE-ENGINEERING/3D-Channel/3D-Channel-Extract/EDGE-AND-RENDER-PROBE.md). Full methodology, hashes and corrections are in [the evidence audit](EVIDENCE-AUDIT-2026-09-30.md).

## Why the edge run existed

The first [28-case numerical report](NUMERICAL-OBSERVATIONS-2026-09-30.md) did not deliberately sample boundaries. The Edge collector added adaptive boundary samples and actual Render Queue exports. This was useful for nested-composition Z-Depth, not all auxiliary channels.

The source renderer identifier was recorded as `ADBE Advanced 3d`. The name alone is not proof of effect-level GPU execution. Geometry was not independently archived from the dirty live project; the uploaded AEP must not silently stand in for a live-project hash.

## Measurement contract

All AA comparisons use Black 5000, White 0, Invert OFF, Collapse OFF and effect ON; Clamp is requested ON at 32 project bpc. Edge discovery samples six scanlines at 16-pixel spacing, then up to 16 transition brackets at integer and quarter-pixel positions. Six paired records cover AA OFF/ON at 8, 16 and 32 project bpc.

`sampleImage(point,[0.5,0.5],true,time)` is alpha-weighted layer-space sampling, not an internal raw buffer. Fractional-position intermediates alone do not establish AA. The paired differences are the evidence. No observed difference would not prove that AA is absent.

Render Queue files include composition transforms and output-module processing. File coordinates and layer-space sample coordinates are not automatically equivalent. Project bpc and stored file precision must be checked separately.

## Reviewed host runs

| Build / suffix | Report status | Retained output |
|---|---|---|
| Edge v01 / 767655 | ERROR | six edge records; two TIFFs after DONE; exactly-one-file assertion failed |
| Edge v02 / 126368 | ERROR | six edge records; half-frame duration rejected before rendering |
| Edge v03 / 381415 | ERROR | six edge records; two TIFFs; old assertion remained |
| Edge v03 / 990482 | ERROR | another v03 run, not v04; same assertion |
| Edge v04 / 508263 | COLLECTED | six edge records; six exports containing twelve images |
| Mega v01 / 853739 | COLLECTED | same scoped depth evidence; its all-channel claim is withdrawn |

`COLLECTED` is an acquisition status, not final acceptance. All six reports contain empty cleanup-error lists, which is a recorded result rather than independent proof of the entire user project state.

The v02 duration change was incorrect: AE rejected 0.02 seconds below its one-frame minimum 0.04 seconds. v04 retains a full-frame request, validates every nonempty matching sequence member, and records all produced files instead of selecting one silently.

Two files do not demonstrate exact single-frame timing. Recorded start/duration readbacks were 0.319986979/0.04000651 seconds for a requested 0.32/0.04. Timing quantization is a supported explanation, not a universal AE rule. Sequence members must remain separately identified.

## AA findings recomputed from existing artifacts

Each run has 1342 paired locations at each depth, with 84 changed locations and no non-finite pairs. Maximum sampleImage RGBA differences:

| Project bpc | Maximum difference |
|---:|---:|
| 8 | 0.12549018859863997 |
| 16 | 0.12442016601562 |
| 32 | 0.12439665198325994 |

Repeated runs corroborate these observations but do not expand fixture coverage or identify DPTH/DPAA callbacks.

## Full image decode, not just a signature check

All 30 images in the six supplied ZIPs were decoded offline. Completed v04 and Mega collections each contain:

| Project bpc | Actual component storage | Size / planes |
|---:|---|---|
| 8 | TIFF unsigned 8-bit | 1920 × 1080 × 4 |
| 16 | PNG unsigned 16-bit, color type 6 | 1920 × 1080 × 4 |
| 32 | PSD 32-bit float, RGB mode, raw planar composite | 1920 × 1080 × 4 |

For both sequence members 00007 and 00008, in both completed collections, AA ON/OFF changes **3072 of 2073600 RGB pixels**. Maximum stored RGB differences are 45 at 8-bit, 11521 at 16-bit, and 0.16127513349056244 at float32. The changed bounding box is x=468–1451, y=263–816 inclusive. Fourth-plane difference is zero.

Within a case, the two sequence members have identical decoded pixels even where their file hashes differ. Corresponding v04/Mega decoded-pixel hashes also match. These are same-session/corresponding-output observations, not MFR, cold-cache or restart tests.

**Do not claim raw-buffer or cross-depth equivalence:** PSD RGB ranges approximately 0.05125763–0.56794423 while the layer-space 32-bit baseline samples range approximately 0.29–0.79. The pipeline difference needs isolation. Output/color processing is a hypothesis, not a proven cause. Same-format AA comparisons remain useful.

Four stored planes and an opaque fourth plane do not test transparent-source behavior. In particular, PSD template settings reported Channels=RGB; plane count alone must not become an alpha-preservation claim.

## Collector safety and validation boundaries

The reviewed Edge implementation duplicates only the outer comp, leaves source geometry read-only, never saves the original AEP, and restores project depth and queued-item flags in cleanup. It checks settings, output paths and signatures. It does not patch binaries, purge caches or claim a hardware execution path. These are code-contract statements; report cleanupErrors is the separate observation.

The historical 21 portable tests covered the original v01 orchestration using a mock host. They did not prove Adobe rendering. After v04 changed `file` to `files` and allowed multiple sequence members, the old test assertions became stale; the audit must not carry the old green result forward to an untested revision. Tests should explicitly cover valid multi-member output and corruption of any member.

## What is retained and what remains open

Retain the observed AA-dependent boundary change and decoded file identities/precision. Do not repeat the six AA cases merely to rename a collector.

Still OPEN: private FourCC tracing, loaded binary identity for each batch, single-frame timing identity, output-pipeline equivalence, transparent/ROI inputs, other auxiliary channels, controlled non-finite/ID data, real CPU/GPU/MFR comparisons and independent implementation equivalence. See [runtime acceptance](RUNTIME-ACCEPTANCE-MACOS-AE25.6.md). Mega v01 is [withdrawn](MEGA-PROBE.md).
