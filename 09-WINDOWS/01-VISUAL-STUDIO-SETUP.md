# Windows — Visual Studio setup

## Start from an Adobe sample

Exact copied-Examples/Skeleton solution, include/resource chain, MSBuild and
final PE/export/import checks: [production walkthrough](09-PRODUCTION-BUILD-PIPELINE.md).
Check available solution configurations/toolset before choosing Release/x64;
the walkthrough gives expected observations, not recorded Windows build output.

Do not reconstruct an After Effects effect project from an empty Visual Studio project unless you have a specific reason and understand every host-specific build step.

The SDK guide explicitly recommends starting from Skeleton or the nearest sample because Windows effect projects contain PiPL resource-generation steps that are easy to lose.

Safe bootstrap:

~~~text
copy closest SDK sample
→ build untouched x64 sample
→ load untouched sample in AE
→ preserve resource/custom build steps
→ rename identifiers
→ replace implementation incrementally
~~~

If the untouched sample does not load, stop there. Do not continue layering product code onto a broken project baseline.

## BuildAll and individual projects

The SDK includes BuildAll.sln for the examples, but product development should still make the individual target reproducible on its own.

Record:

- Visual Studio version;
- MSVC toolset;
- Windows SDK version;
- AE SDK version/build;
- configuration;
- target architecture.

## PiPL generation is part of the build

Windows uses the cross-platform .r resource source and a conversion/custom build step to generate Windows resource input.

The important contract is not the exact historical tool name. It is:

~~~text
.r source
→ Adobe PiPL conversion step
→ Windows resource
→ linked into final .aex
~~~

Do not copy only the C++ files out of a sample and forget the resource step.

PiPL/global setup capability declarations must remain consistent.

## Development output

The SDK sample guidance supports a development output path such as:

    C:\Program Files\Adobe\Common\Plug-ins\7.0\MediaCore\

The sample projects also support AE_PLUGIN_BUILD_DIR for a common development output directory.

This is a development convenience. Production installers should obtain Adobe install paths through the documented registry values instead of hardcoding the development path.

## Privileges

Writing directly under Program Files may require elevation.

Do not solve every build problem by permanently running Visual Studio as Administrator. A cleaner product workflow is:

~~~text
normal build directory
→ post-build/dev install step with explicit privilege if needed
→ AE load
~~~

Keep compile output and privileged installation conceptually separate.

## Configurations

Minimum practical set:

- Debug x64;
- Release x64;
- ARM64 equivalents only when the product intentionally supports a native Windows-on-Arm host.

For release builds:

- optimization enabled deliberately;
- symbols generated;
- runtime library settings consistent across your code/dependencies;
- no accidental Debug CRT dependency;
- warnings reviewed.

Archive the PDB for every shipped binary.

## Runtime library and ABI discipline

All native components loaded into the same product should have deliberate runtime/ABI choices.

Check:

- /MD vs /MDd;
- iterator/debug ABI mismatches;
- third-party library toolset;
- exception/RTTI choices if shared headers cross boundaries;
- exported symbol surface.

Do not expose STL objects as a long-lived binary ABI between independently versioned modules.

## Export surface

A native AE plug-in should export only what the host/product needs.

Avoid leaking third-party library symbols from the .aex. Symbol collisions inside the host process can produce failures far away from the component that caused them.

Treat exported-symbol review as a release check for products linking large C++ libraries.

## Warning policy

Use a high warning level for product code and move warning suppressions to the smallest possible scope.

Do not disable a useful warning globally because a legacy SDK header emits it.

## Reproducibility

A release record should make it possible to answer:

- which compiler built this exact binary?;
- which AE SDK was used?;
- which architecture?;
- which resource/PiPL source?;
- which git SHA?;
- which PDB matches it?;
- what is the SHA-256 of the shipped .aex?

## Verification boundary

This chapter defines the Windows build workflow. Historical compiler evidence for Bible source snapshots is optional evidence, not a pending completion gate for the documentation.
