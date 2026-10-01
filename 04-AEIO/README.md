# AEIO — media import/export plug-ins

**Baseline source review:** Adobe After Effects SDK **25.6 build 61**.
**Core contracts:** `AEIO_ModuleInfo`, frozen `AEIO_FunctionBlock4`, current host suites `AEGP_IOInSuite7` and `AEGP_IOOutSuite6`, registration through `AEGP_RegisterIO`.
**Verification level:** SDK source-reviewed; no new AEIO binary or host import/export run in this editorial iteration.

AEIO — native I/O module for media that After Effects imports and/or exports. Это не effect renderer и не универсальный кодек API: module должен сам корректно распознавать, декодировать, кодировать и обслуживать свой format.

## 1. Где AEIO находится в архитектуре

```text
AEGP EntryPointFunc
→ заполнить AEIO_ModuleInfo
→ заполнить AEIO_FunctionBlock4
→ AEGP_RegisterIO
→ AE вызывает import/output callbacks
→ callback использует IOIn/IOOut/Memory/World/etc suites
```

`AEIO_BasicData` передаётся каждому callback и содержит message function, `SPBasicSuite`, AEGP plug-in id и registered IO refcon. Это не Effect `PF_InData` и не Artisan `PR_InData`.

## 2. ModuleInfo — capabilities до декодирования

`AEIO_ModuleInfo` описывает:

- module signature/name;
- input/output/file/still/video/audio capabilities;
- maximum dimensions;
- supported file kinds/extensions/clipboard types;
- create kind/extension;
- auxiliary extensions;
- secondary flags.

Особенно важные flags:

- `AEIO_MFlag_INPUT` / `OUTPUT`;
- `FILE`, `STILL`, `VIDEO`, `AUDIO`;
- `NO_OPTIONS`, `INPUT_OPTIONS`, `SEQ_OPTIONS_DLG`;
- `HAS_LAYERS`;
- `HAS_AUX_DATA`;
- `CAN_DRAW_DEEP`;
- `HAS_META_DATA`, marker flags;
- `AEIO_MFlag2_CAN_DRAW_FLOAT`;
- ICC/CICP-related flags.

Заявленный flag должен соответствовать реально реализованным callbacks. `HAS_AUX_DATA` без descriptor/draw/free path — не полноценная поддержка auxiliary channels.

## 3. FunctionBlock4 frozen, но окружающие suites продолжают развиваться

`AEIO_FunctionBlock4` в header помечен как revved to 4 in AE10 и frozen there. Он содержит **49 callback slots**: input lifecycle, sparse video/audio, output lifecycle, options, aux channels/files, metadata/user data, markers, verification и MIME.

При этом supplied AE 25.6 имеет:

- `AEGP_IOInSuite7`, version macro 8, frozen in AE 25.3;
- `AEGP_IOOutSuite6`, version macro 9, frozen in AE 25.2.

То есть стабильность callback table **не означает**, что host-side helper suites frozen на том же уровне. Новый модуль должен собираться против declarations целевого SDK.

## 4. Import lifecycle

Упрощённо:

```text
VerifyFileImportable
→ InitInSpecFromFile / Interactive
→ module attaches options/state to AEIO_InSpecH
→ AE asks dimensions/duration/depth/alpha/audio/etc
→ DrawSparseFrame / GetSound as needed
→ optional aux-channel callbacks
→ SynchInSpec / options flatten-inflate if required
→ DisposeInSpec
```

`InitInSpecFromFile` получает UTF-16 path и opaque InSpec. Сам InSpec host-owned; module обычно хранит собственное state/options через IOIn Suite.

## 5. InSpec options: это реальный ownership contract, не просто void*

Официальный `IO` sample:

- создаёт options через `AEGP_NewMemHandle`;
- lock → fill → unlock;
- присоединяет через `AEGP_SetInSpecOptionsHandle`;
- при DisposeInSpec получает options и `AEGP_FreeMemHandle`;
- FlattenOptions делает отдельный disk-safe flat handle.

Особая legacy-оговорка sample: при замене input options он **намеренно не free-ит old options handle** из-за старого внутреннего AE sync path, который byte-copies input to output options. Это sample/source caveat, а не универсальное правило «никогда не free old handle». Для своего module ownership нужно подтвердить current contract и фактический lifecycle.

## 6. Default callbacks

`AEIO_Err_USE_DFLT_CALLBACK` — специальный return code, которым module просит host применить default behavior там, где такой default предусмотрен.

В `IO.cpp` sample через него реализованы, например, `SynchInSpec`, `GetActiveExtent`, `GetDimensions`, `GetDuration`, `GetTime`, `SetOutputFile`, `WriteLabels`, `GetSizes` и другие stubs.

Это не универсальный «success». Для callback, где default не поддерживается или module flag требует собственную реализацию, такой return может быть неверным выбором. Проверяйте конкретный callback/header/sample.

## 7. Sparse frame: region, scale и row layout

`AEIO_DrawSparseFrame` получает `AEIO_DrawSparseFramePB`: quality, rational scale, time range/duration, `required_region` и interrupt callbacks.

Header говорит, что coordinates находятся в **scaled coordinate system**. Empty `required_region` означает full frame. Module должен уважать output `PF_EffectWorld` layout, depth и rowbytes; не вычислять строки как `width*sizeof(pixel)` без проверки.

Sample IO просто заполняет requested region цветом — это демонстрация contract, не decoder.

## 8. Auxiliary channels — отдельный AEIO contract

Для importer, который реально предоставляет Z-depth, Object ID, normals и т.п., `AEIO_FunctionBlock4` содержит:

```text
GetNumAuxChannels
→ GetAuxChannelDesc
→ DrawAuxChannel
→ FreeAuxChannel
```

`DrawAuxChannel` выдаёт `PF_ChannelChunk`; `FreeAuxChannel` — paired cleanup callback. `AEIO_MFlag_HAS_AUX_DATA` лишь сообщает capability; semantic type/dimension/datatype идут через `PF_ChannelDesc`.

Это ровно та граница, которая важна для [auxiliary-channel chapter](../02-EFFECT-PLUGINS/08-AUXILIARY-CHANNELS.md): наличие EXR/RLA/RPF plane в файле ещё не доказывает, что importer выставил AE semantic channel.

## 9. Output lifecycle

Типичный sequence/container output:

```text
InitOutputSpec
→ options / user dialog / OutputInfoChanged
→ SetOutputFile
→ StartAdding
→ AddFrame (0..N)
→ AddSoundChunk / AddMarker as applicable
→ Flush
→ EndAdding
→ DisposeOutputOptions
```

Для single-frame path есть `OutputFrame`. Формат может поддерживать нелинейное добавление frames только если module заявляет соответствующий flag.

`AddFrame` получает rendered `PF_EffectWorld`, origin, frame index/count, compression flag и interrupt callbacks. AE уже отрендерил frame; AEIO обязан **закодировать/записать** его, а не заново исполнять composition.

## 10. Output path и MemorySuite handles

IOOut Suite getters могут возвращать `AEGP_MemHandle` для output file path. Официальный IO sample делает lock/read → unlock → `AEGP_FreeMemHandle`.

Не храните указатель на locked buffer после unlock; не путайте ownership path handle с жизнью самого `AEIO_OutSpecH`.

## 11. Audio

Input `GetSound` получает exact time/sample range и target buffer. Output `AddSoundChunk` получает start time, sample count и data pointer.

Module flags и OutSpec/InSpec audio fields должны согласовываться с реально поддерживаемыми rate/channels/sample-size/encoding. Нельзя заявить `AUDIO` и игнорировать формат samples.

## 12. Color management

`AEGP_IOInSuite7` в SDK 25.6 содержит APIs для:

- embedded/assigned ICC profiles;
- native start/drop-frame metadata;
- CICP color-space metadata.

Header подробно разделяет RGB/non-RGB cases и working-space interpretation. Если importer декодирует YUV/non-RGB напрямую в working space или в specific RGB space, profile contract должен быть выставлен сознательно; иначе AE может интерпретировать pixels в неверном space.

Color metadata — не косметический tag: она меняет смысл sample values.

## 13. Sample IO vs FBIO

`IO.cpp` — более широкий fake video/audio/input/output sample. `FBIO.cpp` — более компактный still-file example.

Оба:

- zero-init `AEIO_ModuleInfo` и `AEIO_FunctionBlock4`;
- заполняют callback table;
- регистрируют death hook;
- вызывают `AEGP_RegisterIO`;
- регистрируют memory id через Utility Suite.

Они полезны как call-order skeleton. Их fake formats, old IOIn/Out suite generations и simplified error paths не являются production codec implementation.

## 14. Error and cancellation policy

AEIO имеет собственные error codes: unsupported/unimplemented/filetype, invalid time, user cancel, disk full, bad filename, parsing, not-sequence, default-callback request.

Production module должен различать:

- malformed input;
- unsupported but valid input;
- I/O failure;
- user cancel;
- disk-full/write failure;
- host callback failure;
- cleanup failure.

Не превращайте любой decoder exception в `UNSUPPORTED_FILETYPE`: это скрывает corrupt file и I/O bugs.

## 15. Architecture

Рекомендуемый слой:

```text
AEIO callback adapter
   ↓
validated module/spec state
   ↓
decoder / encoder core
   ↓
bounded I/O abstraction
   ↓
unit tests outside AE + host integration tests
```

Codec core лучше держать независимым от `AEIO_InSpecH`/`OutSpecH`: это облегчает fuzz/corruption tests и позволяет проверять формат без запуска AE.

## 16. Host acceptance matrix

- clean registration and no duplicate module;
- supported/unsupported/corrupt files;
- still and sequence;
- random seek/sparse region;
- 8/16/float output where claimed;
- alpha/interlace/color-profile/CICP;
- aux channels + paired free;
- audio input/output;
- markers/user metadata if claimed;
- Unicode paths;
- flatten/inflate/save/reopen;
- cancellation;
- disk full / permission denied;
- missing/removable/network path if claimed;
- repeated open/close without leaked options/files.

До этого source-reviewed chapter не является host-verified importer/exporter.

## Source record

SDK hashes, callback generations, IO/FBIO sample ranges and limits: [AEIO/Artisan SDK 25.6 review](../18-SDK-HEADER-TOOLS/12-AEIO-ARTISAN-SDK25.6.md).