# Cookbook — границы доказательств

Обновлено: **2026-10-07**. Правила: [EDITORIAL-GUIDE](../EDITORIAL-GUIDE.md); первичные записи: [общий evidence ledger](../VERIFICATION.md).

## Исторический compiler result — 2026-09-30

В [записи v1.1](../VERIFICATION.md#recorded-baseline-2026-09-30) сообщается об успешных 13 translation-unit syntax/type checks с SDK **25.6 build 61**, macOS arm64, Apple Clang, C++17. Cookbook тогда описывал шесть `code/*.cpp` recipes как проверенные в составе этого baseline.

В сохранённой записи нет точного source SHA или хэшей проверенных translation units. Поэтому её PASS сохраняется как исторически сообщённый результат с пробелом идентичности; нельзя заключить, что именно нынешние файлы проходили компиляцию. Коммит, публикующий отчёт, сам по себе не доказывает identity проверенного source tree.

После этого результата менялись исходники: `EffectStreamRecipes.cpp` перешёл на `EffectSuite5`, а `RenderQueueRecipes.cpp` получил named enum `AEGP_RenderItemStatus_QUEUED` и readback. Исторический PASS сам по себе эти corrections не покрывает; позднейшая exact-source запись приведена отдельно ниже.

## Exact-source compiler record — 2026-10-07

[Общий ledger](../VERIFICATION.md#exact-clean-source-sdk-syntaxtype-check-2026-10-07)
records 13/13 syntax/type PASS at clean source
`ef4e90b1c96c6a9a1cb34b5c2260b2561b20e7eb`, supplied SDK25.6build61,
Apple Clang21 arm64, including cookbook recipes. This is an identified compiler
snapshot, not a rerun at today's publication head, link/resource inspection or
AE runtime result. Later editorial reconciliation did not change these C++ recipes.

## Текущий контракт и source examples

Baseline Cookbook — supplied SDK **25.6 build 61**. [Exact-header audit от 2026-10-01](../18-SDK-HEADER-TOOLS/17-SDK25.6-CONTRACT-AUDIT-2026-10-01.md) фиксирует 35/35 required contracts и 39/39 cookbook call-sites для указанного в нём источника. Более поздние corrections перечислены отдельно в [ledger](../VERIFICATION.md#current-suite-manifest-correction); это не новая проверка всей текущей редакции.

| Материал | Что поддерживает запись | Чего запись не подтверждает |
|---|---|---|
| Главы со ссылками на exact SDK reviews | Декларации, suite generations и разобранные ownership contracts в указанной поставке | Link, host execution и совместимость любого будущего SDK |
| Текущие `code/*.cpp` | SOURCE EXAMPLE; source corrections и SDK-CONTRACT-REVIEWED участки, где указаны источники | Успешную компиляцию нынешнего source tree или выполнение в AE |
| Adobe sample patterns | Устройство операции в конкретном образце и версии | Production-корректность любой адаптации |
| Notes о later SDK generations, включая 26.5 | Отдельный датированный public-source контекст | Наличие этих suites в supplied SDK 25.6 или проверку proprietary later headers |

Суффикс структуры suite, версия AcquireSuite, версия SDK и AE build — разные значения. Следуйте [таблице функций](16-SUITE-FUNCTION-MAP.md) и конкретной source-review записи; не переносите later-generation API в baseline 25.6 без явного adapter/version boundary.

## Как получить evidence для собственного продукта

Если recipe используется в продукте, зафиксируйте его source commit/хэши, exact SDK и compiler, сохраните команды и per-file результаты syntax/type check. Для заявления о работе в AE дополнительно нужны идентичность linked artifact, AE build, OS/architecture, сценарий, ожидаемый и наблюдаемый результат. Матрица платформ определяется обещаниями самого продукта.

Результаты компиляции, линковки и host execution записываются отдельно. Не заменяйте NOT RUN на PASS по наличию source review или зелёной документационной CI.

Редакционное состояние Cookbook — **SOURCE EXAMPLE / SDK-CONTRACT-REVIEWED где указано / RUNTIME-NOT-CLAIMED**. Проверки продуктов полезны для их конкретных claims; готовность документации определяется [редакционным чеклистом](../COMPLETION-CHECKLIST.md).
