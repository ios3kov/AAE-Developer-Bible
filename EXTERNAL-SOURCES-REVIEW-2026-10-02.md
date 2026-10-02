# Проверка внешних источников — 2026-10-02

Цель — выбрать полезные дополнения к Bible, проверив происхождение, версии и конкретные утверждения. Это targeted source review: проверены metadata/coverage и выбранные API-разделы, а не каждая строка четырёх коллекций. Наличие source link или заявления о полноте не заменяет проверку контракта.

## Закреплённые снимки

| Источник | Проверенный снимок | Что прочитано | Решение |
|---|---|---|---|
| [After Effects SDK Knowledge Base](https://github.com/pushREC/after-effects-sdk-kb/tree/0a0fa05ba9d229344986e15cd15968c42640cc90) | `0a0fa05ba9d229344986e15cd15968c42640cc90` | README, source registry, gap analysis; suite/version matrix; Compute Cache signatures; scripting/UXP metadata | Вторичный указатель на темы; его current-version таблицу не переносить |
| [C++ SDK Guide](https://github.com/docsforadobe/after-effects-plugin-guide/tree/6d9b285d9755d1fbf8ead7680ba49de24f94b547) | `6d9b285d9755d1fbf8ead7680ba49de24f94b547` | Ownership notice; Compute Cache; compatibility; выбранные suite headings | Использовать для объяснения, ABI сверять с exact target SDK |
| [Scripting Guide](https://github.com/docsforadobe/after-effects-scripting-guide/tree/7137a990db4bd8dc9f5869b8ca431c7dfed52bdc) | `7137a990db4bd8dc9f5869b8ca431c7dfed52bdc` | Ownership notice; PropertyGroup/PropertyBase; ImportOptions; changelog | Использовать по отдельным member/version границам, сохранять undocumented warnings |
| [Adobe CEP Resources](https://github.com/Adobe-CEP/CEP-Resources/tree/ab5e4e3e53a42fad08e1225a22a991bb1ffe73f6) | `ab5e4e3e53a42fad08e1225a22a991bb1ffe73f6` | README; CEP 12 Cookbook: host matrix, manifest, libraries, JSX loading/main thread | Официальная опора для CEP shell/bridge; старые примеры требуют target-specific настройки |

C++ и scripting repo snapshots включают обновления по 26.5 от 2026-09-10; CEP snapshot — от 2026-02-20. Дата последнего коммита не означает, что каждая страница обновлена или каждый пример выполнен.

## Почему KB нельзя принять за готовый API reference

[Матрица KB](https://github.com/pushREC/after-effects-sdk-kb/blob/0a0fa05ba9d229344986e15cd15968c42640cc90/wave-3/02-aegp-suite-versions.md) представляет следующие значения как текущие для 25.6. Сравнение с уже сохранёнными exact-SDK records Bible даёт расхождения:

| Контракт | В KB | Supplied SDK 25.6 build 61 |
|---|---|---|
| Effect protocol | 13.30 | 13.29 |
| Comp suite | 11 | 12 |
| Effect suite | 4 | 5 |
| Stream suite | 5 | 6 |
| Keyframe suite | 4 | 5 |
| Marker suite | 2 | 3 |

Опора сравнения: [первая SDK запись](18-SDK-HEADER-TOOLS/05-SUPPLIED-SDK-25.6.md), [exact-header audit](18-SDK-HEADER-TOOLS/17-SDK25.6-CONTRACT-AUDIT-2026-10-01.md), [streams/keyframes review](18-SDK-HEADER-TOOLS/10-STREAMS-KEYFRAMES-SDK25.6.md), [mask/text/footage review](18-SDK-HEADER-TOOLS/11-MASK-TEXT-FOOTAGE-SDK25.6.md). Это не новый запуск against SDK bytes. Старые suite generations могут быть осознанным compatibility выбором; дефект здесь — их обозначение как current baseline.

Дополнительные ограничения provenance: в 37 Markdown files найдено 36 front matters; 25 имеют unknown source marker, 31 — `verified: false`. Общий source registry сохраняет дату проверки 2025-12-27, тогда как README расширен до апреля 2026. Эти markers сами по себе не доказывают ошибочность текста, но не поддерживают blanket claim о проверенной полноте. Локального exact-header/compiler report для его current matrix в рассмотренном материале не установлено.

KB [UXP note](https://github.com/pushREC/after-effects-sdk-kb/blob/0a0fa05ba9d229344986e15cd15968c42640cc90/scripting/UXP-STATUS-NOTE.md) датирован 2026-04-19. Его вывод о неналичии официальной AE UXP страницы нельзя использовать как текущий: 2026-10-02 [страница Adobe](https://developer.adobe.com/after-effects/uxp/) и [AE API reference](https://developer.adobe.com/after-effects/uxp/after-effects-api/) доступны. Это обновление публичной документации; availability установленного host/runtime не проверена.

## Ограничения более близких к первоисточнику guides

C++ web guide одновременно содержит later `CompSuite13`/`StreamSuite7` и исторические headings `EffectSuite4`/`KeyframeSuite3`/`MarkerSuite2`. Поэтому дата обновления сайта не задаёт единую native ABI baseline. Новые declarations не приписываются supplied SDK 25.6; старые headings не отменяют найденные в нём текущие generations. Практический пример добавлен в [Header-first rules](18-SDK-HEADER-TOOLS/04-HEADER-FIRST-RULES.md).

Scripting Guide сохраняет полезные различия между документированным API и исследовательскими дополнениями. Например, [ImportOptions](https://github.com/docsforadobe/after-effects-scripting-guide/blob/7137a990db4bd8dc9f5869b8ca431c7dfed52bdc/docs/other/importoptions.md) маркирует `rangeStart`, `rangeEnd`, `isFileNameNumbered()` как officially undocumented. Их наличие в reference и успешный feature probe не превращают их в поддерживаемое обещание Adobe.

В [Project.importFile example](https://github.com/docsforadobe/after-effects-scripting-guide/blob/7137a990db4bd8dc9f5869b8ca431c7dfed52bdc/docs/general/project.md) также обнаружена недостающая закрывающая скобка. Это дефект конкретного source example, а не опровержение описанного метода. В Bible добавлен собственный helper с отдельной syntax check; исходный пример не копировался.

CEP 12 Cookbook включает образцы manifest для старых CSXS/host versions. Нельзя переносить их номера в новый extension без сверки с целевой средой. Host version, manifest schema, CEP runtime и product version — разные поля.

## Что уже добавлено в core

| Дополнение | Проверенная опора | Назначение / предел |
|---|---|---|
| Import preflight: File → ImportOptions → canImportAs → importAs → importFile | Scripting ImportOptions и Project.importFile | [Object model](06-SCRIPTING/01-OBJECT-MODEL.md); авторский SOURCE EXAMPLE, host execution NOT RUN |
| Indexed groups versus named-only properties; undocumented API policy | Scripting PropertyGroup/ImportOptions warnings | Та же глава; запрет обещать полный обход по numProperties или supported contract по feature detection |
| Три CEP слоя версий, library/bootstrap diagnostic chain | Official CEP 12 Cookbook / README | [CEP](07-PANELS/01-CEP.md); DOCUMENTED, installation/runtime не заявлены |
| Worked comparison of secondary matrix/web headings versus exact SDK | Existing SDK records + selected current web headings | [Header-first](18-SDK-HEADER-TOOLS/04-HEADER-FIRST-RULES.md); new native compile не заявлен |
| Разделение announcement, published UXP docs и actual host proof | Adobe announcement + AE UXP pages accessed 2026-10-02 | [UXP transition](07-PANELS/02-UXP-TRANSITION.md); не подтверждает beta/GA на машине читателя |

Material transferred as original explanation with direct source references; большие фрагменты текста, vendor code/libraries и SDK assets не копировались. Docs for Adobe указывают Adobe copyright; MIT compilation notice KB не принимается за разрешение на произвольное копирование его upstream materials. Выбор лицензии собственного текста Bible остаётся задачей владельца в блоке 5.

## Оставшаяся работа

Блок 5: завершить claim/source/date/version таблицу, проверить остальные критичные version-sensitive факты и получить license decision. Блок 2: согласовать CEP protocol/template, parse/bootstrap failure paths и portable regressions. Блок 10: закончить остальные automation/expression recipes. Внешний обзор не закрывает эти блоки целиком и не заменяет SDK/runtime qualification продукта.

**Evidence:** source/documentation review, preserved exact source snapshots and existing SDK records. Native compilation, script execution in AE, CEP installation, UXP host proof — **NOT RUN**.
