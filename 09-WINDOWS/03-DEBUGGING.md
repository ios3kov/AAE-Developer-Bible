# Windows — debugging After Effects plug-ins

Windows debugging should answer three questions quickly:

1. Did After Effects load the artifact you think it loaded?
2. Are the matching symbols loaded?
3. Is the failure inside your code, host interaction, dependency loading or another subsystem?

## Launch from Visual Studio

Project Debugging settings:

- **Command** → exact target `AfterFX.exe`;
- **Working Directory** → host directory;
- **Environment** → product-specific debug variables if needed;
- output/copy step → development plug-in location.

Do not hardcode one developer's AE path into shared project files. Prefer:

- environment variable;
- local property sheet;
- user-local VS settings;
- generated dev config.

## Attach to an existing AE process

Workflow:

1. launch AE normally;
2. Visual Studio → **Attach to Process**;
3. choose the correct `AfterFX.exe`;
4. confirm code type/native debugger;
5. inspect loaded modules;
6. verify symbols for your `.aex`.

Attaching to the wrong AE instance or Beta/release process is a common source of “breakpoint never hits”.

## Verify the actual loaded module

Do not assume that because you copied:

~~~text
C:\some\path\MyPlugin.aex
~~~

AE loaded that exact file.

In debugger/module view record:

- loaded full path;
- image timestamp/build identity if available;
- module architecture;
- matching PDB status.

This matters when:

- several AE versions share MediaCore;
- an old copy exists in another plug-in folder;
- installer/dev copy both exist;
- user-level and machine-level locations differ.

## Symbols

A breakpoint with hollow warning icon usually means one of:

- module not loaded;
- PDB not found;
- PDB does not match binary;
- optimized code changed location;
- source differs from built artifact.

Never fix this by randomly loading a different PDB with the same filename.

## PDB discipline

For every product build worth debugging retain:

- binary;
- exact PDB;
- Git SHA/build ID;
- compiler/toolset;
- SHA-256 or equivalent artifact identity.

A PDB belongs to one exact binary build.

## Debug vs Release

Debug-only bug and Release-only bug can have different causes.

### Debug-only

Possible causes:

- assertions;
- debug allocator;
- different CRT;
- uninitialized memory pattern differences;
- debug-only timing.

### Release-only

Possible causes:

- optimizer exposing UB;
- race/timing change;
- omitted debug initialization;
- LTO/inlining;
- assumptions about object lifetime.

Do not stop after “Debug works”.

## First-chance exceptions

Native debugger can break before AE's error handling sees an exception.

Useful for:

- access violations;
- C++ exceptions crossing boundaries;
- invalid parameter;
- heap corruption.

But AE and libraries may intentionally throw/catch internal exceptions. Filter by module/call stack before treating every first-chance event as your defect.

## C ABI boundaries

Never allow C++ exception to escape an AE C callback/entry point.

Use a boundary guard:

~~~text
extern "C" callback
→ try
→ implementation
→ catch
→ translate to host error
~~~

See [Host call boundary](../19-NATIVE-CODE-FOUNDATION/04-HOST-CALL-BOUNDARY.md).

## Loader/dependency failures

If AE does not load the plug-in:

Check in order:

1. correct architecture;
2. PiPL/resource present;
3. exported entry point;
4. dependent DLLs;
5. MSVC runtime dependency policy;
6. plug-in search path;
7. duplicate/old copies;
8. security/antivirus/quarantine policy;
9. host startup log/error.

Use dependency/import inspection tools rather than guessing.

## Architecture mismatch

Typical Windows native targets:

- x64;
- ARM64 where intentionally supported.

A native DLL dependency with the wrong architecture can make the top-level `.aex` appear “broken” even when your own binary is correct.

Check the complete dependency tree.

## Crash dumps

For a crash report preserve:

- exact plug-in build;
- AE version/build;
- Windows build;
- CPU architecture;
- GPU/driver;
- dump;
- project/repro;
- MFR/GPU state;
- loaded module path.

Without matching PDB, dump analysis may not identify your source line.

## WinDbg workflow

For production dump analysis:

~~~text
open dump
→ configure symbols
→ load matching PDB
→ inspect exception code
→ stack
→ module list
→ threads
→ locks/waits if relevant
→ correlate with exact artifact
~~~

Do not infer causality from the top frame alone; memory corruption often crashes later in unrelated code.

## Hang / deadlock

If AE hangs:

1. break all threads;
2. inspect main thread;
3. inspect threads waiting on your locks;
4. look for host call while holding mutex;
5. inspect worker↔main-thread circular waits;
6. compare with MFR/GPU state.

Common anti-pattern:

~~~text
worker holds product mutex
→ calls host
→ host waits for main thread
→ main thread waits for same product mutex
~~~

## MFR debugging

For render-race bugs record:

- frame numbers;
- thread IDs;
- instance identity;
- sequence/frame data addresses only for debugging, not as persistent IDs;
- render start/end;
- mutation of shared state.

Do not “fix” race by a global mutex around the whole render without understanding performance and host-call consequences.

## GPU debugging

Separate:

- CPU host-side setup;
- GPU resource/lifecycle;
- shader/kernel;
- device reset/loss;
- synchronization;
- CPU/GPU numerical mismatch.

Use the backend-specific tooling appropriate to the product.

Do not debug a GPU output mismatch only from AE screenshots; capture deterministic inputs/parameters.

## Memory corruption

Useful options depend on toolchain/product, but possible approaches include:

- debugger heap checks;
- Application Verifier where compatible;
- compiler sanitizers for pure/internal code where supported;
- guarded allocators in standalone test harnesses.

AE host constraints can make some instrumentation impractical inside the final process. Test pure components outside AE when possible.

## Logging

Logs should include enough identity to connect runtime to source:

~~~text
product version
Git/build ID
AE build
architecture
module path
operation/request ID
thread ID where useful
error code + context
~~~

Avoid writing synchronous verbose logs inside hot render loops in production.

## Project/repro capture

Good bug report:

- minimal project;
- deterministic steps;
- expected;
- actual;
- exact artifact identity;
- platform matrix;
- feature flags.

Bad bug report:

> “AE randomly crashes sometimes.”

## Tools

Depending on problem:

- Visual Studio debugger;
- WinDbg;
- Modules/Symbols views;
- dump tools;
- dependency/import inspection;
- Application Verifier where compatible;
- ETW/performance tooling;
- GPU vendor/backend profilers.

## Product debugging workflow

~~~text
reproduce
→ prove exact module identity
→ load exact symbols
→ classify loader/crash/hang/render/UI
→ reduce repro
→ inspect ownership/threading boundary
→ fix
→ preserve regression evidence
~~~

## Bible evidence boundary

This chapter documents a Windows debugging method. Bible does not need to build or debug its reference source on Windows to make the workflow useful; concrete runtime claims are only made where a recorded runtime result exists.

## Related chapters

- [Visual Studio setup](01-VISUAL-STUDIO-SETUP.md)
- [Windows ARM64](02-X64-ARM64.md)
- [Testing](../10-TESTING/README.md)
- [Crash diagnostics](../10-TESTING/05-CRASH-DIAGNOSTICS.md)
- [Host call boundary](../19-NATIVE-CODE-FOUNDATION/04-HOST-CALL-BOUNDARY.md)
