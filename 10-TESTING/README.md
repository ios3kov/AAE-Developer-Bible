# Testing strategy

AE plug-in нельзя тестировать одной фразой «открыл AE, эффект работает».

## Layers

1. **Pure core unit tests** — math/data logic без AE.
2. **Adapter tests** — conversion between SDK types and internal model.
3. **Golden render tests** — known inputs → known outputs.
4. **Host integration tests** — actual AE.
5. **Cross-version matrix** — каждый supported AE.
6. **Platform/architecture matrix**.
7. **Performance regression**.
8. **Installer/upgrade/uninstall**.
9. **Crash/recovery**.

## Release principle

Каждая заявленная capability должна иметь проверку:
- MFR supported → test MFR concurrency;
- GPU supported → CPU/GPU equivalence + fallback;
- 32 bpc supported → float fixtures;
- Apple Silicon supported → arm64 real host test;
- Windows ARM64 supported → real/native host test.
