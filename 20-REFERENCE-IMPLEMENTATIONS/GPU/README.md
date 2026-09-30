# GPU effect implementation path

Status: **SDK sample workspace: `Effect/SDK_Invert_ProcAmp`; host GPU-test pending**.

The implementation is deliberately based on Adobe's version-matched GPU sample because kernel build dependencies, PiPL flags, GPU device callbacks and generated assets vary by SDK. Materialize it with:

```bash
python3 scripts/materialize_sdk_examples.py "/path/to/SDK/Examples" --only gpu-effect
```

Keep the sample project and replace the CPU/GPU math only after CPU reference and tolerance tests exist. Do not enable GPU flags in a custom binary without checking both `GLOBAL_SETUP` and `PF_RenderOutputFlag_GPU_RENDER_POSSIBLE`.
