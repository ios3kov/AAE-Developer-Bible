# Windows developer bible

Этот раздел описывает Windows lifecycle native After Effects product: Visual Studio, x64/ARM64, debugging, GPU, signing, packaging и CI.

Это **platform guide для разработчика продукта**, а не обязательная Windows build lane самой Bible.

## Platform strategy

Сначала определите:

- x64 support;
- ARM64 policy;
- minimum Windows policy;
- compiler/toolset;
- GPU backend;
- dependency/runtime policy;
- installer/signing policy.

Не начинайте с project configuration, пока support matrix не определена.

## x64

x64 остаётся типичным baseline для существующего Windows ecosystem, но product должен документировать собственную support policy, а не полагаться на привычку.

## ARM64

ARM64 support — отдельный target.

Нужно проверить всю native chain:

- main `.aex`;
- dependent DLLs;
- helper executables;
- codecs/libraries;
- GPU/runtime components;
- installer logic.

Один ARM64 main binary не делает продукт ARM64-ready.

## Visual Studio / Adobe sample

Начинайте от ближайшего Adobe SDK sample, чтобы сохранить:

- PiPL conversion/resource step;
- required exports;
- project defines;
- host-specific build layout.

Сначала соберите/поймите sample shell, потом переносите implementation.

## Runtime/CRT/ABI

Windows native product должен иметь deliberate policy:

- `/MD` vs debug runtime;
- toolset;
- iterator/debug ABI;
- exception/RTTI boundary;
- third-party DLL architecture;
- exported symbol surface.

Не экспортируйте STL types как stable ABI между independently versioned modules.

## Development install

Разделяйте build output и privileged install step.

Не делайте Visual Studio постоянно elevated только потому, что MediaCore path находится под Program Files.

## Debugging

Debug strategy:

- exact AE process;
- actual loaded module path;
- matching PDB;
- architecture;
- dependency tree;
- MFR/GPU state;
- crash dump/minimal repro.

См. [Windows debugging](03-DEBUGGING.md).

## GPU

Windows GPU product может иметь CPU/CUDA/DirectX backends.

Backend/device selection, runtime dependencies и shader/kernel assets должны быть explicit.

См. [Windows GPU](04-GPU.md).

## Signing

Release binaries/installer могут использовать Authenticode according to product policy.

Signing не исправляет broken binary/resource/dependency layout.

Сначала правильный artifact, потом signing.

## Installer

Installer должен:

- использовать documented Adobe install-path policy/registry;
- владеть только своими files;
- поддерживать upgrade/uninstall;
- не удалять user/project data;
- учитывать multiple AE versions;
- логировать actionable install errors.

## PDB discipline

Для каждой shipping binary сохраняйте matching PDB и artifact identity.

Новый PDB под старым version label делает crash analysis недостоверным.

## CI

Типичный Windows product lane:

```text
portable tests
→ x64/ARM64 native build as claimed
→ resource/PiPL inspection
→ package
→ signing
→ installer artifact
```

Host smoke может быть отдельным product lane; Bible не обязана выполнять его для source examples.

## Dependency policy

Для каждой native dependency фиксируйте:

- version;
- license;
- x64/ARM64;
- static/dynamic;
- runtime DLL;
- minimum OS;
- signing/installer implications.

Не обнаруживайте x64-only dependency уже у пользователя.

## Common mistakes

- потерять PiPL resource conversion при переносе project;
- hardcode developer AE path;
- случайно shipping Debug CRT dependency;
- PDB не совпадает с `.aex`;
- DLL architecture mismatch;
- DirectX/CUDA asset отсутствует в installer;
- installer кладёт файл не в тот Adobe path;
- multiple stale copies plug-in в разных MediaCore directories;
- signing different binary than QA evaluated.

## Recommended read order

1. [Visual Studio setup](01-VISUAL-STUDIO-SETUP.md)
2. [x64 / ARM64](02-X64-ARM64.md)
3. [Debugging](03-DEBUGGING.md)
4. [GPU](04-GPU.md)
5. [Code signing](05-CODE-SIGNING.md)
6. [Installation/packaging](06-INSTALLATION-PACKAGING.md)
7. [CI](07-CI.md)
8. [SDK contract/source validation](08-NATIVE-SDK-VALIDATION.md)
9. [Production build pipeline](09-PRODUCTION-BUILD-PIPELINE.md)

## Related Bible sections

- [Environment matrix](../00-START-HERE/02-ENVIRONMENT-MATRIX.md)
- [Build system strategy](../01-ARCHITECTURE/06-BUILD-SYSTEM.md)
- [Testing](../10-TESTING/README.md)
- [Distribution](../11-DISTRIBUTION/03-RELEASE-CHECKLIST.md)

## Evidence boundary

This section documents Windows product development workflow. Bible does not need to build its reference source on every Windows architecture for the guidance to be editorially complete.
