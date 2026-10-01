# macOS developer bible

Этот раздел описывает полный macOS lifecycle native After Effects product: от SDK/Xcode setup до debugging, GPU, signing, packaging и CI.

Это **platform guide для разработчика продукта**. Bible не обязана собирать собственные demo binaries, чтобы объяснять workflow.

## Platform strategy

На Mac сначала определите product policy:

- arm64 only;
- Universal arm64 + x86_64;
- separate helper/native components;
- minimum macOS policy;
- GPU backend;
- signing/notarization requirements.

Не начинайте с Xcode target settings, пока architecture/support matrix не записана.

## Apple Silicon

arm64 — отдельная architecture с собственными implications:

- native dependencies;
- assembly/SIMD assumptions;
- GPU/backend libraries;
- helper tools;
- code signing of nested components.

«Main binary arm64» не означает, что весь bundle Apple-Silicon-ready.

## Intel support

Если продукт всё ещё заявляет Intel support, решите:

- Universal one-bundle;
- separate artifacts;
- end-of-support policy.

Каждая nested native dependency должна соответствовать этой политике.

## Build shell

Для native AE work безопаснее начинать от ближайшего Adobe SDK sample project.

Причина — sample уже содержит host-specific resource/PiPL/build plumbing.

Сначала поймите этот contract, потом переносите build в собственную систему.

## Development install

Разделяйте:

```text
compiler output
→ development install copy
→ immutable release candidate
→ signed/notarized distribution
```

Не тестируйте случайно один bundle, а публикуйте другой.

## Debugging

Debug strategy должна включать:

- exact AE executable/build;
- actual loaded plug-in path;
- matching dSYM;
- architecture;
- MFR/GPU state;
- minimal repro.

Platform signing restrictions могут влиять на debugger attach; version-sensitive details находятся в [debugging chapter](03-DEBUGGING.md).

## GPU

macOS GPU work должен сохранять один effect semantics между CPU и Metal.

Apple Silicon unified memory не отменяет synchronization/lifetime costs.

См. [GPU development](04-GPU.md).

## Signing

Различайте:

- ad-hoc/dev signing;
- Developer ID signing;
- notarization;
- stapling/verification;
- signed nested dependencies.

Не модифицируйте bundle после final signing.

## Packaging

Installer/package должен владеть своими files и не удалять чужие Adobe/user assets.

Upgrade/uninstall policy проектируется так же тщательно, как first install.

## CI

Полезные lanes:

```text
portable tests
→ native platform build
→ bundle/resource inspection
→ package
→ release signing/notarization
```

Конкретный product может добавить host smoke lane, но это не часть редакционной готовности Bible.

## Evidence discipline

Для product artifact полезно сохранять:

- Git SHA;
- SDK baseline;
- Xcode/Clang identity;
- architectures;
- dependency versions;
- bundle hash;
- dSYM;
- signing/notary record.

## Common mistakes

- assuming Universal because Xcode target says Universal while nested dylib is single-arch;
- copying C++ source out of sample and losing PiPL/resource step;
- signing outer bundle before nested components;
- modifying bundle after signing;
- using developer absolute paths for resources;
- debugging a stale copy from another MediaCore location;
- treating ad-hoc signing as release signing;
- notarizing a different artifact than QA tested.

## Recommended read order

1. [Xcode setup](01-XCODE-SETUP.md)
2. [Universal binary](02-UNIVERSAL-BINARY.md)
3. [Debugging](03-DEBUGGING.md)
4. [GPU](04-GPU.md)
5. [Signing/notarization](05-SIGNING-NOTARIZATION.md)
6. [Installation/packaging](06-INSTALLATION-PACKAGING.md)
7. [CI](07-CI.md)
8. [SDK contract/source validation](08-NATIVE-SDK-VALIDATION.md)
9. [Production build pipeline](09-PRODUCTION-BUILD-PIPELINE.md)

## Related Bible sections

- [Environment matrix](../00-START-HERE/02-ENVIRONMENT-MATRIX.md)
- [Build system strategy](../01-ARCHITECTURE/06-BUILD-SYSTEM.md)
- [Testing](../10-TESTING/README.md)
- [Distribution](../11-DISTRIBUTION/README.md)

## Evidence boundary

This section documents the macOS product workflow. Historical compiler/runtime evidence for Bible source snapshots remains evidence about those snapshots, not a requirement that Bible itself ship a Mac binary.
