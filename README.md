# AAE Developer Bible

**Практическая библия разработчика нативных plug-ins, AEGP tools, import/export, render integrations, scripts и panels для Adobe After Effects.**

Snapshot: **2026-09-30**  
Release: **v1.0**  
Primary native reference: **After Effects SDK 26.5**

## Что она закрывает

1. Правильная taxonomy всех основных документированных путей интеграции — **сначала native**.
2. Как AE вызывает Effect/AEGP/AEIO/Artisan и как plug-in вызывает host suites/callbacks.
3. Как native-модули общаются между собой: PICA и `AEGP_EffectCallGeneric`.
4. Как JSX / ScriptUI / CEP общаются с AE.
5. Отдельный production path для **macOS** и **Windows**.
6. Готовые reference implementations и host-independent cores, которые graft-ятся в официальный Adobe SDK sample-shell.
7. SDK-header tools, которые строят точный inventory API для реально установленной версии SDK.
8. Обязательный host verification gate: compile → load → smoke → teardown.

## Начать отсюда

1. [`00-START-HERE/00-DECISION-TREE.md`](00-START-HERE/00-DECISION-TREE.md)
2. [`14-NATIVE-INTEGRATIONS/01-TAXONOMY.md`](14-NATIVE-INTEGRATIONS/01-TAXONOMY.md)
3. [`15-COMMUNICATION/README.md`](15-COMMUNICATION/README.md)
4. [`20-REFERENCE-IMPLEMENTATIONS/README.md`](20-REFERENCE-IMPLEMENTATIONS/README.md)
5. [`21-HOST-VERIFICATION/README.md`](21-HOST-VERIFICATION/README.md)
6. platform: [`08-MACOS/README.md`](08-MACOS/README.md) / [`09-WINDOWS/README.md`](09-WINDOWS/README.md)

## Категории

```text
00-START-HERE/            выбор технологии
01-ARCHITECTURE/          lifecycle, ABI, PiPL, performance
02-EFFECT-PLUGINS/        Effect / SmartFX / MFR / GPU / UI / audio
03-AEGP/                  AEGP hooks/suites/tools
04-AEIO/                  media I/O
05-ARTISAN/               custom 3D renderer
06-SCRIPTING/             ExtendScript / ScriptUI
07-PANELS/                CEP / UXP transition
08-MACOS/                 macOS/Xcode/sign/notarize
09-WINDOWS/               Windows/VS/sign/package
10-TESTING/               correctness/perf/crashes
11-DISTRIBUTION/          shipping/versioning
12-RECIPES/               task-oriented recipes
13-TEMPLATES/             engineering docs/templates
14-NATIVE-INTEGRATIONS/   canonical native taxonomy
15-COMMUNICATION/         all supported communication paths
16-WORKING-TEMPLATES/     compact drop-ins
17-NATIVE-SUITE-COOKBOOK/ AEGP recipes
18-SDK-HEADER-TOOLS/      exact header inventory/diff/verifier
19-NATIVE-CODE-FOUNDATION/RAII/ownership/undo helpers
20-REFERENCE-IMPLEMENTATIONS/ complete reference layer
21-HOST-VERIFICATION/     real AE compile/load/smoke gate
```

## Native-first rule

Effect → AEGP → specialized AEGP (AEIO/Artisan) → display/output hooks are documented before scripting/panels. The Bible does not mix a render Effect with project automation, and does not pretend CEP/JSX can directly call private native pointers.

## Build rule

Adobe recommends starting from the closest official SDK sample rather than a blank project. The Bible therefore does **not** vendor Adobe proprietary SDK/project files. It provides our source, adapters, contracts and exact graft instructions; the installed Adobe SDK supplies headers, PiPL/resources and sample project-shells.

## Verification truth

`SDK-verified` means the API contract is checked against current docs/headers/sample pattern. It does **not** mean a binary was executed in AE on this machine. Native shipping status requires the evidence in [`21-HOST-VERIFICATION`](21-HOST-VERIFICATION/README.md).

## Current panel note

As of this snapshot, CEP remains the practical legacy panel path while UXP support for After Effects transitions toward public beta/production. Keep panel UI separate from business/native logic so the front end can be replaced without rewriting the engine.

## Sources

See [`SOURCES.md`](SOURCES.md). Canonical Adobe docs/SDK headers and official sample projects take priority over secondary references.
