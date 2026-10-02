# Navigation

## 00-START-HERE
- [Decision tree — что именно вы разрабатываете?](00-START-HERE/00-DECISION-TREE.md)
- [Extension types](00-START-HERE/01-EXTENSION-TYPES.md)
- [Environment matrix](00-START-HERE/02-ENVIRONMENT-MATRIX.md)

## 01-ARCHITECTURE
- [Native plug-in lifecycle](01-ARCHITECTURE/01-LIFECYCLE.md)
- [Memory, threading, errors](01-ARCHITECTURE/02-MEMORY-THREADING-ERRORS.md)
- [PiPL and plug-in loading](01-ARCHITECTURE/03-PIPL-AND-LOADING.md)
- [Version compatibility](01-ARCHITECTURE/04-VERSION-COMPATIBILITY.md)
- [Performance architecture](01-ARCHITECTURE/05-PERFORMANCE-ARCHITECTURE.md)
- [Build system strategy](01-ARCHITECTURE/06-BUILD-SYSTEM.md)
- [Communication architecture — one-page rulebook](01-ARCHITECTURE/07-COMMUNICATION-ARCHITECTURE.md)

## 02-EFFECT-PLUGINS
- [Anatomy of an Effect plug-in](02-EFFECT-PLUGINS/01-ANATOMY.md)
- [Parameters and Effect UI](02-EFFECT-PLUGINS/02-PARAMETERS-UI.md)
- [SmartFX](02-EFFECT-PLUGINS/03-SMARTFX.md)
- [Multi-Frame Rendering (MFR) and thread safety](02-EFFECT-PLUGINS/04-MFR-THREAD-SAFETY.md)
- [GPU effects](02-EFFECT-PLUGINS/05-GPU.md)
- [Pixels, color, alpha](02-EFFECT-PLUGINS/06-COLOR-PIXELS.md)
- [Audio effects](02-EFFECT-PLUGINS/07-AUDIO.md)
- [Effect plug-ins](02-EFFECT-PLUGINS/README.md)

## 03-AEGP
- [AEGP hooks and suites](03-AEGP/01-HOOKS-SUITES.md)
- [AEGP project and render automation](03-AEGP/02-PROJECT-RENDER-AUTOMATION.md)
- [AEGP](03-AEGP/README.md)

## 04-AEIO
- [AEIO — media import/export plug-ins](04-AEIO/README.md)

## 05-ARTISAN
- [Artisan](05-ARTISAN/README.md)

## 06-SCRIPTING
- [After Effects scripting object model](06-SCRIPTING/01-OBJECT-MODEL.md)
- [ScriptUI](06-SCRIPTING/02-SCRIPTUI.md)
- [Expressions vs scripts](06-SCRIPTING/03-EXPRESSIONS-VS-SCRIPTS.md)
- [ExtendScript scripting](06-SCRIPTING/README.md)

## 07-PANELS
- [CEP development](07-PANELS/01-CEP.md)
- [UXP transition for After Effects](07-PANELS/02-UXP-TRANSITION.md)
- [Panels: CEP now, UXP next](07-PANELS/README.md)

## 08-MACOS
- [macOS — Xcode setup](08-MACOS/01-XCODE-SETUP.md)
- [macOS — Apple Silicon / Universal binary](08-MACOS/02-UNIVERSAL-BINARY.md)
- [macOS — debugging After Effects plug-ins](08-MACOS/03-DEBUGGING.md)
- [macOS — GPU development](08-MACOS/04-GPU.md)
- [macOS — signing and notarization](08-MACOS/05-SIGNING-NOTARIZATION.md)
- [macOS — installation and packaging](08-MACOS/06-INSTALLATION-PACKAGING.md)
- [macOS — CI pipeline](08-MACOS/07-CI.md)
- [macOS — native SDK validation](08-MACOS/08-NATIVE-SDK-VALIDATION.md)
- [macOS developer bible](08-MACOS/README.md)

## 09-WINDOWS
- [Windows — Visual Studio setup](09-WINDOWS/01-VISUAL-STUDIO-SETUP.md)
- [Windows — x64 and ARM64](09-WINDOWS/02-X64-ARM64.md)
- [Windows — debugging](09-WINDOWS/03-DEBUGGING.md)
- [Windows — GPU](09-WINDOWS/04-GPU.md)
- [Windows — code signing](09-WINDOWS/05-CODE-SIGNING.md)
- [Windows — installation and packaging](09-WINDOWS/06-INSTALLATION-PACKAGING.md)
- [Windows — CI pipeline](09-WINDOWS/07-CI.md)
- [Windows — native SDK validation](09-WINDOWS/08-NATIVE-SDK-VALIDATION.md)
- [Windows developer bible](09-WINDOWS/README.md)

## 10-TESTING
- [Test matrix](10-TESTING/01-TEST-MATRIX.md)
- [Render correctness](10-TESTING/02-RENDER-CORRECTNESS.md)
- [MFR stress tests](10-TESTING/03-MFR-STRESS.md)
- [Performance testing](10-TESTING/04-PERFORMANCE.md)
- [Crash diagnostics](10-TESTING/05-CRASH-DIAGNOSTICS.md)
- [Testing strategy](10-TESTING/README.md)

## 11-DISTRIBUTION
- [Versioning and compatibility](11-DISTRIBUTION/01-VERSIONING-COMPATIBILITY.md)
- [Security and licensing architecture](11-DISTRIBUTION/02-SECURITY-LICENSING.md)
- [Release checklist](11-DISTRIBUTION/03-RELEASE-CHECKLIST.md)
- [Install locations cheat sheet](11-DISTRIBUTION/04-INSTALL-LOCATIONS.md)

## 12-RECIPES
- [Recipe — first native effect](12-RECIPES/01-FIRST-EFFECT.md)
- [Recipe — migrate an existing effect to MFR](12-RECIPES/02-MFR-MIGRATION.md)
- [Recipe — plug-in does not load](12-RECIPES/03-DEBUG-PLUGIN-NOT-LOADING.md)
- [Recipe — CPU/GPU equivalence](12-RECIPES/04-CPU-GPU-EQUIVALENCE.md)
- [Recipe — panel + native core](12-RECIPES/05-HYBRID-PANEL-NATIVE.md)
- [Recipe — profiling a slow effect](12-RECIPES/06-PROFILING.md)

## 13-TEMPLATES
- [Bug report template](13-TEMPLATES/BUG-REPORT.md)
- [Compatibility matrix template](13-TEMPLATES/COMPATIBILITY-MATRIX.md)
- [Performance report template](13-TEMPLATES/PERFORMANCE-REPORT.md)
- [Plug-in specification template](13-TEMPLATES/PLUGIN-SPEC.md)
- [Release notes template](13-TEMPLATES/RELEASE-NOTES.md)

## 14-NATIVE-INTEGRATIONS
- [Native SDK taxonomy](14-NATIVE-INTEGRATIONS/01-TAXONOMY.md)
- [Host call flows](14-NATIVE-INTEGRATIONS/02-HOST-CALL-FLOWS.md)
- [PICA suites — внутренний native service bus After Effects](14-NATIVE-INTEGRATIONS/03-PICA-SUITES.md)
- [Effect plug-ins — полный native map](14-NATIVE-INTEGRATIONS/04-EFFECTS.md)
- [AEGP tools — native automation and deep AE integration](14-NATIVE-INTEGRATIONS/05-AEGP-TOOLS.md)
- [Keyframers](14-NATIVE-INTEGRATIONS/06-KEYFRAMERS.md)
- [Native dockable panels](14-NATIVE-INTEGRATIONS/07-NATIVE-PANELS.md)
- [AEIO — native input/output modules](14-NATIVE-INTEGRATIONS/08-AEIO.md)
- [Artisan — custom 3D renderer](14-NATIVE-INTEGRATIONS/09-ARTISAN.md)
- [BlitHook](14-NATIVE-INTEGRATIONS/10-BLITHOOK.md)
- [Legacy / deprecated native integration](14-NATIVE-INTEGRATIONS/11-LEGACY-NATIVE.md)
- [AEGP suites catalog — After Effects 26.5 snapshot](14-NATIVE-INTEGRATIONS/12-AEGP-SUITES-CATALOG.md)
- [Public SDK docs errata / verification notes](14-NATIVE-INTEGRATIONS/13-DOCS-ERRATA.md)
- [Native integrations — карта всего нативного SDK After Effects](14-NATIVE-INTEGRATIONS/README.md)

## 15-COMMUNICATION
- [After Effects -> Effect](15-COMMUNICATION/01-AE-TO-EFFECT.md)
- [After Effects -> AEGP](15-COMMUNICATION/02-AE-TO-AEGP.md)
- [AEGP -> Effect](15-COMMUNICATION/03-AEGP-TO-EFFECT.md)
- [Plug-in -> Plug-in через published PICA suite](15-COMMUNICATION/04-PLUGIN-TO-PLUGIN-PICA.md)
- [ExtendScript -> After Effects](15-COMMUNICATION/05-SCRIPT-TO-AE.md)
- [CEP panel <-> ExtendScript](15-COMMUNICATION/06-CEP-TO-EXTENDSCRIPT.md)
- [Native <-> script/panel: как собирать гибридный продукт](15-COMMUNICATION/07-NATIVE-TO-SCRIPT-PANEL.md)
- [Threading boundaries](15-COMMUNICATION/08-THREADING-BOUNDARIES.md)
- [Data ownership and lifetime](15-COMMUNICATION/09-DATA-OWNERSHIP.md)
- [Как компоненты общаются друг с другом и с After Effects](15-COMMUNICATION/README.md)

## 16-WORKING-TEMPLATES
- [Working templates](16-WORKING-TEMPLATES/README.md)
- [AEGP menu command template](16-WORKING-TEMPLATES/aegp-menu-command/README.md)
- [AEIO registration skeleton](16-WORKING-TEMPLATES/aeio-registration/README.md)
- [Artisan registration skeleton](16-WORKING-TEMPLATES/artisan-registration/README.md)
- [CEP -> ExtendScript JSON bridge](16-WORKING-TEMPLATES/cep-panel-bridge/README.md)
- [Effect <-> AEGP generic bridge](16-WORKING-TEMPLATES/effect-aegp-generic-bridge/README.md)
- [Minimal Gain effect — drop-in for SDK Skeleton](16-WORKING-TEMPLATES/effect-basic/README.md)
- [Standalone JSX tool](16-WORKING-TEMPLATES/jsx-tool/README.md)
- [Keyframer batch pattern](16-WORKING-TEMPLATES/keyframer-batch/README.md)
- [Native dockable panel registration — Panelator-shaped template](16-WORKING-TEMPLATES/native-panel-registration/README.md)
- [Published PICA suite contract](16-WORKING-TEMPLATES/pica-shared-suite/README.md)

## 17-NATIVE-SUITE-COOKBOOK
- [Как пользоваться cookbook](17-NATIVE-SUITE-COOKBOOK/00-HOW-TO-USE.md)
- [Project + Item recipes](17-NATIVE-SUITE-COOKBOOK/01-PROJECT-ITEMS.md)
- [Composition recipes](17-NATIVE-SUITE-COOKBOOK/02-COMPOSITIONS.md)
- [Layer recipes](17-NATIVE-SUITE-COOKBOOK/03-LAYERS.md)
- [Effect recipes](17-NATIVE-SUITE-COOKBOOK/04-EFFECTS.md)
- [Streams / properties / expressions](17-NATIVE-SUITE-COOKBOOK/05-STREAMS-PROPERTIES.md)
- [Keyframe recipes](17-NATIVE-SUITE-COOKBOOK/06-KEYFRAMES.md)
- [Mask recipes](17-NATIVE-SUITE-COOKBOOK/07-MASKS.md)
- [Text + marker recipes](17-NATIVE-SUITE-COOKBOOK/08-TEXT-MARKERS.md)
- [Footage / import recipes](17-NATIVE-SUITE-COOKBOOK/09-FOOTAGE-IMPORT.md)
- [Render frame → pixels](17-NATIVE-SUITE-COOKBOOK/10-RENDER-FRAMES.md)
- [Render Queue recipes](17-NATIVE-SUITE-COOKBOOK/11-RENDER-QUEUE.md)
- [Memory / Undo / Persistent Data](17-NATIVE-SUITE-COOKBOOK/12-MEMORY-UNDO-PERSISTENCE.md)
- [Guides / Item Views / Selection](17-NATIVE-SUITE-COOKBOOK/13-GUIDES-VIEWS-SELECTION.md)
- [Lifetime + threading rules](17-NATIVE-SUITE-COOKBOOK/14-LIFETIME-THREADING.md)
- [Native recipe index](17-NATIVE-SUITE-COOKBOOK/15-RECIPE-INDEX.md)
- [AEGP Suite function map — native capability index](17-NATIVE-SUITE-COOKBOOK/16-SUITE-FUNCTION-MAP.md)
- [Native Suite Cookbook](17-NATIVE-SUITE-COOKBOOK/README.md)
- [Verification matrix](17-NATIVE-SUITE-COOKBOOK/VERIFICATION.md)
- [v0.3 drop-in C++ code](17-NATIVE-SUITE-COOKBOOK/code/README.md)

## 18-SDK-HEADER-TOOLS
- [Native contract families — кто кого вызывает](18-SDK-HEADER-TOOLS/01-NATIVE-CONTRACT-FAMILIES.md)
- [Workflow: от SDK headers до рабочего recipe](18-SDK-HEADER-TOOLS/02-INVENTORY-WORKFLOW.md)
- [SDK diff policy](18-SDK-HEADER-TOOLS/03-SDK-DIFF-POLICY.md)
- [Header-first rules](18-SDK-HEADER-TOOLS/04-HEADER-FIRST-RULES.md)
- [SDK Header Tools — полный native API без ручного копирования](18-SDK-HEADER-TOOLS/README.md)

## 19-NATIVE-CODE-FOUNDATION
- [Suite acquisition](19-NATIVE-CODE-FOUNDATION/01-SUITE-ACQUISITION.md)
- [AEGP ownership / RAII](19-NATIVE-CODE-FOUNDATION/02-RAII-OWNERSHIP.md)
- [Undo transaction](19-NATIVE-CODE-FOUNDATION/03-UNDO-TRANSACTIONS.md)
- [Host callback ABI boundary](19-NATIVE-CODE-FOUNDATION/04-HOST-CALL-BOUNDARY.md)
- [Native C++ foundation — повторно используемые безопасные куски](19-NATIVE-CODE-FOUNDATION/README.md)
# v1.1 verification and maintenance

- [Verification results and commands](VERIFICATION.md)
- [Coverage matrix](FINAL-COVERAGE-AUDIT.md)
- [Reference implementations and guides](20-REFERENCE-IMPLEMENTATIONS/README.md)


## Audit and completion roadmap — 2026-10-02

- [Редакционный аудит](EDITORIAL-AUDIT-2026-10-02.md)
- [Проверка внешних источников](EXTERNAL-SOURCES-REVIEW-2026-10-02.md)
- [План завершения](COMPLETION-PLAN.md)
- [Поглавный трекер — 127 core pages](CHAPTER-COMPLETION-TRACKER.md)
- [ElasticGridFX transfer plan](22-PROJECT-CASE-STUDIES/ELASTICGRIDFX-TRANSFER-PLAN-2026-10-02.md)
