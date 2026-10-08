# Expressions vs scripts

Scripts and expressions both use JavaScript-like syntax, but they occupy different semantic roles in After Effects.

## Core distinction

## Practical expression contracts — reviewed2026-10-08

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
