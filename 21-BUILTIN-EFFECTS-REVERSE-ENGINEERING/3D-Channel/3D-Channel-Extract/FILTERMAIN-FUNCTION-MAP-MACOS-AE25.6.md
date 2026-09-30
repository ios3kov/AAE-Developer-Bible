# 3D Channel Extract — corrected static function map

Date: **2026-09-30**. Target capture: **AE 25.6.0.101, macOS arm64**.

**Status: partial static reconstruction; full algorithm and full-effect acceptance OPEN.**

This revision explicitly supersedes erroneous selector ordering, datatype spellings and UNCP claims in [the previous reconstruction](https://github.com/ios3kov/AAE-Developer-Bible/blob/b9db3cd30fabb0c164a6dacf28674af304d5d403/21-BUILTIN-EFFECTS-REVERSE-ENGINEERING/3D-Channel/3D-Channel-Extract/FILTERMAIN-FUNCTION-MAP-MACOS-AE25.6.md). History is retained there; see [the evidence audit](EVIDENCE-AUDIT-2026-09-30.md) for acceptance consequences.

## Sources and identity

Source: user-supplied `Aux_Channel_Extract-analysis.txt`, 256343 bytes, SHA-256 `b3a4ee460373966a1c8e414614861249a95bd2f3870c5a0f3536c5331f7118b4`; earlier LLDB transcripts establish loaded-module and function-boundary observations.

The capture records Adobe binary SHA-256 `412a6deefc1d7a710a9019b6a068180556417b0548d0703d34852bcd395dcab8`. This is a recorded identity, not a new hash of the binary loaded in every later probe.

Physical module: `/Applications/Adobe After Effects 2025/Plug-ins/Effects/Aux_Channel_Extract.plugin/Contents/MacOS/Aux_Channel_Extract`. This is adjacent to the application bundle, not inside its `Contents`. The initial absence hypothesis was based on too narrow a search.

The strings include match name `ADBE AUX CHANNEL EXTRACT`, category `3D Channel`, and suite `PF AE Channel Suite`. Their presence alone is not a complete loader/API contract. Chronology: [binary evidence](BINARY-EVIDENCE-MACOS-AE25.6.md).

## Retained observed function boundaries

Image-relative addresses, end exclusive; never reuse them as absolute runtime addresses or unverified file offsets.

| Function | Start | End |
|---|---:|---:|
| ACX_ReportErr | 0x4500 | 0x455C |
| ACX_Power2 | 0x455C | 0x45B0 |
| FilterMain | 0x45B0 | 0x64A4 |
| PF_CopyMultiByteStr | 0x64A4 | 0x6544 |
| RenderX<PF_Pixel16> | 0x6544 | 0x7B10 |
| RenderX<PF_Pixel8> | 0x7B10 | 0x90E0 |
| FillInAllParams | 0x90E0 | 0x9414 |
| HandleEvent | 0x9414 | 0x9D6C |
| IsEffectOnCompLayer | 0x9D6C | 0x9FB8 |
| HandleChangedParam | 0x9FB8 | 0xA418 |
| GetAEEffect_AUX_CHANNEL_EXT | 0xA428 | 0xA708 |
| PluginDataEntryFunction | 0xA7A8 | 0xA934 |

`FilterMain` has an inline float-output path in addition to the two named integer specializations. Absence of a named float specialization does not prove absent 32-bpc processing. Embedded C++ source filenames are not recovered C++ source contents.

## Command dispatch retained, distinct from channel selection

For command indices 0–24: table `0xB4C0`, base `0x4624`, target = base + 4 × uint16 entry. Larger unsigned values take the common return.

```text
0010 0023 01FC 004E 0060 01FC 01FC 01FC
01FC 01FC 01FC 0199 01FC 0000 0000 01B2
01FC 01FC 01FC 01FC 01FC 01FC 01FC 01C9
020F
```

Relevant targets: command 4 -> `0x47A4` parameter construction; 11 -> `0x4C88` named integer RenderX; 13/14 -> `0x4624` shared handler; 15 -> `0x4CEC` event handler; 23 -> `0x4D48`; 24 -> `0x4E60` including inline float processing. Exact SDK enum labels require the applicable header. Numeric command dispatch is not the popup channel dispatch below.

## Corrected channel selector table — reconstructed from captured bytes

At `0x6614–0x6640`, the 16-bpc specialization loads the selector, subtracts one, bounds-checks against 7, reads a byte at `0xB4FA + selector - 1`, and adds four times that byte to `0x6644`.

The captured constant dump uses little-endian 32-bit words. Reconstructing bytes **starting exactly at 0xB4FA** gives:

```text
00 26 15 18 1B 1E 21 24
```

The previous `26 15 18 1B 1E 21 24 00` was a one-byte displacement error. It does not demonstrate an unusual UI-to-internal translation.

| Selector | Table byte | Target | Constructed identifier |
|---:|---:|---:|---|
| 1 | 00 | 0x6644 | DPTH / DPAA, conditional |
| 2 | 26 | 0x66DC | OBID, initialized before dispatch |
| 3 | 15 | 0x6698 | TEXR |
| 4 | 18 | 0x66A4 | NRML |
| 5 | 1B | 0x66B0 | COVR |
| 6 | 1E | 0x66BC | BKCR |
| 7 | 21 | 0x66C8 | UNCP |
| 8 | 24 | 0x66D4 | MATR |

This corrected static order agrees with the localized popup and the numerical report's Z-Depth selector=1. It is not a runtime trace of private channel requests on every source.

The depth branch at `0x6644–0x6664` conditionally selects DPTH/DPAA from captured parameter/state fields. Checkbox interaction or changed AA pixels alone does not identify which private identifier was requested in a later untraced run.

## Parameters: retained mapping, bounded claim

`FillInAllParams` checks out indices 1–6 and copies data before check-in. Setup localization IDs and later scripting metadata support:

| Index | Name |
|---:|---|
| 1 | 3D Channel |
| 2 | Black Point |
| 3 | White Point |
| 4 | Anti-alias |
| 5 | Clamp Output |
| 6 | Invert Depth Map |

The report exposes Black/White API bounds -10000000 to +10000000. These are metadata, not endpoint-write tests. Recorded initial values are not an independently observed factory Reset. Source/bpc UI constraints and script write acceptance remain separate from pixel changes.

## Datatypes and arithmetic — corrected, not a finished implementation

Machine immediates spell **UBT1** (`0x55425431`), **UST2** (`0x55535432`) and **FLT4** (`0x464C5434`). Earlier UB1T/SU2T spellings are retracted. SDK enumeration names/layouts require independent header verification.

| Channel | Static evidence retained | What is not established |
|---|---|---|
| DPTH / DPAA | Float-sample path with range/invert/clamp branches | Complete special-value, anti-alias and host-callback semantics |
| OBID | UST2 check at 0x732C; unsigned halfword load and grayscale stores at 0x7428–0x7444 | Full observable ID boundary contract |
| TEXR | FLT4 check at 0x74FC; two float loads and calls through offset 0xF8, third color component zero | Identity of indirect callback and all edge conversions |
| NRML | FLT4 check at 0x6D20; three-component (v+1)*0.5-style visualization | Complete clamping/rounding/error behavior across paths |
| COVR | FLT4 check at 0x68DC; scalar load, indirect callback, grayscale stores at 0x699C–0x69BC | Do not call the unresolved callback a clamp/conversion by assumption |
| BKCR | UBT1 check at 0x7140; three byte components at 0x7238–0x7274 | General source/alpha/edge contract beyond those loops |
| UNCP | UNCP comparison at 0x6854–0x6864, UBT1 check at 0x6868–0x6878; component bytes and fourth-byte exponent handling at 0x6AE0–0x6B70 | NOT a proven direct three-FLT4 copy; exact packed encoding and corner cases remain open |
| MATR | UBT1 check at 0x7690; byte load and repeated halfword stores at 0x77C4–0x77D0 | Full cross-depth ID display contract |

**UNCP correction:** both the original “simple byte RGB /255” and the later “three direct FLT4 components” descriptions were too strong. The captured path decodes exponent-scaled byte components, then performs range-related arithmetic. A packed mantissa/exponent interpretation is supported; no exact external file layout is claimed here.

**Callback correction:** `blr` through the pointer at offset `0xF8` is unresolved in this audit. Its floating argument/return does not establish its name or semantics. Keep a symbolic callback in provisional pseudocode until the matching SDK structure or runtime target is verified.

`ACX_Power2`'s captured body repeatedly doubles/halves 1.0 and returns 1.0 for zero, supporting the previously reconstructed 2^n helper. This small helper result does not establish the whole UNCP algorithm.

## Acceptance boundaries

The dump, symbol map, numeric tables and selected arithmetic remain useful. Static data cannot be marked complete merely because every UI name has been assigned a row. Current status:

- [x] Captured code/constants/strings and recorded binary hash.
- [x] Corrected selector table recomputed from byte addresses.
- [x] Parameter index/name mapping corroborated by the supplied report.
- [ ] Complete source-backed 8/16/32 pseudocode and indirect callback identities.
- [ ] Controlled auxiliary-footage data for non-depth channels.
- [ ] Exact ID, missing-channel, non-finite and datatype-mismatch behavior.
- [ ] Independent implementation equivalence.

Nested-composition numerical observations are documented separately in [the runtime protocol](RUNTIME-ACCEPTANCE-MACOS-AE25.6.md) and [evidence audit](EVIDENCE-AUDIT-2026-09-30.md). They do not automatically confirm that all these static paths executed.
