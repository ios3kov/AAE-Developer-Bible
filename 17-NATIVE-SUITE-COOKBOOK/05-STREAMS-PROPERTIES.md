# Streams / properties / expressions

**Baseline source review:** Adobe After Effects SDK **25.6 build 61**.
**Suites in that SDK:** `AEGP_StreamSuite6`, `AEGP_DynamicStreamSuite4`.
**Verification level:** SDK-CONTRACT-REVIEWED / RUNTIME-NOT-CLAIMED. Исторический compiler result от 2026-09-30 не содержит exact tested source identity и не подтверждает компиляцию текущих recipes; границы — в [матрице evidence](VERIFICATION.md).

В AEGP значение, параметр эффекта, transform property, marker, mask outline и многие другие свойства представлены через **stream**. `AEGP_StreamRefH` — ссылка на host object; `AEGP_StreamValue2` — отдельное полученное значение со своим lifetime.

Главное правило этой главы: **stream ref, stream value, display name и match name — разные сущности с разными правилами владения и идентичности.**

## 1. Версия suite: не копировать номер из другой версии SDK

В присланном SDK 25.6 `AE_GeneralPlug.h` объявляет:

- `kAEGPStreamSuiteVersion6 = 11` и `AEGP_StreamSuite6`;
- `kAEGPDynamicStreamSuiteVersion4 = 5` и `AEGP_DynamicStreamSuite4`;
- `AEGP_SuiteHandler` умеет получать эти версии и одновременно сохраняет старые suite generations для legacy samples.

Поэтому пример для **25.6** должен компилироваться против `StreamSuite6()`/`DynamicStreamSuite4()`, если ему нужны функции именно этих поколений. Более поздний `StreamSuite7` относится к другой версии SDK и должен быть version-gated отдельно; он не является контрактом 25.6.

Суффикс C++-типа и числовая suite version — тоже разные вещи: `StreamSuite6` имеет version macro 11. Не выводите номер AcquireSuite из имени struct.

## 2. Сначала получить правильный stream и взять на себя его dispose

`AEGP_GetNewLayerStream`, `AEGP_GetNewEffectStreamByIndex`, `AEGP_GetNewMaskStream` и Dynamic Stream функции с `GetNew...StreamRef...` возвращают новый `AEGP_StreamRefH`, который caller обязан освободить через `AEGP_DisposeStream`.

Для обычного layer property:

```cpp
AEGP_StreamRefH streamH = nullptr;
A_Boolean legalB = FALSE;

ERR(suites.StreamSuite6()->AEGP_IsStreamLegal(
    layerH, AEGP_LayerStream_POSITION, &legalB));

if (!err && legalB) {
    ERR(suites.StreamSuite6()->AEGP_GetNewLayerStream(
        plugin_id, layerH, AEGP_LayerStream_POSITION, &streamH));
}

// use streamH

if (streamH) {
    ERR2(suites.StreamSuite6()->AEGP_DisposeStream(streamH));
}
```

`IsStreamLegal` проверяет применимость стандартного layer stream к конкретному layer. Это не универсальная проверка произвольного dynamic match name.

### Effect parameters

`AEGP_GetEffectNumParamStreams` возвращает число parameter streams эффекта. `AEGP_GetNewEffectStreamByIndex` принимает индекс в диапазоне `0..count-1`; **индекс 0 — input layer эффекта**. Это часть SDK-контракта 25.6 и причина не считать индекс 0 первым пользовательским slider.

Parameter index остаётся связанным с контрактом конкретного эффекта. Для внешней автоматизации match name эффекта + осмысленный parameter contract безопаснее, чем предположение, что одинаковые UI labels означают одинаковые индексы.

## 3. Тип значения нужно узнать до чтения union

`AEGP_StreamValue2` содержит union. До обращения к `value.val.one_d`, `two_d`, `color`, `markerP`, `mask` и т.д. получите `AEGP_StreamType`.

```cpp
AEGP_StreamType type = AEGP_StreamType_NO_DATA;
ERR(suites.StreamSuite6()->AEGP_GetStreamType(streamH, &type));
```

SDK 25.6 перечисляет отдельные типы для 1D/2D/3D/4D, spatial variants, color, arbitrary data, marker, layer/mask ID, mask outline и text document. Нельзя интерпретировать один union member как другой только потому, что память «похожа».

`AEGP_GetStreamProperties` отдельно возвращает flags и optional min/max. `HAS_MIN`, `HAS_MAX` и `IS_SPATIAL` — свойства stream, а не его текущего значения.

## 4. Read value: время и expression stage являются частью запроса

`AEGP_GetNewStreamValue` принимает:

- `AEGP_LTimeMode` — layer time или comp time;
- рациональный `A_Time`;
- `pre_expressionB`;
- output `AEGP_StreamValue2`, который потом **обязательно dispose**.

```cpp
A_Time t{0, 1};
AEGP_StreamValue2 value{};
A_Boolean have_valueB = FALSE;

ERR(suites.StreamSuite6()->AEGP_GetNewStreamValue(
    plugin_id,
    streamH,
    AEGP_LTimeMode_CompTime,
    &t,
    FALSE, // after expression
    &value));

if (!err) {
    have_valueB = TRUE;
    // read the union member selected by AEGP_GetStreamType()
}

if (have_valueB) {
    ERR2(suites.StreamSuite6()->AEGP_DisposeStreamValue(&value));
}
```

`pre_expressionB=TRUE` означает sample до expression; `FALSE` — после expression. Поэтому две выборки одного stream в одно время могут намеренно различаться.

`AEGP_IsStreamTimevarying` **учитывает expressions**. Ноль keyframes не означает автоматически constant output: `AEGP_GetStreamNumKFs` может вернуть 0, а expression всё равно сделать свойство time-varying.

### Primitive fast path

`AEGP_GetLayerStreamValue` работает только с primitive stream types. Header прямо исключает arbitrary block, marker и mask outline. Это не сокращённая замена `GetNewStreamValue` для всех типов.

## 5. SetStreamValue и keyframes — разные операции

В header 25.6 `AEGP_SetStreamValue` помечен как legal, когда `AEGP_GetStreamNumKFs == 0` или stream имеет `NO_DATA`. Для animated property используйте Keyframe Suite.

Существующий `Bible_SetStaticOneD` дополнительно проверяет `AEGP_IsStreamTimevarying`. Это **консервативнее** буквального header-критерия: expression без keyframes тоже делает stream time-varying и рецепт отказывается менять его статическим путем. Это защитное решение Cookbook, а не дополнительное правило SDK.

Перед записью:

1. проверьте `AEGP_StreamType`;
2. решите, допустима ли статическая запись или нужен keyframe;
3. получите корректно типизированный `AEGP_StreamValue2`;
4. меняйте только соответствующий union member;
5. сохраните ошибку основной операции отдельно от cleanup;
6. dispose полученного value.

## 6. Expressions: текст и enabled state имеют отдельный lifetime

`AEGP_GetExpressionState`/`AEGP_SetExpressionState` управляют enabled state. Header отмечает, что expression может быть автоматически disabled parser-ом при playback; одно значение флага нельзя трактовать как вечную user preference.

`AEGP_GetExpression` возвращает `AEGP_MemHandle` с Unicode expression text. Его освобождают через `AEGP_FreeMemHandle`, а не `AEGP_DisposeStreamValue`.

`AEGP_SetExpression` принимает UTF-16 строку и **не принимает владение** ей.

Официальный `Easy_Cheese` показывает старое поколение Stream Suite и освобождает полученный expression memory handle. Паттерн ownership полезен, но имена старых suite типов нельзя копировать как актуальную версию 25.6.

## 7. Dynamic streams: hierarchy, match names и structural edits

`AEGP_DynamicStreamSuite4` различает:

- `LEAF`;
- `NAMED_GROUP`;
- `INDEXED_GROUP`.

Базовый обход:

```text
GetNewStreamRefForLayer
→ GetStreamGroupingType
→ GetNumStreamsInGroup
→ GetNewStreamRefByIndex / GetNewStreamRefByMatchname
→ read/copy needed metadata
→ DisposeStream for every acquired ref
```

`GetNewStreamRefByMatchname`, `CanAddStream`, `AddStream` и `GetMatchName` используют **UTF-8 match names**. `SetStreamName` использует UTF-16 display name. Это ещё одна причина не путать programmatic identity с локализованной UI строкой.

Structural functions имеют важные контракты:

- `AEGP_DeleteStream` — undoable, только child `INDEXED_GROUP`; **после удаления stream ref всё равно нужно dispose**;
- `AEGP_ReorderStream` — undoable и обновляет переданный ref так, чтобы он ссылался на перемещённый stream;
- `AEGP_DuplicateStream` возвращает новый index, не новый ref;
- `AEGP_AddStream` возвращает новый ref, который caller должен dispose;
- `AEGP_SetDynamicStreamFlag(..., undoableB=false, ...)` разрешает в таком режиме только `HIDDEN`.

Официальный `Streamie` полезен как пример обхода и cleanup, но он использует старые `StreamSuite2`/`DynamicStreamSuite2`. В частности, его старый `GetStreamName` API нельзя механически переносить на `StreamSuite6`, где имя возвращается как UTF-16 memory handle.

## 8. Separated dimensions: value API и keyframe API ведут себя по-разному

Dynamic Stream Suite вводит leader/follower model для разделяемых многомерных свойств.

Header 25.6 прямо говорит:

- простые `GetNewStreamValue`, `SetStreamValue`, `GetLayerStreamValue` могут работать через leader и автоматически распространяться на followers;
- **keyframe-index APIs на separated leader не работают** — нужно получить конкретные followers через `AEGP_GetSeparationFollower` и работать с ними.

Не хардкодьте предположение «разделяется только Position»: комментарий SDK специально предупреждает не писать код с такой зависимостью.

## 9. Идентичность: index, name, match name, unique stream ID

`AEGP_StreamSuite6` добавляет `AEGP_GetUniqueStreamID`. Это полезная runtime identity, но рассмотренные declarations не дают универсальной гарантии сохранения ID между закрытием/повторным открытием проекта, импортом, merge и всеми structural edits.

Практический порядок для automation:

```text
известный layer/effect context
→ match name / documented stream kind
→ получить свежий StreamRefH
→ проверить grouping/type
→ выполнить операцию
→ dispose ref
```

Не храните `AEGP_StreamRefH` как долговременный ID.

## 10. Ошибки и cleanup

Стандартный шаблон:

```text
основная операция
→ сохранить primary error
→ освободить все полученные StreamValue / StreamRef / MemHandle
→ cleanup error поднимается только если primary error отсутствовал
```

Это особенно важно в рекурсивном dynamic traversal и при чтении complex stream values.

## 11. Product validation guidance

Если конкретный product заявляет runtime support для этих операций, полезно проверить:

- static property без expression;
- property с keyframes;
- expression pre/post evaluation;
- effect parameter index 0 и пользовательские параметры;
- localized display name против match name;
- dynamic indexed-group add/reorder/duplicate/delete;
- separated dimensions;
- marker/text/mask ownership;
- save/reopen и повторное разрешение property;
- error cleanup и отсутствие leaked refs/values.

Source review подтверждает API-контракт. Bible не заявляет собственный host-observed результат для cookbook recipe; product runtime evidence добавляется только там, где продукт делает соответствующий support claim.

## 12. Recommended operation workflow

For a stream/property mutation:

~~~text
resolve fresh layer/effect/property context
→ obtain owned StreamRefH
→ inspect grouping/type/dimensionality
→ decide static value vs keyframe path
→ choose pre/post-expression semantics
→ perform mutation in host-safe/undo context
→ dispose StreamValue/MemHandle/StreamRef with their own APIs
→ re-query after structural edits
~~~

For long-lived UI/application state, store stable product identity and re-resolve the stream at command time rather than caching `AEGP_StreamRefH`.

## 13. Failure modes

Handle explicitly:

- property/effect disappeared;
- stream type differs from expectation;
- dynamic hierarchy changed;
- expression makes static-write policy invalid;
- separated-dimension leader requires follower resolution;
- structural mutation invalidated refs/indices;
- value acquisition succeeded but later mutation failed;
- cleanup/dispose returned an error.

Do not collapse all failures into “property not found”.

## Related chapters

- [Effects](04-EFFECTS.md)
- [Keyframes](06-KEYFRAMES.md)
- [Lifetime/threading](14-LIFETIME-THREADING.md)
- [Keyframer integration](../14-NATIVE-INTEGRATIONS/06-KEYFRAMERS.md)

## Source record

Точные line ranges, hashes и найденные расхождения для SDK 25.6: [Streams/keyframes source review](../18-SDK-HEADER-TOOLS/10-STREAMS-KEYFRAMES-SDK25.6.md).
