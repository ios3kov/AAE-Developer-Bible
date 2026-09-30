# SmartFX + MFR effect starter

Status: **sample-derived / host-test-required**.

Start from Adobe's SmartFX-capable effect sample. Keep the sample PiPL/project files. Replace selector dispatch with `SmartFxMfr.cpp`, then insert your pixel algorithm in `SmartRender`.

What this demonstrates:

1. capability declaration in `GLOBAL_SETUP`;
2. `SMART_PRE_RENDER` requests input based on output ROI;
3. `SMART_RENDER` checks out input/output through SmartFX callbacks;
4. no mutable render globals;
5. MFR is only declared for a render path designed to be re-entrant.

Run `18-SDK-HEADER-TOOLS` against your installed SDK before build, then host-test concurrent frames.
