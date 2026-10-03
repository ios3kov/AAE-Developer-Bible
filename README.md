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

Контрактная опора редакции — реальный Adobe After Effects SDK **25.6 build 61**. [Сохранённый exact-header audit](18-SDK-HEADER-TOOLS/17-SDK25.6-CONTRACT-AUDIT-2026-10-01.md) и later consistency correction в [ledger](VERIFICATION.md#current-suite-manifest-correction) фиксируют **35/35 required contracts** и **39/39 cookbook call-sites** для рассмотренных снимков. Эти результаты не являются новой проверкой каждого текущего файла или требованием собрать Bible как приложение.

## Как читать уровни доказательности

- **DOCUMENTED** — утверждение опирается на опубликованный контракт/документацию.
- **SDK-CONTRACT-REVIEWED** — version-sensitive утверждение сверено с фактическим SDK header/sample.
- **SOURCE EXAMPLE** — пример показывает форму решения и integration pattern; это не обещание готового бинарника.
- **PROJECT-REPORTED / RUNTIME-OBSERVED** — сохранён конкретный результат реального проекта/запуска с указанной границей применимости.
- **RECONSTRUCTED** — вывод восстановлен по evidence и не выдаётся за публичный контракт.

Отсутствие runtime evidence у source example означает только **«Bible не заявляет этот runtime result»**, а не «Bible обязана теперь собрать и протестировать этот пример».

Работа над следующей редакцией ведётся по [плану](COMPLETION-PLAN.md). [Поглавный трекер](CHAPTER-COMPLETION-TRACKER.md) содержит конкретные оставшиеся результаты для всех 127 core pages и не смешивает их с историческими compiler/runtime записями.

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

1. Выберите тип расширения:
   [Decision tree](00-START-HERE/00-DECISION-TREE.md).
   Для сравнения вариантов используйте
   [Extension types](00-START-HERE/01-EXTENSION-TYPES.md).
2. Пройдите один маршрут «читать → повторить → проверить»:
   - [Первый Effect](NAVIGATION.md#route-effect).
   - [Automation tool / ScriptUI / CEP](NAVIGATION.md#route-automation).
   - [Native integration / AEGP](NAVIGATION.md#route-native).
3. Для остальных задач и точечного поиска используйте
   [полную навигацию](NAVIGATION.md).

Платформенные инструкции:
[macOS](08-MACOS/README.md) · [Windows](09-WINDOWS/README.md).

Перед выпуском своего продукта:
[Release checklist](11-DISTRIBUTION/03-RELEASE-CHECKLIST.md).

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

## Additional reference and notices

[Glossary](GLOSSARY.md) · [Known pitfalls](KNOWN-PITFALLS.md) · [Notices](NOTICE.md) · [Generated combined edition](MASTER-AE-DEVELOPER-BIBLE.md) · [Navigation decisions](NAVIGATION-AUDIT.md).

## Documentation validation lanes

Block 4 source validation passed locally and on GitHub for b6f99db (Linux/macOS). Later frozen/generated commits and main-only bot execution need their own evidence. Install the pinned documentation dependency set with `python -m pip install -r requirements-docs.txt`; constraints are in `requirements-docs.lock`. This fixes versions, not package hashes or an identical OS/Python environment.

- **Source validation:** run `python -m unittest discover -s tests/consistency -v` and `python scripts/check_docs_consistency.py`. Generate into an external temporary directory with `python scripts/build_docs.py --output-root /absolute/temporary/staging`; then use `--check --output-root` on that same directory. Copy mkdocs.yml there and build using that staged config. The checkout's older MASTER/MANIFEST are allowed during source editing.
- **Frozen/generated validation:** run `python scripts/build_docs.py --check` before regenerating anything. A stale MASTER or MANIFEST fails. Validate automatically chooses this lane for generated-only push commits; workflow_dispatch can explicitly select it.
- **Identity:** the MASTER header records a relocatable source-content SHA-256, excluding MASTER/MANIFEST. It is not a Git revision. CI reports checkout SHA, triggering SHA and PR head SHA separately. Bot commits retain a `Source-Git-SHA` trailer and report the resulting generated commit SHA.

Consistency tests check the actual request/success/error JSON examples in four CEP documents, the complete 127-row core inventory against nested menu/NAVIGATION, and three registered current evidence boundaries. They detect regressions and explicit unsupported CURRENT-COMPILE/RUNTIME/HOST claims; they do not certify every prose claim or execute AE. Existing source-driven CEP VM tests remain separate.
