# Verification — v1.1

## Parameter/UI and color/pixel chapter review (2026-09-30)

Expanded [parameters and UI](02-EFFECT-PLUGINS/02-PARAMETERS-UI.md) and [pixels, color and alpha](02-EFFECT-PLUGINS/06-COLOR-PIXELS.md) from the supplied SDK 25.6 build 61. The [second source-review record](18-SDK-HEADER-TOOLS/06-PARAMETERS-PIXELS-SDK25.6.md) records hashes for 15 source files, exact declaration/sample line ranges and unresolved source discrepancies.

Reviewed contracts include non-animatable versus non-interpolated parameters; setup macro clearing; USER_CHANGED_PARAM versus UPDATE_PARAMS_UI; UI-only/disabled/hidden states; Point/default units; ARGB32/64/128; the 0..32768 integer 16-bpc range; typed pixel access; rowbytes/origin; alpha-conversion signatures; floating color parameters in the effect working space; and possible multithreading of iterate callbacks.

Source discrepancies are retained explicitly: two numeric typos beside 16-bit constants, Paramarama enum/setup ordering, Supervisor popup changes beyond the documented PF_UpdateParamUI field list, and differing macro initialization behavior. No SDK source was edited to hide them. They are source observations, not newly reproduced host defects.

**Verification level: documentation and SDK source review, not new native compilation.** Authored C++ fragments illustrate setup, UI flags and floating color lookup; they are not linked or host-tested plug-ins. Numeric normalization/alpha examples are mathematical explanations, not native-effect measurements. The TAR identity was rechecked against the previous recorded SHA-256; the prior compressed/decompressed byte comparison is not claimed as a new successful run.

GitHub Validate remains responsible for the documentation build and existing portable regressions on the committed revision. It does not compile these Markdown fragments against the licensed SDK. Native readout development remains paused; no new user AE run, map installation, output conversion experiment or GPU/MFR comparison was performed. Plan gates 2, 3A and 4–9 are not silently closed by editorial work.

## First supplied-SDK chapter review (2026-09-30)

The user supplied `ae25.6_61.64bit.AfterEffectsSDK`. In the first review, the uploaded Zstandard stream was decompressed and compared byte-for-byte with the separately uploaded TAR; they matched. Source hashes and exact file/line references are recorded in [the supplied-SDK review](18-SDK-HEADER-TOOLS/05-SUPPLIED-SDK-25.6.md).

That iteration expanded Effect anatomy and SmartFX and added an auxiliary-channel chapter. It checked declarations, ownership rules and relevant Skeleton/SmartyPants source behavior. In particular, auxiliary-channel checkin and SmartFX world checkin have different documented contracts.

**Scope: SDK source review and documentation.** No new native reader, compiled plug-in, AE render, importer qualification or concurrency run was claimed. The historical compiler baseline below was not repeated and is not automatically attributed to the new upload. GitHub documentation validation is separate from native compilation and host execution.

## Recorded baseline (2026-09-30)

- Adobe After Effects SDK **25.6 build 61**, locally supplied; proprietary headers are not redistributed.
- macOS arm64, Apple Clang, C++17: **13 translation-unit checks passed**.
- Python: **7 tests passed**.
- Foundation: strict C++17 build and behavioral assertions passed against synthetic stubs.
- Full SDK index: 70 headers, 230 recognized tables, 3537 parsed functions. **Incomplete**: unsupported declarations produce diagnostics and a nonzero exit code. These counts are exploratory, not coverage claims.
- Native linking, PiPL packaging, AE loading/rendering, MFR stress and Windows compilation: **not verified**.

The 13 recorded translation-unit checks include two forwarding entry files and a foundation-header probe. These historical results are not repeated by the two editorial reviews above.

`scripts/materialize_sdk_examples.py` provides exact local sample shells for all six gaps. `scripts/host_cycle.py` installs a built bundle and optionally invokes `aerender`, but intentionally reports UI load/unload and MFR stress as pending.

## Reproduce portable checks

```bash
python3 -m unittest discover -s 18-SDK-HEADER-TOOLS/tests -v
mkdir -p .build
c++ -std=c++17 -Wall -Wextra -Werror \
  -I19-NATIVE-CODE-FOUNDATION/tests/stubs \
  -I19-NATIVE-CODE-FOUNDATION/code \
  19-NATIVE-CODE-FOUNDATION/tests/test_foundation.cpp -o .build/foundation-test
.build/foundation-test
python3 -m pip install -r requirements-docs.txt
python3 scripts/build_docs.py --check
python3 scripts/build_docs.py
mkdocs build --strict
```

## Check with the actual SDK (macOS / Clang)

```bash
python3 scripts/check_native.py "/path/to/Adobe-SDK/Examples"
```

This is a **syntax/type** check. It deliberately does not call it a plugin build. Keep Adobe sample utilities, PiPL resources, exported entry points and platform settings when integrating. Compile canonical sources or section-20 forwarding files, never both into the same binary. Copy the foundation headers alongside MenuTool or adjust its relative include.

## Required next host checks

1. Minimal Gain: load, parameter UI, gain 0/1/4, 8/16-bpc and transparent pixels.
2. SmartFX Copy: compare input/output at 8/16/32-bpc, partial/empty ROI, odd sizes, nonzero origins and cancellation. Keep MFR off until concurrent-frame tests pass.
3. MenuTool: successful command execution, menu updates, failed initialization and shutdown.
4. Recipes: disposable project operations, undo, stream/keyframe ownership and render receipt cleanup.
5. Record AE build, SDK, OS/architecture, sample base and actual observed result before upgrading a status to host-verified.
