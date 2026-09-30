# Recipe — first native effect

## Goal

Получить минимальный effect, который reliably loads/renders on both platforms before writing product logic.

## Steps

1. Download/use the target After Effects SDK.
2. Copy `Skeleton` sample.
3. Build untouched sample on one platform.
4. Install/copy it to dev MediaCore.
5. Launch AE and apply sample.
6. Repeat on second platform.
7. Rename product identifiers/entry metadata carefully.
8. Build again before touching render algorithm.
9. Create pure internal `RenderCore` function.
10. Map AE pixels → internal view → RenderCore → output.
11. Add golden test outside AE for RenderCore.
12. Add 8/16/32 support as required.
13. Only then SmartFX/MFR/GPU/UI.

## Done means

- both OS load it;
- no warnings/errors at startup;
- project saves/reopens;
- Debugger symbols work;
- release path not yet needed, but dev signing/loading works.
