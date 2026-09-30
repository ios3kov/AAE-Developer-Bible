# PICA provider ↔ consumer bridge

Status: **sample-derived / host-test-required**.

Two native modules can communicate through a versioned PICA suite. `SharedSuite.h` is the ABI contract. The provider registers the suite with the host's suite registry; the consumer acquires it by exact suite name/version and releases it after use.

See `15-COMMUNICATION/04-PLUGIN-TO-PLUGIN-PICA.md` and `19-NATIVE-CODE-FOUNDATION/01-SUITE-ACQUISITION.md`. Treat the suite struct as a C ABI: POD-compatible arguments, explicit versions, documented ownership and no exceptions across the boundary.
