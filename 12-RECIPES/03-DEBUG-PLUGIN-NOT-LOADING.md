# Recipe — plug-in does not load

Do not randomly edit code. Diagnose the loader chain from outside inward.

## 1 — is the file in a scanned location?

Check:

- exact installed path;
- expected package suffix/layout;
- installer log;
- file actually exists after install;
- directory naming does not disable scanning;
- common MediaCore vs AE-specific policy is intentional.

For Windows release installers, confirm the documented Adobe registry path was resolved rather than guessed.

## 2 — is the artifact the expected build?

Record:

- version;
- git SHA if available;
- binary SHA-256;
- architecture;
- timestamp/build identity.

A stale copy in another scanned folder can make you debug the wrong plug-in.

Search for duplicate installed versions.

## 3 — architecture

macOS:

~~~bash
lipo -info "MyPlugin.plugin/Contents/MacOS/MyPlugin"
~~~

Verify the slice AE is currently running.

Windows:

- inspect PE architecture;
- verify x64 vs ARM64;
- verify helper/DLL architecture too.

A correct main binary with one wrong-architecture dependency still fails.

## 4 — PiPL/resource

Check:

- resource exists;
- plug-in Kind/type is intended;
- entry point string matches export;
- architecture entry declaration matches binary;
- capability flags agree with runtime setup;
- Windows resource conversion step actually ran.

When possible compare against the untouched sample project.

## 5 — exported symbol

Inspect the final native binary for the expected host entry point.

Do not assume the source function name guarantees the linker exported it.

Check C linkage/name decoration rules.

## 6 — signing

macOS development/release:

~~~bash
codesign -vvv --strict "MyPlugin.plugin"
~~~

Inspect entitlements/identity as appropriate.

On current macOS versions, unsigned development plug-ins may be rejected.

Windows:

~~~bat
signtool verify /pa /v MyPlugin.aex
~~~

A signature is not required for every development load scenario, but a broken shipping signature/package is a separate release defect.

## 7 — dependencies

macOS:

~~~bash
otool -L "MyPlugin.plugin/Contents/MacOS/MyPlugin"
~~~

Windows:

- inspect imports/dependencies with appropriate PE tooling.

Look for:

- missing dylib/DLL;
- wrong architecture;
- development-only path;
- Debug CRT;
- missing GPU/licensing helper;
- incompatible third-party runtime.

## 8 — initialization crash

If AE discovers the module and crashes during load:

- attach debugger before host launch if possible;
- inspect crash report/dump;
- minimize global/static constructors;
- disable optional subsystems;
- compare against sample baseline;
- confirm callback exception containment.

A module that crashes before logging its own initializer may still fail in static initialization.

## 9 — duplicate IDs/names/resources

Check product identifiers copied from Skeleton or another plug-in.

Two modules with conflicting identifiers/resources can create confusing behavior.

Rename all required identity fields deliberately; do not mass-search/replace blindly.

## 10 — AE cache/preferences only after evidence

Clearing preferences/caches can be useful, but do not make it step 1 for every loader problem.

First prove the installed artifact/path/architecture/resource are correct so clearing state does not hide a packaging defect.

## Minimal loader report

Record:

~~~text
AE version/build:
OS/arch:
plugin path:
plugin SHA-256:
binary architecture:
PiPL entry:
exported entry:
signature result:
dependencies:
observed host behavior:
~~~

## Stop rule

Change only one layer at a time.

The goal is to identify the first broken link:

~~~text
discovery
→ architecture
→ resource/export
→ trust/signing
→ dependencies
→ initialization
~~~
