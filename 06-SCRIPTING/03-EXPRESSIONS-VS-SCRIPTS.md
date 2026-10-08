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

### Independent expression inventory

`expression-api-inventory-2026-10-08.json`:32 API-category pages/295 third-level headings
including overloads. Page heading strings aren't unique global symbols or complete
signature inventory. `expression-api-reviewed-2026-10-08.json` explicitly records5
full-page operation reviews (52 headings), SHA256/source and coverage route;27 pages
remain unreviewed. No literal mention or downloaded bytes give coverage PASS.

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
