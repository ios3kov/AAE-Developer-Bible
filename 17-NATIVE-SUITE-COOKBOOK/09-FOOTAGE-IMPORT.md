# Footage / import: ownership, interpretation, sequences and proxies

**Baseline source review:** Adobe After Effects SDK **25.6 build 61**.
**Current suite generations in that SDK:** `AEGP_FootageSuite5`, `AEGP_ItemSuite9`, `AEGP_CompSuite12`, `AEGP_LayerSuite9`.
**Verification level:** SDK source-reviewed; exact host import/load/render acceptance remains pending.

Предыдущая версия главы смешивала baseline 25.6 с более поздним `CompSuite13`. Для supplied SDK 25.6 current declaration — `CompSuite12`. Это исправлено здесь.

## 1. Два разных сценария

### A. Импорт media, который After Effects уже умеет читать

Используйте Footage Suite:

```text
UTF-16 path + optional layered/sequence options
→ AEGP_NewFootage
→ caller-owned AEGP_FootageH
→ AEGP_AddFootageToProject
→ project adopts FootageH
→ получаем ItemH
→ optional AddLayer(item, comp)
```

### B. Новый file format / новый importer

Это не `AEGP_NewFootage`. Нужен **AEIO/File Import** path. Footage Suite просит host импортировать уже поддерживаемый тип; она не реализует decoder.

См. `04-AEIO/` и native integration chapters.

## 2. Ownership AEGP_FootageH меняется при adoption

`AEGP_NewFootage` прямо документирует: returned footage **caller owns until disposed or added to project**.

`AEGP_AddFootageToProject`:

- undoable;
- project **adopts** FootageH;
- тот же FootageH нельзя добавить второй раз.

`AEGP_SetItemProxyFootage` и `AEGP_ReplaceItemMainFootage` также принимают footage, которое будет adopted project-ом.

`AEGP_DisposeFootage` говорит обратную сторону контракта: **не dispose footage, которое уже owned/adopted project-ом**.

Production pattern:

```text
footageH = NewFootage
owned_by_plugin = true

try AddFootageToProject / SetProxy / Replace
if adoption succeeded:
    owned_by_plugin = false

on exit:
    if owned_by_plugin:
        DisposeFootage
```

Без этого error path после успешного `NewFootage` и неудачного adoption создаёт утечку caller-owned resource.

## 3. Main/proxy footage, полученное из item, уже принадлежит project

`AEGP_GetMainFootageFromItem` и `AEGP_GetProxyFootageFromItem` возвращают footage, связанное с project item. Это не новый caller-owned object из `NewFootage`.

Не передавайте такой handle в `AEGP_DisposeFootage`: disposal API прямо запрещает освобождать project-owned footage.

`GetProxyFootageFromItem` возвращает ошибку, если proxy отсутствует; сначала проверяйте item state там, где workflow это требует.

## 4. Paths возвращаются как MemorySuite handles

`AEGP_GetFootagePath` возвращает `AEGP_MemHandle` с null-terminated UTF-16 path. Его нужно освободить через `AEGP_FreeMemHandle`.

Аргументы:

- `frame_numL` — номер frame;
- `file_indexL` — main/aux file index;
- `AEGP_FOOTAGE_MAIN_FILE_INDEX` = 0.

Empty string означает отсутствие файла для этого slot. Это не то же самое, что null handle или failed API call.

Официальный `ProjDumper` показывает правильный pair: `GetFootagePath` → `AEGP_FreeMemHandle`.

## 5. File count и auxiliary files

`AEGP_GetFootageNumFiles` возвращает:

- количество main files;
- `files_per_frame`, причём main file включён в count; comment приводит `1` как случай без auxiliary data.

Это полезно для inventory layered/multi-file footage, но само по себе **не доказывает семантические auxiliary channels** вроде Z-depth/Object ID. Для 3D Channel Extract такие channels квалифицируются отдельно через importer/channel API.

## 6. NewFootage: path, layered key, sequence options, interpretation style

```cpp
AEGP_FootageH footageH = nullptr;
ERR(suites.FootageSuite5()->AEGP_NewFootage(
    plugin_id,
    utf16_path,
    layer_key_or_null,
    sequence_options_or_null,
    AEGP_InterpretationStyle_NO_DIALOG_GUESS,
    nullptr,
    &footageH));
```

Path — null-terminated UTF-16 с platform separators.

`AEGP_FootageLayerKey` содержит layer id/index/name/draw style для layered source. Special indices:

- `AEGP_LayerIndex_UNKNOWN = -2`;
- `AEGP_LayerIndex_MERGED = -1`;
- `AEGP_LayerID_UNKNOWN = -1`.

`AEGP_FileSequenceImportOptions`:

- `all_in_folderB`: sequence vs still;
- `force_alphabeticalB`;
- start/end frame;
- `AEGP_ANY_FRAME = -1` для earliest/latest auto selection.

## 7. InterpretationStyle — enum, а не boolean concept

SDK 25.6 определяет:

- `NO_DIALOG_GUESS = 0`;
- `DIALOG_OK = 1`;
- `NO_DIALOG_NO_GUESS = 2`.

Старые Adobe samples передают `FALSE` в этот аргумент; численно это 0 и поэтому совпадает с `NO_DIALOG_GUESS`. Новый код должен использовать **named enum**, а не boolean, иначе смысл теряется и значение 2 невозможно выразить.

## 8. Footage interpretation — отдельный mutable contract

`AEGP_FootageInterp` включает:

- interlace label;
- alpha flags/matte color;
- pulldown phase;
- loop behavior;
- pixel aspect ratio;
- native/conform FPS;
- depth;
- motion-detection flag.

`AEGP_GetFootageInterpretation(itemH, proxyB, ...)` и `SetFootageInterpretation` работают через **ItemH**, а не через detached caller-owned FootageH. Set operation undoable.

Не меняйте interpretation неявно внутри «просто импортировать» helper: это отдельное user-visible project mutation.

## 9. Alpha interpretation

`AEGP_AlphaLabel` имеет flags:

- premultiplied;
- inverted;
- ignore.

И matte RGB для premultiplied interpretation. Эти flags описывают source interpretation, а не готовый pixel world вашего effect.

При тестах import pipeline сохраняйте исходный alpha mode и сравнивайте его после save/reopen; не делайте вывод по одному preview pixel.

## 10. Proxy и replace — adoption тоже меняет ownership

Proxy workflow:

```text
NewFootage(proxy)
→ caller owns proxyH
→ SetItemProxyFootage(proxyH, itemH)
→ project adopts proxyH
→ optional SetItemUseProxy(TRUE)
```

Replace main footage имеет тот же переход ownership после успешного `AEGP_ReplaceItemMainFootage`.

Если SetProxy/Replace возвращает error, caller всё ещё должен располагать cleanup path для не-adopted footage.

## 11. Placeholder and solid footage

`AEGP_NewPlaceholderFootage` создаёт missing-signature footage без изменения project. `AEGP_NewPlaceholderFootageWithPath` дополнительно принимает path platform и AEIO file type.

Header отмечает:

- `AEIO_FileType_NONE` — warning condition;
- при `AEIO_FileType_ANY` path **обязан существовать**;
- если path может отсутствовать, используйте подходящий folder/generic file type.

`AEGP_NewSolidFootage` создаёт caller-owned solid footage. После adoption через project к нему применяются `Get/SetSolidFootageColor` и `SetSolidFootageDimensions`; dimensions ограничены 1..30000.

## 12. Official samples: patterns и их ограничения

### ProjDumper

Полезный read pattern:

`GetMainFootageFromItem` → interpretation/file count/path → `FreeMemHandle(path)`.

Import code показывает NewFootage → AddFootageToProject → proxy adoption, но error paths не являются complete RAII example.

### Projector

Projector создаёт layered PSD footage, ordinary footage, proxy и меняет interpretation. Он использует `FootageSuite5`, но рядом старые Item/Layer suite generations.

В samples `FALSE` передаётся как interpretation style; это работает из-за numeric value 0, но новый код должен использовать enum name.

### Важная ownership граница samples

Если `AEGP_NewFootage` succeeded, а `AEGP_AddFootageToProject` / `SetItemProxyFootage` failed, reviewed sample snippets не показывают complete `DisposeFootage` rollback для каждого такого path. Поэтому samples полезны для call order, но не являются production ownership proof.

## 13. Почему здесь нет «универсальной 10-строчной функции»

Корректный import helper обязан знать:

- path ownership/encoding;
- still vs sequence;
- layered source selection;
- interpretation policy;
- destination folder;
- proxy/main adoption state;
- error cleanup;
- whether user dialogs разрешены;
- missing/relink behavior.

Слишком короткий helper обычно скрывает один из этих contracts.

## 14. Host acceptance matrix

- still file;
- numbered sequence;
- layered PSD merged/specific layer;
- source with alpha interpretation variants;
- proxy attach/toggle;
- replace main footage;
- missing file placeholder;
- solid footage;
- invalid path;
- adoption failure cleanup;
- save/reopen/relink;
- Windows/macOS path cases;
- multi-file/auxiliary footage inventory;
- repeated import without duplicate ownership errors.

Exact import flags/behavior считаются host-verified только после выполнения этих сценариев в named AE build.

## Source record

Точные hashes, suite-generation corrections и sample findings: [Masks/text/footage SDK 25.6 review](../18-SDK-HEADER-TOOLS/11-MASK-TEXT-FOOTAGE-SDK25.6.md).