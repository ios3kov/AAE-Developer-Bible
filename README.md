# AE Developer Bible

**Практическая библия по разработке инструментов, скриптов, панелей и нативных plug-in'ов для Adobe After Effects.**

Research snapshot: **2026-10-01**  

**Canonical writing/editing rules:** [EDITORIAL-GUIDE.md](EDITORIAL-GUIDE.md)  
Status: **working editorial edition — real SDK 25.6 contract-reviewed knowledge base**

## Цель

AE Developer Bible — это **база знаний**, а не отдельный программный продукт и не набор плагинов, которые репозиторий обязан собрать и прогнать внутри After Effects.

Она должна отвечать разработчику на практические вопросы:

- какой тип расширения выбрать;
- как устроены Effect / AEGP / AEIO / Artisan / scripting / panels;
- какие lifecycle, suite, ownership, threading и ABI-контракты действуют;
- как проектировать CPU/GPU/MFR, UI и hybrid-архитектуру;
- как собирать, отлаживать, тестировать, подписывать и распространять продукт;
- какие ошибки встречаются в официальных samples, старых API и реальных проектах;
- какие решения являются документированными фактами, наблюдениями, реконструкцией или рекомендациями.

**Готовность Bible определяется полнотой, точностью, практичностью и согласованностью документации.**

Компиляция всех C++-фрагментов, сборка всех примеров, запуск каждого примера в AE, Windows build, signing/notarization и exhaustive host matrix **не являются условиями готовности самой Bible**. Эти действия описываются как процессы, которые должен применять разработчик своего продукта.

## Источники истины

Для version-sensitive native API приоритет такой:

1. фактические headers нужного Adobe SDK;
2. официальные SDK samples и комментарии;
3. официальная документация Adobe и platform vendors;
4. датированные исследовательские наблюдения;
5. реконструкция и архитектурные рекомендации — только с явной маркировкой.

Для текущей редакции реальный Adobe After Effects SDK **25.6 build 61** сверён по обязательному контрактному baseline: **35/35 required contracts** и **39/39 cookbook call-sites** разрешаются в нужных suite generations. Это проверка точности документации и source examples, а не требование собрать Bible как приложение.

## Как читать уровни доказательности

- **DOCUMENTED** — утверждение опирается на опубликованный контракт/документацию.
- **SDK-CONTRACT-REVIEWED** — version-sensitive утверждение сверено с фактическим SDK header/sample.
- **SOURCE EXAMPLE** — пример показывает форму решения и integration pattern; это не обещание готового бинарника.
- **PROJECT-REPORTED / RUNTIME-OBSERVED** — сохранён конкретный результат реального проекта/запуска с указанной границей применимости.
- **RECONSTRUCTED** — вывод восстановлен по evidence и не выдаётся за публичный контракт.

Отсутствие runtime evidence у source example означает только **«Bible не заявляет этот runtime result»**, а не «Bible обязана теперь собрать и протестировать этот пример».

## Главный принцип

Сначала выбирается **правильный тип расширения**, и только потом технология:

| Задача | Основной путь |
|---|---|
| Обработать пиксели / создать эффект | C++ Effect plug-in |
| Глубоко управлять проектом/AE, меню, hooks | AEGP |
| Импорт/экспорт собственного медиаформата | AEIO |
| Заменить 3D-renderer AE | Artisan — только при реальной необходимости |
| Автоматизировать проект, слои, render queue | ExtendScript |
| Сделать dockable UI-панель | CEP сейчас; UXP — план миграции |
| Высокая скорость + UI | Hybrid: native C++ + panel/script bridge |

## Что читать сначала

1. [Decision tree](00-START-HERE/00-DECISION-TREE.md)
2. [Extension types](00-START-HERE/01-EXTENSION-TYPES.md)
3. Ветка своей платформы:
   - [macOS](08-MACOS/README.md)
   - [Windows](09-WINDOWS/README.md)
4. Для C++ effect plug-in — [Effect plug-ins](02-EFFECT-PLUGINS/README.md)
5. Для production/release процесса — [Distribution](11-DISTRIBUTION/03-RELEASE-CHECKLIST.md)

## Структура

~~~text
00-START-HERE/       выбор архитектуры и технологии
01-ARCHITECTURE/     lifecycle, PiPL, ABI, memory, performance
02-EFFECT-PLUGINS/   effects, SmartFX, MFR, GPU, UI, color, audio
03-AEGP/             глубокая интеграция с AE
04-AEIO/             import/export
05-ARTISAN/          custom 3D renderer
06-SCRIPTING/        ExtendScript / ScriptUI / expressions
07-PANELS/           CEP и переход на UXP
08-MACOS/            Xcode, Universal, debug, signing, notarization
09-WINDOWS/          Visual Studio, x64/ARM64, debug, signing
10-TESTING/          correctness, MFR, GPU/CPU, perf, crashes
11-DISTRIBUTION/     versioning, packaging, release
12-RECIPES/          практические сценарии
13-TEMPLATES/        bug/spec/compatibility/release templates
14-NATIVE-INTEGRATIONS/ taxonomy native integration types
15-COMMUNICATION/    AE, plug-ins, scripts и panels
16-WORKING-TEMPLATES/ source-shaped integration examples
17-NATIVE-SUITE-COOKBOOK/ suite-by-suite recipes
18-SDK-HEADER-TOOLS/ exact SDK contract inventory/audit helpers
19-NATIVE-CODE-FOUNDATION/ ownership/undo/ABI helpers
20-REFERENCE-IMPLEMENTATIONS/ reference source maps
21-BUILTIN-EFFECTS-REVERSE-ENGINEERING/ research atlas
22-PROJECT-CASE-STUDIES/ real-project lessons
~~~

## Что означает «готовая редакция»

Редакция готова, когда:

- основные типы разработки и ключевые workflows покрыты;
- version-sensitive native claims сверены с выбранным SDK baseline;
- публичные, SDK-derived, observed и reconstructed утверждения разделены;
- рецепты и source examples не противоречат объясняющим главам;
- неизвестные и ограничения указаны прямо;
- platform/build/test/release guidance полна как инструкция;
- источники и provenance сохранены;
- навигация, ссылки, generated MASTER/manifest и docs build согласованы.

См. [completion plan](COMPLETION-PLAN.md), [editorial checklist](COMPLETION-CHECKLIST.md) и [coverage matrix](FINAL-COVERAGE-AUDIT.md).

## Состояние UXP / CEP на дату снимка

Adobe 24 сентября 2026 объявила расширение UXP на After Effects. Public beta UXP для After Effects заявлена к ноябрю 2026. На дату этой редакции это **датированный planning fact**, а не уже проверенный AE UXP API.

Практическое правило текущей редакции:

- heavy render/effect code → C++ SDK;
- production panel сейчас → CEP с отделённой business logic;
- UXP учитывать как migration target;
- не путать будущий roadmap с доступным контрактом.

## Что эта база не делает

- Не перепечатывает Adobe SDK Guide.
- Не подменяет лицензированные SDK headers и samples.
- Не обещает, что source example является готовым коммерческим бинарником.
- Не превращает отсутствие собственного host-run в дефект документации.
- Не считает внутренние/недокументированные API production-контрактом.
- Не требует собрать все описанные технологии, чтобы доказать существование или правильность их документированных контрактов.

## Editorial rules

Все правила написания, source hierarchy, evidence vocabulary, block-by-block workflow и definition of done собраны в одном каноническом документе:

[**EDITORIAL-GUIDE.md**](EDITORIAL-GUIDE.md)

Если другой planning/status документ формулирует правило иначе, применяется Editorial Guide.

## Источники

См. [SOURCES.md](SOURCES.md). Источники разделены на official/canonical, SDK source review, community-maintained guides и secondary/research evidence.
