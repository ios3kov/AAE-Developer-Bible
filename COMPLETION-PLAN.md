# План завершения AE Developer Bible

Дата: 2 октября 2026 года. Основа: [аудит репозитория](EDITORIAL-AUDIT-2026-10-02.md) на `da625d129a2e508e9b6f24851e3300c1a3846ffa`.

Канонические правила: [EDITORIAL-GUIDE.md](EDITORIAL-GUIDE.md). Этот файл задаёт roadmap, а не отдельный rulebook. Native baseline остаётся SDK **25.6 build 61**; ранее сохранённые 35/35 contracts и 39/39 cookbook call-sites не объявляются новой проверкой текущего плана.

Цель — выпустить связную, точную и практически применимую редакцию для разработчика After Effects. Большая часть архитектурного и SDK-материала уже написана. Следует сохранить её, исправить подтверждённые несогласованности и добавить недостающие сквозные операции. Увеличение объёма и обязательная host-QA всех примеров не являются целями этого плана.

## Какой результат должен получить читатель

После чтения своего маршрута разработчик должен уметь:

1. Выбрать extension family и объяснить, почему она подходит задаче.
2. Подготовить среду и найти нужный SDK sample/API.
3. Повторить конкретную операцию по согласованным главе и source example.
4. Определить владельца каждого ресурса, срок жизни и cleanup.
5. Понимать threading, invalidation, failure и version boundaries.
6. Составить проверку своего продукта с ожидаемым результатом и правильной областью доказательств.
7. Найти источник любого критичного version-sensitive утверждения.

Для каждого core chapter в coverage tracker отмечать отдельно: полнота объяснения, практический сценарий, provenance, согласованность примеров, links. Статусы: complete / needs expansion / needs reconciliation / intentionally limited. Последний статус требует ясного объяснения, а не служит способом скрыть недописанный материал.

## Прогресс — 2026-10-02

**Блок 1: выполнен; результаты проверок — в [ledger](VERIFICATION.md#block-1-editorial-readiness-and-evidence-2026-10-02).** Устранены active legacy gates, scoped исторический compiler result, согласован FSTR rerun status. [Поглавный трекер](CHAPTER-COMPLETION-TRACKER.md) охватывает 127 core pages. Блок 2 завершён отдельной итерацией 2026-10-04; следующий блок — **3: навигация и маршруты чтения**.

Зависимости: блок 1 задаёт общий evidence язык; блоки 2–4 устраняют protocol/navigation/tooling findings; блок 5 задаёт provenance/version таблицу для практических дополнений 6–15. Маршруты блока 3 обновляются по мере появления этих дополнений. Блок 16 принимается после всех обязательных результатов 1–15 и их поглавной сверки. ElasticGridFX lessons выполняются в mapped блоках, а не отдельной необязательной копией материалов.

По дополнительному поручению пользователя выполнен [targeted external source review](EXTERNAL-SOURCES-REVIEW-2026-10-02.md) и небольшой перенос в scripting/CEP/header-first/UXP chapters. Это частичная работа блока 5 и дополнения к блокам 2/10; они не объявляются полностью завершёнными. После review была пауза. По новому поручению блок 2 завершён 2026-10-04: template/chapters согласованы, portable failures проверены. [Ledger](VERIFICATION.md#block-2-cep-protocol-and-failure-paths-2026-10-04). Блок 3 ещё не начат.

## Порядок работ

План содержит 16 логических блоков. Это рекомендуемый порядок, не обещание, что каждый блок займёт одну сессию. Слишком большой блок можно разделить по самостоятельным результатам. Каждую завершённую тему проверять и отчитывать отдельно в соответствии с EDITORIAL-GUIDE.

| Очередь | Блок | Приоритет | Основной результат |
|---|---|---|---|
| 1 | Единая редакционная готовность и evidence | P1 | Устранены старые gates и unscoped compiler claims |
| 2 | CEP protocol и failure paths | P1 | Глава, template и проверки используют один контракт |
| 3 | Навигация и маршруты чтения | P1 | Core/reference доступны через согласованные переходы |
| 4 | Проверки и генерация документации | P2 | Portable checks и source/generated identity прозрачны |
| 5 | Источники и таблица версий | P2 | Version-sensitive claims имеют проверяемую опору |
| 6 | Effect state и arbitrary data | P2 | Понятна эволюция сохраняемого состояния эффекта |
| 7 | SmartFX пространства и времени | P2 | ROI и temporal dependencies объяснены на сценариях |
| 8 | MFR, Compute Cache и GPU | P2 | Реализационные схемы согласованы с ownership и fallback |
| 9 | Custom UI и audio | P2 | Точные bounded walkthroughs без выдуманных guarantees |
| 10 | Scripting и expression rigs | P2 | Набор законченных automation recipes |
| 11 | AEGP сквозные операции | P2 | Cookbook становится понятным маршрутом команды |
| 12 | macOS от sample до пакета | P2 | Конкретный build/debug/distribution маршрут |
| 13 | Windows от sample до пакета | P2 | Такой же практический уровень с Windows resource chain |
| 14 | AEIO и Artisan walkthroughs | P2 | Обзоры связаны с exact SDK paths и callbacks |
| 15 | Проверки продукта, рецепты и templates | P2 | Заполненный учебный пример и единая evidence vocabulary |
| 16 | Финальная редактура и freeze | P1 перед выпуском | Согласованная редакция с проверенным manifest |

## 1. Единая редакционная готовность и evidence

**Файлы:** EDITORIAL-GUIDE, STATUS, COMPLETION-PLAN/CHECKLIST, VERIFICATION; Effect anatomy/SmartFX/MFR; macOS setup; cookbook VERIFICATION и code README; case studies.

Исправить действующие требования «этап 5», Gates 4–9 и host-gates Bible. Разделить текущие редакционные обязанности, рекомендации QA продукта и исторические записи. В cookbook снять приписывание прежней компиляции текущим файлам; сохранить конкретные даты и исходные identities.

Создать chapter-level tracker в существующей coverage/checklist системе: для каждой core главы записать конкретный пробел, результат и блок этого плана. STATUS должен показывать активный блок и завершённые результаты; план — зависимости; VERIFICATION — факты проверки.

**Готово, когда:** в current guidance одна definition of done; исторический evidence не изменён по смыслу; нет необъяснённых действующих ссылок на отменённые обязательства; compiler/runtime claims привязаны к своим снимкам.

## 2. CEP protocol и failure paths

**Выполнен 2026-10-04.** Канонический prefix contract, JSON/bootstrap errors, controlled parsing, outcome semantics, one-outstanding-call, timeout/late-reply policy и portable tests согласованы с главами. AE/CEP runtime — NOT RUN.

**Файлы:** `07-PANELS/01-CEP.md`, `15-COMMUNICATION/06-CEP-TO-EXTENDSCRIPT.md`, `12-RECIPES/05-HYBRID-PANEL-NATIVE.md`, `16-WORKING-TEMPLATES/cep-panel-bridge/*`, relevant VERIFICATION.

Выбрать один учебный schema: `protocol/requestId/command/payload` и единые success/error envelopes. Устранить расхождение command/payload либо явно отделить разные примеры. Перенести parse в контролируемую error boundary, проверить тип и обязательные поля. Описать bootstrap error, malformed response, unsupported protocol и command failure. Исправить скрытие `JSON_UNAVAILABLE`.

Разграничить request correlation, stale display rejection, порядок mutating commands и idempotency: отброшенный ответ не отменяет выполненное изменение. Добавить небольшой CEP manifest/bootstrap walkthrough, пути загрузки JSX и зависимость JSON/polyfill с provenance. Не притворяться, что skeleton уже является установленной extension.

**Готово, когда:** глава и template согласованы; portable tests ловят три воспроизведённых отказа, Unicode/escaping и malformed envelopes; mutating command ordering описан; runtime остаётся RUNTIME-NOT-CLAIMED без нового host record.

## 3. Навигация и маршруты чтения

**Файлы:** `mkdocs.yml`, NAVIGATION, README, decision tree, section READMEs.

Классифицировать 41 omitted thematic document: core, reference, SDK evidence, research, archive/generated. Добавить в menu Auxiliary Channels, Drawbot, reference guides и доступ к SDK source-review records; historical aliases допускается не показывать, но причина должна быть явной.

Сделать три маршрута: первый Effect; automation tool/ScriptUI/CEP; native integration/AEGP. В каждом оставить короткую последовательность «читать → повторить → проверить», без пересказа всех глав. Заменить направления в decision tree на реальные ссылки. Проверить работу маршрутов по собранным HTML и полезность search.

**Готово, когда:** каждый core/reference chapter достижим предсказуемо; NAVIGATION и site nav не расходятся; для omissions есть явные решения; новичок может пройти маршрут без угадывания файлов.

## 4. Проверки и генерация документации

**Файлы:** `scripts/check_native.py`, его tests, `scripts/build_docs.py`, workflows, requirements-docs.

Канонизировать SDK root внутри manifest helper и покрыть macOS alias-path regression. Уточнить source-validation и generated-consistency lanes. Проверка source PR может собирать generated docs во временном staging; проверка frozen/generated revision должна запрещать stale MASTER/MANIFEST. Привязать результаты bot-regeneration к source SHA, который они представляют.

Добавить целевые consistency tests: canonical CEP schema, незапланированное исчезновение core pages из nav, неподтверждённые текущие evidence labels. Не заменять редакторский review поиском ключевых слов. Зафиксировать зависимости сборки в разумной воспроизводимой форме; явно ограничить permissions, пересмотреть action pinning и сохранение checkout credentials.

**Готово, когда:** исходный macOS тест проходит без TMPDIR workaround; generated drift обнаруживается в нужном lane; правила CI не создают ложных failures во время допустимой bot-regeneration; CI и отчёт называют точные SHA.

## 5. Источники и таблица версий

**Файлы:** SOURCES, environment/version chapters, SDK records, platform source review, CEP/UXP transition, NOTICE.

Ввести компактную таблицу: claim group → exact source → review date → SDK/AE/OS boundary → evidence class. Добавить прямые source links рядом с версионными утверждениями. SDK baseline, host support, panel runtime и platform policy должны иметь разные колонки.

Предварительное сравнение C++/scripting guides, Adobe CEP и [After Effects SDK Knowledge Base](https://github.com/pushREC/after-effects-sdk-kb) выполнено в [review от 2026-10-02](EXTERNAL-SOURCES-REVIEW-2026-10-02.md). У KB выявлены current-25.6 matrix discrepancies; из проверенных первичных разделов перенесены scoped workflows. Завершить оставшуюся claim/source/version таблицу и practical-depth comparison; полный построчный audit внешних коллекций не выполнен. Позиционирование Bible должно опираться на проверяемую пользу, а не утверждение об отсутствии аналогов.

Перепроверить debugger restrictions, macOS signing/notarization и Windows ARM64 по соответствующим источникам. Announcement UXP и опубликованные AE-specific docs повторно проверены 2026-10-02; actual AE availability/runtime не установлены. Перед freeze перепроверить документы и целевую среду. Отсутствующий или неподтверждённый AE-specific contract остаётся явно ограниченным.

Вынести решение владельца о лицензии собственного текста и примеров отдельным пунктом. После решения добавить LICENSE и сохранить права vendor material. Не выбирать условия за владельца автоматически.

**Готово, когда:** для каждого критичного version-sensitive claim есть локально понятная source/identity граница; старые и later-version API не смешаны; неизвестные опубликованы явно; license decision получено либо неопределённость отмечена перед выпуском.

## 6. Effect state и arbitrary data

**Файлы:** Effect parameters, anatomy, memory/threading, compatibility, новое целевое дополнение об arbitrary data и связанный source example.

Показать выбор parameter stream / arbitrary parameter / sequence state / transient cache. Для arbitrary data разобрать только подтверждённые target-SDK callbacks, ownership, copy/compare/interpolation/flatten/unflatten по фактическому контракту. Дать пример versioned payload без сериализации pointers, runtime locks и platform-sized structs.

Связать disk IDs, изменение схемы, reset, старый проект, duplicate и unknown future version. Добавить одну согласованную таблицу изменения source, PiPL и metadata первого Effect — связать с существующим Minimal Gain.

**Готово, когда:** разработчик может выбрать хранилище и составить migration/failure policy; каждое точное API имя подтверждено; пример маркирован source example и связан с объяснением.

## 7. SmartFX пространства и времени

**Файлы:** SmartFX, pixels/color, recipes, relevant source reference.

Дополнить существующую сильную главу двумя сценариями: spatial filter с halo вокруг ROI и temporal effect с несколькими checkout IDs. Показать входной запрос, доступную область, max result, origin/downsample/pixel aspect и boundary policy на конкретных числах.

Разделить layer/comp/effect time, rational time и выбор соседних samples. Не добавлять motion-blur/time-remap гарантии без источника. Дать ownership/error sequence для pre-render snapshot и отсутствующего layer input. Проверки продукта перечислить отдельно от результатов книги.

**Готово, когда:** два сценария можно разобрать по таблице/схеме без догадок; зависимости видимы хосту; math и exact call shape не смешаны; ROI/cache/alpha объяснения не противоречат друг другу.

## 8. MFR, Compute Cache и GPU

**Файлы:** MFR, GPU, performance architecture, platform GPU guides, CPU/GPU recipe и SDK reference.

Сохранить существующую модель state/receipt. Добавить walkthrough cache key → compute → acquisition → checkin и failure/cancellation. Объяснить content identity, padding/serialization, limits и cache ownership на одном примере.

GPU walkthrough: capability → per-device setup → per-frame eligibility → actual GPU world format → render → synchronization/cleanup → teardown. Дать decision table для fallback и memory/device failures строго по подтверждённым contracts. Сопоставить source paths SDK sample с каждой стадией; оптимизация kernel не является доказательством ускорения AE.

**Готово, когда:** reader видит полный source-level маршрут, границы shared/per-device/per-frame state и тестируемую policy; backend support не выводится только из enum или наличия source branch.

## 9. Custom UI и audio

**Файлы:** Drawbot/audio chapters, `20-REFERENCE-IMPLEMENTATIONS/Effect/CustomUI-Drawbot`, SDK source review.

Для UI дополнить acquisition skeleton одним простым draw path с точной borrowed/owned resource таблицей; click/drag и coordinate conversion связать с параметром, сохраняемым в project. Async manager разобрать как жизненный цикл запроса и cancellation, если exact contracts позволяют; иначе честно дать неполную карту и неизвестные.

Для audio дать конкретный stateless processing example на разрешённом формате и contract map setup/render/setdown. DSP math отделить от неизученного host scheduling. Отсутствие bundled AUDIO_RENDER sample не компенсировать выдуманной implementation.

**Готово, когда:** draw и audio pathways конкретнее общих советов; точные operations sourced; intentionally limited области явно перечислены; никакой runtime claim не появляется без evidence.

## 10. Scripting и expression rigs

**Файлы:** `06-SCRIPTING/*`, `15-COMMUNICATION/05-SCRIPT-TO-AE.md`, JSX/ScriptUI templates, новые recipe страницы по необходимости.

Добавить законченные операции: создать comp и layers; импортировать и настроить footage; поставить keys с interpolation/ease; создать text/mask/marker; настроить render queue с reacquire после изменений; построить небольшой expression rig и проверить resolving/error state.

File/Folder, permissions, Unicode/encoding, settings persistence и scheduled chunks раскрыть отдельными короткими сценариями. Применять ES3-compatible host syntax. В каждом примере определить prerequisites, capabilities, undo boundary, structural invalidation, partial failure и expected output.

**Готово, когда:** хотя бы один полный сценарий существует для каждого заявленного базового automation workflow; все fragments согласованы с scripting guide и версии названы; UI shell отделён от operation layer.

## 11. AEGP сквозные операции

**Файлы:** `03-AEGP/*`, cookbook project/items/comp/layer/render/queue, MenuTool и foundation.

Связать существующие recipes в три walkthroughs: menu command с late target resolution; project mutation с cleanup и undo; frame request с receipt и bounded async lifetime. Подчеркнуть callback/host-safe boundary и state invalidation.

Разделить overview, exact cookbook и reusable source, чтобы один контракт не редактировался независимо в трёх местах. Старые compatible suite generations оставить с причиной и областью; optional newer API не должны переопределять baseline.

**Готово, когда:** пользовательский trigger доведён до результата и cleanup; callback exception boundaries явны; explanations и source совпадают; historical compiler evidence scoped.

## 12. macOS от sample до пакета

**Файлы:** `08-MACOS/*`, first-effect/load-debug recipes, install/signing distribution.

Написать практический маршрут exact sample → project settings → resources → universal slices → development signing → load/debug → symbol archive → release staging. Показать диагностические команды и ожидаемые виды результатов без притворных successful outputs.

Debugger instructions отдельно version-gated. Любую re-sign host процедуру ограничить development copy и объяснить её prerequisites. Distribution: inner-to-outer signing, final artifact, notary submission/log, staple where supported, clean install/rollback, existing plugin preservation.

**Готово, когда:** читатель понимает конкретные файлы/настройки и может локализовать compile/resource/load/signing failure; инструкции не требуют менять рабочую AE installation.

## 13. Windows от sample до пакета

**Файлы:** `09-WINDOWS/*`, load-debug recipes, installer/signing distribution.

Разобрать sample project и PiPL conversion/resource/link chain; include/lib paths, export, CRT/toolset, x64/ARM64 и matching dependencies. Дать команды проверки итогового artifact и диагностики load failures. Разделить architecture compile capability и фактическую host support.

Signing/installer walkthrough включает digest/timestamp/verify, Adobe path discovery, update ownership, locked file, rollback и сохранение PDB. Не обещать native ARM64 host support по успешной сборке.

**Готово, когда:** Windows маршрут столь же конкретен, как macOS, но отражает свои resource/ABI/install contracts; version-sensitive facts проверены.

## 14. AEIO и Artisan walkthroughs

**Файлы:** `04-AEIO`, `05-ARTISAN`, corresponding `14-*` главы и `16/20` guides.

Основной массив здесь уже подробный: не переписывать его целиком. Для каждой family добавить одну последовательность чтения exact SDK sample: регистрация → init → operation → partial failure/cancel → persistence → teardown. Указать где sample кончается и начинается production recommendation.

Уменьшить независимое дублирование overview/deep/reference, оставив явные обязанности страниц и links. Source maps не превращать в требование создать новый importer/renderer для выпуска книги.

**Готово, когда:** callbacks/resources traced по источникам; sample-specific shortcut не выдаётся за контракт; incomplete runtime directions честно ограничены.

## 15. Проверки продукта, рецепты и templates

**Файлы:** `10-TESTING`, `11-DISTRIBUTION`, `12-RECIPES`, `13-TEMPLATES`, source reference READMEs.

Добавить один заполненный учебный комплект: spec → compatibility matrix → correctness fixture → failure report → performance report → release notes. Учебные числа маркировать illustrative, не выдавать за выполненные тесты.

Для performance отдельно описать preparation throughput, actual render throughput, RAM Preview и displayed playback. Для correctness различать effect world, export и display/color pipeline. Метрики и tolerances задавать до измерений.

Все six existing recipes связать с конкретным example/API route. Унифицировать NOT_RUN/BLOCKED и evidence scopes, убрать ненужные повторения общих QA правил.

**Готово, когда:** templates можно заполнить по одному цельному примеру; reader понимает, что и почему проверять; книга не заявляет демонстрационный PASS вместо runtime evidence.

## 16. Финальная редактура и freeze

**Файлы:** все изменённые главы плюс README, STATUS, CHECKLIST, COVERAGE, SOURCES, NAVIGATION, CHANGELOG, MASTER/MANIFEST.

Провести cross-chapter review по tracker. Выравнять русскую объясняющую прозу, не менять API names. Расширить glossary терминами из core chapters. Проверить snippets, source references, code links, anchors, licensing/provenance и маршруты чтения.

Обновить research date и версию только после фактической проверки. Сгенерировать MASTER/MANIFEST на конкретном source SHA, проверить no-drift и strict build. Отчёт freeze должен называть source revision, generated revision при наличии отдельного bot commit, выполненные проверки и intentionally limited topics.

**Готово, когда:** все обязательные acceptance criteria ниже выполнены. Публикация выполняется в рамках отдельного разрешённого действия; этот план сам по себе её не осуществляет.

## Единая приёмка каждого блока

1. Прочитать вместе объясняющие главы, рецепты, source example и evidence records темы.
2. Закрыть конкретные противоречия и пробелы без расширения scope до нового продукта.
3. Проверить exact source для новых version-sensitive claims; неизвестное не заменять предположением.
4. Обновить tracker, STATUS, CHANGELOG и relevant VERIFICATION.
5. Выполнить generated-doc и strict-link проверки, а при исправлении поведения инструмента — целевые регрессии.
6. Зафиксировать changes согласно принятому repository workflow; сообщить block, findings, checks, точный HEAD и следующий блок.
7. Остановиться перед следующей темой, как требует EDITORIAL-GUIDE.

## Критерии готовой редакции

- Подтверждённые P1 findings аудита закрыты.
- Для каждой core главы есть результат chapter-level review; каждый applicable вопрос editorial checklist раскрыт содержательно.
- Есть сквозной маршрут первого Effect и сквозной маршрут automation/panel tool.
- Critical version-sensitive claims имеют источник, дату и версионную границу.
- Chapters/recipes/templates используют согласованные identities, protocols и ownership semantics.
- Историческая компиляция и runtime observations не приписаны текущим source snapshots.
- Core/reference навигация полна, archive/generated omissions объяснены.
- Committed MASTER/MANIFEST воспроизводимы на фиксируемой редакции; strict docs build проходит.
- Условия использования authored material определены либо нерешённый вопрос владельца явно отражён до публикации.
- Research appendices не создают скрытых обязательств завершить все built-in effects или исходные проекты.

## Что развивать после основной редакции

Reverse-engineering atlas, новые real-project case studies, host-observed examples, дополнительные SDK generations и готовые sample project bundles полезны, но развиваются отдельными версиями. Полноценный AE UXP guide добавляется после появления доступного AE-specific contract, а не по roadmap других Adobe hosts.

**Первый рекомендуемый шаг: блок 1.** Он устраняет двусмысленность цели и доказательств, после чего остальные блоки можно дописывать по одной понятной системе готовности.


## Дополнение из ElasticGridFX

Ретроспектива FSTR Stretch **0.9.3-perf.1** изучена на immutable documentation snapshot `9d0162de64d01ceb41f6a1374a73544729ed0ec2`. Shipping source `f611312bd7b76ebe5bc5f2bd8b48b44f50c0c761`, build `EGFX-6147dc406abc596e7f2d1b60` и release target — разные identities.

[План переноса с источниками, ограничениями и критериями](22-PROJECT-CASE-STUDIES/ELASTICGRIDFX-TRANSFER-PLAN-2026-10-02.md) является частью этого roadmap. Это запланированное расширение глав, не уже завершённый перенос и не новый runtime PASS.

| Блок | Что добавить из ретроспективы |
|---|---|
| 1 и 5 | Confidence, test status и принятое решение как отдельные оси; source/binary/package/loaded identity; immutable provenance |
| 6 и 7 | Сохранение параметров/анимации и legacy project; separable mapping, Bicubic rows и fallback без изменения arithmetic |
| 8 | Attribution реального plane path до оптимизации; call-local scratch; exceptional-float parity; границы MFR evidence |
| 9 | Native gesture → наблюдаемое изменение → Undo; viewer labels, preview cache и display latency как разные наблюдения |
| 11 | Render completion по полному набору decoded outputs, а не exit0; queue-chain/readback и границы async completion |
| 12 и 13 | Проверка фактически загруженного артефакта; downloaded package и reversible update; Windows переносится только после проверки своих контрактов |
| 15 | Matched-toolchain controls; независимый calibrated decode; отдельные native/export/cache-fill/playback метрики; bounded crash investigation |
| 16 | Scoped case study ElasticGridFX и согласованный freeze: документация не создаёт новый host PASS; tool adaptation остаётся отдельной задачей |

В блок 15 включить **заполненный реальными project-reported данными пример** наряду с illustrative forms: native-only ≈12.062×, ordinary AE export ≈1.3507× и screenshot-bracketed Preview intervals. У каждого значения назвать workload, representation, scope и limitations; не публиковать общий вывод «12× быстрее в AE».

После блоков 5, 8 и 15 написать отдельный ElasticGridFX case study в разделе 22 и связать его с core chapters. Независимая повторная host-QA не обязательна для такого PROJECT-REPORTED переноса. Adaptation `render_observation.py`, `live_identity.py`, `perf_fixture_runner.py` требует проверки зависимостей, лицензии, side effects и host assumptions; код инструментов сейчас не копируется.
