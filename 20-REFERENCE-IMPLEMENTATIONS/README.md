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
| Effect | [Minimal Gain](../16-WORKING-TEMPLATES/effect-basic/README.md) | source example | classic pixel-effect shape |
| Effect | [SmartFX / MFR](Effect/SmartFX-MFR/README.md) | source example | SmartFX/MFR architecture shape |
| Effect UI | [Custom UI / Drawbot](Effect/CustomUI-Drawbot/README.md) | skeleton | Drawbot acquisition/UI boundary |
| AEGP | [MenuTool](AEGP/MenuTool/README.md) | source example | menu command + callback lifecycle |
| AEGP | [Keyframer](AEGP/Keyframer/README.md) | sample-derived pattern | keyframe batching route |
| AEGP UI | [NativePanel](AEGP/NativePanel/README.md) | guide-only | Panelator path |
| AEIO | [MinimalRegistrar](AEIO/MinimalRegistrar/README.md) | guide-only | IO/FBIO registration path |
| Artisan | [MinimalRegistrar](Artisan/MinimalRegistrar/README.md) | guide-only | Artie registration path |
| Bridge | [Effect–AEGP](Bridges/Effect-AEGP/README.md) | source pattern | generic-call message ABI |
| Bridge | [PICA Provider–Consumer](Bridges/PICA-Provider-Consumer/README.md) | source pattern | published suite ABI |
| Script | [ScriptUI Panel](Scripts/ScriptUI-Panel/README.md) | source example | ScriptUI panel pattern |
| CEP | [CEP–ExtendScript bridge](../16-WORKING-TEMPLATES/cep-panel-bridge/README.md) | source example | panel ↔ JSX dispatcher |

Additional reference: [GPU](GPU/README.md).
Its scope and evidence limits are described in that document.

## Using native references

If a reader chooses to build one:

1. obtain the target Adobe SDK legally;
2. start from the closest official sample project;
3. keep the sample's PiPL/resource/platform plumbing;
4. graft the Bible source/pattern;
5. apply the product's own compiler/host/release testing.

Those product-validation steps are described elsewhere in the Bible, but **the Bible itself does not need to execute them for every reference**.

`scripts/materialize_sdk_examples.py` can create local untracked sample workspaces as an optional developer utility.

For an actual SDK project, preserve its relative dependencies:

```sh
python3 scripts/materialize_sdk_examples.py "/path/to/SDK/Examples" --workspace --out .build/sdk-workspace --only native-panel
```

Workspace mode copies the **whole locally licensed Examples tree** into a fresh
output directory; `--only` selects entries in `workspace-index.json`, not files to
copy. It refuses existing or SDK-overlapping output. Default mode still extracts
individual source shells for inspection/adaptation; those isolated copies are not
standalone build projects. Do not commit or redistribute the licensed workspace.

Historical compiler/runtime evidence, where present, remains documented in [VERIFICATION.md](../VERIFICATION.md).
