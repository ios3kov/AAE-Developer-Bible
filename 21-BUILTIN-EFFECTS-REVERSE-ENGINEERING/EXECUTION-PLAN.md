# Built-in Effects Reverse Engineering — Execution Plan

Status: **approved plan**  
Date: **2026-09-30**

## Goal

Поштучно разобрать реализацию каждого штатного/bundled эффекта After Effects на основе **фактической установки и реальных бинарников**, а не только пользовательской документации.

Документация Adobe используется как контроль полноты и источник documented capabilities. Реализация определяется только по наблюдаемым данным установленного AE.

## Classification

Каждый эффект в `MASTER-EFFECT-LIST.md` должен получить один implementation class:

- **HOST-BUILTIN** — реализация находится внутри executable/frameworks/libraries самого After Effects.
- **SHIPPED-PLUGIN** — эффект поставляется отдельным Adobe `.plugin` / `.aex` или отдельным native module.
- **BUNDLED-THIRD-PARTY** — поставляется с AE, но реализация принадлежит стороннему поставщику.
- **UNKNOWN** — mapping ещё не доказан.

Не выводить класс из одного только отсутствия отдельного файла. `HOST-BUILTIN` требует положительного binary/runtime evidence.

## Evidence levels

Каждое утверждение маркируется:

- **DOCUMENTED** — подтверждено документацией Adobe/поставщика.
- **PROVEN** — непосредственно подтверждено binary/resource/registration evidence.
- **OBSERVED** — подтверждено контролируемым runtime experiment.
- **RECONSTRUCTED** — вывод из доказательств; исходный код не известен.
- **UNKNOWN** — данных недостаточно.

Match name, binary name, internal function, GPU path и algorithm нельзя угадывать.

## Phase 1 — installation inventory

Отдельно для macOS и Windows собрать:

- After Effects executable;
- frameworks / dylibs / DLLs;
- `.plugin` / `.aex`;
- resources / PiPL;
- bundled third-party modules;
- versions;
- architectures;
- code-signing metadata;
- SHA-256.

Результат: machine-readable inventory + human-readable report.

## Phase 2 — Effect → implementation map

Для каждого эффекта определить, насколько позволяет evidence:

```text
Display Name
→ Match Name
→ Classification
→ Binary / executable / framework
→ Registration evidence
→ Category
→ Bit depth
→ MFR
→ GPU
```

Первый результат должен быть полной таблицей всех эффектов, даже если часть строк остаётся `UNKNOWN`.

## Phase 3 — HOST-BUILTIN first

Первый приоритет — эффекты, доказанно встроенные в host.

Начальная очередь следует `MASTER-EFFECT-LIST.md`.

Первый target: **3D Channel → 3D Channel Extract**.

Для HOST-BUILTIN анализировать:

```text
After Effects executable/framework
→ match-name / UI-name strings
→ registration/resources
→ xrefs
→ relevant functions
→ parameters
→ host interaction
→ CPU path
→ GPU path
→ threading/memory
→ reconstructed render pipeline
```

## Phase 4 — static analysis

Для каждого target:

- Mach-O / PE metadata;
- sections/resources;
- imports/exports;
- strings;
- symbols when present;
- PiPL/registration structures;
- xrefs from effect/match-name evidence;
- parameter-related constants/tables;
- SIMD/vector paths;
- GPU/Metal/Windows GPU references;
- threading primitives;
- memory allocation patterns;
- relevant disassembly/decompiler output.

Raw evidence and interpretation must remain separate.

## Phase 5 — runtime analysis

Create minimal reproducible AE projects and probes for:

- parameter tree/defaults/ranges;
- 8/16/32-bpc behavior;
- alpha handling;
- ROI;
- edge behavior;
- CPU/GPU switching;
- MFR/concurrent frames;
- deterministic output;
- unusual dimensions/origins;
- cancellation;
- numerical response to controlled input images.

Record AE build, OS, architecture, project, input and output hashes.

## Phase 6 — algorithm reconstruction

Produce an evidence-backed pipeline:

```text
INPUT
→ preprocessing
→ parameter conversion
→ core operation
→ color/pixel handling
→ edge/ROI handling
→ OUTPUT
```

Never present decompiler interpretation as original Adobe source.

## Phase 7 — reimplementation template

After each effect analysis, create an independent SDK reference implementation demonstrating the same architectural/algorithmic concept without copying Adobe code.

Each effect directory:

```text
<Category>/<Effect>/
├── README.md
├── ANALYSIS.md
├── BINARY-EVIDENCE.md
├── PARAMETERS.md
├── RENDER-PIPELINE.md
├── GPU.md
├── RUNTIME-TESTS.md
├── REIMPLEMENTATION.md
└── template/
```

The template must state its own verification level.

## Phase 8 — remaining implementation classes

Order:

1. HOST-BUILTIN
2. SHIPPED-PLUGIN
3. BUNDLED-THIRD-PARTY

Third-party implementations remain clearly separated from Adobe-native architecture.

## Phase 9 — platform order

### macOS

Build the complete first evidence map and effect analyses on macOS.

### Windows

Repeat against the Windows installation and compare:

- Mach-O ↔ PE;
- framework/dylib ↔ DLL/module;
- registration differences;
- CPU implementations;
- GPU backend differences;
- architecture/compiler differences;
- effect behavior/output equivalence.

Do not assume the Windows binary mapping matches macOS.

## Per-effect Definition of Done

An effect is **analysed** only when:

- classification has evidence;
- display name and match name are recorded where obtainable;
- implementation binary/module is identified where obtainable;
- parameters are documented;
- render behavior has controlled tests;
- CPU/GPU/MFR status is recorded;
- static evidence is linked;
- reconstructed pipeline is clearly distinguished from proven facts;
- unknowns are listed;
- reimplementation recipe exists.

An effect is **host-verified** only after its recorded runtime tests pass on a named AE build/platform.

## Immediate next step

Build the macOS installation scanner and generate the first:

`Effect → HOST-BUILTIN / SHIPPED-PLUGIN / BUNDLED-THIRD-PARTY / UNKNOWN → binary/module`

mapping.

Then begin the first full analysis with **3D Channel Extract**.
