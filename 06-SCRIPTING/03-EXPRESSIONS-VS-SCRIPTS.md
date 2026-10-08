# Expressions vs scripts

Scripts and expressions both use JavaScript-like syntax, but they occupy different semantic roles in After Effects.

## Core distinction

## Practical expression contracts — reviewed2026-10-08

### Property animation: trigger bounds, loops and sampling

Full pinned [Property](https://github.com/docsforadobe/after-effects-expression-reference/blob/a5c5c5066d0395239d524510ace060963f5c0d33/docs/objects/property.md)
read. Expression Property is evaluation context, not writable scripting Property.
name/display propertyIndex aren't stable instance identity; propertyGroup(countUp)
provides hierarchy-relative relations for duplicated groups, provided actual structure
validated. numKeys changes with separated dimensions and includes markers on marker
property; never key(0) or key(numKeys) before checking count.

Concrete marker-triggered playback on keyed numeric property,26.0+ JavaScript engine:

~~~javascript
var m = thisLayer.marker;
var result = value;
if (numKeys >= 2 && m.numKeys > 0) {
    var trigger = m.previousKey(time);
    if (trigger.time <= time) {
        var first = key(1).time;
        var last = key(numKeys).time;
        var elapsed = Math.max(0, Math.min(time - trigger.time, last - first));
        result = valueAtTime(first + elapsed);
    }
}
result;
~~~

previousKey returns at-or-before but clamps to first before first marker; explicit
trigger.time<=time prevents premature playback. nextKey returns after requested time
but clamps to last after final key; returned object isn't proof an upcoming event.
Both introduced26.0, JavaScript expression engine only, not scripting methods or
Legacy ExtendScript expression support. Older rig uses bounded indexed scan or
nearestKey plus time check; nearest isn't necessarily previous. key(index) returns
Key/MarkerKey, marker-name overload only for marker properties; duplicate-name policy
needs marker-specific review. No count-zero behavior promised. Source example ignores
pre-first trigger/count/zero-duration gates: these product checks are deliberate.

Loop command validates numeric animatable property and at least two distinct key times,
then chooses loopOut/loopIn (key intervals) or loopOutDuration/loopInDuration (seconds).
numKeyframes1 spans last two keys for loopOut, first two for loopIn,0 uses all keys.
cycle repeats, pingpong reverses, offset accumulates endpoint difference; continue
extrapolates endpoint velocity and **doesn't accept** interval/duration argument.
Duration0 uses layer In/Out-boundary semantics, not universal all-keys equivalent;
use explicit positive duration for bounded product loop. Source wording for loopInDuration
default says segment begins at Out point while first-key-forward description suggests
other endpoint: retain ambiguity and avoid that default in portable generated rigs.
Source Text/paths/custom histogram don't support these generic numeric loops.
cycle seam can jump if endpoints differ; pingpong/offset isn't automatic seamless
motion. Inspect boundary/negative-time/in-out behavior and qualify actual output.

value is current property value; expression valueAtTime(t) has **no scripting
preExpression boolean**. velocity/velocityAtTime return same-dimensional temporal
rate; speed/speedAtTime scalar spatial speed, not arbitrary numeric rate. Source's
valueAtTime(random(4)) example doesn't select discrete four keys on interpolated
animation: continuous random time interpolates values. To choose actual key values
use explicit integer selection and key(index).value under engine policy; don't
present time sampling as discrete selection or baked-key preservation.

smooth(width,samples,t) uses temporal box filter, default0.2 seconds/5 samples;
bounded positive width and odd sample count include center under product policy.
More samples increase evaluation cost; it isn't causal live filtering or one-time
script smoothing. wiggle(freq,amp,octaves,amp_mult,t) perturbs property value, amp in
property units; do not add value a second time to its returned absolute result.
For2D Y-only perturbation return [value[0],wiggle(3,50)[1]], preserving X. Scale
correlated axes need explicit vector construction, not assumption components match.
Bound octave/sample cost, confirm dimensions/range (opacity clamping separate).
temporalWiggle changes sample time of existing animation, not spatial amplitude;
its table copies "property units" for amp despite description time perturbation.
No unambiguous units contract established here: keep target-build qualification,
don't claim pixels converted directly into seconds. All outcomes remain expectations,
not executed AE results or hidden evaluation-order state.

### Paths: rebuild values, don't mutate project geometry from expression

Full pinned [Path Property](https://github.com/docsforadobe/after-effects-expression-reference/blob/a5c5c5066d0395239d524510ace060963f5c0d33/docs/objects/path-property.md)
read,15.0+ methods. Concrete flatten/open path expression on intended mask Path:

~~~javascript
var p = thisProperty.points(time);
var zeros = [];
for (var i = 0; i < p.length; i++) zeros.push([0, 0]);
thisProperty.createPath(p, zeros, zeros, false);
~~~

createPath returns Path evaluation value, not adding masks or persistent vertices.
points must contain at least one finite2D pair; explicit nonempty tangent arrays match
point count. Default empty tangent arrays accepted as documented special case despite
table equal-count wording; explicit zeros avoid relying on mismatch handling.
Tangents are **offsets from parent vertices**, not absolute handle coordinates.
points/inTangents/outTangents sample optional time and round four decimals; copying
through them isn't lossless original geometry serialization. isClosed no time arg
documented, so don't invent closure-state sampling overload.

Mask points relative layer upper-left origin; shape paths relative group anchor and
brush points relative stroke start. Don't pass shape-group coordinates straight into
layer.toComp while ignoring nested group transforms. Concrete mask follower on2D
Position: source.mask("Bible Path").maskPath.pointOnPath(u,time) → source.toComp(point,time)
→ parent.fromComp(compPoint,time) if parent exists → compatible Position dimensions.
Choose finite u0..1 under product policy, validated mask/name and ownership policy.
No3D/shape-group generalized mapping claimed by this bounded mask route.

pointOnPath uses **arc length**, not Bezier parameter/vertex index; closed0/1 same point,
open1 last point. Linear u yields uniform progress along sampled local path; animated
geometry or nonuniform transforms can invalidate constant comp/world-space speed.
tangentOnPath/normalOnPath return unit-length2D offsets at arc fraction, not point
positions or stored Bezier outTangents. Offset curve point = point + distance*normal;
use Vec transform for direction versus point transform for position. Incoming direction
is negative tangent, not original incoming handle magnitude. Cusp/degenerate path
orientation/error behavior not fully described: reject unsupported state/report, no
invented stable normal. name is display property name, not path identity. Bound
diagnostic loops and cache sampled arrays within evaluation rather than re-read each
vertex; no path image/host execution from these designs.

### Interpolation/vector/color operations — full review2026-10-08

Full pinned general/interpolation, vector-math, color-conversion and other-math pages
read at revision above. Concrete driver remap: validated finite Slider value →
linear(driver,0,100,20,80) → Opacity. Five-argument linear clamps outside driver
interval; three-argument uses normalized0..1, not seconds unless driver is time.
ease has zero endpoint velocity both ends; easeIn only start, easeOut only end.
Validate finite tMin<tMax and matching value shapes under product policy; equal/
reversed intervals aren't described robustly in source. These functions return
evaluated value, not editing key temporal interpolation or reproducing a user Bezier
curve. Endpoints can descend (value1>value2) while driver interval stays ascending.

Vector methods global, no Math prefix: add/sub componentwise, mul/div vector by
scalar, dot scalar product, cross2/3D vector product, length magnitude or distance
between two points, normalize unit direction. General dimension padding with zero
can hide2D/3D mistakes: validate intended shape instead of treating permissive input
as semantic compatibility. Guard divisor and length near zero before div/normalize;
source doesn't define useful direction for zero vector. Use explicit3D inputs for
cross-dependent orientation where2D cross result convention isn't detailed.

Concrete bounded direction construction: same-space source/target points → sub →
length → if nonzero normalize → mul(direction,distance) → add(origin,offset). dot
projection only on qualified unit axis; distance point2 argument is not arbitrary
second vector normalization. clamp constrains components, not vector magnitude;
Opacity route clamp(wiggle(0.5,500),0,100). Source clamp example comment says0..100
but actual code upper500: do not copy code as proof comment contract.

lookAt(fromPoint,atPoint) expects world3D points and returns Orientation angles
pointing z-axis toward target. Source example using raw positions assumes suitable
unparented context; resolve world coordinates for general rig, disable competing
auto-orient deliberately. Returned world-target rotation is not promised correct
local Euler orientation for arbitrary parent rotations/nonuniform scales; qualify
parent conversion route separately. Coincident points undefined in terse source:
choose explicit fallback/unsupported result, not a stable facing claim.

degreesToRadians/radiansToDegrees bridge AE angle fields to Math trig:
value + 10*Math.sin(degreesToRadians(time*90)) on Rotation declares degree amplitude10
and90 degrees phase/second. Don't interpret time directly as degrees or forget radians
on Math.sin. These scalar functions don't convert coordinate vectors/orientation order.

Color command: validated exact6/8 hex digits after allowed prefix →16.0+ hexToRgb →
RGBA result,6 digits alpha1,8 last byte alpha. API ignores characters beyond8 but
product validator rejects extra bytes instead of silently truncating malformed brand
color. Three-character CSS shorthand not documented. rgbToHsl/hslToRgb take four
normalized0..1 components (HSLA hue also normalized, not degrees), alpha retained by
schema; sample conversion round-trip isn't profile/gamma/ICC/HDR transform proof.
Source rgbToHsl example uses malformed property call; use rgbToHsl(colorValue).
For hue edit, validated RGBA → HSLA → bounded hue policy → RGBA → Color property,
not TextDocument's3-component schema. HDR out-of-range values aren't covered by these
normalized conversion contracts: require explicit product gamut/tone policy rather
than silently clamp/claim color-managed identity. No image/math/expression runtime.

### Comp/project/effect lookup and data-driven rigs — full review2026-10-08

Full pinned objects/comp, project, footage, effect, dropdown, propertygroup and mask
pages read. Expression thisComp is containing comp, not whichever UI comp active;
comp(name) and precompLayer.source access other comp context. layer(index/name/
otherLayer,relIndex) follows Timeline order; duplicate name returns topmost, reorder
breaks relative-index assumptions. layerByComment is case-sensitive **substring**,
first/topmost match, not exact stable ID or regex. Rig installer must establish unique
owned names/comments and fail on ambiguity, not use broad "Control" substring silently.

Comp width/height pixels, pixelAspect separate display aspect, duration/frameDuration
seconds, displayStartTime/timecode policy separate from animation time. Center Position
[width/2,height/2] assumes unparented2D positioning; parent/3D needs coordinate route.
Comp.bgColor four-component expression color versus scripting CompItem.bgColor three.
shutterAngle/shutterPhase degree observations, not proof motion blur applied. activeCamera
is **render camera at current frame**, not Composition panel view; default/no-camera
behavior not specified by page, so don't invent null or a guaranteed real camera layer.

thisProject.bitsPerChannel8/16/32 and linearBlending read evaluation settings, not
working-space identity or guaranteed color result. fullPath empty unsaved, platform-
specific absolute path otherwise: use only intentional diagnostics, not cross-machine
rig identity, File handle or embedding private directory names in deliverables.

Effect.active reports effect switch; param(name/index) returns Property and effect
points in layer space. Resolve expected effect/parameter schema and duplicate/naming
policy before generating expression; index independent of locale but not of vendor
parameter reorder. PropertyGroup.name/propertyIndex relative display/structure;
numProperties immediate children, not recursive total. propertyGroup climbs hierarchy,
enabling structurally relative duplicated rigs but not writable group creation/removal.
Expression absence/failure isn't same null contract as scripting property lookup.

26.0+ JavaScript-engine dropdown .items/.text/.textAtTime exposes labels including
other effect/layer menus, **not Layer Control labels**. .value remains numeric index;
use owned enum-index mapping for logic (language changes labels), labels for Source
Text display. Changing owned menu order still requires semantic index migration.
textAtTime(t), not source prose typo timeAtTime, is time-sampled label; not scripting
propertyParameters/valueText/setPropertyParameters. For Layer Control use actual
returned Layer.name after validated selection; don't infer layer ID from label.

Concrete JSON-driven opacity: installer validates imported trusted footage/schema,
bounded array/record count and finite field types → expression reads
footage("Bible Data.json").sourceData → validated intended record.opacity → explicit
clamp0..100/fallback policy → returns value. sourceData structure follows JSON shape;
don't blindly assume top-level array just because page type says array. sourceText
contains JSON String; **do not eval** source example's untrusted file contents.
Use parsed sourceData or engine-qualified JSON parser with schema/size policy.
Expressions aren't filesystem/network fetchers; scripts import/update data deliberately.

Footage duration/frameDuration/width/height/pixelAspect/ntscDropFrame/name report source
metadata, not layer stretch/time-remap/current playhead or successful decode. MGJSON
dataValue(path) static/dynamic value, dataKeyCount(path), dataKeyTimes(path,t0,t1) and
dataKeyValues(path,t0,t1) expose dynamic samples. Paths one **array of hierarchy indices**;
source examples [1][0] evaluate to scalar1, not nested path [1,0]. Validate schema/
path and expected stream kind, bound time window/sample cost, pair sample times/values
only after equal length/type checks. Default sample extent comes from stream, not comp
duration. Source doesn't fully specify dynamic dataValue time mapping/interpolation/
out-of-range behavior; qualify those rather than promise automatic source-time remap.
External data import/publish is separate from expression evaluation/packaged assets.

Mask invert/expansion/feather/opacity/path are evaluation observations/links, not setters
to mutate mask mode/group; expansion pixels versus opacity percent. maskFeather table
says Number while common dimensional use needs qualified value shape: inspect target
field, don't assign invented vector schema from this prose. Mask page's blanket no
numeric path manipulation predates separate15.0 Path methods: use versioned path
contract reviewed above, not claim current paths entirely inaccessible. Mask settings
don't establish resulting alpha/occlusion. No media/data/menu/mask runtime performed.

### Keys and marker metadata: index isn't marker name

Full pinned objects/key, marker-property and markerkey pages read. Key.index timeline
order1-based, time seconds and value underlying typed keyed value; not writable handle,
persistent ID or sampled interpolation. Flash-at-nearest recipe first checks numKeys>0,
then easeOut(abs(time-nearestKey(time).time),0,0.1,100,0); nearest flash is symmetric
around key, not strictly post-trigger. For post-trigger use previous-boundary gate.

Marker.numKeys count, key(index) indexed order, key(name) **comment**, duplicate names
first in time. Comp page warning against old composition marker-number access doesn't
eliminate modern marker.key(index) (explicitly documented by marker page): distinguish
numeric display-name "1" from indexed first marker. For named Start/End ramp resolve
unique owned comments, validate end.time>start.time then linear; fix source typo
thisLayr to thisLayer. No empty-marker nearestKey call or assumed unique comments.

MarkerKey.comment/chapter/cuePointName/url/frameTarget metadata Strings; eventCuePoint
true Event/false Navigation. Do not execute comment/URL/parameters or trigger browser/
network from value evaluation. duration seconds doesn't force hold/loop behavior;
if intended use [time,time+duration) explicitly and validate duration policy.
parameters associative String values unlike scripting MarkerValue pair array:
validate named field present, parse finite bounded number before use, no schema from
mere marker existence. Marker time/index inherited Key metadata aren't displayed
number/name. protectedRegion16.0+ comp markers and nested-comp protected markers,
not ordinary layer marker universal flag; observation doesn't implement custom retime
or guarantee consumer behavior. Bounded Source Text diagnostics avoid eval/private
metadata leakage and handle marker count first. No marker/Key/metadata runtime.

### Global/layer/camera/light contexts — full review2026-10-08

Full pinned general/general, general/global, layer/layer, layer/general, properties,
sub-objects, threed and objects/camera/light pages read. Zero-heading navigation pages
describe category/inheritance, not new undocumented methods. thisComp/thisLayer/
thisProperty/thisProject are **containing evaluation** objects, time composition
seconds; no app active-item/selection/UI mutation. Implicit thisLayer names convenient
but explicit namespaces preferred in generated code to avoid local-name collision.
colorDepth project bpc diagnostic, not transfer function or shader pixel format.
comp/footage names need unique owned resolution policy established by installer.

Concrete held random scalar expression: posterizeTime(1/framesToTime(12)); random(50,100).
Finite positive update rate with explicit frames/fps policy; posterizeTime changes
property evaluation cadence, not comp fps, output render rate or guaranteed single
execution at each interval. Page lists numeric return but sample uses standalone
cadence call followed by value: don't treat returned Number as output amplitude.
No undocumented zero-rate "evaluate once forever" contract. Subframes/motion blur/
engine contexts require qualification; random timeless policy still separate.

Layer.enabled video switch, active includes in/out interval; audioActive audio switch/
interval, hasAudio component, not PCM amplitude or silence. hasVideo description
video but Type line says audio (copy error): preserve distinction, not duplicate
hasAudio logic. width/height source dimensions, not transformed pixel bounds. index
order changes with structural edits; name display metadata. hasParent gates parent
access; position parent-space when parent exists, otherwise world, anchorPoint local,
scale percentages, opacity percent, rotation z degrees for3D. audioLevels stereo
[left,right] **decibels property values**, not media amplitude; use deliberate audio-
analysis preparation rather than claiming reactive audio from these levels alone.

inPoint/outPoint/startTime seconds: source warns reverse-time may invert in/out order;
don't force increasing interval from normal-layer assumption when reporting/replaying
reversed footage. timeRemap only enabled property seconds, not enable setter.
Layer.source Comp/Footage defaults adjust to source time; sourceTime(t) obtains mapped
numeric source time (description says source object despite Number return). No simple
time-startTime replacement promised across stretch/remap/reverse. When reading another
comp's animation choose explicit mapped sample time versus implicit source context,
avoiding double application of source-time conversion.

effect(name/index), mask(name/index) topmost duplicate-name/current1-based order, not
persistent IDs. sourceRectAtTime(t,includeExtents) returns local {left,top,width,height};
13.2+, paragraph extents15.1+. true gives paragraph **box**, not visible glyph alpha;
shape bounds expanded. Copied smoothing-filter wording in t table is not an actual
filter operation. Concrete background-box rig: text rect at intended time → derive
four local corners/desired padding → map through transforms → return shape rectangle/
position of compatible space. No post-effects/occlusion/motion-blur image bounds
guaranteed; layer dimensions aren't interchangeable with rect.width/height.

sampleImage(point,radius,postEffect,t) expects2D **layer-space pixel point**, [0,0]
center upper-left pixel; radius half extents, default[0.5,0.5] one pixel. Returns
alpha-weighted averaged RGBA, not raw channel histogram. Concrete color follower:
source.sampleImage(localPoint,[2,1.5],true,time) → compatible4-component Color field;
source point mapped from comp through qualified fromComp/fromCompToSurface route.
postEffect true includes **direct** layer masks/effects, not all adjustment/precomp/
final composition processing. Transparent/border/HDR cases need actual host/image
qualification; page doesn't specify every weighting/edge rule. Bound samples/regions,
avoid self-dependency cycles; "no longer disables multiprocessing" isn't a universal
MFR thread-safety/performance guarantee for the entire rig or native plugin.

3D material inspector: orientation3-vector degrees versus rotationX/Y/Z scalar,
ambient/diffuse/metal/shininess/specular percentages and lightTransmission numeric.
acceptsLights nominal Boolean Number; acceptsShadows/castsShadows preserve enum2
"Only" instead of flattening truthy bool. These are renderer-sensitive observations,
not setters to force renderer or proof identical Advanced3D/PBR material behavior.
No universal inherited material access on Camera/Light: source excludes material,
source/effect/mask/width/height/anchorPoint/scale/opacity/audioLevels/timeRemap for both.
Typed rig generation must branch actual layer role before accessing those properties.

Camera.active requires enabled/in-range **topmost** camera, unlike ordinary enabled
layer active. Camera page syntax cameraOption (singular) is preserved as source-route
ambiguity; verify actual pick-whip/API target before emitting it in production.
aperture/focusDistance/zoom pixels, blurLevel and irisRoundness percentages, irisRotation
degrees; depthOfField0/1. irisShape indices1..10 include divider2: don't assign it as
real iris. highlightGain/Saturation, irisAspectRatio/DiffractionFringe ranges source
1..100; highlightThreshold depends bpc (source8-bit0..100,16-bit0..32768,32-bit0..1).
Don't normalize every option with one color/percent rule. pointOfInterest world per
page, general position parent-relative: inspect target parent context explicitly.

Concrete focus-distance expression route: owned validated camera/target → world
positions → camera-space target depth for intended optical-axis focus, with explicit
camera transform and parent policy → qualify DOF on/output. Euclidean distance from
length(cameraPos,targetPos) is **not** necessarily optical-axis depth for off-axis
target. Source scale compensation uses distance/zoom and raw positions: restrict to
qualified simple unparented on-axis rig, guard zoom>0, don't advertise arbitrary
perspective/parent/camera-roll equivalence.

Light typed inspector: color4-vector, intensity/coneFeather/shadowDarkness percent,
coneAngle degrees, shadowDiffusion pixels; castsShadows bool (unlike material "Only"
enum). falloff dropdown numeric, falloffDistance/radius numeric with no full units/
range enum map here; preserve current qualified values, don't fabricate choices.
pointOfInterest world per page; lightOption singular syntax needs target qualification
like cameraOption. Light type/renderer gates available options; these pages don't
document environment-source mapping or current native lighting contracts. All source
operations above not executed in AE; qualification gaps remain explicit.

### Independent expression inventory

### Text expression styles and variable axes — full review2026-10-08

Full pinned text/text, sourcetext, style and variable-fonts pages read. Text.sourceText
is content,17.0+ also exposes SourceText style operations, **not scripting
TextDocument**. Text.Font... is an expression-menu dialog that inserts internal font
name String, not callable expression API. Font resolution/installation/licensing
remains separate from a successful style-object construction.

Concrete owned plain-title Source Text expression,17.0+ style route:

~~~javascript
text.sourceText.createStyle()
    .setFont("Impact")
    .setFontSize(48)
    .setText("Bible Title")
    .setApplyFill(true)
    .setFillColor([0.2, 0.6, 1.0]);
~~~

This deliberately creates uniform style, not preserves arbitrary mixed runs. Font
must exist under deployment policy; no substitute/glyph/render PASS inferred.
createStyle initializes empty style; inheriting reference.getStyleAt(0,time) chooses
**one character at explicit time**, not all reference runs/paragraphs. Check nonempty
content and valid index first; source doesn't define empty/out-of-range recovery.
SourceText.style explicitly equated to getStyleAt(0,0) by pinned page: don't describe
it as necessarily animated current-time style; use explicit getStyleAt(index,time)
when temporal sampling intended. SourceText25.0 flags distinguish horizontal/vertical
and point/paragraph text; they aren't conversion setters or layout/glyph bounds.

25.0+ range-style route: generate final bounded content, setText, calculate valid
startIndex/count for that final content (zero-based character indexing; spaces and
line breaks count), then supported per-character setters. A simple ASCII product
can use .setFillColor([1,0,0],0,5) for five initial characters of known content.
Source doesn't establish grapheme/surrogate/combining-sequence indexing guarantees:
don't equate visible glyph count with JS length for arbitrary multilingual text.
replaceText(String,start,count) can change length; recalculate later ranges. Omitted
count means rest of string, not one character. These evaluations return output style,
not durable project edit or scripting CharacterRange/ParagraphRange.

Style review groups and operation policy:

| Family | Read/write operation and boundaries |
| --- | --- |
| Font/size/scaling | font/fontSize/horizontalScaling/verticalScaling and matching setters; validate finite size/scale and installed internal font name, don't assume renderer glyph metric identity. |
| Case/faux/ligature | isAllCaps/isSmallCaps/isFauxBold/isFauxItalic/isLigature and setAllCaps/setSmallCaps/setFauxBold/setFauxItalic/setLigature; ranges only25.0+, faux isn't installed real font face, case display isn't necessarily source String replacement. |
| Paint/stroke | applyFill/applyStroke, fillColor/strokeColor RGB three normalized components, strokeWidth; enable fill/stroke explicitly and positive width for visible stroke. lineJoin/setLineJoin use bevel/miter/round; scoped setter25.0+, not native pixel-compositing blend mode. |
| Baseline/digits | baselineDirection default/rotated/tate-chuu-yoko, baselineOption default/subscript/superscript, baselineShift numeric, digitSet default/hindidigits and matching setters; distinguish text orientation from baseline direction. |
| Spacing | tracking, leading, isAutoLeading and matching setters; explicit setAutoLeading(false) before manual leading, scoped consistently. Numeric tracking/shift/leading units/ranges not fully specified here; don't borrow every scripting unit. |
| Kerning | kerning/kerningType manual/metrics/optical read; setKerning(value,index) versus setKerningType(metrics/optical,start,count). **manual not setter enum**; automatic takes precedence, no promised disable-automatic setter route. |
| Paragraph layout | direction, justification, isEveryLineComposer, isHangingRoman, leadingType, firstLineIndent, leftMargin/rightMargin, spaceBefore/spaceAfter; getters often first paragraph, setters whole layer, not mixed-paragraph preservation. |
| Tsume | getter0..1 versus setTsume table0..100; no declared reversible conversion/round-trip contract. Qualify units before automatic migration. |

When both setText and paragraph setters used, pinned warnings require **setText
first**, then setDirection/setEveryLineComposer/setFirstLineIndent/setHangingRoman/
setJustification/setLeadingType/setLeftMargin/setRightMargin/setSpaceBefore/setSpaceAfter.
direction left-to-right/right-to-left changes left/right justification interpretation;
justification exact strings alignCenter/alignLeft/alignRight/justifyFull/
justifyLastCenter/justifyLastLeft/justifyLastRight; leadingType bottom-to-bottom/
top-to-top. Read first paragraph isn't full-document snapshot for restoring mixed
formatting. Don't invent paragraph range overloads for whole-layer setters.

Pinned page's general "all methods chain" conflicts with Returns **None** for
setKerning/setKerningType/setTsume. Until vendor/target contract resolved, do not
generate those calls as fluent chain or assert returned TextStyle. setKerningType
and setTsume may need separate qualified invocation, not automatic chain inference.
No manual-kerning recovery or Tsume reversible setter guarantee from repository build.

26.0 variable-font page has **zero third-level headings but actual API guidance**:
text.animator("Animator 1").property.fontAxisWght (also Wdth/Slnt/Ital/Opsz examples).
fontAxis[Tag] prose is naming-pattern notation, not promise dynamic JS indexing
fontAxis["wght"]. Use exact documented constructed property spelling and owned
animator; actual axis must exist on chosen variable font and be added to animator.
Validate tag/property/font and source-provided axis bounds rather than assume universal
weight0..1000 or divide weight by10 as a universal Opacity mapping. Concrete controlled
route: qualified axis value and finite known min<max → linear(axis,min,max,0,100).
No invented custom-tag capitalization normalization, font-axis discovery expression,
font download or global font design-vector setter. No typography/axis/host execution.

### Independent expression inventory

`expression-api-inventory-2026-10-08.json`:32 API-category pages/295 third-level headings
including overloads. Page heading strings aren't unique global symbols or complete
signature inventory. `expression-api-reviewed-2026-10-08.json` explicitly records32
full-page operation reviews (295 headings), SHA256/source and coverage route; all32
pages classified, including non-API/navigation headings and variable-font zero-heading
guidance. This closes only this pinned page-review scope, **not complete expression
language signatures, current official/vendor contracts or installed-host validation**.
No literal mention or downloaded bytes give coverage PASS.

Pinned expression-reference revision
[`a5c5c5066d0395239d524510ace060963f5c0d33`](https://github.com/docsforadobe/after-effects-expression-reference/tree/a5c5c5066d0395239d524510ace060963f5c0d33).
Full [layer-space transforms](https://github.com/docsforadobe/after-effects-expression-reference/blob/a5c5c5066d0395239d524510ace060963f5c0d33/docs/layer/layer-space-transforms.md),
[time conversion](https://github.com/docsforadobe/after-effects-expression-reference/blob/a5c5c5066d0395239d524510ace060963f5c0d33/docs/general/time-conversion.md),
[random numbers](https://github.com/docsforadobe/after-effects-expression-reference/blob/a5c5c5066d0395239d524510ace060963f5c0d33/docs/general/random-numbers.md)
read; source designs only, no AE expression evaluation observed. The separate
scripting648-heading partition does not count these expression members.

### Coordinates: position, direction and projected surface aren't interchangeable

Expression toComp/fromComp and toWorld/fromWorld transform **points**; corresponding
Vec methods transform **directions**. All take optional sample time defaulting to
time. Comp/world coincide for2D, but3D comp space camera-relative versus camera-
independent world. Don't feed parent-space position directly into a purported world
conversion. Concrete3D target-follow expression on follower Position:

~~~javascript
var target = thisComp.layer("Bible Target");
var p = target.toWorld(target.anchorPoint, time);
hasParent ? parent.fromWorld(p, time) : p;
~~~

Product-controlled name must resolve; qualify follower3D status, parent transform,
random seeks/animation and missing-target policy. This uses target's anchor, not its
parent-space position. Expression returns value for this property, not mutating rig.
For layer-space points through two layers use destination.fromWorld(source.toWorld(p,t),t)
with same time; different comp contexts aren't automatically compatible world origins.
Direction conversion uses toWorldVec/fromWorldVec (or comp equivalents), no translation;
zero vector/nonuniform scale need explicit normalization policy. Source toWorldVec
example mistakenly calls toWorld on point difference; use method contract, not that
example. Don't promise perspective toCompVec acts like screen-space point difference
at every depth without qualification.

fromCompToSurface projects onto3D layer's zero-z plane via active camera and returns
2D layer point: useful for effect point controls. It isn't arbitrary geometry ray
intersection, a2D-layer helper, or identical to fromComp. Degenerate camera/plane
cases aren't detailed in page: expose errors/unsupported input rather than invented
fallback intersection. These expression methods are not AVLayer scripting's current-
time/first-character sourcePointToComp or compPointToSource; no API by-name porting.

### Frame conversion and timecode: display offsets and rounding

framesToTime(frames,fps) accepts fractional frames and returns seconds; timeToFrames
returns integer with policy: absolute rounds toward negative infinity, duration
away from zero. Defaults use time+thisComp.displayStartTime and comp fps, so a bake/
sampling tool must pass intended time explicitly rather than accidentally include
display offset. At24fps, declared expectations: timeToFrames(-0.01,24,false)=-1;
timeToFrames(0.01,24,true)=1; framesToTime(0.5,24)=1/48. These aren't executed assertions
or proof exact floating-point boundary parity. Quantization means conversions aren't
universal inverses for fractional inputs.

Concrete Source Text time label:

~~~javascript
timeToCurrentFormat(time + thisComp.displayStartTime,
                    1 / thisComp.frameDuration, false, thisComp.ntscDropFrame);
~~~

For elapsed duration pass elapsed seconds and true, not display start. Return String
is display, not authoritative timebase/EDL interchange. timeToTimecode defaults base30,
not automatic comp fps; timeToNTSCTimecode separate NTSC/drop-frame formatting.
timeToFeetAndFrames explicit fps/framesPerFoot (default16) for film display, not media
frame rate detection. Drop-frame skips numbering, not source frames or retime; explicit
ntscDropFrame argument for timeToCurrentFormat introducedCS5.5. Check negative times,
nonzero display start, fractional fps and chosen display policy independently.

### Randomness: repeatable evaluation isn't persistent identity

seedRandom(offset,true) removes time from seed, not layer/property identity. Concrete
static per-property opacity variation:

~~~javascript
seedRandom(123456, true);
random(20, 80);
~~~

Expected bounded20..80 and stable over time for same qualified layer/property/context;
not identical across duplicate/import/host versions. Default seed includes unique
layer identifier, property, time and offset. Changing offset controls sequence and
wiggle initial value; doesn't establish same random stream across independent
properties. For persistent product values across migration generate/store values
in owned controls under script policy instead of treating seed as external database ID.

random(max) scalar/array gives0..max; two-bound array variant pads smaller dimension
with zeros. Validate matching vector shapes in product code rather than silently
accept unintended padding. gaussRandom bounds contain approximately90%, **not clamp**:
choose explicit bounded output policy if used for opacity/size. noise(scalar or2/3D
array) returns scalar -1..1 correlated Perlin signal, not vector per input component.
For smooth rotation perturbation use value + amplitude*noise(time*frequency), with
explicit amplitude/range expectations; not random global counter or sampling-order
state. random historical CS6/CC layer-ID behavior change means same seed text isn't
a cross-version bit-identical delivery guarantee. Full wiggle/property contract and
remaining expression pages require separate review, not credited by this block.

**Script**

~~~text
user/tool command
→ reads project
→ may mutate project structure/state
→ finishes
~~~

**Expression**

~~~text
property evaluation
→ reads allowed context
→ computes property value
→ may be evaluated repeatedly/out of intuitive order
~~~

Do not use an expression as a project-automation engine and do not use a script as a per-frame expression evaluator.

## Scripts are orchestration

Typical script responsibilities:

- create/remove items/layers;
- add effects/properties;
- set keyframes;
- import footage;
- configure render queue;
- rename/restructure project;
- run a user command;
- build rigs/templates.

Scripts can create coherent Undo history and return command success/error.

A script should validate before mutation and reacquire host references after structural changes where required.

## Expressions are evaluation

Typical expression responsibilities:

- calculate one property from time;
- link properties;
- procedural animation;
- derive values from controls/layers;
- small deterministic math.

An expression may be evaluated many times, including during preview/render and cache/dependency work.

Therefore expression code should not depend on hidden call order.

## No side-effect architecture

Treat expressions as value functions.

Do not design an expression to:

- write files;
- mutate the project;
- update UI;
- manage network state;
- keep a reliable mutable global counter;
- perform a one-time project migration.

Those belong in scripts/panels/native tools.

## Performance

An expression can run on many properties across many frames.

Common expensive patterns:

- repeated broad layer/property searches;
- repeated string/path logic;
- deep cross-comp dependency chains;
- duplicated heavy math on many properties;
- unnecessary sample loops.

Move one-time setup into a script when the resulting project can express the dependency directly.

Do not precompute dynamic values in a script if that changes required semantics.

## Identity and naming

Expressions that reference layers/effects by visible name can break after rename/localization/user edits.

Where the expression API provides stable approaches, prefer them; for product-generated rigs, define a naming/metadata policy and migration behavior.

A script generating the rig should validate that the references it creates actually resolve.

## Error handling

Script error:

~~~text
command fails
→ report structured/user-visible error
→ mutation may need cleanup
~~~

Expression error:

~~~text
property evaluation fails
→ AE reports expression error
→ rendered/evaluated value may fall back according to host behavior
~~~

Do not hide a script failure by injecting a broken expression and hoping AE reports it later.

## Version compatibility

Expression engines and available functions can change between AE generations.

For a product shipping expression rigs:

- record oldest/newest tested AE;
- keep old-project fixtures;
- test save/reopen;
- test expressions after project migration;
- avoid relying on a function merely because another Adobe host/browser supports it.

## Script-generated expressions

This is a valid hybrid pattern:

~~~text
script validates rig
→ creates controls/layers
→ assigns known expression source
→ verifies expression enabled/resolves
→ user animates controls
~~~

Treat the expression text as versioned product data.

If its semantics change, consider migration of existing projects rather than silently overwriting user-edited expressions.

## When to choose which

Use a script when the question is:

> What should the project/tool do now?

Use an expression when the question is:

> What value should this property have when AE evaluates it?

Use both when a script creates a stable project structure and expressions provide ongoing value relationships.

## Testing

For script + expression products test:

- fresh rig creation;
- duplicate rig;
- renamed user layers;
- missing target;
- old project;
- save/reopen;
- random frame seeks;
- render queue;
- expression disabled/error state;
- performance on many instances.

See [object model](01-OBJECT-MODEL.md).

## Законченный rig route

[ES3 demo rig](../16-WORKING-TEMPLATES/jsx-tool/build-demo-rig.jsx) создаёт новую
640×360 comp, Null/Slider, text, linear opacity keys, marker и mask. Script
обращается по matchNames; expression связывает opacity с product-controlled
`Bible Control`/`Bible Amount`. Expression прибавляет Slider к анимированному `value`
и ограничивает 0…100. При Slider50 expected opacity=50 в t=0 и100 в t=1;
отключение expression возвращает keyed0→100. Это expectations, не host observation.
`valueAtTime(0,false)` + `expressionEnabled/expressionError` проверяют resolution,
не все frames. Имена expression не становятся stable IDs: rename/missing control
сломает rig; duplicate/migration требует policy владельца продукта.

Expression literal фиксирован, не user string interpolation. Для динамического
имени escape backslash, quote и linebreak в JS literal либо использовать validated
layer-control strategy; не вставлять произвольный текст как executable expression.
Source example не запускался в AE; host expression engine/support нужно проверять
на целевой версии. В error path удаляется только вновь созданная comp; Undo не
считается atomic rollback. User-edited expression не перезаписывается migration
без явного согласия.

### Source/readback scope — 2026-10-07

The rig uses scripting match names for transforms/text/effect groups; the expression
uses fixed English product-controlled layer/effect names and numeric parameter1,
not match-name lookup or persisted stable IDs. It checks evaluation at t=0 only and
does not assert the returned numeric value. Expected values for Slider50 are50 at0,
100 at1; intermediate values follow the chosen linear keys plus clamp. These are
declared expectations, not assertions already executed by the source.

For dynamic expression source, literal escaping must cover backslash, quote,
CR/LF and Unicode line separators U+2028/U+2029 for the chosen engine. JSON transport
escaping and expression-literal escaping are different boundaries; do not assume
one arbitrary JSON serializer makes injected code safe. The fixed source here avoids
interpolation entirely. Feature/version and expression-engine qualification remain
separate from Node syntax checks and native SDK25.6 provenance.
