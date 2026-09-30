# v0.3 drop-in C++ code

Эти файлы предназначены для **graft в официальный AEGP sample project**, где уже есть:
- Adobe headers;
- `AEGP_SuiteHandler.h`;
- `ERR` / `ERR2` convention;
- PiPL/platform build steps.

Они не пытаются переопределить proprietary SDK.

## Files

- `BibleAegpCommon.h` — no-throw undo guard.
- `ProjectItemRecipes.cpp` — project/root/item traversal.
- `CompLayerRecipes.cpp` — create comp, enumerate layers, stable LayerID.
- `EffectStreamRecipes.cpp` — find/apply effect, read/write scalar stream.
- `KeyframeRecipes.cpp` — batch keyframe transaction pattern.
- `RenderRecipes.cpp` — checkout/get-world/checkin pattern.
- `RenderQueueRecipes.cpp` — add comp, re-query queue, set output path, enable render.

## Verification label

**Compile-shaped / SDK-contract verified; host-test-required.**

В песочнице нет Adobe SDK distribution и AE host, поэтому финальная гарантия — build + run в вашей реальной matrix macOS/Windows.
