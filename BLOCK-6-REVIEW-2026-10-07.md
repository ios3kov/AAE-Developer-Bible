# Block 6 — Effect state and arbitrary data

Reviewed together: lifecycle, anatomy, parameters, memory/flatten guidance,
Effect capability map, AE→Effect communication and canonical Minimal Gain source.
Native baseline: SDK 25.6 build 61, local licensed `Examples/Headers/AE_Effect.h`
1961–2169, `UI/ColorGrid/ColorGrid.h`, `ColorGrid_Arb_Handler.cpp`.

Added storage selection, exact arbitrary selector/union map, input/output ownership,
bounded persistence and v1→v2 lesson, disk-ID versus arbitrary-type-ID distinction,
Reset/old-project/future-schema policy and source/PiPL identity table.

Findings: actual enum is singular `PF_Cmd_ARBITRARY_CALLBACK`, despite plural header
comment. Compare enum has named ordering values beyond simplified 0/1 comment.
The authored codec is deliberately not a complete SDK callback adapter.
Runtime callbacks, project migration and Undo remain RUNTIME-NOT-CLAIMED.

Portable codec checks v2 roundtrip, v1 migration, all truncated prefixes, future
schema, invalid range, null input and unchanged destination on failure.
CI results belong to the published revision, not inferred from local checks.
