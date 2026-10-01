# Recipe — CPU/GPU equivalence

## Goal

Prove that each claimed GPU backend implements the same effect semantics as the CPU reference within a predefined numerical tolerance.

GPU support is not accepted because the GPU selector runs or because output looks similar.

## 1. Freeze the semantic reference

Before GPU tuning, freeze a known-good CPU implementation and its fixtures.

Record:

- product commit/hash;
- AE build;
- pixel format;
- parameter vector;
- input fixture hash;
- expected CPU output.

If CPU semantics are still changing, equivalence results are unstable.

## 2. Define comparison metrics before looking at GPU output

For integer/exact paths, exact equality may be appropriate.

For float/GPU paths define:

- max absolute channel error;
- RMS/mean error;
- alpha-specific threshold;
- allowed count/percentage above threshold;
- NaN/Inf policy.

Tolerance chosen after the failure is not a test specification.

## 3. Use diagnostic inputs

Include:

- black/white/mid-gray;
- primary/secondary colors;
- horizontal/vertical gradients;
- one-pixel impulse;
- checkerboard;
- transparent colored edges;
- partial alpha;
- odd frame sizes;
- HDR negative/positive values where 32-bpc semantics allow them.

Natural photographs alone hide edge/indexing bugs.

## 4. Test parameter boundaries

For every important parameter:

- default;
- minimum;
- maximum;
- values around branch boundaries;
- animated values;
- combinations that change kernel/path.

Do not compare only defaults.

## 5. Match render context

CPU and GPU comparisons must use the same:

- frame/time;
- project color settings;
- input;
- output bit depth;
- parameters;
- ROI/request;
- host version.

Otherwise the diff mixes algorithm and environment.

## 6. Preserve raw comparison evidence

For each failed frame save:

- CPU output;
- GPU output;
- absolute-difference image;
- threshold mask;
- worst pixel coordinates/values;
- summary metrics.

This turns a visual mismatch into actionable data.

## 7. Common mismatch classes

### Alpha/premultiplication

RGB can look correct while alpha or transparent RGB is wrong.

### Clamp/order

CPU may clamp before an operation while GPU clamps after.

### Coordinate/origin

ROI, nonzero origin or odd sizes expose indexing assumptions.

### Precision

Different instruction ordering can create acceptable low-bit float drift; it must remain inside the predefined tolerance.

### NaN/Inf

Explicitly define how invalid floating values are handled. Do not allow backend-specific accidental behavior.

## 8. Lifecycle/fallback

GPU correctness also includes setup/setdown and fallback.

Test:

~~~text
GPU available
→ GPU render
→ device/setup failure injected or unavailable
→ CPU fallback / supported error path
→ subsequent render remains valid
~~~

No stale gpu_data or device resources after setdown.

## 9. MFR + GPU

If both features are claimed, test them together.

Look for:

- shared device state races;
- frame/instance mix-up;
- unsafe caches;
- cancellation;
- device teardown while work exists.

Passing CPU MFR and single-frame GPU separately is not enough.

## 10. Performance comes after correctness

Only after equivalence passes:

- kernel time;
- upload/download;
- synchronization;
- setup;
- total frame time;
- crossover by resolution.

A faster wrong result is a correctness failure.

## Acceptance gate

For every claimed GPU backend and pixel depth:

- comparison fixtures pass predefined tolerance;
- alpha passes independently;
- odd/ROI cases pass where relevant;
- no NaN/Inf regression;
- setup/setdown pass;
- CPU fallback/error path passes;
- MFR combination passes if both are advertised.

See [Render correctness](../10-TESTING/02-RENDER-CORRECTNESS.md) and [Performance](../10-TESTING/04-PERFORMANCE.md).
