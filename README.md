# AE Developer Bible

**Практическая библия разработчика инструментов, скриптов, панелей и нативных plug-in'ов для Adobe After Effects.**

Research snapshot: **2026-09-30**  
Status: **v1.0 — native-first final reference edition**

Эта база отвечает не на вопрос «что есть в API», а на вопрос **«как правильно спроектировать, собрать, отладить, протестировать и выпустить инструмент для After Effects»**.

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

1. [`00-START-HERE/00-DECISION-TREE.md`](00-START-HERE/00-DECISION-TREE.md)
2. [`00-START-HERE/01-EXTENSION-TYPES.md`](00-START-HERE/01-EXTENSION-TYPES.md)
3. Затем ветку своей платформы:
   - [`08-MACOS/README.md`](08-MACOS/README.md)
   - [`09-WINDOWS/README.md`](09-WINDOWS/README.md)
4. Для C++ effect plug-in — [`02-EFFECT-PLUGINS/README.md`](02-EFFECT-PLUGINS/README.md)
5. Перед релизом — [`11-DISTRIBUTION/03-RELEASE-CHECKLIST.md`](11-DISTRIBUTION/03-RELEASE-CHECKLIST.md)

## Структура

```text
00-START-HERE/       выбор архитектуры и технологии
01-ARCHITECTURE/     общая архитектура SDK, lifecycle, PiPL, ABI
02-EFFECT-PLUGINS/   эффекты, SmartFX, MFR, GPU, UI, color
03-AEGP/             глубокая интеграция с AE
04-AEIO/             import/export
05-ARTISAN/          custom 3D renderer
06-SCRIPTING/        ExtendScript / ScriptUI / expressions
07-PANELS/           CEP и переход на UXP
08-MACOS/            Xcode, Universal, debug, signing, notarization
09-WINDOWS/          Visual Studio, x64/ARM64, debug, signing
10-TESTING/          correctness, MFR, GPU/CPU, perf, crashes
11-DISTRIBUTION/     versioning, packaging, release
12-RECIPES/          практические пошаговые сценарии
13-TEMPLATES/        шаблоны ТЗ, bug report, compatibility matrix
14-NATIVE-INTEGRATIONS/ полный taxonomy нативных C++ integration types
15-COMMUNICATION/      как AE, plug-ins, scripts и panels общаются
16-WORKING-TEMPLATES/  рабочие drop-in C++/JSX/CEP шаблоны
17-NATIVE-SUITE-COOKBOOK/ suite-by-suite native recipes + C++ drop-ins
18-SDK-HEADER-TOOLS/     generate/verify/diff exact native SDK contracts
19-NATIVE-CODE-FOUNDATION/ reusable suite/ownership/undo ABI helpers
20-REFERENCE-IMPLEMENTATIONS/ native-first copyable reference implementations
```


## Финальный слой v1.0

- Добавлен `20-REFERENCE-IMPLEMENTATIONS`: native-first карта copyable implementations для Effect, SmartFX/MFR, Custom UI/Drawbot, AEGP, Keyframer, native panels, AEIO, Artisan, Effect↔AEGP, PICA и ScriptUI.
- Добавлен `FINAL-COVERAGE-AUDIT.md`, который напрямую сопоставляет требования библии с конкретными разделами.
- Уточнён статус примеров: `drop-in`, `sample-derived`, `host-test-required`. Нативный пример не называется host-verified без реальной загрузки в After Effects.

## Новое в v0.4

- Добавлен header-derived API inventory: локальный Adobe SDK автоматически превращается в точный Suite/FunctionBlock → function → signature index.
- Генератор охватывает AEGP, PF/Effect, AEIO function blocks, Artisan/PR entry points, Drawbot и другие native function tables.
- Добавлены `verify_recipe_symbols.py` и `diff_sdk_inventory.py`: проверка cookbook calls против конкретного SDK и diff двух SDK versions.
- Добавлены отдельные launchers для macOS (`run-macos.sh`) и Windows (`run-windows.ps1`).
- Добавлен native C++ foundation: PICA suite acquire/release, move-only owners для stream/effect/frame/memory handles, undo scope и exception boundary.
- Python tooling проходит unit test; C++ foundation проходит strict C++17 compile (`-Wall -Wextra -Werror`) против синтетического ABI-stub.
- Это не заменяет compile/load test с реальным Adobe SDK + After Effects host.

## Новое в v0.3

- Suite-by-suite native cookbook: project/items/comps/layers/effects/streams/keyframes/masks/text/render/render queue/guides.
- Добавлен function map по основным AEGP suites: какой вызов за что отвечает.
- Добавлены новые compile-shaped C++ drop-ins для project traversal, comp/layer, effect/stream, keyframes, frame checkout и render queue.
- Добавлен `14-NATIVE-INTEGRATIONS/13-DOCS-ERRATA.md`: зафиксированы ошибки/опечатки публичного HTML guide и правило «headers are source of truth».
- Введены уровни доверия `SDK-verified`, `sample-derived`, `host-test-required`.
- Исправлены найденные при перепроверке сигнатур ошибки до релиза v0.3 (`CreateComp` framerate, mask API, render-queue state, LayerID type).

## Новое в v0.2

- Полная taxonomy нативных integration types: Effect, AEGP, Keyframer, native panel, AEIO, Artisan, Interactive Artisan, BlitHook, shared PICA suites и legacy paths.
- Отдельная карта внутренней коммуникации: selectors, hooks, PICA, generic Effect calls, scripting и CEP bridge.
- Working templates: Minimal Gain Effect, AEGP menu tool, Effect↔AEGP message protocol, PICA shared-suite ABI, standalone JSX и CEP JSON bridge.
- Зафиксировано правило: C++ templates graft-ятся в официальный SDK sample, чтобы не ломать PiPL/platform build plumbing.

## Состояние UXP / CEP на дату снимка

Adobe 24 сентября 2026 объявила расширение UXP на After Effects. **Public beta UXP для After Effects заявлена к ноябрю 2026**, поэтому на дату этой базы UXP нельзя считать стабильным production-путём для AE. CEP остаётся рабочим legacy-путём, но Adobe объявила его постепенный вывод; полный retirement заявлен к концу 2029.

Практическое правило на сегодня:

- новый тяжёлый render/effect код → **C++ SDK**;
- новая панель, которую надо выпустить прямо сейчас → **CEP**, но архитектуру отделять от UI, чтобы облегчить UXP migration;
- не зашивать бизнес-логику в CEP DOM/Node-код без слоя абстракции.

## Что эта база не делает

- Не перепечатывает Adobe SDK Guide.
- Не подменяет headers и sample projects из официального SDK.
- Не обещает бинарную совместимость без тестирования.
- Не считает внутренние/недокументированные API допустимым production-контрактом.

## Golden rules

1. Для native-разработки **стартуй от ближайшего Adobe sample**, а не с пустого Xcode/Visual Studio проекта.
2. Один `.r`/PiPL источник — для macOS и Windows.
3. Никогда не выпускай MFR-флаг, пока render path не доказанно thread-safe.
4. Не держи mutex, вызывая обратно host API.
5. Не позволяй C++ exception пересечь `extern "C"` entry point.
6. Результат CPU и GPU должен быть визуально/численно эквивалентен в пределах заранее заданной tolerance.
7. Каждый заявленный AE version и architecture — отдельная строка test matrix.
8. Signing/notarization — часть build pipeline, а не ручной финальный ритуал.
9. Любая оптимизация принимается только после profiling и regression test.
10. «Работает у разработчика» ≠ «готово к релизу».

## Источники

См. [`SOURCES.md`](SOURCES.md). Источники разделены на canonical/official, community-maintained Adobe SDK guides и secondary references.
