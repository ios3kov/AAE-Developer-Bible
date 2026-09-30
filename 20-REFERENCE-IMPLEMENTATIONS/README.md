# Reference implementations

This directory turns the architecture chapters into copyable starting points.

## Status vocabulary

- **drop-in** — intended to be copied into the closest official Adobe SDK sample shell.
- **sample-derived** — follows the public SDK/sample contract, but still needs the exact SDK version's headers/project plumbing.
- **host-test-required** — API shape is documented, but this repository has not loaded/rendered it inside a licensed local After Effects host.

**Important:** Adobe's SDK headers and sample project files are not redistributed here. For native projects, start from the closest official SDK sample, then replace the implementation with the files here. This is deliberate: PiPL/resource build plumbing and platform settings change across SDK releases.

## Native-first matrix

| Family | Example | Status | Purpose |
|---|---|---|---|
| Effect | `../16-WORKING-TEMPLATES/effect-basic` | drop-in | classic pixel effect |
| Effect | `Effect/SmartFX-MFR` | sample-derived / host-test-required | SmartFX + MFR selector skeleton |
| Effect UI | `Effect/CustomUI-Drawbot` | sample-derived / host-test-required | custom UI event + Drawbot acquisition pattern |
| AEGP | `AEGP/MenuTool` | drop-in | menu command + host callback lifecycle |
| AEGP | `AEGP/Keyframer` | sample-derived / host-test-required | keyframe batching path |
| AEGP UI | `AEGP/NativePanel` | host-test-required | native panel registration path |
| AEIO | `AEIO/MinimalRegistrar` | host-test-required | importer/exporter registration boundary |
| Artisan | `Artisan/MinimalRegistrar` | host-test-required | custom renderer registration boundary |
| Bridge | `Bridges/Effect-AEGP` | sample-derived / host-test-required | `AEGP_EffectCallGeneric` message ABI |
| Bridge | `Bridges/PICA-Provider-Consumer` | sample-derived / host-test-required | plug-in ↔ plug-in PICA suite ABI |
| Script | `Scripts/ScriptUI-Panel` | runnable | dockable ExtendScript panel |
| CEP | `../16-WORKING-TEMPLATES/cep-panel-bridge` | runnable with CEP host | panel ↔ ExtendScript JSON bridge |

## Build rule

Native examples intentionally do **not** invent replacement Xcode/Visual Studio projects. Copy the matching Adobe SDK sample project and graft in the implementation. See `08-MACOS`, `09-WINDOWS`, and `18-SDK-HEADER-TOOLS`.
