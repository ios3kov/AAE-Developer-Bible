# Text documents and markers

**Baseline source review:** Adobe After Effects SDK **25.6 build 61**.
**Suites in that SDK:** `AEGP_TextDocumentSuite1`, `AEGP_MarkerSuite3`, `AEGP_StreamSuite6`, `AEGP_KeyframeSuite5`.
**Verification level:** SDK source-reviewed; no new AE host mutation test in this editorial iteration.

Text и marker в AEGP связаны со streams, но их payload lifetimes разные. Text Document хранится в special stream value; marker — payload keyframe в marker stream.

## 1. Text Document — специальный stream value

Получите Source Text stream, проверьте тип `AEGP_StreamType_TEXT_DOCUMENT`, затем получите `AEGP_StreamValue2`.

```text
Text LayerH
→ GetNewLayerStream(SOURCE_TEXT)
→ GetStreamType == TEXT_DOCUMENT
→ GetNewStreamValue
→ value.val.text_documentH
→ TextDocumentSuite1
→ SetStreamValue / KeyframeSuite as appropriate
→ DisposeStreamValue
→ DisposeStream
```

`AEGP_TextDocumentH`, полученный через stream value, нельзя сохранять дольше lifetime самого `AEGP_StreamValue2` без отдельного документированного ownership contract.

## 2. Читать text: GetNewText возвращает MemorySuite handle

`AEGP_TextDocumentSuite1::AEGP_GetNewText` возвращает `AEGP_MemHandle` с null-terminated UTF-16 (`A_u_short`). Его освобождают через `AEGP_FreeMemHandle`.

```text
GetNewText(plugin_id, text_documentH, &unicodeH)
→ lock/read memory handle по MemorySuite contract
→ unlock
→ FreeMemHandle
```

Это не `DisposeStreamValue`: text memory handle и stream value — два разных resources.

## 3. SetText принимает character count, не byte count

`AEGP_SetText(text_documentH, unicodePS, lengthL)` получает `lengthL` как число characters. Для UTF-16 нельзя подставлять `strlen()` UTF-8 или `sizeof(buffer)` в байтах без пересчёта.

```cpp
const A_u_short text[] = {0x0042, 0x0042, 0x0042};
A_long length = static_cast<A_long>(sizeof(text) / sizeof(text[0]));
ERR(suites.TextDocumentSuite1()->AEGP_SetText(
    value.val.text_documentH, text, length));
```

## 4. Static Source Text и animated Source Text — разные операции

После изменения `text_documentH` значение нужно применить к stream.

Если Source Text не имеет keyframes и static-write contract допустим — `SetStreamValue`. Если текст keyframed, используйте Keyframe Suite и меняйте нужный keyframe value.

Не пытайтесь «починить» animated text вызовом `SetStreamValue`: current Stream Suite ограничивает этот API streams без keyframes/NO_DATA.

## 5. Text_Twiddler — pattern evidence, не current suite signature

Supplied `Text_Twiddler.cpp` использует `StreamSuite2`, получает `SOURCE_TEXT`, проверяет `TEXT_DOCUMENT`, изменяет document через `TextDocumentSuite1`, записывает stream value и затем dispose-ит value/refs.

Полезны:

- type check;
- UTF-16 character count;
- stream-value cleanup;
- Undo grouping.

Но новый 25.6 code должен брать current `StreamSuite6`; старый sample не определяет актуальную suite generation.

---

# Markers

## 6. Marker — value в marker stream на keyframe time

Модель:

```text
Layer/Comp marker stream
→ Keyframe count/time
→ GetNewKeyframeValue
→ value.val.markerP
→ MarkerSuite3 read/write payload
→ SetKeyframeValue
→ DisposeStreamValue
```

Marker не является отдельным «timeline object handle» с независимым временем: timing приходит из keyframe stream, payload — из Marker Suite.

## 7. MarkerSuite3 payload

Current suite поддерживает:

- marker strings: comment, chapter, URL, frame target, cue point name;
- navigation/protect-region flags;
- cue-point key/value parameters;
- duration;
- label index;
- New/Dispose/Duplicate Marker.

`AEGP_GetMarkerString` возвращает UTF-16 `AEGP_MemHandle`, который нужно `AEGP_FreeMemHandle`. `AEGP_GetIndCuePointParam` может вернуть **два** handles — key и value; оба требуют cleanup.

## 8. Cue point parameters: Insert только резервирует slot

Header прямо говорит, что `AEGP_InsertCuePointParam` **только резервирует место**. После него нужен `AEGP_SetIndCuePointParam` для записи key/value.

Индексы должны быть:

- get/set/delete: `0..count-1`;
- insert: `0..count`.

При удалении нескольких cue params учитывайте сдвиг positional indices.

## 9. Предпочтительный marker-edit pattern

Для уже существующего marker key безопаснее работать через typed keyframe value:

```text
Insert/find keyframe
→ GetNewKeyframeValue
→ убедиться, что markerP получен
→ MarkerSuite3 SetMarkerString/Flag/Duration/Label
→ SetKeyframeValue
→ DisposeStreamValue
```

Так ownership всего complex payload остаётся связан с `AEGP_StreamValue2`, полученным у host.

## 10. Standalone NewMarker требует отдельной ownership дисциплины

`AEGP_MarkerSuite3` имеет явную пару `AEGP_NewMarker` / `AEGP_DisposeMarker` и `AEGP_DuplicateMarker`.

Если marker создан как standalone value и **не передан в ownership container**, caller должен иметь явный cleanup path. Не добавляйте одновременно `DisposeMarker` и `DisposeStreamValue` к одному pointer без понимания того, кто в конкретном workflow владеет payload — иначе можно получить double cleanup.

В reviewed `Mangler` sample marker создаётся через старый `MarkerSuite1`, pointer подставляется в `AEGP_StreamValue2`, затем wrapper освобождается `DisposeStreamValue`; отдельного `DisposeMarker` в этой функции нет. Это sample-specific pattern, а не самостоятельное доказательство универсального adoption rule.

Для нового кода Cookbook предпочитает получение marker payload через `GetNewKeyframeValue`, когда это возможно.

## 11. Duration, protect region и label

`Set/GetMarkerDuration` работают с `A_Time`. Protect Region — marker flag, не отдельный stream type. `Set/GetMarkerLabel` меняют label metadata.

Не смешивайте marker duration с длиной keyframe interval: keyframe задаёт anchor time, duration — часть marker payload.

## 12. Host acceptance matrix

Text:

- static Source Text;
- keyframed Source Text;
- Unicode non-ASCII;
- empty string;
- expression + Source Text;
- undo/redo;
- save/reopen.

Markers:

- layer and comp marker streams;
- create/read/update/delete;
- comment/chapter/URL/cue name;
- multiple cue params;
- duration;
- protect-region flag;
- label;
- duplicate marker;
- repeated batch edits + cleanup.

До этих тестов документация source-reviewed, но не host-verified.

## Source record

Точные hashes и sample limits: [Masks/text/footage SDK 25.6 review](../18-SDK-HEADER-TOOLS/11-MASK-TEXT-FOOTAGE-SDK25.6.md).