# SmartFX pass-through (MFR validation pending)

Status: **source implementation / SDK 25.6 macOS syntax-checked / host-test-required**.

Start from Adobe's SmartFX-capable effect sample. Keep its utility sources/project files. Use `SmartFxMfr.cpp` as the implementation, and synchronize PiPL identity and flags with the code. The render uses the host World Transform copy callback, avoiding manual rowbytes/pixel-format assumptions. Validate 8/16/32-bpc, ROI and origins in AE before extending it.

What this demonstrates:

1. capability declaration in `GLOBAL_SETUP`;
2. `SMART_PRE_RENDER` requests input based on output ROI;
3. `SMART_RENDER` checks out input/output through SmartFX callbacks;
4. no mutable render globals;
5. MFR is **not declared** until the final render path passes concurrent-frame host tests.

Run `scripts/check_native.py` against your SDK for syntax/type checks, build in the sample shell, then record host results in `VERIFICATION.md`.
