# Поглавная сверка — 2026-10-07

Это результаты фактически прочитанных страниц и связанного source, не blanket
approval всего репозитория. C означает editorial coverage, не runtime success.

## Effect state block

Read together: lifecycle, memory/flatten, anatomy, parameter model; Minimal Gain
EffectMain.cpp; authored VersionedState.h and portable tests; capability and
AE→Effect pages. Exact SDK AE_Effect.h:1961–2169 reread.

| Core page | Результат | Осознанная граница |
|---|---|---|
| 01-ARCHITECTURE/01-LIFECYCLE.md | C: recovery/partial failure route linked | Product runtime not claimed |
| 02-EFFECT-PLUGINS/01-ANATOMY.md | C: identity/flags/version table aligned with source | No SDK project shipped |
| 02-EFFECT-PLUGINS/02-PARAMETERS-UI.md | C: arbitrary ownership/selectors, ID distinctions, schema migration | Codec not callback adapter |
| 14-NATIVE-INTEGRATIONS/04-EFFECTS.md | C: storage route points to canonical chapter | Capability overview, not dispatcher |
| 15-COMMUNICATION/01-AE-TO-EFFECT.md | C: borrowed value and selector distinction aligned | No hidden cache/persistence guarantee |

Corrections: arbitrary type ID and parameter disk ID are different fields, not
necessarily unequal integers. New UI parameter needs new disk ID; new payload
field keeps arbitrary parameter ID and evolves wire schema. Codec encode assumes
validated input explicitly. Gain bounds 0…4/default1 and 8/16-bpc-only source agree
with illustrative spec; deep flag only, outflags2=0, no sequence state.

## AEGP/source follow-up

Further source read: CompLayerRecipes.cpp, EffectStreamRecipes.cpp,
RenderQueueRecipes.cpp and MenuTool.cpp. Documented exact source limits:
fixed comp settings; bounded LayerID list can silently truncate; ApplyEffect disposes
ref rather than reverting applied effect; queue helper lacks preflight/path readback/
rollback; MenuTool is ping, not target mutation. Walkthrough recommends caller work
without attributing it to these snippets. Compiler/runtime not rerun here.

Read RenderRecipes.cpp, KeyframeRecipes.cpp, AegpOwners.h, HostCallbackGuard.h,
generic-bridge protocol chapter/template and queue chapter. Render cleanup returns
secondary failure only if primary absent; destructor fallback ignores cleanup errors.
Keyframe recipe owns values and batch but borrows stream, uses CompTime, does not
set interpolation or supply callback guard. Generic Ping is illustrative; reload
stub now refuses instead of reporting fake success. Per-recipe review remains open
for other AEGP recipes; this entry does not close the whole block11 tracker.

## Validation boundary

## SmartFX follow-up

Read SmartFX chapter, auxiliary chunk section and actual
`20-REFERENCE-IMPLEMENTATIONS/Effect/SmartFX-MFR/SmartFxMfr.cpp` plus README.
Source is pass-through: ID1, copy request/result extents, WorldTransform copy,
early checkin normal-error path, no MFR flag. Math blur/temporal walkthrough is
not its implementation. Source null-world rejection differs from illustrative
temporal empty-input-as-black policy and is now explicit. Catch-all is an ABI
boundary, not an early-checkin RAII owner for callback exceptions. No native build
rerun or host ROI/depth/empty-input success claimed. These distinctions are reviewed;
full block7 pixel/channel cross-page acceptance is still separately pending.

Portable codec and scripting safety checks do not emulate AE SDK callbacks.
Strict generated docs/freshness validate publication consistency, not API semantics.
Evidence ledger records performed checks; licenses remain owner-undecided.
