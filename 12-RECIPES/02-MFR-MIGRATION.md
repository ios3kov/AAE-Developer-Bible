# Recipe — migrate an existing effect to MFR

1. Disable/not set MFR support flag.
2. Inventory every global/static/singleton.
3. Inventory writes to global/sequence state during render.
4. Inventory third-party library global state.
5. Move scratch to frame-local structures.
6. Convert reusable tables to immutable state.
7. Replace unsafe cache with explicit concurrent/cache API design.
8. Ensure no lock survives a host callback/suite call.
9. Create MFR stress project.
10. Compare MFR off/on output.
11. Run repeated renders and cancellation.
12. Enable MFR support flag.
13. Measure scaling and lock contention.
14. Ship only if correctness + stability + performance all pass.
