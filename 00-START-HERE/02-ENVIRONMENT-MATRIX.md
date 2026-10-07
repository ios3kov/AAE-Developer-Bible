# Environment matrix

Перед разработкой зафиксируйте **целевую среду продукта**.

Не используйте:

- “latest AE”;
- “latest macOS”;
- “обычный Windows PC”;
- “GPU enabled”;

как спецификацию. Эти формулировки невозможно воспроизвести.

## Зачем нужна матрица

Она отвечает на четыре разных вопроса:

1. **Что продукт обещает поддерживать?**
2. **На чём продукт разрабатывается?**
3. **Что реально проверялось?**
4. **Что является только planned/experimental?**

Не смешивайте эти четыре статуса.

## Core dimensions

| Dimension | Что зафиксировать |
|---|---|
| After Effects | product-supported versions/build families |
| Adobe SDK | baseline version/build used for native contracts |
| OS | supported minimum/maximum policy |
| CPU architecture | arm64/x86_64/x64/ARM64 as relevant |
| compiler/toolchain | Xcode/Clang or Visual Studio/MSVC generation |
| extension type | Effect / AEGP / AEIO / Artisan / Script / CEP / hybrid |
| pixel formats | 8/16/32 bpc actually supported by feature |
| SmartFX | yes/no + ROI assumptions |
| MFR | supported/disabled/experimental |
| GPU | backend/device requirements |
| panel runtime | CEP version / migration boundary |
| signing | development vs release policy |
| dependencies | bundled/runtime/framework requirements |
| host products | AE only vs Premiere compatibility where applicable |

## Source boundaries

Current review2026-10-07: published AE UXP members examined here require27.0;
native guide lists26.5 changes, but actual26.5 SDK headers not acquired/reviewed.
[Currentness/source map](../CURRENTNESS-REVIEW-2026-10-07.md) separates these from
retained25.6 exact baseline. Do not assume a26.5 native host exposes27.0 UXP API.

[Claim/source/version table](../BLOCK-5-SOURCES.md) keeps SDK ABI, documented host requirements, panel runtime and platform policy in separate columns. SDK 25.6 build 61 is the Bible native baseline, not an AE/OS support range. Current Adobe Windows-on-Arm requirements are documented separately from our unperformed native ARM64 host tests.

## Platform baseline

| Dimension | macOS | Windows |
|---|---|---|
| IDE | Xcode | Visual Studio |
| Main native architecture | arm64; x86_64 only if product still supports Intel | x64; ARM64 only if product intentionally supports it |
| Native effect package | plug-in bundle from SDK project | `.aex` |
| Common dev plug-in location | Adobe Common MediaCore path | Adobe Common MediaCore path / registry-driven product install |
| Debugger | Xcode / LLDB | Visual Studio / WinDbg |
| Development signing | ad-hoc where platform requires it | usually not required for local load |
| Release signing | Developer ID | Authenticode |
| OS trust path | Gatekeeper/notarization | Windows certificate/reputation chain |

Exact paths and platform details live in the platform chapters.

## Status dimensions

For each row/property use explicit state:

- **supported** — product policy says yes;
- **tested** — concrete evidence exists;
- **experimental** — feature exists but product does not promise it;
- **planned** — roadmap only;
- **unsupported** — deliberately not supported;
- **unknown** — not yet decided.

Do not use a green checkmark for both “supported” and “tested”; they are different claims.

## Example project matrix

~~~yaml
product: ExamplePlugin
product_version: 1.0.0

after_effects:
  supported:
    - "25.x"
    - "26.x"
  sdk_baseline: "25.6 build 61"

macos:
  supported: true
  min_os: "product policy"
  arch:
    arm64: supported
    x86_64: unsupported
  toolchain: "Xcode release policy"

windows:
  supported: true
  arch:
    x64: supported
    arm64: planned
  toolchain: "Visual Studio release policy"

effect:
  bpc:
    8: supported
    16: supported
    32: supported
  smartfx: supported
  mfr: experimental

gpu:
  mac:
    metal: supported
  windows:
    directx: experimental
    cuda: unsupported

panel:
  runtime: "CEP"
  migration_target: "UXP when target APIs are available"

premiere:
  compatible: unsupported
~~~

## Development matrix vs support matrix

### Development matrix

What engineers need to build/debug:

- toolchains;
- SDK path;
- debug host;
- signing setup;
- local install path;
- symbols.

### Support matrix

What customers/users are promised:

- AE versions;
- OS versions;
- architectures;
- GPU/backend;
- feature limitations.

### Test/evidence matrix

What was actually exercised.

Keep these separately even if they are generated from one source file.

## AE version identity

Record enough to distinguish:

- major/minor product version;
- exact build when diagnosing regressions;
- Beta vs release where behavior may differ.

A project saying only “AE 26” is often insufficient for compatibility debugging.

## SDK baseline is not support range

The SDK used to read/build native contracts does not automatically equal:

- minimum supported AE;
- maximum supported AE;
- binary compatibility range.

The product's compatibility policy must be stated separately.

## Architecture matrix

### macOS

Decide deliberately:

- arm64 only;
- Universal arm64+x86_64;
- separate artifacts.

Do not accidentally claim Intel support just because one dependency happens to contain an x86_64 slice.

### Windows

Decide deliberately:

- x64;
- Windows ARM64;
- separate installers/packages if needed.

Third-party libraries can constrain architecture even when your own code compiles.

## GPU matrix

Do not use one boolean `gpu: true`.

Record:

- backend;
- supported devices/families;
- minimum API/OS policy if relevant;
- CPU fallback;
- feature parity expectations.

Example:

~~~yaml
gpu:
  cpu_fallback: true
  mac:
    metal: supported
  windows:
    directx: supported
    cuda: unsupported
~~~

## MFR matrix

Record separately:

- code path thread-safe by design;
- capability advertised;
- enabled in release policy;
- known exclusions.

A product can have MFR-safe architecture while still shipping with MFR disabled for a particular release.

## Panels

Panel support needs its own lifecycle/version boundary:

- CEP runtime;
- host version;
- Node usage;
- external helper;
- migration plan.

Do not put business logic directly into CEP-specific APIs if a UXP migration is expected.

## Third-party dependencies

For each native dependency record:

- version;
- architecture slices;
- linkage model;
- license;
- signing/notarization implications;
- GPU/runtime requirements.

Dependency policy belongs in the environment matrix because it can reduce supported platforms before your own code does.

## Matrix as product input

Use the matrix to drive:

~~~text
architecture decisions
→ build variants
→ CI lanes
→ test coverage
→ installer rules
→ compatibility page
→ release notes
→ support diagnostics
~~~

Do not maintain seven contradictory copies manually if one structured source can generate them.

## Bible vs product matrix

AE Developer Bible documents **how to design this matrix**.

Bible itself does not need to build every combination listed in examples. When Bible reports a historical runtime/compiler result, it records that exact environment as evidence for that claim only.

## Related chapters

- [Version compatibility](../01-ARCHITECTURE/04-VERSION-COMPATIBILITY.md)
- [macOS](../08-MACOS/README.md)
- [Windows](../09-WINDOWS/README.md)
- [Testing](../10-TESTING/README.md)
- [Distribution](../11-DISTRIBUTION/03-RELEASE-CHECKLIST.md)
