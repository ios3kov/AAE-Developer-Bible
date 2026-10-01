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
- `RenderQueueRecipes.cpp` — add comp, re-query queue and set output path; **the final render-state argument has an open correctness finding below**.

## Known source-review finding — 2026-10-01

`RenderQueueRecipes.cpp` calls `AEGP_SetRenderState(rq_itemH, TRUE)`. The supplied SDK's RQItemSuite3 takes `AEGP_RenderItemStatusType`, not a Boolean. With the usual TRUE=1 this requests **UNQUEUED**, not **QUEUED=2**. The earlier description “enable render” was therefore misleading. Do not use the recipe unchanged as a verified queue-enabling operation.

[The SDK review](../../18-SDK-HEADER-TOOLS/09-AEGP-PROJECT-RENDER-SDK25.6.md) records exact source ranges; [the AEGP chapter](../../03-AEGP/02-PROJECT-RENDER-AUTOMATION.md) explains named status constants, readback, queue invalidation and partial failures. The C++ implementation has not been changed or host-tested in this editorial iteration. Code correction and its behavioral checks remain open; documentation CI does not close them.

## Verification label

**Historical SDK 25.6 macOS syntax/type baseline; linking and host tests pending.** A successful compiler check does not prove correct enum selection or operation semantics. The finding above remains open despite the earlier syntax baseline.

Команда и результаты: [VERIFICATION.md](../../VERIFICATION.md). Сохраните relative includes к `19-NATIVE-CODE-FOUNDATION` или перенесите helpers вместе с recipes. Host callbacks, вызывающие recipes, должны иметь exception boundary.
