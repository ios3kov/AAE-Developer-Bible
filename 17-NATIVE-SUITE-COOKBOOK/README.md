# Native Suite Cookbook

**Edition:** v1.1 documentation line  
**Primary acceptance baseline:** After Effects / SDK 25.6 for the current Bible plan. Later-version notes are explicitly version-gated.

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

- **SDK source-reviewed** — declaration/ownership statement сверены с конкретным supplied SDK snapshot; это не runtime result.
- **sample-derived** — pattern найден в официальном sample-проекте Adobe; sample может использовать старую suite generation.
- **syntax/type baseline** — отдельный recorded compiler check для конкретного source snapshot.
- **host-test-required** — поведение ещё должно быть проверено внутри указанного After Effects build.

> Supplied SDK 25.6 используется для source review и локальной проверки контрактов, но Adobe headers не публикуются в репозитории. Recorded compiler baseline и host acceptance — отдельные evidence levels. C++ куски остаются drop-in кодом для официального SDK sample, а не «самодельным SDK».

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


## Version discipline

Главы `05-STREAMS-PROPERTIES.md` и `06-KEYFRAMES.md` перепроверены по supplied SDK 25.6: `AEGP_StreamSuite6`, `AEGP_DynamicStreamSuite4`, `AEGP_KeyframeSuite5`. Главы `07-MASKS.md`, `08-TEXT-MARKERS.md`, `09-FOOTAGE-IMPORT.md` также приведены к baseline 25.6: `MaskSuite6`, `MaskOutlineSuite3`, `TextDocumentSuite1`, `MarkerSuite3`, `FootageSuite5`, `ItemSuite9`, `CompSuite12`, `LayerSuite9`. Более поздние API не должны молча становиться baseline 25.6. Источники: `18-SDK-HEADER-TOOLS/10-STREAMS-KEYFRAMES-SDK25.6.md` и `11-MASK-TEXT-FOOTAGE-SDK25.6.md`.
