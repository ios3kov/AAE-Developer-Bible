# Auxiliary channel readout — contract and offline gate

Date: **2026-09-30**. Build: `ACX-CHANNEL-GATE-20260930-01`.

**Implemented: request generation and offline capture-content validation. Native collector, exact-SDK compilation, importer execution and native-effect acceptance are NOT RUN. No user AE run is requested.**

This milestone adds a prerequisite for the eventual combined test package. It does not replace the withdrawn Mega runner, install a map, or claim that the prepared EXRs have been imported by AE.

## Why another gate is necessary

The [input qualification](INPUT-QUALIFICATION-2026-09-30.md) established the actual EXR planes and their values using the independent OpenEXR reader. It did not establish the semantic tags, component types or buffers exposed by the user's installed importer. A popup write, a black rendered image, or an EXR header alone cannot bridge that gap.

The new implementation is [acx_channel_gate.py](../../../scripts/acx_channel_gate.py); its [regression tests](../../../scripts/test_acx_channel_gate.py) use explicitly synthetic packets. Both use the versioned fixture generator as the data oracle; they do not implement Adobe's effect algorithm.

## Public API basis — not a claim about the installed importer

The [Adobe C++ SDK guide, auxiliary-channel access](https://ae-plugins.docsforadobe.dev/effect-details/useful-utility-functions/#accessing-auxiliary-channel-data), reviewed 2026-09-30, documents channel-count enumeration, indexed and typed descriptor lookup, channel checkout, and mandatory checkin through `PF_ChannelSuite1`. Returned descriptor information is usable only when the lookup reports found. The documented checkout takes a requested datatype: the request, descriptor and returned buffer must therefore be recorded separately.

The **JSON protocol below is our proposed collector contract, not an Adobe ABI declaration**. It deliberately contains no guessed C++ offsets or struct sizes. A future native adapter must compile against the actual target SDK headers and use their definitions. Documentation alone is not an exact-header compile check. The guide's malformed datatype-size text is not used to size host structures.

The [candidate protocol](AUXILIARY-FIXTURE-CANDIDATE.md) contains the pinned historical importer-source analysis. That source is not identified as the loaded AE 25.6 importer. Its mapping/conversion behavior must not be silently promoted to a host observation.

## Capture transaction required of the native reader

1. Bind a new run ID to the built reader's SHA-256 and the fixture generator. Pin AE `25.6x101`, macOS arm64 as the first target. Preserve loaded-module identity and a read-only snapshot of the actual channel-map file, or an explicit missing-file observation.
2. Use a directly imported footage layer as input parameter 0, with no proxy, full resolution, origin `(0,0)`, and time `0/1`. Never force an auxiliary selector on a precomposition. Hash each source file before and after the collection.
3. Enumerate every indexed auxiliary descriptor with `PF_GetLayerChannelCount` and `PF_GetLayerChannelIndexedRefAndDesc`. Preserve the count, zero-based indexes, found flags and error codes. A failed enumeration is not a successful absence test.
4. Make each planned typed query through `PF_GetLayerChannelTypedRefAndDesc`. Preserve its descriptor separately from the index inventory. Do not choose arbitrarily between duplicate semantic tags.
5. Only for a compatible, present descriptor, request that same datatype via `PF_CheckoutLayerChannel`. Copy the bounded full buffer while it is checked out, accounting for row stride. Record source byte order, shape, component count and requested/returned types. The offline format is row-major, interleaved, little-endian hex **without row padding**, not a screenshot or RGBA effect output.
6. Call `PF_CheckinLayerChannel` after every successful checkout, including failures during serialization; release the acquired suite. A failed checkin or suite release cannot be hidden behind a BLOCKED channel.

These are implementation requirements, not completed calls. The native reader and integration into the future single-run package are the next work item. Collection must use SDK-permitted callbacks; no arbitrary-thread calls, pointer retention after checkin or binary patching are authorized by this document.

## Exact scope of the first gate

| File | Typed queries | Expected candidate input |
|---|---:|---|
| `aux_known.exr` | 7 | DPTH/FLT4/1, OBID/UST2/1, TEXR/FLT4/2, NRML/FLT4/3, COVR/FLT4/1, BKCR/UBT1/3, MATR/UBT1/1 |
| `rgba_only.exr` | 7 | The same semantic tags absent; ordinary RGBA intentionally matches the opaque auxiliary file |
| `depth_specials.exr` | 1 | DPTH/FLT4/1, including preserved signed zeros and nonfinite bit patterns |
| `alpha_depth.exr` | 1 | DPTH/FLT4/1; this is only an input-depth check, not effect transparency acceptance |

There are **16 planned typed checks**: nine full-buffer comparisons and seven absence comparisons. Their declared dimensions remain 64 x 32. Every expected source file SHA-256 is regenerated and bound to the request, so an edited manifest cannot silently replace the input oracle.

The finite palettes, asymmetric tile layout, ID extremes, distinct vector components and nonfinite values come from the previously reference-decoded files. Exact canonical bytes are the strict candidate qualification criterion. A difference, including NaN canonicalization, is reported for investigation; it is **not automatically an Adobe defect**. No new universal NaN or color-conversion rule is inferred.

UNCP and DPAA are not in this gate. Datatype-mismatch *effect behavior*, alpha rendering, ROI, GPU, MFR, timing and output conversion remain separate untested suites.

## JSON schema conventions

Schema identifier: `ACX_NATIVE_CHANNEL_READOUT_V1`. Reference implementation is the validator and tests, not an inferred schema from the old report.

A request contains the fresh `run_id`, `collector_sha256`, `target_host`, `fixture_build`, `fixture_generator_sha256`, the coordinate contract and the exact four-asset query plan. The built native reader must be pinned **before** creating a real request. The CLI has no option to emit synthetic host evidence.

A capture contains the same identity fields and these groups:

- `evidence_origin`: `NATIVE_HOST_CAPTURE`; `SYNTHETIC_TEST` is reserved for portable tests and is rejected by the normal CLI.
- `host`: actual `ae_build`, `os`, `os_family`, `architecture`.
- `importer`: `loaded_module_path`, `version`, `sha256`; `mapping` records `state`, inspected `path`, and UTF-8 `text` plus its SHA-256 when present. Snapshot text must not be newline-normalized.
- `assets`: unique known `name`, `file_sha256_before`, `file_sha256_after`, `source_kind`, `source_is_proxy`, `param_index`, rational `time`, `channel_count_error`, `channel_count`, complete `indexed` and `typed` records.
- Each index record contains its `index`, `error`, `found` and descriptor (`tag`, `dtype`, `dimension`, `name`). Each typed record contains its requested `tag`, `query_error`, `found`, descriptor, and any checkout/request/checkin fields.
- Each successful compatible checkout contains a `chunk`: datatype, component dimension, width/height, origin/scale, source byte order, host row stride, `encoding=interleaved-le-hex-no-padding`, complete `data_hex` and its SHA-256.
- `cleanup_errors` must be empty and `suite_release_error` must be zero.

Found-false records must not contain descriptors or pretend a checkout occurred. Failed checkouts must not contain bytes or a checkin. Error codes, dimensions, time and indexes are integers, not booleans or decimal approximations. JSON floats are unnecessary: actual floating values are preserved in the raw hex payload. Duplicate keys, nonstandard constants, oversized inputs, symlink JSON files and overwriting an existing output are rejected.

A map snapshot is configuration evidence, not proof that the running importer consumed it. A path and hash in JSON do not independently prove which executable was loaded. The reader's identity/capture method still needs review. **The gate validates packet content and consistency; it does not authenticate the truth of a self-reported packet.** Output always records `authenticity=NOT_AUTHENTICATED`.

## Result semantics

`MATCHED_BYTES` means the reported compatible raw buffer matches all expected canonical bytes. `MATCHED_ABSENCE` means a successful typed not-found query agrees with a complete index inventory for the known RGBA-only control. Neither status validates a native effect.

`BLOCKED` means the planned semantic channel cannot currently be qualified (not exposed, incompatible descriptor, or host query/checkout error). Other independent comparisons may be retained, but the overall result is `PARTIAL`. `MISMATCH` preserves the first differing byte/pixel/component and both hashes; it is not relabeled as missing data.

Malformed, stale, incomplete or contradictory packets and failed cleanup cause a nonzero error without writing a success result. The sole all-matching label is `MATCHED_CAPTURE_CONTENT`; there is no full-effect PASS. `native_effect_acceptance` always remains `NOT_RUN` and the uncovered suites stay in the result.

## Portable validation and delivery boundary

The current local implementation passes **41 synthetic protocol/regression tests**, plus all **20 existing input-generator tests**. Coverage includes old Mega rejection, stale runs/builds, wrong EXRs/proxies/precomps, duplicate/missing descriptors, type coercion, missing bytes, corruption despite updated hashes, swapped UV components, exact ID boundaries, signed-zero changes, error handling and resource-cleanup reporting. These are not native host tests.

The dedicated `ACX channel gate` CI job repeats these tests with Python 3.11, separately from the independent OpenEXR input job. Native collector compilation and execution stay NOT RUN until actually performed.

Developer commands (not user AE instructions):

```sh
python -m unittest discover -s scripts -p 'test_acx_channel_gate.py' -v
python -m unittest discover -s scripts -p 'test_acx_fixture_candidate.py' -v
# Only after a native reader binary is built and hashed:
python scripts/acx_channel_gate.py request /new/request.json --collector-sha256 <actual-binary-sha256>
python scripts/acx_channel_gate.py verify /new/request.json /returned/capture.json /new/result.json
```

Exit 0 means all reported channel-content checks match; exit 2 retains PARTIAL/MISMATCH; exit 1 means invalid input or I/O failure. Original request/capture files are never overwritten. Do not send the old Mega or the candidate mapping to the user as a substitute for the missing native reader.
