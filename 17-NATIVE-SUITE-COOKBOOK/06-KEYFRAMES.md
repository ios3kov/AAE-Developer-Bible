# Keyframes: чтение, изменение, batch insert, interpolation

**Baseline source review:** Adobe After Effects SDK **25.6 build 61**.
**Suites in that SDK:** `AEGP_KeyframeSuite5` + `AEGP_StreamSuite6`; для hierarchy/separated dimensions дополнительно `AEGP_DynamicStreamSuite4`.
**Verification level:** SDK-CONTRACT-REVIEWED / RUNTIME-NOT-CLAIMED. Исторический compiler result от 2026-09-30 не содержит exact tested source identity и не подтверждает компиляцию текущего recipe; границы — в [матрице evidence](VERIFICATION.md).

Keyframe API работает поверх конкретного `AEGP_StreamRefH`. Поэтому правильная операция начинается не с индекса ключа, а с доказанного stream context, его типа, dimensionality и временного пространства.

## 1. Ноль keyframes не означает constant property

`AEGP_GetStreamNumKFs` возвращает:

- `AEGP_NumKF_NO_DATA (-1)` для `AEGP_StreamType_NO_DATA`;
- `0`, если keyframes нет;
- положительное число keyframes.

Header отдельно предупреждает: при `0` keyframes stream всё ещё может иметь expression. Для вопроса «меняется ли результат во времени?» используйте также `AEGP_IsStreamTimevarying`, который учитывает expressions.

```cpp
A_long count = 0;
ERR(suites.KeyframeSuite5()->AEGP_GetStreamNumKFs(
    streamH, &count));
```

Не превращайте `count == 0` в утверждение «значение константно».

## 2. Keyframe index — позиция в текущем наборе, а не вечный ID

`AEGP_GetKeyframeTime` принимает `AEGP_KeyframeIndex` и `AEGP_LTimeMode`. После вставки или удаления набор индексов может измениться. Для долгой операции сохраняйте осмысленное время/собственную identity и заново проверяйте нужный keyframe перед mutation.

```cpp
A_Time t{};
ERR(suites.KeyframeSuite5()->AEGP_GetKeyframeTime(
    streamH,
    key_index,
    AEGP_LTimeMode_CompTime,
    &t));
```

Layer time и comp time — разные пространства. Не смешивайте индекс ключа, UI time и raw `A_Time` без явного mode.

## 3. InsertKeyframe: существующий key в том же времени не дублируется

SDK 25.6 прямо говорит, что `AEGP_InsertKeyframe` оставляет stream unchanged, если keyframe уже существует в указанном времени, и возвращает соответствующий index.

```cpp
A_Time t{1, 1};
AEGP_KeyframeIndex index = 0;

ERR(suites.KeyframeSuite5()->AEGP_InsertKeyframe(
    streamH,
    AEGP_LTimeMode_CompTime,
    &t,
    &index));
```

После этого значение задаётся через Keyframe Suite. Сам insert не является универсальной операцией «создать новый уникальный ключ любой ценой».

## 4. Полученное keyframe value имеет ownership

`AEGP_GetNewKeyframeValue` возвращает `AEGP_StreamValue2`, который нужно освободить через `AEGP_DisposeStreamValue`.

```cpp
AEGP_StreamValue2 value{};
A_Boolean have_valueB = FALSE;

ERR(suites.KeyframeSuite5()->AEGP_GetNewKeyframeValue(
    plugin_id, streamH, index, &value));

if (!err) {
    have_valueB = TRUE;
    // modify the union member matching AEGP_StreamType
    ERR(suites.KeyframeSuite5()->AEGP_SetKeyframeValue(
        streamH, index, &value));
}

if (have_valueB) {
    ERR2(suites.StreamSuite6()->AEGP_DisposeStreamValue(&value));
}
```

`AEGP_SetKeyframeValue` не принимает ownership входного value. Cleanup остаётся обязанностью caller.

Официальный `Easy_Cheese` показывает тот же lifetime pattern на старых suite generations: получает keyframe value, изменяет marker и освобождает value через Stream Suite. Копировать нужно ownership pattern, а не старые типы/версии API.

## 5. Тип и dimensionality проверяются до interpolation/ease

Перед редактированием:

```text
GetStreamType
→ GetStreamValueDimensionality
→ GetStreamTemporalDimensionality
→ GetValidInterpolations
→ только затем interpolation/ease/tangent операции
```

`AEGP_GetValidInterpolations` находится в Stream Suite. SDK 25.6 перечисляет LINEAR, BEZIER, HOLD и CUSTOM mask. Нельзя предполагать, что любой stream принимает любой тип interpolation.

`AEGP_GetStreamTemporalDimensionality` определяет допустимый диапазон `dimensionL` для temporal ease: **0..temporal_dim-1**.

## 6. Interpolation, ease, tangents и flags — разные слои поведения

Keyframe Suite5 предоставляет отдельные функции:

- `Get/SetKeyframeInterpolation` — in/out interpolation;
- `Get/SetKeyframeTemporalEase` — speed/influence по temporal dimension;
- `Get/SetKeyframeSpatialTangents` — spatial tangents;
- `Get/SetKeyframeFlags` — continuous/autobezier/roving flags;
- `Get/SetKeyframeLabelColorIndex` — label color utilities, добавленные в Suite5.

Это не одна «Bezier настройка». Например, spatial tangent имеет смысл только для подходящего spatial stream, а temporal ease индексируется по temporal dimensionality.

`AEGP_SetKeyframeFlag` устанавливает **один flag за вызов** через `(flag, true_falseB)`. Не передавайте произвольную комбинацию как будто это set-all-flags API.

`Easy_Cheese` демонстрирует изменение temporal ease и затем BEZIER interpolation. Это sample behavior, не доказательство, что BEZIER валиден для каждого stream.

## 7. Spatial tangents: values тоже нужно dispose

`AEGP_GetNewKeyframeSpatialTangents` может вернуть два `AEGP_StreamValue2`. Каждый реально полученный value подчиняется тому же cleanup contract через `AEGP_DisposeStreamValue`.

Не используйте spatial tangent API только потому, что value dimensionality > 1; сначала проверьте stream properties/type.

## 8. Batch insert: один transaction на серию ключей

Canonical [OneD recipe](code/KeyframeRecipes.cpp) takes borrowed stream and CompTime
arrays; [operation chain](../03-AEGP/02-PROJECT-RENDER-AUTOMATION.md) supplies caller
Undo/guard/lifetime. Validate arrays/count/time scales before batch: the helper
checks pointers/count/type, **not each time scale, numeric finiteness, sorting or
duplicate-time policy**. Count 0 still requires non-null arrays and enters batch.
Source disposes
each acquired value and ends batch after failed SetAddKeyframe. Interpolation/ease
are separate; separated follower must be resolved correctly before OneD operation.

Для серии keyframes используйте:

```text
AEGP_StartAddKeyframes
→ AEGP_AddKeyframes
→ AEGP_SetAddKeyframe
→ ...
→ AEGP_EndAddKeyframes(TRUE/FALSE)
```

Пример:

```cpp
AEGP_AddKeyframesInfoH addH = nullptr;
ERR(suites.KeyframeSuite5()->AEGP_StartAddKeyframes(
    streamH, &addH));

for (...) {
    A_long index = 0;
    ERR(suites.KeyframeSuite5()->AEGP_AddKeyframes(
        addH, AEGP_LTimeMode_CompTime, &times[i], &index));

    if (!err) {
        ERR(suites.KeyframeSuite5()->AEGP_SetAddKeyframe(
            addH, index, &values[i]));
    }
}

if (addH) {
    const A_Boolean commitB = err ? FALSE : TRUE;
    A_Err end_err = suites.KeyframeSuite5()->AEGP_EndAddKeyframes(
        commitB, addH);
    if (!err) err = end_err;
}
```

`EndAddKeyframes(FALSE, ...)` — explicit non-commit path batch API. Он не заменяет глобальную Undo-модель команды: если операция одновременно меняет другие части проекта, проектируйте общий undo scope отдельно.

The helper explicitly ends an acquired batch on ordinary returned SDK errors, not
on every C++ exception: an outer callback guard converts exceptions but does not
resume skipped value disposal or `EndAddKeyframes`. Use exception-safe owners when
extending this recipe. A failed End call is reported only when no earlier error
exists; separate diagnostics are needed to retain both failure details.

Существующий `Bible_AddOneDKeyframes` использует этот pattern и производит value через `AEGP_GetNewStreamValue`, а не вручную заполняет неизвестный union. Это defensive source pattern; Bible не заявляет runtime result для recipe.

## 9. Delete и mutation во время обхода

`AEGP_DeleteKeyframe` undoable и принимает текущий index. При массовом удалении безопаснее:

- сначала определить набор целей;
- удалять с конца к началу **или** заново получать count/time/index после structural mutation;
- не сохранять список индексов и затем менять начало массива ключей, ожидая, что остальные позиции останутся прежними.

Это рекомендация по positional index semantics, а не отдельная гарантия о внутренней реализации AE.

## 10. Separated dimensions — критическая ловушка

`AEGP_DynamicStreamSuite4` прямо предупреждает: когда leader property разделён на followers, простые value APIs могут работать через leader, но **keyframe-index APIs вроде `AEGP_GetNewKeyframeValue` на leader работать не будут**.

Правильный путь:

```text
IsSeparationLeader
→ AreDimensionsSeparated
→ GetSeparationFollower(dim)
→ keyframe API на конкретном follower
→ DisposeStream(follower)
```

Это особенно важно для Position и любых будущих separable properties. Не хардкодьте только текущий UI случай.

## 11. Expressions и keyframes существуют одновременно

Expression и keyframes — не взаимоисключающие состояния. Поэтому:

- `GetStreamNumKFs` отвечает про keys;
- `IsStreamTimevarying` учитывает expression;
- `GetNewStreamValue(pre_expressionB)` выбирает evaluation stage;
- keyframe value APIs работают с сохранёнными key values, а не с произвольным post-expression sample.

Если инструмент копирует анимацию, отдельно решите, копирует ли он keys, expression, оба слоя или только evaluated result.

## 12. Labels в Suite5

SDK 25.6 `AEGP_KeyframeSuite5` добавляет `GetKeyframeLabelColorIndex` и `SetKeyframeLabelColorIndex`. Это отдельная metadata operation; она не меняет interpolation или value.

Не требуйте Suite5, если ваш backward-compatible код реально использует только более старый subset. Но baseline Bible для SDK 25.6 должен описывать доступное current generation честно.

## 13. Official samples: полезны как паттерны, но они legacy-versioned

`Easy_Cheese.cpp` использует `StreamSuite2` и `KeyframeSuite3`, хотя тот же SDK 25.6 предоставляет `StreamSuite6` и `KeyframeSuite5`. Sample сохраняет ценность для:

- expression ownership;
- stream property inspection;
- keyframe value cleanup;
- ease/interpolation sequence;
- menu/hook workflow.

Но новый код не должен механически закрепляться на старой suite generation только потому, что sample исторический.

## 14. Product validation matrix

Если конкретный keyframer product заявляет runtime support, полезно проверить:

- 1D static → animated;
- existing key at same time;
- insert/delete multiple keys;
- linear/hold/bezier where valid;
- temporal ease per dimension;
- spatial tangent case;
- expression + keyframes;
- separated dimensions/followers;
- label color where supported;
- undo/redo;
- save/reopen;
- error injection + cleanup;
- repeated execution without leaked refs/values.

Эти проверки относятся к product runtime/support evidence. Для Bible chapter/source review остаётся SDK-CONTRACT-REVIEWED / RUNTIME-NOT-CLAIMED, если отдельного runtime record нет.

## 15. Recommended keyframer workflow

~~~text
resolve fresh stream
→ inspect type/dimensionality/separation state
→ normalize desired times/values as pure data
→ open semantic undo scope
→ choose single-key or batch API
→ write values/interpolation/ease/tangents/flags deliberately
→ close batch on every path
→ dispose every acquired StreamValue/StreamRef
→ return fresh keyframe summary
~~~

Keep computation of large key sets separate from host mutation. Background code can prepare pure times/values; host refs should be resolved and mutated only in the documented host-safe context.

## 16. Failure modes

Plan for:

- unsupported stream type;
- separated leader passed to index-based keyframe API;
- duplicate-time semantics;
- dimensionality mismatch;
- interpolation unsupported for target stream;
- batch start/add/set/end failure;
- expression policy conflict;
- project/property changed during async planning;
- cleanup error after primary mutation error.

Undo grouping does not make these failures transactional automatically.

## Related chapters

- [Streams/properties](05-STREAMS-PROPERTIES.md)
- [Lifetime/threading](14-LIFETIME-THREADING.md)
- [Keyframer integration](../14-NATIVE-INTEGRATIONS/06-KEYFRAMERS.md)
- [Keyframer batch template](../16-WORKING-TEMPLATES/keyframer-batch/README.md)

## Source record

Точные hashes, source ranges, sample-version discrepancies и recipe review: [Streams/keyframes SDK 25.6 review](../18-SDK-HEADER-TOOLS/10-STREAMS-KEYFRAMES-SDK25.6.md).
