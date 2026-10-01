# SmartFX pass-through reference

Status: **source implementation / SDK 25.6 macOS syntax-checked / host-test-required**.

SmartFxMfr.cpp is intentionally a small pass-through reference with SmartFX support. It does **not** currently declare MFR support.

## Why MFR stays disabled

The source has no mutable render globals, but thread safety is a whole-effect property.

PF_OutFlag2_SUPPORTS_THREADED_RENDERING is enabled only after the final product render path, dependencies, caches and third-party code pass concurrent-frame host tests.

Source shape alone is not enough.

## Start from a SmartFX-capable SDK project

Preserve the exact SDK sample project, resources and utility files.

Synchronize:

- product name/match name;
- entry point;
- PiPL flags;
- GlobalSetup flags;
- architectures.

Do not graft only SmartFxMfr.cpp into a broken/incomplete project shell.

## GlobalSetup

The reference declares:

- deep-color awareness;
- SmartFX support;
- float-color awareness.

It deliberately omits the threaded-rendering flag.

A future product must keep PiPL/outflags/runtime behavior consistent.

## Smart pre-render

The implementation copies the output request into the input checkout request and records the returned result/max-result rectangles.

This demonstrates the request/rectangle lifecycle, not an optimized dependency analysis.

A real effect should calculate only the input region it truly needs.

## Smart render

The reference:

1. checks out input pixels using checkout ID 1;
2. checks out output;
3. validates worlds;
4. uses WorldTransformSuite copy;
5. always checks input pixels back in if checkout succeeded;
6. preserves the first operation error unless checkin is the first error.

This avoids manual rowbytes/pixel-format loops in the pass-through baseline.

## What to test before extending

- full frame;
- small ROI;
- edge ROI;
- empty/single-pixel region if host path generates it;
- odd dimensions;
- nonzero origin;
- 8/16/32-bpc;
- alpha;
- save/reopen;
- repeated random frame requests.

## Adding algorithm code

Keep the existing host lifecycle and replace only the copy operation with a typed internal render core.

Do not mix algorithm rewrite, parameter-system rewrite and MFR enablement in one change.

## Enabling MFR

Follow 12-RECIPES/02-MFR-MIGRATION.md.

Required before setting PF_OutFlag2_SUPPORTS_THREADED_RENDERING:

- state inventory;
- thread-safe render path;
- third-party dependency review;
- repeated MFR stress;
- MFR off/on pixel comparison;
- cancellation;
- memory trend;
- lock review.

## Verification command

Use scripts/check_native.py against the exact SDK for syntax/type checks, then compile/link in the SDK project and run host fixtures.

Record the host result in VERIFICATION/evidence; do not replace NOT RUN with PASS after syntax checking.

## Verification boundary

Current evidence is syntax/type level for the supplied SDK baseline. Host ROI/pixel/MFR acceptance remains open.
