# Built-in Effects Reverse Engineering

Цель раздела — поштучно разобрать эффекты, которые поставляются с Adobe After Effects, **по реальным установленным бинарникам**, а не реконструировать их только по пользовательской документации.

Baseline каталога: официальный Adobe **After Effects effect list**, updated 2026-05-13. Adobe описывает его как список всех эффектов After Effects и публикует для эффектов MFR/GPU/bit-depth capabilities.

## Правило доказательности

Для каждого эффекта разделяем:

1. **Documented** — имя, категория, MFR/GPU/bit depth из Adobe documentation.
2. **Binary observed** — фактический .plugin/.aex/module, architecture, hashes, PiPL/resources, imports/exports, strings/symbols.
3. **Runtime observed** — callbacks/selectors, parameter tree, CPU/GPU behavior, threading, render characteristics.
4. **Reconstructed** — вероятная внутренняя архитектура/алгоритм, всегда отдельно от доказанных фактов.
5. **Reimplementation recipe** — как построить функционально аналогичный SDK effect без копирования Adobe code.

Нельзя угадывать match name или имя binary. Пока они не извлечены из установленного AE, значение — `TO VERIFY FROM INSTALLED AE`.

## Главный каталог

[MASTER-EFFECT-LIST.md](MASTER-EFFECT-LIST.md)

## Карточка будущего анализа

| Field | Meaning |
|---|---|
| Display name | UI name from Adobe catalog / AE |
| Category | Adobe Effects & Presets category |
| Match name | only when observed/evidenced |
| Binary | actual .plugin/.aex/module only when observed |
| macOS / Windows | mapping may differ |
| PiPL / registration | observed resource/registration data |
| MFR / GPU / bpc | documented + runtime verification |
| Parameters | actual parameter tree and types |
| Host calls / suites | observed/reconstructed interaction with AE |
| CPU path | static/runtime findings |
| GPU path | static/runtime findings |
| Dependencies | imported frameworks/DLLs |
| Threading / memory | observed behavior |
| Algorithm | evidence-backed reconstruction |
| Confidence | documented / observed / reconstructed |
| Reimplementation | SDK architecture for analogous behavior |

## Scope

The master list includes bundled entries that Adobe itself lists (for example Mocha AE and CINEWARE), but marks them separately so bundled third-party/external technology is not confused with Adobe-native effect binaries.
