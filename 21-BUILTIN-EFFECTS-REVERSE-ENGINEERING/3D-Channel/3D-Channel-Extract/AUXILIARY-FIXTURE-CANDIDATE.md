# Auxiliary input candidate — known data before another AE run

Date: **2026-09-30**. Build: **ACX-INPUT-20260930-01**.

**This is an input-fixture milestone, not a new AE acceptance runner. Do not install the candidate mapping or rerun the old Mega Probe.** The atlas investigation remains ongoing; this does not block core Bible editorial readiness. Original AEP, captured reports and existing results are unchanged.

## Decision and sources

Use small, uncompressed, single-part OpenEXR files as inspectable candidate input data. This avoids requiring the user to model or render another scene. It does **not** mean that OpenEXR names automatically become native auxiliary channels, nor that this replaces RPF/RLA coverage.

[Adobe's 3D Channel documentation](https://helpx.adobe.com/after-effects/desktop/apply-effects-and-animation-presets/list-of-effects/3d-channel-effects.html) explicitly supports tagged OpenEXR and describes `OpenEXR_channel_map.txt`. The map belongs next to the importer plug-in, **not next to each EXR**. Therefore simply sending a multi-channel EXR would repeat the earlier methodology error.

The historical importer source was reviewed at [fnordware/openexrAE, 8089d5257872522e51e80717353e707adc193a06](https://github.com/fnordware/openexrAE/tree/8089d5257872522e51e80717353e707adc193a06):

- [OpenEXR.cpp](https://github.com/fnordware/openexrAE/blob/8089d5257872522e51e80717353e707adc193a06/src/OpenEXR.cpp), `OpenEXR_Init`: loads the mapping at importer initialization; when the map has no entries, the explicit fallback adds only `Z -> DEPTH/FLOAT`.
- [OpenEXR_ChannelMap.cpp](https://github.com/fnordware/openexrAE/blob/8089d5257872522e51e80717353e707adc193a06/src/OpenEXR_ChannelMap.cpp): documents case-sensitive names, pipe-separated components, channel FourCCs and data codes. Relevant correct spellings are `UST2` and `UBT1`.
- `OpenEXR.cpp` auxiliary-buffer path: chooses FLOAT/UINT reading from the requested AE datatype and converts into byte/short buffers. An EXR storage type is **not** sufficient evidence of an AE buffer datatype. Merely changing a FLOAT plane to UINT is not a controlled native datatype-mismatch test.

This source is historical and is **not identified as the user's installed AE 25.6 importer**. Installed importer identity, actual map and semantic channel descriptors must be verified before accepting any channel test.

Byte-layout references: [OpenEXR file layout](https://openexr.com/en/latest/OpenEXRFileLayout.html) and [reference Python module](https://openexr.com/en/latest/python.html). The format documentation explicitly gives precedence to the reference library. Accordingly CI uses a separately implemented decoder, **OpenEXR 3.3.3**, in addition to the fixture's bounded byte reader. No upstream importer code is copied into the fixture generator.

## Artifacts and exact contents

All images are **64 x 32**, origin `(0,0)`, full data/display windows, uncompressed scanlines, unit sampling, FLOAT32 or UINT32 storage. Every 8 x 8 tile uses palette index `(x//8 + 3*(y//8)) % 8`; the shifted rows expose flips/transposes. The generated manifest includes full palettes, file hashes and every decoded plane's hash.

| File | Physical EXR planes | Purpose, not a host result |
|---|---:|---|
| `aux_known.exr` | 16 | RGBA plus data candidates for seven semantic mode families below |
| `rgba_only.exr` | 4 | Exactly the same RGBA as the opaque auxiliary image, with **no auxiliary planes**; separate missing-data control |
| `depth_specials.exr` | 5 | RGBA plus `Z = -Inf, -1, -0, +0, 1, +Inf, NaN, 10000`; keep nonfinite tests isolated |
| `alpha_depth.exr` | 5 | RGBA with zero/fractional/full alpha, RGB premultiplied by A, plus known finite Z |

These are **synthetic test inputs**, not measurements or outputs fabricated for Adobe. They need no 3D renderer and do not claim a physical scene interpretation.

### Semantic mapping candidate

| Intended mode | Physical planes | EXR storage | Proposed AE tag / buffer |
|---|---|---|---|
| Z-Depth | `Z` | FLOAT | `DPTH / FLT4` |
| Object ID | `objectID` | UINT | `OBID / UST2` |
| Texture UV | `acxU`, `acxV` | FLOAT | `TEXR / FLT4`, dimension 2 |
| Normals | `acxNX`, `acxNY`, `acxNZ` | FLOAT | `NRML / FLT4`, dimension 3 |
| Coverage | `acxCoverage` | FLOAT | `COVR / FLT4` |
| Background RGB | `acxBgR`, `acxBgG`, `acxBgB` | UINT values 0..255 | `BKCR / UBT1`, dimension 3 |
| Material ID | `materialID` | UINT values 0..255 | `MATR / UBT1` |

`OpenEXR_channel_map.CANDIDATE.txt` is documentation/configuration **for review**, not installed configuration. It deliberately does not have the filename automatically consumed by the importer. No existing map is replaced and no AE/global setting is modified.

**UNCP is deliberately not mapped.** The corrected dump shows byte/exponent processing; a three-float copy would misrepresent the unresolved external contract. DPAA, native datatype mismatch and the importer semantics of nonfinite values are also not qualified by these files.

### Known discriminating values

Object IDs: `0, 1, 255, 256, 32767, 32768, 65534, 65535`. Material IDs: `0, 1, 2, 127, 128, 253, 254, 255`. UV components differ. Normal vectors include the six signed axes and `(0.6,0.8,0)` / its negative. Background components are distinct. Fractional coverage and alpha are present.

Ordinary depth palette: `-1000, 0, 250, 1000, 2000, 3500, 5000, 7500`. This includes both sides of a 0..5000 mapping interval, unlike the earlier upper-clamp-only observation.

## What is verified and what is not

The generator uses only Python's standard library. It refuses an existing destination, validates generated bytes, then writes `manifest.json` last. Verification checks sizes, names, windows, offsets, row lengths, types, complete planes and hashes. It rejects unsupported flags/compression, path injection, corrupt payloads and overwritten map content. A successful byte check is explicitly **FILE_INPUTS_ONLY_NOT_AE**.

CI independently decodes **all four files / 30 planes / 61,440 scalar values** through OpenEXR 3.3.3 and compares every channel's native dtype, dimensions and little-endian pixel bytes, including nonfinite depth bits. `reference-validation.json` is written separately: the original manifest's `reference_reader=NOT_RUN` is not rewritten as historical evidence. Require the separate successful reference record before describing the input as reference-decoded.

Twenty portable regression tests cover content, orientation, ID boundaries, special values, transparency inputs, deterministic bytes, unsafe paths/names, existing destinations and corrupt files. They do not emulate the native effect.

All candidate artifacts keep `ae_importer_qualification=NOT_RUN` and `native_effect_acceptance=NOT_RUN`. A correct file plus proposed map is still not proof that AE exposes the intended buffers.

## Acceptance matrix prepared before host testing

1. **Importer qualification:** record importer path/version/hash and the actual mapping. Enumerate semantic channel type, datatype, dimension and representative raw samples via a suitable host auxiliary-channel readout. Verify these against this manifest, separately from final effect-image comparison. Wrong tags or dimensions block only that suite; black output is not an availability test.
2. **Controlled depth outputs:** after qualification, the previously supported finite-depth hypothesis predicts `(Z-5000)/(0-5000)` for Black 5000, White 0, Invert OFF; Clamp ON clips it. Predictions are `1.2, 1, .95, .8, .6, .3, 0, -.5` before clamping. Test these at 32 bpc before comparing quantized paths. No finite normalization equation is assigned to NaN/Inf.
3. **Other modes:** inputs, dimensions and source values are specified above. Complete the source-backed arithmetic/callback mapping before labeling pixel outcomes PASS. For normals, `(n+1)/2` is a hypothesis from the reconstruction, not a new measured result. ID rounding/scaling, packed UNCP and unknown callbacks remain OPEN.
4. **Output pipeline:** same time, known transforms, color/output settings and decoded precision must be established independently. The old PSD/sampleImage discrepancy prevents reusing a cross-depth equivalence criterion unmodified.
5. **Concurrency, ROI and errors:** these require actual test bodies and observable execution, not labels or constants. The four input files alone do not test GPU/MFR or ROI.

A future single package can contain separate suites, but it must not call all of them PASS merely because collection finished. No new user run is requested by this document.

## Reproduction (developer/CI, not an AE instruction)

```sh
python -m unittest discover -s scripts -p test_acx_fixture_candidate.py -v
python scripts/acx_fixture_candidate.py build /new/output/directory --source-commit <commit>
python -m pip install OpenEXR==3.3.3 numpy==1.26.4
python scripts/acx_fixture_candidate.py verify /new/output/directory --reference
```

The dedicated `ACX input qualification` workflow publishes only after reference validation. Generated EXR binaries are workflow artifacts, not vendored external samples. The generator, tests and this protocol are the reproducible source of the candidate.
