# Gate 4 — exact SDK acceptance runbook

Target for the current Bible line: **Adobe After Effects SDK 25.6 build 61**.

This runbook closes only the SDK/compiler gate. It does not build a shipping plug-in, install it, or run After Effects.

## Required inputs

Use:

- a clean Bible Git checkout;
- the exact licensed Adobe SDK `Examples` directory;
- macOS: Clang/Xcode toolchain intended for the candidate;
- Windows: Visual Studio Developer Command Prompt / VsDevCmd with `cl.exe`;
- no copied/edited SDK headers.

Do not run acceptance from an unknown dirty tree.

## macOS

~~~bash
cd 18-SDK-HEADER-TOOLS
./run-macos.sh "/path/to/After Effects SDK/Examples"
~~~

Expected evidence directory:

~~~text
18-SDK-HEADER-TOOLS/generated/local-sdk/
├── ae-sdk-inventory.json
├── ae-sdk-inventory.md
└── native-compile-report.json
~~~

## Windows

From a Visual Studio Developer Command Prompt / VsDevCmd environment:

~~~powershell
cd 18-SDK-HEADER-TOOLS
.\run-windows.ps1 "C:\path\to\After Effects SDK\Examples"
~~~

The same three evidence files are produced.

## What the runner checks

Order is intentionally fail-closed:

~~~text
exact local headers
→ inventory parser with all diagnostics retained
→ required SDK 25.6 table/function manifest
→ no diagnostics affecting required contracts
→ exact SuiteHandler generation checks in cookbook calls
→ compiler syntax/type checks
→ machine-readable evidence report
~~~

A later step does not rescue an earlier failure.

## Required-contract gate

`sdk25.6-required-contracts.json` pins the minimum contract surface used by the current Bible edition.

The run fails if a required suite/function-block is absent, including the pinned generations for:

- AEGP registration/menu/utility;
- project/item/comp/layer/effect;
- streams/dynamic streams/keyframes;
- masks/text/markers/footage;
- render queue/output module/frame render;
- AEIO;
- Artisan;
- native panels;
- GPU;
- Custom UI/Drawbot;
- PICA/SP.

Selected high-risk tables also pin critical function names.

This is a minimum baseline, not a complete Adobe SDK ABI model.

## Suite-generation gate

For calls written through `AEGP_SuiteHandler`, the symbol checker verifies both function name and expected suite generation.

Example:

~~~cpp
suites.StreamSuite6()->AEGP_GetStreamType(...)
~~~

must resolve to `AEGP_StreamSuite6`.

Finding `AEGP_GetStreamType` only in another generation is a failure.

## Compiler evidence

`native-compile-report.json` records:

- schema/version;
- verification boundary;
- SDK Examples root;
- aggregate SDK header-manifest SHA-256;
- SDK header count;
- compiler path/style/identity;
- Bible Git SHA;
- clean/dirty state;
- every translation-unit path;
- SHA-256 of every translation unit;
- exact compiler command;
- return code;
- stdout/stderr tail;
- final PASS/FAIL summary.

The platform runners require a known clean Git commit.

## Gate 4 PASS criteria — one platform

A platform compiler lane is PASS only when all are true:

- inventory artifact is generated successfully;
- required-contract verifier exits 0;
- no unparsed/partial diagnostic affects a required contract;
- cookbook symbol/suite-generation verifier exits 0;
- compiler report summary is PASS;
- every translation unit is PASS;
- report has a Git SHA;
- dirty is exactly `false`;
- SDK header manifest exists and is a 64-character SHA-256;
- compiler identity is recorded.

## Cross-platform Gate 4

The complete Gate 4 requires:

### macOS
- current clean Bible revision;
- SDK 25.6 exact-header inventory PASS;
- required contract PASS;
- current native source syntax/type PASS with Clang.

### Windows
- current clean Bible revision;
- same declared SDK baseline;
- required contract PASS;
- current native source syntax/type PASS with MSVC.

Windows is not inferred from macOS.

## What this gate still does not prove

Even after both compiler lanes pass, the following remain later gates:

- PiPL/resource project build;
- native link;
- Mach-O/PE architecture;
- plug-in discovery/load in AE;
- parameter/project/render semantics;
- pixels;
- save/reopen;
- MFR;
- GPU;
- signing/notarization/AuthentiCode;
- installer/upgrade/uninstall;
- clean-machine acceptance.

## Failure classification

### Parser diagnostic

The platform runners deliberately use `--allow-incomplete` only so the complete diagnostic inventory can be emitted. That flag is **not** a PASS by itself.

Immediately afterwards, `verify_required_contracts.py` fails the run if any diagnostic touches a required Gate-4 table/function. Non-required diagnostics remain visible in the evidence record and may be improved later.

Inspect the exact SDK declaration. Improve parser grammar only when the declaration can be represented deterministically without hiding calling convention/layout information.

### Missing required table/function

Check, in order:

1. correct SDK version/build;
2. parser diagnostic;
3. actual SDK generation change;
4. manifest mistake.

Do not weaken the manifest merely to get green output.

### Suite-generation mismatch

Inspect the exact target SDK header and the nearest current SDK sample. Do not cast an old suite table into the expected generation.

### Compiler failure

Compiler/type evidence outranks prose examples. Fix source or document a real version boundary; do not suppress type errors.

### Dirty source

Commit or deliberately reset the intended source before producing acceptance evidence. A dirty-tree compile can be useful for development but is not Gate-4 acceptance.

## Evidence retention

For an accepted run retain:

- the three generated files;
- Bible Git SHA;
- SDK archive/source identity;
- platform/OS/toolchain version;
- command used;
- CI/local operator/date.

Do not commit licensed Adobe headers to the public Bible.

## Current status — 2026-10-01

Portable tooling and regression tests are PASS.

Real SDK 25.6 required-contract preflight is now **PASS** on the source-equivalent audit snapshot recorded in [the exact SDK run record](17-GATE4-SDK25.6-RUN-2026-10-01.md):

- 140 headers scanned;
- 233 contract tables;
- 3,560 function entries;
- 35 required tables/functions: 0 missing;
- 39 cookbook call-sites: 0 unknown;
- 4 retained non-required partial diagnostics.

Fresh macOS Clang/Xcode syntax/type acceptance on the current Bible native source remains **NOT RUN** in a real macOS environment.

Windows real SDK/MSVC acceptance also remains **NOT RUN**.
