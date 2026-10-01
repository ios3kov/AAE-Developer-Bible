# Coverage and verification matrix

Edition: **v1.1 working line**, updated 2026-10-01. A chapter being present does not mean its API family is fully implemented.

| Area | Documentation | Implementation | Verification |
|---|---|---|---|
| Extension selection, architecture, communication | Architectural guidance | Protocol headers and recipes | Source/editorial review; host behavior separate |
| Safe tooling | Transactional install/materialization and fail-closed render harness guidance | `host_cycle.py`, SDK sample materializer, portable regression tests | Gate 2 closed: Validate `36839553520` on `22095cd86a74`; not an AE host PASS |
| Classic Effect | Lifecycle and rendering guidance | Minimal Gain, 8/16-bpc | SDK 25.6 macOS syntax/type check; host pending |
| SmartFX | ROI/checkout guidance | Host-copy pass-through, 8/16/32-bpc intent | SDK syntax/type check; pixel/ROI host tests pending; MFR disabled |
| Custom UI / Drawbot | Event and lifetime guidance | Drawing-reference acquisition skeleton | SDK syntax/type check; no drawing implementation |
| AEGP MenuTool | Hooks and suites | Command registration and info callback | SDK syntax/type check; host lifecycle tests pending |
| AEGP recipes | Project, layers, streams, keyframes, render queue | Selected C++ recipes | SDK syntax/type check; host operations pending |
| Native panels | Architecture and Panelator sample path | Local SDK sample workspace | Host test pending |
| AEIO | Architecture and IO/FBIO sample path | Local SDK sample workspace | Host test pending |
| Artisan | Architecture and Artie sample path | Local SDK sample workspace | Host test pending |
| PICA / Effect↔AEGP | Communication protocol and Sweetie/Commando paths | Local SDK sample workspaces | End-to-end host test pending |
| JSX / ScriptUI | Usage guidance | Scripts supplied | AE execution pending |
| CEP | Dispatcher architecture | Logic files; packaging dependencies external | Host execution pending |
| GPU | Backend design and testing guidance | SDK_Invert_ProcAmp sample path | GPU comparison pending |
| SDK tooling | Reproducible commands, required-contract manifest and evidence boundaries | Declaration inventory, required table/function gate, exact SuiteHandler-generation check, compiler-report driver | Real SDK 25.6 required preflight PASS: 35/35 contracts, 39/39 cookbook calls; 4 non-required partial diagnostics retained; current macOS/MSVC compile still pending |
| C++ foundation | Ownership/undo/callback guidance | Helpers | Behavioral stub tests and SDK syntax/type check |
| macOS / Windows | Build/sign/package plus clean-machine release pipelines | Sample materializer + syntax drivers | historical macOS syntax baseline; Windows native compile/host still pending |
| Built-in effect research atlas | Evidence levels, execution plan and effect catalog | 3D Channel Extract evidence/function-map pilot | partial static/runtime evidence; full-effect acceptance and catalog completion remain open |

## Vocabulary

- **Guide only**: explanatory material, no source implementation.
- **Skeleton**: partial code with explicitly missing behavior.
- **Source implementation**: behavior is implemented, but host correctness is not implied.
- **SDK syntax-checked**: the compiler accepted types and declarations for a named SDK/platform.
- **Host-verified**: a recorded load/operation/render test passed on a named AE build. None is claimed here yet.

Historical directory names are retained for existing links. `MinimalRegistrar` directories contain guides, not registrar implementations. `drop-in` describes how source is integrated into an Adobe sample, not a verification level.
