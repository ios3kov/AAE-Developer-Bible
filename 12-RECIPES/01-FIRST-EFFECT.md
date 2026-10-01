# Recipe — first native effect

## Goal

Reach a minimal native effect that can be reproduced from a clean checkout, built with the target SDK, installed, loaded by After Effects and rendered before product-specific complexity is added.

## Phase 1 — establish an untouched baseline

1. Choose the exact After Effects SDK version.
2. Copy Skeleton or the closest official sample.
3. Record SDK build, toolchain, OS and architecture.
4. Build the untouched sample.
5. Preserve the original PiPL/resource build steps.
6. Install it into the documented development location.
7. Launch the target AE version.
8. Apply the sample and render one deterministic frame.

If the official sample baseline does not load, stop. Do not debug product code that does not exist yet.

## Phase 2 — rename without changing behavior

Change only identity:

- product/display name;
- identifiers that must be unique;
- entry metadata where required;
- output filename/bundle identifiers;
- version metadata.

Keep render behavior unchanged.

Then repeat:

~~~text
build
→ install
→ load
→ apply
→ render
~~~

This isolates registration/resource mistakes from algorithm mistakes.

## Phase 3 — isolate the render core

Prefer:

~~~text
AE adapter
→ internal pixel/view abstraction
→ RenderCore
→ output adapter
~~~

Keep RenderCore independent of PF_InData, host handles and UI wherever practical.

That gives you a unit-testable algorithm and smaller host boundary.

## Phase 4 — first golden fixture

Before advanced features:

- one deterministic source image;
- one parameter set;
- one frame/time;
- known BPC;
- explicit expected output.

Test RenderCore outside AE, then compare the host output.

## Phase 5 — add capabilities one by one

Recommended order:

1. 8-bpc baseline;
2. 16-bpc if claimed;
3. 32-bpc if claimed;
4. alpha/odd sizes/origins;
5. SmartFX/ROI if needed;
6. persistence/sequence state;
7. custom UI;
8. MFR;
9. GPU.

After each step, keep the previous fixture passing.

## macOS

For development use the per-user MediaCore path and an ad-hoc-signed plug-in when required by the macOS/AE version.

Before release later:

- architecture slices;
- Developer ID;
- notarization;
- clean install.

Do not mix release-signing complexity into the first algorithm bring-up.

## Windows

Preserve the sample's PiPL resource-generation custom build step.

Start with x64 unless product requirements explicitly demand ARM64 immediately.

Archive the matching PDB once the project becomes a real product candidate.

## Done means

The first-effect milestone is complete only when a recorded artifact can demonstrate:

- exact SDK/toolchain known;
- native build succeeds;
- PiPL/entry point valid;
- AE discovers the plug-in;
- effect can be applied;
- deterministic frame matches expected output;
- save/reopen does not lose basic state;
- debugger symbols match the artifact.

"Source compiles" is not done.

## Next

Only after this baseline should you add SmartFX, MFR, GPU or a complex panel.

See 10-TESTING/06-EVIDENCE-AND-ACCEPTANCE.md for the evidence record.
