# Поглавный трекер завершения

Обновлено: **2026-10-04**. План: [16 логических блоков](COMPLETION-PLAN.md). Правила: [EDITORIAL-GUIDE](EDITORIAL-GUIDE.md); существующий source/evidence baseline — [coverage matrix](FINAL-COVERAGE-AUDIT.md).

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

Все строки сейчас остаются в очереди: ни одна core глава не объявляется полностью закрытой созданием этого трекера. `L` в обзоре означает, что это route/index, а не самостоятельная реализация. Для UXP, BlitHook и catalogue/errata предел отдельно указан в строке; остальные применимые оси ещё требуют сверки. Для provenance запланирован итоговый проход блока 5, для links блок 3 завершён; остальные оси оцениваются отдельно. Столбец «Результат / блок» указывает ведущую содержательную работу, а не все зависимости.

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
| [Native plug-in lifecycle](01-ARCHITECTURE/01-LIFECYCLE.md) | R | E | R | R | C | Связать lifecycle с versioned persistence и failure/recovery состояниями Effect. **№6** |
| [Память, время жизни ресурсов и ошибки](01-ARCHITECTURE/02-MEMORY-THREADING-ERRORS.md) | R | E | R | R | C | Сверить memory/thread policy с receipt lifecycle Compute Cache и bounded MFR incident. **№8** |
| [PiPL, регистрация и загрузка плагина](01-ARCHITECTURE/03-PIPL-AND-LOADING.md) | R | E | R | R | C | Связать PiPL/resource chain с конкретными macOS/Windows sample walkthroughs. **№13** |
| [Version compatibility](01-ARCHITECTURE/04-VERSION-COMPATIBILITY.md) | R | E | R | R | C | Добавить читаемую таблицу SDK/AE/suite/architecture и сценарий отказа при несовместимости. **№5** |
| [Performance architecture](01-ARCHITECTURE/05-PERFORMANCE-ARCHITECTURE.md) | E | E | R | R | C | Разделить native core, host render, RAM Preview и измеренную конкурентность. **№8** |
| [Build system strategy](01-ARCHITECTURE/06-BUILD-SYSTEM.md) | R | E | R | R | C | Связать общие правила с конкретными resource/export/build маршрутами обеих платформ. **№13** |
| [Communication architecture](01-ARCHITECTURE/07-COMMUNICATION-ARCHITECTURE.md) | C | C | C | C | C | Envelopes, correlation и mutation ordering/idempotency согласованы. **№2 выполнен**. |

## 02-EFFECT-PLUGINS

| Глава | Т | С | И | П | Л | Оставшийся результат / блок |
|---|---|---|---|---|---|---|
| [Устройство Effect-плагина: от регистрации до кадра](02-EFFECT-PLUGINS/01-ANATOMY.md) | R | E | R | R | C | Связать lifecycle с migration/resetup/flatten и sample state example. **№6** |
| [Параметры и интерфейс Effect-плагина](02-EFFECT-PLUGINS/02-PARAMETERS-UI.md) | E | E | R | R | C | Добавить arbitrary data, schema evolution, compare/interpolate/flatten и disk-ID migration. **№6** |
| [SmartFX: зависимости, области и время жизни буферов](02-EFFECT-PLUGINS/03-SMARTFX.md) | E | E | R | R | C | Добавить blur/transform/temporal walkthrough с checkout IDs, ROI и time conversion. **№7** |
| [MFR: параллельный рендер, состояние и Compute Cache](02-EFFECT-PLUGINS/04-MFR-THREAD-SAFETY.md) | E | E | R | R | C | Добавить receipt/error cleanup схему и ограниченный incident record из ElasticGridFX. **№8** |
| [GPU effects](02-EFFECT-PLUGINS/05-GPU.md) | E | E | R | R | C | Разобрать device state, one backend, fallback и подтверждение реально исполненной ветки. **№8** |
| [Пиксели, цвет и прозрачность в Effect-плагине](02-EFFECT-PLUGINS/06-COLOR-PIXELS.md) | E | E | R | R | C | Добавить calibrated output, exact sampling, NaN/Inf и integer/float/alpha правила. **№7** |
| [Audio effects](02-EFFECT-PLUGINS/07-AUDIO.md) | E | E | R | R | C | Дать bounded sound-world walkthrough; сохранять отсутствие sample-backed AUDIO_RENDER guarantees. **№9** |
| [Дополнительные каналы: глубина, ID, нормали и сырые данные](02-EFFECT-PLUGINS/08-AUXILIARY-CHANNELS.md) | R | E | R | R | C | Связать channel checkout/checkin, dimensions и coordinate conversion с SmartFX walkthrough. **№7** |
| [Custom UI and Drawbot](02-EFFECT-PLUGINS/09-CUSTOM-UI-DRAWBOT.md) | E | E | R | R | C | Добавить один draw/hit/drag путь с cleanup и scoped async-manager границей. **№9** |
| [Effect plug-ins](02-EFFECT-PLUGINS/README.md) | R | L | R | L | C | Навигация и маршрут проверены; **№3 выполнен**. Остальные редакционные оси остаются R/L; итоговая сверка — **№16**. |

## 03-AEGP

| Глава | Т | С | И | П | Л | Оставшийся результат / блок |
|---|---|---|---|---|---|---|
| [AEGP: инициализация, hooks и suites](03-AEGP/01-HOOKS-SUITES.md) | R | E | R | R | C | Проследить menu command от resolve target до cleanup, ошибки и report. **№11** |
| [AEGP: операции с проектом и рендером](03-AEGP/02-PROJECT-RENDER-AUTOMATION.md) | E | E | R | R | C | Добавить import/create/animate/queue/render operation chains с rollback и identity. **№11** |
| [AEGP](03-AEGP/README.md) | R | L | R | L | C | Навигация и маршрут проверены; **№3 выполнен**. Остальные редакционные оси остаются R/L; итоговая сверка — **№16**. |

## 04-AEIO

| Глава | Т | С | И | П | Л | Оставшийся результат / блок |
|---|---|---|---|---|---|---|
| [AEIO — media import/export plug-ins](04-AEIO/README.md) | E | E | R | R | C | Связать importer/exporter сценарий с exact SDK callback/file paths и cleanup. **№14** |

## 05-ARTISAN

| Глава | Т | С | И | П | Л | Оставшийся результат / блок |
|---|---|---|---|---|---|---|
| [Artisan — custom composition 3D renderer](05-ARTISAN/README.md) | E | E | R | R | C | Связать normalized scene и render lifecycle с exact Artie path и current suites. **№14** |

## 06-SCRIPTING

| Глава | Т | С | И | П | Л | Оставшийся результат / блок |
|---|---|---|---|---|---|---|
| [After Effects scripting object model](06-SCRIPTING/01-OBJECT-MODEL.md) | E | E | R | R | C | Добавить bulk rename/import/replace операции со stable targeting и partial failure. **№10** |
| [ScriptUI](06-SCRIPTING/02-SCRIPTUI.md) | E | E | R | R | C | Связать dockable panel с reusable command, progress/cancel и stale target. **№10** |
| [Expressions vs scripts](06-SCRIPTING/03-EXPRESSIONS-VS-SCRIPTS.md) | E | E | R | R | C | Добавить законченный expression rig с matchName и escaping/version границами. **№10** |
| [ExtendScript scripting](06-SCRIPTING/README.md) | R | L | R | L | C | Навигация и маршрут проверены; **№3 выполнен**. Остальные редакционные оси остаются R/L; итоговая сверка — **№16**. |

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
| [Evidence and acceptance](10-TESTING/06-EVIDENCE-AND-ACCEPTANCE.md) | R | E | R | R | C | Согласовать PASS/FAIL/BLOCKED/NOT RUN с заполненным sample record. **№15** |
| [Host verification in After Effects](10-TESTING/06-HOST-VERIFICATION.md) | R | E | R | R | C | Связать evidence ladder с калибровкой output и actual route/frame coverage. **№15** |
| [Test evidence and acceptance records](10-TESTING/07-TEST-EVIDENCE.md) | E | E | R | R | C | Добавить machine-readable filled record и отдельную raw evidence reference. **№15** |
| [Clean-machine release acceptance](10-TESTING/08-CLEAN-MACHINE-ACCEPTANCE.md) | R | E | R | R | C | Показать scoped install/upgrade/rollback record без фиктивных выполненных проверок. **№15** |
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
| [Recipe — migrate an existing effect to MFR](12-RECIPES/02-MFR-MIGRATION.md) | E | E | R | R | C | Добавить state inventory→immutable snapshot→cache receipt→concurrency workflow. **№8** |
| [Recipe — plug-in does not load](12-RECIPES/03-DEBUG-PLUGIN-NOT-LOADING.md) | R | E | R | R | C | Связать failure tree с resources/exports/architecture/logs обеих платформ. **№13** |
| [Recipe — CPU/GPU equivalence](12-RECIPES/04-CPU-GPU-EQUIVALENCE.md) | E | E | R | R | C | Добавить matched identity/toolchain, exact/tolerance/NaN и fallback comparisons. **№15** |
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
| [Host call flows](14-NATIVE-INTEGRATIONS/02-HOST-CALL-FLOWS.md) | R | E | R | R | C | Сопоставить call flows с одним сквозным AEGP command и resource cleanup. **№11** |
| [PICA suites — versioned native service bus](14-NATIVE-INTEGRATIONS/03-PICA-SUITES.md) | R | E | R | R | C | Согласовать ABI/version/ownership ошибки с bridge/cookbook examples. **№11** |
| [Effect plug-ins — native capability map](14-NATIVE-INTEGRATIONS/04-EFFECTS.md) | R | E | R | R | C | Связать native Effect model со state/arbitrary migration walkthrough. **№6** |
| [AEGP tools — native automation and deep AE integration](14-NATIVE-INTEGRATIONS/05-AEGP-TOOLS.md) | R | E | R | R | C | Связать command/update/idle/death flow со stable targets и partial init. **№11** |
| [Keyframers](14-NATIVE-INTEGRATIONS/06-KEYFRAMERS.md) | R | E | R | R | C | Добавить route к animate recipe, separated dimensions и batch failure cleanup. **№11** |
| [Native dockable panels](14-NATIVE-INTEGRATIONS/07-NATIVE-PANELS.md) | R | E | R | R | C | Сверить panel commands/model handoff с stale generations и shutdown recipe. **№11** |
| [AEIO — registration and callback lifecycle](14-NATIVE-INTEGRATIONS/08-AEIO.md) | R | E | R | R | C | Согласовать callback walkthrough с основным AEIO разделом и exact source paths. **№14** |
| [Artisan — registration, contexts and render contract](14-NATIVE-INTEGRATIONS/09-ARTISAN.md) | R | E | R | R | C | Согласовать Artie/current-suite walkthrough с основным renderer разделом. **№14** |
| [BlitHook — display-pipeline frame hook](14-NATIVE-INTEGRATIONS/10-BLITHOOK.md) | R | L | R | L | C | Согласовать borrowed buffer/IPC boundary; async lifetime оставить ограниченным известным контрактом. **№11** |
| [Legacy / historical native integration boundaries](14-NATIVE-INTEGRATIONS/11-LEGACY-NATIVE.md) | R | E | R | R | C | Сверить old/current suite table и разделить source migration от project compatibility. **№5** |
| [AEGP suites catalog — After Effects 26.5 snapshot](14-NATIVE-INTEGRATIONS/12-AEGP-SUITES-CATALOG.md) | R | L | R | L | C | Согласовать catalogue с exact baseline; не превращать inventory в runtime coverage claim. **№5** |
| [Public SDK docs errata / verification notes](14-NATIVE-INTEGRATIONS/13-DOCS-ERRATA.md) | R | L | R | L | C | Связать errata с dated sources; сохранить superseded finding и later correction. **№5** |
| [Native integrations — карта всего нативного SDK After Effects](14-NATIVE-INTEGRATIONS/README.md) | R | L | R | L | C | Навигация и маршрут проверены; **№3 выполнен**. Остальные редакционные оси остаются R/L; итоговая сверка — **№16**. |

## 15-COMMUNICATION

| Глава | Т | С | И | П | Л | Оставшийся результат / блок |
|---|---|---|---|---|---|---|
| [After Effects → Effect plug-in](15-COMMUNICATION/01-AE-TO-EFFECT.md) | R | E | R | R | C | Согласовать selector/state/persistence границы с Effect migration примером. **№6** |
| [After Effects → AEGP](15-COMMUNICATION/02-AE-TO-AEGP.md) | R | E | R | R | C | Согласовать initializer/hooks/main-thread lifecycle с command walkthrough. **№11** |
| [AEGP → Effect: generic call](15-COMMUNICATION/03-AEGP-TO-EFFECT.md) | R | E | R | R | C | Добавить generic-call chain с fresh EffectRef, layer time и separate error classes. **№11** |
| [Plug-in → Plug-in через published PICA suite](15-COMMUNICATION/04-PLUGIN-TO-PLUGIN-PICA.md) | R | E | R | R | C | Согласовать version/ownership/service failure с provider/consumer source example. **№11** |
| [ExtendScript → After Effects](15-COMMUNICATION/05-SCRIPT-TO-AE.md) | R | E | R | R | C | Связать reusable commands, undo и partial failure с automation recipes. **№10** |
| [CEP panel <-> ExtendScript](15-COMMUNICATION/06-CEP-TO-EXTENDSCRIPT.md) | C | C | C | C | C | Envelopes, parse/type/errors, JSON bootstrap и mutation policy согласованы; отдельный INTERNAL_ERROR и его client blocking проверены portable tests; Unicode fixture изолирован, runtime не заявлен. **№2 выполнен**. |
| [Native <-> script/panel: как собирать гибридный продукт](15-COMMUNICATION/07-NATIVE-TO-SCRIPT-PANEL.md) | R | E | R | R | C | Разнести transport correlation, freshness, cancellation и host command ordering. **№2** |
| [Threading boundaries](15-COMMUNICATION/08-THREADING-BOUNDARIES.md) | R | E | R | R | C | Согласовать workers/MFR/UI handoff с cache и bounded incident схемами. **№8** |
| [Data ownership and lifetime](15-COMMUNICATION/09-DATA-OWNERSHIP.md) | R | E | R | R | C | Согласовать payload/receipt lifetimes, stale generations и failure cleanup. **№8** |
| [Как компоненты общаются друг с другом и с After Effects](15-COMMUNICATION/README.md) | R | L | R | L | C | Навигация и маршрут проверены; **№3 выполнен**. Остальные редакционные оси остаются R/L; итоговая сверка — **№16**. |

## 17-NATIVE-SUITE-COOKBOOK

| Глава | Т | С | И | П | Л | Оставшийся результат / блок |
|---|---|---|---|---|---|---|
| [Как пользоваться cookbook](17-NATIVE-SUITE-COOKBOOK/00-HOW-TO-USE.md) | R | E | R | R | C | Дать route от задачи к exact suite/source, operation chain и evidence. **№11** |
| [Project + Item recipes](17-NATIVE-SUITE-COOKBOOK/01-PROJECT-ITEMS.md) | R | E | R | R | C | Добавить import/resolve/adopt chain с dangerous New/Open и invalidation policy. **№11** |
| [Composition recipes](17-NATIVE-SUITE-COOKBOOK/02-COMPOSITIONS.md) | R | E | R | R | C | Связать create/configure comp с current suite, undo и partial cleanup. **№11** |
| [Layer recipes](17-NATIVE-SUITE-COOKBOOK/03-LAYERS.md) | R | E | R | R | C | Связать stable LayerID/fresh resolution с create/edit/remove сценариями. **№11** |
| [Effect recipes](17-NATIVE-SUITE-COOKBOOK/04-EFFECTS.md) | R | E | R | R | C | Связать find/apply/dispose EffectRef с stream mutation и generic-call errors. **№11** |
| [Streams / properties / expressions](17-NATIVE-SUITE-COOKBOOK/05-STREAMS-PROPERTIES.md) | R | E | R | R | C | Проследить acquire/sample/set/dispose с expression/separated-dimension границами. **№11** |
| [Keyframes: чтение, изменение, batch insert, interpolation](17-NATIVE-SUITE-COOKBOOK/06-KEYFRAMES.md) | R | E | R | R | C | Дать animate chain и batch error path с timebase/interpolation ownership. **№11** |
| [Masks: reference lifetime, outline stream и geometry](17-NATIVE-SUITE-COOKBOOK/07-MASKS.md) | R | E | R | R | C | Связать MaskRef/outline/value cleanup со scoped create/edit operation. **№11** |
| [Text documents and markers](17-NATIVE-SUITE-COOKBOOK/08-TEXT-MARKERS.md) | R | E | R | R | C | Связать UTF-16/document/marker ownership со scoped write/keyframe recipe. **№11** |
| [Footage / import: ownership, interpretation, sequences and proxies](17-NATIVE-SUITE-COOKBOOK/09-FOOTAGE-IMPORT.md) | E | E | R | R | C | Дать import/adopt/replace chain с caller-owned failure rollback. **№11** |
| [Render frame → pixels](17-NATIVE-SUITE-COOKBOOK/10-RENDER-FRAMES.md) | E | E | R | R | C | Дать configure→checkout→world→checkin chain с calibration/output scope. **№11** |
| [Render Queue recipes](17-NATIVE-SUITE-COOKBOOK/11-RENDER-QUEUE.md) | E | E | R | R | C | Дать add/configure/queue/readback chain с named enum, state и artifact identity. **№11** |
| [Memory / Undo / Persistent Data](17-NATIVE-SUITE-COOKBOOK/12-MEMORY-UNDO-PERSISTENCE.md) | R | E | R | R | C | Связать undo vs rollback и ownership adoption с failed command cleanup. **№11** |
| [Guides / Item Views / Selection](17-NATIVE-SUITE-COOKBOOK/13-GUIDES-VIEWS-SELECTION.md) | R | E | R | R | C | Согласовать current/later API gates со stable selection и UI-only workflow. **№11** |
| [Lifetime + threading rules](17-NATIVE-SUITE-COOKBOOK/14-LIFETIME-THREADING.md) | R | E | R | R | C | Проследить handle validity, suite-before-owner teardown и async shutdown в рецепте. **№11** |
| [Native recipe index](17-NATIVE-SUITE-COOKBOOK/15-RECIPE-INDEX.md) | R | L | R | L | C | Согласовать operation index с новыми chains, exact code и evidence links. **№11** |
| [AEGP Suite function map — native capability index](17-NATIVE-SUITE-COOKBOOK/16-SUITE-FUNCTION-MAP.md) | R | L | R | L | C | Сверить function/suite version map с exact SDK records, сохранять compatibility choices. **№5** |
| [Native Suite Cookbook](17-NATIVE-SUITE-COOKBOOK/README.md) | R | L | R | L | C | Навигация и маршрут проверены; **№3 выполнен**. Остальные редакционные оси остаются R/L; итоговая сверка — **№16**. |

## 19-NATIVE-CODE-FOUNDATION

| Глава | Т | С | И | П | Л | Оставшийся результат / блок |
|---|---|---|---|---|---|---|
| [Suite acquisition](19-NATIVE-CODE-FOUNDATION/01-SUITE-ACQUISITION.md) | R | E | R | R | C | Согласовать acquire/release/failure с command lifetime и optional dependency. **№11** |
| [AEGP ownership / RAII](19-NATIVE-CODE-FOUNDATION/02-RAII-OWNERSHIP.md) | R | E | R | R | C | Проследить owner cleanup/adoption при частично выполненной operation chain. **№11** |
| [Undo groups and transaction boundaries](19-NATIVE-CODE-FOUNDATION/03-UNDO-TRANSACTIONS.md) | R | E | R | R | C | Связать Undo grouping с explicit rollback и partial mutation example. **№11** |
| [Host callback ABI boundary](19-NATIVE-CODE-FOUNDATION/04-HOST-CALL-BOUNDARY.md) | R | E | R | R | C | Проследить exceptions/host errors/cleanup через один command callback. **№11** |
| [Native C++ foundation — reusable safety layer](19-NATIVE-CODE-FOUNDATION/README.md) | R | L | R | L | C | Навигация и маршрут проверены; **№3 выполнен**. Остальные редакционные оси остаются R/L; итоговая сверка — **№16**. |

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
