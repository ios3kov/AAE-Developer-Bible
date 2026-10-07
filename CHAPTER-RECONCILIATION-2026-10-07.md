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

## Scripting demo semantic correction

Read ScriptUI chapter, Object Model chapter and authored demo rig. Original
slider-only opacity expression ignored the newly created keys. Now `value + slider`
with clamp preserves their visible role; checks canSetExpression and busy queue.
Expected opacity at t0/t1 is50/100 for slider50. Key interpolation remains LINEAR,
not an ease authoring walkthrough. UI architecture recommendations are distinct
from this standalone IIFE; the source is not a reusable command-layer implementation.

## Evidence record follow-up

Read test-evidence, evidence/acceptance, host-verification and clean-machine chapters
together with worked Gain pack and actual GainPixel source. Added downloadable
authored plan JSON with predeclared 8/16-bpc values, null observations and no invented
raw evidence. Portable structure/arithmetic tests validate the document, not renderer.
Source does clamp RGB and retain alpha; semantic RGBA arrays are not PF_Pixel layout.
Actual project JSON evidence is linked separately with immutable hashes and private
raw-data limits. Upgrade/rollback design is explicitly NOT_RUN, not a release PASS.

## AEIO / Artisan reconciliation

Read both overviews, native-integration companions, working registration guides
and reference-workspace guides together. Reread supplied AE_GeneralPlug.h:2782–2819,
IO.cpp:985–1112 and Artie.cpp:1611–1674. Registration fragment now uses actual PR
API symbols and A_Version product parameter; IO const table arguments match header.
Reference ownership distinguishes host specs from module options.

Found IO HAS_AUX_DATA advertised but provider slots not populated in zero-initialized
function block; documented, not accepted as auxiliary support. IO memory-id and
Artie death-hook registration occur after module/renderer registration; neither
proves rollback on later failure. Licensed workspace routes are not standalone
implementations. No codec/scene/host runtime claimed.

## Platform workflow follow-up

Read macOS/Windows GPU, packaging, CI and production-pipeline chapters together
with debugger chapters and supplied SDK25.6 SDK_Invert_ProcAmp project custom-build
commands. Windows ARM64-conditioned CUDA command uses x64 host compiler; reported
as a source limitation, not a successful build. CUDA `-use_fast_math` means explicit
numeric policy is necessary. Mac embedded Metal generation and obsolete tool path
remain source facts, not current Xcode execution evidence.

Added own-file upgrade/rollback designs for each platform with candidate/prior/
installed/restored identities, stopped-host boundary and conflict refusal. CI routes
bind source/SDK/toolchain, inspected machine/slices and symbols to candidate/signing/
package transitions. No installer, GPU, Windows or signing execution claimed. These
are scoped follow-up results; remaining platform rows require complete related-page
and version-source reconciliation before full closure.

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

## Validation boundary

Portable codec and scripting safety checks do not emulate AE SDK callbacks.
Strict generated docs/freshness validate publication consistency, not API semantics.
Evidence ledger records performed checks; licenses remain owner-undecided.
