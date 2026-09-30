# SmartFX

SmartFX — render model для более умной коммуникации effect ↔ host и basis для полноценной 32-bpc поддержки в AE effect SDK.

## Зачем

Обычный full-frame подход может заставлять эффект получать/обрабатывать намного больше input, чем реально нужно output region.

SmartFX позволяет строить pipeline, где plug-in:
- на prerender этапе описывает, что ему понадобится;
- host предоставляет нужные inputs/regions;
- render заполняет требуемый output.

## Design pattern

```text
SMART_PRE_RENDER
  determine dependencies / ROI / state
  request required input region(s)
      ↓
SMART_RENDER
  checkout requested data
  execute pure render core
  write only valid output
```

## 32-bpc

Не считать «поддержкой 32-bit» простое преобразование float → 8-bit внутри эффекта. Алгоритм должен быть определён в float domain и иметь понятную политику clamp/negative/HDR values.

## Cache identity

Если output зависит от внешнего/sequence/UI state, который host сам не видит как обычную dependency, cache identity должен учитывать этот state через поддержанные SDK механизмы. Иначе возможны stale frames.

## Test cases

- full frame vs small ROI;
- translated/offscreen layer;
- masks;
- 8/16/32-bpc;
- alpha edge cases;
- parameter animation;
- cache invalidation after custom dialog/UI change;
- CPU/GPU equivalence.
