# Поглавный трекер завершения

Обновлено: **2026-10-07**. План: [16 логических блоков](COMPLETION-PLAN.md). Правила: [EDITORIAL-GUIDE](EDITORIAL-GUIDE.md); существующий source/evidence baseline — [coverage matrix](FINAL-COVERAGE-AUDIT.md).

## Дополнения 2026-10-07 — reconciliation queue

Ниже сохранены исходные задачи аудита; строки без C **не означают отсутствие уже
добавленного текста**. До freeze каждому затронутому row требуется отдельный
cross-page review. Добавления и результаты:

- [№6](BLOCK-6-REVIEW-2026-10-07.md): lifecycle/arbitrary codec/migration реализованы,
  C++ portable test PASS; SDK callback adapter намеренно не заявлен.
- [№7](BLOCK-7-REVIEW-2026-10-07.md): spatial/temporal math и calibration; auxiliary
  dimensions/checkin связаны с маршрутом, не равны RGBA ROI.
- [№8](BLOCK-8-REVIEW-2026-10-07.md): cache/GPU routes +
  [bounded incident](22-PROJECT-CASE-STUDIES/ELASTICGRIDFX-PERFORMANCE-SCOPE-2026-10-07.md).
- [№9](BLOCK-9-REVIEW-2026-10-07.md): sample-backed draw и bounded audio/async UI.
- [№10](BLOCK-10-REVIEW-2026-10-07.md): authored JSX rig + automation operation map.
- [№11](BLOCK-11-REVIEW-2026-10-07.md): три AEGP chains; exact per-recipe review остаётся.
- [№12/13](BLOCK-12-13-REVIEW-2026-10-07.md): concrete sample/build/sign/rollback routes;
  per-platform version-sensitive rereview и individual links остаются.
- [№14](BLOCK-14-REVIEW-2026-10-07.md): exact IO/Artie callbacks; no codec/renderer runtime.
- [№15](BLOCK-15-REVIEW-2026-10-07.md): worked evidence pack + primary-record performance
  scope; template/recipe linking и final wording sweep остаются.

Общая сборка документации/регрессии не закрывают автоматически 127 technical rows.

## Block 5 source handoff — 2026-10-04

[Claim/source boundaries](BLOCK-5-SOURCES.md) и [source review](BLOCK-5-REVIEW-2026-10-04.md) завершены в редакционной области: retained SDK records, fresh platform/roadmap review и selected practical-depth comparison. Это не закрывает все оси 127 core rows: содержательные expansion/reconciliation задачи блоков 6–15 остаются. Новые APIs/workflows получают отдельные scoped source records. Лицензия отложена владельцем до freeze; runtime не заявлен.

## Что здесь учитывается

Это рабочая очередь для **127 core pages**: Markdown непосредственно в разделах 00–15, 17 и 19, включая их обзорные README. Dated source reviews, verification ledgers, вложенные source/reference guides и исследовательские приложения учитываются отдельно ниже. Каждый core page включён ровно один раз.

Строки задают конкретный оставшийся результат по аудиту и плану. Это не новая полная техническая сертификация каждой главы и не отмена прежних source reviews. `R` может обозначать запланированную сверку, а не уже обнаруженную ошибку. Сам факт наличия текста, большого объёма или зелёной CI не закрывает строку.

Пять независимых осей: **Т** — полнота объяснения; **С** — практический сценарий; **И** — provenance/version boundary; **П** — согласованность source example/recipe; **Л** — ссылки и маршрут чтения.

| Код | Статус | Когда ставить |
|---|---|---|
| C | complete | Применимые критерии оси проверены; есть dated block/evidence record |
| E | needs expansion | В указанном блоке нужно добавить конкретное объяснение или сценарий |
| R | needs reconciliation | Нужно сверить с связанными главами, source examples, источниками или routes |
| L | intentionally limited | Ограничение явно названо; standalone code/runtime walkthrough не обещан для этой оси |

Создание трекера само по себе не закрывает главы. Текущий результат определяется
пятью статусами каждой строки и её review record: строки с пятью `C` уже прошли
поглавную сверку; остальные остаются в очереди по незакрытым осям. `L` в обзоре
означает, что это route/index, а не самостоятельная реализация. Для UXP, BlitHook
и catalogue/errata предел отдельно указан в строке. Source handoff блока 5
выполнен; для новых дополнений сохраняется отдельная provenance-сверка. Ось ссылок
закрыта блоком 3 и повторно проверяется после изменений. Столбец «Результат / блок»
указывает ведущую содержательную работу, а не все зависимости.

## Выполнено в блоке 3

Ось **Л** закрыта для 127 core pages: все HTML-страницы достижимы через меню/индексы, локальные ссылки и якоря проверены. Дополнительно проверены 26 reference pages; общий охват 153 страницы и 498 ссылок/якорей. Это навигационная сверка, не закрытие остальных содержательных осей. [Реестр](NAVIGATION-AUDIT.md).

## Выполнено в блоке 1

Согласованы текущие evidence labels в Effect anatomy/SmartFX/MFR, macOS setup, Cookbook и связанных reference guides; снято приписывание исторического compiler PASS нынешнему коду. Dated SDK reviews и reuse audit получили пояснения исторического процесса. Эти исправления закрывают findings блока 1, но не практические дополнения строк ниже.

В следующих блоках обновлять оси каждой затронутой строки отдельно. Для полного закрытия строки все применимые оси должны стать C или обоснованным L, а результат — ссылаться на dated verification entry. Блок 16 проверяет весь набор перед freeze.

## Частичные дополнения после внешнего review

[Targeted review](EXTERNAL-SOURCES-REVIEW-2026-10-02.md) добавил import preflight/provenance в Object model, manifest/library/bootstrap diagnostic steps в CEP, published-docs boundary в UXP и worked native-source comparison в Header-first. Соответствующие главы сохраняют E/R для остальных practical/version/recipe результатов. После паузы блок 2 завершён 2026-10-04; остальные блоки не объявляются завершёнными.

## 00-START-HERE

| Глава | Т | С | И | П | Л | Оставшийся результат / блок |
|---|---|---|---|---|---|---|
| [Decision tree — что именно вы разрабатываете?](00-START-HERE/00-DECISION-TREE.md) | E | E | R | R | C | Навигация и маршрут проверены; **№3 выполнен**. Остальные редакционные оси остаются R/L; итоговая сверка — **№16**. |
| [Extension types](00-START-HERE/01-EXTENSION-TYPES.md) | R | E | R | R | C | Навигация и маршрут проверены; **№3 выполнен**. Остальные редакционные оси остаются R/L; итоговая сверка — **№16**. |
| [Environment matrix](00-START-HERE/02-ENVIRONMENT-MATRIX.md) | R | R | R | R | C | Разнести SDK, AE build, suite generation и OS/architecture; датировать ограничения. **№5** |

## 01-ARCHITECTURE

| Глава | Т | С | И | П | Л | Оставшийся результат / блок |
|---|---|---|---|---|---|---|
| [Native plug-in lifecycle](01-ARCHITECTURE/01-LIFECYCLE.md) | C | C | C | C | C | Recovery/partial failure связан с versioned codec; [review](CHAPTER-RECONCILIATION-2026-10-07.md). |
| [Память, время жизни ресурсов и ошибки](01-ARCHITECTURE/02-MEMORY-THREADING-ERRORS.md) | C | C | C | C | C | Receipt/error cleanup и incident limits согласованы; [review](CHAPTER-RECONCILIATION-2026-10-07.md). |
| [PiPL, регистрация и загрузка плагина](01-ARCHITECTURE/03-PIPL-AND-LOADING.md) | R | E | R | R | C | Связать PiPL/resource chain с конкретными macOS/Windows sample walkthroughs. **№13** |
| [Version compatibility](01-ARCHITECTURE/04-VERSION-COMPATIBILITY.md) | R | E | R | R | C | Добавить читаемую таблицу SDK/AE/suite/architecture и сценарий отказа при несовместимости. **№5** |
| [Performance architecture](01-ARCHITECTURE/05-PERFORMANCE-ARCHITECTURE.md) | C | C | C | C | C | Core/export/Preview и observed overlap разделены; [review](CHAPTER-RECONCILIATION-2026-10-07.md). |
| [Build system strategy](01-ARCHITECTURE/06-BUILD-SYSTEM.md) | R | E | R | R | C | Связать общие правила с конкретными resource/export/build маршрутами обеих платформ. **№13** |
| [Communication architecture](01-ARCHITECTURE/07-COMMUNICATION-ARCHITECTURE.md) | C | C | C | C | C | Envelopes, correlation и mutation ordering/idempotency согласованы. **№2 выполнен**. |

## 02-EFFECT-PLUGINS

| Глава | Т | С | И | П | Л | Оставшийся результат / блок |
|---|---|---|---|---|---|---|
| [Устройство Effect-плагина: от регистрации до кадра](02-EFFECT-PLUGINS/01-ANATOMY.md) | C | C | C | C | C | Identity/source и state route согласованы; [review](CHAPTER-RECONCILIATION-2026-10-07.md). |
| [Параметры и интерфейс Effect-плагина](02-EFFECT-PLUGINS/02-PARAMETERS-UI.md) | C | C | C | C | C | Arbitrary selectors/ownership/schema/disk IDs раскрыты; [review](CHAPTER-RECONCILIATION-2026-10-07.md). |
| [SmartFX: зависимости, области и время жизни буферов](02-EFFECT-PLUGINS/03-SMARTFX.md) | C | C | C | C | C | ROI/time math и actual Copy scope согласованы; [review](CHAPTER-RECONCILIATION-2026-10-07.md). |
| [MFR: параллельный рендер, состояние и Compute Cache](02-EFFECT-PLUGINS/04-MFR-THREAD-SAFETY.md) | C | C | C | C | C | Receipt/key/scratch/cleanup и bounded incident сверены; [review](CHAPTER-RECONCILIATION-2026-10-07.md). |
| [GPU effects](02-EFFECT-PLUGINS/05-GPU.md) | C | C | C | C | C | Metal route, device ownership и eligibility/error policy согласованы; [review](CHAPTER-RECONCILIATION-2026-10-07.md). |
| [Пиксели, цвет и прозрачность в Effect-плагине](02-EFFECT-PLUGINS/06-COLOR-PIXELS.md) | C | C | C | C | C | Calibration/exceptional floats и actual Gain truncation разделены; [review](CHAPTER-RECONCILIATION-2026-10-07.md). |
| [Audio effects](02-EFFECT-PLUGINS/07-AUDIO.md) | C | C | C | L | C | Bounded DSP arithmetic; AUDIO_RENDER wiring намеренно не обещан без matching sample; [review](CHAPTER-RECONCILIATION-2026-10-07.md). |
| [Дополнительные каналы: глубина, ID, нормали и сырые данные](02-EFFECT-PLUGINS/08-AUXILIARY-CHANNELS.md) | C | C | C | C | C | Descriptor/chunk geometry и mandatory checkin согласованы с RGBA route; [review](CHAPTER-RECONCILIATION-2026-10-07.md). |
| [Custom UI and Drawbot](02-EFFECT-PLUGINS/09-CUSTOM-UI-DRAWBOT.md) | C | C | C | C | C | Sample draw cleanup и authored gesture/async limits разделены; [review](CHAPTER-RECONCILIATION-2026-10-07.md). |
| [Effect plug-ins](02-EFFECT-PLUGINS/README.md) | R | L | R | L | C | Навигация и маршрут проверены; **№3 выполнен**. Остальные редакционные оси остаются R/L; итоговая сверка — **№16**. |

## 03-AEGP

| Глава | Т | С | И | П | Л | Оставшийся результат / блок |
|---|---|---|---|---|---|---|
| [AEGP: инициализация, hooks и suites](03-AEGP/01-HOOKS-SUITES.md) | C | C | C | C | C | Actual ping/partial registration versus command/idle/shutdown design; [review](CHAPTER-RECONCILIATION-2026-10-07.md#remaining-aegpnative-integration-closure). |
| [AEGP: операции с проектом и рендером](03-AEGP/02-PROJECT-RENDER-AUTOMATION.md) | C | C | C | C | C | Chains и фактические source/partial-cleanup limits сверены; [review](CHAPTER-RECONCILIATION-2026-10-07.md). |
| [AEGP](03-AEGP/README.md) | R | L | R | L | C | Навигация и маршрут проверены; **№3 выполнен**. Остальные редакционные оси остаются R/L; итоговая сверка — **№16**. |

## 04-AEIO

| Глава | Т | С | И | П | Л | Оставшийся результат / блок |
|---|---|---|---|---|---|---|
| [AEIO — media import/export plug-ins](04-AEIO/README.md) | C | C | C | C | C | Exact IO route, options/cleanup и sample capability mismatch; [review](CHAPTER-RECONCILIATION-2026-10-07.md). |

## 05-ARTISAN

| Глава | Т | С | И | П | Л | Оставшийся результат / блок |
|---|---|---|---|---|---|---|
| [Artisan — custom composition 3D renderer](05-ARTISAN/README.md) | C | C | C | C | C | Artie route/current suites и normalized scene/lifetime согласованы; [review](CHAPTER-RECONCILIATION-2026-10-07.md). |

## 06-SCRIPTING

| Глава | Т | С | И | П | Л | Оставшийся результат / блок |
|---|---|---|---|---|---|---|
| [After Effects scripting object model](06-SCRIPTING/01-OBJECT-MODEL.md) | C | C | C | C | C | Actual rename/import/rig versus replace design; target/partial/source limits; [review](CHAPTER-RECONCILIATION-2026-10-07.md#scripting-completion-reconciliation). |
| [ScriptUI](06-SCRIPTING/02-SCRIPTUI.md) | C | C | C | C | C | Plain-result synchronous command, dock/layout and separate deferred cancel design; [review](CHAPTER-RECONCILIATION-2026-10-07.md#scripting-completion-reconciliation). |
| [Expressions vs scripts](06-SCRIPTING/03-EXPRESSIONS-VS-SCRIPTS.md) | C | C | C | C | C | Rig matchNames versus fixed expression names, readback/escaping/engine limits; [review](CHAPTER-RECONCILIATION-2026-10-07.md#scripting-completion-reconciliation). |
| [ExtendScript scripting](06-SCRIPTING/README.md) | C | L | C | L | C | Reconciled route index, not standalone implementation; [review](CHAPTER-RECONCILIATION-2026-10-07.md#scripting-completion-reconciliation). |

## 07-PANELS

| Глава | Т | С | И | П | Л | Оставшийся результат / блок |
|---|---|---|---|---|---|---|
| [CEP development](07-PANELS/01-CEP.md) | C | C | C | C | C | Manifest/bootstrap walkthrough и controlled failure paths согласованы. **№2 выполнен**. |
| [UXP transition for After Effects](07-PANELS/02-UXP-TRANSITION.md) | R | L | R | L | C | Перепроверить официальные даты; ограничить главу migration context без выдуманного API. **№5** |
| [Panels: CEP now, UXP transition](07-PANELS/README.md) | R | L | R | L | C | Навигация и маршрут проверены; **№3 выполнен**. Остальные редакционные оси остаются R/L; итоговая сверка — **№16**. |

## 08-MACOS

| Глава | Т | С | И | П | Л | Оставшийся результат / блок |
|---|---|---|---|---|---|---|
| [macOS — Xcode setup](08-MACOS/01-XCODE-SETUP.md) | E | E | R | R | C | Дать exact sample/target/settings путь до build artifact, объяснить SDK path/resource шаги. **№12** |
| [macOS — Apple Silicon / Universal binary](08-MACOS/02-UNIVERSAL-BINARY.md) | R | E | R | R | C | Добавить проверку slices/ресурсов/export на одном конкретном product artifact. **№12** |
| [macOS — debugging After Effects plug-ins](08-MACOS/03-DEBUGGING.md) | E | E | R | R | C | Добавить attach/breakpoint/LLDB/symbols walkthrough и диагностические развилки. **№12** |
| [macOS — GPU development](08-MACOS/04-GPU.md) | R | E | R | R | C | Связать backend/device policy с macOS sample и подтверждением выбранного GPU пути. **№12** |
| [macOS — signing and notarization](08-MACOS/05-SIGNING-NOTARIZATION.md) | E | E | R | R | C | Дать конкретный signing/notary/stapling маршрут с identity и проверяемым результатом. **№12** |
| [macOS — installation and packaging](08-MACOS/06-INSTALLATION-PACKAGING.md) | E | E | R | R | C | Добавить staging/install/upgrade/rollback пример с владением установленными файлами. **№12** |
| [macOS — CI pipeline](08-MACOS/07-CI.md) | R | E | R | R | C | Связать CI outputs, symbol archive и signed artifact с точным source/build identity. **№12** |
| [macOS — native SDK validation](08-MACOS/08-NATIVE-SDK-VALIDATION.md) | R | E | R | R | C | Согласовать alias-path fix и source report; optional compile не смешивать с docs readiness. **№4** |
| [macOS — production build pipeline](08-MACOS/09-PRODUCTION-BUILD-PIPELINE.md) | E | E | R | R | C | Свести sample→resources→bundle→symbols→package в воспроизводимый учебный маршрут. **№12** |
| [macOS developer bible](08-MACOS/README.md) | R | L | R | L | C | Навигация и маршрут проверены; **№3 выполнен**. Остальные редакционные оси остаются R/L; итоговая сверка — **№16**. |

## 09-WINDOWS

| Глава | Т | С | И | П | Л | Оставшийся результат / блок |
|---|---|---|---|---|---|---|
| [Windows — Visual Studio setup](09-WINDOWS/01-VISUAL-STUDIO-SETUP.md) | E | E | R | R | C | Дать exact sample/VS target/include/lib settings и resource chain до .aex. **№13** |
| [Windows — x64 and ARM64](09-WINDOWS/02-X64-ARM64.md) | R | E | R | R | C | Разнести target architecture, toolchain и подтверждённую host support matrix. **№13** |
| [Windows — debugging After Effects plug-ins](09-WINDOWS/03-DEBUGGING.md) | E | E | R | R | C | Добавить attach/breakpoint/exception/symbols walkthrough и диагностику load failure. **№13** |
| [Windows — GPU development](09-WINDOWS/04-GPU.md) | R | E | R | R | C | Связать backend/device/fallback с конкретным Windows sample/configuration. **№13** |
| [Windows — code signing](09-WINDOWS/05-CODE-SIGNING.md) | E | E | R | R | C | Дать SignTool/signature/timestamp verification пример для конкретного artifact. **№13** |
| [Windows — installation and packaging](09-WINDOWS/06-INSTALLATION-PACKAGING.md) | E | E | R | R | C | Добавить owned-file install/upgrade/rollback маршрут с expected results. **№13** |
| [Windows — CI pipeline](09-WINDOWS/07-CI.md) | R | E | R | R | C | Связать Windows build/symbol/package outputs с source identity и target matrix. **№13** |
| [Windows — native SDK validation](09-WINDOWS/08-NATIVE-SDK-VALIDATION.md) | R | E | R | R | C | Согласовать MSVC report и portable lane; не приписывать stub PASS реальному SDK. **№4** |
| [Windows — production build pipeline](09-WINDOWS/09-PRODUCTION-BUILD-PIPELINE.md) | E | E | R | R | C | Проследить source→PiPL/.r→.rc/.res→.aex→symbols→installer на одном примере. **№13** |
| [Windows developer bible](09-WINDOWS/README.md) | R | L | R | L | C | Навигация и маршрут проверены; **№3 выполнен**. Остальные редакционные оси остаются R/L; итоговая сверка — **№16**. |

## 10-TESTING

| Глава | Т | С | И | П | Л | Оставшийся результат / блок |
|---|---|---|---|---|---|---|
| [Test matrix](10-TESTING/01-TEST-MATRIX.md) | E | E | R | R | C | Добавить заполненную учебную матрицу с expected/observed и exact identity. **№15** |
| [Render correctness](10-TESTING/02-RENDER-CORRECTNESS.md) | E | E | R | R | C | Добавить identity calibration, exceptional floats и matched-toolchain parity recipe. **№15** |
| [MFR stress tests](10-TESTING/03-MFR-STRESS.md) | E | E | R | R | C | Добавить bounded hang/cancel incident template с доказательствами concurrency. **№15** |
| [Performance testing](10-TESTING/04-PERFORMANCE.md) | E | E | R | R | C | Показать раздельные core/render/Preview метрики, повторения и frame coverage. **№15** |
| [Crash diagnostics](10-TESTING/05-CRASH-DIAGNOSTICS.md) | E | E | R | R | C | Добавить заполненный crash/hang record с artifact/symbol identity и границами вывода. **№15** |
| [Evidence and acceptance](10-TESTING/06-EVIDENCE-AND-ACCEPTANCE.md) | C | C | C | C | C | Status/origin/decision связаны с filled NOT_RUN record; [review](CHAPTER-RECONCILIATION-2026-10-07.md). |
| [Host verification in After Effects](10-TESTING/06-HOST-VERIFICATION.md) | C | C | C | C | C | Expected channels, calibration/actual route/frame coverage и ladder согласованы; [review](CHAPTER-RECONCILIATION-2026-10-07.md). |
| [Test evidence and acceptance records](10-TESTING/07-TEST-EVIDENCE.md) | C | C | C | C | C | Downloadable filled plan и separate primary JSON/raw hash references; [review](CHAPTER-RECONCILIATION-2026-10-07.md). |
| [Clean-machine release acceptance](10-TESTING/08-CLEAN-MACHINE-ACCEPTANCE.md) | C | C | C | C | C | Scoped own-file upgrade/rollback record и NOT_RUN observations; [review](CHAPTER-RECONCILIATION-2026-10-07.md). |
| [Testing strategy](10-TESTING/README.md) | R | L | R | L | C | Навигация и маршрут проверены; **№3 выполнен**. Остальные редакционные оси остаются R/L; итоговая сверка — **№16**. |

## 11-DISTRIBUTION

| Глава | Т | С | И | П | Л | Оставшийся результат / блок |
|---|---|---|---|---|---|---|
| [Versioning and compatibility](11-DISTRIBUTION/01-VERSIONING-COMPATIBILITY.md) | R | E | R | R | C | Согласовать version table, disk IDs и source/artifact compatibility promises. **№5** |
| [Security and licensing architecture](11-DISTRIBUTION/02-SECURITY-LICENSING.md) | R | E | R | R | C | Зафиксировать license/provenance правила примеров и происхождение third-party SDK assets. **№5** |
| [Release checklist](11-DISTRIBUTION/03-RELEASE-CHECKLIST.md) | R | E | R | R | C | Добавить filled documentation/product evidence пример и artifact-bound release gate. **№15** |
| [Install locations cheat sheet](11-DISTRIBUTION/04-INSTALL-LOCATIONS.md) | R | E | R | R | C | Сверить официальные platform paths и связать их с owned-file installers. **№13** |
| [Release artifacts, installers and update strategy](11-DISTRIBUTION/05-RELEASE-ARTIFACTS-UPDATES.md) | E | E | R | R | C | Связать binary/PiPL/UI identity, symbols и upgrade/rollback evidence. **№15** |

## 12-RECIPES

| Глава | Т | С | И | П | Л | Оставшийся результат / блок |
|---|---|---|---|---|---|---|
| [Recipe — first native effect](12-RECIPES/01-FIRST-EFFECT.md) | E | E | R | R | C | Связать конкретный sample, build steps, expected gain и evidence boundaries. **№12** |
| [Recipe — migrate an existing effect to MFR](12-RECIPES/02-MFR-MIGRATION.md) | C | C | C | C | C | Inventory/snapshot/cache/candidate/observed overlap route согласован; [review](CHAPTER-RECONCILIATION-2026-10-07.md). |
| [Recipe — plug-in does not load](12-RECIPES/03-DEBUG-PLUGIN-NOT-LOADING.md) | R | E | R | R | C | Связать failure tree с resources/exports/architecture/logs обеих платформ. **№13** |
| [Recipe — CPU/GPU equivalence](12-RECIPES/04-CPU-GPU-EQUIVALENCE.md) | C | C | C | C | C | Identity, numeric policy, actual route и fallback comparisons согласованы; [review](CHAPTER-RECONCILIATION-2026-10-07.md). |
| [Recipe — panel + native core](12-RECIPES/05-HYBRID-PANEL-NATIVE.md) | C | C | C | C | C | Prefix schema, ordering и error outcomes согласованы. **№2 выполнен**. |
| [Recipe — profiling a slow effect](12-RECIPES/06-PROFILING.md) | E | E | R | R | C | Добавить воспроизводимый profiling record с warmup/repeats/core-host-Preview scopes. **№15** |
| [Practical recipes](12-RECIPES/README.md) | R | L | R | L | C | Навигация и маршрут проверены; **№3 выполнен**. Остальные редакционные оси остаются R/L; итоговая сверка — **№16**. |

## 13-TEMPLATES

| Глава | Т | С | И | П | Л | Оставшийся результат / блок |
|---|---|---|---|---|---|---|
| [Bug report template](13-TEMPLATES/BUG-REPORT.md) | E | E | R | R | C | Добавить заполненный example с exact artifact, raw evidence и bounded conclusion. **№15** |
| [Compatibility matrix template](13-TEMPLATES/COMPATIBILITY-MATRIX.md) | E | E | R | R | C | Показать filled rows с SDK/AE/OS/architecture и честными NOT RUN. **№15** |
| [Performance report template](13-TEMPLATES/PERFORMANCE-REPORT.md) | E | E | R | R | C | Добавить filled report с раздельными performance layers и frame coverage. **№15** |
| [Plug-in specification template](13-TEMPLATES/PLUGIN-SPEC.md) | E | E | R | R | C | Связать filled spec с persistence, errors, expected output и verification matrix. **№15** |
| [Working templates](13-TEMPLATES/README.md) | R | L | R | L | C | Навигация и маршрут проверены; **№3 выполнен**. Остальные редакционные оси остаются R/L; итоговая сверка — **№16**. |
| [Release notes template](13-TEMPLATES/RELEASE-NOTES.md) | E | E | R | R | C | Показать filled release record с artifact identity и реальными evidence limits. **№15** |

## 14-NATIVE-INTEGRATIONS

| Глава | Т | С | И | П | Л | Оставшийся результат / блок |
|---|---|---|---|---|---|---|
| [Native SDK taxonomy](14-NATIVE-INTEGRATIONS/01-TAXONOMY.md) | R | E | R | R | C | Навигация и маршрут проверены; **№3 выполнен**. Остальные редакционные оси остаются R/L; итоговая сверка — **№16**. |
| [Host call flows](14-NATIVE-INTEGRATIONS/02-HOST-CALL-FLOWS.md) | C | C | C | C | C | Command flow связан с actual source/design и cleanup; [review](CHAPTER-RECONCILIATION-2026-10-07.md#remaining-aegpnative-integration-closure). |
| [PICA suites — versioned native service bus](14-NATIVE-INTEGRATIONS/03-PICA-SUITES.md) | C | C | C | C | C | Public ABI, buffers/errors/publication и header-only scope; [review](CHAPTER-RECONCILIATION-2026-10-07.md#remaining-aegpnative-integration-closure). |
| [Effect plug-ins — native capability map](14-NATIVE-INTEGRATIONS/04-EFFECTS.md) | C | C | C | C | C | Canonical state route без duplicate contracts; [review](CHAPTER-RECONCILIATION-2026-10-07.md). |
| [AEGP tools — native automation and deep AE integration](14-NATIVE-INTEGRATIONS/05-AEGP-TOOLS.md) | C | C | C | C | C | Stable targets/partial init и operation route согласованы; [review](CHAPTER-RECONCILIATION-2026-10-07.md#remaining-aegpnative-integration-closure). |
| [Keyframers](14-NATIVE-INTEGRATIONS/06-KEYFRAMERS.md) | C | C | C | C | C | Actual CompTime scalar batch versus follower/cancel/Undo design; [review](CHAPTER-RECONCILIATION-2026-10-07.md#remaining-aegpnative-integration-closure). |
| [Native dockable panels](14-NATIVE-INTEGRATIONS/07-NATIVE-PANELS.md) | C | C | C | C | C | Freshness/cancel/quiescence и guide-only platform scope; [review](CHAPTER-RECONCILIATION-2026-10-07.md#remaining-aegpnative-integration-closure). |
| [AEIO — registration and callback lifecycle](14-NATIVE-INTEGRATIONS/08-AEIO.md) | C | C | C | C | C | Overview/templates/reference ownership и source routes сверены; [review](CHAPTER-RECONCILIATION-2026-10-07.md). |
| [Artisan — registration, contexts and render contract](14-NATIVE-INTEGRATIONS/09-ARTISAN.md) | C | C | C | C | C | Typed registration/version и partial init сверены с Artie; [review](CHAPTER-RECONCILIATION-2026-10-07.md). |
| [BlitHook — display-pipeline frame hook](14-NATIVE-INTEGRATIONS/10-BLITHOOK.md) | C | L | C | L | C | Synchronous owned-copy/IPC и quiescence; async protocol намеренно ограничен; [review](CHAPTER-RECONCILIATION-2026-10-07.md#remaining-aegpnative-integration-closure). |
| [Legacy / historical native integration boundaries](14-NATIVE-INTEGRATIONS/11-LEGACY-NATIVE.md) | R | E | R | R | C | Сверить old/current suite table и разделить source migration от project compatibility. **№5** |
| [AEGP suites catalog — After Effects 26.5 snapshot](14-NATIVE-INTEGRATIONS/12-AEGP-SUITES-CATALOG.md) | R | L | R | L | C | Согласовать catalogue с exact baseline; не превращать inventory в runtime coverage claim. **№5** |
| [Public SDK docs errata / verification notes](14-NATIVE-INTEGRATIONS/13-DOCS-ERRATA.md) | R | L | R | L | C | Связать errata с dated sources; сохранить superseded finding и later correction. **№5** |
| [Native integrations — карта всего нативного SDK After Effects](14-NATIVE-INTEGRATIONS/README.md) | R | L | R | L | C | Навигация и маршрут проверены; **№3 выполнен**. Остальные редакционные оси остаются R/L; итоговая сверка — **№16**. |

## 15-COMMUNICATION

| Глава | Т | С | И | П | Л | Оставшийся результат / блок |
|---|---|---|---|---|---|---|
| [After Effects → Effect plug-in](15-COMMUNICATION/01-AE-TO-EFFECT.md) | C | C | C | C | C | Selector/borrowed values согласованы; [review](CHAPTER-RECONCILIATION-2026-10-07.md). |
| [After Effects → AEGP](15-COMMUNICATION/02-AE-TO-AEGP.md) | C | C | C | C | C | Initializer/partial hooks и worker quiescence сверены; [review](CHAPTER-RECONCILIATION-2026-10-07.md#remaining-aegpnative-integration-closure). |
| [AEGP → Effect: generic call](15-COMMUNICATION/03-AEGP-TO-EFFECT.md) | C | C | C | C | C | Fresh ref/layer-time/payload sentinel и delivery/domain/cleanup; [review](CHAPTER-RECONCILIATION-2026-10-07.md#remaining-aegpnative-integration-closure). |
| [Plug-in → Plug-in через published PICA suite](15-COMMUNICATION/04-PLUGIN-TO-PLUGIN-PICA.md) | C | C | C | C | C | SDK patterns versus header-only template, release/error/ABI rules; [review](CHAPTER-RECONCILIATION-2026-10-07.md#remaining-aegpnative-integration-closure). |
| [ExtendScript → After Effects](15-COMMUNICATION/05-SCRIPT-TO-AE.md) | C | C | C | C | C | Local partial result versus wire envelope, Undo/transport/operation routes; [review](CHAPTER-RECONCILIATION-2026-10-07.md#scripting-completion-reconciliation). |
| [CEP panel <-> ExtendScript](15-COMMUNICATION/06-CEP-TO-EXTENDSCRIPT.md) | C | C | C | C | C | Envelopes, parse/type/errors, JSON bootstrap и mutation policy согласованы; отдельный INTERNAL_ERROR и его client blocking проверены portable tests; Unicode fixture изолирован, runtime не заявлен. **№2 выполнен**. |
| [Native <-> script/panel: как собирать гибридный продукт](15-COMMUNICATION/07-NATIVE-TO-SCRIPT-PANEL.md) | C | C | C | C | C | Correlation/freshness/ordering/cancel/unknown outcome разделены; transport design limits; [review](CHAPTER-RECONCILIATION-2026-10-07.md#remaining-aegpnative-integration-closure). |
| [Threading boundaries](15-COMMUNICATION/08-THREADING-BOUNDARIES.md) | C | C | C | C | C | Worker/generation/quiescence и incident границы разделены; [review](CHAPTER-RECONCILIATION-2026-10-07.md). |
| [Data ownership and lifetime](15-COMMUNICATION/09-DATA-OWNERSHIP.md) | C | C | C | C | C | Phase-specific checkin и borrowed cache-value/payload lifetime согласованы; [review](CHAPTER-RECONCILIATION-2026-10-07.md). |
| [Как компоненты общаются друг с другом и с After Effects](15-COMMUNICATION/README.md) | R | L | R | L | C | Навигация и маршрут проверены; **№3 выполнен**. Остальные редакционные оси остаются R/L; итоговая сверка — **№16**. |

## 17-NATIVE-SUITE-COOKBOOK

| Глава | Т | С | И | П | Л | Оставшийся результат / блок |
|---|---|---|---|---|---|---|
| [Как пользоваться cookbook](17-NATIVE-SUITE-COOKBOOK/00-HOW-TO-USE.md) | C | C | C | C | C | Source/operation route и successful-Start-only Undo balance уточнены; [review](CHAPTER-RECONCILIATION-2026-10-07.md). |
| [Project + Item recipes](17-NATIVE-SUITE-COOKBOOK/01-PROJECT-ITEMS.md) | C | C | C | C | C | Query source/partial outputs, New/Open и import route сверены; [review](CHAPTER-RECONCILIATION-2026-10-07.md). |
| [Composition recipes](17-NATIVE-SUITE-COOKBOOK/02-COMPOSITIONS.md) | C | C | C | C | C | Fixed create source отделён от config/Undo/compensation design; [review](CHAPTER-RECONCILIATION-2026-10-07.md). |
| [Layer recipes](17-NATIVE-SUITE-COOKBOOK/03-LAYERS.md) | C | C | C | C | C | ID/context resolution и bounded/truncated collector scope сверены; [review](CHAPTER-RECONCILIATION-2026-10-07.md). |
| [Effect recipes](17-NATIVE-SUITE-COOKBOOK/04-EFFECTS.md) | C | C | C | C | C | Apply/dispose versus mutation compensation и generic-call route сверены; [review](CHAPTER-RECONCILIATION-2026-10-07.md). |
| [Streams / properties / expressions](17-NATIVE-SUITE-COOKBOOK/05-STREAMS-PROPERTIES.md) | C | C | C | C | C | OneD/source policy, expression stage и separated followers сверены; [review](CHAPTER-RECONCILIATION-2026-10-07.md). |
| [Keyframes: чтение, изменение, batch insert, interpolation](17-NATIVE-SUITE-COOKBOOK/06-KEYFRAMES.md) | C | C | C | C | C | Actual CompTime batch cleanup/preconditions и interpolation limits сверены; [review](CHAPTER-RECONCILIATION-2026-10-07.md). |
| [Masks: reference lifetime, outline stream и geometry](17-NATIVE-SUITE-COOKBOOK/07-MASKS.md) | C | C | C | C | C | Partial create/edit flow, disposal versus deletion и sample limits сверены; [review](CHAPTER-RECONCILIATION-2026-10-07.md). |
| [Text documents and markers](17-NATIVE-SUITE-COOKBOOK/08-TEXT-MARKERS.md) | C | C | C | C | C | Typed write/readback и payload/UTF-16 ownership сверены; [review](CHAPTER-RECONCILIATION-2026-10-07.md). |
| [Footage / import: ownership, interpretation, sequences and proxies](17-NATIVE-SUITE-COOKBOOK/09-FOOTAGE-IMPORT.md) | C | C | C | C | C | Adoption/error ownership и interpretation/proxy/replace design сверены; [review](CHAPTER-RECONCILIATION-2026-10-07.md). |
| [Render frame → pixels](17-NATIVE-SUITE-COOKBOOK/10-RENDER-FRAMES.md) | C | C | C | C | C | Options/receipt/world/source subset и calibration/output scope сверены; [review](CHAPTER-RECONCILIATION-2026-10-07.md). |
| [Render Queue recipes](17-NATIVE-SUITE-COOKBOOK/11-RENDER-QUEUE.md) | C | C | C | C | C | Named enum/readback, STOPPED/partial mutation и actual helper limits сверены; [review](CHAPTER-RECONCILIATION-2026-10-07.md). |
| [Memory / Undo / Persistent Data](17-NATIVE-SUITE-COOKBOOK/12-MEMORY-UNDO-PERSISTENCE.md) | C | C | C | C | C | Actual helper composition и observable transaction limits раскрыты; [review](CHAPTER-RECONCILIATION-2026-10-07.md). |
| [Guides / Item Views / Selection](17-NATIVE-SUITE-COOKBOOK/13-GUIDES-VIEWS-SELECTION.md) | C | C | C | L | C | Selection freshness и model/view partial failure; later API gate, no adapter source; [review](CHAPTER-RECONCILIATION-2026-10-07.md). |
| [Lifetime + threading rules](17-NATIVE-SUITE-COOKBOOK/14-LIFETIME-THREADING.md) | C | C | C | C | C | Render owner/suite lifetimes и отдельный async shutdown route сверены; [review](CHAPTER-RECONCILIATION-2026-10-07.md). |
| [Native recipe index](17-NATIVE-SUITE-COOKBOOK/15-RECIPE-INDEX.md) | C | L | C | L | C | Index связывает actual code, design chains и evidence; не implementation; [review](CHAPTER-RECONCILIATION-2026-10-07.md). |
| [AEGP Suite function map — native capability index](17-NATIVE-SUITE-COOKBOOK/16-SUITE-FUNCTION-MAP.md) | C | L | C | L | C | Selected capability map с 25.6/source-subset/later gates; не exact inventory; [review](CHAPTER-RECONCILIATION-2026-10-07.md). |
| [Native Suite Cookbook](17-NATIVE-SUITE-COOKBOOK/README.md) | C | L | C | L | C | Overview routes/current contracts/evidence и actual source index согласованы; [review](CHAPTER-RECONCILIATION-2026-10-07.md). |

## 19-NATIVE-CODE-FOUNDATION

| Глава | Т | С | И | П | Л | Оставшийся результат / блок |
|---|---|---|---|---|---|---|
| [Suite acquisition](19-NATIVE-CODE-FOUNDATION/01-SUITE-ACQUISITION.md) | C | C | C | C | C | Type/name/version, optional failure, replacement и teardown сверены с helper; [review](CHAPTER-RECONCILIATION-2026-10-07.md). |
| [AEGP ownership / RAII](19-NATIVE-CODE-FOUNDATION/02-RAII-OWNERSHIP.md) | C | C | C | C | C | Actual render chain, ownership/adoption и secondary-error limits сверены; [review](CHAPTER-RECONCILIATION-2026-10-07.md). |
| [Undo groups and transaction boundaries](19-NATIVE-CODE-FOUNDATION/03-UNDO-TRANSACTIONS.md) | C | C | C | C | C | Helper balance отделён от command compensation и actual mutation; [review](CHAPTER-RECONCILIATION-2026-10-07.md). |
| [Host callback ABI boundary](19-NATIVE-CODE-FOUNDATION/04-HOST-CALL-BOUNDARY.md) | C | C | C | C | C | Guard/fallback/cleanup и unsupported fatal recovery сверены; [review](CHAPTER-RECONCILIATION-2026-10-07.md). |
| [Native C++ foundation — reusable safety layer](19-NATIVE-CODE-FOUNDATION/README.md) | C | C | C | C | C | Overview/helper/test/source limits согласованы; route, не standalone plugin; [review](CHAPTER-RECONCILIATION-2026-10-07.md). |

## Поддерживающие материалы и приложения

| Материал | Оставшийся результат | Блоки |
|---|---|---|
| [Working templates](16-WORKING-TEMPLATES/README.md) | CEP fixes; source/contract alignment с соответствующей core главой; filled use cases | 2, 6–15 |
| [SDK tools и records](18-SDK-HEADER-TOOLS/README.md) | Alias-path regression, transparent generated identity, dated-source/version/provenance sweep | 4, 5 |
| [Cookbook evidence](17-NATIVE-SUITE-COOKBOOK/VERIFICATION.md), [code guide](17-NATIVE-SUITE-COOKBOOK/code/README.md) | Исторические compiler claims согласованы в блоке 1; recipes ещё сверить со сквозными операциями | 1 выполнен; 11 |
| [Reference guides](20-REFERENCE-IMPLEMENTATIONS/README.md) | Сделать все intended guides достижимыми; reconcile source и practical steps в соответствующих блоках | 3, 6–15 |
| [Platform source review](11-DISTRIBUTION/05-PLATFORM-SOURCE-REVIEW-2026-10-01.md) | Перепроверить датированные официальные факты перед freeze | 5, 16 |
| [Case studies](22-PROJECT-CASE-STUDIES/README.md) | Scoped FSTR/Hot Loader перенос без расширения старых runtime результатов | 2, 11, 15 |
| [ElasticGridFX transfer](22-PROJECT-CASE-STUDIES/ELASTICGRIDFX-TRANSFER-PLAN-2026-10-02.md) | Реализовать уже mapped sampling/performance/identity уроки; инструменты отдельно reviewed перед адаптацией | 5–8, 12–15 |
| [Built-in effects atlas](21-BUILTIN-EFFECTS-REVERSE-ENGINEERING/README.md) | Исследовательское приложение; полный каталог не блокирует core edition | По ценности, вне обязательного freeze |
| [Coverage matrix](FINAL-COVERAGE-AUDIT.md), [checklist](COMPLETION-CHECKLIST.md), [ledger](VERIFICATION.md) | После каждого блока согласовывать фактические результаты и открытые задачи | 1–16 |

Generated MASTER/MANIFEST и historical aliases не являются отдельными core chapters. Их source/generated consistency проверяется в блоках 4 и 16; dated audit остаётся исходным входом, исправления фиксируются в текущем плане и ledger.
