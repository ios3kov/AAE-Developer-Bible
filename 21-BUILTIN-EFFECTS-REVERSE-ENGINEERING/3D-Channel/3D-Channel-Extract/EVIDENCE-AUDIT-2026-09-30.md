# 3D Channel Extract — evidence audit and acceptance correction

Date: **2026-09-30**. Reviewed snapshot: `b9db3cd30fabb0c164a6dacf28674af304d5d403`.

**Preserve original evidence; withdraw full-effect completion claims. No new After Effects run was performed for this audit.**

`COLLECTED`, `RECORDED` and `EXPORTED` describe acquisition, not plug-in-wide acceptance. The previous source and interpretations remain in [the frozen revision](https://github.com/ios3kov/AAE-Developer-Bible/tree/b9db3cd30fabb0c164a6dacf28674af304d5d403).

## Sources and method

Reopened the original 28-case `report.json`, all **six supplied Edge/Mega ZIPs**, and `Aux_Channel_Extract-analysis.txt`. Parsed every report, recomputed AA comparisons, decoded **all 30 supplied image files**, and calculated archive/report/file/decoded-pixel hashes. Original files were read without modification; no JSX or native code was executed.

TIFF: tifffile. PNG: OpenCV unchanged-depth decoding, BGRA reordered to RGBA. PSD: explicit header/section-length parsing of the supplied version-1 RGB, four-channel, uncompressed planar 32-bit composite. Unsupported PSD layouts fail. No ICC/display conversion is applied by the offline audit. File bytes and decoded pixels are hashed separately.

Original archives, report, AEP and dump, plus the analysis script and per-file manifest, are preserved together in the private Library at `AAE-Developer-Bible/Evidence/ACX_Evidence_Audit_20260930.zip`. Bundle SHA-256: `3e6e213b1865d54be8251b2ddd633905244e0e022e21437ed70d53360121eb22`. The bundle includes a longer audit narrative. It is not a new AE test run.

## 1. Retained scoped Z-Depth observations

The [28-case numerical analysis](NUMERICAL-OBSERVATIONS-2026-09-30.md) remains useful for the supplied **nested-composition fixture**. Recalculation confirms baseline equals baseline_repeat and invert equals reversed endpoints at all 45 recorded locations in each project depth.

| Check | 8 bpc | 16 bpc | 32 bpc |
|---|---:|---:|---:|
| Equal endpoints at 1000: observed gray | 0.50196081399918 | 0.5 | 0.5 |
| Maximum baseline + invert - 1 RGB residual | 0.00392153859139 | 0.00003051757813 | 0.0000000298023201 |

For the 32-bpc narrow range, Clamp ON exactly clips the recorded OFF RGB samples into 0–1. OFF includes approximately 0.05, 1.05 and 2.55. Negative-input clamping was not tested. Collapse ON/OFF observations remain separate.

These observations do not establish independently known source depth or bit-exact coverage of every render branch. The project was dirty: the uploaded AEP hash does not identify the exact live scene. Preserve renderer identifier `ADBE Advanced 3d` literally; do not infer its UI label or effect-level GPU execution.

## 2. AA evidence survives, including actual exported pixels

Each of the six Edge/Mega reports contains six paired edge records. Recalculation gives **84/1342 changed sample locations** per AA pair at each bpc; no non-finite components. Maximum RGBA differences are 0.12549018859863997, 0.12442016601562 and 0.12439665198325994 at 8/16/32 bpc respectively. Repetition is not additional coverage. Fractional sampleImage measurements do not identify DPTH/DPAA.

Both Edge v04 and Mega v01 contain twelve decodable images: AA OFF/ON at three depths, sequence members 00007 and 00008 for each export.

| Project bpc | Actual stored file | Dimensions | Planes |
|---:|---|---|---:|
| 8 | TIFF unsigned 8-bit | 1920 × 1080 | 4 |
| 16 | PNG unsigned 16-bit, color type 6 | 1920 × 1080 | 4 |
| 32 | PSD 32-bit float raw composite, RGB mode | 1920 × 1080 | 4 |

AA OFF/ON comparisons at the same bpc and sequence number reproduce these numbers in both archives and both sequence members:

| Project bpc | Changed RGB pixels / frame | Maximum stored RGB difference | Fourth-plane difference |
|---:|---:|---:|---:|
| 8 | 3072 / 2073600 | 45 | 0 |
| 16 | 3072 / 2073600 | 11521 | 0 |
| 32 | 3072 / 2073600 | 0.16127513349056244 | 0 |

Changed-pixel bounding box is x=468–1451, y=263–816 inclusive. This establishes an AA-dependent boundary-image change for this fixture, not the complete AA algorithm.

Sequence members 00007/00008 have identical decoded pixels within each record; TIFF/PSD file hashes can differ. All twelve corresponding v04/Mega decoded-pixel hashes match. These results do not establish cold-cache or concurrency behavior.

Two files do not pass an exactly-one-frame timing test. Requested start/duration were 0.32/0.04 seconds; readback was `0.319986979`/`0.04000651`. Timing quantization is a supported explanation, not a universal AE interval rule.

**Important export limitation:** PSD stored RGB spans approximately 0.05125763–0.56794423, whereas layer-space 32-bit baseline sampling spans approximately 0.29–0.79. These paths are not numerically equivalent. Output processing/color handling is a hypothesis to isolate, not a proven cause. Same-format AA pairs remain meaningful; cross-depth/raw-buffer equivalence stays OPEN.

The fourth plane is constant full-scale. This is not a transparency/ROI test. PSD settings report `Channels: RGB` despite four stored planes; header plane count alone does not prove transparent-source handling.

## 3. Collector errors versus effect errors

| Run suffix / build | Acquisition | Retained evidence | Meaning |
|---|---|---|---|
| 767655 / Edge v01 | ERROR | six AA records; two TIFFs | exactly-one-file assertion after DONE |
| 126368 / Edge v02 | ERROR | six AA records; no image | half-frame duration rejected before render |
| 381415 / Edge v03 | ERROR | six AA records; two TIFFs | old exactly-one-file assertion remained |
| 990482 / Edge v03 | ERROR | six AA records; two TIFFs | another v03 run, not v04 |
| 508263 / Edge v04 | COLLECTED | six AA records; twelve images | completed collection, not full acceptance |
| 853739 / Mega v01 | COLLECTED | six AA records; twelve images; capability records | depth retained; all-channel interpretation rejected |

All supplied reports record no cleanup errors; that is not independent verification of the user's entire post-run state. Half-frame changes, delivery of old builds and repeated AA collection caused avoidable reruns. They are process/collector defects, not new effect coverage.

## 4. Claims withdrawn / tests NOT RUN

- **All eight channels:** not accepted. Mega forced selectors 1–8 on a precomp. Accepted writes and black RGB at one center sample for 2–8 do not prove channel contents, availability, absence, datatype or an error contract.
- **Missing channel, dtype mismatch, ID boundaries:** not controlled tests. Mega returned explanatory constants under outer RECORDED wrappers. They are NOT RUN, not PASS.
- **Transparency/ROI:** no dedicated input/output test; exports record `Use Region of Interest: false`.
- **CPU/GPU/MFR:** no controlled comparison or effect-level execution evidence. `UNAVAILABLE_PUBLIC_SCRIPT_API` is an unsubstantiated limitation label, not proof that public MFR configuration is impossible.
- **Private FourCC and loaded binary during batches:** NOT MEASURED. Earlier LLDB sessions must not be silently attributed to later untraced runs.
- **Bit-exact independent implementation:** OPEN. There is no native-versus-independent output comparison.

Mega v01 is withdrawn as an acceptance runner. The previous source is preserved in Git history; its current entry point is a non-mutating withdrawal notice. No new host probe is issued in this audit.

## 5. Static corrections from the supplied dump

These are source-derived corrections, not new host observations. The [static map](FILTERMAIN-FUNCTION-MAP-MACOS-AE25.6.md) must use them:

1. At `0xB4FA`, reconstructed little-endian bytes are **00 26 15 18 1B 1E 21 24**, not the previously rotated sequence. Base `0x6644` means selector 1 reaches depth, 2 reaches OBID, then TEXR/NRML/COVR/BKCR/UNCP/MATR. The alleged UI/internal rotation was our byte-offset error.
2. Machine datatype literals are **UBT1** (`0x55425431`) and **UST2** (`0x55535432`), not UB1T/SU2T.
3. **UNCP is not established as a direct three-FLT4 copy.** Its comparison at `0x6854–0x6864` enters an UBT1 check at `0x6868–0x6878`, then component bytes and a fourth-byte exponent calculation at `0x6AE0–0x6B70`. Packed mantissa/exponent processing is supported; the complete external contract remains open. Both earlier simplified descriptions were too strong.
4. The indirect call through offset **0xF8** is not identified by the fact that it receives/returns floating values. Do not name it a conversion/clamp without matching SDK layout or runtime resolution.

Thus “core static reconstruction complete for all eight families” is withdrawn too. Symbol boundaries, captured identity and selected arithmetic remain retained observations.

## 6. External verification, separate from measurements

[Adobe's 3D Channel documentation](https://helpx.adobe.com/after-effects/desktop/apply-effects-and-animation-presets/list-of-effects/3d-channel-effects.html), reviewed 2026-09-30, documents nested depth extraction, its disabled channel popup, and the 32-bpc-only Clamp control. It also supports RPF/RLA and appropriately tagged OpenEXR; RPF/RLA is not the only possible source. A format name does not prove channel population. Do not replace the recorded accepted Clamp OFF behavior with a broader reading of documentation.

[Adobe PSD specification](https://www.adobe.com/devnet-apps/photoshop/fileformatashtml/) is the byte-layout reference for the existing composites. [Adobe automated rendering](https://helpx.adobe.com/after-effects/using/automated-rendering-network-rendering.html) and the maintained [scripting Application reference](https://ae-scripting.docsforadobe.dev/general/application/#appsetmultiframerenderingconfig) inform future MFR design; they are not execution evidence for this collector.

## 7. Gate before another user run

Preserve originals and hashes; never edit reports into PASS. Complete source-backed errata and callback identification from the existing dump. Prepare separate auxiliary footage with independently inventoried identifiers, datatypes, dimensions and known values, plus a separate missing-channel control. Define expected outputs/tolerances before testing. Keep nested Z-Depth, footage channels, output conversion and concurrency as separate suites within one package. Implement actual test bodies; NOT RUN/BLOCKED keeps its gate open even when collection completes. Review fixture coverage and portable tests before delivery. Do not rerun completed depth matrices for cosmetic changes.

**No user AE action is required now. Gate 8 remains OPEN.**

## Evidence hashes

| Original artifact | SHA-256 |
|---|---|
| 28-case report | `b6bd1e918d69f6ae2d6b7f02d3a97e3979cac7edf0af16130488dc5374d66491` |
| Uploaded AEP, not live-project identity | `c9d1a9f0b8175975b73b5a753bf2ada5e54955064132bf56710f9475290e581e` |
| Disassembly text | `b3a4ee460373966a1c8e414614861249a95bd2f3870c5a0f3536c5331f7118b4` |
| Edge v01 ZIP | `562734664b2d390f75b43b37dc8591ff04e9d18b8c84015289d52c478d00fe52` |
| Edge v02 ZIP | `d9f8e0fb986da61afa4a47c2b573d57832f53247e701a0e122b066d182cbc90b` |
| Edge v03 ZIP, 381415 | `d5a2e51791435b53b286ec6b7b350b1ba4f4fb21576d04ec2c34c58c7048f5ad` |
| Edge v03 ZIP, 990482 | `83dd240ae62f56440543247a47d45b49e801cc4c0214c4a19e178b1c76090880` |
| Edge v04 ZIP | `6764f77f8b8c1351e5ccb5f56d97f1e21bfddeca9b71fc2a41ade24c34e271df` |
| Mega v01 ZIP | `1cc7cbab1955481fd3543312080a90b221bf70fd6133f5e749609c2f96d16d1f` |
