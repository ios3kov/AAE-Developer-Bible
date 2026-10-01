# Windows — native SDK validation

Header-derived validation is the first Windows native preflight.

It is not Windows build or host evidence.

## Run

~~~powershell
cd 18-SDK-HEADER-TOOLS
.\run-windows.ps1 "C:\path\to\After Effects SDK\Examples"
~~~

Use the exact candidate SDK.

## What PASS means

A successful run means only the tool's implemented checks passed, for example:

- supported header declarations parsed without unresolved **required-contract** diagnostics; unrelated diagnostics remain recorded;
- inventory schema/version validation passed;
- cookbook/reference suite symbols resolved against that inventory;
- the current Bible native C++ translation units passed MSVC C++17 syntax/type checks;
- a machine-readable report records SDK header-manifest identity, MSVC identity, exact commands and per-source results.

The parser is deliberately conservative; unsupported declarations are not silently guessed.

## What PASS does not mean

It does not prove:

- PiPL/resource generation;
- link;
- x64/ARM64 architecture correctness;
- dependency/runtime availability;
- Authenticode;
- installer behavior;
- AE discovery/load;
- render/project semantics;
- MFR/GPU safety.

## Required next gates

~~~text
header inventory + symbol check + MSVC syntax/type report
→ Windows resource/PiPL project step
→ link
→ PE/import/architecture inspection
→ native tests
→ AE development install/load
→ Authenticode
→ installer
→ clean VM install/host smoke
~~~

Keep PDB and exact binary hashes with the evidence.

## Windows architecture

If ARM64 is claimed, run a real ARM64 build/dependency/host lane.

A successful x64 header preflight says nothing about an ARM64 third-party library or native AE host.

## SDK upgrade

Diff candidate inventory against the previously accepted SDK and manually inspect high-risk changes before fixing call sites.

See 18-SDK-HEADER-TOOLS/03-SDK-DIFF-POLICY.md.

## Failure handling

If the tool cannot parse a declaration:

- inspect the header;
- classify parser limitation vs actual SDK change;
- improve parser deterministically if needed;
- leave unresolved facts unresolved.

Do not cast or suppress a native mismatch to keep the validation lane green.

## Verification boundary

Windows compiler/link/sign/install/host acceptance remains separate. A header PASS must never be copied into the compatibility matrix as Windows PASS.


For the exact PASS/FAIL evidence contract, see [Gate 4 — exact SDK acceptance runbook](../18-SDK-HEADER-TOOLS/16-GATE4-ACCEPTANCE-RUNBOOK.md).
