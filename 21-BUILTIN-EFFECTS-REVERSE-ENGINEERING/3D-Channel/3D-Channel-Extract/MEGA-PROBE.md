# ACX Mega Probe

Build: `ACX-MEGA-20260930-01`.

One-run, fail-soft runtime collector built on the host-validated ACX Edge/Render v04 path.

It preserves the successful edge AA and Render Queue export workflow and adds a capability sweep for selector values 1–8. Unsupported scenarios are recorded as `UNAVAILABLE`/`BLOCKED` instead of fabricating auxiliary data or aborting the whole run.

Evidence boundaries:
- selector write/readback and sampled output do not prove the underlying private FourCC callback;
- current fixture cannot manufacture Object ID, Material ID, UV, normals, datatype mismatch or missing-channel footage;
- MFR is not claimed without a public verifiable control/readback path;
- project GPU setting is recorded, not treated as proof of effect-level GPU execution;
- source AEP is never saved by the collector.

Run with the existing validated `3dextract.aep` / `DEPTH_TEST` fixture and return the entire generated `AE_Edge_Render_ACX-MEGA-...` folder as ZIP.
