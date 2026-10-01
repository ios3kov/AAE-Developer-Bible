# Test matrix

A full Cartesian product of every AE version, OS, CPU, color depth, GPU and scenario can be too expensive. The answer is not to test one happy path; it is to define risk-based lanes.

## Axes

| Axis | Values |
|---|---|
| AE | every claimed major/minor family |
| OS | minimum supported + current stable + important transition versions |
| CPU | mac arm64, mac x86_64 if claimed, Win x64, Win ARM64 if claimed |
| BPC | 8 / 16 / 32 as claimed |
| MFR | off / on |
| GPU | CPU fallback / each claimed backend |
| Resolution | tiny / odd / HD / 4K / stress |
| Project | new / migrated old / malformed persistence |
| Render mode | UI preview / render queue / aerender if supported |
| Install | fresh / upgrade / uninstall / repair where applicable |

## Test lanes

### PR smoke

Fast failures:

- pure unit tests;
- protocol/schema tests;
- native syntax/build for primary dev architecture where available;
- one small golden CPU fixture;
- generated docs/resources validation.

Goal: reject obvious regressions quickly.

### Nightly / continuous integration

Broader:

- multiple render fixtures;
- MFR stress loop;
- GPU comparison on equipped runner;
- memory trend;
- installer smoke in VM;
- current GA AE host cycle where automation exists.

Goal: find concurrency/environment regressions before release week.

### Pre-release matrix

Every public support claim:

- all supported AE versions/families;
- all claimed OS/CPU targets;
- all claimed BPC modes;
- MFR/GPU combinations;
- old project migration;
- installer fresh/upgrade/uninstall;
- clean-machine signing/trust path.

This lane produces release evidence.

## Pairwise/risk reduction

When full Cartesian coverage is impossible:

1. identify high-risk interactions;
2. use pairwise coverage for lower-risk dimensions;
3. always run explicitly dangerous combinations.

Never omit:

- MFR + mutable instance state;
- GPU + 32-bpc if both claimed;
- oldest project schema + newest plug-in;
- installer upgrade across a filename/path change;
- each CPU architecture actually shipped.

Document what was not combined.

## Required project fixtures

### basic.aep

- one layer;
- one effect;
- defaults;
- deterministic source.

Purpose: loading/default/basic render.

### animated-extremes.aep

- every important parameter animated;
- min/max/boundary values;
- abrupt interpolation where relevant;
- random seeks.

Purpose: time and parameter handling.

### stacked.aep

- multiple instances;
- masks/transforms/precomps;
- common effects before/after;
- multiple layer sizes.

Purpose: composition interaction/state separation.

### mfr-stress.aep

- long duration;
- multiple comps/layers/instances;
- different parameter values;
- enough work for concurrent frames.

Purpose: race/state bleed/deadlock.

### color-depth.aep

- 8/16/32-bpc variants;
- transparency;
- HDR/negative float values where valid;
- gradients and edge colors.

Purpose: pixel format correctness.

### roi-origins.aep

- odd sizes;
- cropped/precomp offsets;
- nonzero origins;
- partial regions.

Purpose: SmartFX/rowbytes/coordinate bugs.

### legacy-project-N.aep

One fixture per materially different persisted schema.

Purpose: project migration.

### malformed-state fixtures

Only if product owns serialized data:

- truncated header;
- unknown version;
- impossible length/count;
- corrupt checksum if used.

Purpose: fail safely.

## Fixture immutability

Release fixtures should be versioned and not silently re-saved by the newest AE before the migration test.

Store:

- creation AE version;
- product version;
- fixture purpose;
- expected output/hash/metric.

## Environment identity

Each matrix result records:

~~~json
{
  "ae": "...",
  "os": "...",
  "cpu": "...",
  "gpu": "...",
  "driver": "...",
  "plugin_hash": "...",
  "fixture": "...",
  "result": "PASS"
}
~~~

Without environment identity, a green cell is hard to reproduce.

## Stop rule

If a support-matrix cell is claimed but never exercised by any planned lane, either add evidence or remove the claim.
