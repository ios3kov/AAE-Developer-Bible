# Завершение дополнения по доступным источникам

Дата: **2026-10-08**. Parent последнего source-блока:
`065df27eb0687cc71843d9d71fc2ff599a4b9392`.

Редакционная очередь по перечисленным опубликованным источникам завершена.
В книге **130 core страниц**; отдельные research/evidence приложения сохраняют
собственные границы. Исторический freeze edition1.1 от2026-10-07 остаётся записью
того времени. Дополнение расширяет книгу и не заявляет непроведённую приёмку
всего текущего proprietary SDK/API.

## Проверенное покрытие

| Область | Фактический результат | Что означает знаменатель |
|---|---|---|
| Native public guide | [89/89 страниц](NATIVE-PUBLIC-GUIDE-REVIEW-2026-10-08.md) | Полный текст pinned guide, включая history, cross-host и navigation; не все exact SDK declarations |
| Scripting DOM | [648 заголовков](scripting-api-reviewed-2026-10-07.json):642 documented и6 research exclusions | Классификация именованных заголовков выбранного DOM inventory; не все overloads/engine features |
| Expressions | [32/32 страницы,295 headings](expression-api-reviewed-2026-10-08.json) | Полное чтение pinned expression guide, включая страницы без API headings; не вся спецификация JS |
| Match names | [8/8 страниц,757 повторяемых строк](scripting-matchnames-reviewed-2026-10-08.json) | Буквальные identifiers и их родительские маршруты; не availability каждого установленного эффекта |
| ExtendScript runtime | [73/73 страницы](EXTENDSCRIPT-RUNTIME-REVIEW-2026-10-08.md) | File/Folder, ScriptUI, BridgeTalk, runtime/data/tooling, history/navigation; не современная host support matrix |
| AE UXP host API | [44/44 страницы,1448 повторяемых строк/заголовков](uxp-api-reviewed-2026-10-08.json) | Полное чтение опубликованных host pages на pin; не1448 уникальных APIs и не отсутствующие type/async declarations |
| UXP platform workflows | [52 уникальных файла](uxp-platform-reviewed-2026-10-08.json):47 Hub и5 AE setup/site | Выбранные lifecycle/UI/files/network/storage/distribution operations; не весь shared UXP Hub |
| Host/platform | [4 официальные страницы](HOST-PLATFORM-REVIEW-2026-10-08.md) | Dated release/requirements/Advanced3D/known issues; не собственная проверка оборудования/driver/renderer |

Числа имеют разные единицы, иногда пересекающиеся источники и не складываются
в количество функций API. Source inventory и редакционный ledger раздельны:
первый задаёт точные файлы/хеши, второй связывает прочитанное с операциями и
сохранёнными ограничениями. Успешный поиск имени функции сам по себе не закрывает
её практический маршрут.

## Что теперь можно делать по книге

Native-главы объясняют lifecycle и зависимости эффекта, SmartFX/ROI/checkout,
MFR/cache, pixels/Drawbot, AEGP project/render/monitor/audio, AEIO media/output и
Artisan query boundaries. Compatibility и distribution различают AE, PPro,
смешанные suite generations и исторические sample routes.

Scripting и panel-главы проводят от plain command и модели к форме, очереди,
импорту/экспорту, файлам и внешнему взаимодействию. Runtime supplement добавляет
конкретные операции с единицами, reflection, Socket framing, библиотечными
ресурсами, XML/XMP и отладкой. UXP host и platform контракты отделены от JSX/CEP;
совпадение имени метода не обещает перенос реализации.

Для неоднозначных исходных таблиц указан конфликт и выбран безопасный применимый
маршрут либо явная граница. Исторические и undocumented материалы не превратились
в обещание поддержки современной версией AE.

## Оставшиеся внешние зависимости

1. **Exact SDK26.5 archive/build/headers/utilities/samples.** Доступ к точной
   поставке не получен. SDK25.6 build61 остаётся проверенной native baseline;
   public26.5 guide не заменяет archive/header/toolset diff.
2. **Неопубликованные AE UXP contracts.** AE-specific setup/runtime mapping,
   constructor/enum/type exports и полный DeferredCall/error/cancel contract не
   восстановлены догадкой. Упоминание `.wait()` сохранено, но оно не заполняет
   отсутствующее описание всех async semantics.
3. **Противоречия публичных references.** Конкретные native/runtime/UXP ошибки
   перечислены рядом с операциями и в ledgers. Полный source review не превращает
   malformed signature в точное объявление и не создаёт missing vendor promise.

Эти границы перечислены в [currentness record](CURRENTNESS-REVIEW-2026-10-07.md).
Новые AE/SDK/UXP/network/library runs не являются заявленным результатом этого
редакционного дополнения. Product-specific execution/compatibility evidence
добавляется отдельно, если конкретный продукт хочет заявить такое поведение.

## Воспроизведение и публикация

Использовать pinned `requirements-docs.txt` и обычные repository checks:

```sh
python -m unittest discover -s scripts -p 'test_public_guide_inventory.py' -v
python -m unittest discover -s tests/consistency -v
node scripts/test_document_file_examples.js
python scripts/check_docs_consistency.py
python scripts/generate_sources_table.py --check
python scripts/build_docs.py
python scripts/build_docs.py --check
mkdocs build --strict
git diff --check
```

Exact source inventory reproduction описано в native и runtime reviews.
Текущие local results и уже завершённые GitHub runs фиксируются в
[VERIFICATION](VERIFICATION.md). Новая source revision — commit, впервые
добавляющий этот файл; generated-only follow-up определяется отдельно. Это
позволяет назвать containing revision без невозможного включения собственного
commit hash в его содержимое. Generated output сверяется с опубликованными bytes.

Local final checks passed:13 inventory +3 scripting-ledger +11 consistency tests
and16 source-extracted file-example cases,130-core navigation, source-table
freshness, strict MkDocs and whitespace. The source examples keep their stated
runtime limits. Two internal anchor mismatches were fixed before the successful
final build. Exact published GitHub runs are checked separately.

Окончательная публикация выполняется после checks; GitHub status относится к
точному source commit, а не автоматически ко всем будущим изменениям книги.
