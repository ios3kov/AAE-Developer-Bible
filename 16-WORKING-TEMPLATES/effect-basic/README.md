# Minimal Gain effect — working template

Status: **source implementation / SDK 25.6 macOS syntax-checked / host-test pending**.

Requires C++17, the SDK utility sources and the official sample project/PiPL build configuration.

## Base project

Copy the target SDK Skeleton sample first.

Keep:

- Xcode/Visual Studio project;
- entry.h and SDK utilities;
- PiPL .r source and Windows conversion step;
- platform architecture settings;
- output bundle/aex layout.

Replace the effect implementation with EffectMain.cpp and synchronize product identity in both source and PiPL.

## Behavior

The source implements:

- About;
- GlobalSetup;
- one floating Gain parameter;
- classic Render;
- 8-bpc processing;
- 16-bpc processing;
- alpha pass-through;
- host Iterate suites;
- C ABI exception containment.

It intentionally does not claim:

- 32-bpc float;
- SmartFX;
- MFR;
- GPU;
- custom UI.

Those capabilities must be implemented and tested before flags are added.

## Parameter contract

Param index:

~~~text
0 input
1 Gain
~~~

Gain uses a stable disk ID of 1 in this example.

Once real projects exist, parameter IDs/meaning become persistence compatibility data. Do not reuse an old disk ID for a new semantic.

## Render semantics

For each pixel:

~~~text
alpha = input alpha
RGB = clamp(input RGB × gain, channel range)
~~~

8-bit and 16-bit paths use the corresponding host iteration suites and channel maxima.

The code intentionally avoids raw rowbytes loops in this first template.

## Why alpha is not multiplied

Gain here means RGB gain while preserving alpha.

That is a product semantic decision for this template, not a universal AE rule.

If your actual effect changes alpha, define and test that behavior explicitly.

## Threading state

Render uses only callback-local GainInfo plus immutable function code. There is no mutable render global in this file.

Still, MFR is deliberately not declared. Final thread safety also depends on every dependency and future product change.

Follow 12-RECIPES/02-MFR-MIGRATION.md before enabling threaded rendering.

## 32-bpc path

PF_OutFlag_DEEP_COLOR_AWARE covers the implemented deep-color 16-bit path here; it is not a claim of 32-bpc float support.

Add a separate float path and the appropriate current-SDK capability only after exact float semantics and tests exist.

## Error boundary

EffectMain catches PF_Err and unknown C++ exceptions before they leave the exported callback.

For a product codebase, consider the shared HostCallbackGuard policy from 19-NATIVE-CODE-FOUNDATION so callback error mapping is consistent.

## First host fixture

Create a deterministic source containing:

- black;
- mid-gray;
- white;
- primary colors;
- partial alpha.

Test Gain:

- 0;
- 0.5;
- 1;
- 2;
- 4.

Verify RGB values/clamping and unchanged alpha at 8 and 16 bpc.

## Save/reopen

Apply the effect, change Gain, save, restart AE and reopen.

Confirm:

- effect resolves by identity;
- parameter value survives;
- output matches pre-save result.

## Extension order

~~~text
host load/basic render
→ 8/16 correctness
→ 32-bpc if required
→ SmartFX/ROI
→ MFR
→ GPU
→ custom UI
~~~

Do not turn the minimal template into every feature at once.

## Verification boundary

Syntax/type checking is not load/render evidence. Record actual build/install/host results in VERIFICATION/evidence before changing host-test pending to PASS.
