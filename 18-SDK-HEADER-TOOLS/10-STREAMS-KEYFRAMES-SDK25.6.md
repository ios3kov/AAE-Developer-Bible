# SDK 25.6: AEGP streams, properties и keyframes

Дата: **2026-10-01**. Источник — присланная пользователем поставка `ae25.6_61.64bit.AfterEffectsSDK`, build 61.

**Результат:** переписаны главы Cookbook про streams/properties и keyframes по фактическим declarations SDK 25.6 и двум Adobe samples. Это source review и документация; новый native binary и host test не выполнялись.

## Место в плане

Итерация продолжает содержательную сверку Библии с SDK в рамках этапов 3–4 `COMPLETION-PLAN.md`. Она не закрывает Gate 3A, exact-SDK compiler gate, AEGP keyframer host acceptance или общие Gates 5–7.

Обновлены:

- `17-NATIVE-SUITE-COOKBOOK/05-STREAMS-PROPERTIES.md`;
- `17-NATIVE-SUITE-COOKBOOK/06-KEYFRAMES.md`;
- маршрут чтения AEGP, STATUS и VERIFICATION.

Исходные recipe `.cpp` не менялись в этой итерации: их contracts и ограничения только сопоставлены с текущим header.

## Идентичность источника

SHA-256 принятого TAR: `eee39a787ab09226a5a08c27496335faf79cbe52dd96f19cf795e48af09e2df6`.

Рассмотренные SDK-файлы:

| Файл | SHA-256 | Основные диапазоны |
|---|---|---|
| `Examples/Headers/AE_GeneralPlug.h` | `30d12ec3eb5af1a902c7414053b1be1da0204b226e0b1cdc71272be1e137000c` | 1367–1585 Stream types/Suite6; 1599–1790 DynamicStreamSuite4; 1812–1947 KeyframeSuite5 |
| `Examples/Util/AEGP_SuiteHandler.h` | `2eeec0827ca13f039eb87c961c8c41e77f046379457930d4bb2700c756b40b13` | 99–124 suite members; 268–305 acquire/release support |
| `Examples/Util/AEGP_SuiteHandler.cpp` | `7c054c7b0778b1b26463d6bf31cd57ee1d971946e8da22fb174e9f088741606f` | suite-handler lifetime implementation |
| `Examples/AEGP/Easy_Cheese/Easy_Cheese.cpp` | `8f24fcd95201bfc8e7f8dbd66b984891d8720dc34c72f97b0c63dccc0bd33d18` | 173–201 expressions; 203–234 stream info; 237–329 keyframe value/ease |
| `Examples/AEGP/Easy_Cheese/Easy_Cheese.h` | `ffc98712a41962869fae12c473df3fff7cd86d0f7116b7f906e15e10cdd1ab72` | sample declarations/context |
| `Examples/AEGP/Streamie/Streamie.cpp` | `e1c6359bba00d39dea5137de5f2ecce1fb74da1fcf50e5443047a70a40911bce` | 43–116 discovery/cleanup; 119–190 structural stream edits |
| `Examples/AEGP/Streamie/Streamie.h` | `adab44dbd4975cf5620a3aded2b4ad38bfb5dae357ea22908f9ce10c89641255` | sample declarations/context |

Reviewed Bible recipe blobs at the start of this iteration:

- `EffectStreamRecipes.cpp`: `8b473f10c872aec992eb728c91444b629041c0a1`;
- `KeyframeRecipes.cpp`: `19d798ddd0aba617cf98a41ebd6271ddd1315624`.

## Главное версионное исправление

Старый Cookbook был смешан с более поздним snapshot:

- Streams chapter называл `AEGP_StreamSuite7` и упоминал AE 26.5 как текущий API;
- Keyframes chapter говорил `AEGP_KeyframeSuite3+` и показывал Suite3 calls.

В **поставленном SDK 25.6** current declarations и SuiteHandler дают:

| Family | C++ type | suite version macro value |
|---|---|---:|
| Stream | `AEGP_StreamSuite6` | `kAEGPStreamSuiteVersion6 = 11` |
| Dynamic Stream | `AEGP_DynamicStreamSuite4` | `kAEGPDynamicStreamSuiteVersion4 = 5` |
| Keyframe | `AEGP_KeyframeSuite5` | `kAEGPKeyframeSuiteVersion5 = 5` |

Это ещё раз показывает, что суффикс struct не обязательно равен числовой версии `AcquireSuite`. Главы переписаны на baseline 25.6. Более поздние API notes должны быть явно version-gated, а не подменять baseline.

## Streams: подтверждённые contracts

### Ownership

`GetNewLayerStream`, `GetNewEffectStreamByIndex`, `GetNewMaskStream`, `GetNewStreamRefForLayer/Mask`, `GetNewStreamRefByIndex/Matchname`, `GetNewParentStreamRef` и `AddStream` возвращают refs, которые caller должен dispose через `AEGP_DisposeStream`.

`GetNewStreamValue` возвращает `AEGP_StreamValue2`, который caller должен передать `AEGP_DisposeStreamValue`. `GetStreamName` и `GetExpression` возвращают `AEGP_MemHandle`, освобождаемый Memory Suite.

Это три разных cleanup family; взаимозаменять их нельзя.

### Type and value

`AEGP_StreamValue2` — union. `AEGP_GetStreamType` определяет допустимый member. Stream flags отдельно описывают HAS_MIN/HAS_MAX/IS_SPATIAL.

`GetNewStreamValue` включает `AEGP_LTimeMode`, `A_Time` и `pre_expressionB`. `IsStreamTimevarying` прямо помечен как учитывающий expressions.

`SetStreamValue` header-комментарием ограничен streams без keyframes (`GetStreamNumKFs==0`) или NO_DATA. Существующий `Bible_SetStaticOneD` дополнительно блокирует expression-driven time varying stream через `IsStreamTimevarying`; это консервативное решение recipe, а не более широкий SDK запрет.

### Effect parameter index 0

`GetNewEffectStreamByIndex` документирует индекс 0 как input layer эффекта. Поэтому parameter numbering внешней автоматизации не начинается автоматически с первого пользовательского slider.

### Dynamic hierarchy and strings

`DynamicStreamSuite4` различает LEAF/NAMED_GROUP/INDEXED_GROUP. Match-name APIs принимают UTF-8, а `SetStreamName` — UTF-16 display name.

`DeleteStream` требует затем всё равно dispose ref; `ReorderStream` обновляет ref на перемещённый stream. `AddStream` возвращает новый owned ref.

### Separated dimensions

Header отдельно разрешает простым value APIs работать через leader, но запрещает keyframe-index APIs на separated leader: для keyframes нужно получить follower.

## Keyframes: подтверждённые contracts

`GetStreamNumKFs` возвращает `AEGP_NumKF_NO_DATA=-1` для NO_DATA и 0 при отсутствии keys, причём header отдельно напоминает, что expression всё ещё может существовать.

`InsertKeyframe` не создаёт duplicate key, если key уже есть в указанное время; stream остаётся unchanged и возвращается index.

`GetNewKeyframeValue` и `GetNewKeyframeSpatialTangents` возвращают stream values, которые должны быть disposed через Stream Suite. Set-функции не принимают ownership.

`GetStreamValueDimensionality` и `GetStreamTemporalDimensionality` — разные вопросы. Temporal ease принимает dimension в диапазоне `0..temporal_dim-1`.

`SetKeyframeFlag` меняет один flag за вызов. Interpolation, temporal ease, spatial tangents, flags и label color — разные операции.

`StartAddKeyframes`/`AddKeyframes`/`SetAddKeyframe`/`EndAddKeyframes` образуют batch transaction. Suite5 добавляет keyframe label color utilities.

## Samples: что переносить, а что нет

### Easy Cheese

Sample SDK 25.6 использует старые `StreamSuite2` и `KeyframeSuite3`. Из него полезны patterns:

- expression MemHandle освобождается Memory Suite;
- keyframe value освобождается Stream Suite;
- stream properties/time-varying/dimensionality проверяются отдельно;
- temporal ease и interpolation — отдельные calls.

Но старую suite generation нельзя считать текущей только потому, что sample компилировался исторически.

### Streamie

Streamie использует `DynamicStreamSuite2`/`StreamSuite2`. Он показывает получение group refs, quiet-errors around expected lookup failures, structural operations и cleanup refs.

Особенно важно: старый sample читает stream name в character buffer. В current `StreamSuite6` `AEGP_GetStreamName` возвращает UTF-16 `AEGP_MemHandle`. Поэтому прямое копирование строки sample в новый Suite6 code неверно.

## Найденные границы и расхождения

1. **Later-SDK leakage в Cookbook:** StreamSuite7 был указан как baseline, хотя supplied 25.6 его не содержит. Исправлено в документации.
2. **Legacy sample generations:** Easy Cheese/Streamie остаются в поставке и используют старые suites. Они являются pattern evidence, не current-signature evidence.
3. **Keyframes + expression:** `0` keyframes не гарантирует constant property.
4. **Separated dimensions:** value APIs и keyframe-index APIs имеют разный контракт на leader property.
5. **UniqueStreamID:** Suite6 возвращает runtime identifier, но reviewed declaration не обещает вечную стабильность после save/reopen/import/merge. Глава не превращает его в persistent database key.

## Recipe review

`EffectStreamRecipes.cpp` использует `StreamSuite6` и корректно dispose-ит effect ref/stream value. Его `Bible_SetStaticOneD` консервативно отказывается от expression-driven time varying stream. Host behavior не повторялся.

`KeyframeRecipes.cpp` использует `KeyframeSuite5`, batch add transaction и `DisposeStreamValue`. Он не содержит special handling separated leader/follower; caller должен передавать stream, на котором keyframe-index API legal. Это теперь явно задокументировано.

Исходный code не редактировался в этой итерации; отсутствие code diff не означает host acceptance.

## Проверка этой итерации

| Проверка | Статус |
|---|---|
| Source TAR identity | hash совпадает с ранее принятой поставкой |
| Header/sample review | выполнен для перечисленных файлов |
| Cookbook documentation version correction | выполнено |
| New exact-SDK compilation | NOT RUN |
| AEGP host keyframe/stream execution | NOT RUN |
| Save/reopen, separated dimensions, expression/key interaction | NOT RUN |
| Windows host verification | NOT RUN |

GitHub Validate проверяет итоговый committed documentation tree отдельно. Его green status не является host evidence.

## Следующий редакционный блок

После streams/keyframes логично сверить masks, text/markers и footage/import ownership, после чего вернуться к обязательным plan gates: reuse audit, exact compiler и host-verified reference examples.