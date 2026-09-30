# Coverage and verification matrix

Edition: **v1.1**, 2026-09-30. A chapter being present does not mean its API family is fully implemented.

| Area | Documentation | Implementation | Verification |
|---|---|---|---|
| Extension selection, architecture, communication | Architectural guidance | Protocol headers and recipes | Manual review |
| Classic Effect | Lifecycle and rendering guidance | Minimal Gain, 8/16-bpc | SDK 25.6 macOS syntax/type check; host pending |
| SmartFX | ROI/checkout guidance | Host-copy pass-through, 8/16/32-bpc intent | SDK syntax/type check; pixel/ROI host tests pending; MFR disabled |
| Custom UI / Drawbot | Event and lifetime guidance | Drawing-reference acquisition skeleton | SDK syntax/type check; no drawing implementation |
| AEGP MenuTool | Hooks and suites | Command registration and info callback | SDK syntax/type check; host lifecycle tests pending |
| AEGP recipes | Project, layers, streams, keyframes, render queue | Selected C++ recipes | SDK syntax/type check; host operations pending |
| Native panels | Architecture and sample selection | Guide only | No implementation/host test |
| AEIO | Architecture and callback overview | Guide only | No importer/exporter implementation |
| Artisan | Architecture and sample selection | Guide only | No renderer implementation |
| PICA / Effect↔AEGP | Communication protocol | Contract headers | No end-to-end provider/consumer host test |
| JSX / ScriptUI | Usage guidance | Scripts supplied | AE execution pending |
| CEP | Dispatcher architecture | Logic files; packaging dependencies external | Host execution pending |
| GPU | Backend design and testing guidance | No GPU implementation | CPU/GPU comparison pending |
| SDK tooling | Reproducible commands and limits | Declaration index, symbol-name check, textual/order diff | Synthetic regression tests; full SDK index incomplete |
| C++ foundation | Ownership/undo/callback guidance | Helpers | Behavioral stub tests and SDK syntax/type check |
| macOS / Windows | Build/distribution guidance | SDK syntax-check driver for Clang | macOS baseline checked; Windows pending |

## Vocabulary

- **Guide only**: explanatory material, no source implementation.
- **Skeleton**: partial code with explicitly missing behavior.
- **Source implementation**: behavior is implemented, but host correctness is not implied.
- **SDK syntax-checked**: the compiler accepted types and declarations for a named SDK/platform.
- **Host-verified**: a recorded load/operation/render test passed on a named AE build. None is claimed here yet.

Historical directory names are retained for existing links. `MinimalRegistrar` directories contain guides, not registrar implementations. `drop-in` describes how source is integrated into an Adobe sample, not a verification level.
