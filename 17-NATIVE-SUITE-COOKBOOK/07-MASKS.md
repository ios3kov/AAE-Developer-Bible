# Mask recipes

**Suites:** `AEGP_MaskSuite6`, `AEGP_MaskOutlineSuite3`, `AEGP_StreamSuite7`  
**Confidence:** SDK-verified.

## Сколько masks на layer

```cpp
A_long count = 0;
ERR(suites.MaskSuite6()->AEGP_GetLayerNumMasks(
    layerH, &count));
```

## Получить mask

```cpp
AEGP_MaskRefH maskH = nullptr;
ERR(suites.MaskSuite6()->AEGP_GetLayerMaskByIndex(
    layerH, index, &maskH));

// ...
ERR2(suites.MaskSuite6()->AEGP_DisposeMask(maskH));
```

---

## Создать mask

```cpp
AEGP_MaskRefH maskH = nullptr;
A_long mask_index = 0;
ERR(suites.MaskSuite6()->AEGP_CreateNewMask(
    layerH,
    &maskH,
    &mask_index));
```

После создания mask path живёт как stream, а не как «vector<point> внутри mask handle».

---

## Получить Outline stream

```cpp
AEGP_StreamRefH outline_streamH = nullptr;
ERR(suites.StreamSuite7()->AEGP_GetNewMaskStream(
    plugin_id,
    maskH,
    AEGP_MaskStream_OUTLINE,
    &outline_streamH));
```

Затем `GetNewStreamValue` возвращает mask outline value/handle по соответствующему stream type. Геометрию читать/писать через Mask Outline Suite.

Dispose:

```cpp
ERR2(suites.StreamSuite7()->AEGP_DisposeStream(outline_streamH));
```

---

## Opacity / Feather / Expansion

Те же mechanics:

```text
GetNewMaskStream(maskH, AEGP_MaskStream_OPACITY)
GetNewMaskStream(maskH, AEGP_MaskStream_FEATHER)
GetNewMaskStream(maskH, AEGP_MaskStream_EXPANSION)
```

Дальше это обычные stream/keyframe operations.

---

## Изменить mask mode / invert

Mask Suite предоставляет metadata-level operations: mode, invert, lock и прочее. Их не надо пытаться менять через outline geometry.

---

## Удалить mask

После delete mask reference считается invalid:

```cpp
ERR(suites.MaskSuite6()->AEGP_DeleteMaskFromLayer(maskH));
maskH = nullptr;
```

Если после этого нужны соседние masks — re-query их по текущему layer state.
