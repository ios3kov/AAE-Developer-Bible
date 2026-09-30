# AEIO — media import/export plug-ins

AEIO — AEGP specialization для import/export media.

## Import side

AEIO может:
- распознать/открыть файл;
- хранить interpretation/options;
- декодировать и отдавать AE frames;
- отдавать audio;
- сообщать metadata/capabilities.

## Export side

AEIO может:
- предоставлять output options;
- принимать rendered frames/audio от AE;
- кодировать и писать собственный format/container.

## Responsibility boundary

AEIO не получает «готовый codec за бесплатно». Compression/decompression и file format correctness — ответственность plug-in/подключённой codec library.

## Architecture

```text
AEIO callbacks
   ↓
Host adapter
   ↓
Format model / options
   ↓
Decoder / Encoder
   ↓
I/O abstraction
```

Decoder/encoder полезно сделать тестируемым вне AE.

## Tests

- corrupt/truncated files;
- odd dimensions;
- alpha/no alpha;
- all supported bit depths;
- audio only/video only;
- seek/random access;
- huge duration/files;
- cancellation;
- disk full/write errors;
- Unicode paths;
- network/removable storage errors if claimed supported.
