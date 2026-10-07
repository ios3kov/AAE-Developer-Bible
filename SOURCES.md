# Sources registry

Research snapshots: retained 2026-10-01 / 2026-10-02; selected platform/roadmap rereview **2026-10-04**.

Freeze rereview **2026-10-07**: Apple notarization workflow, sample-first/install/
debugger guides, Windows ARM build/SignTool and AE UXP landing reviewed within
[macOS/Windows reconciliation](CHAPTER-RECONCILIATION-2026-10-07.md).
Adobe host requirements fetch HTTP403; dated2026-10-04 support snapshot retained
explicitly, not freshly certified. No exhaustive external-link/API audit or installed
beta/GA/native host verification. SDK25.6 baseline and per-record dates unchanged.

[Claim/source/version table](BLOCK-5-SOURCES.md) separates SDK, host, panel and platform boundaries. [Block 5 review](BLOCK-5-REVIEW-2026-10-04.md) records practical-depth comparison, fresh checks and remaining uncertainty.

## Внешний source review — 2026-10-02

[Отчёт](EXTERNAL-SOURCES-REVIEW-2026-10-02.md) закрепляет snapshots C++ SDK Guide, Scripting Guide, Adobe CEP Resources и вторичного [After Effects SDK Knowledge Base](https://github.com/pushREC/after-effects-sdk-kb/tree/0a0fa05ba9d229344986e15cd15968c42640cc90). Проверены происхождение, metadata и выбранные API-разделы. KB current-25.6 matrix расходится с существующими exact-SDK records, поэтому он остаётся указателем на темы, а не native ABI authority.

Из ближних к первоисточнику guides добавлены bounded scripting/CEP workflows и правило version-specific чтения; исключены undocumented импортные members из обычного recipe. Guides также содержат исторические headings и отдельный malformed source example. Только проверенные claim/source pairs переносятся в core; коллекции не объявляются полностью валидированными.

## Tier A — Adobe / platform vendor

- Adobe After Effects Developer Portal  
  https://developer.adobe.com/after-effects/
- Adobe Developer Blog — UXP / CEP migration announcement, 2026-09-24  
  https://blog.developer.adobe.com/en/publish/2026/09/investing-in-the-future-of-creative-cloud-extensibility-uxp-comes-to-our-flagship-applications
- Adobe CEP Resources  
  https://github.com/Adobe-CEP/CEP-Resources
- Adobe CEP 12 HTML Extension Cookbook  
  https://github.com/Adobe-CEP/CEP-Resources/blob/master/CEP_12.x/Documentation/CEP%2012%20HTML%20Extension%20Cookbook.md
- Adobe CEP Samples  
  https://github.com/Adobe-CEP/Samples
- Apple — Developer ID  
  https://developer.apple.com/developer-id/
- Apple — Creating distribution-signed code for macOS  
  https://developer.apple.com/documentation/xcode/creating-distribution-signed-code-for-the-mac/
- Apple — Notarizing macOS software  
  https://developer.apple.com/documentation/security/notarizing-macos-software-before-distribution
- Apple — Customizing notarization workflow  
  https://developer.apple.com/documentation/security/customizing-the-notarization-workflow
- Microsoft — SignTool  
  https://learn.microsoft.com/en-us/windows/win32/seccrypto/signtool
- Microsoft — Windows on Arm development  
  https://learn.microsoft.com/en-us/windows/arm/

## Tier B — Adobe SDK material maintained at Docs for Adobe

- After Effects C++ SDK Guide  
  https://ae-plugins.docsforadobe.dev/
- After Effects Scripting Guide  
  https://ae-scripting.docsforadobe.dev/
- Source repository for C++ guide  
  https://github.com/docsforadobe/after-effects-plugin-guide

Important: Docs for Adobe is community-maintained. For shipping decisions, validate version-sensitive facts against the actual SDK headers/samples and Adobe release notes you build against.

## Tier C — useful existing knowledge base

- pushREC / after-effects-sdk-kb  
  https://github.com/pushREC/after-effects-sdk-kb

Used as a map of coverage/gaps, not as the canonical API contract.

## High-value pages

- Start creating plug-ins  
  https://ae-plugins.docsforadobe.dev/intro/how-to-start-creating-plug-ins/
- Sample projects  
  https://ae-plugins.docsforadobe.dev/intro/sample-projects/
- PiPL resources  
  https://ae-plugins.docsforadobe.dev/intro/pipl-resources/
- Compatibility across AE versions  
  https://ae-plugins.docsforadobe.dev/intro/compatibility-across-multiple-versions/
- Apple Silicon support  
  https://ae-plugins.docsforadobe.dev/intro/apple-silicon-support/
- Windows on Arm support  
  https://ae-plugins.docsforadobe.dev/intro/windows-on-arm-support/
- Debugging plug-ins  
  https://ae-plugins.docsforadobe.dev/intro/debugging-plug-ins/
- macOS debugger attach  
  https://ae-plugins.docsforadobe.dev/intro/debugging-ae-macos/
- GPU build instructions  
  https://ae-plugins.docsforadobe.dev/intro/gpu-build-instructions/
- MFR  
  https://ae-plugins.docsforadobe.dev/effect-details/multi-frame-rendering-in-ae/
- SmartFX  
  https://ae-plugins.docsforadobe.dev/smartfx/smartfx/
- Custom UI / Drawbot  
  https://ae-plugins.docsforadobe.dev/effect-ui-events/custom-ui-and-drawbot/
- AEGP overview  
  https://ae-plugins.docsforadobe.dev/aegps/overview/
- AEIO  
  https://ae-plugins.docsforadobe.dev/aeios/aeios/
- Artisan  
  https://ae-plugins.docsforadobe.dev/artisans/artisans/
- Where installers put plug-ins  
  https://ae-plugins.docsforadobe.dev/intro/where-installers-should-put-plug-ins/
- ExtendScript object model  
  https://ae-scripting.docsforadobe.dev/introduction/objectmodel/

## Source quality rule

When sources disagree:

1. Actual SDK headers/sample shipped with the target SDK win for compile-time/API facts.
2. Current Adobe platform/security documentation wins for signing/notarization/distribution.
3. Adobe developer announcements win for migration timelines.
4. Docs for Adobe is the practical explanatory guide.
5. Third-party articles are hints only until reproduced or verified.

## v0.2 native architecture sources

- Native integration map / What Can I Do
  https://ae-plugins.docsforadobe.dev/intro/what-can-i-do/
- Effect entry point
  https://ae-plugins.docsforadobe.dev/effect-basics/entry-point/
- Effect command selectors
  https://ae-plugins.docsforadobe.dev/effect-basics/command-selectors/
- AEGP implementation and entry point
  https://ae-plugins.docsforadobe.dev/aegps/implementation/
- AEGP suites / command hooks / generic effect calls
  https://ae-plugins.docsforadobe.dev/aegps/aegp-suites/
- Effect use of AEGP suites and dependency caveats
  https://ae-plugins.docsforadobe.dev/aegps/cheating-effect-usage-of-aegp-suites/
- AEIO calling sequence
  https://ae-plugins.docsforadobe.dev/aeios/calling-sequence/
- Artisan registration/data types
  https://ae-plugins.docsforadobe.dev/artisans/artisan-data-types/
- CEP official samples / AfterEffectsPanel
  https://github.com/Adobe-CEP/Samples
- CEP official resources/cookbook
  https://github.com/Adobe-CEP/CEP-Resources
- SDK 26.5 history (updated September 2026)
  https://ae-plugins.docsforadobe.dev/history/


## v0.3 native cookbook sources

- AEGP Suites — complete public function reference  
  https://ae-plugins.docsforadobe.dev/aegps/aegp-suites/
- AEGP data types / handle model  
  https://ae-plugins.docsforadobe.dev/aegps/data-types/
- AEGP details / invalidation / begin-end patterns  
  https://ae-plugins.docsforadobe.dev/aegps/aegp-details/
- Effect use of AEGP suites / cache dependency warning  
  https://ae-plugins.docsforadobe.dev/aegps/cheating-effect-usage-of-aegp-suites/
- Official sample project index (`Projector`, `Streamie`, `QueueBert`, `Easy Cheese`, `Sweetie`, etc.)  
  https://ae-plugins.docsforadobe.dev/intro/sample-projects/
- How to start / graft from official samples  
  https://ae-plugins.docsforadobe.dev/intro/how-to-start-creating-plug-ins/
- SDK 26.5 version history  
  https://ae-plugins.docsforadobe.dev/history/

### Secondary signature sanity checks

Used only where the rendered HTML guide appears inconsistent; actual Adobe SDK headers still win:

- Header-derived Rust bindings (`after_effects_sys`)  
  https://docs.rs/after-effects-sys/
- Adobe Community SDK discussions for known signature/documentation mismatches  
  https://community.adobe.com/


## v0.4 contract-verification sources

- AEGP Suites / PICA-style function tables  
  https://ae-plugins.docsforadobe.dev/aegps/aegp-suites/
- SDK version history / suite generation changes  
  https://ae-plugins.docsforadobe.dev/history/
- Public Adobe SDK sample index / recommended graft workflow  
  https://ae-plugins.docsforadobe.dev/intro/sample-projects/

The v0.4 tooling deliberately does **not** bundle Adobe SDK headers. Exact inventories are generated from the SDK headers present on the developer's own machine; those headers remain the compile-time source of truth.


## Project evidence reviewed — 2026-10-02

ElasticGridFX / FSTR Stretch 0.9.3-perf.1: [retrospective](https://github.com/ios3kov/ElasticGridFX/blob/9d0162de64d01ceb41f6a1374a73544729ed0ec2/docs/retrospective-0.9.3-perf.1.md), [project know-how](https://github.com/ios3kov/ElasticGridFX/blob/9d0162de64d01ceb41f6a1374a73544729ed0ec2/docs/AE_ENGINEERING_KNOWHOW.md). Immutable documentation snapshot: `9d0162de64d01ceb41f6a1374a73544729ed0ec2`; shipping source differs and is recorded separately.

Classification: **PROJECT-REPORTED**; user acceptance is **USER-REPORTED**. These are scoped product observations, not Adobe API contracts or a new Bible-owned host test. [Transfer plan and primary records](22-PROJECT-CASE-STUDIES/ELASTICGRIDFX-TRANSFER-PLAN-2026-10-02.md).
