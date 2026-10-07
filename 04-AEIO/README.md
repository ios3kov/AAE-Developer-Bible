# AEIO — media import/export plug-ins

**Baseline source review:** Adobe After Effects SDK **25.6 build 61**.
**Core contracts:** `AEIO_ModuleInfo`, frozen `AEIO_FunctionBlock4`, current host suites `AEGP_IOInSuite7` and `AEGP_IOOutSuite6`, registration through `AEGP_RegisterIO`.
**Evidence level:** SDK-CONTRACT-REVIEWED / RUNTIME-NOT-CLAIMED.

AEIO — native I/O module for media that After Effects imports and/or exports. Это не effect renderer и не универсальный кодек API: module должен сам корректно распознавать, декодировать, кодировать и обслуживать свой format.

## Exact IO sample reading walkthrough

SDK 25.6 `Examples/AEGP/IO/IO.cpp`: читать module/function-block construction и
registration, затем `My_InitInSpecFromFile` (70), `My_DisposeInSpec` (183),
`My_FlattenOptions` (200), `My_InflateOptions` (255), `My_DrawSparseFrame` (325),
`My_GetSound` (394). Export: `My_InitOutputSpec` (441), flat/dispose output options
(500/538), `My_StartAdding` (651), `My_AddFrame` (735), `My_EndAdding` (760).
Line anchors относятся только к приложенной поставке; искать также имена functions.

Import route: validate untrusted header → create local options → attach to InSpec
with exact ownership API → populate metadata → random frame request with actual
time/region/world → bounded decode/cancel → dispose attached state. Сначала читать
`PretendToReadFileHeader`: название буквально предупреждает, что sample не является
полным parser/codec. Его stub callbacks не доказывают sound/format support.

Export route: validate options/path → initialize own encoder → append frame by
provided time/count policy → finalize or explicit incomplete/cancel result → release
encoder/options. Flat options сериализуют schema, не file pointer. Failed init
освобождает только successfully owned resources; ownership attachment не считать
равным простому присваиванию pointer. Temporary-file + atomic publish — production
recommendation, не автоматически показанная в IO guarantee.

Callback names/shape и paired host APIs сверять с target `AE_IO.h` и current
IOIn7/IOOut6. Sample старые generations не становятся current из-за наличия в SDK.

Source inconsistency: ConstructModuleInfo advertises HAS_AUX_DATA (line1018),
but ConstructFunctionBlock (1033–1082) does not assign GetNumAuxChannels,
GetAuxChannelDesc, DrawAuxChannel or FreeAuxChannel slots. Entry zero-initializes
the table. Thus IO is not evidence of a complete auxiliary provider; do not copy
its capability flags unchanged into a real importer. It registers IO before
RegisterWithAEGP obtains the memory id; later failure has no demonstrated unregister
rollback. Product initialization must address that partial-registration boundary.
Overview задаёт purpose, [registration chapter](../14-NATIVE-INTEGRATIONS/08-AEIO.md)
разбирает контракт, reference guide объясняет licensed workspace; не три независимых
implementation. No runtime import/export claimed.

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

Recommended decomposition:

```text
AEIO callback adapter
   ↓
validated InSpec/OutSpec state
   ↓
format/codec service
   ↓
bounded file/stream I/O
   ↓
pure parser/decoder/encoder components
```

Keep codec/core logic independent from `AEIO_InSpecH` / `AEIO_OutSpecH` wherever practical.

Benefits:

- malformed-file tests outside AE;
- deterministic decoder/encoder fixtures;
- fuzz/property tests for parser boundaries;
- no host handles inside long-lived codec objects;
- easier cancellation and file-handle ownership;
- easier reuse in helper tools.

The AEIO adapter should translate host lifecycle into domain operations; it should not contain the complete codec implementation.

## 16. Input state machine

A production importer should model its live spec state explicitly.

Example:

```text
UNINITIALIZED
→ HEADER_PARSED
→ LIVE_SPEC_READY
→ SOURCE_OPEN / LAZY_SOURCE
→ DISPOSING
→ DISPOSED
```

State may contain:

- copied canonical path;
- parsed immutable header/index;
- decoder configuration;
- cache/index;
- audio format;
- color/alpha interpretation data;
- product-owned file handle/reader;
- cancellation generation.

Do not put raw callback-local pointers into spec state.

## 17. Live options vs flat options

Treat these as different representations.

### Live options

Optimized for current process/session:

- handles to product-owned parsed state;
- normalized paths;
- decoded metadata;
- runtime cache configuration.

### Flat options

Disk/project-safe representation:

- versioned;
- endian/size explicit where relevant;
- no raw pointers;
- no file descriptors;
- no process addresses;
- no C++ vtables/STL object layout.

Pattern:

```text
live options
→ FlattenOptions
→ versioned flat bytes

flat bytes
→ validate version/size
→ InflateOptions
→ reconstruct fresh live state
```

Unknown/corrupt future versions need an explicit recovery policy.

Do not memcpy a live C++ struct as persistence format unless its byte layout is deliberately specified as the persisted schema.

## 18. Random access and sparse frame semantics

A host importer should assume frame requests can be:

- non-monotonic;
- repeated;
- skipped;
- sparse-region;
- at different quality/scale;
- cancelled.

Do not build a decoder architecture that only works for:

```text
frame 0 → frame 1 → frame 2 → ...
```

unless the format genuinely requires sequential decoding and your module implements an explicit seek/index/cache strategy around that constraint.

For compressed inter-frame media, product state may need:

- keyframe/index map;
- bounded decode cache;
- seek/reset path;
- deterministic repeated-frame behavior.

Sparse draw should separate **requested output region** from **codec decode dependency**: decoder may need more source data than the final requested rect, but must only write within the host output contract.

## 19. Required-region and scale discipline

`required_region`, scale and output world layout are independent inputs.

Do not infer:

- full-frame dimensions from output rect;
- contiguous rows from width;
- 1:1 scale;
- origin zero.

All writes must respect `rowbytes`, output pixel format and requested/scaled coordinates.

## 20. Cancellation

Cancellation is a normal lifecycle event, not exceptional corruption.

For decode/write loops:

```text
bounded unit of work
→ check interrupt/cancel
→ stop promptly
→ close/release product-owned resources
→ return cancellation result
```

Do not wait until a multi-gigabyte decode/write finishes before checking host cancellation.

Cleanup after cancel should be idempotent: normal DisposeInSpec/EndAdding may still follow depending on host flow.

## 21. Source file lifetime

Decide whether the importer:

- opens/closes per frame;
- keeps a lazy shared reader in spec state;
- caches only metadata/index and reopens data;
- supports removable/network paths.

If keeping file handles open:

- own them explicitly;
- close on DisposeInSpec and error;
- define behavior when source disappears;
- honor CloseSourceFiles callback semantics where applicable;
- do not rely on current working directory.

## 22. Importer selection and file verification

`VerifyFileImportable` should be cheap, bounded and safe on untrusted input.

Prefer a small sniff:

```text
open bounded prefix
→ validate magic/version/basic shape
→ answer importable/not importable
```

Do not fully decode the file in the verifier unless the format genuinely requires it.

Wrong extension and valid signature policy should be deliberate.

Malformed and merely unsupported files are different outcomes.

## 23. Audio input

Input audio path needs its own validated format contract:

- sample rate;
- channels;
- sample size/encoding;
- requested time/sample range;
- destination layout;
- conversion policy.

Do not reuse video frame timing math blindly for audio sample offsets.

If audio is not supported, do not advertise the module flag/callback path as though it is.

## 24. Output state machine

For sequence/container output:

```text
UNINITIALIZED
→ OPTIONS_READY
→ FILE_SELECTED
→ ADDING
→ FINALIZING
→ FINALIZED
```

On failure/cancel, transition through cleanup rather than pretending `EndAdding` completed normally.

State should track independently:

- file opened?;
- header written?;
- frames written?;
- audio started?;
- trailer/index pending?;
- temporary path/rename pending?;
- finalization complete?.

## 25. Atomic output strategy

When format permits, safer output can use:

```text
write temporary product-owned file
→ finalize successfully
→ flush/close
→ atomic/controlled rename to destination
```

This reduces half-valid outputs after cancellation/crash.

It is not universally possible for every container/filesystem, so document format/product policy.

Never overwrite an existing destination before you know your overwrite/recovery semantics.

## 26. AddFrame / frame order

Do not assume frames always arrive in monotonically increasing order unless callback/format contract guarantees it.

If format requires sequential output:

- validate frame order;
- reject unsupported order clearly;
- or buffer/reorder within bounded policy.

Do not silently write frame N into slot N+1.

## 27. Output audio

For audio output define:

- expected sample format;
- chunk ordering;
- sample/time conversion;
- interleaving;
- buffering;
- finalization.

A product that advertises audio must handle audio cancellation/write failure independently from video success.

## 28. Metadata and markers

If the module claims metadata/marker support:

- define mapping between AE data and file schema;
- preserve unknown metadata intentionally or explicitly drop it;
- version your own metadata payloads;
- define string encoding;
- define marker timebase conversion;
- avoid hidden lossy transformations.

Metadata support is not “copy arbitrary blobs”.

## 29. Auxiliary channels

Aux data flow is a separate contract:

```text
enumerate semantic channels
→ describe PF_ChannelDesc
→ draw requested chunk
→ host consumes
→ FreeAuxChannel
```

Every allocation returned by `DrawAuxChannel` needs paired release semantics.

Do not expose a file plane as Z-depth/Object ID merely because its byte layout resembles one; semantic descriptor matters.

## 30. Color management

Importer should make an explicit color interpretation decision.

Possible source information:

- embedded ICC;
- assigned profile;
- CICP;
- non-RGB/native color model;
- alpha interpretation;
- field/interlace metadata.

Do not apply color transform twice: either return pixels in the contract expected by AE and declare metadata accordingly, or use the documented conversion path.

Exporter likewise needs to distinguish:

- pixels AE hands to module;
- output encoding color space;
- file metadata/profile written.

## 31. Error taxonomy

Keep domain errors meaningful:

| Class | Example |
|---|---|
| unsupported | valid format/version feature not supported |
| corrupt | malformed/truncated/inconsistent file |
| I/O | read/write/permission/network failure |
| resource | allocation/decoder init failure |
| cancel | user/host requested stop |
| destination | disk full/name/overwrite failure |
| host | suite/callback/contract failure |
| cleanup | close/finalize/release failure |

Do not report a disk failure as unsupported media.

## 32. Failure cleanup

For every callback that acquires product resources:

```text
acquire
→ mark owned
→ operation
→ failure possible
→ cleanup owned resources
→ preserve primary error
```

Examples:

- options MemHandle;
- file handle;
- decoder instance;
- temp output file;
- aux channel buffer;
- metadata handle.

## 33. Threading

Do not infer thread safety from callback table stability.

Codec core may be thread-safe while host suites are not, or vice versa.

Document separately:

- AEIO callback thread assumptions from exact contract;
- decoder internal thread safety;
- shared cache synchronization;
- file-handle concurrency;
- cancellation synchronization.

Avoid holding product locks while calling opaque host APIs.

## 34. Performance

Measure separately:

- file I/O;
- parse/index;
- decode;
- color conversion;
- scale/region copy;
- audio conversion;
- cache hit/miss;
- encode;
- flush/finalize.

Do not optimize full-frame decode if host mostly requests sparse previews until profiling proves it matters.

## 35. Security / untrusted media

Validate before allocation/read:

- dimensions;
- counts;
- offsets;
- multiplication/overflow;
- compressed sizes;
- recursion/decompression limits;
- metadata/string lengths;
- chunk boundaries.

Never trust file-provided sizes to fit platform integer types.

## 36. Product validation guidance

If a concrete importer/exporter claims these capabilities, useful runtime cases include:

- clean registration and no module conflict;
- supported/unsupported/corrupt files;
- still and sequence;
- random seek / repeated frame;
- sparse region and scale;
- claimed pixel depths;
- alpha/interlace/color profile/CICP;
- aux channels + paired free;
- audio input/output;
- markers/user metadata if claimed;
- Unicode paths;
- flatten/inflate/save/reopen;
- cancellation;
- disk full / permission denied;
- removable/network path if claimed;
- repeated open/close without leaked state;
- exporter finalization/recovery after failure.

These cases establish product support evidence. Bible remains SDK-CONTRACT-REVIEWED / RUNTIME-NOT-CLAIMED unless a separate runtime record exists.

## 37. Production workflow

### Importer

```text
define format/capabilities
→ implement bounded verifier
→ build pure parser/index
→ define InSpec live state
→ implement one deterministic frame
→ add random/sparse access
→ add options flatten/inflate
→ add audio/metadata/aux as claimed
→ add cancel/error cleanup
→ optimize/cache
```

### Exporter

```text
define output schema/options
→ OutSpec state
→ select destination
→ open temp/final target
→ write deterministic frame
→ add sequence/audio/metadata
→ implement cancel/write-failure cleanup
→ finalize atomically where possible
→ verify produced file independently
```

## Related chapters

- [AEIO native integration](../14-NATIVE-INTEGRATIONS/08-AEIO.md)
- [Footage / import](../17-NATIVE-SUITE-COOKBOOK/09-FOOTAGE-IMPORT.md)
- [Auxiliary channels](../02-EFFECT-PLUGINS/08-AUXILIARY-CHANNELS.md)
- [Memory / Undo / Persistent Data](../17-NATIVE-SUITE-COOKBOOK/12-MEMORY-UNDO-PERSISTENCE.md)
- [Lifetime / threading](../17-NATIVE-SUITE-COOKBOOK/14-LIFETIME-THREADING.md)
- [Release checklist](../11-DISTRIBUTION/03-RELEASE-CHECKLIST.md)

## Source record

SDK hashes, callback generations, IO/FBIO sample ranges and limits: [AEIO/Artisan SDK 25.6 review](../18-SDK-HEADER-TOOLS/12-AEIO-ARTISAN-SDK25.6.md).
