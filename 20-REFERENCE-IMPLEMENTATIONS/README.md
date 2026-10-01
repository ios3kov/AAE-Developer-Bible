# Reference implementations

This section maps Bible concepts to **reference source shapes and official SDK sample starting points**.

It is not a suite of binaries that must be built to complete the Bible.

## Purpose

Use this section when a reader asks:

- what source shape does this architecture turn into;
- which Adobe sample should I start from;
- where is the relevant Bible recipe/header;
- what pieces are intentionally omitted.

For native work, Adobe SDK project/PiPL/utility files remain licensed external material and are not redistributed here.

## Reference vocabulary

- **source example** — Bible-owned source illustrating a contract/pattern;
- **sample-derived pattern** — explanation/source shape based on a named Adobe sample family;
- **guide-only** — architecture and integration route, intentionally no implementation;
- **skeleton** — intentionally partial source for one boundary;
- **runtime observed** — used only where a concrete recorded execution result exists.

Older `host-test-required` wording is superseded. Lack of a Bible-owned runtime run is an evidence boundary, **not a TODO required to finish the documentation**.

## Native-first matrix

| Family | Reference | Editorial status | Purpose |
|---|---|---|---|
| Effect | `../16-WORKING-TEMPLATES/effect-basic` | source example | classic pixel-effect shape |
| Effect | `Effect/SmartFX-MFR` | source example | SmartFX/MFR architecture shape |
| Effect UI | `Effect/CustomUI-Drawbot` | skeleton | Drawbot acquisition/UI boundary |
| AEGP | `AEGP/MenuTool` | source example | menu command + callback lifecycle |
| AEGP | `AEGP/Keyframer` | sample-derived pattern | keyframe batching route |
| AEGP UI | `AEGP/NativePanel` | guide-only | Panelator path |
| AEIO | `AEIO/MinimalRegistrar` | guide-only | IO/FBIO registration path |
| Artisan | `Artisan/MinimalRegistrar` | guide-only | Artie registration path |
| Bridge | `Bridges/Effect-AEGP` | source pattern | generic-call message ABI |
| Bridge | `Bridges/PICA-Provider-Consumer` | source pattern | published suite ABI |
| Script | `Scripts/ScriptUI-Panel` | source example | ScriptUI panel pattern |
| CEP | `../16-WORKING-TEMPLATES/cep-panel-bridge` | source example | panel ↔ JSX dispatcher |

## Using native references

If a reader chooses to build one:

1. obtain the target Adobe SDK legally;
2. start from the closest official sample project;
3. keep the sample's PiPL/resource/platform plumbing;
4. graft the Bible source/pattern;
5. apply the product's own compiler/host/release testing.

Those product-validation steps are described elsewhere in the Bible, but **the Bible itself does not need to execute them for every reference**.

`scripts/materialize_sdk_examples.py` can create local untracked sample workspaces as an optional developer utility.

Historical compiler/runtime evidence, where present, remains documented in [VERIFICATION.md](../VERIFICATION.md).
