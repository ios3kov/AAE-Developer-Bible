# 3D Channel Extract — FilterMain and function map

Date: **2026-09-30**  
Host under investigation: **After Effects 25.6.0.101, macOS arm64**  
Status: **symbol boundaries and selector-table targets captured; render reconstruction in progress**

This supplements the chronological [binary investigation](BINARY-EVIDENCE-MACOS-AE25.6.md).

## Evidence and scope

Sources are the user's LLDB transcripts from this investigation:

- `Вставленный текст.txt`: complete `FilterMain` disassembly, followed by a repeated 250-instruction excerpt and a host backtrace.
- The subsequent memory read: 25 unsigned 16-bit selector-table entries.
- `Вставленный Markdown.md`: `image lookup` results, verbose symbol ranges, and the complete symbol table for the target module.

The names and addresses below are observations from those transcripts. Branch targets are arithmetic reconstructions from the captured table and dispatch instructions. No additional function bodies, source files, or SDK declarations are assumed to have been recovered.

## Physical module: correction to the initial search hypothesis

LLDB identifies a separate module at:

```text
/Applications/Adobe After Effects 2025/Plug-ins/Effects/Aux_Channel_Extract.plugin/Contents/MacOS/Aux_Channel_Extract
```

It is outside `Adobe After Effects 2025.app/Contents`, in the adjacent installation-level `Plug-ins` directory.

This supersedes the early working claim in the chronological investigation that the effect has no physical standalone plug-in. Searching only inside the application bundle did not establish absence from the installation. Hardcoded PiPL metadata and a separate loadable plug-in are not mutually exclusive.

Captured module slide/base for this LLDB session:

```text
0x170458000
```

Use the image-relative addresses below for documentation. Do not reuse session addresses after a restart without checking the current module mapping.

## Function boundaries

End addresses are exclusive. All addresses in this table are image-relative, not absolute file-byte offsets.

| Function | Start | End | Size |
|---|---:|---:|---:|
| `AE_AUX_CHANNEL_EXT::ACX_ReportErr` | `0x4500` | `0x455C` | `0x005C` |
| `AE_AUX_CHANNEL_EXT::ACX_Power2` | `0x455C` | `0x45B0` | `0x0054` |
| `FilterMain` | `0x45B0` | `0x64A4` | `0x1EF4` |
| `PF_CopyMultiByteStr` | `0x64A4` | `0x6544` | `0x00A0` |
| `AE_AUX_CHANNEL_EXT::RenderX<PF_Pixel16>` | `0x6544` | `0x7B10` | `0x15CC` |
| `AE_AUX_CHANNEL_EXT::RenderX<PF_Pixel8>` | `0x7B10` | `0x90E0` | `0x15D0` |
| `AE_AUX_CHANNEL_EXT::FillInAllParams` | `0x90E0` | `0x9414` | `0x0334` |
| `AE_AUX_CHANNEL_EXT::HandleEvent` | `0x9414` | `0x9D6C` | `0x0958` |
| `AE_AUX_CHANNEL_EXT::IsEffectOnCompLayer` | `0x9D6C` | `0x9FB8` | `0x024C` |
| `AE_AUX_CHANNEL_EXT::HandleChangedParam` | `0x9FB8` | `0xA418` | `0x0460` |
| `AE_AUX_CHANNEL_EXT::GetAEEffect_AUX_CHANNEL_EXT` | `0xA428` | `0xA708` | `0x02E0` |
| `PluginDataEntryFunction` | `0xA7A8` | `0xA934` | `0x018C` |

There are nine code-symbol matches for `AE_AUX_CHANNEL_EXT::`. This is a symbol inventory, not proof that all implementation logic is contained in nine non-inlined functions.

Compiler metadata also preserves these source filenames:

```text
AEFX_Aux_Channel_Extract.cpp
AEFX_Aux_Channel_ExtractUI.cpp
aux_channel_ext.pipl.cpp
```

These are source-file names embedded in symbol metadata; their source contents have not been recovered.

## Exact selector jump table

The disassembly compares the unsigned command value against `0x18`. Values above 24 take the common return path. For values 0 through 24, dispatch performs:

```text
table = image + 0xB4C0
branch_base = image + 0x4624
target = branch_base + 4 * uint16_table[command]
```

Captured table, in command order:

```text
0010 0023 01FC 004E 0060 01FC 01FC 01FC
01FC 01FC 01FC 0199 01FC 0000 0000 01B2
01FC 01FC 01FC 01FC 01FC 01FC 01FC 01C9
020F
```

| Command index | Table entry | Image-relative branch target | Direct observation / interpretation |
|---|---|---|---|
| 0 | `0x0010` | `0x4664` | Resource/string callback path. |
| 1 | `0x0023` | `0x46B0` | Resource setup and output-field initialization path. |
| 2 | `0x01FC` | `0x4E14` | Common return path. |
| 3 | `0x004E` | `0x475C` | Resource/handle cleanup path. |
| 4 | `0x0060` | `0x47A4` | Repeated parameter-description construction and host callbacks; parameter-setup interpretation. |
| 5–10 | `0x01FC` | `0x4E14` | Common return path. |
| 11 | `0x0199` | `0x4C88` | Dispatches to the named `RenderX<PF_Pixel8>` or `RenderX<PF_Pixel16>` implementation. |
| 12 | `0x01FC` | `0x4E14` | Common return path. |
| 13, 14 | `0x0000` | `0x4624` | Calls `HandleChangedParam`; both indices share this branch. |
| 15 | `0x01B2` | `0x4CEC` | Tail-calls `HandleEvent`. |
| 16–22 | `0x01FC` | `0x4E14` | Common return path. |
| 23 | `0x01C9` | `0x4D48` | Request/rectangle preparation and an indirect host callback. |
| 24 | `0x020F` | `0x4E60` | Buffer acquisition and bit-depth-dependent processing, including an inline float-processing path. |

These numeric indices are established by the machine code. Exact `PF_Cmd_*` enum labels must be checked against the applicable SDK header before publishing a header-verified selector map. Sharing a handler does not make two selectors semantically identical.

## What FilterMain already establishes

The supplied disassembly directly names calls to `FillInAllParams`, `HandleChangedParam`, `HandleEvent`, and the two `RenderX` specializations. It also contains acquisition of `PF AE Channel Suite`, version 1.

For command 24, a 16-bit field read from the extra input structure is compared with 16 and 32. The 16 case calls `RenderX<PF_Pixel16>`; the remaining non-32 case calls `RenderX<PF_Pixel8>`. The 32 case executes substantial processing inside `FilterMain` itself, with float arithmetic and 16-byte output-pixel strides.

Consequently, the absence of a separately named `RenderX<PF_PixelFloat>` symbol is not evidence of absent 32-bit processing. Inspecting only the two named `RenderX` functions would omit the inline path.

Already visible arithmetic includes a three-component `(component + 1) * 0.5` conversion, byte-component division by 255, and unsigned-16-to-float replication. Their exact parameter/channel semantics and edge cases remain reconstruction work; those observations are not a complete algorithm specification.

## Capture corrections

The earlier `image dump symtab Aux_Channel_Extract | grep ...` command did not pipe its output. LLDB treated `|`, `grep`, and the pattern as additional module arguments and issued matching warnings. The preceding symbol-table output remains useful evidence.

For the next static capture, use an ordinary shell, not the `(lldb)` prompt. The confirmed physical module path allows disassembly without starting another After Effects process. Capture the full code, constants, and identity together rather than repeatedly copying overlapping console excerpts.



## Static binary capture milestone — 2026-09-30

A complete shell capture of the target arm64 binary is now available as `Aux_Channel_Extract-analysis.txt`. The capture contains SHA-256 identity, full `__TEXT,__text` disassembly, `__TEXT,__const`, and `__TEXT,__cstring`.

Captured binary SHA-256:

```text
412a6deefc1d7a710a9019b6a068180556417b0548d0703d34852bcd395dcab8
```

### OBSERVED — binary identity and registration

The binary contains:

```text
Plug-Ins/Effects/Aux_Channel_Extract
ADBE AUX CHANNEL EXTRACT
ADBE_AUX_CHANNEL_EXTRACT
3D Channel
```

`GetAEEffect_AUX_CHANNEL_EXT` constructs the effect registration metadata. This is direct static evidence that the physical module participates in registration of the native effect. It does not by itself document the complete host loader contract.

### OBSERVED — user-visible channel modes

The localization strings enumerate exactly eight menu entries, in this order:

1. Z-Depth
2. Object ID
3. Texture UV
4. Surface Normals
5. Coverage
6. Background RGB
7. Unclamped RGB
8. Material ID

The constant block also contains eight four-byte channel identifiers:

```text
DIBO RXET LMRN RVOC RCKB PCNU RTAM
```

The byte order visible in an `otool` word dump must be decoded before publishing a final SDK four-character-code mapping. The eight-entry UI list and the eight-way machine-code dispatch are observed; the exact identifier-to-SDK-name mapping is still reconstruction work.

### OBSERVED — parameters and diagnostics

The binary contains user-visible labels:

```text
Black Point
White Point
Anti-alias
Clamp Output
Invert Depth Map
```

and diagnostics including:

```text
Cannot acquire multi-channel suite.
Channel not available.
Datatype mismatch
Plus Infinity
Minus Infinity
```

These establish feature/diagnostic presence. Defaults, numeric ranges, enable/disable rules and precise per-channel semantics still require parameter-setup decoding or controlled host observation.

### OBSERVED — channel access

The render code acquires:

```text
PF AE Channel Suite
```

and uses its callbacks before channel-dependent processing. This directly supports the architectural statement that auxiliary data is requested through AE's channel-suite interface rather than being inferred solely from ordinary RGBA input pixels.

Other suite-name strings in the binary include AEGP PF Interface, Layer, Item, Project, PF Param Utils and PF AE Adv App suites. String presence alone is not proof that every suite participates in every render path.

### PROVEN — ACX_Power2

The complete body of `AE_AUX_CHANNEL_EXT::ACX_Power2(char)` is captured. It starts at image-relative `0x455C` and ends at `0x45B0`.

The positive branch starts at 1.0 and repeatedly doubles. The negative branch starts at 1.0 and repeatedly halves. Zero returns 1.0. Therefore, for the representable signed-char input domain:

```text
ACX_Power2(n) = 2^n
```

This helper is no longer an inference from its symbol name.

### OBSERVED — render architecture

The static capture confirms the previously observed function boundaries:

- `RenderX<PF_Pixel16>` at `0x6544..0x7B10`
- `RenderX<PF_Pixel8>` at `0x7B10..0x90E0`
- `FillInAllParams` at `0x90E0..0x9414`

The command-24 path in `FilterMain` contains a separate inline 32-bpc float-processing path. Therefore the absence of a named `RenderX<PF_PixelFloat>` symbol must not be interpreted as absence of float rendering.

The code also shows an eight-way channel selection and constructs channel identifiers before acquiring/using the channel suite.

### OBSERVED — visible conversion primitives

The captured machine code contains, in channel-dependent paths:

- byte-component conversion to float using division by 255;
- unsigned-16 conversion to float;
- a three-component `(component + 1) * 0.5` transformation;
- float comparisons between the two range values before processing.

These are implementation observations, not yet a complete per-channel specification. They must be attached to exact channel cases before the Bible claims semantic equivalence.

### INFERRED / not yet promoted to fact

The following are plausible from the structure but remain intentionally unpromoted:

- which four-character identifier corresponds to each of the eight UI modes;
- which visible conversion primitive belongs to every named mode;
- exact anti-alias behavior;
- exact Black/White Point normalization formula for every channel;
- behavior when Black Point equals White Point;
- complete meaning of range reversal;
- exact alpha policy;
- exact clamp ordering;
- CPU/GPU/MFR behavior.

### UNKNOWN / requires host fixtures or deeper decoding

- exact parameter defaults and legal ranges;
- parameter enable/disable dependencies;
- exact output for missing channels and datatype mismatch in every render path;
- byte-for-byte/pixel-for-pixel equivalence across 8/16/32 bpc;
- interaction of Invert Depth Map with Black/White Point and Clamp Output;
- performance and concurrency characteristics.



## Parameter checkout map from FillInAllParams

The complete `FillInAllParams` body is now decoded far enough to establish its checkout contract.

It performs six host parameter checkouts, using indices **1 through 6**, and checks each one back in after copying the returned `PF_ParamDef` data into a contiguous local aggregate used by the render/event code.

The parameter-setup branch independently requests localized strings in this order:

| Effect parameter slot | Localization ID | Observed label |
|---:|---:|---|
| 1 | 1 | `3D Channel` |
| 2 | 8 | `Black Point` |
| 3 | 9 | `White Point` |
| 4 | 20 | `Anti-alias` |
| 5 | 21 | `Clamp Output` |
| 6 | 22 | `Invert Depth Map` |

This gives a direct parameter-slot mapping, not merely a list of strings found in the binary.

`FillInAllParams` itself does not establish the human meaning of every copied field. Exact defaults, numeric limits and UI enable/disable dependencies still require decoding the setup structures and/or host observation.

## Channel selector dispatch decoded

The render functions load the channel selector, subtract one, and dispatch through an eight-entry byte jump table at image-relative `0xB4FA`. The table bytes are:

```text
26 15 18 1B 1E 21 24 00
```

with branch base `0x6644` in the 16-bpc specialization. This establishes the following **stored-selector-value → machine channel identifier** map:

| Stored selector value | Branch | Identifier integer | ASCII FourCC |
|---:|---:|---:|---|
| 1 | fall-through to `0x66DC` | `0x4F424944` | `OBID` |
| 2 | `0x6698` | `0x54455852` | `TEXR` |
| 3 | `0x66A4` | `0x4E524D4C` | `NRML` |
| 4 | `0x66B0` | `0x434F5652` | `COVR` |
| 5 | `0x66BC` | `0x424B4352` | `BKCR` |
| 6 | `0x66C8` | `0x554E4350` | `UNCP` |
| 7 | `0x66D4` | `0x4D415452` | `MATR` |
| 8 | `0x6644` | conditional | `DPTH` or `DPAA` |

The depth branch selects between `DPTH` and `DPAA` using additional parameter/state tests before joining the common channel-acquisition path.

This table is **PROVEN for the stored selector values used by the machine code**. It must not yet be rewritten as a final UI-order table: the localized eight-name string is stored as `Z-Depth|Object ID|Texture UV|Surface Normals|Coverage|Background RGB|Unclamped RGB|Material ID`, while the machine selector values above place the depth path at stored value 8. The UI/value translation needs one more setup/host check before those two representations are reconciled.

### Identifier interpretation status

The following semantic readings are strongly supported by both their FourCC spelling and the localized mode inventory:

- `OBID` — Object ID
- `TEXR` — texture-related channel
- `NRML` — Surface Normals
- `COVR` — Coverage
- `BKCR` — Background RGB/color
- `UNCP` — Unclamped RGB/color
- `MATR` — Material ID
- `DPTH` / `DPAA` — depth variants

The Bible keeps the machine identifiers and UI labels separate until the exact host/API mapping is independently tied down.

## Render case tree: first exact branches

The 16-bpc renderer compares the acquired channel identifier and channel datatype before entering specialized loops. The static capture already proves several structural facts:

- channel acquisition happens before pixel iteration;
- a channel-availability flag is tested and a missing/unavailable channel exits the processing path;
- channel datatype is checked before a specialized conversion loop;
- the output loop writes 16-bit AE pixels with an 8-byte stride;
- some branches explicitly fill output alpha while channel data populate RGB;
- depth/range values are converted to float and ordered with `min/max`-style floating comparisons before channel processing;
- `UNCP`, `COVR`, `OBID`, `TEXR` and the remaining identifiers enter distinct conversion blocks rather than one generic RGB-copy routine.

The exact arithmetic of each block is being reconstructed next. Until that is complete, these structural observations should not be summarized as a single universal normalization formula.

## Updated reconstruction workflow

The static-capture milestone is complete. The next reconstruction pass should work from the captured file rather than collecting more overlapping LLDB excerpts:

1. ~~decode `FillInAllParams` and parameter setup into a parameter-index table;~~ **Complete for slots 1–6; defaults/ranges remain.**
2. ~~decode the eight channel-case targets and four-character identifiers;~~ **Complete for stored selector values; UI/value translation remains.**
3. annotate the 8-bit and 16-bit functions side-by-side;
4. annotate the inline 32-bpc path;
5. derive pseudocode only after each arithmetic block has a channel identity;
6. validate edge cases with controlled AE fixtures;
7. promote only host-confirmed/reproducible behavior to algorithm-equivalence claims.


## Next acceptance criteria

1. ~~Capture both complete `RenderX` bodies and `FillInAllParams`, preserving function boundaries.~~ **Complete in the static binary capture.**
2. ~~Decode `ACX_Power2`.~~ **Complete: `2^n` for signed-char `n`.**
3. Associate parameter indices and channel-table cases with evidence before naming their UI semantics.
4. Write separate pseudocode for the 8-bit, 16-bit, and inline 32-bit paths, including missing-channel handling, range reversal, equal limits, clamping, and alpha writes.
5. Validate reconstructed pixel behavior against controlled host fixtures before claiming algorithm equivalence.

This milestone records the function map and dispatch evidence only. Algorithm equivalence and performance have not been tested.
