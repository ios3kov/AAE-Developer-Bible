# Status

**v1.0 — final native-first reference edition**

See `FINAL-COVERAGE-AUDIT.md` for requirement-by-requirement coverage and verification boundaries.

# Status

Research snapshot: **2026-09-30**

Current edition: **v0.4 — self-verifying native SDK contracts + reusable native foundation**

## Completed

- Core Effect / AEGP / AEIO / Artisan documentation.
- macOS and Windows branches.
- Testing/distribution/recipes/templates.
- Native taxonomy: Effect, AEGP, Keyframer, native panels, AEIO, Artisan, BlitHook, shared PICA suites and legacy paths.
- Communication model between AE, Effect, AEGP, scripts and CEP.
- Working drop-in templates and protocol headers.
- Native Suite Cookbook for project graph, layers, effects, properties, animation, masks/text, render and render queue.
- AEGP suite → function capability map.
- Public SDK docs errata / header-verification policy.
- Additional C++ drop-ins for common native operations.
- Header-derived native SDK inventory generator (AEGP/PF/AEIO/Artisan/Drawbot/function tables).
- Recipe symbol verifier and SDK-to-SDK contract diff.
- macOS/Windows native validation launchers.
- Reusable PICA/AEGP ownership + undo + ABI-boundary helpers with stub compile test.

## Verification level

- Current-version facts cross-checked against the public After Effects C++ SDK Guide and 26.5 release notes.
- High-risk signatures in v0.3 were re-checked individually against published SDK declarations/header-derived contracts.
- v0.4 inventory tooling is tested on synthetic ABI-shaped headers; C++ foundation compiles under C++17 against a synthetic host ABI stub.
- JS/HTML templates are self-contained logic.
- C++ templates are designed as drop-ins for official Adobe SDK samples.
- The sandbox does **not** contain the proprietary Adobe SDK distribution or an After Effects host, so no claim of compiled/host-executed binaries is made.

## Next engineering wave

- Run the header-derived inventory against a locally supplied current Adobe SDK header set.
- Compile the drop-ins against the official SDK on macOS and Windows.
- Add SmartFX/MFR/GPU complete starter variants.
- Add host verification matrix across supported AE versions/architectures.
