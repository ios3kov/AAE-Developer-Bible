# SDK Header Tools — exact contract audit helpers

These tools keep **version-sensitive Bible claims aligned with a real Adobe SDK**.

They are not a requirement to compile the whole Bible.

## Editorial purpose

The useful editorial question is:

> Does the SDK version we cite actually contain the suite generation/function/table the text and recipes say it contains?

For Adobe After Effects SDK **25.6 build 61**, the real-header audit records:

- 35/35 required contract tables/functions present;
- 39/39 cookbook call-sites resolving to expected SuiteHandler generations;
- 0 required parser diagnostics;
- four unrelated partial parser diagnostics retained explicitly.

That is the current contract-accuracy baseline for the Bible.

## Inventory

`tools/ae_sdk_inventory.py` indexes C ABI-style tables such as AEGP, PF, DRAWBOT, AEIO, PR and PICA/SP tables.

It records source file/hash, normalized declarations and parser diagnostics.

`--allow-incomplete` means only “emit the inventory including diagnostics”. It never means “everything is verified”.

## Required-contract audit

`sdk25.6-required-contracts.json` defines the minimum contract surface referenced by the current core native chapters/recipes.

`verify_required_contracts.py` fails when a required table/function is absent, a required table has a parser diagnostic, or the inventory schema is unsupported.

Unrelated diagnostics remain visible without turning the Bible into a project to implement a complete C/C++ parser for every Adobe structure.

## Recipe audit

`verify_recipe_symbols.py` checks cookbook call-site names and, for SuiteHandler calls, the expected suite generation.

This is a **documentation/source consistency check**. It does not need to prove a shipping binary.

## SDK diff

`diff_sdk_inventory.py` is useful when a future edition moves to another SDK baseline.

## Optional compiler helper

`scripts/check_native.py` and the platform runners can produce additional syntax/type evidence for source snapshots.

They are useful to a developer who wants extra confidence in a source example, but **compiler evidence is not a completion criterion for AE Developer Bible**.

Historical compiler results remain in [VERIFICATION.md](../VERIFICATION.md) because they are real evidence about those snapshots.

## Canonical audit documents and compatibility aliases

Canonical documents:

- [SDK contract audit runbook](16-SDK-CONTRACT-AUDIT-RUNBOOK.md)
- [SDK 25.6 contract audit record](17-SDK25.6-CONTRACT-AUDIT-2026-10-01.md)

The old `16-GATE4-...` / `17-GATE4-...` paths remain only as short compatibility aliases so historical links do not break. They are not the active completion model.

## Current real SDK evidence

See [SDK 25.6 contract audit record](17-SDK25.6-CONTRACT-AUDIT-2026-10-01.md).

The result supports the Bible's current native contract claims. No additional macOS/Windows compilation is required to call the documentation editorially complete.

## SDK 25.6 source-review records

These records document scoped header/sample reviews.
They are not additional compiler or After Effects runtime results.
Read each record's provenance and limitations.

1. [Supplied SDK and review scope](05-SUPPLIED-SDK-25.6.md)
2. [Parameters and pixels](06-PARAMETERS-PIXELS-SDK25.6.md)
3. [Memory and MFR](07-MEMORY-MFR-SDK25.6.md)
4. [Registration and AEGP](08-REGISTRATION-AEGP-SDK25.6.md)
5. [AEGP project and render](09-AEGP-PROJECT-RENDER-SDK25.6.md)
6. [Streams and keyframes](10-STREAMS-KEYFRAMES-SDK25.6.md)
7. [Masks, text and footage](11-MASK-TEXT-FOOTAGE-SDK25.6.md)
8. [AEIO and Artisan](12-AEIO-ARTISAN-SDK25.6.md)
9. [Panels and BlitHook](13-PANELS-BLITHOOK-SDK25.6.md)
10. [PICA, bridges and legacy contracts](14-PICA-BRIDGES-LEGACY-SDK25.6.md)
11. [GPU, audio and custom UI](15-GPU-AUDIO-CUSTOM-UI-SDK25.6.md)

## Generated tooling material

- [Generated material index](generated/README.md)
- [Fixture inventory](generated/fixture-inventory.md)

Fixture inventory is tooling material, not a substitute for the
real-SDK contract audit. Consult each document for its provenance.
