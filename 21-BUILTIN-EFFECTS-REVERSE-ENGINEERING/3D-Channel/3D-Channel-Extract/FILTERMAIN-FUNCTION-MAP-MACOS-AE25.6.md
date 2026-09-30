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

## Next acceptance criteria

1. Capture both complete `RenderX` bodies and `FillInAllParams`, preserving function boundaries.
2. Decode the small `ACX_Power2` helper rather than inferring its exponent convention from its name.
3. Associate parameter indices and channel-table cases with evidence before naming their UI semantics.
4. Write separate pseudocode for the 8-bit, 16-bit, and inline 32-bit paths, including missing-channel handling, range reversal, equal limits, clamping, and alpha writes.
5. Validate reconstructed pixel behavior against controlled host fixtures before claiming algorithm equivalence.

This milestone records the function map and dispatch evidence only. Algorithm equivalence and performance have not been tested.
