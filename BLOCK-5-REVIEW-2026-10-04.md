# Блок 5 — review источников и версионных границ

Дата: **2026-10-04**. База: `e0acf996133db1fb39df677e42a42cc3231a2568`; исходный post-merge реестр блока 4: `afec0755b5dc1cdcdb6d4ad467202e2715538192`. Это редакционная/source работа, не новый Adobe host или release test.

## Объём и входы

[Таблица](BLOCK-5-SOURCES.md) разделяет SDK baseline, host support, panel runtime и platform policy. Канонические данные — [claim registry](sources/claim-registry.json). SDK-группы ссылаются на retained exact-header/sample reviews; байты SDK не пересканированы в этой итерации. Даты этих записей не заменены сегодняшней датой. Отдельная таблица provenance содержит проверенные исторические регенерации Bible, а не вымышленные SDK Git SHA.

Это полный реестр выбранных критичных групп текущего блока, а не полный построчный аудит каждой API-страницы. Exact SDK declarations, cleanup и call shapes продолжают ссылаться на узкие диапазоны/хэши в SDK review records. Future workflows блоков 6–15 получают отдельные claim/source пары по мере наполнения.

## Перепроверка платформы и roadmap

| Группа | Прямой источник, прочитанный 2026-10-04 | Вывод / граница |
|---|---|---|
| macOS debugger attach | [SDK Guide](https://ae-plugins.docsforadobe.dev/intro/debugging-ae-macos/) | В guide раздельно описаны non-Beta 26.5+ development copy и Beta 2027+ developer mode. Это later-version documentation; не переносить на 25.6 и не заявлять installed build/attach PASS. |
| Windows ARM64 effect | [SDK Guide](https://ae-plugins.docsforadobe.dev/intro/windows-on-arm-support/) и [Microsoft](https://learn.microsoft.com/en-us/windows/arm/add-arm-support) | ARM64 target/entry declaration и dependency chain относятся к сборке; native host qualification отдельна. Guide указывает VS 17.4+; Microsoft различает native и cross-compilation prerequisites. |
| AE Windows on Arm | [Adobe requirements](https://helpx.adobe.com/after-effects/desktop/get-started/technical-requirements/system-requirements.html), page updated 2026-09-09 | Текущая страница перечисляет Snapdragon X и Windows 11 24H2 build 26100.2033. Это публичная support specification; её unversioned URL не устанавливает, что каждая прежняя AE версия поддерживала ARM64. Загрузка нашего плагина не проверена. |
| macOS Developer ID | [Apple](https://developer.apple.com/developer-id/) | Developer ID / notary ticket и cutoff altool 2023-11-01 подтверждены опубликованными требованиями; это не successful submission. |
| Notarization prerequisites | [Apple prerequisites](https://developer.apple.com/documentation/security/notarizing-macos-software-before-distribution), [workflow](https://developer.apple.com/documentation/security/customizing-the-notarization-workflow), [issues](https://developer.apple.com/documentation/security/resolving-common-notarization-issues) | Проверены Hardened Runtime для app/CLI targets, secure timestamp, release entitlement boundary, log/stapling workflow. Host entitlements не объявляются универсальным рецептом для каждого plug-in. |
| Windows signature | [SignTool](https://learn.microsoft.com/en-us/windows/win32/seccrypto/signtool) | /fd и /td описаны для file/timestamp digests; SHA256 рекомендован. Command documentation не означает подпись и verify конкретного продукта. |
| CEP → UXP | [Adobe announcement 2026-09-24](https://blog.developer.adobe.com/en/publish/2026/09/investing-in-the-future-of-creative-cloud-extensibility-uxp-comes-to-our-flagship-applications) | AE beta by November 2026 остаётся датированным планом; runtime availability не установлена. |
| AE UXP docs | [AE-specific landing](https://developer.adobe.com/after-effects/uxp/) | Документация опубликована, отделяет shared UXP от host APIs и содержит beta expansion note. Это не проверка установленного host/API. |

Apple HTML documentation endpoints возвращали JavaScript shell, а Markdown ссылки не открывались инструментом. Полный основной текст трёх страниц прочитан из официальных DocC JSON `https://developer.apple.com/tutorials/data/documentation/<path>.json` (`primaryContentSections`, включая text/code/reference элементы). Developer ID HTML прочитан отдельно. Эта техническая fallback-процедура не считается выполнением signing/notarization.

## Практическая глубина: что заимствуем и что дописываем

Сравнение ограничено выбранными маршрутами и закреплёнными snapshots [предыдущего review](EXTERNAL-SOURCES-REVIEW-2026-10-02.md); не объявляет всю коллекцию валидной и не измеряет преимущество по количеству строк.

| Материал / выбранный маршрут | Что даёт источник | Что уже есть в Bible | Содержательная следующая работа |
|---|---|---|---|
| C++ Guide — Compute Cache | Callback/function reference, class registration, key и value lifecycle | [Memory/MFR](01-ARCHITECTURE/02-MEMORY-THREADING-ERRORS.md), exact [SDK record](18-SDK-HEADER-TOOLS/07-MEMORY-MFR-SDK25.6.md), архитектурные recipes | В блоке 8 связать key → compute → receipt → checkin в walkthrough с cancellation/failure. Сигнатуры брать из SDK 25.6, не из later web headings. |
| C++ Guide — SmartFX | Requests/rectangles, checkout и rendering contract | [SmartFX](02-EFFECT-PLUGINS/03-SMARTFX.md) и sample-source review | Блок 7: числовые spatial/temporal примеры, halo/ROI и sample-time boundaries. Документированный checkout не означает host test примера. |
| Scripting Guide — ImportOptions / PropertyGroup | Конкретные member rules и invalidation при addProperty; предупреждения undocumented fields | [Object model](06-SCRIPTING/01-OBJECT-MODEL.md), bounded import preflight и portable syntax boundary | Блок 10: законченные comp/layers/keys/text/render-queue сценарии. Не копировать malformed upstream import example или обещать supported rangeStart/rangeEnd. |
| CEP Resources — manifest / evalScript | Host/runtime fields, engine separation и shell/bridge mechanisms | [CEP](07-PANELS/01-CEP.md), согласованный [bridge](15-COMMUNICATION/06-CEP-TO-EXTENDSCRIPT.md), portable regressions блока 2 | Использовать documented bootstrap, но значения manifest подбирать по целевой среде. Установка extension внутри AE остаётся отдельной продуктовой проверкой. |
| Secondary KB — SmartFX / suite matrix | Широкая карта тем и reference summaries | Exact 25.6 source records, явные source/version/evidence boundaries | Выбирать темы для блоков 6–11; не переносить несовпадающую «current 25.6» matrix. Сам объём KB не доказывает correctness или runtime qualification. |
| ElasticGridFX retrospective | Case-specific cache/performance/process observations | [Transfer plan](22-PROJECT-CASE-STUDIES/ELASTICGRIDFX-TRANSFER-PLAN-2026-10-02.md) и provenance | Применять bounded lessons в блоках 7–8 и 12–15; reported performance не превращать в гарантию SDK/AE. |

Проверяемая польза Bible — связанные объяснение, source example, failure/cleanup и маршрут чтения. Утверждение, что аналогов нет, не используется. Авторские walkthroughs дописываются по плану; этот review не закрывает их заранее.

## Лицензионное решение

Владелец **2026-10-04** выбрал: «Пока оставить лицензию неопределённой и отметить это перед выпуском». LICENSE с MIT/CC условиями не добавляется. Это зафиксированная неопределённость, которую нужно разрешить перед edition freeze/public release в блоке 16. Vendor SDK, samples, docs и trademarks сохраняют свои условия; лицензия чужой компиляции не даёт разрешения на произвольное копирование upstream material. См. [NOTICE](NOTICE.md).

## Генерация и CI

`python3 scripts/generate_sources_table.py` детерминированно отображает reviewed JSON; `--check` отклоняет drift. Validation проверяет обязательные границы, dates, evidence classes, полные SHA/digest и существование review records. Она не устанавливает истинность prose, внешнюю доступность URL или Adobe runtime support.

CI проверяет таблицу до staging MASTER/MANIFEST. Source registry меняется через редакторское review; bot-regeneration не подменяет review и не добавляет строку о своём собственном generated SHA в source input. Новые фактические run identities доступны в workflow summary/packet; принятую историческую запись можно добавить следующим независимым source commit.

Compile, signing, notarization, ARM64 host, AE/CEP/UXP runtime: **NOT RUN**. Ни один такой статус не обновляется по green documentation CI.
