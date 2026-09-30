# Reference implementations

v1.1 verification: [coverage matrix](../FINAL-COVERAGE-AUDIT.md), [commands and results](../VERIFICATION.md). AEIO/Artisan/native-panel entries are **guide only**; Drawbot is an acquisition skeleton. Script/CEP host execution is pending. The historical matrix below describes intended integration, not test evidence.

MenuTool, Keyframer and bridge files forward to canonical sources in sections 16/17. Compile either location, not both, and retain the relative directory layout or copy the canonical implementation.

This directory turns the architecture chapters into copyable starting points.

## Status vocabulary

- **drop-in** — intended to be copied into the closest official Adobe SDK sample shell.
- **sample-derived** — follows the public SDK/sample contract, but still needs the exact SDK version's headers/project plumbing.
- **host-test-required** — host execution is pending; this label alone does not establish that source is implemented or compiled.
- **guide-only** — architecture/sample selection, no implementation supplied.
- **skeleton** — partial code, missing behavior explicitly documented.

**Important:** Adobe's SDK headers and sample project files are not redistributed here. For native projects, start from the closest official SDK sample, then replace the implementation with the files here. This is deliberate: PiPL/resource build plumbing and platform settings change across SDK releases.

## Native-first matrix

| Family | Example | Status | Purpose |
|---|---|---|---|
| Effect | `../16-WORKING-TEMPLATES/effect-basic` | drop-in | classic pixel effect |
| Effect | `Effect/SmartFX-MFR` | SDK syntax-checked / host-test-required | SmartFX pass-through; MFR disabled |
| Effect UI | `Effect/CustomUI-Drawbot` | skeleton / SDK syntax-checked | Drawbot acquisition only; no drawing |
| AEGP | `AEGP/MenuTool` | drop-in | menu command + host callback lifecycle |
| AEGP | `AEGP/Keyframer` | sample-derived / host-test-required | keyframe batching path |
| AEGP UI | `AEGP/NativePanel` | guide-only | native panel registration path |
| AEIO | `AEIO/MinimalRegistrar` | guide-only | importer/exporter registration boundary |
| Artisan | `Artisan/MinimalRegistrar` | guide-only | custom renderer registration boundary |
| Bridge | `Bridges/Effect-AEGP` | sample-derived / host-test-required | `AEGP_EffectCallGeneric` message ABI |
| Bridge | `Bridges/PICA-Provider-Consumer` | sample-derived / host-test-required | plug-in ↔ plug-in PICA suite ABI |
| Script | `Scripts/ScriptUI-Panel` | source supplied / host-test pending | dockable ExtendScript panel |
| CEP | `../16-WORKING-TEMPLATES/cep-panel-bridge` | logic supplied / packaging and host-test pending | panel ↔ ExtendScript JSON bridge |

## Build rule

Native examples intentionally do **not** invent replacement Xcode/Visual Studio projects. Copy the matching Adobe SDK sample project and graft in the implementation. See `08-MACOS`, `09-WINDOWS`, and `18-SDK-HEADER-TOOLS`.
