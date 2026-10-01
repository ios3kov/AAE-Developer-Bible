# macOS — production build pipeline

This chapter connects the individual macOS topics into one reproducible release flow.

It does **not** mean the Bible examples are host-verified. A production pipeline is only accepted after an actual plug-in bundle is built, installed and loaded in the declared AE/OS matrix.

## Inputs

Pin:

- source commit;
- Adobe AE SDK version/build used for compilation;
- Xcode version;
- macOS runner/build image;
- deployment target;
- architectures;
- dependency versions;
- product version/build number.

Do not let the release job silently pick "latest" toolchains.

## Recommended stages

```text
clean checkout
 -> dependency validation
 -> compile resources
 -> build arm64
 -> build x86_64 if supported
 -> merge/produce universal bundle
 -> inspect architectures
 -> verify PiPL/resources/exports
 -> run native/unit tests
 -> sign nested code
 -> sign plug-in bundle
 -> package
 -> notarize
 -> staple where applicable
 -> verify package
 -> install on clean test machine
 -> launch/load in AE
 -> archive symbols + manifest + checksums
```

## Build configuration

Release builds should normally have:

- `NDEBUG`/release assertions policy explicitly chosen;
- no debug-only host backdoors;
- warnings reviewed;
- deterministic version macros;
- symbols produced even if stripped from the shipping binary;
- consistent C++ language level;
- dependency search paths that do not depend on one developer's home directory.

## Architecture verification

After building, inspect the Mach-O binary:

```bash
lipo -info "/path/to/MyPlugin.plugin/Contents/MacOS/MyPlugin"
```

If universal support is claimed, both required slices must be present.

Also verify dependent dylibs have compatible architecture slices. A universal main binary with arm64-only nested code is not a universal product.

## Bundle verification

Before signing, verify:

- expected executable path;
- bundle identifier/version;
- PiPL/resource output exists;
- only intended helper/dylib files are present;
- no local build cache or secrets were copied into the bundle.

## Signing order

Sign from the inside out:

```text
nested dylib/helper
 -> framework if any
 -> plug-in bundle
 -> installer/package/container
```

Do not mutate signed code afterwards.

Development ad-hoc signing and release Developer ID signing are different trust models.

See [signing and notarization](05-SIGNING-NOTARIZATION.md).

## Notarization

Treat notarization as a release gate, not as an optional upload step.

The pipeline should retain:

- submission ID;
- notarization result/log;
- exact artifact hash submitted;
- final stapled package hash where stapling applies.

A rebuilt package is a different artifact and needs to go through the gate again.

## Installation test

Do not validate only from the build tree.

Install the exact packaged artifact using the same path/policy as customers, then verify:

1. file ownership/permissions;
2. plug-in appears in expected host;
3. AE loads it without quarantine/signature errors;
4. basic operation succeeds;
5. uninstall removes only product-owned files.

## AE host matrix

For every supported AE/macOS/architecture combination, record:

- AE exact version/build;
- macOS version;
- architecture;
- native/Rosetta path if applicable;
- load result;
- required functional smoke test.

Intel support is not proved merely because an x86_64 slice exists.

## Symbols

Archive:

- dSYM;
- exact release binary;
- source commit;
- compiler/toolchain version;
- build manifest.

Symbols must be tied to the exact binary UUIDs shipped.

## Failure gates

Release must fail on:

- compile/resource error;
- unexpected architecture;
- missing nested dependency;
- signing failure;
- notarization rejection;
- package checksum mismatch;
- clean install failure;
- AE load/smoke-test failure.

A warning-only release pipeline is not sufficient for these cases.

## Reproducibility

The goal is not necessarily byte-for-byte reproducibility across Apple's signing/notarization systems. The goal is a fully reconstructable build recipe with traceable source, inputs and final artifact identity.
