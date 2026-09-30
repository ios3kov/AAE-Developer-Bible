# Auxiliary input qualification — result, 2026-09-30

**File inputs verified. AE importer qualification and full-effect acceptance remain NOT RUN / OPEN. No user AE run is requested.**

This completes the offline input-construction milestone defined in [the candidate protocol](AUXILIARY-FIXTURE-CANDIDATE.md), not the host-channel milestone. No existing AEP, Adobe installation, channel map, preference or old report was changed.

## Reproducible identity

- Build: `ACX-INPUT-20260930-01`.
- Source snapshot: `563fda578aee59a558a1bd0672ede67e911963f4`.
- Generator Git blob: `9ba4d0eca8e7e6e731b3a36cbfd5eb6f1c6a901e`.
- [ACX input qualification run 36763022587](https://github.com/ios3kov/AAE-Developer-Bible/actions/runs/36763022587): **success**.
- Job `qualify-file-inputs`, ID `110050114113`: all steps completed successfully.
- [Immutable workflow artifact 11118894188](https://github.com/ios3kov/AAE-Developer-Bible/actions/runs/36763022587/artifacts/11118894188): `ACX-input-candidate-563fda578aee59a558a1bd0672ede67e911963f4`, 21,142 bytes.
- ZIP SHA-256: `7d59826e65a8eed875583572d3655835607b8f4d182f059931db5662fab43e2e`.
- The identical downloaded ZIP is preserved in the private Library at `AAE-Developer-Bible/Evidence/ACX_Input_Candidate_563fda5.zip`.

The downloaded artifact's digest was recomputed and matched GitHub's digest. Its manifest identifies the source snapshot above; the script and test source are included. The local bounded verifier also successfully rechecked the downloaded files. A local pre-commit development output is not substituted for this artifact.

## Executed checks

1. **20 portable regression tests passed locally and in CI.** These cover file structure, exact ID boundary values, asymmetric orientation, matching RGBA-only control, nonfinite bits, premultiplied transparency, deterministic encoding, overwrite refusal, invalid names/types, corrupt payloads and manifest/map tampering.
2. **OpenEXR 3.3.3 independently decoded all four EXRs.** CI used CPython 3.11.16 and NumPy 1.26.4. The comparison checks every plane's native datatype, dimensions and full little-endian pixel bytes, including signed zero and nonfinite input values.
3. **30 planes / 61,440 scalar values matched the prescribed inputs.** `reference-validation.json` records `status=PASS`, `reference=3.3.3`, and `scope=FILE_INPUTS_ONLY_NOT_AE`.
4. `manifest.json` is not retroactively rewritten: its initial `reference_reader=NOT_RUN` is superseded only by the separate reference validation record. Both records retain `ae_importer_qualification=NOT_RUN`.

| Input file | Planes | Scalar values checked | SHA-256 |
|---|---:|---:|---|
| `aux_known.exr` | 16 | 32,768 | `73936b5abfc437d1a4572c39adf218cc7778c0de0b428b7052f84310fb3cd882` |
| `rgba_only.exr` | 4 | 8,192 | `be6952b719b42699ad1b74d1f821bb4b2f6bb4043b7adf2fe76698a225ad5627` |
| `depth_specials.exr` | 5 | 10,240 | `ca9544c448fbb88ad704c07238050ea888df8e3d3730f338bc9b7ac33208230c` |
| `alpha_depth.exr` | 5 | 10,240 | `807f53cc78fb1f251fedb96118c02185dbe0fcbe1100a1fe41fa18515e7ad7f2` |

All four files are 64 x 32. Complete channel names, storage types, palettes and plane hashes are in the manifest. The seven proposed semantic families are depth, Object ID, UV, normals, coverage, background RGB and Material ID. **Physical file content is verified; those AE semantic mappings are not yet verified.**

## Limits and next gate

The candidate map is named `OpenEXR_channel_map.CANDIDATE.txt` and is **not installed**. Read the actual installed importer identity and existing mapping before considering any configuration change. A proposed map from historical source does not prove current importer behavior.

Before the next combined host test, qualify the auxiliary descriptors and representative raw channel samples delivered by AE against the manifest. Keep actual footage-layer tests separate from nested-composition Z-Depth. The RGBA-only file is an input missing-data control, not a completed missing-channel behavior test.

UNCP remains excluded until its external packed-byte/exponent contract is resolved. DPAA identity, datatype-mismatch delivery, ROI callbacks, output conversion and CPU/GPU/MFR still require their own observable test bodies. No full-effect check is marked PASS because these files decode correctly.

## Pipeline incident retained

The first workflow submission at `7b4771859ae3a0af05ed8f58d103fa2d6c4d0c46` was rejected before jobs ran: the YAML plain scalar contained `--only-binary=:all:` followed by a space. Local YAML parsing reproduced the syntax error. Commit `563fda578aee59a558a1bd0672ede67e911963f4` changed that command to a folded block; the workflow then passed. The failed run is not counted as a test execution.
