# Effect ↔ AEGP bridge

Status: **sample-derived / host-test-required**.

The supported direct native path is `AEGP_EffectCallGeneric`: the AEGP finds an installed effect instance and sends a versioned POD message through the Effect's generic selector. Keep the ABI in `Protocol.h` C-compatible, fixed-width and versioned.

See `15-COMMUNICATION/03-AEGP-TO-EFFECT.md` for the complete call flow and ownership rules. Do not pass STL objects, C++ exceptions or process-local pointers across a persisted/shared ABI.
