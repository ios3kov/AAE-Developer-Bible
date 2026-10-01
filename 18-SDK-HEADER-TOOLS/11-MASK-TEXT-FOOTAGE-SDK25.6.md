# SDK 25.6: masks, text/markers и footage/import ownership

Дата: **2026-10-01**. Источник — присланный Adobe After Effects SDK **25.6 build 61**.

**Результат:** переписаны Cookbook chapters 07–09 по current declarations supplied SDK. Это документация/source review; host mutation, import/render и leak tests не выполнялись.

## Место в плане

Работа продолжает editorial/source-contract review текущей редакции Bible. Она фиксирует exact SDK contracts и source findings; compiler/host evidence конкретных products остаётся отдельным evidence class.

Обновлены:

- `17-NATIVE-SUITE-COOKBOOK/07-MASKS.md`;
- `17-NATIVE-SUITE-COOKBOOK/08-TEXT-MARKERS.md`;
- `17-NATIVE-SUITE-COOKBOOK/09-FOOTAGE-IMPORT.md`.

## Идентичность

SHA-256 принятого SDK TAR: `eee39a787ab09226a5a08c27496335faf79cbe52dd96f19cf795e48af09e2df6`.

| Файл | SHA-256 | Рассмотренные области |
|---|---|---|
| `Examples/Headers/AE_GeneralPlug.h` | `30d12ec3eb5af1a902c7414053b1be1da0204b226e0b1cdc71272be1e137000c` | 1951–2073 text/marker; 2268–2445 mask/outline; 2487–2666 footage |
| `Examples/Util/AEGP_SuiteHandler.h` | `2eeec0827ca13f039eb87c961c8c41e77f046379457930d4bb2700c756b40b13` | current suite generations/accessors |
| `Examples/AEGP/Text_Twiddler/Text_Twiddler.cpp` | `405308bf437fbd5a417c82d796d6aef068296f5bd7bd34ab8bae741e0db3fcfd` | 45–100 Source Text pattern |
| `Examples/AEGP/Mangler/Mangler.cpp` | `e919e89f6ea3fc3106e8ea60d7bd084dbc5a411c5bd433ecc1a19eb7d063a741` | 71–130 marker construction; mask/keyframe operations elsewhere |
| `Examples/AEGP/Projector/Projector.cpp` | `f7db7a6a1cb0e3d1cac7e6ae4e5478601c009d0e6ef9782dc52f7ad6c24ef127` | 349–430 footage; 583–657 mask outline |
| `Examples/AEGP/ProjDumper/ProjDumper.cpp` | `99913472c3a0161fe18590e8247beb5b647e692c2a2823bc92e8821c663f9fd8` | 318–330 footage read/path cleanup; 487–540 import/proxy |

## Suite generations в 25.6

| Family | Current C++ type | Version macro value |
|---|---|---:|
| Mask | `AEGP_MaskSuite6` | 7 |
| Mask outline | `AEGP_MaskOutlineSuite3` | 5 |
| Text document | `AEGP_TextDocumentSuite1` | 1 |
| Marker | `AEGP_MarkerSuite3` | 3 |
| Footage | `AEGP_FootageSuite5` | 11 |
| Item | `AEGP_ItemSuite9` | 14 |
| Comp | `AEGP_CompSuite12` | 26 |
| Layer | `AEGP_LayerSuite9` | 15 |

Предыдущая footage chapter содержала `CompSuite13` и ориентировалась на 26.5. Для supplied SDK 25.6 это не current declaration; baseline исправлен на `CompSuite12`.

## Masks — подтверждённые contracts

`GetLayerMaskByIndex` возвращает MaskRefH, который caller должен DisposeMask. `DeleteMaskFromLayer` отдельно говорит, что после удаления ref **всё равно нужно dispose**.

Mask metadata (invert/mode/motion blur/feather falloff/color/lock/RotoBezier/ID) отделена от animatable mask streams. Старые mask name functions obsoleted; header направляет к Dynamic Stream naming.

Outline приходит как stream value типа MASK. `MaskOutlineSuite3` работает с open state, segments, vertices и variable feather points. Для closed outline `vertex[0] == vertex[num_segments]`; tangents relative to position; setting vertex 0 имеет special last-vertex tangent behavior.

`CreateVertex` сдвигает последующие indices. Поэтому stored vertex/feather indices нужно revalidate после structural edits.

### Projector ownership finding

Projector sample создаёт `new_maskH` через старый `MaskSuite4`, редактирует outline и dispose-ит stream value, но в просмотренной функции **не вызывает `AEGP_DisposeMask(new_maskH)`**. Current header задаёт явный MaskRef disposal contract.

Это не доказанная runtime leak measurement; это source-level reason не использовать sample как ownership gold standard.

## Text — подтверждённые contracts

`TextDocumentSuite1::AEGP_GetNewText` возвращает UTF-16 `AEGP_MemHandle`, который должен освобождаться Memory Suite. `AEGP_SetText` принимает число characters, а не byte count.

Text document handle обычно приходит внутри `AEGP_StreamValue2`; его lifetime не следует расширять за disposal stream value.

Text_Twiddler использует старый StreamSuite2, но полезно демонстрирует type check, UTF-16 length, SetText → SetStreamValue и cleanup value/ref. Для animated Source Text static SetStreamValue не является универсальным path; нужен Keyframe Suite.

## Markers — подтверждённые contracts

`MarkerSuite3` имеет explicit `NewMarker`, `DisposeMarker`, `DuplicateMarker`, string fields, cue-point params, flags, duration и label.

`GetMarkerString` и `GetIndCuePointParam` возвращают MemorySuite handles; latter может вернуть key+value handles одновременно.

`InsertCuePointParam` только резервирует slot; content задаётся последующим `SetIndCuePointParam`.

Marker timing принадлежит keyframe stream, marker payload — marker value. Для existing keyframe safest documented ownership path — GetNewKeyframeValue → mutate markerP → SetKeyframeValue → DisposeStreamValue.

### Mangler ownership nuance

Mangler sample создаёт marker через старый MarkerSuite1, подставляет pointer в StreamValue2 и затем dispose-ит StreamValue wrapper без отдельного DisposeMarker в этой функции. Header не содержит достаточной фразы, чтобы превратить этот sample-specific pattern в универсальное adoption правило для всех самостоятельно созданных marker pointers.

Поэтому chapter разделяет standalone New/DisposeMarker ownership и StreamValue ownership и предупреждает против double cleanup.

## Footage — подтверждённые contracts

`AEGP_NewFootage` возвращает caller-owned FootageH **до** disposal или adoption project-ом.

Adoption functions:

- `AEGP_AddFootageToProject`;
- `AEGP_SetItemProxyFootage`;
- `AEGP_ReplaceItemMainFootage`.

После successful adoption `AEGP_DisposeFootage` вызывать нельзя. Если adoption failed, caller остаётся владельцем и обязан иметь cleanup path.

`GetMainFootageFromItem`/`GetProxyFootageFromItem` возвращают project-owned footage; это не detached resources для DisposeFootage.

`GetFootagePath` возвращает UTF-16 MemHandle, который нужно FreeMemHandle. ProjDumper это показывает.

`GetFootageNumFiles` возвращает main-file count и files-per-frame (main включён). Это inventory multi-file footage, но не доказательство semantic auxiliary channel types.

`AEGP_FileSequenceImportOptions` задаёт still/sequence, alphabetical order и start/end frames; `AEGP_ANY_FRAME=-1` означает auto earliest/latest.

`AEGP_InterpretationStyle` — enum 0/1/2. Projector/ProjDumper historical code передаёт `FALSE`; это численно работает как `NO_DIALOG_GUESS=0`, но новый code должен использовать named enum.

`AEGP_FootageInterp` включает field/alpha/pulldown/loop/pixel aspect/native+conform FPS/depth/motion detection. Interpretation mutation — отдельная undoable operation.

Placeholder-with-path contract отдельно предупреждает: `AEIO_FileType_ANY` требует существующий path; `AEIO_FileType_NONE` — warning condition.

### Adobe sample rollback finding

В reviewed import samples есть straightforward successful paths NewFootage → adoption, но не каждый error branch после successful NewFootage показывает DisposeFootage rollback. Поэтому sample call order не является complete RAII/error-cleanup proof.

## Что исправлено в Bible

1. `StreamSuite7` в masks/text baseline заменён на supplied 25.6 `StreamSuite6`.
2. Footage chapter baseline suite list исправлен с later `CompSuite13` на 25.6 `CompSuite12`.
3. Mask deletion теперь явно отделена от MaskRef disposal.
4. Text UTF-16 MemHandle lifetime и character count записаны явно.
5. Marker stream/value ownership отделён от standalone marker allocation.
6. Footage ownership теперь описывает pre-adoption/post-adoption transition и failure cleanup.
7. Historical samples помечены как pattern evidence, а не current-suite or production-ownership proof.

## Проверка этой итерации

| Проверка | Статус |
|---|---|
| SDK TAR identity | hash совпадает с принятой поставкой |
| Header/sample review | выполнен по перечисленным files/ranges |
| Documentation correction | выполнена |
| Exact-SDK compile новых snippets | NOT RUN |
| Mask/text/marker host mutation | NOT RUN |
| Real footage import/proxy/relink | NOT RUN |
| Leak diagnostics / failure rollback | NOT RUN |
| Windows host checks | NOT RUN |

Следующий editorial block после этого может охватить AEIO/Artisan или оставшиеся Cookbook families; editorial readiness определяется полнотой и согласованностью документации.

## Later cookbook consistency update — 2026-10-01

A later editorial block completed the production-guidance layer around the already-reviewed SDK 25.6 contracts.

The exact suite baseline did **not** change:

- `AEGP_MaskSuite6`;
- `AEGP_MaskOutlineSuite3`;
- `AEGP_TextDocumentSuite1`;
- `AEGP_MarkerSuite3`;
- `AEGP_FootageSuite5`;
- `AEGP_ItemSuite9`;
- `AEGP_CompSuite12`;
- `AEGP_LayerSuite9`.

The later pass added/reconciled:

- mask create/edit/dispose workflow, structural invalidation, vertex/feather-index hazards and anti-patterns;
- text Source Text workflow, UTF-16 MemorySuite lifetime and static-vs-keyframed write path;
- marker keyframe/value workflow versus standalone `NewMarker` ownership;
- footage explicit `OwnedByPlugin → AdoptedByProject` transition and failure rollback;
- footage interpretation as a separate undoable mutation rather than an implicit side effect of import;
- Footage Suite versus AEIO boundary for host-supported media versus new file formats;
- product-validation guidance replacing old “host acceptance pending” wording.

The original source hashes/findings above remain provenance for the SDK review and are not rewritten retroactively.

**Evidence level after this pass:** SDK-CONTRACT-REVIEWED / RUNTIME-NOT-CLAIMED. No new AE runtime result is asserted.
