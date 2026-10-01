# План доведения AE Developer Bible до готовой редакции

Updated: **2026-10-01**

Canonical writing rules: [EDITORIAL-GUIDE.md](EDITORIAL-GUIDE.md). This file contains the roadmap, not a second rulebook.

## Цель

AE Developer Bible должна стать **полной, точной и практической базой знаний по разработке для Adobe After Effects**.

Готовая редакция не обязана сама быть набором собранных plug-in binaries. Её задача — дать разработчику правильную архитектуру, version-sensitive контракты, workflows, ограничения, типичные ошибки, recipes и критерии проверки **его собственного продукта**.

## Что не является условием готовности Bible

Для завершения редакции **не требуется**:

- компилировать весь C++ из репозитория;
- собирать Minimal Gain / SmartFX / MenuTool как отдельный QA-проект;
- прогонять каждый source example внутри After Effects;
- делать обязательный Windows build всех примеров;
- подписывать/notarize/AuthentiCode демонстрационные binaries;
- завершать весь research atlas встроенных эффектов;
- превращать source recipes в коммерчески готовые plugins.

Если runtime/build evidence уже существует, Bible сохраняет его и аккуратно ограничивает выводы. Если его нет, Bible просто не заявляет этот runtime result.

## Критерии готовой редакции

### 1. Coverage

Покрываются extension selection, native families, scripting/panels, memory/threading, platforms, debugging/testing, packaging/distribution, recipes и templates.

### 2. Source accuracy

Для native API:

~~~text
exact SDK header/sample
→ Bible explanation
→ source-shaped recipe/example
~~~

Текущий baseline: Adobe After Effects SDK **25.6 build 61**.

Real SDK audit 2026-10-01:

- 35/35 required contracts;
- 39/39 cookbook call-sites;
- 0 required parser diagnostics.

Это достаточная contract-level проверка редакционной точности текущих native глав. Compiler helpers могут использоваться дополнительно разработчиком, но не являются completion gate Bible.

### 3. Evidence discipline

Bible различает:

- DOCUMENTED;
- SDK-CONTRACT-REVIEWED;
- PROJECT-REPORTED / RUNTIME-OBSERVED;
- RECONSTRUCTED;
- recommendation/design guidance.

Отсутствие host-run не должно превращаться в искусственный TODO, если текст не заявляет host-observed результат.

### 4. Practical usefulness

Каждый практический раздел должен объяснять:

- когда использовать технологию;
- когда её не использовать;
- architecture/lifecycle;
- основные entry points/suites/contracts;
- ownership/lifetime/threading;
- platform/version caveats;
- production workflow;
- debugging/testing guidance;
- частые ошибки;
- related recipes/templates.

### 5. Editorial consistency

README, STATUS, coverage, source-review records, recipes и examples не должны противоречить друг другу.

### 6. Research appendices

Разделы 21–22 дают дополнительную практическую ценность и могут развиваться после выпуска core Bible. Полный каталог всех bundled effects не блокирует core edition.

### 7. Editorial release

Перед фиксацией редакции:

- проверить navigation и links;
- проверить provenance/licensing notes;
- пересобрать generated MASTER/manifest;
- выполнить strict documentation build;
- зафиксировать research date;
- обновить changelog/version.

## Этапы

| Этап | Содержание | Статус |
|---|---|---|
| **A. Scope & taxonomy** | структура, decision tree, типы расширений, платформы | **готово** |
| **B. Core technical coverage** | Effect/AEGP/AEIO/Artisan/scripting/panels/platform/testing/distribution | **основной массив написан** |
| **C. SDK/source accuracy** | source reviews, real SDK 25.6 contract audit, errata/version boundaries | **baseline готов** |
| **D. Consistency & practical sweep** | пройти главу за главой, убрать противоречия, дополнить слабые места, проверить recipes/templates | **текущий этап** |
| **E. Research appendices** | atlas/case studies | **ongoing, non-blocking** |
| **F. Editorial release** | links/nav/provenance/generated docs/changelog/freeze | **после D** |

## Текущий приоритет

**Продолжать писать и редактировать Bible.**

Следующая работа:

1. пройти основные разделы по единому шаблону полноты;
2. найти слабые/короткие главы;
3. найти старые или конфликтующие формулировки;
4. связать source-review findings с основными главами;
5. привести examples/recipes к единой evidence vocabulary;
6. завершить финальный editorial audit.

[COMPLETION-CHECKLIST.md](COMPLETION-CHECKLIST.md) является текущим редакционным чеклистом.
