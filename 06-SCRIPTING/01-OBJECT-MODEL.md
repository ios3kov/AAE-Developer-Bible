# After Effects scripting object model

## Current scripting delta — review 2026-10-07

Source snapshot: [scripting changelog](https://github.com/docsforadobe/after-effects-scripting-guide/blob/7137a990db4bd8dc9f5869b8ca431c7dfed52bdc/docs/introduction/changelog.md).
These are **ExtendScript DOM introduction versions**, not native SDK generations
or UXP availability. DOCUMENTED/source designs; no new host runtime observed.

| Introduced | Operation and contract | Safe workflow |
|---|---|---|
| 26.0 | Property.propertyParameters / valueText: dropdown strings / selected text, read-only | Use numeric value for selection and strings for display; labels are not durable/localization-independent IDs |
| 26.0 | PropertyGroup.addVariableFontAxis(axisTag) on ADBE Text Animator Properties only | Discover actual font designAxesData; add valid 4-character axis; reacquire invalidated indexed-group properties; use actual font bounds, not universal wght100–900 |
| 26.3 | LayerCollection.addParametricMesh(name, meshType); ParametricMeshLayer and mesh/bevel options | Validate comp/type before Undo; create, read back layer type/mesh, report partial result; do not replace unavailable mesh with solid as equivalent |
| 26.3 | Camera FocusAreaWidth/NearFarBlurMultiplier | Advanced3D-only; property presence does not prove active renderer supports desired image |
| 26.5 | GuideOptions, typed enums, getGuideAsObject and object overloads | Full-state readback and explicit units; never persist raw guide enum integers across versions |
| 26.5 | layerInputStage/inputLayerAndStage, setters and cycle-safe query | Require LAYER_INDEX property; revalidate source/index/stage after structural mutation |

### Guide edit: partial update without destroying units

Preconditions: selected intended Item/Layer; valid current guide index; AE26.5+
API actually available. Read `getGuideAsObject(index)` to show current state.
Create `new GuideOptions()`, set only `color = [0,0,1]`, then call
`target.setGuide(index, options)` within an Undo group. Read back full state; verify
color and unchanged orientation/positionType/position/pinned. Older positional
form is **setGuide(position, index)**, reversed arguments! Do not turn a percentage
guide into pixels accidentally. Structural insertion/removal invalidates index
selection; re-list before mutation. Undo grouping is not transactional rollback.

Scripting guide warns orientationType/positionType integer values differ between
AE versions: compare `GuideOrientationType` / `GuidePositionType` constants, not0/1.
If constants or object getters unavailable, refuse fidelity-preserving edit or offer
explicit lossy pixel-only operation; never assert identical semantics.

### Layer input stage: source pair, not just property.value

[Property reference](https://github.com/docsforadobe/after-effects-scripting-guide/blob/7137a990db4bd8dc9f5869b8ca431c7dfed52bdc/docs/property/property.md)
documents `inputLayerAndStage` as `[layerIndex, stageIndex]`;0 means no source layer.
`setInputLayerAndStage(layerIndex, stageIndex)` changes both in one Undo step;
returns nothing, so do not impose UXP Application boolean-success behavior.
`setLayerInputStage(stage)` changes stage only. Non-LAYER_INDEX property throws.

Concrete conservative command: late resolve target property and source layer in
its comp → validate integer index0..numLayers and LAYER_INDEX → snapshot old pair
→ use documented SOURCE constant and combined setter → read back both. SOURCE
is documented always cycle-safe. For richer stages re-query
`getInputStageCycleSafeLimit()` with the relevant current source; do not compare
sentinel integers using a guessed numeric ordering. An old-source safe limit does
not certify a proposed different-source pair. If allowed-stage policy is unclear,
do not offer that mutation. Readback failure leaves possible mutation; no blind retry.

### Variable font axis: discovery before creation

Set the actual installed variable font on a copied TextDocument and write it back.
Inspect `FontObject.designAxesData`; validate requested tag/range. Resolve Text →
Animators → intended animator → `ADBE Text Animator Properties`; addVariableFontAxis
only here. Save necessary indices, reacquire group/property after indexed additions,
set bounded value/keyframes, verify keys and render-font availability separately.
`ADBE Text Variable Font Spacing` appears only after an active axis; its dropdown
affects character spacing compensation, not a generic font substitution fix.
Missing font/axis: stop without silently selecting another font. Source:
[PropertyGroup](https://github.com/docsforadobe/after-effects-scripting-guide/blob/7137a990db4bd8dc9f5869b8ca431c7dfed52bdc/docs/property/propertygroup.md).

This closes the scoped26.x changelog delta, not a full historical scripting/expression
member audit. Mesh shape/options source:
[ParametricMeshLayer](https://github.com/docsforadobe/after-effects-scripting-guide/blob/7137a990db4bd8dc9f5869b8ca431c7dfed52bdc/docs/layer/parametricmeshlayer.md).

## Сквозные automation операции

### Character/paragraph/composed-line accessors — full review2026-10-08

Full pinned [CharacterRange](https://github.com/docsforadobe/after-effects-scripting-guide/blob/7137a990db4bd8dc9f5869b8ca431c7dfed52bdc/docs/text/characterrange.md),
[ParagraphRange](https://github.com/docsforadobe/after-effects-scripting-guide/blob/7137a990db4bd8dc9f5869b8ca431c7dfed52bdc/docs/text/paragraphrange.md) and
[ComposedLineRange](https://github.com/docsforadobe/after-effects-scripting-guide/blob/7137a990db4bd8dc9f5869b8ca431c7dfed52bdc/docs/text/composedlinerange.md)
read. Accessors introduced24.3, pasteFrom25.1. They refer to the specific detached
TextDocument instance, not live layer text. Every edit still needs explicit commit
with static/key/time policy and fresh readback; no text host runtime performed.

Concrete mixed-style report/edit: get intended TextDocument → create bounded
characterRange(start,end) → check isRangeValid → read requested attributes, recording
undefined as **mixed/indeterminate**, not0/false/default → edit only requested styles
→ recreate ranges after length change → commit → reacquire and verify actual text/
style/layout. characterStart/end read-only, end exclusive; reading bounds can throw
when invalid. Zero span is insertion point. text read on zero span empty; assigning
text replaces range, empty deletes, equal start/end inserts. Fixed range bounds
don't automatically grow/shrink to match replacement. isRangeValid can later become
true after text grows, but that isn't stable semantic ownership of the original text.

CharacterRange.fillColor/strokeColor setting enables applyFill/applyStroke across
range. Values are RGB floats with possible HDR overbright values, not universally
clamped0..1; mixed reads undefined. Unlike TextDocument, range color reads don't
throw merely because fill/stroke disabled. kerning reads manual amount only, undefined
for metric/optical/mixed auto kern or mixed manual values; assignment selects manual
NO_AUTO_KERN, not a computed optical kerning readback. strokeOverFill is per-character
order and may be overridden by whole-layer All Strokes/All Fills First. Attribute
readback alone doesn't establish final rendering order.

Paragraph styling command: paragraphRange(selectedStart,selectedEnd) → validate →
read characterStart/end → obtain characterRange() once for bounded style edits →
commit/readback. Paragraph range can have equal character bounds only for empty final
paragraph. Derived CharacterRange is **independent** of future parent-range limits,
not a live wrapper; reconstruct after structural edits. CharacterRange excludes
boxText/boxTextPos/boxTextSize/pointText/lineOrientation/baselineLocs/paragraphCount
and nested characterRange/paragraphRange/paragraphCharacterIndexesAt APIs; don't
blindly copy whole TextDocument settings object into it.

Composed-line styling command: freshly composed TextDocument → composedLineRange
→ isRangeValid → characterRange() → requested styling → commit → **reacquire new
TextDocument and line ranges**. ComposedLineRange always has some length; its layout
snapshot remains unchanged during detached text edits, even deleting all text.
isRangeValid verifies bounds, not freshly recomposed layout. Composed lines aren't
paragraphs; don't map paragraph index to wrapped-line index. Derived CharacterRange
is independent and can become invalid. For all-overset/zero-line case report no
composed range rather than indexing0 or claiming text visible.

Each accessor's toString returns creation parameters, not range text, identity or
serialized style. It is safe even when range invalid: use for diagnostics without
reading throwing bounds, but don't eval it to reconstruct user data. Preserve
source/target validity and recreate after pasteFrom as covered below; paste copies
text/style, not guaranteed recomposition. These workflows supply range operations,
not full inherited TextDocument field/overload coverage.

### Full font ecosystem review —2026-10-08

Full pinned FontObject/FontsObject pages reread (source links in font preflight below).
Existing session/revision/glyph/replace workflow remains; this completes the remaining
font descriptor/discovery/default-policy contracts, not all TextDocument styling.
FontObject is a **soft reference**: retaining it doesn't keep native font proxy alive;
after removal any property read can throw. Catch invalid references, re-enumerate on
fontServerRevision change, and never hold one across asynchronous activation unchecked.

Concrete font picker: current revision → enumerate allFonts or filtered lookup
getFontsByFamilyNameAndStyleName/getFontsByPostScriptName → handle empty/multiple
arrays → display postScriptName, familyName/styleName/fullName plus native Unicode
name variants, technology/type/version, writingScripts, substitute/Adobe Fonts status
and variable designVector → explicit candidate selection → revision recheck and late
fontID resolution → assign/commit and verify actual font/layout. ASCII versus native
names are display/disambiguation, not proof one is file basename. location can be
empty; don't infer missing font or redistribute font bytes from path/isFromAdobeFonts.
Font licensing/embedding rights are separate from install/lookup success.

fontsDuplicateByPostScriptName (24.6+) gives duplicate groups with primary at0;
first candidate doesn't establish desired file/technology/design instance. Source
getFontsByPostScriptName prose says entry0 used with TextDocument.fontObject while
TextDocument.fontObject must be reviewed on its own; don't generalize tuple ordering
into exact-font persistence. getFontsByPostScriptName may **create a previously absent
variable font instance** when prefix matches. Even a lookup can change font ecosystem;
recheck revision, don't claim every discovery call is side-effect-free.

Variable picker: hasDesignAxes gates axis workflow; familyPrefix is variable-only;
fontsWithDefaultDesignAxes returns one default instance per unique variable dictionary.
otherFontsWithSameDict (25.1+) enumerates related variable instances, empty for ordinary
font or single instance. Dictionary identity doesn't guarantee equal designVector or
appearance. technology and type are distinct CTFontTechnology/CTFontType enums,
writingScripts CTScript array isn't guaranteed glyph support for every Unicode member.
Font version String is diagnostic, not binary hash or supported host-version matrix.

25.1+ fallback report: getCTScriptForString(text,preferredCTScript) returns contiguous
range counts chars and ctScript; preferred breaks ambiguous membership ties, empty
text → empty array. Validate accumulated range bounds against intended text and
retain index/Unicode policy; don't derive grapheme/glyph/layout counts from this API.
getDefaultFontForCTScript exposes fallback mapping but guarantees **neither all nor
any glyphs** for that script. Preflight selected text with hasGlyphsFor and qualify
shaping; default lookup isn't a successful-font-substitution report.

Intentional fallback-policy edit: save current getDefaultFontForCTScript mapping →
choose non-variable FontObject (variable rejected) and explicit user consent →
setDefaultFontForCTScript → read mapping → report changed boolean. false means mapping
unchanged, not failure. null resets to **application-launch default**, not necessarily
the prior user mapping; restore captured font only while valid. Roman default also
reinitializes Character panel after style reset. Restoring environment policy doesn't
undo text already typed/substituted under that policy.

favoriteFontFamilyList/mruFontFamilyList (24.6+) accept unsorted family-name arrays,
empty clears. These alter user's Character/Properties UI lists, not project font
availability. Snapshot/merge/restore only for intentional operation, don't reset as
hidden picker initialization. pollForAndPushNonSystemFontFoldersChanges (24.6+) checks
known Adobe non-system folders; true means detected and **async update scheduled**,
not font installed/ready, false no known change. Observe later revision, re-enumerate
with bounded retry/timeout policy and expose pending result; no synchronous wait or
specific completion callback guaranteed. Do not copy/install fonts as part of report.

Pinned intro says Adobe sync cannot be disabled, later freezeSyncSubstitutedFonts24.6
explicitly disables attempts: use versioned later contract, retain historical intro
scope. No font installation/polling/default mutation or runtime observed here.

### Typed value objects and current light/mesh options — review2026-10-08

Full pinned [GuideOptions](https://github.com/docsforadobe/after-effects-scripting-guide/blob/7137a990db4bd8dc9f5869b8ca431c7dfed52bdc/docs/other/guideoptions.md),
[KeyframeEase](https://github.com/docsforadobe/after-effects-scripting-guide/blob/7137a990db4bd8dc9f5869b8ca431c7dfed52bdc/docs/other/keyframeease.md),
[LightLayer](https://github.com/docsforadobe/after-effects-scripting-guide/blob/7137a990db4bd8dc9f5869b8ca431c7dfed52bdc/docs/layer/lightlayer.md) and
[ParametricMeshLayer](https://github.com/docsforadobe/after-effects-scripting-guide/blob/7137a990db4bd8dc9f5869b8ca431c7dfed52bdc/docs/layer/parametricmeshlayer.md)
read. Source-design review; no light/mesh image or host execution.

GuideOptions fields are optional; setGuide changes only supplied fields. orientation
uses HORIZONTAL/VERTICAL, positionType PIXEL/PERCENTAGE; position finite, clamped
±100000 pixels or **±300 percent**, not normalized0..1. color is RGB0..1;
pinned means opposite edge (horizontal bottom, vertical right), not a generic locked
flag. GuideOptions.orientation differs from guides-array orientationType spelling.
Concrete center guide: new options → VERTICAL/PERCENTAGE/50/color/pinned explicit
→ add on intended Item/Layer → returned index/full readback. No current typed constants
before26.5; older pixel fallback must be offered as different lossy capability.

KeyframeEase(speed,influence) uses influence0.1..100 and speed in property's own units,
not a universal normalized curve factor. Build separate incoming/outgoing ease objects,
apply correctly shaped arrays via setTemporalEaseAtKey, then keyIn/OutTemporalEase
readback. Editing detached ease object's speed/influence alone isn't writing a key.
Do not apply three ease entries to spatial Position just because value has3 components;
the earlier temporal-shape rule is authoritative for that operation.

Environment light command: validate LightLayer and actual renderer/capability →
choose same-comp **2D** source layer → lightType=LightType.ENVIRONMENT → lightSource
assignment → read back type/source and inspect representative image. lightSource
introduced24.3 for HDR/EXR sources;25.2 expands to any2D video/still/precomp layer.
3D source throws; don't convert user's source to2D silently. PARALLEL/SPOT/POINT/
AMBIENT are other lightType values with different option relevance. LightSource
is an actual layer link, not File path or AVLayer.environmentLayer legacy switch.
API presence/readback doesn't verify renderer/environment lighting quality.

Mesh edit command26.3+: validate actual ParametricMeshLayer → read parametricMeshType
→ choose allowed shape and confirm topology-changing edit → set type → reacquire
type-specific parametricMeshOptions / applicable parametricBevelOptions → change only
supported intended fields → assign through documented getter/setter route → read back
and qualify geometry/output. Collection constructor table says MeshType while mesh
attribute documents **ParametricMeshType**: use actual published attribute enum and
validate installed constructor contract, don't invent alias equivalence.

| Shape | Mesh fields | Bevel fields |
|---|---|---|
| Cube | width,height,depth,smoothingAngle | radius,sides |
| Sphere | radius,sides,sliceCaps,sliceStart,sliceEnd,smoothingAngle | Not documented |
| Plane | width,length,cornerRadius,cornerSides | Not documented |
| Torus | ringRadius,pipeRadius,ringSides,pipeSides,caps,sliceStart,sliceEnd,smoothingAngle | Not documented |
| Cone | topRadius,bottomRadius,height,sides,topCap,bottomCap,sliceCaps,sliceStart,sliceEnd,smoothingAngle | topRadius,topSides,bottomRadius,bottomSides |
| Cylinder | radius,height,sides,topCap,bottomCap,sliceCaps,sliceStart,sliceEnd,smoothingAngle | radius,sides |

Torus public list names **caps**, unlike sphere/cone/cylinder sliceCaps. The page
lists fields but not complete numeric bounds/units, defaults, object construction or
partial-update semantics. Don't manufacture radius/range/sides declarations or assume
GuideOptions-style patch behavior. Retain full readback snapshot for assignment;
if safe option reconstruction isn't established for target build, disable that edit
while retaining validated shape creation/type operation. Inherited property list isn't
proof every AVLayer operation is meaningful for parametric geometry.

### Property tree inspection and structural mutation — review2026-10-08

Full pinned [PropertyBase](https://github.com/docsforadobe/after-effects-scripting-guide/blob/7137a990db4bd8dc9f5869b8ca431c7dfed52bdc/docs/property/propertybase.md)
and [PropertyGroup](https://github.com/docsforadobe/after-effects-scripting-guide/blob/7137a990db4bd8dc9f5869b8ca431c7dfed52bdc/docs/property/propertygroup.md)
read. Concrete inspector: current layer identity → resolve explicit named root groups
via property(matchName) → branch propertyType leaf/indexed/named → enumerate indexed
children1..numProperties and recursively record parent path/type/occurrence/index
→ bounded output with missing/null/invalid diagnostics. **numProperties counts indexed
properties**, not every named layer property: a loop over layer.numProperties isn't
a complete transform/text/camera inventory. Resolve known named roots separately;
don't claim arbitrary host-property completeness from one recursion algorithm.

property(name) returns null if string child missing; property(index) requires current
valid bounds. Lookup is one hierarchy step, not a slash-separated recursive path.
Use canonical matchNames (source example ADBE Masks differs from table's ADBE Mask
Parade; prefer established ADBE Mask Parade). MatchName identifies property type,
not unique repeated effect/animator instance. parentProperty is null on Layer;
propertyDepth0 on Layer. propertyGroup(countUp) ascends1..depth, default1; depth-level
lookup can return Layer. Don't call propertyGroup(0) as invented root helper.

isEffect/isMask classify groups; elided means organizational group hidden in UI, not
absent children. isModified means changed since creation, not dirty-since-save or
tool ownership. selected changes UI; prefer selectedProperties arrays to repeated
full-tree selection sampling. active is read-only layer video gate (never true for
audio-only) or property enabled observation. canSetEnabled guards enabled assignment;
no effect eyeball → don't set blindly. Enabled isn't final pixel/audio visibility.
name is display metadata; writable for indexed-group children (Layer naming has its
own inherited semantics), not arbitrary named-group children. propertyType is listed
read/write in source but no type-conversion operation described: treat as discriminator,
not supported way to turn Property into PropertyGroup or author a new property type.

Concrete effect-stack edit: resolve layer/ADBE Effect Parade and intended occurrence
→ snapshot matchName/order/parameters and confirm requested duplicate/reorder/delete
→ check indexed-parent precondition → duplicate() or moveTo(validIndex)/remove()
→ reacquire **all affected siblings and descendants** from layer → verify types/order/
values → report partial outcome. duplicate returns new PropertyBase; moveTo/remove
return nothing. Removal recursively removes group's children; text animator is a
documented removal exception. No operations on arbitrary fixed transform children.
Adding/reordering/removing invalidates references: even old sibling's parameter can
be invalid after another effect removal. Never keep handles across structure change
or silently use old index to target a now different instance. Re-evaluate expressions,
matte/effect stage choices and visual result separately. canAddProperty is preflight,
not transaction; use addProperty/addVariableFontAxis recipes above with reacquisition.

DOCUMENTED/operation design; full pages read, no property-stack runtime performed.

### AVLayer: matte/source/render switches are independent contracts

Reviewed2026-10-08: full pinned
[AVLayer](https://github.com/docsforadobe/after-effects-scripting-guide/blob/7137a990db4bd8dc9f5869b8ca431c7dfed52bdc/docs/layer/avlayer.md).
DOCUMENTED/source designs; no matte/retime/source/coordinate runtime result.

Concrete23.0+ matte assignment: late resolve recipient and intended same-comp AVLayer
matte → reject self/cycle under product policy → snapshot trackMatteLayer/type
→ setTrackMatte(matte, ALPHA/LUMA or inverted variant) → read back layer/type/
hasTrackMatte and inspect intended output. Since23.0 matte isn't layer-order-dependent;
isTrackMatte says a layer is used as matte, not ownership or exclusivity. Legacy
trackMatteType setter isn't recommended for new scripts. Older-host adjacency path
requires explicit reordering/qualification, not an identical modern API claim.

removeTrackMatte detaches while **preserving type**; legacy assignment of NO_TRACK_MATTE
detaches and resets type. setTrackMatte(null, validType) detaches and sets that type.
Source warning says NO_TRACK_MATTE invalid/no-op yet example includes a null/NO_TRACK_MATTE
call: baseline uses removeTrackMatte for preserve-type removal, never relies on the
ambiguous combination. Getter type alone doesn't prove a matte currently attached;
check trackMatteLayer/hasTrackMatte. Return is nothing; no readback → unknown outcome,
not safe blind retry. Matte state doesn't prove image/channel correctness.

Concrete layer-only source replacement: resolve intended AVLayer and current source
→ choose valid project FootageItem/CompItem with cycle/dependency checks → snapshot
timing/transform/source/naming/expression policy → replaceSource(newSource,fixExpressions)
→ read back source/dimensions/name/animation and evaluate affected expressions
→ report partial outcome. This differs from FootageItem.replace, which changes shared
source usages. AVLayer.source is read-only and null for text; don't assign it directly.
Replacing null-layer source doesn't turn it into a visible ordinary layer (source
warning calls state isNull while public Layer attribute is nullLayer); inspect actual
state, don't invent a new writable flag. fixExpressions can be costly and isn't an
all-time semantic correctness proof; plan controlled batch plus deliberate expression
repair/review rather than repeat after exception. isNameFromSource is false for explicit
names or no source; source replacement must not silently enforce naming policy.

Concrete retime: check canSetTimeRemapEnabled → snapshot old remap/keys/timing
→ explicit enable → reacquire Time Remap property and inspect host-created state
→ apply typed source-time values at planned composition-time keys → read back and
qualify first/last/reverse/loop frames. canSet isn't proof setter cannot fail; disabling
remap is not a guaranteed way to restore old keyframes. Don't toggle merely to simplify
duration logic. Reject scene detection while remap enabled as described above.

| Layer policy | Operation/readback boundary |
|---|---|
| Audio | hasAudio means source component; audioEnabled is switch; audioActive/audioActiveAtTime check switch, solo and in/out gates. Not PCM amplitude, non-silence or encoded-audio proof |
| Sampling | frameBlending read-only observation; set frameBlendingType NO_FRAME_BLEND/FRAME_MIX/PIXEL_MOTION and consider comp.frameBlending independently. quality BEST/DRAFT/WIREFRAME and samplingQuality BICUBIC/BILINEAR aren't codec quality or universal image parity |
| Blur/effects | motionBlur is layer flag requiring appropriate comp/output policy; effectsActive toggles layer effects. Changing either alters evaluation, not just diagnostic UI |
| Compositing | adjustmentLayer, blendingMode and preserveTransparency are distinct rendering choices. Use actual enum symbols (source notes SILHOUETE_ALPHA spelling); don't synthesize enum integers or equate modes across color/depth contexts |
| Structure/renderer | canSetCollapseTransformation gates collapseTransformation. threeDLayer changes layer dimensionality; reacquire transform properties afterward. threeDPerChar applies only to text. environmentLayer source description is legacy Ray-traced3D and sets threeDLayer true; not verified Advanced3D environment setup |
| Guide flag | guideLayer is layer role, not Item/Layer guide arrays or ViewOptions guide visibility. Don't infer final-output inclusion policy solely from this short DOM property description; inspect chosen render-settings/consumer behavior |
| Geometry | width/height read-only layer dimensions, not transformed comp-space bounds or full effect extents |

### AVLayer coordinate and bounds operations: no expression API substitution

sourceRectAtTime(time,extents) returns source-space top/left/width/height for text/shape
content; extents true is documented for shape bounds expansion. It is not final
post-effects, masked, transformed or motion-blurred alpha bounds. Concrete2D alignment:
read rectangle at intended time → derive four source corners → sourcePointToComp
each corner at current comp time → derive desired comp-space alignment → convert
desired point with compPointToSource where appropriate → edit intended transform
using property/key policy → read back/qualify. Bound samples and establish comp.time
deliberately if current-time conversion is required, restoring UI time afterward.

sourcePointToComp/compPointToSource take finite2-component coordinate arrays despite
syntax lines omitting arguments. On text they reflect only **first character at current
time**; no arbitrary3D/per-character/world-vector mapping guarantee. These scripting
methods aren't expression toComp/toWorld/toCompVec and don't inherit optional time/
vector contracts by similar name. Animated/per-character3D/camera-sensitive alignment
needs an explicit qualified route, not a universal two-point inverse assumption.

calculateTransformFromPoints takes top-left/top-right/**bottom-right**3-component
points and returns object of transform values. Source example names third variable
bl, conflicting with parameter table: use documented bottom-right, record conflict,
don't copy ambiguous example geometry. This is calculation, not mutation. Reject
degenerate/nonfinite geometry under product policy; whitelist returned fields and
resolve proper matchNames/types before applying with static/key/separation policy,
not blind for-in setters over arbitrary object. No documented perspective/planarity/
all-renderer equivalence inferred from its terse description. openInViewer can return
null for text/shapes and changes Layer-panel focus, not coordinate/output correctness.

### Media Replacement controllers: capability then add, not replace media

18.0+ canAddToMotionGraphicsTemplate(comp) checks eligible AVLayer and not-already-added
state. Requires video-switch layer, not adjustment/null; source CompItem or supported
FootageItem, not SolidSource/non-media FileSource. Concrete registration: resolve
intended layer and EGP comp → validate eligibility → canAdd → explicit controller
name/consent → addToMotionGraphicsTemplate or addToMotionGraphicsTemplateAs
→ inspect boolean and EGP state/controller count → report. False can display warning;
don't retry as duplicate operation. This adds a **Media Replacement controller**,
doesn't set alternate media, export a MOGRT or prove target-consumer compatibility.
Names are display metadata; controller index gap documented above remains. Property
alternate-source APIs need their separately reviewed capability/source contracts.

### Layer construction and structural edits — review2026-10-08

Full pinned [Layer](https://github.com/docsforadobe/after-effects-scripting-guide/blob/7137a990db4bd8dc9f5869b8ca431c7dfed52bdc/docs/layer/layer.md)
and [LayerCollection](https://github.com/docsforadobe/after-effects-scripting-guide/blob/7137a990db4bd8dc9f5869b8ca431c7dfed52bdc/docs/layer/layercollection.md)
pages read. DOCUMENTED/source workflows, not executed layer operations.

Concrete creation: validate CompItem/current project and requested type → begin Undo
→ create via typed collection method → retain returned layer plus newly created
project sources → set explicit timing/transform/content → read back → report created
identities and partial outcome. add(item,duration) duration applies only to still
footage, not movie/sequence/audio, and creation honors user start-time preferences.
Never infer startTime/inPoint/outPoint solely from constructor arguments.

| Constructor | Required practical distinction |
|---|---|
| addSolid | Creates SolidSource + project FootageItem + AVLayer. RGB0..1, width/height4..30000, PAR0.01..100. Layer removal doesn't promise source cleanup; remove only owned unreferenced source |
| addNull | Returns AVLayer representing null, with optional still duration; nullLayer observation isn't proof tool ownership |
| addShape | Empty ShapeLayer, not automatically a visible shape/fill/stroke; explicitly add vector groups/content and reacquire indexed properties |
| addText/addBoxText | Horizontal point/paragraph text; String or TextDocument for point source, finite positive box dimensions under product policy; explicitly style/commit/preflight fonts |
| addVerticalText/addVerticalBoxText |24.2+, initial VERTICAL_RIGHT_TO_LEFT orientation; not interchangeable with rotating horizontal text |
| addCamera/addLight | Name and2D centerPoint; camera Point of Interest z initially0. Establish actual transform/type/options deliberately, not assume centerPoint is full3D position |
| addParametricMesh |26.3+, validated MeshType; use mesh recipe above and qualify renderer separately |

Layer.id (22.0+) survives save/reopen but is reassigned on project import. Store project
context and containingComp identity; index1..numLayers changes on structural edits,
PropertyBase.propertyIndex on Layer is undefined. byName returns first/topmost match
or null; never use duplicate display names as stable identity. isNameSet distinguishes
explicit name from source-derived (always true without source); it isn't an ownership
marker. comment/label0..16 are metadata, not behavior/custom RGB. locked is user edit
intent: don't silently unlock targets. selectedProperties can contain groups as well
as leaf values. marker may be null; use marker commit recipe after checking.

Timing plan: snapshot startTime/inPoint/outPoint/stretch → validate finite requested
seconds/range and reverse-time policy → apply deliberate timing edits → read all fields
again. start/in/out ranges are±10800 seconds, stretch percentage±9900; near-zero
positive/negative magnitudes clamp to±1 per source. Reject zero stretch as product
policy rather than invent useful zero-rate behavior. Layer.time is read-only current
**composition** time; not source time. Time remap must be handled separately. shy
affects Timeline display; solo affects evaluation with other solo layers. hasVideo
means eyeball switch exists, not rendered pixels. activeAtTime checks enabled/solo/
in-out gates, not masks/opacity/occlusion/image visibility. autoOrient chooses enum
policy: per-character camera facing requires per-character3D text; don't impose it
on every layer type. Verify requested rendering behavior independently.

Parent command: same-comp child/parent → reject self/ancestor cycle under product
policy → snapshot transforms and parent → choose **preserve apparent pose** via
parent assignment (compensating transform values), or **preserve local numeric values**
via setParentWithJump (possible visible jump) → read back parent/transforms and inspect
relevant times. setParentWithJump() without argument removes parent. Neither simple
description proves every animated pose across time is preserved; don't silently
reparent an animated rig claiming exact all-frame equivalence.

Reorder command: resolve owned layer and same-comp anchor by identity → moveBefore/
moveAfter or moveToBeginning/moveToEnd → reread indices/order and dependent matte/
expression relationships. Returns nothing, not success boolean. remove deletes layer,
not its project source; re-resolve remaining indices. duplicate returns new Layer
without changing UI selection; track returned identity, don't infer selection moved.
copyToComp returns nothing and prepends copy at destination.layer(1), shifting all
old indices. Capture destination state and validate resulting first layer; don't
reuse old target indices or blindly retry. Source retains dated13.6 parent-crash fix
and13.7 effect-copy Undo crash warning; neither current-host safety nor current-host
crash was tested here. Offer qualified-build copy path, not universal Undo-safe promise.

Precompose command: fresh intended same-comp layer identities → resolve unique current
indices immediately before call → confirm moveAllAttributes and resulting structure
→ precompose(indices,name,flag) → record returned CompItem/new parent-comp structure
→ inspect timings/parenting/mattes/expressions/dependencies → report. false is allowed
only for one layer; default true moves attributes into new comp. Operation moves
original layers and creates new comp/instance; not a recursive project-media copy.
An exception can leave structural change; no index-based blind rollback/retry.

applyPreset(File) applies to **currently selected layers of receiver's comp**, not
necessarily receiver; no selection creates a new solid. Concrete safe command:
choose trusted existing .ffx → snapshot selection → explicitly select intended bounded
targets and deselect others → apply once → inspect changes/new effects/keyframes
→ restore selection in finally only for still-existing layers → report separately.
Do not apply once per selected receiver (would reapply to whole selection repeatedly).
Preset isn't read-only data or safe to apply without mutation consent.

doSceneEditDetection (22.3+) rejects non-video/time-remapped video. Choose NONE for
detection-only array of **composition-time** seconds; MARKERS/SPLIT/SPLIT_PRECOMP
mutate respective structures. Snapshot ownership/timing, confirm mode, inspect output
array and new objects; detected cuts aren't ground-truth correctness or frame-delivery
evidence. Relist after splits/precomps instead of continuing stale layer indices.

Layer guides use same model contract as Item guides, but in **layer view**: guides
array0-based, addGuide returns index, removal shifts higher indices, positional
setGuide(position,index) reverses object overload setGuide(index,options). Full-state
getGuideAsObject and units/color/pinning require26.5; preserve enum version boundary
and finite pixel clamp±100000. These methods don't set comp guide visibility or
render an overlay. Use guide recipe above on the intended layer, not its source Item.

### Application/project lifecycle: protect the current document

Reviewed2026-10-08, full pinned
[Application](https://github.com/docsforadobe/after-effects-scripting-guide/blob/7137a990db4bd8dc9f5869b8ca431c7dfed52bdc/docs/general/application.md) and
[Project](https://github.com/docsforadobe/after-effects-scripting-guide/blob/7137a990db4bd8dc9f5869b8ca431c7dfed52bdc/docs/general/project.md).
DOCUMENTED/source designs, no new installed-host, filesystem-save or Team Projects result.

Read-only environment report: app.version/buildName/buildNumber/isoLanguage,
isRenderEngine/isWatchFolder, memoryInUse → app.project → file/revision/numItems,
current color/expression/GPU settings → report. version is alphanumeric, not a float;
locale is AE UI locale, not $.locale. memoryInUse is bytes, not available RAM or a
leak diagnosis. app.activeViewer can be null. Project.activeItem is null with no or
multiple selected items; Project.selection is an array in Project-panel sort order,
not Timeline layer selection. app.fonts/preferences/settings/renderQueue expose
the separately documented objects; don't substitute UXP contracts for these handles.

Concrete switch/open command: choose existing project File and consent/save policy
before mutation → revalidate current app.project and pending jobs → explicitly save
or prompt to save → Project.close(PROMPT_TO_SAVE_CHANGES), stop on false → app.open(file)
or app.newProject → require non-null result → discard old object/property references
and job generation → report actual new project. newProject can prompt and return null;
open() without File prompts and can return null. Never copy source's convenience
close(DO_NOT_SAVE_CHANGES) into an unconfirmed tool. SAVE_CHANGES may need a first-save
dialog. Project.file is read-only/null until saved. Project.dirty and app.openFast
are explicitly research-only; baseline save protection must not rely on either.

Project.save(File) writes to specified location and returns nothing; save() on an
unsaved project prompts. saveWithDialog returns boolean. Choose new owned path or
explicit overwrite consent, then check current project.file and actual artifact;
no return value isn't proof reopen/media completeness. Save is external I/O, not
Undo rollback. app.quit/restart terminate or replace the session: explicit owner
consent and unfinished-job/save handling, never automatic error recovery in a user's
interactive session. saveProjectOnCrash=false removes crash-save opportunity;
don't disable it to hide dialogs. setSavePreferencesOnQuit changes global persistence
policy but this page offers no getter for the old flag: don't promise exact temporary
restoration without a known prior value. app.activate is UI focus, not validation.

### Undo, error suppression and delayed tasks

beginUndoGroup/endUndoGroup return nothing; call end only after successful begin.
Nested group names are ignored inside outer group. Script-end auto-close is documented,
but explicit finally closure allows cleanup reporting. Undo grouping doesn't reverse
filesystem writes, Team Projects publication or non-undoable replaceFont. Report
partial mutation and separate cleanup errors; no blanket transaction guarantee.

beginSuppressDialogs suppresses **script error dialogs**, not every import/save/
overwrite/security prompt. Pair endSuppressDialogs only after successful begin;
its alert argument chooses whether accumulated errors are shown. Preserve app.onError
and restore in finally. Contract type is function-name String/null with error and
severity arguments, despite function-object source example. Use a named persistent
scope callback and retain this discrepancy rather than claim one example proves
portable registration. Callbacks log bounded data; don't quit/restart or recursively
mutate the project as generic error handling.

scheduleTask receives executable JavaScript String, delay **milliseconds**, repeat
boolean and returns task ID. Use a fixed namespaced dispatcher string, not concatenated
user text. Store data in validated job state: generation, expected project, item/layer
IDs, cursor, cancel flag and completed results. Each invocation revalidates project/
targets and queue state, performs bounded work in its own Undo scope, reports partial
outcome, then schedules next chunk. No closure capture, exact timer latency, background
worker or Promise semantics are documented. cancelTask removes queued task by ID;
invalidate generation too so stale callbacks cannot continue. It doesn't undo completed
edits or interrupt an already running render. Never keep one Undo scope across callbacks.

executeCommand uses a GUI menu ID and returns no success result. findMenuCommandId
depends on exact localized menu text and isn't reliable across language packages.
Prefer DOM API; otherwise pin command/build/locale, establish focus/selection and
inspect resulting state. Don't infer cross-release ID stability or use menu Undo
as generic compensation. app.effects discovers matchName/internal version and
localized displayName/category; use matchName for adding effects, and don't confuse
internal version string with vendor product version or rendered compatibility.

External-script protocol: app.exitCode resets to0 at each evaluation; set explicit
positive failure code plus an owned structured report. On Windows command-line -r/-s
can use exitAfterLaunchAndEval (Mac has no effect); Mac AppleScript DoScript returns
exitCode. Neither0 nor app termination proves decoded delivery. Distinguish launch,
script outcome, render outcome and artifact validation. No external launch executed here.

### Project settings: display, color and compute are different policies

Concrete settings command: snapshot only requested fields and project/revision →
validate current capabilities and explain project-wide effect → mutate within bounded
scope → read back and report → qualify representative compositions/output separately.
Project.revision starts1 and increases per user action, not a cross-session content
hash, job ID or documented lock. Recheck after dialogs; unchanged revision alone
doesn't prove external media/font environment unchanged.

| Policy | Contract and safe operation |
|---|---|
| Color | bitsPerChannel only8/16/32. listColorProfiles supplies available workingSpace descriptions; empty String means None. workingGamma only2.2/2.4 and ignored when workingSpace is set. linearBlending, linearizeWorkingSpace and compensateForSceneReferredProfiles are separate settings; don't collapse them into one linear-light switch or declare output color parity from readback |
| GPU | availableGPUAccelTypes can be null with no viewers; require a returned supported enum before setting gpuAccelType. Source prose uses Metal while examples use METAL: use the actual host enum, don't generate numeric constants from labels. Project acceleration isn't an effect GPU-render success or renderer selection |
| Expressions | expressionEngine is extendscript or javascript-1.0, not the script interpreter/UXP runtime. Changing affects project expressions; preflight engine-dependent syntax and evaluate representative times. autoFixExpressions changes broken expressions only when replacement evaluates without errors; not a general rename, all-expression migration or semantic correctness proof |
| Time display | timeDisplayType FRAMES/TIMECODE; framesUseFeetFrames and feetFramesFilmType MM16/MM35 choose display. footageTimecodeDisplayStartType selects0/source media. framesCountType START_0/START_1/TIMECODE_CONVERSION; conversion resets displayStartFrame to0. Project.displayStartFrame only0/1, unlike composition start frame; don't use it to offset keyframe times |
| UI | toolType changes active tool, showWindow changes Project panel, transparencyGridThumbnails changes thumbnails. No hidden camera/layer creation just to select a tool; UI state isn't output configuration |
| Metadata | xmpPacket is RDF/XML String. Parse through available AdobeXMPScript/XMPMeta, modify only owned namespace fields and serialize while preserving unrelated metadata. Never execute packet text; validate size/schema and avoid secrets. Library availability isn't established by a source example |

### Project import, inventory and destructive maintenance

Project.items/numItems/item enumerate all items1-based; rootFolder contains immediate
top-level items only. itemByID is project-scoped; the pinned page doesn't specify its
missing-ID behavior, so catch failure and validate result/type/id. layerByID (22.0+)
returns null when absent and throws for invalid unsigned-integer input. Don't pass
unvalidated strings or store IDs as cross-import identity. Re-resolve after deletion.

importFile takes ImportOptions; returned concrete type must be checked against chosen
import mode (the Project page describes FootageItem even though ImportOptions supports
COMP/PROJECT). importFileWithDialog returns array of created Items or null, not one
footage. importPlaceholder bounds: dimensions4..30000, fps1..99, duration0..10800;
source calls result PlaceholderItem while source hierarchy uses FootageItem/
PlaceholderSource. Inspect actual object/source rather than invent a constructor.
setDefaultImportFolder takes Folder and returns boolean; override lasts until reset
with no args or quit. It has no documented prior-value getter: resetting override isn't
exact restoration of an unknown prior user override. Validate Folder, not a File
returned by Folder(path) for an existing file. Import doesn't mean decoded media PASS.

reduceProject(keepItems), removeUnusedFootage and consolidateFootage are whole-project
maintenance, returning removed counts. They are **not owned-item cleanup primitives**.
Use explicit backup/copy and fresh keep-set confirmation before reduceProject;
report removed count/current identities and recheck dependencies. No promise this
short public description proves preservation of every expression-linked dependency,
external asset or future template use. Consolidation may remove identities callers
cached; re-inventory. Never run any of these silently after failed import.

### Team Projects: explicit collaboration, no automatic conflict winner

Published methods introduced14.2; API presence isn't an authenticated/service entitlement
or current server-availability check. Preflight isTeamProjectEnabled,
isLoggedInToTeamProject, isAnyTeamProjectOpen/isTeamProjectOpen(name); listTeamProjects
returns available name Strings and excludes archived projects. Names aren't a promised
stable remote ID. Obtain explicit target/description before newTeamProject or
openTeamProject; both return boolean. Don't silently replace the local user's document.

Concrete sharing command: confirm current team project and collaboration intent →
check isShareCommandEnabled → shareTeamProject(comment) → inspect boolean and current
state → report request/result, not universal remote delivery. Sync separately checks
isSyncCommandEnabled then syncTeamProject; false/error doesn't authorize retry or
overwriting local changes. Before conflict handling check isResolveCommandEnabled and
show the explicit policy: ACCEPT_THEIRS replaces local version; ACCEPT_YOURS keeps
local version; ACCEPT_THEIRS_AND_COPY copies/renames local then takes shared version.
resolveConflict returns boolean; never choose winner automatically or assert atomic
cloud rollback. Retain diagnostics and avoid blind retry after unknown result.

closeTeamProject returns boolean; require explicit unshared-change policy. For local
handoff convertTeamProjectToProject(File) supports .aep/.aet, **not .aepx**; use a new
owned destination, check boolean and artifact, validate media separately. This is
conversion, not publishing/sharing or collecting all source bytes. No Team Projects
login/cloud/conflict/conversion performed by this review.

### Global performance controls and Watch Folder

setMultiFrameRenderingConfig (22.0+) applies to next render and resets to prior UI
settings at **script completion**. Validate max_cpu_perc1..100, pass100 when disabling;
configure and render in same controlled script, not assume a later scheduled script
inherits it. It doesn't make unsafe effects MFR-safe. disableRendering is app-wide
Caps-Lock-like state; snapshot/restore deliberate temporary changes, not a cancel API.
purge target semantics changed24.3: ALL_CACHES now includes disk, ALL_MEMORY_CACHES RAM
only; older ALL_CACHES RAM only. UNDO_CACHES removes undo history. Never purge silently
as routine cleanup or call cache purge a performance fix without measurement.

setMemoryUsageLimits changes preferences; pinned prose describes old32-bit/low-GB
thresholds, not a verified modern memory allocation model. Do not compute current AE
RAM budgets from it or promise exact restoration absent prior-value access. Performance
reports should record actual host build/settings, not infer support from these enums.

watchFolder(Folder) starts network rendering; pauseWatchFolder(true/false) pauses/
resumes **search**, endWatchFolder ends mode, isWatchFolder reports dialog/watching.
These aren't general filesystem watcher callbacks or proof outstanding outputs stopped.
Validate trusted owned network folder/jobs and explicit operator intent; don't enter
mode on a shared arbitrary directory or end someone else's active watch job. Check
rendering outcomes/artifacts independently. parseSwatchFile(File) parses ASE data,
not an ICC conversion: branch RGB/CMYK/LAB/Gray schema, validate channel domains before
using RGB, preserve non-RGB values for an explicit conversion pipeline. Don't feed
CMYK or LAB numeric tuples directly into bgColor/SolidSource.color.

### Item identity and composition preset: resolve before changing

Reviewed2026-10-07: full pinned
[Item](https://github.com/docsforadobe/after-effects-scripting-guide/blob/7137a990db4bd8dc9f5869b8ca431c7dfed52bdc/docs/item/item.md) and
[CompItem](https://github.com/docsforadobe/after-effects-scripting-guide/blob/7137a990db4bd8dc9f5869b8ca431c7dfed52bdc/docs/item/compitem.md)
pages. DOCUMENTED/source operation design; no composition or MOGRT executed.

Item.id survives saving/reopening the same project, but project import assigns new
IDs. Persist project context plus item ID, not an index/name as global identity.
Item.dynamicLinkGUID identifies Dynamic Link; it is not a generic lookup or delivery
API. Item.typeName is localized display text: use concrete CompItem/FootageItem/
FolderItem checks, not a translated-name regex. Item.name changes Project panel
metadata. comment is user metadata (limit15,999 bytes after encoding conversion),
not a secret vault or behavior switch. label0..16 indexes user label preferences;
it doesn't assign arbitrary RGB. selected is UI state, not ownership/cleanup consent.

Concrete bin operation: snapshot intended IDs/current parentFolder/name/label/comment
→ validate existing project and destination FolderItem after any dialog → move via
parentFolder and edit only requested fields → read back → report partial mutations.
Item.remove deletes project objects, not disk files; removing a folder recursively
removes its contents. Never implement failed-import cleanup by deleting a nonempty
shared bin. Resolve current membership and dependencies before explicit deletion.

Concrete comp preset: resolve intended CompItem → snapshot requested fields only
→ validate renderer against current renderers array and finite bounded values
→ obtain successful Undo scope → apply requested settings in dependency-aware order
→ read back each field → report changed fields/error/cleanupError. Do not reset
unrequested settings to defaults. CompItem.duplicate returns a new comp with the same
layers; it is not a documented recursive clone of all nested media/compositions.
Track returned identity and shared dependencies before editing a duplicated rig.

| Setting group | Contract and operation boundary |
|---|---|
| Time display | displayStartFrame (17.1+) avoids floating calculation of start frame; displayStartTime is seconds, range -10800..86339 on17.1+, older minimum0. dropFrame changes timecode representation, not frameRate or frame count |
| Timing/range | frameDuration is reciprocal of frameRate. workAreaStart/workAreaDuration are seconds; validate intended interval against comp duration and read both after setting. Work area doesn't automatically set RenderQueueItem timeSpan |
| Renderer/nesting | renderer must belong to renderers (installed modules, not a universal hardcoded list). preserveNestedFrameRate/preserveNestedResolution choose nesting policy, not proof all layers/effects support requested renderer |
| Resolution/background | resolutionFactor is two integers1..99; [1,1] full, [2,2] half. bgColor is RGB0..1; composition background isn't a substitute for an explicit opaque rendered background layer/output-alpha policy |
| Motion sampling | motionBlur is comp switch; shutterAngle0..720, shutterPhase-360..360. motionBlurSamplesPerFrame2..64 concerns Classic3D/shapes/certain effects; motionBlurAdaptiveSampleLimit16..256 concerns2D motion. No universal sample/image guarantee across renderers |
| Preview/UI | draft3d is Composition-panel mode; hideShyLayers changes Timeline visibility, not render eligibility. frameBlending is comp switch, not automatic qualification of layer modes/result |

CompItem.layers/numLayers enumerate1-based layer collection; layer(index),
layer(otherLayer, relIndex), layer(name) are distinct overloads. Validate same-comp
relative reference and current bounds; names can collide and indices shift.
selectedLayers and selectedProperties are **0-based arrays**, the latter includes
PropertyGroup as well as Property. Snapshot selection before structural edits and
re-resolve invalidated property references. activeCamera is the front-most enabled
camera or null; null isn't a failed composition. markerProperty may be null; apply
the marker value/commit workflow only after checking it. openInViewer returns Viewer
or null and changes focus, not output. openInEssentialGraphics is UI activation
returning nothing. CompItem.counters is explicitly research-only, app-wide and
described as doing nothing: not a supported progress counter or documented ledger row.

### Item guides: array indices and model state, not viewer visibility

Item.guides is read-only0-based array. Read fresh state before addGuide/removeGuide/
setGuide; getGuideAsObject requires26.5. addGuide returns the new index; removal shifts
higher indices downward. Delete a prevalidated owned subset descending, then relist;
never persist guide indices as stable IDs. Positional add/move use pixels with finite
positions clamped to±100,000. Preserve26.5 units/color/pinning through GuideOptions,
not a positional rewrite; use the partial-update recipe above. Legacy positional
setGuide cannot change orientation. Current guide state and ViewOptions visibility/
snap/lock are separate operations. Source retains legacy0/1 orientation table while
warning enum integers changed; version-gate legacy pixel path and use current typed
constants for26.5, never one raw-integer mapping across releases.

### Essential Graphics export: explicit project save and filesystem outcome

motionGraphicsTemplateName (15.0+) determines exported filename, not comp.name.
motionGraphicsTemplateControllerCount and getMotionGraphicsTemplateControllerName /
setMotionGraphicsControllerName (16.1+) inspect/rename existing panel controllers.
Names are display metadata, not persistent property IDs. The pinned CompItem page
does **not specify the controller index base**: do not infer it from layer indices
or guess a bulk loop; implementation must first establish the host's controller
index contract. The setter returns String per source, not boolean mutation success.
Adding eligible properties requires separately reviewed Property capability/add APIs;
renaming a controller doesn't add it or certify MOGRT compatibility.

Concrete export design: validate target comp/controllers/fonts/dependencies → choose
safe template name, existing destination folder and explicit overwrite policy
→ confirm project save destination/state → save only with user consent (dirty project
otherwise prompts during export) → exportAsMotionGraphicsTemplate(false, folderPath)
→ inspect returned boolean and expected .mogrt artifact → report separately from
consumer import/render validation. folderPath is a **String folder path**, not output
File or complete filename. Omitted path uses user's common Motion Graphics Templates
folder. true allows overwriting, not versioned/atomic publication; default to false
and don't retry unknown outcomes. Successful export doesn't prove Premiere/font/
media compatibility. Saving the project and exporting a file are external side
effects, not undone by the composition Undo group.

### Script settings and application preferences: separate stores/policies

Reviewed2026-10-07, full6 pages at pinned scripting revision
`7137a990db4bd8dc9f5869b8ca431c7dfed52bdc`:
[Preferences](https://github.com/docsforadobe/after-effects-scripting-guide/blob/7137a990db4bd8dc9f5869b8ca431c7dfed52bdc/docs/other/preferences.md),
[Settings](https://github.com/docsforadobe/after-effects-scripting-guide/blob/7137a990db4bd8dc9f5869b8ca431c7dfed52bdc/docs/other/settings.md),
[View](https://github.com/docsforadobe/after-effects-scripting-guide/blob/7137a990db4bd8dc9f5869b8ca431c7dfed52bdc/docs/other/view.md),
[Viewer](https://github.com/docsforadobe/after-effects-scripting-guide/blob/7137a990db4bd8dc9f5869b8ca431c7dfed52bdc/docs/other/viewer.md),
[ViewOptions](https://github.com/docsforadobe/after-effects-scripting-guide/blob/7137a990db4bd8dc9f5869b8ca431c7dfed52bdc/docs/other/viewoptions.md),
[System](https://github.com/docsforadobe/after-effects-scripting-guide/blob/7137a990db4bd8dc9f5869b8ca431c7dfed52bdc/docs/general/system.md).
Source workflows, no host-preference/process execution performed.

Concrete tool preference: namespaced section + schema-version key →
Settings.haveSetting → getSetting → strict bounded parse/validation → default on
absent/invalid value with visible diagnostic → saveSetting only on user change
→ getSetting readback. Values are strings; parse boolean explicitly, not
Boolean("false"). Settings values persist between sessions of that installation,
not automatically across AE versions or inside project files. Migration needs
explicit user-approved import, schema compatibility and conflict policy.
Source warns get/save above1999 bytes throw (observed AE15.0.1): conservative
small settings only; this dated observation isn't proof exact limit in every later
build. Use owned UTF-8 file with checked write/close for larger documents, never
preferences as a secret vault. Internal section prefix is Settings_; do not prepend
it twice when using Settings API.

Preferences.havePref checks existing section/key in chosen PREFType before typed
getPrefAsBool/Float/Long/String. savePrefAsBool/Float/Long/String, deletePref,
saveToDisk/reload are application-level operations, not project Undo commands.
Keep PREFType identical for read/write/delete: default MACHINE_SPECIFIC differs
from machine-independent/render/output/composition/text/paint stores. Source prose
says optional third argument generically; typed save signatures actually take
value then optional prefType as **fourth** argument. Follow method signature.

For intentional internal-pref change: whitelist documented target key/build →
record prior existence/value/type/store → explicit consent → typed save → readback
→ explicitly chosen saveToDisk/reload policy → report. Do not blindly reload whole
preferences to refresh one setting while user has unrelated unsaved state. Restore
only owned temporary changes in finally; restore failure is separate error and
restoring a value does not reverse actions already triggered. Never delete entire
sections or alter script security permissions silently. Source doesn't guarantee
every preference takes immediate effect without restart; qualify selected setting,
not extrapolate API readback to actual host behavior.

### Viewer diagnostic preset: UI state, not output settings

Concrete operation: resolve current app.activeViewer, handle null → check Viewer.type
and views array → validate activeViewIndex against0-based array → snapshot selected
View.options fields → set requested channels/checkerboards/exposure/zoom and guide
display flags → read back → optionally restore snapshot after diagnostic. Validate
exposure[-40,40], zoom[0.01,16] (normalized, not integer percent). Re-resolve after
panel closure/focus change; do not act on stale UI references.

Viewer.active / View.active are focus observations; Viewer.setActive / View.setActive
return boolean activation, not render success. Viewer.maximized and activeViewIndex
are user-visible mutations; never force them as hidden prerequisite. Viewer.views
is a JS array, unlike1-based project collections. Viewer.type distinguishes comp,
layer and footage panels. View.options belongs to that view, not all views/comps.

ViewOptions.channels selects ChannelType; checkerboards affects transparency grid;
exposure/zoom affect display. guidesVisibility/guidesSnap/guidesLocked/rulers (16.1)
are view state, not GuideOptions model creation or persistent rendering constraints.
ViewOptions.fastPreview (12.0) throws in Layer/Footage viewer. Source describes Draft
only for legacy ray-traced3D, not universal support in Classic/Advanced3D. Do not
present a historical enum as current renderer capability; gate actual host/renderer
before offering mode. Source examples use equality comparisons, **not assignments**.
UI readback and screenshot are not proof encoded output has changed or final quality.

### External helper invocation: shell text is not a job protocol

System.osName can be blank on Windows7+ per source; $.os is suggested alternative.
System.osVersion / machineName / userName are diagnostic strings, not certified
architecture/OS support matrix. Redact machine/user names unless user approves
diagnostic sharing. No vendor support guarantee inferred from local OS strings.

System.callSystem executes command-line text and returns output text. It doesn't
provide a documented structured exit-code/process handle/cancellation API here.
Don't interpret empty output or text "success" as delivered artifact. Never build
shell commands by concatenating project/marker/user text. Prefer fixed trusted
helper executable with validated file-based request and response; quote arguments
for the actual platform shell and handle spaces/quotes/newlines explicitly.
No single shell escaping function applies unchanged to cmd.exe and POSIX shell.

Concrete helper design: prepare owned bounded request file with job/source identity
→ validate helper path/version and explicit permission → invoke helper using fixed
protocol → read bounded response after it terminates → validate schema/job ID,
explicit outcome and expected files → independently decode/check artifact. Refuse
missing/mismatched response, don't retry unknown outcome. Keep long-running work
out of UI paint/status callbacks; use a designed external service/IPC for cancelable
jobs rather than pretend callSystem has timeout/async semantics. Do not launch a
shell or install software as part of read-only project inspection.

### Proxy workflow and AVItem type limits

Reviewed2026-10-07 at pinned scripting revision
`7137a990db4bd8dc9f5869b8ca431c7dfed52bdc`:
[AVItem](https://github.com/docsforadobe/after-effects-scripting-guide/blob/7137a990db4bd8dc9f5869b8ca431c7dfed52bdc/docs/item/avitem.md).
Logical base classes **AVItem and Item are undefined in ExtendScript**. Validate
actual CompItem/FootageItem constructors and capabilities; `instanceof AVItem`
throws instead of safely filtering project items. AVItem.name changes project display
name, not file name. usedIn is copied membership; refresh after structural changes.
hasAudio/hasVideo indicate source components, not enabled/audible/visible output.

Concrete attach-proxy command: late resolve target CompItem/FootageItem → choose
existing file/sequence and confirm replacement of existing proxy → record old
proxySource/useProxy/interpretation → call setProxy or setProxyWithSequence
→ reacquire proxySource → validate actual type/geometry/timing/alpha → apply intended
proxy interpretation with source gates → explicitly choose final useProxy state
→ report result. Proxy setters enable useProxy automatically and **do not preserve
interpretation**, using preferences and possibly estimated unlabeled alpha. This
differs from FootageItem.replace. A successful proxy assignment isn't preview parity
or proof Render Queue uses proxies: verify render-settings Proxy Use separately.

proxySource is read-only; setProxyToNone removes it and disables useProxy. Toggling
useProxy=false leaves the assigned source available; disabling is not removal.
setProxyWithSolid / setProxyWithPlaceholder create respective typed sources and
enable useProxy, using their own bounds; no filesystem creation/export occurs.
Do not use placeholders/solids as successful media-delivery substitutes. Partial
failure can leave assigned/enabled proxy; report actual state, don't automatically
remove a user proxy as compensation. FileSource.reload isn't proxy reload.

Read/write policy depends on concrete source: CompItem duration/frameRate/frameDuration
are writable; FootageItem timing is read-only through AVItem and changed through
mainSource.conformFrameRate. width/height are writable on comps or solid footage,
not generic movie/still FileSource. Changing shared solid geometry affects usages.
frameDuration/frameRate are reciprocals with floating roundoff; use explicit tolerances.
pixelAspect readback may differ from rounded UI values (e.g.1.33 vs1.33333).
time sets direct preview time, rejecting still footage; not a keyframe or delivery
range setter. footageMissing can mean placeholder as well as missing file: only
read missingFootagePath from a valid FileSource. isMediaReplacementCompatible (18.0)
is an alternate-source capability check with source/cycle restrictions, not blanket
permission for every target Property.setAlternateSource or proxy operation.

### Shape and mask authoring: geometry, feather and UI state

Sources fully read:
[Shape](https://github.com/docsforadobe/after-effects-scripting-guide/blob/7137a990db4bd8dc9f5869b8ca431c7dfed52bdc/docs/other/shape.md),
[MaskPropertyGroup](https://github.com/docsforadobe/after-effects-scripting-guide/blob/7137a990db4bd8dc9f5869b8ca431c7dfed52bdc/docs/property/maskpropertygroup.md).
Concrete rectangle: validate intended layer/mask and coordinate-space policy →
resolve or add ADBE Mask Atom with indexed-group reacquisition → set maskMode ADD,
inverted=false and explicit rotoBezier policy → new Shape with four finite vertices
in path-local coordinates, closed=true and zero tangents → write ADBE Mask Shape
using static/key policy → reacquire/read back vertices/closed/mode → qualify image
separately. Do not cast comp-space points directly into arbitrary transformed layer
or shape-group paths. A visible mask outline is not proof expected rendered coverage.

Shape.inTangents/outTangents are vectors **relative to each vertex**, not absolute
positions; arrays match vertices count. Open path ignores first incoming/last outgoing
tangent. RotoBezier ignores supplied tangents and calculates them; requesting manual
tangent fidelity requires rotoBezier=false. Editing Shape value alone doesn't commit:
write updated object back through the path property. Preserve animated-path policy
and topology intentionally; don't replace all keys via a static setter.

Variable feather arrays are in creation order, not sorted geometric order:
featherSegLocs is0-based segment, featherRelSegLocs0..1 on that segment; move segment
first then relative position. featherRadii can be negative for inner feather;
featherTypes outer0/inner1 cannot change direction after point creation. Preserve
associated entries/counts on geometry edits; do not assume vertex insertion remaps
feather segments. featherInterps uses0/non-Hold or1/Hold; featherTensions0..1 and
featherRelCornerAngles0..100 are different units. If topology changes and a valid
mapping isn't known, refuse fidelity-preserving edit or explicitly rebuild feather
with user-approved loss; do not silently discard it.

MaskPropertyGroup.color is outline **UI color**, not rendered fill. locked prevents
UI edits, not a substitute for tool consent/ownership checks. maskFeatherFalloff and
maskMotionBlur choose respective enums; source type text misspells MakMotionBlur
while values use MaskMotionBlur. Don't invent a new enum from that typo. Feather
falloff and blur flags require output qualification, not inferred image PASS.

### Marker authoring: commit values and preserve unrelated fields

Source fully read:
[MarkerValue](https://github.com/docsforadobe/after-effects-scripting-guide/blob/7137a990db4bd8dc9f5869b8ca431c7dfed52bdc/docs/other/markervalue.md).
Concrete edit: resolve comp.markerProperty or intended layer.marker → find exact
marker time (nearest key plus explicit keyTime check) → get keyValue or create
new MarkerValue → modify requested comment/duration/label only → preserve other
metadata → setValueAtKey/setValueAtTime → reacquire/read back value/time. MarkerValue
is property data, not a live mutation handle or persistent item identity.
Do not overwrite another marker just because its time is nearest to your request.

comment is Timeline text; duration is seconds, not number of keys/frames.
label0..16 (16.0+) refers to label preferences; can't set custom label colors here.
protectedRegion (16.0+) applies to composition markers and reflected nested-comp
protected regions, not ordinary layer markers generally. Don't promise a layer
marker protectedRegion edit supplies responsive-design time protection.
chapter/url/frameTarget/cuePointName/eventCuePoint are format/legacy consumer
metadata; saving them in AE doesn't guarantee current codecs/players export/use them.
Treat URL/comment/parameters as data, never execute code or open links automatically.
getParameters returns named key/value object; setParameters stringifies values via
toString and ordering isn't UI ordering. Merge user-requested keys into existing
parameters and commit marker value; don't erase unrelated pairs. No secrets should
be stored in markers intended for project/metadata distribution.

### Import/relink: distinguish source replacement from interpretation

Reviewed2026-10-07 at pinned scripting revision
`7137a990db4bd8dc9f5869b8ca431c7dfed52bdc`: ImportOptions, FootageItem,
FolderItem/ItemCollection and all4 source pages. Source links:
[ImportOptions](https://github.com/docsforadobe/after-effects-scripting-guide/blob/7137a990db4bd8dc9f5869b8ca431c7dfed52bdc/docs/other/importoptions.md),
[FootageItem](https://github.com/docsforadobe/after-effects-scripting-guide/blob/7137a990db4bd8dc9f5869b8ca431c7dfed52bdc/docs/item/footageitem.md),
[FootageSource](https://github.com/docsforadobe/after-effects-scripting-guide/blob/7137a990db4bd8dc9f5869b8ca431c7dfed52bdc/docs/sources/footagesource.md),
[FileSource](https://github.com/docsforadobe/after-effects-scripting-guide/blob/7137a990db4bd8dc9f5869b8ca431c7dfed52bdc/docs/sources/filesource.md).
DOCUMENTED for documented members; research-only exceptions below.

Concrete import: choose existing File and sequence policy → ImportOptions(file)
→ canImportAs desired type → set importAs/sequence/forceAlphabetical explicitly
→ Project.importFile → validate returned item/source type and duration/dimensions
→ apply intended supported interpretation → organize into owned FolderItem
→ report created identities and actual source state. canImportAs is a capability
check, not proof all sequence frames exist/decode or import cannot fail. Importing
as PROJECT/COMP can create multiple dependent items; compensation must track actual
created objects, never delete arbitrary project contents on an exception.

ImportOptions.rangeStart/rangeEnd/isFileNameNumbered are explicitly **officially
undocumented research APIs** in guide. Do not label them Adobe public contracts.
Range setters can conflict with forceAlphabetical, reset range on invalid ordering,
or create missing frames past sequence length. Baseline recipe doesn't depend on
them: import verified sequence, then set requested layer/queue range explicitly.
A filename containing digits does not prove a contiguous valid sequence. This
research warning applies even though these members appear in the inventory.

FootageItem.file is null for non-FileSource; mainSource is read-only and replaced
by replace(file), replaceWithSequence(file, forceAlphabetical), replaceWithPlaceholder
or replaceWithSolid. Never assign mainSource/file as a generic relink setter.
FileSource.file is also read-only; FileSource.reload is mainSource-only, not proxy.
For missing source report FileSource.missingFootagePath and AVItem.footageMissing;
do not dereference a null File or claim current local bytes from the missing path.
FootageItem.openInViewer can return null; viewer activation isn't relink success.

Concrete relink: identify intended FootageItem and all affected uses → confirm
new source/type → snapshot old path/type/interpretation and project backup policy
→ replace/replaceWithSequence → reacquire mainSource → compare actual dimensions,
timing, alpha interpretation and representative output → report partial outcome.
Replacement preserves previous interpretation but unlabeled alpha may be estimated;
do not assume automatic interpretation matches delivery intent. Existing layer
usage is affected by replacing shared source. Readback failure does not justify a
second replacement/retry. A missing old file cannot be restored by merely saving
its pathname. Placeholders/solids have separate width/height/fps/PAR bounds; validate
against selected method, not one universal constructor signature.

### Source interpretation: gated fields and dependency order

FootageSource.hasAlpha gates alphaMode/invertAlpha/premulColor relevance. IGNORE
ignores alpha inversion; premulColor applies only to PREMULTIPLIED. A deliberate
alpha change sets mode then applicable fields and reads them back. guessAlphaMode
mutates estimates (no change without alpha), not a correctness oracle. SolidSource.color
is RGB0..1, not pixel buffer or linear/display color equivalence; editing a shared
solid source affects its usages. PlaceholderSource adds no own members; inherited
isStill depends on duration (zero-duration placeholder is still).

FootageSource.isStill gates conformFrameRate/loop/fieldSeparationType/removePulldown;
still sources reject those time-based setters. nativeFrameRate is read-only;
conformFrameRate0 means native only when pulldown is OFF. displayFrameRate is read-only
and, with pulldown, conform rate×0.8. Don't report conformFrameRate as final effective
rate unconditionally. loop requires non-still source and valid count1..9999.

For resetting to native progressive timing: disable removePulldown first, then
field separation OFF, then conformFrameRate0; don't set OFF while dependent pulldown
is active. For requested pulldown: establish appropriate field separation, conform
rate, then selected phase; read back effective rate. highQualityFieldSeparation
requires non-still footage and field separation not OFF. guessPulldown mutates
field separation and phase estimates; only run with explicit intent.
Source prose uses PulldownPhase.OFF while its list says PulldownPhase.RemovePulldown.*:
record inconsistency and verify actual enum on supported host before implementation,
not invent a portable enum namespace. No host execution of that conflict claimed.

### Project bins and owned creation

ItemCollection.addComp creates comp with validated name/dimensions/PAR/duration/fps;
ItemCollection.addFolder creates bin. Collection belonging to a non-root folder
sets created item's parentFolder to that folder. Existing item move uses parentFolder,
not filesystem File/Folder rename. FolderItem.items/numItems/item enumerate immediate
children only; project.items contains all project items. Avoid counting nested
children twice in recursive traversal. Snapshot target identities before moving or
removing items; don't mutate live1-based index traversal and skip shifted entries.
Folder deletion cleanup must be restricted to owned empty bins; don't infer ownership
from a shared name or delete user contents because your import failed.

### Render queue: prepare, arm, execute, validate are separate stages

Reviewed2026-10-07: all5 renderqueue DOM source pages at
`7137a990db4bd8dc9f5869b8ca431c7dfed52bdc`:
[RenderQueue](https://github.com/docsforadobe/after-effects-scripting-guide/blob/7137a990db4bd8dc9f5869b8ca431c7dfed52bdc/docs/renderqueue/renderqueue.md),
[RenderQueueItem](https://github.com/docsforadobe/after-effects-scripting-guide/blob/7137a990db4bd8dc9f5869b8ca431c7dfed52bdc/docs/renderqueue/renderqueueitem.md),
[OutputModule](https://github.com/docsforadobe/after-effects-scripting-guide/blob/7137a990db4bd8dc9f5869b8ca431c7dfed52bdc/docs/renderqueue/outputmodule.md),
[RQItemCollection](https://github.com/docsforadobe/after-effects-scripting-guide/blob/7137a990db4bd8dc9f5869b8ca431c7dfed52bdc/docs/renderqueue/rqitemcollection.md),
[OMCollection](https://github.com/docsforadobe/after-effects-scripting-guide/blob/7137a990db4bd8dc9f5869b8ca431c7dfed52bdc/docs/renderqueue/omcollection.md).
DOCUMENTED/source workflow, no new render/encoded-output result.

Concrete scoped command: validated CompItem → check RenderQueue.rendering false
→ enumerate existing queue and refuse execution if unrelated items are armed
→ choose available render/output templates and new output destination before mutation
→ RQItemCollection.add(comp) → immediately set RenderQueueItem.render=false
→ apply render template → set requested timeSpanStart/timeSpanDuration/skipFrames
→ get outputModule(1) → apply output template → reacquire module
→ configure settable overrides → reacquire module again → set file and read back
→ leave item unarmed for user review. This extends the existing
[import-and-queue example](../16-WORKING-TEMPLATES/jsx-tool/import-and-queue.jsx).

Arming is a separate explicit command: revalidate queue/items/paths/settings → set
owned item.render=true → confirm QUEUED → obtain explicit render confirmation.
RenderQueue.render() blocks until process complete and starts the **queue**, not
only your item. Never silently disable/re-enable other people's queued items or
start while foreign armed items remain. Preparation and filesystem overwrite checks
do not reserve output atomically; recheck before execution and use unique owned
destinations or product-specific collision policy. For sequences check the entire
output pattern/directory, not only one nominal File.

Collection indices are1-based; numItems/numOutputModules count items. RenderQueue.item
reference table says0..numItems, while RQItemCollection explicitly says first index1:
preserve this documentation inconsistency and use1..numItems, not a speculative0
probe. OMCollection.add creates an extra output module; verify every module path,
format and collision independently. RenderQueueItem.outputModules/items are
collections, not plain JS arrays. RenderQueueItem.comp is read-only; to change comp,
remove the owned queue item and create a new one. Never remove foreign items/modules
as compensation. Removal/duplication shifts index-based resolution; don't use stored
queue index as persistent identity across structural edits.

### Settings/templates: local capability, not a portable codec contract

RenderQueueItem.templates and OutputModule.templates expose available local names.
Both applyTemplate calls return nothing; validate membership and read back actual
settings. RenderQueueItem.saveAsTemplate / OutputModule.saveAsTemplate alter local
template libraries; require user intent and collision policy, don't write a template
as a hidden prerequisite. OutputModule.name is display metadata, not a durable ID.
RenderQueueItem.duplicate of DONE becomes QUEUED: immediately disarm a duplicated
item before editing and avoid inherited output-file collisions.

getSetting/getSettings/setSetting/setSettings introduced13.0. Use
GetSettingsFormat.STRING_SETTABLE or NUMBER_SETTABLE to discover applicable writable
settings; SPEC describes possibilities, STRING/NUMBER describe readable values.
Read-only dump isn't a valid write-back patch. RenderQueueItem setting key/value
strings in source examples are English; template names are installation-dependent.
Validate schema/types against the chosen host rather than deriving numeric enums
from UI ordering. Source notes OutputModule Format is readable but not settable
through this interface: select a valid format template, don't promise arbitrary
codec selection via setSettings({Format: ...}).

**OutputModule is invalidated after settings modification** per source warning.
Always re-fetch item.outputModule(index) before further mutation/readback. Failed
setSettings may leave changed settings: reacquire/report actual state, not retry
the whole preparation and create duplicate items. OutputModule.file takes
ExtendScript File, unlike reviewed UXP string-path APIs. Use File/Folder path
handling; don't copy unescaped Windows backslash literals from source examples.
Output File Info supports template/path components; ensure filename pattern matches
movie/sequence format and destination policy. includeSourceXMP is an explicit
metadata/privacy decision. postRenderAction defaults should be selected deliberately:
NONE avoids automatic IMPORT/IMPORT_AND_REPLACE_USAGE/SET_PROXY project mutations.

### Range, status and callbacks

RenderQueueItem.timeSpanStart and timeSpanDuration are seconds in composition time,
not frame count or layer time. Validate positive duration and intended comp range;
read back after template application because template settings may change it.
RenderQueueItem.skipFrames0 is full coverage;1 skips alternate frames, movie frames
have doubled duration. Range length unchanged does not mean every requested frame
was rendered. Do not label a skipFrames preview as full-delivery evidence.

RenderQueueItem.render=true maps to QUEUED, false to UNQUEUED. status also includes
NEEDS_OUTPUT, RENDERING, WILL_CONTINUE, USER_STOPPED, ERR_STOPPED and DONE.
RenderQueue.rendering is true during active **or paused** rendering; paused is not
permission to edit application/queue. RenderQueueItem.onStatusChanged contract is
function-name string/null, although source example assigns function directly.
Use documented named callback in the script's actual persistent engine scope,
record/test build behavior, and preserve previous callbacks. Do not generalize this
example discrepancy into a guaranteed function-object registration API.

Callbacks can call RenderQueue.pauseRendering(true/false) and stopRendering;
cannot mutate queue/application while active/paused. Record small status/error data,
avoid dialogs or heavy processing, then inspect outcome after render returns.
Preserve/restore app.onError and owned onStatusChanged hooks in finally, report
restoration errors separately. Synchronous blocking render does not promise a
browser-like event loop/timer cancellation path. RenderQueue.showWindow is UI only.
RenderQueue.queueNotify / RenderQueueItem.queueItemNotify (22.0) are notification
preferences, not completion callbacks or delivery evidence. RenderQueueItem.logType
selects errors/settings/per-frame logging; startTime and elapsedSeconds may be null
before rendering and aren't artifact identity.

Post-run report: item status, requested range/skip policy, every output module's
actual file/settings, errors and cleanup outcomes. DONE is host completion, not
decoded-file validation. Check sequence frame coverage, dimensions, channel/depth/
codec, timing, nonempty decodable outputs and expected image content separately.
Do not delete partial files automatically unless explicitly product-owned and policy
allows it; preserve diagnostics on ERR_STOPPED/USER_STOPPED.

### AME handoff is not an AE output-module render

RenderQueue.canQueueInAME indicates queued items exist. RenderQueue.queueInAME(false)
queues without starting; true also starts AME processing. Requires AME11.0+ per
source and uses AME's **most recently used preset**; true removes the opportunity
to adjust preset first. Refuse foreign queued items as with AE render. Default to
false and inspect AME destinations/preset before manual execution. Return is nothing,
not a job ID or encoded-file success. AME handoff/request, observed AME job and
validated output are separate evidence. Do not assume AE output-module codec/path
settings transfer unchanged to AME or that duplicate calls are idempotent.

### Property animation: typed plan before mutation

Reviewed2026-10-07 against pinned scripting source
`7137a990db4bd8dc9f5869b8ca431c7dfed52bdc`,
[Property](https://github.com/docsforadobe/after-effects-scripting-guide/blob/7137a990db4bd8dc9f5869b8ca431c7dfed52bdc/docs/property/property.md),
[PropertyGroup](https://github.com/docsforadobe/after-effects-scripting-guide/blob/7137a990db4bd8dc9f5869b8ca431c7dfed52bdc/docs/property/propertygroup.md),
[PropertyBase](https://github.com/docsforadobe/after-effects-scripting-guide/blob/7137a990db4bd8dc9f5869b8ca431c7dfed52bdc/docs/property/propertybase.md).
DOCUMENTED/source operation design, not executed AE animation.

Concrete authoring command: resolve intended layer/property → validate
propertyValueType/canVaryOverTime and existing keys/expression policy → build
finite times and correctly shaped values → show overwrite scope → begin Undo
→ set values → resolve keys by time and verify keyTime → set supported interpolation
→ verify keys/values/interpolation → end Undo with independent cleanup error.
Product policy here requires strictly increasing times (reject duplicates), equal
array lengths and bounded batch size; not an undocumented Adobe uniqueness rule.
For opacity, request times[0,1] and values[0,100], LINEAR. Preserve unrelated keys;
if replacing an interval, explicitly list/removal-confirm only that interval.

Property.setValue only sets a static no-key property; it throws when keys exist.
Property.setValueAtTime creates or updates the key at the requested time;
Property.setValueAtKey requires an existing valid key index.
Property.setValuesAtTimes creates/updates each requested time and requires equal
length arrays; no whole-call transactional rollback is documented. An exception
can leave a partial outcome: refresh keys and report, never blind retry.
These setters return nothing, not boolean success.

Property.nearestKeyIndex is not proof a key exists **at** your time. Check numKeys,
then keyTime with an explicitly chosen numerical tolerance appropriate to product
time representation. Do not round times to frame boundaries unless that is requested
policy. Property.removeKey shifts indices; delete selected keys highest-to-lowest.
Stored key indices do not survive insertion/removal as stable identity.

Check Property.isInterpolationTypeValid before Property.setInterpolationTypeAtKey.
Omitted outType uses inType. For Property.setTemporalEaseAtKey, ease array length
is2 for TwoD,3 for ThreeD, **1 for all other types including spatial vectors**;
do not derive it from value.length. Construct KeyframeEase with valid product values.
Property.setSpatialTangentsAtKey accepts only TwoD_SPATIAL/ThreeD_SPATIAL, matching
2/3-component tangent vectors; temporal easing is not a spatial tangent operation.
Auto-Bezier/continuous/roving policies require their own member checks, not implied
by this scoped LINEAR operation.

### Structural mutation and expression evaluation

PropertyGroup.canAddProperty guards intended matchName before PropertyGroup.addProperty.
Adding to an indexed group recreates it and invalidates existing property references;
save propertyIndex where appropriate and reacquire after subsequent additions.
Text animator is the documented named-group exception. PropertyBase.matchName avoids
localized display names but is a **type identifier**, not a unique instance ID when
the same effect occurs more than once. Resolve intended occurrence/parent and verify
its matchName after index lookup; stale index alone is not identity.

Property.expression assignment evaluates the expression: invalid string generates
error and disables expression; empty string disables without error. Validate
canSetExpression, preserve old string/enabled state for diagnostics, assign, inspect
Property.expressionError and expressionEnabled. A successful initial evaluation
does not establish correctness for all times/assets. Property.valueAtTime(time,true)
reads pre-expression value; false requests evaluated value and can wait for expensive
expressions such as sampleImage. Bound diagnostic samples; don't run full-frame
expression sampling in a UI repaint loop. The Source Text layer-time exception is
described in font usage preflight below.

Property.dimensionsSeparated applies to a separation leader. Before editing Position,
inspect isSeparationLeader/dimensionsSeparated; when already separated use
Property.getSeparationFollower(dim) with0-based dimension and author scalar keys.
Do not toggle separation merely to fit a generic vector setter; separation can
change animation representation and needs explicit product migration policy.

### Font preflight: identity, substitutes and project usage

Reviewed2026-10-07 at scripting source `7137a990db4bd8dc9f5869b8ca431c7dfed52bdc`:
[FontsObject](https://github.com/docsforadobe/after-effects-scripting-guide/blob/7137a990db4bd8dc9f5869b8ca431c7dfed52bdc/docs/text/fontsobject.md),
[FontObject](https://github.com/docsforadobe/after-effects-scripting-guide/blob/7137a990db4bd8dc9f5869b8ca431c7dfed52bdc/docs/text/fontobject.md),
[Project](https://github.com/docsforadobe/after-effects-scripting-guide/blob/7137a990db4bd8dc9f5869b8ca431c7dfed52bdc/docs/general/project.md).
DOCUMENTED/source workflow, no host result claimed.

Concrete read-only preflight: validate project and font API → record
FontsObject.fontServerRevision → flatten FontsObject.allFonts family arrays for
display → read FontsObject.missingOrSubstitutedFonts and Project.usedFonts → report
source font identity and each usedAt.layerID/layerTimeD → recheck revision and mark
stale if it changed. Do not mutate sync policy or activate fonts as a hidden side
effect of a report. Resolve layers by Project.layerByID; skip/report deleted targets.

Critical time-domain exception: **Source Text.valueAtTime expects layer time** in
the usedFonts example, unlike other properties' comp-time usage. Preserve supplied
layerTimeD; don't substitute comp.time or subtract startTime again blindly.

FontObject.fontID is stable only within this application session, may change after
restart. FontsObject.getFontByID can return undefined after removal. Persist font
descriptors, not fontID as cross-launch identity; re-resolve and handle ambiguity.
FontsObject.allFonts groups are not uniquely keyed by family name; duplicate
PostScript names are allowed across technology/writing-script tuples. Never pick
array[0] automatically for a release-critical replacement. Display technology,
writing scripts, designVector and substitute status for user selection.

FontsObject.fontServerRevision changes on installation/removal, substituted-project
open/close, variable instances and English-name sort preference. Cache by this
revision only within the session; a matching revision is not render/image proof.
FontObject.designAxesData gives name/tag/min/max/default; designVector order follows
axes, not alphabetical tag order. Both can be undefined for non-variable fonts.
FontObject.hasSameDict tests variable-font dictionary identity, not equal appearance.
FontObject.postScriptNameForDesignVector returns a name, not installed availability.
FontObject.hasGlyphsFor (25.1+) answers whether **all** characters have glyphs;
false doesn't identify which character, true doesn't prove shaping/layout correctness.

### Project-wide font replacement is not Undo-safe

Project.usedFonts / Project.replaceFont introduced24.5. Plan: fresh usage report →
explicit from/to font choice and backup/save policy → re-resolve both font instances
and project → user confirmation of non-undoable mutation → replaceFont → refresh
usage and text/layout diagnostics. No automatic retry if an exception leaves unknown
outcome. The return is boolean **at least one layer changed**, not a changed-count,
complete glyph-success result or saved-project confirmation.

Project.replaceFont preserves mixed-style ranges but is **not undoable**; wrapping
it in beginUndoGroup cannot provide rollback. Optional noFontLocking=false allows
glyph fallback; true can yield missing glyphs without a complete detection/report
API. For substituted fromFont with identical target properties, documentation says
fallback is suppressed and the option treated as true. A successful replacement
does not establish final glyph coverage. Preflight sampled text with hasGlyphsFor
where available and qualify relevant frames/layout separately.

FontsObject.freezeSyncSubstitutedFonts (24.6) controls automatic Adobe Fonts sync;
FontsObject.substitutedFontReplacementMatchPolicy selects POSTSCRIPT_NAME,
CTFI_EQUAL or DISABLED replacement matching. These are application-environment
policies, not per-layer edits. If a tool deliberately changes them, save old values,
restore in finally, report restoration error separately and don't promise restoration
undoes already completed font activation/replacement.

### Text ranges: detached edit, explicit commit, fresh composition

Source: [TextDocument](https://github.com/docsforadobe/after-effects-scripting-guide/blob/7137a990db4bd8dc9f5869b8ca431c7dfed52bdc/docs/text/textdocument.md),
[CharacterRange](https://github.com/docsforadobe/after-effects-scripting-guide/blob/7137a990db4bd8dc9f5869b8ca431c7dfed52bdc/docs/text/characterrange.md).
TextDocument.characterRange / paragraphRange / composedLineRange introduced24.3.
Character indices start0; explicit end is exclusive, optional end selects one
character; -1 follows current text end. Cannot span final carriage return. Paragraph
and composed-line ranges use their respective indices, not character offsets.

Concrete styling edit: resolve intended Source Text and time/key policy → obtain
TextDocument value → validate start/end against that value → obtain characterRange
→ edit chosen styling fields only → commit with setValue for static property or
explicit key/time route → reacquire TextDocument → verify target styling and text.
Do not overwrite animated Source Text through a generic static setter; do not treat
first-character aggregate style as proof all mixed-style characters match.

CharacterRange.isRangeValid must be checked after edits changing length.
CharacterRange.pasteFrom (25.1) deletes target text then pastes source text/style;
original range bounds stay fixed and a shorter paste can invalidate the target.
Recreate accessors after structural text changes. Validation before paste is not
permission to reuse the old accessor afterward.

TextDocument.composedLineCount is a snapshot from initial composed state; editing
the detached TextDocument does **not** recompose it. It may be zero for all-overset
text. Commit and reacquire before using composedLineRange or reporting line layout.
TextDocument.boxOverflow (24.6) reports some text didn't compose into the box;
don't hide overflow by claiming successful text assignment proves full visibility.
Absent versioned APIs require an explicit older-host path or unsupported report,
not interpreting undefined as no missing fonts/no overflow.

[Import/queue source](../16-WORKING-TEMPLATES/jsx-tool/import-and-queue.jsx): диалоги
input/output диалоги до Undo → canImportAs → import → comp/layer → disabled queue item → exact template
prompt внутри Undo → reacquire → output path readback. Не запускает render и не включает чужие
items. Extension/sequence-pattern согласовать с template вручную; path selection
не доказывает format compatibility. Компенсация касается только созданных objects;
при failed dependent cleanup footage сохраняется для диагностики.

Начать с [demo rig](../16-WORKING-TEMPLATES/jsx-tool/build-demo-rig.jsx): validated
project → create comp/layers → resolve matchNames → set keys/interpolation →
write TextDocument/Shape/MarkerValue → expression resolution → explicit cleanup.
Host runtime не заявлен; syntax ES3 и guide objects не равны support matrix.

Demo expression uses animated `value` plus slider with clamp, so keys are not
silently overridden: slider50 yields expected opacity50 at t=0 and100 at t=1.
`valueAtTime(0,false)` requests post-expression evaluation; expressionEnabled/error
checks establish script-level resolving only, not a complete pixel correctness test.
The script currently creates linear keys; it is not an ease/Bezier authoring example.

Bulk rename: snapshot selected layer objects/old names перед изменением, validate
все proposed names, открыть один Undo group, менять последовательно и сообщать
changed count + failure. Имя не stable identity; не resolve заново по уже изменённому
имени. Partial failure не скрывать return=0 после успешно переименованных слоёв.

Import: выбрать существующий File, проверить `ImportOptions.canImportAs`, задать
importAs/sequence явно, импортировать, настроить interpretation только для подходящего
source, добавить Layer в validated comp. На failure удалять лишь созданные tool-owned
items, если policy это допускает, не чужой project. Replace: validate target FootageItem
и new media до `replace`; сохранить old path/interpretation для diagnostic, но не
обещать восстановление missing media простым Undo. Structural changes в indexed
groups инвалидируют property references: сохранить index и re-query после addProperty.

Queue route: add validated comp → acquire outputModule(1) → проверить доступные
template names → applyTemplate → вновь получить outputModule → установить новый
owned output File → readback path/settings → queue status. Нельзя render в существующий
неизвестный output или считать exit0 доказательством полного набора decoded frames.

File/Folder: permissions на script filesystem/network не предполагать включёнными.
Для UTF-8 text установить encoding до open, проверить return/status, close в finally;
не переписывать существующий file без explicit policy. `app.settings` — preferences,
не project persistence или secret vault. Scheduled chunks хранят generation/job ID,
обрабатывают bounded batch и revalidate target; cancelTask прекращает будущие
invocations, не откатывает уже совершённые изменения. Не держать Undo group
открытым через произвольные scheduled callbacks.

After Effects scripting exposes the host through an ExtendScript object graph. It is a high-level automation API for project structure, timeline state, properties, import and render queue. It is not the same API surface as Effect or AEGP suites.

## Source composition and remaining operation limits — 2026-10-07

| Operation | Actual source | Design / failure boundary |
|---|---|---|
| Bulk rename | [ScriptUI command](../20-REFERENCE-IMPLEMENTATIONS/Scripts/ScriptUI-Panel/AEDeveloperBiblePanel.jsx) snapshots selected layer refs and proposed names, returns changed/total/error/cleanupError | Synchronous, current selection only; not scheduled stable-ID resolution; no rollback or collision-free naming promise |
| Standalone rename | [Small IIFE](../16-WORKING-TEMPLATES/jsx-tool/rename-selected-layers.jsx) prefixes current names and returns count on success | Repeat adds prefix; failure alerts but does not report partial count; not the reusable command above |
| Import + queue | Existing import-and-queue IIFE creates owned objects and disabled queue item | Template prompt occurs after creation inside Undo, not all dialogs before Undo; path readback only, not settings/format verification |
| Rig | Existing build-demo-rig IIFE creates new comp and checks expression resolution | Linear keys; new-comp compensation, no reusable rig command or render proof |
| Replace | Workflow below | Design only: no replacement script shipped |

**Replace workflow.** Snapshot the intended FootageItem and original file/source
interpretation for diagnostics. Choose media before mutation, then revalidate the
same project and target after the dialog; reject a removed/replaced/non-file target
or newly busy queue. `canImportAs` is import preflight, not a guarantee that `replace`
will decode or preserve every media characteristic. Inside one successful Undo
scope call the documented `FootageItem.replace(File)`, re-query the new source and
check intended dimensions/duration/interpretation and dependent layer expectations.
Failure after replacement is partial/unknown until readback, not automatically
restored by Undo or a cached old path. Do not remove the pre-existing footage item
as compensation. This is a worked command design, not executed source.
Source: [pinned FootageItem reference](https://github.com/docsforadobe/after-effects-scripting-guide/blob/7137a990db4bd8dc9f5869b8ca431c7dfed52bdc/docs/item/footageitem.md).
That reference states `replace` creates a new FileSource, updates media-derived
name/dimensions/frameDuration/duration, preserves prior interpretation parameters,
and estimates alpha interpretation for unlabeled alpha. Re-query rather than retain
the old `mainSource` object. Sequence replacement is a separate `replaceWithSequence`
operation, not this single-file workflow.

Import lesson chooses input/output before Undo but prompts for an exact template
after queue creation. User must inspect format, range and output settings before
enabling; code only compares `om.file.fsName`. A new path is not an exclusive
filesystem reservation. The two-second/25fps comp is fixed, not matched to imported
media duration/framerate. If queue removal fails, do not infer all dependent
cleanup succeeded: the source still attempts comp removal and retains footage
when earlier cleanup failures were recorded. These limits are not host observations.

## Mental map

~~~text
app
└── project
    ├── items
    │   ├── CompItem
    │   │   └── layers
    │   │       └── PropertyGroup / Property
    │   │           ├── transforms
    │   │           ├── effects
    │   │           ├── masks
    │   │           ├── text animators
    │   │           └── markers / keyframes
    │   ├── FootageItem
    │   └── FolderItem
    └── renderQueue
        └── RenderQueueItem
            └── OutputModule(s)
~~~

## Collections are 1-based

AE scripting collections are not normal JavaScript arrays. Items, layers, render-queue entries and many property groups use indices starting at 1.

~~~jsx
var firstItem = app.project.item(1);
var firstLayer = comp.layer(1);
~~~

Make conversion explicit when code moves between zero-based JavaScript arrays and one-based AE collections.

## Validate type before use

An active item can be absent, a composition, footage or a folder. Never cast by assumption.

~~~jsx
var item = app.project.activeItem;

if (!(item instanceof CompItem)) {
    throw new Error("Open or select a composition first.");
}
~~~

Apply the same rule to layers, footage, output modules and optional properties.

## Stable targeting

Display names may be localized, changed by Adobe or renamed by the user. For effects and properties, prefer stable match-name identifiers where the scripting API exposes them.

~~~jsx
var effects = layer.property("ADBE Effect Parade");
var slider = effects.property("ADBE Slider Control");
~~~

Use visible names for presentation. Do not make them the only machine identity in a production tool.

For product-owned layers or objects, keep your own stable identifier in deliberate project metadata instead of relying only on a layer name such as "Controller".

## Structural mutation can invalidate references

Indexed property groups are a classic scripting trap. Adding, moving or removing children can rebuild a group and invalidate object references saved earlier.

Risky:

~~~jsx
var fx = layer.property("ADBE Effect Parade");
var a = fx.addProperty("ADBE Slider Control");
fx.addProperty("ADBE Color Control");
// saved reference a may no longer be valid
~~~

Safer:

~~~jsx
var fx = layer.property("ADBE Effect Parade");
var a = fx.addProperty("ADBE Slider Control");
var aIndex = a.propertyIndex;

fx.addProperty("ADBE Color Control");

a = fx.property(aIndex); // reacquire after structural mutation
~~~

Treat host objects as host-owned references, not immortal JavaScript objects.

`numProperties` описывает indexed children, а не все доступные свойства слоя. Часть свойств доступна по имени/match name. Поэтому обычный цикл `1..numProperties` не является полным обозревателем всего layer API: сначала определите нужные roots и область обхода. Источник: [PropertyGroup в закреплённом Scripting Guide](https://github.com/docsforadobe/after-effects-scripting-guide/blob/7137a990db4bd8dc9f5869b8ca431c7dfed52bdc/docs/property/propertygroup.md).

## Undo groups are not database transactions

For user-triggered mutations, group related operations:

~~~jsx
app.beginUndoGroup("Build Rig");

try {
    // validate, then mutate
} finally {
    app.endUndoGroup();
}
~~~

This gives the user coherent undo history. It does not mean an exception automatically rolls the project back.

If partial mutation is unacceptable:

1. validate prerequisites before the first edit;
2. collect errors before running a batch;
3. create resources in a controlled order;
4. explicitly clean up product-owned resources on failure where possible.

Put undo ownership at the command boundary instead of opening nested undo groups in low-level helpers.

## Defensive scripting checklist

Before a destructive or cast-like assumption, verify:

- app.project exists;
- active item exists and is the expected type;
- layer/property index is in range;
- property/effect exists;
- canSetExpression, canVaryOverTime, canAddProperty or another capability is true when relevant;
- input file exists before import/read;
- project has a path before code depends on project.file;
- output directory exists and is writable;
- render-queue references are reacquired after structural changes when required;
- cancel leaves the project in a deliberate state.

For batch tools, validate as much as possible before the first project mutation.

## Import preflight: один файл как footage

Сначала проверьте входной File и допустимый тип импорта. Только затем меняйте проект. Авторский helper ниже получает уже выбранный File; он не открывает диалог и не создаёт проект.

~~~jsx
function importFootageFile(inputFile) {
    if (!app.project) {
        throw new Error("Open a project first.");
    }
    if (!(inputFile instanceof File) || !inputFile.exists) {
        throw new Error("Select an existing file.");
    }

    var options = new ImportOptions(inputFile);
    if (!options.canImportAs(ImportAsType.FOOTAGE)) {
        throw new Error("This file cannot be imported as footage.");
    }
    options.importAs = ImportAsType.FOOTAGE;
    options.sequence = false;

    app.beginUndoGroup("Import footage file");
    try {
        return app.project.importFile(options);
    } finally {
        app.endUndoGroup();
    }
}
~~~

Контракт: [ImportOptions](https://github.com/docsforadobe/after-effects-scripting-guide/blob/7137a990db4bd8dc9f5869b8ca431c7dfed52bdc/docs/other/importoptions.md) и [Project.importFile](https://github.com/docsforadobe/after-effects-scripting-guide/blob/7137a990db4bd8dc9f5869b8ca431c7dfed52bdc/docs/general/project.md). Проверка `canImportAs` не гарантирует успешного чтения: импорт всё равно может завершиться ошибкой. `finally` закрывает undo group, а не выполняет rollback.

Ожидаемые сценарии продукта: отсутствующий файл и недопустимый тип отказывают до mutation; допустимый файл добавляется как отдельный item; повторный вызов не обещает deduplication. Для sequence нужен отдельный сценарий. Уровень примера — **SOURCE EXAMPLE / RUNTIME-NOT-CLAIMED**; выполнение в AE здесь не записано.

## Command layer instead of UI-driven scripting

### OneD temporal ease: самостоятельная операция

Prerequisite: caller passes an already resolved, tool-owned OneD property in a
disposable comp, with no enabled expression and no keys. Caller opens/closes Undo
and compensates only its newly created comp on failure; this helper does not remove
user keys to force eligibility. Source example / AE NOT_RUN:

```jsx
function addEasedOneD(prop) {
    if (!prop || prop.propertyValueType !== PropertyValueType.OneD ||
        !prop.canVaryOverTime || prop.expressionEnabled || prop.numKeys !== 0 ||
        !prop.isInterpolationTypeValid(KeyframeInterpolationType.BEZIER))
        throw new Error("Need unkeyed expression-free OneD property");
    prop.setValuesAtTimes([0, 1], [0, 100]);
    for (var k = 1; k <= 2; k++) {
        prop.setInterpolationTypeAtKey(k, KeyframeInterpolationType.BEZIER,
            KeyframeInterpolationType.BEZIER);
        prop.setTemporalAutoBezierAtKey(k, false);
        prop.setTemporalEaseAtKey(k, [new KeyframeEase(0, 33.333)],
            [new KeyframeEase(0, 33.333)]);
    }
    return {keys: prop.numKeys, firstTime: prop.keyTime(1), lastTime: prop.keyTime(2),
        firstOutSpeed: prop.keyOutTemporalEase(1)[0].speed};
}
```

Expected: keys at0/1s with values0/100, Bezier interpolation, zero endpoint speeds;
inspect readback interpolation/ease before treating it as accepted. Failure after
the first setter can leave partial keys; caller compensation is necessary. OneD
uses one ease object per direction. TwoD/ThreeD quantitative properties need
dimension-matched arrays; spatial properties have separate temporal/spatial
semantics. Do not copy this helper into a Position leader/follower by cast.
Source: [pinned Property guide](https://github.com/docsforadobe/after-effects-scripting-guide/blob/7137a990db4bd8dc9f5869b8ca431c7dfed52bdc/docs/property/property.md),
setValuesAtTimes, setInterpolationTypeAtKey, setTemporalAutoBezierAtKey,
setTemporalEaseAtKey and keyOutTemporalEase. This is separate from the linear rig.

Source-quality caveat: that guide's setTemporalAutoBezierAtKey paragraph refers
to keySpatialContinuous even though its keyTemporalAutoBezier attribute paragraph
describes Bezier temporal interpolation; setTemporalContinuousAtKey's newVal text
also calls continuity auto-Bezier. Treat these as documentation inconsistencies,
not authority to invoke spatial APIs on OneD. The fragment explicitly disables
temporal auto-Bezier and declares manual ease; verify actual readback in target AE.

Do not bury the entire product in a button callback.

Prefer:

~~~text
UI event
  -> validate plain command
  -> command/service function
  -> AE scripting DOM
  -> normalize plain result
  -> UI renders result
~~~

The command function should remain callable from ScriptUI, CEP, a JSX harness or a future UXP adapter without rewriting the operation.

## Long operations

### File/Folder и preferences: bounded сценарии

**UTF-8 text export (SOURCE EXAMPLE / AE NOT_RUN).** Включённые scripting file
permissions — prerequisite, не обещание helper. Dialog до mutation, новый filename,
проверка parent Folder и возвращаемых I/O statuses. Здесь нет project edits и Undo:

```jsx
function writeNewUtf8(file, text) {
    if (!file || file.exists || !file.parent.exists)
        throw new Error("Choose a new file in an existing folder");
    file.encoding = "UTF-8";
    var opened = false, primary = null, closeProblem = null;
    try {
        if (!file.open("w")) throw new Error(file.error || "Open failed");
        opened = true;
        if (!file.write(text)) throw new Error(file.error || "Write failed");
    } catch (e) { primary = e; }
    finally {
        if (opened) {
            try { if (!file.close()) closeProblem = "Close failed: " + file.error; }
            catch (c) { closeProblem = c.toString(); }
        }
    }
    if (primary || closeProblem)
        throw new Error((primary ? primary.toString() : "") + "\n" + (closeProblem || ""));
    return file.fsName;
}
```

Expected: Unicode text roundtrips through an independent UTF-8 reader, output
path returned only after successful close. Failure can leave partial own file;
do not report complete export. `exists` check is **not exclusive creation**: race
can create a file before open("w"). Use a product-owned staging directory under
controlled access; if collision-free publication against concurrent writers is
required, use an external service with exclusive-create/atomic-publish semantics,
not this helper. Never delete user files as automatic error cleanup.

**Preferences.** A tool can save a short non-secret mode string under its own
`app.settings` section; this does not mutate project and needs no Undo. Example:

```jsx
function saveMode(mode) {
    if (mode !== "preview" && mode !== "final") throw new Error("Invalid mode");
    app.settings.saveSetting("BibleDemo", "mode", mode);
    if (app.settings.getSetting("BibleDemo", "mode") !== mode)
        throw new Error("Preference readback mismatch");
}
function readMode() {
    if (!app.settings.haveSetting("BibleDemo", "mode")) return "preview";
    var value = app.settings.getSetting("BibleDemo", "mode");
    return value === "final" ? "final" : "preview";
}
```

Expected current preference readback, not proof of persistence across process exit.
Test restart separately in target AE. Settings I/O can fail; caller reports the
error instead of marking saved. Unknown values use declared safe default; no secret
or binary blob, no attempt to override host's preference storage location.
The guide documents values as strings, per-version preferences (not automatically
migrated across AE installs), and a reported1999-byte failure limit in AE15.0.1;
keep tiny preferences rather than interpreting that observation as a universal
modern capacity guarantee.
Exact
File/Folder APIs follow [ExtendScript File reference](https://extendscript.docsforadobe.dev/file-system-access/file-object/)
(open/write/close returns reviewed2026-10-07), not browser File APIs; Settings follows
[pinned guide](https://github.com/docsforadobe/after-effects-scripting-guide/blob/7137a990db4bd8dc9f5869b8ca431c7dfed52bdc/docs/other/settings.md).

Host-side ExtendScript can block interactive work. Avoid one giant call that performs expensive file parsing, networking or computation and then mutates the project.

Split work into:

1. pure/external computation where practical;
2. short host mutations;
3. explicit progress and cancellation checkpoints for genuinely long jobs.

When CEP invokes ExtendScript through evalScript, the host-side script runs on the host main thread. A long script call can starve both AE interaction and CEP event scheduling.

## Version gates

New scripting methods arrive in specific AE versions. Prefer feature detection where possible.

~~~jsx
if (typeof someObject.someNewMethod === "function") {
    someObject.someNewMethod();
} else {
    // supported fallback or clear compatibility error
}
~~~

Use app.version only when behavior cannot be detected directly.

A compatibility statement should name AE versions actually tested, not merely versions whose API documentation contains the method.

Проверяйте также provenance самого member. В [ImportOptions reference](https://github.com/docsforadobe/after-effects-scripting-guide/blob/7137a990db4bd8dc9f5869b8ca431c7dfed52bdc/docs/other/importoptions.md) `rangeStart`, `rangeEnd`, `isFileNameNumbered()` явно отмечены как officially undocumented. Feature detection показывает наличие member, а не устойчивый поддерживаемый контракт. Исследовательские API требуют отдельной opt-in policy и ограничения версий продукта.

Актуальный Scripting Guide включает более поздние API, включая 26.5. Используйте его per-member version notes; native SDK baseline 25.6 не является общей версией всех scripting возможностей. Дата этого source review: **2026-10-02**, [область проверки](../EXTERNAL-SOURCES-REVIEW-2026-10-02.md).

## Boundary with expressions

Scripts mutate project state and perform automation. Expressions are evaluated as part of property evaluation and should not be used as a substitute for project orchestration.

See:

- 03-EXPRESSIONS-VS-SCRIPTS.md
- ../15-COMMUNICATION/05-SCRIPT-TO-AE.md

## Verification boundary

This chapter documents the scripting model, provenance limits and architecture patterns. It does not claim that its fragments have been executed in every supported AE version. Product-specific runtime assertions need separately identified host evidence.
