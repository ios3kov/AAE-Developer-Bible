# Performance architecture

## Оптимизировать по слоям

1. **Algorithm** — убрать лишнюю работу до SIMD/GPU.
2. **Region/extent** — не считать пиксели, которые не нужны.
3. **Memory** — cache locality, reuse, no per-pixel allocation.
4. **Threading/MFR** — concurrent frames без lock bottleneck.
5. **Compute Cache** — повторно использовать дорогие расчёты, если корректно.
6. **GPU** — только там, где transfer/dispatch overhead окупается.
7. **Host interaction** — минимизировать checkouts/suite calls внутри hot loops.

## Golden benchmark

Хранить 3 класса проектов:
- tiny: overhead-sensitive;
- typical: real production comp;
- stress: 4K/8K, long effect stack, extreme params.

Снимать:
- render wall time;
- per-frame median/p95;
- CPU utilization;
- peak memory;
- GPU time if measurable;
- cache hit rate;
- MFR scaling 1→N concurrent frames.

Нельзя принимать optimization, если она ломает determinism, color precision или stability.
