# Native recipe source — v1.1

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

**SDK 25.6 macOS syntax/type-checked; linking and host tests pending.**

Команда и результаты: [VERIFICATION.md](../../VERIFICATION.md). Сохраните relative includes к `19-NATIVE-CODE-FOUNDATION` или перенесите helpers вместе с recipes. Host callbacks, вызывающие recipes, должны иметь exception boundary.
