# macOS — Xcode setup

## Start from an Adobe SDK sample

For a native effect, start from Skeleton or the closest supplied SDK example instead of reconstructing an Xcode target from scratch.

This preserves host-specific pieces that are easy to miss:

- Adobe include configuration;
- PiPL/resource generation;
- bundle type and extension;
- exported entry point setup;
- architecture settings;
- sample utility sources;
- build phases expected by the SDK project.

A safe bootstrap sequence is:

~~~text
copy closest sample
→ build untouched sample
→ load untouched sample in AE
→ rename product identifiers
→ replace implementation incrementally
→ keep the resource/build contract intact
~~~

Do not change code, project format, output path, architecture and signing all at once. When the first load fails, you want only one variable to investigate.

## Development output path

The SDK guide recommends the per-user MediaCore path for macOS development:

    ~/Library/Application Support/Adobe/Common/Plug-ins/7.0/MediaCore/

The 7.0 directory is the historical CC convention.

Do not point normal Xcode build output at the system /Library MediaCore path and then build with sudo. The current SDK guide explicitly warns that this can leave root-owned build artifacts and produce confusing dependency-graph or temporary-file failures.

If you need a system-level copy for a specific test:

1. build normally as the user;
2. finish signing the built bundle;
3. copy the finished artifact with the required privileges.

## Separate build output from release staging

For a commercial project, distinguish:

~~~text
Derived/build output
→ development install copy
→ release staging directory
→ signed/notarized package
~~~

QA should test the exact staged artifact that release signs and packages, not a different binary rebuilt later from the same commit.

## Xcode scheme

For the Run scheme executable, select the installed After Effects host.

Then Build & Run can:

1. build the plug-in;
2. place/copy it into the development plug-in path;
3. start AE under the debugger.

Attach behavior depends on macOS and AE build. See 03-DEBUGGING.md.

## Build configurations

Recommended minimum:

- Debug — assertions/logging, symbols, development signing;
- ReleaseWithSymbols — production optimization plus symbol archive;
- Release — shipping settings if kept separately.

Avoid a release configuration that silently changes semantic compiler options beyond optimization.

Archive the dSYM for every shipped binary and tie it to:

- product version;
- build number;
- git commit;
- binary SHA-256;
- architectures.

## macOS 15+ development signing

The current AE SDK guide notes that macOS 15+ prevents loading unsigned plug-ins. Add a development signing step after the binary has reached its final built state.

Ad-hoc signing is acceptable for local development. It is not the release trust model.

Do not mutate the bundle after signing and then debug a mysteriously rejected copy.

## Deployment target

Choose the minimum macOS deployment target from the actual product support matrix.

It must agree with:

- supported AE versions;
- third-party library minimums;
- APIs your code uses;
- QA coverage.

Do not set an older target merely because Xcode accepts it.

## Warning policy

Use strict warnings for your own code. If Adobe/third-party headers produce legacy warning noise, isolate that boundary instead of globally disabling useful warnings.

Recommended release rule:

- new warning in product code fails CI;
- known external-header warnings are documented and scoped;
- no warning suppression without a reason.

## Reproducibility

Record for every native build:

- Xcode version;
- Apple Clang version;
- SDK path/hash identity;
- macOS SDK version;
- deployment target;
- architectures;
- build configuration;
- git SHA.

"Built on my Mac" is not a release record.

## Verification boundary

В [исторической записи от 2026-09-30](../VERIFICATION.md#recorded-baseline-2026-09-30) сообщается об успешных macOS arm64 syntax/type checks с SDK 25.6. Точный source SHA/хэши проверенных translation units в этой записи отсутствуют; она не подтверждает компиляцию нынешних файлов. Для своего продукта разработчик отдельно проверяет сборку, линковку, ресурсы, подпись и загрузку конкретного артефакта. Глава описывает этот маршрут без заявления о новом build/host результате Библии.
