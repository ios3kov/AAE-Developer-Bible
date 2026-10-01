# Render correctness

Render tests should compare actual output data, not screenshots of the After Effects UI.

## Golden strategy

Choose the strictest comparison that remains valid for the algorithm.

### Exact comparison

Use exact bytes/hash only when output is expected to be bit-identical for the defined environment.

Good candidates:

- integer copy/pass-through;
- deterministic lookup/table operations;
- exact alpha/channel routing.

Do not use an exact hash for a floating GPU path if mathematically equivalent outputs can vary in low bits.

### Tolerance comparison

For float/GPU/numerical algorithms record:

- maximum absolute error;
- maximum relative error where meaningful;
- mean/RMS error;
- count/percentage of pixels above threshold;
- separate alpha threshold;
- NaN/Inf count.

Tolerance is part of the test specification, not something chosen after seeing the result.

## Compare in a controlled representation

Avoid differences caused only by output codec or color management when the test intends to measure the effect algorithm.

Where possible compare:

- uncompressed/lossless output;
- known project working space;
- explicit bit depth;
- known alpha interpretation.

If color management is part of the feature, then color-management behavior itself must become part of the fixture.

## Test patterns

Use synthetic patterns that make specific bugs obvious:

- single impulse pixel;
- horizontal gradient;
- vertical gradient;
- 1px and 2px checkerboard;
- transparent colored edges;
- fully transparent nonzero RGB;
- solid black/white/mid-gray;
- primary/secondary colors;
- HDR negative -> positive ramp;
- odd dimensions: 1x1, 3x5, 1919x1079;
- very wide/tall frame;
- nontrivial alpha.

Natural images are useful later but are poor at isolating indexing/alpha/rowbytes defects.

## Alpha

Test independently:

- opaque;
- fully transparent;
- partial alpha;
- colored transparent pixels;
- premultiplied-looking edge cases if algorithm interacts with alpha.

Never infer alpha correctness from RGB similarity.

## Rowbytes and origins

A render implementation must not assume tightly packed rows or zero origins unless the API guarantees it for that path.

Fixtures should exercise:

- odd width;
- cropped/offset layers;
- partial render region;
- nonzero origin;
- ROI smaller than full frame.

## SmartFX ROI

For SmartFX/pre-render capable effects include:

- full frame;
- small requested rectangle;
- rectangle touching each edge;
- empty rectangle;
- single-pixel rectangle;
- output request larger/smaller than meaningful source region.

Assert both output correctness and safe behavior.

## Temporal effects

If output depends on time/history:

- sequential forward render;
- random seek order;
- backwards seeks;
- repeated same frame;
- skipped frames;
- cache purge;
- render after project reopen;
- same frame requested from different render contexts.

The same frame/time/configuration should not depend on accidental prior preview order unless the effect explicitly implements documented temporal state.

## CPU/GPU equivalence

Compare CPU and each GPU backend using the same input/output metric.

Report:

~~~text
backend
frame/time
max abs diff
RMS diff
alpha max diff
pixels above tolerance
~~~

A fast GPU output outside tolerance is a correctness failure.

## Error pixels

Diff visualization helps triage.

Generate:

- absolute-difference image;
- threshold mask;
- coordinates/value of worst N pixels.

Preserve those artifacts on CI failure.

## Golden update policy

Changing expected output is code review work.

A golden update must explain:

- intended algorithm change;
- why old expected output is wrong/obsolete;
- tolerance change if any;
- affected supported versions.

Never "accept new golden" merely to make CI green.

## Pass condition

Every fixture defines PASS before implementation changes are evaluated.

A test with no fixed expected metric is an observation, not acceptance evidence.
