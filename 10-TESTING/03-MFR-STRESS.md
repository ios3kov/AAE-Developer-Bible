# MFR stress tests

## Purpose

Поймать race/deadlock/state bleed, которые не проявляются в single-frame preview.

## Scenarios

1. Один effect instance, long comp, full render.
2. 20+ instances одного effect.
3. Несколько comps в render queue.
4. Одновременно разные parameter values.
5. Rapid cancel/restart renders.
6. Cache purge между runs.
7. MFR off → on → off.
8. GPU backend вместе с MFR.
9. Old project with migrated sequence data.
10. Repeated render loop 50–100 раз для flaky races.

## Observability

Debug build log:
- instance id;
- frame/time;
- thread id;
- backend;
- sequence/global state revision;
- cache key/hit.

Лог должен позволять доказать, что два frames не пишут один unsafe state.

## Failures

Любой из этих симптомов — release blocker:
- nondeterministic pixels;
- sporadic crash;
- hang/deadlock;
- state from another layer/instance;
- increasing memory every render;
- corrupted project after save/reopen.
