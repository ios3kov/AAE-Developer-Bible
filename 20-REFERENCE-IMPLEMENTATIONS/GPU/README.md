# GPU effect reference path

Status: **SDK sample workspace: Effect/SDK_Invert_ProcAmp / RUNTIME-NOT-CLAIMED**.

Materialize the exact licensed SDK sample:

~~~bash
python3 scripts/materialize_sdk_examples.py "/path/to/SDK/Examples" --only gpu-effect
~~~

## Why use the SDK sample shell

GPU effect support spans more than one render function:

- GlobalSetup capability declaration;
- GPU device setup;
- device-specific capability flags;
- GPU data lifetime;
- pre-render/render selectors;
- GPU world format/ownership;
- device setdown;
- kernel build assets/toolchain.

These details vary by SDK and platform, so the Bible keeps the official sample project/plumbing rather than inventing a replacement build shell.

## CPU oracle first

Before changing GPU math:

~~~text
known-good CPU algorithm
→ deterministic fixtures
→ fixed numeric tolerance
→ GPU implementation
→ automated comparison
~~~

Do not develop CPU and GPU semantics independently.

## Capability declaration

A GPU support flag in GlobalSetup is only the first gate.

Device setup must also report what the actual framework/device can render. The final path must handle a device/backend that cannot support the effect.

Do not advertise GPU support based only on compile-time macros.

## gpu_data lifetime

Treat device setup data as product-owned state with explicit device lifetime.

~~~text
GPU_DEVICE_SETUP
→ create device resources / gpu_data
→ GPU renders use them
→ GPU_DEVICE_SETDOWN
→ release
~~~

No render may use gpu_data after setdown.

## World ownership

GPU worlds/buffers are host/API-owned according to the relevant checkout contract. Do not free them with an unrelated allocator.

Keep every checkout/checkin/release pair visible.

## CPU fallback

Test unsupported/failing GPU path.

Expected behavior must be defined:

- host selects CPU render;
- product returns a supported capability/error path;
- no half-initialized device state remains.

A GPU-only crash is not an acceptable fallback.

## Correctness fixtures

At minimum compare:

- 8/16/32 where claimed;
- alpha;
- gradients/edges;
- odd dimensions;
- ROI/origins where supported;
- parameter boundaries;
- NaN/Inf policy for float;
- repeated render.

Use 12-RECIPES/04-CPU-GPU-EQUIVALENCE.md.

## MFR combination

If MFR and GPU are both public claims, test them together.

Look for shared device-state races, cancellation, cross-frame buffer reuse and teardown while requests are in flight.

## Performance

Profile:

~~~text
world preparation
→ upload/translation
→ dispatch
→ kernel
→ synchronization
→ download/conversion
~~~

Kernel time alone is not end-user render time.

## Build/release

GPU dependencies/assets need the same architecture/signing/package discipline as the main plug-in.

A Universal macOS plug-in with a one-architecture nested GPU/helper dependency is not Universal in practice.

## Verification boundary

This reference explains an SDK sample workspace without claiming GPU execution. Materializing the SDK sample and compiling it does not prove a modified product kernel, fallback or performance. Those claims need results for the identified product artifact/backend/device; their absence is an evidence boundary for this guide.
