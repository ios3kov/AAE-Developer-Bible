# Build system strategy

The first build-system goal is not elegance. It is preserving the exact host integration machinery required to produce a loadable After Effects component.

## Phase 1 — prove Adobe sample projects

For the first native plug-in, use the project shipped with the exact target SDK:

- Xcode on macOS;
- Visual Studio on Windows.

Adobe's SDK guidance recommends starting from the closest sample/Skeleton rather than reconstructing the project because host-specific PiPL/resource build steps are easy to miss.

Baseline:

~~~text
exact SDK sample
→ untouched build
→ development install
→ AE load
→ record evidence
~~~

Do this before introducing a meta-build system.

## Phase 2 — separate portable core

A healthy architecture usually looks like:

~~~text
core/
  algorithms
  data model
  protocol
  serialization
  pure tests

adapters/
  effect
  AEGP
  AEIO
  panel/helper

platform build shells/
  Xcode
  Visual Studio
~~~

The portable core can use CMake or another cross-platform system early because it does not need PiPL/host loading.

The thin host target can remain in the official sample project until equivalence is understood.

## Phase 3 — enumerate every hidden build responsibility

Before replacing Xcode/Visual Studio project plumbing, inventory:

- C/C++ sources;
- exported entry points;
- PiPL/resource source;
- Windows PiPL conversion/custom build step;
- bundle/aex output layout;
- include paths;
- SDK utilities;
- platform frameworks/libs;
- architecture declarations;
- deployment target;
- compiler defines;
- asset/kernel generation;
- signing hooks;
- post-build development install.

If one item is omitted, a clean compile may still produce a non-loadable plug-in.

## CMake migration gate

A unified CMake/native target is accepted only after it produces an artifact equivalent in all relevant host-visible ways.

Compare sample-project build vs new build:

- exported symbols;
- architectures;
- PiPL/resource contents;
- bundle/file layout;
- linked dependencies;
- version metadata;
- load behavior in AE;
- render/operation fixture.

Do not delete the known-good project until this comparison passes.

## Project layout options

### Official host shells + shared core

~~~text
/core
/tests
/plugin-mac   Xcode
/plugin-win   Visual Studio
~~~

Lowest migration risk.

### Generated native projects

CMake generates Xcode/VS while custom commands recreate resources and packaging.

Useful after the build contract is understood.

### Fully scripted toolchain

Appropriate for mature CI, but every host-specific resource/signing/install step must remain explicit.

## Dependencies

Every dependency record should include:

- name/version;
- source and hash;
- license;
- redistribution rights;
- macOS architectures;
- Windows architectures;
- static/dynamic;
- minimum OS/runtime;
- exception/RTTI/runtime-library assumptions;
- thread-safety/MFR implications;
- GPU/runtime requirements;
- signing/notarization implications.

Do not discover an x64-only or debug-only dependency on the customer's machine.

## ABI boundaries

Keep third-party C++ ABI from leaking into long-lived interfaces between independently versioned components.

Prefer C-shaped/versioned protocol structures across module boundaries.

Standard-library ABI, allocator, runtime and compiler mode can differ across components/builds.

## Reproducibility

Every release records:

- git SHA/tag;
- SDK version/build/hash identity;
- compiler/toolchain;
- OS SDK;
- target architectures;
- dependency lock;
- configuration;
- product/schema/protocol versions;
- unsigned/staged artifact hash;
- signed/package artifact hashes.

Latest is not a reproducible version.

## Generated files

Generated resource/protocol/version files need one authoritative source.

CI should fail if:

~~~text
source inputs
→ regeneration
→ working tree differs
~~~

Do not commit generated data that silently drifts from its source without a verification rule.

## CI lanes

Separate:

~~~text
portable tests
→ native compile/resources
→ package
→ host test
→ release signing
~~~

A documentation or unit-test runner does not substitute for a native platform/host lane.

Release credentials must not be exposed to untrusted pull requests.

## Development install is not release package

Keep distinct:

~~~text
compiler output
→ dev install copy
→ immutable release candidate
→ signed/notarized installer/package
~~~

QA should test the same candidate that release publishes.

## Stop rule

Do not migrate the plug-in build system merely because a new system is more fashionable.

Migrate when it provides a concrete benefit and the new output has proven host equivalence.

See [macOS](../08-MACOS/README.md), [Windows](../09-WINDOWS/README.md) and [distribution](../11-DISTRIBUTION/03-RELEASE-CHECKLIST.md).
