# Windows developer bible

## Target

Коммерческий native AE plug-in на Windows в 2026:

- Visual Studio project based on Adobe SDK sample;
- x64 как основной shipping target;
- ARM64 target добавлять там, где target Adobe hosts работают native и продукт заявляет поддержку;
- PiPL resource build step сохранён;
- symbols/PDB архивируются;
- release binaries Authenticode-signed;
- installer использует корректный Adobe plug-in path policy/registry.

## Read order

1. `01-VISUAL-STUDIO-SETUP.md`
2. `02-X64-ARM64.md`
3. `03-DEBUGGING.md`
4. `04-GPU.md`
5. `05-CODE-SIGNING.md`
6. `06-INSTALLATION-PACKAGING.md`
7. `07-CI.md`
8. `08-NATIVE-SDK-VALIDATION.md`
9. `09-PRODUCTION-BUILD-PIPELINE.md`
