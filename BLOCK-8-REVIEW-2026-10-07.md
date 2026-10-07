# Block 8 — MFR/cache/GPU implementation routes

Added complete receipt/error/cancel flow, canonical geometry key design and owned
versus borrowed cache value distinctions. GPU Metal walkthrough separates host
device and effect pipeline ownership, eligibility from execution, and failure from
assumed CPU retry. Performance distinguishes route attribution, native throughput,
ordinary host export, Preview fill and playback. Basis: existing exact SDK 25.6
Compute Cache / GPU source reviews; new examples are recommendations, not runtime.

Remaining reconciliation includes case-study primary incident records and platform
routes. No concurrency, Metal execution or speedup is newly claimed.
