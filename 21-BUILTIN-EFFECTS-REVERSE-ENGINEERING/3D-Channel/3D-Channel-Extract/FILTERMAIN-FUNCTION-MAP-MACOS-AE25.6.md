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



## Cross-bit-depth render reconstruction

The three render implementations now line up strongly enough to document several channel formulas. The claims below are restricted to arithmetic directly visible in the captured binary; where a channel datatype name has not been independently resolved from the SDK, the machine FourCC is used.

### NRML — normal visualization

**PROVEN arithmetic:** the float path reads three float components and writes each RGB component as:

```text
out = (component + 1.0) * 0.5
```

The 16-bpc path performs the equivalent mapping into the AE 16-bit pixel domain. The output alpha is filled opaque for valid output pixels.

This is consistent with visualization of signed normal components in [-1,+1], but the range statement is semantic interpretation; the transform itself is machine-code evidence.

### BKCR — background RGB

**PROVEN conversion shape:** the channel is accepted in an 8-bit three-component form. Each source byte is converted to float and divided by **255.0** in the float-output path. The 16-bpc path scales the same byte components into the AE 16-bit output domain. RGB components are copied independently; alpha is filled opaque.

Conceptual float pseudocode:

```cpp
out.a = 1.0f;
out.r = src.r / 255.0f;
out.g = src.g / 255.0f;
out.b = src.b / 255.0f;
```

### COVR — coverage

The renderer has a dedicated COVR branch and requires a float channel datatype before processing. It is not routed through the byte-RGB or normal-vector conversion blocks.

The exact scalar-to-output formula still needs a clean isolated extraction before promotion to pseudocode.

### OBID — Object ID

The dedicated OBID branch requires a two-byte unsigned channel representation. The value is replicated to R, G and B, producing a grayscale visualization, with opaque output alpha.

The exact display scaling/wrapping behavior at all integer values should still be verified with fixtures before claiming a user-level formula.

### TEXR — texture coordinates

The TEXR branch requires a float channel representation. In the float-output path it reads two float components, applies the host float conversion callback to each, writes them into two color components and explicitly writes the remaining color component as zero; alpha is opaque.

This proves a two-component UV-style visualization structure. Exact R/G component ordering is intentionally left for fixture verification rather than inferred from register offsets alone.

### UNCP — unclamped color

**Superseded by the full branch pass below:** UNCP is a three-component `FLT4` path, not byte RGB. See **Coverage and Unclamped RGB resolved**.

### MATR — Material ID

MATR has its own branch and datatype check rather than sharing the OBID dispatch. It produces a visualization from a scalar identifier. Exact integer conversion/scaling is still being isolated before publishing a formula.

### DPTH / DPAA — depth

Depth is the most elaborate path and is shared by two machine identifiers, `DPTH` and `DPAA`. Both require a float channel datatype.

The code:

1. converts Black Point and White Point to float;
2. orders them into low/high values for clipping;
3. uses the Invert Depth Map state to select which endpoint is treated as the output start/end;
4. computes a range difference;
5. reads a float depth sample;
6. optionally clamps the sample to the ordered range when Clamp Output is active;
7. for ordinary finite values, computes a normalized scalar from the sample and the selected endpoint/range;
8. replicates that scalar to R, G and B;
9. writes opaque alpha.

The finite-value core visible in the float path is equivalent in structure to:

```cpp
range = mapped_white - mapped_black;
value = depth;
if (clamp_output)
    value = clamp(value, min(black, white), max(black, white));

if (range != 0)
    gray = (value - mapped_black) / range;
else
    gray = fallback;
```

The binary also contains explicit handling for very large positive/negative float values and a separate fallback for a zero/degenerate range. Therefore the simplified pseudocode above is **not yet a complete bit-exact specification**.

### 8 / 16 / 32 consistency

The captured implementations show the same channel decision tree repeated across:

- inline 32-bpc float output in `FilterMain`;
- `RenderX<PF_Pixel16>`;
- `RenderX<PF_Pixel8>`.

The principal differences are output-domain conversion and pixel stride:

- 32-bpc: float RGBA;
- 16-bpc: AE 16-bit integer RGBA;
- 8-bpc: byte RGBA.

This is strong static evidence of one conceptual auxiliary-channel algorithm implemented for three output depths, rather than three unrelated algorithms.



## Additional exact formulas: byte RGB, UV, scalar-ID and datatype contracts

A second cross-bit-depth pass resolves several previously open conversion details.

### BKCR / byte RGB path

The 8-bpc renderer's byte-RGB branch copies three adjacent source bytes directly into output RGB and writes output alpha = 255.

The 16-bpc counterpart reads the same three byte components and maps them into AE's 16-bit domain using the float conversion visible in the function. The 32-bpc path divides by 255.0.

This confirms that the byte-RGB family is a direct component visualization, not a luminance conversion.

### TEXR / two-float path

The 16-bpc TEXR block requires datatype FourCC `FLT4`, reads two consecutive 32-bit floats, converts each through the host float conversion callback, writes the two converted values to two output color components, explicitly writes the third component as zero, and writes opaque alpha.

The 32-bpc block has the same two-component shape. The remaining uncertainty is only the human R/G naming of the two destination offsets; the arithmetic and zero third component are established.

### OBID datatype and visualization

The OBID block checks datatype FourCC `SU2T` and reads one unsigned 16-bit source value. In the 16-bpc renderer the scalar is transformed and then replicated to all three output color components. The 32-bpc path converts the unsigned-16 scalar to float and likewise replicates it.

This establishes **scalar → grayscale RGB**. The exact user-visible wrap/bias rule for the 16-bit integer display still deserves a fixture because the machine code contains a conditional integer adjustment around the half-range boundary.

### MATR datatype and visualization

The MATR block checks datatype FourCC `UB1T`, reads one source byte, and replicates that value to R, G and B. The 8-bpc renderer does this directly; the 16-bpc renderer stores the scalar into each 16-bit color component; alpha is opaque.

Thus Material ID is also rendered as grayscale, but it has a different source datatype from Object ID.

### NRML datatype

The normal branch checks datatype FourCC `FLT4`. This is consistent across the render implementations and supports the already reconstructed three-float normal visualization.

### Depth datatype

Both `DPTH` and `DPAA` converge on a branch that checks `FLT4` before the depth loop. The Black/White range and invert logic therefore operate on float auxiliary samples.

### Missing datatype path

When the acquired channel datatype does not match the expected FourCC, the render functions enter a shared error path that requests localized diagnostic ID 7 (`Datatype mismatch`), sets the host error-message flag, and returns an error status rather than silently reinterpreting the bytes.

This behavior is now static-code evidence.



## Coverage and Unclamped RGB resolved

The remaining major channel branches can now be separated correctly.

### COVR — Coverage

The COVR branch requires `FLT4`. It reads a single 32-bit float auxiliary sample, passes it through the host float conversion callback used elsewhere by this effect, and **replicates the resulting scalar to R, G and B**. Alpha is opaque.

Cross-depth structure:

```cpp
coverage = host_float_convert(src_float);
out.a = opaque;
out.r = coverage;
out.g = coverage;
out.b = coverage;
```

The 8- and 16-bpc implementations perform the corresponding conversion into their integer output domains.

The localization string `Coverage %.2f` independently confirms that Coverage is treated as a scalar value by the effect UI/event path. This closes the previously open Coverage formula at the structural level.

### UNCP — Unclamped RGB correction

Earlier notes classified UNCP with the byte-RGB family. The full branch analysis corrects that.

UNCP requires `FLT4` and reads **three float components**. Each component is converted independently through the host float conversion callback and written to RGB; alpha is opaque.

Conceptually for 32-bpc output:

```cpp
out.a = 1.0f;
out.r = host_float_convert(src[0]);
out.g = host_float_convert(src[1]);
out.b = host_float_convert(src[2]);
```

The 8/16-bpc paths then quantize/scale those converted float values into their output domains. This matches the localization format `Unclamped Color %.1f %.1f %.1f`.

Therefore **BKCR and UNCP are not the same source datatype**:

- BKCR is byte RGB/color data;
- UNCP is three-component float color data.

## Event/UI evidence

The binary's localized event strings expose the values the custom interaction path can inspect/display:

- `Layer Coordinates: %d, %d`
- `Depth %.2f`
- `Depth not available`
- `Normal %.2f, %.2f, %.2f`
- `Texture uv %.2f, %.2f`
- `Coverage %.2f`
- `Object ID %d`
- `Background Color %d %d %d`
- `Unclamped Color %.1f %.1f %.1f`
- `Material ID %d`

This is useful corroboration of channel dimensionality, but string presence alone is not a substitute for the render-loop evidence above.

## Near-complete static reconstruction status

At this point all eight channel families have a statically identified source shape and output visualization structure:

| UI concept | Machine channel | Source shape observed | Visualization |
|---|---|---|---|
| Z-Depth | `DPTH` / `DPAA` | float scalar | Black/White normalized grayscale, optional inversion/clamp |
| Object ID | `OBID` | unsigned 16-bit scalar | grayscale ID visualization |
| Texture UV | `TEXR` | 2 × float | two color components + zero third component |
| Surface Normals | `NRML` | 3 × float | `(component + 1) * 0.5` |
| Coverage | `COVR` | float scalar | replicated grayscale |
| Background RGB | `BKCR` | 3 × byte | direct RGB |
| Unclamped RGB | `UNCP` | 3 × float | direct float RGB / quantized for integer output |
| Material ID | `MATR` | byte scalar | replicated grayscale |

The mapping between UI ordering and the stored selector integer still needs an actual parameter-value observation before it is called bit-exact host behavior.

## What static analysis cannot honestly close by itself

The binary dump is now sufficient for the core render architecture, but the following acceptance items require runtime fixtures rather than more disassembly:

- exact UI selector integer ↔ menu item mapping;
- exact default/range values as exposed by AE;
- DPTH vs DPAA selection under the Anti-alias checkbox;
- Black Point == White Point observable output;
- Plus/Minus Infinity observable output;
- missing-channel output and returned host error;
- exact Object ID half-range behavior;
- pixel-level equivalence fixtures for 8/16/32 bpc;
- CPU/GPU/MFR runtime status.

These are deliberately left open instead of being guessed from static code.

## Revised compact channel contract

| Machine channel | Expected source datatype observed in code | Output structure |
|---|---|---|
| `DPTH` / `DPAA` | `FLT4` | normalized grayscale RGB + opaque A |
| `OBID` | `SU2T` | scalar grayscale RGB + opaque A |
| `TEXR` | `FLT4` | two float components, third color component zero + opaque A |
| `NRML` | `FLT4` | `(xyz + 1) * 0.5` visualization + opaque A |
| `COVR` | `FLT4` | float scalar → grayscale RGB + opaque A |
| `BKCR` | byte RGB family | direct RGB visualization + opaque A |
| `UNCP` | `FLT4` | three float components → RGB + opaque A |
| `MATR` | `UB1T` | byte scalar grayscale RGB + opaque A |

FourCC datatype labels above are written exactly as reconstructed from the machine immediates. Their SDK typedef/enumeration spelling should be cross-checked before translating them into higher-level SDK names.

## Remaining algorithm gaps after cross-bit-depth pass

Before claiming a bit-exact independent implementation, the following remain open:

- exact OBID half-range adjustment/wrap semantics at the user-visible boundary;
- exact UV component-to-R/G naming (the two-component arithmetic itself is resolved);
- exact DPTH vs DPAA selection condition and anti-alias semantics;
- exact infinity/degenerate-range behavior;
- effect of Clamp Output outside the depth path, if any;
- pixel behavior for unavailable/mismatched channel data;
- fixture confirmation of alpha and edge behavior.


## Updated reconstruction workflow

The static-capture milestone is complete. The next reconstruction pass should work from the captured file rather than collecting more overlapping LLDB excerpts:

1. ~~decode `FillInAllParams` and parameter setup into a parameter-index table;~~ **Complete for slots 1–6; defaults/ranges remain.**
2. ~~decode the eight channel-case targets and four-character identifiers;~~ **Complete for stored selector values; UI/value translation remains.**
3. **Cross-bit-depth pass substantially complete:** NRML, BKCR, TEXR, UNCP and depth structure reconstructed; COVR/ID edge formulas remain.
4. **Inline 32-bpc path correlated with the named 8/16-bit implementations.**
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
