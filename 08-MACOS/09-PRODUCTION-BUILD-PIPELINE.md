# macOS — production build pipeline

This chapter connects the individual macOS topics into one reproducible release flow.

It does **not** mean the Bible examples are host-verified. A production pipeline is only accepted after an actual plug-in bundle is built, installed and loaded in the declared AE/OS matrix.

## Inputs

## Конкретный учебный маршрут: SDK Skeleton

Использовать локально лицензированный SDK 25.6 `Examples/Template/Skeleton/Mac/Skeleton.xcodeproj`.
Скопировать **весь Examples tree** в новый workspace, чтобы relative Headers/Util
и Rez dependencies сохранились. В Bible не публиковать vendor sources.

```bash
xcodebuild -list -project "$EXAMPLES/Template/Skeleton/Mac/Skeleton.xcodeproj"
xcodebuild -project "$EXAMPLES/Template/Skeleton/Mac/Skeleton.xcodeproj" \
  -scheme Skeleton -configuration Debug -destination 'generic/platform=macOS' \
  -derivedDataPath "$WORK/DerivedData" build \
  ARCHS='arm64 x86_64' ONLY_ACTIVE_ARCH=NO \
  MACOSX_DEPLOYMENT_TARGET=12.0 CODE_SIGNING_ALLOWED=NO \
  CONFIGURATION_BUILD_DIR="$WORK/Products"
```

`EXAMPLES` — copied tree, `WORK` — fresh development output. Target 12.0 — example
build setting, не проверенный minimum OS. Проверить toolchain/sample availability;
предупреждения старого SDK project не игнорировать. Sample compiler settings вроде
`-fno-threadsafe-statics` требуют review перед использованием lazy shared state.
Ожидаемый output — `Products/Skeleton.plugin`, не AE installation. Rez step должен
создать resource в bundle; build output проверить, а не угадать его по suffix.

```bash
lipo -archs "$WORK/Products/Skeleton.plugin/Contents/MacOS/Skeleton"
nm -gU "$WORK/Products/Skeleton.plugin/Contents/MacOS/Skeleton"
otool -L "$WORK/Products/Skeleton.plugin/Contents/MacOS/Skeleton"
plutil -p "$WORK/Products/Skeleton.plugin/Contents/Info.plist"
```

Ожидаемые **виды** результатов: requested slices; entry symbols для фактического
sample; intended dependencies; consistent bundle version/identifier. Это не
подставленные успешные outputs. Source, PiPL Name/match/code/flags/version и
bundle identity изменить согласованно при graft Minimal Gain. Не устанавливать
два renamed Skeleton bundles с одинаковым match name и считать их независимыми.

Development: ad-hoc sign отдельный built bundle, не рабочий AE. Debug: launch/attach
development host по [version-gated debugger policy](03-DEBUGGING.md), breakpoint
на EffectMain, проверить cmd и фактически loaded image path/UUID. Если breakpoint
не hit: discovery path → duplicate identity → architecture → signature/quarantine
→ exports/PiPL → symbols; не начинать с изменения pixel math.

Release shell: archive exact binary+dSYM (`dwarfdump --uuid` matching), sign nested
code inside-out с выбранной Developer ID identity, package, notary submit/log,
staple supported container, verify final artifact. Команды и security границы в
[signing](05-SIGNING-NOTARIZATION.md). Notary success не доказывает AE load.
Install staging ведёт owned-files manifest; update при закрытом AE сохраняет прежний
artifact/metadata для rollback, не удаляет presets/чужие plug-ins. Повторная установка
на developer Mac не clean-machine result. CI outputs связываются с source/hash,
toolchain, SDK и UUID, не только названием release ZIP.

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
