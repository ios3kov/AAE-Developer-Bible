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

Additional bounded operations: OneD temporal ease, new UTF-8 text output with
close-error preservation/race caveat, and own-section settings readback. Pinned
Property/Settings guide and live ExtendScript File open/write/close reviewed.
Upstream temporal/spatial wording inconsistencies retained explicitly; settings
reported byte limits not generalized to every host. No execution of new fragments.

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

Pixel/color chapter reread with actual GainPixel source and auxiliary descriptor/
chunk contract. Gain uses clamp then integer cast (truncation), not the chapter's
optional round-to-nearest formula; the formula is explicitly a design alternative.
PF_Pixel16 white32768, ARGB field order and semantic RGBA plan arrays agree.
Exceptional float/output calibration guidance is separate from Gain's integer-only
implementation. Removed empty duplicate heading. This review does not establish
new color conversion, ROI math implementation or auxiliary runtime output.

## Validation boundary

### Completion follow-up: SmartFX / pixels / auxiliary

Read the complete SmartFX, pixel/color and auxiliary chapters together with the
CPU/GPU equivalence recipe and actual SmartFX Copy/Minimal Gain sources. Corrected
the ambiguous sentence that made checkout ID sound like an effect identifier.
Added the source-scope table in the canonical SmartFX chapter: Copy has no halo,
temporal dependencies, snapshot, GPU or MFR flag; NULL rejection differs from the
walkthrough's selected empty-input policy. Ordinary cleanup and exception boundary
remain distinct. Pixel chapter now directly documents Gain's clamp/cast truncation
with a distinguishing input, not merely the optional rounding formula.

This review reconciles these authored examples and explanations against the
already recorded SDK source contracts. It does not establish new SDK, renderer,
auxiliary source qualification or host evidence. Other tracker rows remain open
until their related-page review is recorded.

### Completion follow-up: foundation composition

Read suite acquisition, RAII ownership, undo and callback boundary chapters with
the actual RenderRecipes/KeyframeRecipes sources. Added the render operation's
borrowed-options/world and owned-receipt lifetimes, ordinary primary-error policy
and fallback-checkin diagnostic limit. Keyframe recipe's ordinary cleanup does
not establish exception unwind safety. Undo guidance now explicitly separates
EffectRef disposal and footage adoption from safe mutation compensation; the
operation table is a recommended command-layer design, not shipped transaction
code. No new SDK declaration or host result introduced.

Also read all four foundation headers, overview and portable test source. Added
two caller prerequisites visible in the code: template type/name/public version
must match because typed acquisition is a cast, and callback fallback must be
nonzero to avoid success after exception. Failed replacement acquisition resets
the former owner; it is not a transactional service upgrade. Existing stub tests
cover local mechanics, not host legality. Foundation page closure refers only to
the applicable editorial questions and these explicit limitations.

Owner decision during completion: keep the authored material without a reuse
license for now. NOTICE preserves the earlier record and states the new decision;
editorial readiness does not grant reuse rights.

Portable codec and scripting safety checks do not emulate AE SDK callbacks.
Strict generated docs/freshness validate publication consistency, not API semantics.
Evidence ledger records performed checks; authored reuse license remains intentionally
not granted by the owner (see NOTICE), not an unresolved editorial decision.

## Remaining audit material closure

Read remaining GPU/audio, AEIO/Artisan, compatibility, ScriptUI, native panel,
errata, RAII and CEP bootstrap/staging material alongside current authoritative
chapters and owners. Topic-by-topic transfer/non-transfer decisions are in
[audit reconciliation](AUDIT-BRANCH-RECONCILIATION-2026-10-07.md). Added owner reset
hazard, matrix scope/identity/failure route and non-colliding HTML source download.
Historical build result and current protocol are preserved without old duplicate
reports or unsupported manifest compatibility. This closes branch review, not
all remaining chapter tracker rows or final freeze.

## Effect render / cache / UI completion reconciliation

Read complete SmartFX, pixels, auxiliary, MFR, GPU, audio and Drawbot chapters;
memory/performance architecture; threading/ownership companions; MFR migration
and CPU/GPU equivalence recipes; bounded ElasticGridFX incident record. Copy/Gain
source comparison is recorded above; GPU and UI walkthroughs retain the dated
SDK sample-review provenance, not a new claim of direct proprietary source review.

| Closed core pages | Reconciled result | Limit retained |
|---|---|---|
| SmartFX / pixels / auxiliary | Halo/origin/time IDs; actual Copy scope; Gain truncation; channel type/geometry and mandatory checkin | Math/DSP recommendations are not new render implementations |
| Memory / MFR | Receipt independent of primary error; borrowed cache value; request scratch; shutdown quiescence | No concurrency or leak run |
| Performance architecture | Route attribution, core/export/Preview timings and N×scratch | Case study is PROJECT-REPORTED, not replicated |
| GPU / CPU-GPU equivalence | Metal source route, negotiation versus execution; no assumed CPU retry; numeric policy and fallback fixtures | Backend build/platform details retain scoped source limits |
| MFR migration | Inventory → snapshots → cache → candidate flag → observed overlap/output checks | Product acceptance criteria, not Bible runtime gate |
| Threading / data ownership | Generation is not worker cancellation; shutdown dependency; phase-specific cleanup replaces generic checkout rule | No universal suite thread-safety or lifetime promise |
| Audio | Bounded float32 arithmetic/range and independent audio checkout | No matching bundled AUDIO_RENDER dispatcher; field wiring remains explicitly limited |
| Custom UI / Drawbot | Owned drawing objects versus borrowed supplier/surface; hit/drag/persistence/Undo observations separated | Interaction design and async-manager limits explicit, no shipped gesture implementation |

These thirteen rows close applicable editorial axes against recorded contracts and
current examples. Removing empty verification headings improves section scope.
No C++ implementation changed; no new compilation, AE execution, audio/UI/GPU
result, MFR repair or performance result is inferred from this reconciliation.

## Cookbook composition follow-up

Read cookbook00–15 with all six recipe translation units and BibleAegpCommon.h,
code guide and project/render automation. Eight rows closed in this block:
automation, how-to, compositions, masks, text/markers, memory/Undo/persistence,
lifetime/threading and recipe index (index scenario/source axes L). The remaining
cookbook rows keep their prior status until recorded
closure. Existing per-source reconciliation above remains valid.

Found and corrected unconditional EndUndoGroup after failed Start in the how-to
fragment. Balance-only UndoGroup does not expose Start/End errors; constructing it
cannot serve as mutation authorization. Added fixed-comp source scope; bounded
mask failure and existing-marker write flows; helper composition limits and actual
code/evidence route table. Corrected the automation table's stale wording that
read the historical TRUE defect as current. These are editorial/source comparisons,
not new API signatures, compiler evidence, host mutation or exception-safety tests.

## Remaining cookbook rows — closure

Eleven remaining cookbook rows closed using the complete chapter00–15/six-recipe
comparison recorded above, plus function map, overview, local evidence and source
guides read in this pass. No blanket SDK26.5/header audit is implied. The selected
function map now directs exact-signature work to the target SDK (25.6 baseline),
not unconditionally 26.5, and lists current versus deliberately older source suites.

Project queries/partial count; LayerID truncation/context; apply/dispose/mutation;
static OneD/expression restrictions; CompTime batch/ordinary versus exception cleanup;
footage adoption/proxy/replace; frame options/receipt/read-only world; stopped queue,
named enum/readback and partial item creation are reconciled against actual helper
scope. Added direct frame-copy/output calibration link and selection/model/view
failure route. Guide fallback remains design only (source axis L); map/overview are
route indexes (scenario/source axes L). No authored mask/text/footage/guide TU invented.

Local evidence/source guides now link the existing exact-source compiler snapshot
`ef4e90b` separately from identity-incomplete 2026-09-30 evidence. No compiler rerun
or attribution of historical PASS to every later publication head. All cookbook
core rows now C or explicit L; other native integration/hook/bridge rows remain open.

## Remaining AEGP/native integration closure

Parent `b20806b`. Read complete hooks, host flows, PICA, AEGP tools, keyframers,
native panels, BlitHook, AE→AEGP, generic-call, plug-in PICA and native/script/panel
chapters together. Read actual MenuTool.cpp, Protocol.h, SharedSuite.h and scalar
KeyframeRecipes.cpp; matching working/reference guides and portable protocol test.
SDK declarations/sample observations retain the dated registration, streams,
panels/BlitHook and PICA source-review provenance: no new direct proprietary-source
review or target-SDK compiler run claimed by this pass.

Eleven core rows close editorially; BlitHook scenario/source axes remain bounded L.
Added initializer→command/update/idle→shutdown ownership/failure table. MenuTool is
ping, has no idle/worker/target mutation; ordinary degraded return and exception
fallback are distinct. Generic caller design now names ConvertCompToLayerTime and
explicit non-success sentinel: actual Protocol.h defaults result_code to zero.
PICA shared header is declarations only, not a provider/consumer; public ABI,
publication failure, caller-buffer ownership and separate release errors clarified.

Scalar helper borrows stream/arrays, uses CompTime and ordinary End(FALSE/TRUE),
not interpolation/ease/Undo/cancel/exception-safe batch ownership. Working/reference
diagrams now put optional metadata after successful finalization and fresh index
resolution. Native panel teardown now establishes worker/callback quiescence before
destroying reachable controller state; cancel/generation/timeout do not prove it.
Hybrid command ordering, unknown-outcome retry and late target revalidation are
separate from response correlation. BlitHook retains synchronous-copy versus
unqualified async protocol boundary. No C++ implementation changed; no host result.

Next queue: scripting → platforms/compatibility → testing/distribution/templates
→ index/source/link reconciliation and final freeze. No new audit branch or mandatory
host test introduced. Local publication/portable results are in [ledger](VERIFICATION.md).

## Scripting completion reconciliation

Parent `1054917`. Read all four scripting pages, script→AE companion, three
standalone JSX lessons, ScriptUI reference source/guide and existing portable
import/queue tests together. Five core rows now C or index-bounded L. Pinned
FootageItem guide at `7137a990` fetched/read for replace/new FileSource,
interpretation preservation, media attributes and separate sequence replacement.
Other per-member/version/provenance boundaries retain the existing dated records.

ScriptUI source now returns plain partial-result data with separate Undo-close
error, validates/snapshots immediate targets and proposed names, rechecks project/
queue/comp, restores button state and initializes layout for either root. No
deferred scheduler or stable-ID persistence invented. Added eight fake-host portable
scenarios and CI step; they exercise JavaScript control flow, not ExtendScript or
real ScriptUI/AE behavior. Standalone prefix renamer remains a separate limited IIFE.

Corrected blanket dialogs-before-Undo claim: import template prompt occurs after
owned object creation inside Undo; source only reads back path, not settings/format.
Fixed comp duration/fps and cleanup dependency limits explicit. Replace is a worked
design, not shipped script. Rig checks expression resolution at t0, not numeric
assertions/all frames; fixed expression names versus script matchNames and literal
escaping/engine limits explicit. Deferred progress/cancel/stale-target behavior is
documented separately from synchronous source. No host run or runtime support claim.

Next: platforms/compatibility → testing/distribution/templates → final freeze.
