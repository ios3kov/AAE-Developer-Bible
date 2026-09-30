# Test matrix

## Minimal matrix

| Axis | Values |
|---|---|
| AE | every claimed major/minor family |
| OS | minimum supported + current stable |
| CPU | mac arm64, mac x86_64 if claimed, Win x64, Win ARM64 if claimed |
| BPC | 8 / 16 / 32 |
| MFR | off / on |
| GPU | off / each supported backend |
| Resolution | tiny / HD / 4K / stress |
| Project | new / migrated old project |

Полный Cartesian product может быть дорогим. Делить на:
- PR smoke matrix;
- nightly expanded matrix;
- pre-release full matrix.

## Required project fixtures

### `basic.aep`
- one layer;
- one effect;
- defaults.

### `animated-extremes.aep`
- every param animated;
- min/max/odd values;
- time remap / random seeks.

### `stacked.aep`
- multiple instances;
- masks/transforms/precomps;
- other common effects around yours.

### `mfr-stress.aep`
- long duration;
- multiple comps/layers/instances;
- concurrent render pressure.

### `color-depth.aep`
- 8/16/32-bpc variants;
- HDR and transparency fixtures.

### `legacy-project.aep`
- saved by previous shipped plug-in version.
