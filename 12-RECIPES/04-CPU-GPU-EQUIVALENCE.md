# Recipe — CPU/GPU equivalence

## Goal

Prove that every claimed GPU backend implements the same product semantics as the CPU reference within a predeclared numerical tolerance.

Performance comes after correctness.

## 1 — freeze the reference

Choose a known CPU implementation and artifact version.

Record:

- git SHA;
- binary hash;
- AE build;
- project/fixture version.

Do not change CPU semantics while evaluating GPU differences without explicitly updating the reference.

## 2 — define fixtures

Include:

- gradients;
- impulse pixels;
- checkerboards;
- transparency;
- colored transparent edges;
- min/max parameters;
- odd dimensions;
- nonzero origins/ROI;
- HDR negative/positive float values for 32-bpc;
- temporal cases if relevant.

Natural images can supplement, not replace, diagnostic fixtures.

## 3 — define tolerance before results

For each depth/backend define:

- max absolute RGB error;
- alpha error;
- RMS/mean error;
- allowed count above threshold;
- NaN/Inf policy.

Exact copy-like effects may require exact output.

## 4 — capture CPU output

Render the same frame/settings to a comparison-friendly representation.

Avoid lossy codecs.

Store reference hash/metadata.

## 5 — capture GPU output

For each backend/device class:

- same project;
- same frame/time;
- same parameters;
- same color settings;
- same output representation.

Record backend/device/driver.

## 6 — compute differences

Report:

~~~text
max abs diff
RMS diff
alpha max diff
pixels above tolerance
worst pixel coordinates/values
~~~

Generate a heatmap/threshold mask on failure.

## 7 — investigate semantic causes

Typical differences:

- clamp order;
- integer normalization;
- premultiply/unpremultiply;
- half/float precision;
- coordinate origin;
- edge sampling;
- texture interpolation mode;
- color transform applied in one path only;
- different rounding.

Do not raise tolerance until the cause is understood.

## 8 — repeat across BPC

Test every mode claimed:

- 8-bpc;
- 16-bpc;
- 32-bpc.

Do not infer 16/32 correctness from an 8-bit result.

## 9 — ROI and odd sizes

For SmartFX/GPU paths test:

- partial region;
- empty region;
- single pixel;
- odd width/height;
- cropped/nonzero origins.

Many GPU indexing bugs hide on standard HD dimensions.

## 10 — MFR

If MFR and GPU are both claimed, repeat equivalence under concurrent rendering.

GPU correctness in single-frame preview is not enough.

## 11 — fallback

Force or simulate:

- unsupported device;
- GPU initialization failure;
- backend unavailable;
- allocation failure where testable.

Expected behavior must be defined:

~~~text
safe CPU fallback
or
clear supported failure
~~~

Never return an uninitialized/partial frame as success.

## 12 — performance only after PASS

Once equivalence passes, benchmark transfer, kernel and synchronization cost.

A GPU backend that is correct but slower may still be useful for other reasons, but that decision must be explicit.

## Release evidence

Store CPU/GPU diff report with artifact/environment identity described in 10-TESTING/06-EVIDENCE-AND-ACCEPTANCE.md.
