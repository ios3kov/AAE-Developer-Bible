# Windows — production build pipeline

This chapter connects the Windows build, signing and installer topics into one release flow.

It is a process definition, not proof that the Bible examples already compile or load on Windows.

## Inputs

Pin:

- source commit;
- Adobe AE SDK version/build;
- Visual Studio version;
- MSVC toolset;
- Windows SDK version;
- target architectures;
- dependency versions;
- product version/build number.

Do not let CI silently change compiler or SDK generation for a release branch.

## Recommended stages

```text
clean checkout
 -> restore/validate dependencies
 -> compile PiPL/resources
 -> build x64
 -> build ARM64 if supported
 -> run native/unit tests
 -> inspect imports/dependencies
 -> sign .aex/.dll/.exe
 -> build installer
 -> sign installer
 -> verify signatures
 -> install on clean test VM/machine
 -> launch/load in AE
 -> archive PDB + manifest + checksums
```

## Visual Studio configuration

Keep Release configuration explicit:

- correct PlatformToolset;
- correct WindowsTargetPlatformVersion;
- C++ language level;
- Runtime Library choice;
- warnings policy;
- exception/RTTI policy;
- preprocessor version macros;
- resource build step;
- output directory.

Do not depend on environment variables that exist only on one developer workstation unless CI defines and validates them.

## Architecture

x64 remains the normal baseline for supported desktop AE releases unless your compatibility matrix says otherwise.

If ARM64 is shipped:

- build it as a real target;
- verify every static/dynamic dependency;
- test on a native ARM64 host path;
- do not present x64 emulation as native ARM64 verification.

Keep architecture artifacts separate until packaging.

## Dependency inspection

Before signing, inspect the final binary for accidental dependencies on:

- Debug CRT;
- developer-local DLLs;
- absolute build paths;
- unshipped helper libraries.

A successful link does not prove the customer's machine has the same runtime environment.

## Signing

Sign final binaries after all mutation:

```text
.aex
.dll
.exe/helper
 -> installer
```

Use SHA-256 and a trusted timestamping workflow appropriate to the organization's signing infrastructure.

Then verify signatures independently.

See [code signing](05-CODE-SIGNING.md).

## Installer

Installer logic should:

- resolve official Adobe plug-in install locations;
- handle supported multi-version AE installations intentionally;
- keep user data/presets/license state according to documented policy;
- support clean upgrade/uninstall semantics;
- log actionable failure details.

Do not hardcode only one After Effects version path.

## Clean-machine test

Install the exact signed release artifact on a machine/VM that does not contain the developer build tree.

Verify:

1. install succeeds with expected privileges;
2. expected files are present;
3. no missing runtime dependency appears;
4. AE discovers and loads the plug-in;
5. smoke test succeeds;
6. uninstall removes only product-owned files.

## AE host matrix

Record per supported combination:

- Windows version;
- AE version/build;
- architecture;
- install path selected;
- load result;
- smoke-test result.

A signed installer is not proof of AE compatibility.

## Symbols

Archive:

- PDB files;
- exact signed binaries;
- source commit;
- compiler/toolset versions;
- build manifest.

Never rely on regenerating PDBs later from "same source". The shipped binary and symbols are one release identity.

## Failure gates

Fail the release on:

- resource compilation error;
- binary build error;
- wrong architecture;
- unexpected dependency;
- signature failure;
- installer build/signature failure;
- clean install failure;
- AE load/smoke-test failure.

## Release artifact identity

Create a manifest containing at least:

```text
product version
git commit
SDK version/build
compiler/toolset
target architecture
binary hashes
installer hash
signing timestamp metadata
supported AE range
```

This makes support and rollback possible without guessing what was shipped.
