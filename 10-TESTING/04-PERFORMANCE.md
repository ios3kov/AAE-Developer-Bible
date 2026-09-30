# Performance testing

## Metrics

- cold first frame;
- warm frame;
- full comp render time;
- per-frame median/p95;
- peak RSS/memory;
- MFR scaling;
- CPU utilization;
- GPU kernel + synchronization time;
- cache hit rate.

## Baseline

Каждый release сравнивать с last shipped version на одной машине/AE build/project.

Пример gate:

```text
Typical project: no >5% regression without explicit approval
Stress project: no OOM / unbounded growth
MFR scaling: no global-lock serialization regression
GPU: must beat CPU on target workload class or have another justified benefit
```

Numbers — product-specific; главное, чтобы threshold был заранее определён.

## Profiling order

1. time whole render;
2. locate slow selector/backend;
3. profile algorithm;
4. allocation profile;
5. lock contention;
6. GPU transfers/sync;
7. host callbacks/checkouts.

Не оптимизировать по ощущениям.
