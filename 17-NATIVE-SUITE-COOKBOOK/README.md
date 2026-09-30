# Native Suite Cookbook

**Edition:** v0.3  
**Target snapshot:** After Effects 26.5 SDK, 2026-09-30

Этот раздел — практический слой над AEGP/native API: **какую suite брать, какой handle получить, кто им владеет, что надо dispose-ить и в каком порядке вызывать функции**.

## Карта

| Задача | Основные suites | Recipe |
|---|---|---|
| проект / root folder / project items | Proj + Item | [01](01-PROJECT-ITEMS.md) |
| создать composition / solid / camera / light | Comp | [02](02-COMPOSITIONS.md) |
| найти / добавить / дублировать / удалить layer | Layer + Comp | [03](03-LAYERS.md) |
| найти / применить / удалить effect | Effect | [04](04-EFFECTS.md) |
| читать / писать properties и expressions | Stream + DynamicStream | [05](05-STREAMS-PROPERTIES.md) |
| keyframes, interpolation, batch insert | Keyframe + Stream | [06](06-KEYFRAMES.md) |
| masks / mask path | Mask + MaskOutline + Stream | [07](07-MASKS.md) |
| text / markers | TextDocument + Marker + Stream | [08](08-TEXT-MARKERS.md) |
| import footage / interpretation | Footage | [09](09-FOOTAGE-IMPORT.md) |
| render frame → pixels | RenderOptions + Render + World | [10](10-RENDER-FRAMES.md) |
| render queue / output modules | RenderQueue + RQItem + OutputModule | [11](11-RENDER-QUEUE.md) |
| undo / memory / persistent data | Utility + Memory + PersistentData | [12](12-MEMORY-UNDO-PERSISTENCE.md) |
| guides / views / selection | Guide + ItemView + Collection | [13](13-GUIDES-VIEWS-SELECTION.md) |
| handles / invalidation / UI thread | cross-cutting | [14](14-LIFETIME-THREADING.md) |
| copy/paste index | — | [15](15-RECIPE-INDEX.md) |
| suite → function map | all AEGP suites | [16](16-SUITE-FUNCTION-MAP.md) |

## Уровни доверия

- **SDK-verified** — имя и shape вызова сверены с публичным AE SDK Guide / 26.5 notes.
- **sample-derived** — порядок работы соответствует официальным sample-проектам Adobe.
- **host-test-required** — архитектура корректная, но бинарная проверка требует установленного proprietary SDK + конкретного AE host.

> В этой песочнице нет proprietary Adobe SDK headers и After Effects host, поэтому здесь **не заявляется бинарный host-test**. C++ куски специально оформлены как drop-in код для официального SDK sample, а не как «самодельный SDK».

## Базовый pipeline AEGP

```text
AE loads .aex/.plugin
    ↓
EntryPointFunc()
    ↓
AEGP_PluginID + SPBasicSuite
    ↓
Acquire/use suite
    ↓
Get host-owned handle/ref
    ↓
Perform operation
    ↓
Dispose only what API says plug-in owns
    ↓
Return A_Err
```

## Главное правило

Не хранить в долгоживущем состоянии `AEGP_StreamRefH`, `AEGP_EffectRefH`, RQ/output-module refs и подобные ссылки без явной гарантии API. Структурное изменение проекта часто делает их невалидными. Долговременно хранить лучше **stable IDs / match names / собственные данные**, а handles получать заново.
