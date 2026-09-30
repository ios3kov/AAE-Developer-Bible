# macOS developer bible

## Target

Коммерческий native AE plug-in на Mac в 2026 должен по умолчанию рассматриваться как:

- **Universal binary:** arm64 + x86_64, если продукт всё ещё заявляет Intel support;
- собранный в Xcode;
- корректно PiPL-marked для обеих architectures;
- ad-hoc signed в dev workflow на macOS 15+;
- Developer ID signed + notarized для внешнего release;
- проверенный отдельно на Apple Silicon native AE и Intel path, если Intel заявлен.

## Read order

1. `01-XCODE-SETUP.md`
2. `02-UNIVERSAL-BINARY.md`
3. `03-DEBUGGING.md`
4. `04-GPU.md`
5. `05-SIGNING-NOTARIZATION.md`
6. `06-INSTALLATION-PACKAGING.md`
7. `07-CI.md`
