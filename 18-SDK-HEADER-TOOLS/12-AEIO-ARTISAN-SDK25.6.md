# SDK 25.6: AEIO и Artisan

Дата: **2026-10-01**. Источник — присланный Adobe After Effects SDK **25.6 build 61**.

**Результат:** переписаны основные AEIO/Artisan chapters и integration contracts по current headers, bundled IO/FBIO/Artie samples и Register/Canvas suites. Это source review/documentation; новые native binaries и host runs не выполнялись.

## Место в плане

Итерация расширяет предметную часть stages 3–4 и документирует две integration families из Gate 6. **Gate 6 не закрыт:** нужен минимальный complete example, build/install/host report и correctness/stress evidence.

Обновлены:

- `04-AEIO/README.md`;
- `14-NATIVE-INTEGRATIONS/08-AEIO.md`;
- `05-ARTISAN/README.md`;
- `14-NATIVE-INTEGRATIONS/09-ARTISAN.md`.

## SDK identity

Принятый TAR SHA-256: `eee39a787ab09226a5a08c27496335faf79cbe52dd96f19cf795e48af09e2df6`.

| Файл | SHA-256 | Рассмотренные ranges |
|---|---|---|
| `Examples/Headers/AE_IO.h` | `be99e982c35069968dfa1b51030f04d47997a3cd7d524e5a658e8abf321c1822` | 72–104 BasicData/errors; 453–546 ModuleInfo; 569–856 FunctionBlock4 |
| `Examples/Headers/PR_Public.h` | `27f794d12ae0fed69c8a6fe79ed5d257c95a14534a8d6379aa8d2486321721e7` | 4–113 architecture/API/InData; 130–336 query/lifecycle/entry table |
| `Examples/Headers/AE_GeneralPlug.h` | `30d12ec3eb5af1a902c7414053b1be1da0204b226e0b1cdc71272be1e137000c` | 2782–2819 RegisterArtisan/RegisterIO; 3511–3907 Canvas8/ArtisanUtil1; 4264–4627 IOIn7/IOOut6 |
| `Examples/AEGP/IO/IO.cpp` | `ce05c82fa32a9b2387178709d59bd65a4bc095367df67c6d7e143666df65000e` | 69–276 input/options; 325–422 sparse/audio; 440–810 output; 985–1111 registration |
| `Examples/AEGP/IO/IO_PiPL.r` | `c2fb856b431d7730ff24a6ba18c59c3d740747161ef9d41acf14f378470fd27c` | 7–36 AEGP PiPL/entry symbol |
| `Examples/AEGP/FBIO/FBIO.cpp` | `ec686e1bd71cfcc18146ac682cb59d21fed4906c64883b23562a0dc209fb627b` | 820–951 ModuleInfo/function table/registration |
| `Examples/AEGP/FBIO/FBIO_PiPL.r` | `07fe98b71745a1c4e6c272f09b38af99a62a6a8dca18994a6e8b48e4899cb0f4` | PiPL registration resource |
| `Examples/AEGP/Artie/Artie.cpp` | `f6d025442b7b6a565ec86c6792db6b85c946d4ef342e6436ac781738a7d9b783` | 276–418 lifecycle stubs; 910–1095 scene/texture helpers; 1537–1608 render; 1611–1674 registration |
| `Examples/AEGP/Artie/Artie_PiPL.r` | `c5316a53b7ee6c4e2ac99358865acf035cd8a220bb6682cb8d0c6bc809aca179` | 7–36 AEGP PiPL/entry symbol |

## AEIO: current 25.6 contracts

### Callback table versus host suites

`AEIO_FunctionBlock4` содержит **49 callback slots** и помечен header-ом as frozen in AE10. Surrounding host suites продолжают rev:

- `AEGP_IOInSuite7`, version macro **8**, frozen in AE 25.3;
- `AEGP_IOOutSuite6`, version macro **9**, frozen in AE 25.2.

Следствие: sample call pattern и callback table shape стабильнее, но exact helper-suite generation берётся из target SDK, не из bundled sample.

### Basic data and error semantics

`AEIO_BasicData` содержит message callback, `SPBasicSuite`, AEGP plug id и refcon. AEIO имеет специализированные errors, включая `AEIO_Err_USE_DFLT_CALLBACK`, user cancel, disk full, bad filename, parsing/not-sequence.

`USE_DFLT_CALLBACK` — semantic delegation to host, не alias for success/unimplemented.

### Module capabilities

`AEIO_ModuleInfo` разделяет input/output/file/still/video/audio/options/layers/aux data/metadata/markers/deep flags. `flags2` добавляет float, ICC, CICP and other capabilities.

Capability flag alone не доказывает implemented callback path.

### Input options lifetime

`IO.cpp` создаёт options via MemorySuite, lock/fill, attaches to InSpec, unlocks; DisposeInSpec frees current options. Flatten creates separate flat options handle.

Source caveat: sample deliberately leaves old InSpec options handle unfreed after replacement due a comment about legacy AE sync bytecopy. Bible preserves this as historical sample-specific evidence instead of converting it to universal ownership rule.

### Sparse pixels and aux channels

`DrawSparseFrame` receives scale/time/required region/interrupts and writes to `PF_EffectWorld`; coordinates documented as scaled.

Aux pipeline: `GetNumAuxChannels` → `GetAuxChannelDesc` → `DrawAuxChannel` → `FreeAuxChannel`. This importer-side free callback is distinct from consumer-side PF Channel Suite checkout/checkin.

### Output state

`StartAdding` sample reads output metadata/path and conceptually opens/writes header; `AddFrame` receives rendered world; `EndAdding` finalizes. File path handles are MemorySuite resources.

IO sample's fake codec bodies are placeholders and do not prove format correctness.

### Color metadata

Current IOInSuite7 includes ICC embedded/assigned profile APIs and CICP setup. Old IO sample uses IOInSuite4 and therefore cannot be treated as complete 25.6 color-management reference.

## AEIO bundled samples

`IO` and `FBIO`:

- use AEGP PiPL/EntryPointFunc;
- clear ModuleInfo/FunctionBlock structs;
- fill callback table;
- register death hook;
- `AEGP_RegisterIO`;
- register memory id.

`IO` implements a broad fake video/audio/import/export skeleton and returns default callback on many paths. `FBIO` is a smaller still-oriented example. Neither is production codec proof.

## Artisan: current contract

`PR_Public.h` defines artisans as AEGP renderer modules and sets API version **1.0**. Other render parameters are queried via AEGP suites using opaque contexts.

`PR_ArtisanEntryPoints` lifecycle:

- global setup/setdown/about;
- instance setup/setdown/flatten/dialog;
- frame setup/render/frame setdown;
- query.

Only `render_func` is mandatory according to the table/sample comment. Plugin owns allocated global/instance/render data indicated by header comments.

### Context and suite baseline

Current SDK has:

- `AEGP_CanvasSuite8`, version macro **14**;
- `AEGP_ArtisanUtilSuite1`, version 1;
- current supporting Layer/Stream/etc suites elsewhere in header.

Artie uses older CanvasSuite5, LayerSuite5, ItemSuite6, StreamSuite2. It is pattern evidence, not current-signature evidence.

Canvas Suite supplies comp/time/ROI, layer contexts, texture/layer render services, track matte contexts, render receipts, bins, transforms, interactive viewport/buffer state and time mapping.

### Resource families

Reviewed header comments distinguish cleanup:

- Canvas textures → DisposeTexture;
- owned WorldH from relevant render calls → World Suite dispose;
- RenderReceiptH → DisposeRenderReceipt;
- PR plugin private global/instance/render handles → plugin setdown responsibilities.

Generic one-size-fits-all deleter would be wrong.

### Artie sample limitations

Artie lifecycle callbacks Global/Instance/Frame/Query are mostly empty success stubs. Therefore sample does not prove persistence, renderer options, query behavior or render-state cleanup.

Artie scene code is a teaching raytracer. Its Xcode project comment explicitly warns artisans are tricky and sample is a skeleton, not a best-case renderer.

Artie helper itself notes source item dimensions do not work for text layers and hints at render-context bounds APIs. Bible records this as a warning against treating every layer as raster footage.

Registration source sets both `artisan_version.majorS` and `.minorS` to `Artie_MAJOR_VERSION`. This may be intentional or typo; no silent correction is made without runtime/product intent.

## Architecture boundary

Artisan can integrate a custom 3D renderer into AE composition rendering, but still uses AE render contexts and host-provided layer/texture/effect services. This is not documented proof of a separate engine capable of rendering arbitrary complete AE compositions independently.

AEIO handles media I/O; Artisan handles renderer integration. Neither replaces the standard Effect API or arbitrary third-party plug-in execution.

## Verification status

| Check | Status |
|---|---|
| Headers/samples source review | DONE for listed ranges |
| Documentation rewrite | DONE |
| New exact-SDK compile | NOT RUN |
| AEIO module registration/load | NOT RUN |
| Real import/export pixel/audio/aux tests | NOT RUN |
| Artisan registration/selectability/render | NOT RUN |
| Artisan save/reopen/interactive/resource stress | NOT RUN |
| Windows host tests | NOT RUN |

GitHub docs CI, if green, confirms repository/document build only. Gate 6/7 remain open.