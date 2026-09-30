# Text + marker recipes

## Text

**Suites:** `AEGP_StreamSuite7`, `AEGP_TextDocumentSuite1`  
**Confidence:** SDK-verified.

Text document — значение специального stream.

Pipeline:

```text
Text LayerH
→ layer TEXT_DOCUMENT stream
→ GetNewStreamValue
→ TextDocumentH
→ TextDocumentSuite GetNewText / SetText
→ DisposeStreamValue
→ DisposeStream
```

### Получить текст

`AEGP_TextDocumentSuite1::AEGP_GetNewText` возвращает host memory handle с Unicode text.

```text
Get text document handle from stream value
→ AEGP_GetNewText(plugin_id, text_docH, &unicode_memH)
→ lock/read
→ unlock
→ AEGP_FreeMemHandle
```

### Задать текст

```cpp
ERR(suites.TextDocumentSuite1()->AEGP_SetText(
    text_docH,
    reinterpret_cast<const A_u_short*>(utf16_text),
    utf16_length));
```

Не передавать `strlen()` UTF-8 как UTF-16 length.

---

## Markers

**Suites:** `AEGP_MarkerSuite2`, `AEGP_StreamSuite`, `AEGP_KeyframeSuite`  
**Confidence:** SDK-verified.

Marker stream — time-varying stream. Времена marker'ов — keyframe mechanics, marker payload — Marker Suite.

Pipeline:

```text
layer/comp marker StreamRefH
→ GetStreamNumKFs
→ GetKeyframeTime
→ GetNewKeyframeValue
→ MarkerValP
→ MarkerSuite read/write strings, duration, flags
```

### Создать marker value

```text
MarkerSuite.NewMarker
→ set comment/chapter/url/cue strings as needed
→ set duration
→ write into marker stream keyframe
→ MarkerSuite.DisposeMarker
```

Следить за ownership marker object отдельно от stream value.

---

## Правильная модель

Marker — не «отдельный объект на timeline». Это **value в marker stream в keyframe time**. Поэтому массовые операции удобно строить на Keyframe Suite.
