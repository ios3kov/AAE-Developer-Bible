# Render correctness

## Golden image strategy

Не сравнивать screenshots UI. Сравнивать actual rendered pixel output.

Для deterministic CPU path:
- exact hash, если mathematically stable across platforms;
- otherwise pixel diff with strict documented tolerance.

Для GPU/float:
- max absolute error;
- mean/RMS error;
- count of pixels above tolerance;
- separate alpha tolerance.

## Test patterns

- impulse pixel;
- horizontal/vertical gradient;
- checkerboard 1px/2px;
- transparent colored edges;
- solid black/white/gray;
- HDR negative→positive ramp;
- odd dimensions (1x1, 3x5, 1919x1079);
- very wide/tall image;
- nontrivial alpha.

## Temporal effects

Если output зависит от time:
- random seek order;
- backwards render;
- duplicate frames;
- skipped frames;
- render after cache purge;
- same frame from different render contexts.

## Pass condition

Tolerance должна быть частью test spec до реализации backend-а.
