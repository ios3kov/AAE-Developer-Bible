# Аудит AE Developer Bible

Дата: 2 октября 2026 года. Репозиторий: https://github.com/ios3kov/AAE-Developer-Bible. Проверенный HEAD: `da625d129a2e508e9b6f24851e3300c1a3846ffa`.

Библия имеет сильную техническую основу и широкий охват. До готовой редакции её отделяют согласование доказательств и примеров, более конкретные учебные сценарии и полноценная навигация. Главная задача — превратить уже написанную базу знаний в связный практический справочник. Требование собрать и запустить каждый демонстрационный плагин для этого не нужно.

## Объём и границы проверки

Выполнены полная инвентаризация дерева, структурный проход по всем разделам, проверка редакционных правил, статусов, источников, навигации, генератора, четырёх workflows и переносимых тестов. Углублённо проверены ключевые главы Effect/SmartFX/MFR, scripting/CEP, ownership, cookbook, foundation и связанные примеры. Это аудит репозитория и редакционной готовности; он не означает построчную независимую сертификацию всех API-утверждений во всех 204 документах.

В дереве 204 Markdown-документа без сгенерированного MASTER, около 167 тысяч слов по подсчёту whitespace-токенов. В тематических разделах 00–22 находится 191 документ. Manifest содержит 270 записей. Объём сам по себе не является оценкой качества.

SDK 25.6 build 61 в эту сессию не предоставлен и не проверялся заново. Результаты 35/35 contracts и 39/39 call-sites — сохранённые результаты прежнего аудита с указанными ограничениями. AE, native platform builds, Windows, signing и notarization в текущем аудите не запускались. Для оценки документации это допустимая граница, которую следует сохранить явно.

## Что уже сделано хорошо

- Правильное разделение Effect, AEGP, AEIO, Artisan, ScriptUI, CEP, native panels и BlitHook.
- Внятная иерархия источников и baseline SDK 25.6. Исторические suite generations отделены от текущих во многих ключевых главах.
- Подробные модели ownership, lifetime, структурной invalidation, cleanup и threading. Undo не выдаётся за автоматический rollback.
- SmartFX разделяет ROI, результат, maximum result, checkout IDs, параметры и буферы. MFR не сводится к включению флага.
- Source review сохраняет обнаруженные расхождения headers/samples вместо молчаливого копирования.
- Исследовательские кейсы отделяют private loader, project-reported результаты и общедоступные SDK-контракты.
- Тесты инструментов включают отрицательные сценарии и запреты на ложный успех. Генерация документации воспроизводится на проверенном HEAD.

## Подтверждённые проблемы

Приоритет P1 означает исправить до фиксации редакции; P2 — значимое улучшение практической полноты; P3 — сопровождение. Это редакционные приоритеты, а не шкала опасности коммерческого продукта.

### 1. Старый completion model остался в действующих главах

**P1, высокая уверенность.** `EDITORIAL-GUIDE.md` и текущий план отменяют обязательную сборку/host-QA примеров, но:

- `02-EFFECT-PLUGINS/01-ANATOMY.md:119` требует сборку Minimal Gain и gates этапа 5;
- `02-EFFECT-PLUGINS/03-SMARTFX.md:110` называет host-готовность SmartFX Copy незакрытым этапом 5;
- `02-EFFECT-PLUGINS/04-MFR-THREAD-SAFETY.md:204` ссылается на прежние обязательства плана;
- `08-MACOS/01-XCODE-SETUP.md:137` оставляет full host-cycle acceptance открытым без ясного разграничения;
- `22-PROJECT-CASE-STUDIES/README.md:7,111` сохраняет старые этапы/Gates и host-gates Bible.

Читатель получает два разных определения готовности книги. Исправление: в действующих инструкциях заменить старые обязанности книги на рекомендации проверки продукта; исторические записи сохранить с датой и отметкой superseded. Не удалять честные NOT_RUN из исторического evidence.

### 2. CEP-протокол расходится между главой и шаблоном

**P1, высокая уверенность, воспроизведено без AE.** В `15-COMMUNICATION/06-CEP-TO-EXTENDSCRIPT.md:54` поле версии называется `version`; в `16-WORKING-TEMPLATES/cep-panel-bridge/host/index.jsx:17` ожидается `protocol`. Команды и payload также различаются: глава показывает `renameSelectedLayer/name`, шаблон — `renameSelected/prefix`.

Разные независимые иллюстрации допустимы, но README шаблона прямо заявляет совпадение schema с communication chapter, а `VERIFICATION.md` утверждает, что именно это расхождение уже исправлено. Передача запроса с `version` в шаблон воспроизводимо возвращает `UNSUPPORTED_VERSION`.

Исправление: один канонический учебный протокол либо явное объяснение разных независимых примеров. Все утверждения о выполненном согласовании должны соответствовать фактическому тексту.

### 3. CEP-пример не соблюдает описанную обработку ошибок

**P1, высокая уверенность, воспроизведено без AE.**

- В главе `15-COMMUNICATION/06-CEP-TO-EXTENDSCRIPT.md:96` `JSON.parse(raw)` стоит перед `try`. Неверный JSON выбрасывает исключение вместо error envelope. Версия запроса в этом фрагменте не проверяется.
- Шаблон host dispatcher возвращает `JSON_UNAVAILABLE` с `requestId:null` (`host/index.jsx:7`). UI отбрасывает его как stale response (`index.js:36`), и пользователь не видит bootstrap-ошибку.
- Отбрасывание устаревшего ответа не отменяет уже выполненную mutation. Повторные нажатия rename могут несколько раз добавить prefix; эта граница недостаточно объяснена рядом с примером.

Исправление: определить bootstrap/transport/protocol/domain errors, проверять parse и schema, показывать ошибку текущего callback даже без валидного host request ID по явно заданной политике, документировать порядок mutating commands и повторное выполнение. Добавить небольшие реальные contract tests именно этих отказов.

### 4. Историческая компиляция приписана текущим исходникам

**P1, высокая уверенность.** `17-NATIVE-SUITE-COOKBOOK/VERIFICATION.md:5,36` утверждает, что все шесть recipes и current source syntax/type-checked. `17-NATIVE-SUITE-COOKBOOK/code/README.md` уже корректно ограничивает compiler evidence прежним снимком. После него менялись EffectSuite и render-queue source.

Исправление: указать дату, исходный SHA/хэши проверенных файлов и историческую область compiler evidence; текущие source examples обозначить своим действительным уровнем доказательности. Новая компиляция нужна только для нового заявления о компиляции, а не как условие готовности книги.

### 5. Строгая сборка не обеспечивает полноту навигации

**P1, высокая уверенность.** Из 191 тематического Markdown-документа 41 не указан прямо в `mkdocs.yml`. Среди них `08-AUXILIARY-CHANNELS.md`, `09-CUSTOM-UI-DRAWBOT.md`, SDK source-review главы и все 11 вложенных reference guides. Часть доступна через внутренние ссылки и поиск; отсутствие в меню не означает полную недоступность.

`validation.nav.omitted_files: info` позволяет строгой сборке пройти. Не каждый omitted historical/generated file следует добавлять в меню: требуется явная классификация core/reference/research/archive. `NAVIGATION.md`, MkDocs nav и вводные README нужно согласовать. В decision tree направления показаны преимущественно как code-пути, а не переходы.

### 6. Локальный portable test падает на macOS

**P2, высокая уверенность.** Из 78 Python-тестов `scripts/test_*.py` один падает: `test_sdk_header_manifest_is_deterministic_and_sensitive`. `sdk_header_manifest()` разрешает реальные пути файлов, но в `relative_to(examples)` передаёт неканонический корень (`scripts/check_native.py:69,75`). На macOS `/var/...` и `/private/var/...` относятся к одному месту, но не равны как строки путей.

С `TMPDIR=/private/tmp` тот же тест проходит. CLI предварительно делает `examples.resolve()`; выявленный отказ относится к helper/test-пути и переносимости набора проверок, а не доказывает отказ обычного CLI. Исправление: канонизация корня в самом helper и проверка alias-path случая.

### 7. CI проверяет пересборку, но не запрещает stale generated files

**P2, высокая уверенность.** Validate сначала перезаписывает MASTER/MANIFEST, затем собирает docs. Он не вызывает `build_docs.py --check` до изменения файлов и не проверяет resulting diff. Поэтому сборка подтверждает генерируемость, но сама по себе не совпадение committed generated files с исходниками.

На текущем HEAD совпадение подтверждено отдельно. Regenerate docs пишет в main, повторяет попытки от latest main и имеет concurrency — это оправданный механизм, а не автоматически дефект. В последних 10 публичных runs Validate успешно завершён для source-parent `3fd9a3e`; отдельного Validate для generated commit `da625d1` в этой выборке нет. Между ними изменены только MASTER/MANIFEST. Не переносить статус CI на другой SHA без указания этой границы.

Исправление: два явно различимых результата — source validation и generated consistency. Публикация generated edition должна быть связана с конкретным проверенным source SHA. Не превращать допустимый промежуток до bot-regeneration в ложное падение всех source PR.

### 8. Практические главы неодинаково конкретны

**P2, редакционная оценка.** Native ownership/cookbook сильнее, чем scripting, panel bootstrap и некоторые platform recipes. Например, CEP chapter показывает layout, но не минимальный согласованный `manifest.xml`, bootstrap, JSON/polyfill dependency и точный путь диагностики первого запуска. Object-model глава объясняет хорошие границы, но даёт мало законченных операций с keyframes/import/render queue.

Первый эффект описан как правильная последовательность фаз, однако читателю приходится самостоятельно собирать таблицу конкретных изменений source/PiPL/metadata и связывать её с Minimal Gain. macOS debugging значительно короче Windows debugging и опирается на version-sensitive рекомендации.

Критерий исправления — не увеличение числа слов, а воспроизводимый учебный сценарий: вход → подготовка → вызовы → владение → отказ → ожидаемый результат → связанные файлы.

### 9. Ряд сложных тем только упомянут

**P2, предложения по покрытию, не утверждения о дефектах API.** Нужен отдельный цельный материал об arbitrary data и эволюции сохранённых данных эффекта; о пространстве/времени Effect inputs, temporal checkout, ROI для фильтра с соседями; о scripting keyframes/ease/expressions, File/Folder и Unicode; о bounded async frame requests, завершении и cancellation в Custom UI.

GPU, audio и Drawbot честно сохраняют ограничения, но многие операции описаны на уровне схемы. Их можно дополнить exact source maps, небольшими source examples или маркированным псевдокодом без выдуманных runtime guarantees. Там, где contract не установлен, конкретность не должна достигаться угадыванием.

### 10. Provenance не одинаково удобно проверять

**P2, высокая уверенность в структуре, полнота внешних фактов проверена частично.** SDK records содержат файлы, hashes и line ranges. Многие scripting/platform главы ссылаются на “current guide” без локальной связи с датированным источником. Центральный SOURCES существует, но читателю сложно сопоставить отдельное утверждение с конкретной страницей и границей версии.

Основной CEP/UXP roadmap перепроверен по официальному Adobe announcement: план AE beta к ноябрю 2026, AE CEP milestone декабря 2028 и общий переход конца 2029 согласуются с источником. Это planning facts, а не подтверждённый AE UXP API. Adobe CEP 12 cookbook подтверждает AEFT и отдельные host/runtime versions. Полная перепроверка Apple/Microsoft/debugger/ARM64 claims в эту сессию не выполнена; доступ к содержательному тексту Apple notarization page через использованный web-reader оказался ограничен.

Источники: [Adobe UXP announcement](https://blog.developer.adobe.com/en/publish/2026/09/investing-in-the-future-of-creative-cloud-extensibility-uxp-comes-to-our-flagship-applications), [официальный CEP 12 cookbook](https://github.com/Adobe-CEP/CEP-Resources/blob/master/CEP_12.x/Documentation/CEP%2012%20HTML%20Extension%20Cookbook.md), [Microsoft SignTool](https://learn.microsoft.com/en-us/windows/win32/seccrypto/signtool).

### 11. Условия переиспользования собственных примеров не определены явно

**P2, структурный факт.** В checkout нет LICENSE. NOTICE описывает независимость проекта и права Adobe, но не задаёт условия использования собственного текста и authored snippets. Для справочника с reusable templates это практически значимая неопределённость.

Предложение: владелец выбирает условия для текста и собственного кода; отдельно сохраняются vendor licenses/provenance. Аудит не выбирает лицензию за владельца и не даёт юридического заключения.

### 12. Hardened CI и языковая редактура

**P3.** Статический scanner отметил 10 action references без full SHA и четыре checkout со стандартным сохранением credentials. Это задачи усиления supply chain, не доказательство эксплуатации. Для read-only jobs можно явно ограничить permissions и отключить сохранение Git credentials; для regeneration authenticated Git необходим.

Scanner-кандидат «auth route без rate limit» в `acx_channel_gate.py:282` ложный: это offline argparse CLI, а не HTTP endpoint. `contents:write` у regeneration оправдан его задачей.

Основной язык принят русским, однако многие новые разделы написаны английской прозой. GLOSSARY краткий, отсутствуют многие термины ownership/receipt/ROI/timebase. Нужна единая редактура, которая оставляет API names точными и устраняет повторяющиеся общие предупреждения там, где достаточно ссылки на каноническую главу.

## Карта полноты

| Направление | Оценка по прочитанным материалам | Работа до редакции |
|---|---|---|
| 00–01 выбор и архитектура | Сильная основа | Маршруты новичок/Effect/automation; canonical state/version tables |
| 02 Effect | Сильные базовые контракты | Старые gates; arbitrary data; temporal/spatial recipes; concrete GPU/UI/audio paths |
| 03 AEGP | Хорошая основа | Несколько сквозных commands и lifecycle/error source maps |
| 04–05 AEIO и Artisan | Подробные обзоры | Согласовать уровни overview/deep/reference; bounded source walkthrough |
| 06 scripting | Хорошие правила, мало операций | Keyframes, import/render queue, text/masks, files, expression rigs |
| 07 panels | Хорошая архитектура | Полный CEP bootstrap; согласованный протокол; transport failures |
| 08–09 platforms | Хорошие workflows | Конкретные build/resource/debug recipes; source refresh; одинаковая глубина |
| 10–13 testing, release, recipes, templates | Сильная методология | Один заполненный сквозной пример вместо только пустых форм; reader-product wording |
| 14–15 integrations/communication | Детально, есть дублирование | Canonical ownership/flow links и устранение CEP contradictions |
| 16–20 source/reference/SDK | Полезная основа | Навигация; exact evidence identity; chapter/example contract checks |
| 21–22 исследования | Хорошая дисциплина границ | Убрать obsolete completion dependencies; развивать независимо |

## Выполненные проверки

| Проверка | Результат | Граница вывода |
|---|---|---|
| `build_docs.py --check` | PASS | Committed MASTER/MANIFEST совпадают с генератором |
| Независимые SHA-256, 270 manifest rows | PASS, 0 mismatches | Совпадение файлов с manifest |
| Генерация и `mkdocs build --strict` | PASS | Навигационные omissions разрешены как INFO |
| Python `scripts/test_*.py` | FAIL, 78 tests, 1 error | 77 без ошибки; macOS alias-path defect |
| Повтор одного падавшего теста с canonical TMPDIR | PASS | Подтверждает конкретную причину, не заменяет исходный FAIL |
| SDK inventory/validation fixtures | PASS, 17 tests | Synthetic fixtures, не новый real SDK audit |
| JSX depth portable suite | PASS, 13 tests | Без AE |
| JSX edge/export portable suite | PASS, 22 tests | Без Adobe renderer |
| Withdrawn Mega entry point | PASS | Запрещённые побочные действия не выполняются |
| Protocol C++ headers | PASS | Portable compile/run |
| Foundation C++ stub tests | PASS | Stub behavior, не real SDK/host |
| macOS runner shell syntax | PASS | Только shell syntax |
| PowerShell parser | NOT_RUN | `pwsh` отсутствует |
| CEP three failure reproductions | CONFIRMED | Node VM с заглушками, AE не используется |
| Static code audit | REVIEW_REQUIRED | Confirmed CI hardening + один false positive |
| GitHub Validate | PASS на `3fd9a3e` | Source-parent; generated HEAD отдельно проверен локально |
| Новая SDK/native/AE/signing matrix | NOT_RUN | Не требуется для редакционного аудита |

Последний просмотренный Validate: https://github.com/ios3kov/AAE-Developer-Bible/actions/runs/36885767413. Regeneration: https://github.com/ios3kov/AAE-Developer-Bible/actions/runs/36885767510.

## Решение

Фиксировать завершённую редакцию пока рано: есть подтверждённые противоречия между правилами, главами, примерами и evidence. База достаточно развита, чтобы завершать её последовательными редакционными блоками без переписывания с нуля.

Сначала закрыть findings 1–5, затем наполнить практические маршруты, выровнять provenance и завершить freeze. Дополнительные SDK/runtime эксперименты нужны только для спорных утверждений, которые нельзя честно изложить на существующем уровне доказательности.

Исходники и tracking documents репозитория не изменены. Локальные generated docs/site созданы в игнорируемых каталогах; рабочее дерево Git после проверок чистое. Подробный следующий порядок работ дан в [плане завершения](COMPLETION-PLAN.md).
