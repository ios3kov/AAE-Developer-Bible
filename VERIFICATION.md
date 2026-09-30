# Verification — v1.1

## Recorded baseline (2026-09-30)

- Adobe After Effects SDK **25.6 build 61**, locally supplied; proprietary headers are not redistributed.
- macOS arm64, Apple Clang, C++17: **13 translation-unit checks passed** (including two forwarding entry files and a foundation-header probe).
- Python: **7 tests passed**.
- Foundation: strict C++17 build and behavioral assertions passed against synthetic stubs.
- Full SDK index: 70 headers, 230 recognized tables, 3537 parsed functions. **Incomplete**: unsupported declarations produce diagnostics and a nonzero exit code. These counts are exploratory, not coverage claims.
- Native linking, PiPL packaging, AE loading/rendering, MFR stress and Windows compilation: **not verified**.

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
