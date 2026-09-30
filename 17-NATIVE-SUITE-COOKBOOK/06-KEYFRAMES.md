# Keyframe recipes

**Suites:** `AEGP_KeyframeSuite3+`, `AEGP_StreamSuite`  
**Confidence:** SDK-verified + official `Easy Cheese` pattern.

## Узнать число keyframes

```cpp
A_long count = 0;
ERR(suites.KeyframeSuite3()->AEGP_GetStreamNumKFs(
    streamH, &count));
```

---

## Время keyframe

```cpp
A_Time t{};
ERR(suites.KeyframeSuite3()->AEGP_GetKeyframeTime(
    streamH,
    key_index,
    AEGP_LTimeMode_CompTime,
    &t));
```

---

## Добавить один keyframe

```cpp
A_Time t{1, 1};
A_long key_index = 0;

ERR(suites.KeyframeSuite3()->AEGP_InsertKeyframe(
    streamH,
    AEGP_LTimeMode_CompTime,
    &t,
    &key_index));
```

После этого задать value через Keyframe Suite.

---

## Правильный batch insert

Официальный guide отдельно предупреждает: одиночные inserts могут быть дорогими для undo. Для серии keyframes использовать begin/end cookie.

```cpp
AEGP_AddKeyframesInfoH addH = nullptr;
ERR(suites.KeyframeSuite3()->AEGP_StartAddKeyframes(
    streamH, &addH));

A_long idx0 = 0;
A_Time t0{0, 1};
ERR(suites.KeyframeSuite3()->AEGP_AddKeyframes(
    addH, AEGP_LTimeMode_CompTime, &t0, &idx0));

AEGP_StreamValue2 v0{};
// v0 must be valid for stream type;
// safest pattern is derive correctly-typed value via StreamSuite.
ERR(suites.KeyframeSuite3()->AEGP_SetAddKeyframe(
    addH, idx0, &v0));

// ... more keys ...

ERR(suites.KeyframeSuite3()->AEGP_EndAddKeyframes(
    TRUE,   // commit
    addH));
addH = nullptr;
```

Если операция прерывается — `EndAddKeyframes(FALSE, addH)` для отмены transaction по контракту suite.

---

## Production pattern: derive typed value

Не строить `AEGP_StreamValue2` вслепую:

```text
GetStreamType
→ GetNewStreamValue at nearby/current time
→ modify correct union member
→ SetAddKeyframe / SetKeyframeValue
→ DisposeStreamValue
```

Так `streamH`/type-specific data корректно заполнены.

---

## Интерполяция и ease

После вставки:

```text
GetValidInterpolations
→ SetKeyframeInterpolation
→ SetKeyframeTemporalEase
→ optional spatial tangents / flags
```

Сначала проверять поддерживаемые interpolation flags — не каждая property поддерживает spatial/ease одинаково.

---

## Удаление

```cpp
ERR(suites.KeyframeSuite3()->AEGP_DeleteKeyframe(
    streamH, key_index));
```

Удаление сдвигает subsequent indices. При массовом delete идти с конца к началу либо каждый раз re-query.

---

## Undo

Batch keyframe edit обычно всё равно следует помещать в один `AEGP_StartUndoGroup` / `AEGP_EndUndoGroup` на уровне пользовательской команды.
