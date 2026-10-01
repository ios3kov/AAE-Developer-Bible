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
- `CompLayerRecipes.cpp` — create comp, enumerate layers, LayerID lookup; lifetime must follow the applicable SDK contract.
- `EffectStreamRecipes.cpp` — find/apply effect, read/write scalar stream.
- `KeyframeRecipes.cpp` — batch keyframe transaction pattern.
- `RenderRecipes.cpp` — checkout/get-world/checkin pattern.
- `RenderQueueRecipes.cpp` — add comp, re-query queue, set output path, queue the item with the named enum and verify state by readback.

## Render-queue enum correction — 2026-10-01

Earlier source review found that this recipe passed `TRUE` to `AEGP_SetRenderState`. The supplied SDK declares an `AEGP_RenderItemStatusType` there; `TRUE=1` maps to `UNQUEUED`, while `QUEUED=2`.

The recipe is now corrected to:

- pass `AEGP_RenderItemStatus_QUEUED`;
- call `AEGP_GetRenderState` afterwards;
- fail if the readback is not `AEGP_RenderItemStatus_QUEUED`.

This closes the **source-level argument-selection defect**. It does **not** prove runtime queue behavior inside After Effects. Queue STOPPED requirements, valid output configuration, invalidation behavior and actual render execution still require host verification.

[The SDK review](../../18-SDK-HEADER-TOOLS/09-AEGP-PROJECT-RENDER-SDK25.6.md) preserves the original finding and source evidence.

## Verification label

**Historical SDK 25.6 macOS syntax/type baseline; linking and host tests pending.** The enum-selection source defect has been corrected, but this revised source has not yet been promoted to host-verified queue behavior.

Команда и результаты: [VERIFICATION.md](../../VERIFICATION.md). Сохраните relative includes к `19-NATIVE-CODE-FOUNDATION` или перенесите helpers вместе с recipes. Host callbacks, вызывающие recipes, должны иметь exception boundary.
