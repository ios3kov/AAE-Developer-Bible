# Plug-in specification template

## Product

- name:
- target version:
- owner:
- repository:
- product type/status:

## Problem

What artist/user problem is solved?

What is explicitly out of scope?

## Success criteria

Measurable criteria:

1.
2.
3.

## Extension type

- [ ] Effect
- [ ] AEGP
- [ ] AEIO
- [ ] Artisan
- [ ] Native panel
- [ ] ExtendScript
- [ ] ScriptUI
- [ ] CEP
- [ ] UXP
- [ ] External helper
- [ ] Hybrid

Why is this type required?

Which simpler type was considered and rejected?

## Public support matrix

### After Effects

- minimum supported:
- newest GA tested:
- beta/lab:
- unsupported versions:

### macOS

- minimum OS:
- arm64:
- x86_64:
- GPU requirements:

### Windows

- minimum OS:
- x64:
- ARM64:
- GPU requirements:

Do not write "all versions" without a real matrix.

## SDK / toolchain

- AE SDK exact version/build:
- macOS Xcode/Clang:
- Windows Visual Studio/MSVC:
- C++ standard:
- external SDKs:

## Registration / identity

- plug-in kind:
- entry point:
- PiPL/resource source:
- match name:
- category/display name:
- version fields:

## Render

- 8-bpc:
- 16-bpc:
- 32-bpc:
- alpha behavior:
- SmartFX:
- ROI:
- auxiliary channels:
- MFR:
- GPU backends:
- CPU fallback:
- audio if applicable:

## Render invariants

- coordinate/origin assumptions:
- rowbytes policy:
- color-space assumptions:
- deterministic expectations:
- numerical tolerance:

## State and ownership

### Global

- global_data:
- mutable/immutable:
- setup/setdown owner:

### Instance/sequence

- sequence_data:
- schema version:
- flatten/migration:
- MFR access rules:

### Caches

- cache key:
- owner:
- eviction:
- invalidation:
- thread safety:

### Borrowed host objects

List host-owned references and lifetime limits.

## UI

- standard parameters:
- custom Drawbot:
- ScriptUI:
- panel:
- CEP/UXP:
- accessibility/localization requirements:

## Communication

- panel/script/native topology:
- protocol version:
- request envelope:
- error envelope:
- cancellation:
- stale-response policy:
- large-data/data-plane transport:
- helper IPC/authentication:

## Threading

- callbacks that may be concurrent:
- worker-thread responsibilities:
- host-thread-only operations:
- locks:
- third-party thread-safety assumptions:

## Persistence / project compatibility

- parameter ID policy:
- sequence schema:
- old project fixtures:
- migration rules:
- downgrade expectation:

## Filesystem / network

- paths read/written:
- user data location:
- temp/cache location:
- network endpoints:
- offline behavior:

## Licensing/security

- entitlement model:
- render-farm/headless policy:
- secrets:
- token storage:
- failure states:
- telemetry/privacy:

## Dependencies

| Dependency | Version | License | mac arm64 | mac x86_64 | Win x64 | Win ARM64 |
|---|---|---|---|---|---|---|
| | | | | | | |

## Performance budget

- target frame/resolution:
- cold first-frame budget:
- warm-frame/render budget:
- panel latency:
- memory budget:
- MFR scaling target:
- GPU crossover/target:

## Failure behavior

Define behavior for:

- unsupported GPU;
- allocation failure;
- cancel;
- corrupted persisted state;
- missing native/helper component;
- protocol mismatch;
- network/server down;
- invalid license;
- installer upgrade failure.

## Build/distribution

### macOS

- architectures:
- development signing:
- Developer ID identity:
- notarization:
- installer/package:
- install path policy:
- dSYM retention:

### Windows

- architectures:
- Authenticode:
- installer:
- registry path policy:
- PDB retention:

## Test plan

### Unit/contract

- pure core:
- schema/protocol:
- error handling:

### Render

- golden fixtures:
- BPC:
- alpha/HDR:
- ROI/origins:
- CPU/GPU:

### Concurrency

- MFR:
- cancel:
- stress repetitions:

### Host

- AE matrix:
- save/reopen:
- panel lifecycle:

### Distribution

- fresh install:
- upgrade:
- uninstall:
- clean-machine trust/signing:

## Acceptance evidence

Link/ID for each required capability:

| Capability | Test ID | Required environments | Status |
|---|---|---|---|
| | | | NOT_RUN |

## Release blockers

1.
2.

## Open questions

1.
2.
