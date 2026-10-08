# Footage / import: ownership, interpretation, sequences and proxies

**Baseline source review:** Adobe After Effects SDK **25.6 build 61**.
**Current suite generations in that SDK:** `AEGP_FootageSuite5`, `AEGP_ItemSuite9`, `AEGP_CompSuite12`, `AEGP_LayerSuite9`.
**Evidence level:** SDK-CONTRACT-REVIEWED / RUNTIME-NOT-CLAIMED.

Предыдущая версия главы смешивала baseline 25.6 с более поздним `CompSuite13`. Для supplied SDK 25.6 current declaration — `CompSuite12`. Это исправлено здесь.

## 1. Три разных сценария

Сквозной [import/adopt/create/animate/queue route](../03-AEGP/02-PROJECT-RENDER-AUTOMATION.md)
использует эту страницу как exact ownership contract. Здесь нет authored compiled
FootageRecipes.cpp: snippet ниже и SDK sources — evidence basis; не путать наличие
chapter с отдельным tested implementation. До adoption error dispose caller-owned
footage; после adoption компенсация через project-item policy, не DisposeFootage.

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

### B. Новый media decoder или encoder

**Public guide, 2026-10-08: DOCUMENTED / RUNTIME-NOT-CLAIMED.**

AEIO предоставляет AE pixels/audio собственного формата. MediaCore — другой
importer API; именно для него guide описывает приоритет importers и попытку
следующего обработчика. Установка AEIO сама по себе не обещает перехват уже
обслуживаемого формата. [Источник](https://github.com/docsforadobe/after-effects-plugin-guide/blob/6d9b285d9755d1fbf8ead7680ba49de24f94b547/docs/aeios/aeios.md)

### C. Формат описывает проект или timeline

Для файла, который нужно преобразовать в композиции и связанные items, public
guide выделяет `AEGP_FIMSuite3`. Путь: зарегистрировать import flavor, его
filetypes/extensions и callbacks; после импорта обозначить результат через
`AEGP_SetImportedItem`. Это отдельный контракт от media AEIO. [Источник](https://github.com/docsforadobe/after-effects-plugin-guide/blob/6d9b285d9755d1fbf8ead7680ba49de24f94b547/docs/aegps/aegp-suites.md#L4115-L4141)

**Рекомендация:** сначала определить результат импорта. Decoder выдаёт samples;
project translator создаёт структуру проекта и использует уже поддерживаемое
media. Во втором случае заранее разобрать файл в собственный план, а host objects
создавать с проверкой актуального контекста, Undo и отчётом частично выполненных
действий. Регистрация flavor не решает ownership созданных items и не реализует
чтение нового media формата.

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

## 14. Product validation guidance

If a concrete product claims footage/import behavior, useful runtime cases include:

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

These cases establish product runtime/support evidence. Bible does not require running them to document the SDK contract accurately.

## 15. Recommended import/adoption workflow

For host-supported media:

~~~text
normalize UTF-16 path + import options
→ NewFootage
→ plugin owns FootageH
→ validate destination/project context
→ AddFootageToProject / SetProxy / Replace
→ on success: ownership transfers to project
→ on failure: plugin still disposes FootageH
→ use returned ItemH / project-owned footage only through project APIs
~~~

Implement the ownership transition explicitly. A small state object/RAII wrapper can represent:

~~~text
OwnedByPlugin
→ AdoptedByProject
~~~

and release its cleanup obligation only after successful adoption.

## 16. Interpretation workflow

Treat interpretation as a distinct project mutation:

~~~text
import/adopt footage
→ obtain ItemH
→ GetFootageInterpretation
→ modify only intended fields
→ SetFootageInterpretation
→ preserve unrelated interpretation settings
~~~

Do not hide interpretation changes inside a generic "import file" helper unless that is part of the product contract.

## 17. Failure and rollback cases

Plan for:

- invalid/missing path;
- unsupported media;
- NewFootage failed;
- NewFootage succeeded but adoption failed;
- proxy/replace failed after caller acquired new footage;
- destination folder/item invalidated;
- sequence range/options malformed;
- placeholder path/file-type mismatch;
- interpretation mutation failed;
- path MemHandle acquired but later read/copy failed;
- project changed during async path preparation.

Most important ownership rule:

> after `NewFootage`, failure before successful adoption still leaves a caller-owned resource to dispose.

## 18. Path and identity policy

Do not keep a returned path pointer beyond MemorySuite lock lifetime.

For long-lived product state store copied path/config data, not locked MemHandle pointers or detached host handles.

Do not treat path alone as permanent project-item identity; relink/replace/proxy workflows can change file associations.

## 19. Anti-patterns

Avoid:

- passing Boolean `FALSE` where `AEGP_InterpretationStyle` is expected;
- disposing footage already adopted by project;
- forgetting disposal when adoption fails;
- disposing project-owned footage returned from Item APIs;
- assuming `GetFootageNumFiles` describes semantic Z-depth/Object-ID channels;
- treating Footage Suite as custom decoder API instead of using AEIO;
- hiding interpretation mutation inside unrelated import logic;
- copying sample suite generations without checking current headers.

## Related chapters

- [Project / items](01-PROJECT-ITEMS.md)
- [Compositions](02-COMPOSITIONS.md)
- [Layers](03-LAYERS.md)
- [Memory / Undo / Persistent Data](12-MEMORY-UNDO-PERSISTENCE.md)
- [AEIO](../04-AEIO/README.md)
- [AEIO native integration](../14-NATIVE-INTEGRATIONS/08-AEIO.md)

## Source record

Точные hashes, suite-generation corrections и sample findings: [Masks/text/footage SDK 25.6 review](../18-SDK-HEADER-TOOLS/11-MASK-TEXT-FOOTAGE-SDK25.6.md).
