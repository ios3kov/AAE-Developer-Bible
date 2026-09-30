# Streams / properties / expressions

**Suites:** `AEGP_StreamSuite7`, `AEGP_DynamicStreamSuite4`  
**Confidence:** SDK-verified.

В AEGP «property» обычно представлен `AEGP_StreamRefH`.

## Получить Position stream слоя

```cpp
AEGP_StreamRefH streamH = nullptr;
ERR(suites.StreamSuite7()->AEGP_GetNewLayerStream(
    plugin_id,
    layerH,
    AEGP_LayerStream_POSITION,
    &streamH));

// use...
ERR2(suites.StreamSuite7()->AEGP_DisposeStream(streamH));
```

Перед запросом незнакомого stream:

```cpp
A_Boolean legalB = FALSE;
ERR(suites.StreamSuite7()->AEGP_IsStreamLegal(
    layerH, AEGP_LayerStream_POSITION, &legalB));
```

---

## Прочитать value в момент времени

```cpp
A_Time t{0, 1};
AEGP_StreamValue2 value{};

ERR(suites.StreamSuite7()->AEGP_GetNewStreamValue(
    plugin_id,
    streamH,
    AEGP_LTimeMode_CompTime,
    &t,
    FALSE,      // post-expression
    &value));

// read value according to stream type

ERR2(suites.StreamSuite7()->AEGP_DisposeStreamValue(&value));
```

Не читать неправильное union field. Сначала:

```cpp
AEGP_StreamType type = AEGP_StreamType_NO_DATA;
ERR(suites.StreamSuite7()->AEGP_GetStreamType(streamH, &type));
```

---

## Записать non-time-varying value

`AEGP_SetStreamValue` допустим для stream, который не time-varying.

```cpp
A_Boolean timevaryingB = FALSE;
ERR(suites.StreamSuite7()->AEGP_IsStreamTimevarying(
    streamH, &timevaryingB));

if (!timevaryingB) {
    A_Time t{0, 1};
    AEGP_StreamValue2 value{};

    ERR(suites.StreamSuite7()->AEGP_GetNewStreamValue(
        plugin_id, streamH,
        AEGP_LTimeMode_CompTime,
        &t, TRUE, &value));

    value.val.one_d = 50.0;

    ERR(suites.StreamSuite7()->AEGP_SetStreamValue(
        plugin_id, streamH, &value));

    ERR2(suites.StreamSuite7()->AEGP_DisposeStreamValue(&value));
}
```

Для animated property — Keyframe Suite.

---

## Effect parameter stream

```cpp
AEGP_StreamRefH paramH = nullptr;
ERR(suites.StreamSuite7()->AEGP_GetNewEffectStreamByIndex(
    plugin_id,
    effectH,
    param_index,
    &paramH));

// read/write/keyframe
ERR2(suites.StreamSuite7()->AEGP_DisposeStream(paramH));
```

`param_index` должен соответствовать effect parameter contract.

---

## Expression

```cpp
A_Boolean enabledB = FALSE;
ERR(suites.StreamSuite7()->AEGP_GetExpressionState(
    plugin_id, streamH, &enabledB));

ERR(suites.StreamSuite7()->AEGP_SetExpression(
    plugin_id, streamH, utf16_expression));

ERR(suites.StreamSuite7()->AEGP_SetExpressionState(
    plugin_id, streamH, TRUE));
```

`GetExpression` возвращает memory handle — освободить по контракту через Memory Suite.

---

## Dynamic stream traversal

Dynamic Stream Suite нужен для hierarchy вроде Effects, masks и property groups.

Паттерн:

```text
root StreamRefH
→ GetNumStreamsInGroup
→ GetNewStreamRefByIndex
→ GetMatchName
→ recurse
→ DisposeStream
```

После `AddStream`, `DeleteStream`, `ReorderStream` или duplicate **не использовать старые child refs** — повторно пройти hierarchy.

---

## Match name first

Для automation:

```text
display name = UI/localized/user-visible
match name   = stable programmatic identity (где предусмотрен)
```

Искать dynamic property group по match name, а не по UI строке.

---

## AE 26.5: layer-param render stage

`AEGP_StreamSuite7` добавляет отдельный get/set render stage для `PF_Param_LAYER`: source before masks / after masks / через конкретный effect stage.

Это новый feature. Делать runtime/host gating и не требовать StreamSuite7 для функций, которым достаточно старого stream API.
