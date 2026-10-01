# Masks: reference lifetime, outline stream и geometry

**Baseline source review:** Adobe After Effects SDK **25.6 build 61**.
**Suites in that SDK:** `AEGP_MaskSuite6`, `AEGP_MaskOutlineSuite3`, `AEGP_StreamSuite6`, `AEGP_KeyframeSuite5`, `AEGP_DynamicStreamSuite4`.
**Verification level:** SDK source-reviewed; host mutation/render tests remain pending.

Mask в AEGP состоит из двух уровней: metadata самого mask object и animatable streams (outline/opacity/feather/expansion). Не пытайтесь хранить всю маску как один C++ объект с одним lifetime.

## 1. Suite versions в SDK 25.6

`AE_GeneralPlug.h` объявляет:

- `AEGP_MaskSuite6`, macro version **7**;
- `AEGP_MaskOutlineSuite3`, macro version **5**;
- mask streams читаются через `AEGP_StreamSuite6`.

Как и в других AEGP families, номер в имени struct не равен обязательно числовой версии `AcquireSuite`.

## 2. MaskRefH — отдельный owned reference

Количество masks:

```cpp
A_long count = 0;
ERR(suites.MaskSuite6()->AEGP_GetLayerNumMasks(layerH, &count));
```

`AEGP_GetLayerMaskByIndex` прямо помечает returned `AEGP_MaskRefH` как ref, который caller должен освободить `AEGP_DisposeMask`.

```cpp
AEGP_MaskRefH maskH = nullptr;
ERR(suites.MaskSuite6()->AEGP_GetLayerMaskByIndex(
    layerH, index, &maskH));

// use maskH

if (maskH) {
    ERR2(suites.MaskSuite6()->AEGP_DisposeMask(maskH));
}
```

`AEGP_DeleteMaskFromLayer` **не заменяет dispose**: header специально говорит, что после удаления всё равно нужно `DisposeMask(mask_refH)`. Это важное отличие между удалением project object и освобождением caller reference.

## 3. Создание и metadata mask

`AEGP_CreateNewMask` — undoable operation и возвращает mask ref + optional index. Metadata-level функции отдельно управляют:

- invert;
- mode;
- motion blur state;
- feather falloff;
- color;
- lock state;
- RotoBezier state;
- mask ID.

Имя mask больше не относится к старым Get/SetMaskName: header помечает их obsolete и направляет к Dynamic Stream API для mask hierarchy/name operations.

Не смешивайте metadata с outline geometry. `SetMaskMode` не меняет path, а редактирование path не меняет mode/invert автоматически.

## 4. Outline, opacity, feather и expansion — streams

Outline stream:

```cpp
AEGP_StreamRefH outlineH = nullptr;
ERR(suites.StreamSuite6()->AEGP_GetNewMaskStream(
    plugin_id,
    maskH,
    AEGP_MaskStream_OUTLINE,
    &outlineH));
```

Тот же Stream Suite получает opacity/feather/expansion через соответствующие `AEGP_MaskStream_*` constants. Следовательно, animation этих свойств подчиняется обычным stream/keyframe правилам.

## 5. Mask outline value принадлежит StreamValue lifetime

Для path сначала получите typed stream value:

```cpp
A_Time t{0,1};
AEGP_StreamValue2 value{};
A_Boolean have_valueB = FALSE;

ERR(suites.StreamSuite6()->AEGP_GetNewStreamValue(
    plugin_id, outlineH, AEGP_LTimeMode_CompTime, &t, TRUE, &value));

if (!err) {
    have_valueB = TRUE;
    // value.val.mask is AEGP_MaskOutlineValH for MASK stream
}
```

Сам `AEGP_MaskOutlineValH` в таком сценарии является частью полученного `AEGP_StreamValue2`. После работы dispose делается через `AEGP_DisposeStreamValue`; затем dispose самого `outlineH` через `AEGP_DisposeStream`.

Не сохраняйте `value.val.mask` после disposal stream value.

## 6. Геометрия outline: индексы и tangents

`AEGP_MaskOutlineSuite3` даёт:

- open/closed state;
- число segments;
- get/set vertex info;
- create/delete vertex;
- variable feather points.

Ключевые детали header:

- N segments означает segments `0..N-1`;
- vertex index имеет диапазон `0..num_segments`;
- для closed mask `vertex[0] == vertex[num_segments]`;
- in/out tangents задаются **относительно position**;
- `SetMaskOutlineVertexInfo` требует уже существующий vertex;
- `CreateVertex` вставляет vertex по index и сдвигает последующие индексы;
- setting vertex 0 имеет специальный эффект на out tangent последнего vertex.

Поэтому нельзя обращаться с outline как с обычным `std::vector<Point>` без учёта closed-path alias и tangent semantics.

## 7. Запись outline обратно

Типичный static-path workflow:

```text
GetNewMaskStream(OUTLINE)
→ GetNewStreamValue
→ проверить StreamType == MASK
→ изменить AEGP_MaskOutlineValH через MaskOutlineSuite3
→ SetStreamValue, только если static-write contract допустим
→ DisposeStreamValue
→ DisposeStream
→ DisposeMask
```

Если outline имеет keyframes или expression-driven behavior, используйте Keyframe Suite / соответствующий evaluation model вместо blind `SetStreamValue`.

## 8. Variable feather points

Suite3 отдельно имеет get/set/create/delete feather points. Feather point содержит segment binding и позицию на segment; structural изменение vertices может менять смысл сохранённых indices.

Рекомендация: после insert/delete vertices заново читать feather/segment topology перед последующими index-based edits.

## 9. Structural edits и Undo

`CreateNewMask` и `DeleteMaskFromLayer` помечены undoable. Dynamic stream operations над mask children тоже могут быть undoable по своим contracts.

Для пользовательской команды, которая одновременно создаёт mask, меняет path и свойства, используйте один общий Undo group на уровне command workflow. Это не освобождает от каждой resource cleanup obligation.

## 10. Adobe Projector: полезный geometry pattern, но не ownership gold standard

`Projector.cpp` в supplied SDK:

- создаёт mask через старый `MaskSuite4`;
- получает outline через старый `StreamSuite2`;
- создаёт четыре vertices и меняет geometry через `MaskOutlineSuite2`;
- записывает value обратно и dispose-ит stream value.

Но просмотренный код **не вызывает `AEGP_DisposeMask(new_maskH)`** после `AEGP_CreateNewMask`, хотя current header для mask refs формулирует explicit dispose lifecycle и `DeleteMaskFromLayer` отдельно напоминает о необходимости dispose. Поэтому sample нельзя использовать как доказательство, что MaskRef cleanup не нужен.

Это source finding, не измеренная утечка в host. Новая production-реализация должна следовать current header и проверяться leak/lifecycle test-ом.

## 11. Host acceptance matrix

Минимальные реальные тесты:

- layer без masks / с несколькими masks;
- create + undo/redo;
- delete + reference cleanup;
- invert/mode/lock/color;
- open и closed outlines;
- insert/delete vertices;
- tangent behavior у vertex 0;
- animated outline/opacity/feather/expansion;
- variable feather points;
- RotoBezier toggle;
- save/reopen;
- repeated execution + leak diagnostics.

До этого глава имеет уровень SDK source review, не host-verified.

## Source record

Точные hashes, sample ranges и version corrections: [Masks/text/footage SDK 25.6 review](../18-SDK-HEADER-TOOLS/11-MASK-TEXT-FOOTAGE-SDK25.6.md).