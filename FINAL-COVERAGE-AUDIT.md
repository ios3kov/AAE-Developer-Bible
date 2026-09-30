# Final coverage audit

Research snapshot: 2026-09-30.

## User requirements

| Requirement | Coverage | Where |
|---|---|---|
| Correct categories | complete | `00-START-HERE`, `14-NATIVE-INTEGRATIONS`, `NAVIGATION.md` |
| Native AE mechanisms first | complete | `14-NATIVE-INTEGRATIONS`, `17-NATIVE-SUITE-COOKBOOK`, `19-NATIVE-CODE-FOUNDATION` |
| How Effect plug-ins work | complete | `02-EFFECT-PLUGINS`, native integrations, working templates |
| How AEGP tools work | complete | `03-AEGP`, native integrations, cookbook |
| How AEIO works | complete at architecture/API level | `04-AEIO`, native integrations |
| How Artisan works | complete at architecture/API level | `05-ARTISAN`, native integrations |
| Keyframer / native panel / BlitHook | covered | `14-NATIVE-INTEGRATIONS` |
| Scripts / ScriptUI | covered + runnable example | `06-SCRIPTING`, `20-REFERENCE-IMPLEMENTATIONS/Scripts` |
| CEP / future UXP | covered | `07-PANELS`, CEP bridge |
| Communication with AE | complete | `01-ARCHITECTURE/07-*`, `15-COMMUNICATION` |
| Native plug-in ↔ native plug-in | covered | PICA suite + Effect↔AEGP bridge |
| macOS separately | complete workflow | `08-MACOS` |
| Windows separately | complete workflow | `09-WINDOWS` |
| Copyable code | broad coverage | `16-WORKING-TEMPLATES`, `17-.../code`, `19-.../code`, `20-REFERENCE-IMPLEMENTATIONS` |
| Exact SDK signatures | self-verifying | `18-SDK-HEADER-TOOLS` |

## What "working" means here

This repository can syntax/unit-test its own generic tooling and C++ foundation, but it does not redistribute Adobe's proprietary SDK package and does not have a licensed AE host in CI. Therefore native host-load validation must be run locally against the exact Adobe SDK + After Effects version.

The Bible deliberately distinguishes:

- runnable script/CEP examples;
- native **drop-ins** designed for official Adobe sample shells;
- sample-derived native reference code;
- host-test-required areas such as AEIO/Artisan/native panels.

That distinction is a feature, not a gap: claiming an AEIO or Artisan binary is "really working" without loading it in the target host would be misleading.
