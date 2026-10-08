# ExtendScript runtime: полная сверка guide

Дата: **2026-10-08**. Parent Bible revision:
`065df27eb0687cc71843d9d71fc2ff599a4b9392`.

Прочитаны и сопоставлены с практическими операциями **73/73 Markdown страницы
под `docs/`** в JavaScript Tools Guide. К ранее опубликованным File/Folder/runtime
материалам добавлены ScriptUI, BridgeTalk, остальные runtime/data interfaces и
раздел отладки. Новая глава увеличивает текущий core inventory до **130** страниц.

## Источник и воспроизводимость

| Поле | Значение |
|---|---|
| Repository | [docsforadobe/javascript-tools-guide](https://github.com/docsforadobe/javascript-tools-guide/tree/ac6839049e17f4652d301e7d28f8f0d3d5fbb66a) |
| Commit | `ac6839049e17f4652d301e7d28f8f0d3d5fbb66a`, 2026-01-23 |
| Git tree | `edb30d633a85608f310fd3bb9a3023d42cd21766` |
| Exact bytes / lines | 1 045 098 / 18 027 |
| Inventory | [extendscript-runtime-inventory-2026-10-08.json](extendscript-runtime-inventory-2026-10-08.json) |
| Review ledger | [extendscript-runtime-reviewed-2026-10-08.json](extendscript-runtime-reviewed-2026-10-08.json) |

Непересекающиеся группы: **8** File/Folder/base-runtime страниц, **31** ScriptUI/
BridgeTalk и **34** остальных runtime/data/tooling страниц. Старый восьмистраничный
блок сохраняет свою дату и состав; его portable file tests не становятся тестами
всех остальных runtime interfaces. Все raw bytes сверены с Git blobs, размерами
и SHA256. Полное чтение включает большие XML/XMP/native-interface таблицы, а также
исторические и индексные страницы.

Это community-maintained mirror Adobe material со старыми CS4/CS5/ESTK разделами.
Полнота чтения конкретного snapshot не означает modern AE support matrix,
все signatures или разрешение противоречивых declarations догадкой.

## Передача в книгу

| Глава | Законченный практический маршрут |
|---|---|
| [File/Folder](06-SCRIPTING/01-OBJECT-MODEL.md#extendscript-files-runtime) | Сохранены bounded read/export, byte/character distinction, permission/cancel/cleanup и отдельный sidecar/project outcome; общий ledger теперь включает73 страницы |
| [ScriptUI](06-SCRIPTING/02-SCRIPTUI.md) | Modal outcomes и Window/Panel boundary; initial/repeated layout; draft model, event/listener ownership и re-entry; list/tree rebuild; localization/drawing; bounded progress update |
| [BridgeTalk](15-COMMUNICATION/05-SCRIPT-TO-AE.md#bridgetalk) | Полный target, retained message, queue expiry versus synchronous wait, receipt/intermediate/final result, bounded registry и неизвестный outcome |
| [Runtime/data/debugger](06-SCRIPTING/04-EXTENDSCRIPT-RUNTIME.md) | Reflection, units/localization, byte-framed Socket, ExternalObject ownership, XML edit/readback, XMP packet и update-mode file lifecycle, actual debugger route |

Новые собственные snippets: ScriptUI layout и tree creation, read-only BridgeTalk
probe construction, per-instance UnitValue conversion, XMP packet preparation
и минимальный debugger `attach` config. Они иллюстрируют конкретные операции;
нового выполнения JSX, network/library/XML/XMP или AE не было.

## Дополнительные первичные источники

Вне знаменателя73 отдельно прочитаны:

- Adobe `SnpCreateTreeView.jsx` на CEP revision
  `ab5e4e3e53a42fad08e1225a22a991bb1ffe73f6`: sample подтверждает TreeView child
  ownership, пропущенный формальной generic `add()` table. Filesystem traversal
  и построение пути из display label из sample не перенесены в рецепт.
- Adobe ESTK `Readme.md` на той же revision: точный источник исторической
  границы32-bit Toolkit. File identity сохранена отдельно в ledger.
- Официальный [Adobe V2 debugger README](https://marketplace.visualstudio.com/items?itemName=Adobe.extendscript-debug),
  прочитанный2026-10-08. Это dated vendor source, без выдуманной immutable revision
  или original-HTML hash. Сохранённая hashed extraction частичная:325 различных
  нумерованных строк из611; дополнительные разделы читались отдельными запросами.
  Полное чтение относится к совокупной сверке, не к полноте этого cache. Hash tool
  extraction явно отделён от исходной страницы.

Ранее прочитанная vendor-страница разрешений AE scripts также остаётся отдельным
датированным источником, а не ещё одной страницей guide.

## Исправления после независимого ревью

Socket recipe явно задаёт длину payload **в байтах**, `BINARY` и последующее
декодирование; текстовый `read(n)` не получает UTF-8 byte count как число символов.
XMP writer сначала открывает собственную staging-копию с `OPEN_FOR_UPDATE`.
Описание `script` ограничено debugger `launch`; `attach` сам код не запускает.

Canonical global localization property — `$.localize`. Одиночное
`$.localization` в ScriptUI source противоречит подробному `$` reference и
localization guide; оно не объявлено alias. Исправлены и глава, и ledger.

Other retained source gaps include malformed ExternalObject signatures and
`unload`/`terminate`, XMP argument/constant/return discrepancies, unsupported
ScriptUI discoveries, missing modern host guarantees and historical debugger
statements. Recipes use the unambiguous contract or name the unresolved boundary.

## Проверки

Exact73-page set/hash/blob/size/line checks passed. Strict JSON debugger config
parses. Independent source and integration reviews completed; the four corrections
above were applied. Local checks passed:13 inventory tests (including5 native/
runtime public-guide tests),3 scripting-ledger tests,11 consistency tests and16
source-extracted file-example cases. The130-core checker, generated source-table
freshness and whitespace checks passed. Python3.12.14 / Node24.19.0. Negative
consistency fixtures intentionally report stale generated files.

Strict MkDocs completed in5.21 seconds after two cross-platform anchor mismatches
were corrected with explicit ASCII IDs. The rebuilt site reports no unresolved
anchor from this block. These are documentation/control-flow checks, not real
File/Folder, network, library, XML/XMP, debugger or AE execution.

Inventory reproduction, using the repository's documentation environment:

```sh
python scripts/audit_public_guide_inventory.py --profile extendscript --output extendscript-runtime-inventory-2026-10-08.json
python -m unittest discover -s scripts -p 'test_public_guide_inventory.py' -v
python -m unittest discover -s tests/consistency -v
node scripts/test_document_file_examples.js
python scripts/build_docs.py --check
mkdocs build --strict
```

The inventory command accepts the same exact-tree/raw-cache options as the
[native review](NATIVE-PUBLIC-GUIDE-REVIEW-2026-10-08.md). Source page counts,
portable control-flow checks and host execution remain different evidence levels.
