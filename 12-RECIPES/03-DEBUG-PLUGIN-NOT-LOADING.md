# Recipe — plug-in does not load

Concrete command/artifact branches: [macOS Skeleton inspection](../08-MACOS/09-PRODUCTION-BUILD-PIPELINE.md)
and [Windows machine/exports/imports/PiPL](../09-WINDOWS/09-PRODUCTION-BUILD-PIPELINE.md).
Check discovery/duplicates before pixel algorithm; loaded module path/UUID/PDB identity
must match the artifact under test. Unknown loaded identity means unresolved diagnosis.

## Goal

Reduce a load failure to one layer instead of changing code blindly.

Use this order:

~~~text
discovery
→ architecture
→ signature/trust
→ dependencies
→ PiPL/resource
→ exported entry point
→ initialization
→ host/version compatibility
~~~

## 1. Prove the host sees the location

Record the exact installed path.

Check:

- correct native plug-in folder;
- expected bundle/file suffix;
- no duplicate older copy earlier in the search path;
- no installer placing the artifact into another AE version;
- permissions allow the host to read it.

For debugging, temporarily remove duplicate product builds so only one candidate exists.

## 2. Compare with an untouched sample

On the same machine and AE build:

~~~text
known-good Adobe sample
→ same development install policy
→ launch AE
~~~

If the sample also fails, investigate environment/toolchain/install policy before product code.

## 3. Verify architecture

### macOS

Inspect the executable inside the bundle:

~~~bash
lipo -info "/path/MyPlugin.plugin/Contents/MacOS/MyPlugin"
~~~

The required host architecture must exist and agree with PiPL declarations.

### Windows

Inspect PE machine type and packaged dependencies.

An x64 .aex does not become ARM64-native because Windows can emulate unrelated applications.

## 4. Verify trust/signing

### macOS

Verify the actual installed bundle, not a build-directory copy:

~~~bash
codesign -vvv --strict "/path/MyPlugin.plugin"
~~~

For release artifacts also verify the intended Developer ID/notarization path.

### Windows

~~~bat
signtool verify /pa /v MyPlugin.aex
~~~

Code signing proves identity/integrity, not AE compatibility, but trust failures must be eliminated before deeper debugging.

## 5. Inspect dependencies

Look for:

- missing dylib/DLL;
- wrong architecture dependency;
- debug runtime dependency;
- absolute developer-local search path;
- missing helper/framework;
- incompatible commercial SDK runtime.

macOS: inspect linked dylibs and nested code architecture.

Windows: inspect imports and ensure the clean target machine actually has every required runtime.

## 6. Verify PiPL/resource

Check:

- PiPL resource was generated;
- Kind/type is correct for the plug-in family;
- entry symbol string is correct;
- architecture declaration matches the binary;
- effect metadata/version/category are coherent;
- capability flags do not contradict GlobalSetup.

On Windows, verify the custom .r → resource step was not lost while cloning the project.

## 7. Verify exported entry point

The symbol named by the PiPL/resource must exist with the expected C ABI/calling convention.

Do not debug EffectMain internals before confirming the host can resolve the symbol.

## 8. Stop risky global initialization

If discovery happens but AE crashes or silently rejects during module load, inspect:

- global/static constructors;
- filesystem/network work before host initialization;
- licensing startup;
- GPU runtime initialization;
- helper process launch;
- environment-variable assumptions.

Prefer explicit initialization inside the documented host lifecycle so failures can be reported and cleaned up.

## 9. Attach debugger / collect crash evidence

For an initialization crash:

- exact plug-in hash;
- exact AE build;
- crash report/dump;
- matching dSYM/PDB;
- top symbolized frames;
- last product log event.

See [Crash diagnostics](../10-TESTING/05-CRASH-DIAGNOSTICS.md).

## 10. Version boundary

If the same build works in one AE generation and not another:

1. reproduce with identical artifact;
2. compare host version only;
3. check SDK compatibility/release notes;
4. check suite acquisition/version assumptions;
5. check PiPL capability/version metadata;
6. preserve both PASS and FAIL evidence.

Do not immediately patch around an assumed Adobe regression.

## 11. Binary search recent changes

If a previously loadable product stopped loading, bisect high-risk changes:

- project/resource file;
- entry point;
- architecture;
- signing;
- dependency;
- SDK/toolset;
- initialization.

Avoid simultaneous speculative fixes.

## Acceptance gate

The incident is resolved when the exact artifact:

- is discovered from the intended path;
- has correct architecture/dependencies;
- passes intended trust/signature checks;
- has correct PiPL/entry contract;
- completes initialization;
- appears/loads in the target AE build;
- has a recorded root cause.

A workaround without root-cause evidence remains a workaround.
