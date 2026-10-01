# SDK contract audit runbook

> Historical filename retained for link compatibility. The former “Gate 4 compiler acceptance” completion model is superseded.

Target baseline: **Adobe After Effects SDK 25.6 build 61**.

## Purpose

Use this runbook when editing version-sensitive native chapters.

The goal is to answer:

- does the cited SDK expose the expected suite/table generation;
- do critical functions exist in that table;
- do cookbook SuiteHandler calls point to the same generation;
- are parser limitations visible rather than silently ignored.

This is an **editorial contract audit**, not a requirement to build every Bible example.

## Recommended flow

~~~text
exact SDK headers
→ inventory with diagnostics preserved
→ required SDK table/function manifest
→ required-diagnostic check
→ cookbook name + suite-generation check
→ record findings in source-review docs
~~~

For the current SDK 25.6 baseline this flow has already been run successfully.

## Required-contract manifest

`sdk25.6-required-contracts.json` pins the minimum version-sensitive contract surface used by the current edition.

If a required table/function is missing, reconcile:

1. SDK identity/version;
2. parser limitation;
3. actual SDK change;
4. Bible text/recipe;
5. manifest mistake.

Do not fix prose by guessing.

## Parser diagnostics

All diagnostics remain visible.

A diagnostic is editorially blocking when it affects a contract the Bible currently relies on.

A diagnostic in an unrelated table is still recorded, but the Bible does not need a complete C/C++ parser for every Adobe structure before publishing documentation.

## Cookbook suite-generation check

For calls such as:

~~~cpp
suites.StreamSuite6()->AEGP_GetStreamType(...)
~~~

the audit checks that the function belongs to the expected `AEGP_StreamSuite6` table in the selected SDK baseline.

## Optional compiler evidence

A developer may additionally run platform compiler helpers.

That can catch C++/toolchain issues in a source snapshot, but it is **optional evidence**, not an editorial completion gate.

Compilation becomes relevant to a Bible claim only when the Bible says that a particular artifact was actually compiled or run.

## Evidence retention

Keep SDK identity, inventory summary, required-contract result, cookbook result, diagnostics, Bible snapshot and date. Do not publish licensed Adobe headers.

## Current result — 2026-10-01

Real SDK 25.6 audit:

- 140 headers scanned;
- 233 contract tables indexed;
- 3,560 function entries;
- 35 required contracts: **0 missing**;
- 39 cookbook call-sites: **0 unknown**;
- 0 required parser diagnostics;
- 4 non-required partial diagnostics retained.

See [the exact SDK record](17-SDK25.6-CONTRACT-AUDIT-2026-10-01.md).

For the current edition, this closes the **SDK contract-accuracy editorial requirement**. No whole-repository macOS/Windows build is required.
