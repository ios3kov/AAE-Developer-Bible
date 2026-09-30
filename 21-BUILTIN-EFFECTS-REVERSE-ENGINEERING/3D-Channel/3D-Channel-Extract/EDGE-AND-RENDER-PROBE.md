# 3D Channel Extract — edge sampling and frame export

Date: **2026-09-30**. Gate 8 remains OPEN.

Build: **ACX-EDGE-20260930-01**. Implementation and portable tests are recorded; **execution of this new collector inside After Effects is NOT RUN**. This is a test artifact, not a production plug-in or a completed host-acceptance report.

Script: [ACX_Edge_Render_Probe.jsx](../../../scripts/ACX_Edge_Render_Probe.jsx). Portable tests: [test_acx_edge_render_probe.js](../../../scripts/test_acx_edge_render_probe.js).

## Why this run exists

The [previous numerical report](NUMERICAL-OBSERVATIONS-2026-09-30.md) contains 28 records and 1260 RGBA observations. Anti-alias ON/OFF did not differ on its 45-point grid. That grid did not deliberately sample object boundaries, and no raw frame export was performed. The existing results remain valid within their documented scope; this script does **not** repeat that 28-case matrix.

The prior report records the renderer identifier `ADBE Advanced 3d`. The new script records the actual current identifier and does not change the source renderer or silently substitute a different renderer. It does not infer a renderer name or effect-level GPU behavior from a project setting.

## Run once

Keep the existing `3dextract.aep` open, with `DEPTH_TEST` containing one 2D precomp layer and only `3D Channel Extract` on that layer. Use **File > Scripts > Run Script File** to run the JSX. No new scene is required. The playhead must be within the layer duration; the script records and uses the nearest valid frame-aligned time.

A unique `AE_Edge_Render_...` folder is created on Desktop. Return the **whole folder as ZIP**, including `report.json` and exported images. A PARTIAL or ERROR report is useful evidence: retain it instead of repeating the run or resetting the effect.

## Exact matrix

All measurements use Black 5000, White 0, Invert OFF, Collapse OFF, effect ON. Clamp is explicitly requested ON at 32 bpc. The disabled channel menu is never forced; Z-Depth value 1 is required and checked.

| Phase | Work |
|---|---|
| Edge discovery | At 32 project bpc and AA OFF, sample three horizontal and three vertical scanlines, at quarter/half/three-quarter positions, with 16-pixel spacing. |
| Edge selection | Select up to 16 adjacent-sample brackets whose maximum RGBA change exceeds 0.02. Record all discovery samples and selected brackets. |
| Paired edge measurements | Sample the selected brackets, plus two pixels on either side, at integer and quarter-pixel positions. Use exactly the same locations for AA OFF/ON at each of 8, 16 and 32 project bpc. Six records. |
| Native frame exports | Request one full-resolution frame with AA OFF and one with AA ON at each of 8, 16 and 32 project bpc. Six planned image exports through the Render Queue. |

No transition found is `BLOCKED_NO_TRANSITIONS`, not a successful anti-alias test. At most 16 brackets and six scanlines are examined; thin features or some edges may be missed. The script does not generate or alter geometry to manufacture an anti-alias difference.

## Sampling and export are different measurements

Edge observations use `sampleImage(point, [0.5,0.5], true, time)` in layer space. These are alpha-weighted area samples, including at fractional positions. An intermediate value at a fractional point does not itself prove renderer anti-aliasing. The report compares **paired** AA OFF/ON observations, retaining non-finite values explicitly. A zero difference is not proof that anti-aliasing is absent or broken.

Render Queue output is the full outer composition, including its layer transforms and output-module processing. It is not the plug-in's internal raw pixel buffer. Do not equate a layer-space sample coordinate with an output-file coordinate without accounting for the outer transform.

## Output-template handling

The script inspects up to 128 installed output-module templates by their actual `Format` and settings, rather than inventing a template name or trying to write the read-only Format setting. It prefers OpenEXR, then TIFF, PNG or Photoshop image formats. An 8-bit-only template is not silently used for 16/32-bit project output. For 32-bpc output it requires EXR or an explicitly floating/32-bit template; for 16 bpc it requires EXR or higher-capacity depth metadata.

**Project bpc and file precision are separate.** EXR may contain half-float or full-float components; template color-management, alpha and compression settings can affect the exported values. All available template settings and chosen render/output settings are retained. Full image decoding, channel depth, alpha representation, compression, dimensions, SHA-256 and numerical comparisons must be checked after the returned artifacts are available. File-format selection is not a claim of bit-exact or lossless output.

If a suitable image template is absent, that bpc export is `BLOCKED`, the template inventory is saved and edge observations are retained. No codec installation, template creation or preference mutation is attempted.

## Safety contract

- File-write permission is checked before project changes.
- Only a disposable duplicate of the outer composition is edited. The nested source, its renderer and geometry are read-only.
- The script does not save the AEP, close the project, purge caches, change preferences, modify plug-ins or run shell commands.
- Existing QUEUED items are temporarily disabled for export and restored in `finally`. DONE/other unqueued items are not toggled or re-rendered. A queued item with an existing status callback blocks export before its flags are changed.
- Only the script-owned Render Queue item may be queued at render start. There is exactly one output module and one requested frame.
- Output paths must remain inside the unique run folder. Crop/resize are disabled when exposed; unexpected readbacks stop export. Post-render import/replacement and source XMP are disabled.
- OutputModule is reacquired after changing its settings because the documented API can invalidate the old object.
- A stopped/failed render ends further export attempts. DONE alone is insufficient: the case also requires exactly one nonempty expected image with a matching signature. Signature screening is not a complete file decoder.
- Temporary queue items/composition are removed and original project bpc/queued flags restored. Cleanup failures produce ERROR. Temporary edits may still leave the project dirty; the original on-disk AEP is not overwritten.
- Checkpoints precede host calls. The 300-second limit is a soft between-call budget, not a watchdog capable of interrupting a hung AE.

## Acceptance after the returned report

Check parameter before/after readbacks, known Collapse state, paired coordinates, all finite/non-finite outcomes, cleanup and queue results. Decode every exported image and verify dimensions, precision and alpha before comparing AA variants or bpc outputs. Retain the selected source renderer and output pipeline in any conclusion.

`RECORDED`, `EXPORTED`, and top-level `COLLECTED` describe acquisition. They are **not** a verdict on every effect feature. This run does not close private DPTH/DPAA tracing, other auxiliary channels, controlled infinity/ID fixtures, MFR, cold-cache determinism, loaded-binary identity or independent-implementation equivalence. See the [full runtime protocol](RUNTIME-ACCEPTANCE-MACOS-AE25.6.md).

## Portable validation and identity

Source script introduced at `e9b512d1ecffdbed983275f1fb31451844465a28`; tests at `fbfe4d86a5b120c916af52b2538591d00fb61449`.

- Script Git blob: `415e3dbfa3fe132176817d954b7b071fe7088294`.
- Script SHA-256: `f4e27a52a446ccda1d19d8f13aec643fbae578586454c996fbca11cb5257621e`.
- Local Node 22.16: **21 portable orchestration/safety checks PASS** using `node scripts/test_acx_edge_render_probe.js`.
- The JSX parses as ECMAScript 3 using Node's bundled Acorn 8.14.1 after removing the Adobe `#target` directive.

The tests use a synthetic host/queue/filesystem and synthetic sample values. They exercise failure, cancellation, settings readback, stale output-module references, template absence, non-finite samples, output absence/corruption and state restoration. They do **not** simulate or verify Adobe's pixel algorithm. New collector host execution and actual frame decoding remain NOT RUN.

## API sources consulted

[OutputModule API](https://ae-scripting.docsforadobe.dev/renderqueue/outputmodule/) documents template enumeration/application, read-only Format access and object invalidation after settings changes. [RenderQueueItem API](https://ae-scripting.docsforadobe.dev/renderqueue/renderqueueitem/) documents render flags, statuses, time-span settings and settings readback. These sources inform the new automation code; they are not substituted for measurements of the user's fixture.


## Partial host run — 2026-09-30

Run `ACX-EDGE-20260930-01-1790789109165-767655` reached edge sampling successfully and then stopped during the first frame-export validation.

Preserved evidence identity:
- supplied ZIP: `AE_Edge_Render_ACX-EDGE-20260930-01-1790789109165-767655.zip`;
- report SHA-256: `0bd7ca686f6e4617ce07ea106bbd43951a2da6b261200a7a9cfc78ccf2c2d2a1`;
- report status: `ERROR`; cleanup errors: 0;
- six AA edge records are present, 1342 samples each;
- at each of 8/16/32 bpc, AA ON differs from AA OFF at 84/1342 sampled locations;
- maximum observed RGBA delta: 8 bpc `0.1254901886`, 16 bpc `0.1244201660`, 32 bpc `0.1243966520`.

This is positive runtime evidence that the Anti-alias switch changes Z-Depth output at deliberately sampled boundaries in this fixture. It does not by itself identify DPTH versus DPAA callbacks.

The first Render Queue item reached DONE, but AE emitted two TIFF sequence files (`frame_00007.tif` and `frame_00008.tif`) for the requested interval. The v01 collector expected exactly one file and correctly stopped rather than silently accepting ambiguous output. Both files were non-empty (8,313,088 bytes). Their SHA-256 values are `dab1c4123afab941051ed69a4ac749b5ea70bfded5e578113f96939e8d7bf4d9` and `2669082a4b639d9d9480dcb636094a4e22ea3188d3e2908218797885c2c0d4d1`.

Root cause: the requested duration equaled one composition frame while the recorded frame-aligned start/duration values straddled AE's Render Queue frame-boundary interpretation, so two sequence files were produced. Build `ACX-EDGE-20260930-02` uses a half-frame render duration after setting the aligned start; this preserves a single target frame while avoiding the boundary ambiguity. Host validation of v02 remains pending.
