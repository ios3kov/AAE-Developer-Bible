# Crash diagnostics

Filled [bounded incident record](../22-PROJECT-CASE-STUDIES/ELASTICGRIDFX-PERFORMANCE-SCOPE-2026-10-07.md):
control build/loaded UUID + raw hash + 19/60 outputs + SIGABRT/thread17. Cause UNKNOWN,
fix NONE, six bounded retries not reproduced. Termination stack не устанавливает
первопричину; user closure не означает FIXED. Сохранять symbols UUID отдельно:
record без matching symbols не даёт права придумывать symbolicated plugin cause.

Crash investigation is much easier when every shipped artifact has an identity and matching symbols.

## Every build needs identity

At minimum record:

- semantic product version;
- internal build number;
- git SHA;
- platform/architecture;
- exact binary SHA-256;
- toolchain;
- AE SDK generation/build;
- build configuration.

Expose a user-readable version somewhere that support can collect without opening the binary in a hex editor.

## macOS

Archive the exact dSYM corresponding to every shipped native binary.

Crash ticket should collect where possible:

- .ips/crash report;
- AE exact version/build;
- macOS version;
- CPU architecture;
- plug-in version/hash;
- project or minimal reproduction;
- operation when crash occurred;
- MFR state;
- GPU/backend;
- hardware/driver relevant details;
- whether fresh AE launch reproduces.

Symbolication must use the matching dSYM. A similarly named dSYM from another rebuild is not evidence.

## Windows

Archive exact PDB per architecture/build.

Crash ticket:

- dump type/path;
- AE exact version/build;
- Windows build;
- x64/ARM64;
- plug-in version/hash;
- CPU/GPU/driver;
- project/repro;
- MFR/GPU mode;
- installer version if load/startup related.

Tie PDB to the binary hash.

## Triage classification

Start with a stable class:

1. plug-in discovery/load/init;
2. parameter/UI/event callback;
3. CPU render;
4. GPU setup/render/setdown;
5. MFR/concurrency;
6. project serialization/migration;
7. script/panel/bridge;
8. installer/update;
9. third-party dependency;
10. host/environment baseline.

Classification keeps unrelated crash families from being mixed into one ticket.

## First question: where is the fault?

A stack containing AE and the plug-in is not enough to blame either component.

Inspect:

- crashing instruction/module;
- top symbolized frames;
- exception type;
- corrupted parameters/pointers;
- prior plug-in logs;
- whether memory corruption could have happened earlier.

A crash inside an OS/Adobe function can still be caused by invalid data supplied earlier by the plug-in.

## Known-good baseline

If the failure can be expressed using an untouched Adobe sample or a tiny minimal plug-in, reproduce there.

Result meanings:

- product only fails -> focus product/integration;
- sample also fails -> isolate host/SDK/environment;
- both pass but customer project fails -> reduce project/state.

Do not publish "Adobe bug" from one ambiguous stack.

## Reproduction reduction

Reduce in this order:

~~~text
customer project copy
→ remove unrelated comps/layers
→ remove unrelated effects
→ freeze input asset
→ freeze frame/time
→ isolate parameter values
→ isolate MFR/GPU
→ minimal reproducible project
~~~

Keep an original copy before destructive reduction.

## Hangs

A hang is not a crash but needs similar evidence.

Collect:

- process sample/thread dump;
- all thread stacks;
- last progress/log message;
- locks/waits if identifiable;
- operation duration;
- MFR state;
- helper process state.

A timeout followed by force-kill without a thread dump destroys the best evidence.

## Memory corruption

Symptoms can appear far after the write that caused them.

Use platform sanitizers/debug allocators where compatible with the host/test harness, and reproduce pure core/adapter code outside AE when possible.

High-risk areas:

- rowbytes/pixel indexing;
- stale host references;
- buffer size arithmetic;
- cross-module ABI;
- async callback lifetime;
- cache ownership.

## Crash loops

If a plug-in crashes AE during startup, support needs a recovery path.

Document:

- where the plug-in is installed;
- how to temporarily remove/disable it;
- how to preserve user projects/settings;
- how to collect the failing binary/log before removal.

Do not make recovery require running the crashing plug-in.

## Privacy

Crash packages can contain project paths/names and memory contents.

Define:

- what users should redact;
- how dumps are transferred;
- retention/access policy;
- whether project files are required.

Do not request full private projects by default when a reduced fixture is enough.

## Release use

Crash-free local development is not a metric by itself.

Release confidence comes from:

- stress loops;
- migration fixtures;
- installer/load tests;
- exact symbols retained;
- ability to diagnose the failures that do escape.
