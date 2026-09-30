# Native integrations — карта всего нативного SDK After Effects

Research baseline: **After Effects 26.5 SDK (September 2026)**.

Этот раздел отвечает на вопрос: **какие типы нативных расширений реально существуют в After Effects, кто вызывает кого и для каких задач нужен каждый тип**.

## 1. Нативные категории

| Категория | Кто инициирует работу | Главный контракт | Для чего |
|---|---|---|---|
| Effect plug-in | After Effects | `EffectMain(PF_Cmd, ...)` | Пиксели, аудио, параметры, custom UI, SmartFX/GPU |
| AEGP | After Effects + hooks | PICA suites + registered hooks | Проект, слои, keyframes, меню, render queue, automation |
| Keyframer | AEGP specialization | AEGP stream/keyframe suites | Keyframe Assistant / пакетная работа с keyframes |
| Native dockable panel | AEGP/panel API | native panel callbacks | Нативная dockable UI-панель |
| AEIO | specialized AEGP | `AEGP_RegisterIO()` + function block | Собственный media input/output |
| Artisan | specialized AEGP | `AEGP_RegisterArtisan()` + render entry points | Замена 3D renderer композиции |
| Interactive Artisan | specialized AEGP | `AEGP_RegisterInteractiveArtisan()` | Interactive 3D preview/render |
| BlitHook | native display hook | frame/display callback stream | Получать кадры, выводимые Composition panel |
| Shared PICA suite provider | AEGP/native module | published function suite | Общая native-служба для нескольких plug-ins |
| Legacy format/filter APIs | legacy | старые Photoshop/FPF contracts | Только поддержка старого кода; не начинать новый продукт |

## 2. Что не является отдельным native plug-in type

- **SmartFX** — расширенный render path Effect API, а не отдельный тип plug-in.
- **MFR** — модель многокадрового исполнения Effect API.
- **GPU effect** — Effect plug-in с GPU selectors/suites.
- **Custom UI / Drawbot** — UI-механизм Effect API.
- **Audio effect** — режим Effect API.
- **CEP / UXP / ExtendScript** — отдельный JS-слой, не C++ native plug-in type.

## 3. Правильный выбор

```text
Нужно менять изображение/аудио?
  -> Effect

Нужно менять проект, слои, keyframes, меню, render queue?
  -> AEGP

Нужно добавить формат медиа?
  -> AEIO (или современный MediaCore importer, если подходит задача)

Нужно заменить 3D renderer композиции?
  -> Artisan

Нужно получать отображаемые кадры?
  -> BlitHook

Нужно красивое HTML UI + automation?
  -> CEP сейчас / UXP после production readiness

Нужно высокоскоростное ядро + удобная панель?
  -> Native C++ core + panel/script bridge
```

## 4. Главное правило архитектуры

Не выбирать API по привычному языку программирования. Сначала определить, **кто владеет данными и кто должен инициировать вызов**:

- кадр и параметры эффекта принадлежат render graph AE → Effect API;
- project model принадлежит AE → AEGP suites;
- файл и его decoding/encoding lifecycle → AEIO;
- UI HTML → CEP/UXP, а изменение проекта выполняет ExtendScript/native bridge;
- shared high-performance service → native suite/IPC, но не чтение случайной общей памяти между plug-ins.

## Дальше

- [`01-TAXONOMY.md`](01-TAXONOMY.md) — полный taxonomy.
- [`02-HOST-CALL-FLOWS.md`](02-HOST-CALL-FLOWS.md) — жизненные циклы.
- [`03-PICA-SUITES.md`](03-PICA-SUITES.md) — внутренний «bus» C++ SDK.
- [`04-EFFECTS.md`](04-EFFECTS.md) — все подвиды Effect API.
- [`05-AEGP-TOOLS.md`](05-AEGP-TOOLS.md) — native tools через AEGP.
- [`06-KEYFRAMERS.md`](06-KEYFRAMERS.md) — Keyframe Assistant.
- [`07-NATIVE-PANELS.md`](07-NATIVE-PANELS.md) — native dockable panel.
- [`08-AEIO.md`](08-AEIO.md), [`09-ARTISAN.md`](09-ARTISAN.md), [`10-BLITHOOK.md`](10-BLITHOOK.md).
- [`11-LEGACY-NATIVE.md`](11-LEGACY-NATIVE.md) — deprecated/legacy.
- [`12-AEGP-SUITES-CATALOG.md`](12-AEGP-SUITES-CATALOG.md) — полный AEGP suite map 26.5.

Sources: Adobe C++ SDK Guide — What Can I Do, AEGP Overview, Sample Projects, AEIO, Artisan; SDK 26.5 history.

- [`13-DOCS-ERRATA.md`](13-DOCS-ERRATA.md) — known public-doc mismatches and verification policy.
