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
- `EffectStreamRecipes.cpp` — find/apply effect through current SDK 25.6 `EffectSuite5`, read/write scalar stream through `StreamSuite6`.
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

**Evidence boundary:** historical SDK 25.6 syntax/type evidence exists for an earlier source snapshot. Current recipes are SOURCE EXAMPLES / SDK-CONTRACT-REVIEWED where noted; Bible does not claim runtime results unless a separate runtime record exists. The render-queue enum defect is corrected at source level.

Команда и результаты: [VERIFICATION.md](../../VERIFICATION.md). Сохраните relative includes к `19-NATIVE-CODE-FOUNDATION` или перенесите helpers вместе с recipes. Host callbacks, вызывающие recipes, должны иметь exception boundary.
