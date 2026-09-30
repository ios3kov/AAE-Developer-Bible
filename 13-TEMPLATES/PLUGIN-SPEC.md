# Plug-in specification template

## Product

- Name:
- Version target:
- Owner:
- Repository:

## Problem

What artist/user problem is solved?

## Extension type

- [ ] Effect
- [ ] AEGP
- [ ] AEIO
- [ ] Artisan
- [ ] ExtendScript
- [ ] CEP
- [ ] UXP
- [ ] Hybrid

Why this type?

## Support matrix

### After Effects
- Minimum:
- Maximum tested:

### macOS
- Minimum OS:
- arm64: yes/no
- x86_64: yes/no

### Windows
- x64: yes/no
- ARM64: yes/no

## Render

- 8 bpc:
- 16 bpc:
- 32 bpc:
- SmartFX:
- MFR:
- GPU backends:
- CPU fallback:

## State

- global_data:
- sequence_data:
- serialization version:
- caches:

## UI

- standard params:
- custom Drawbot:
- panel:

## Performance budget

- target frame/resolution:
- target latency/render time:
- memory budget:

## Failure behavior

- unsupported GPU:
- missing license/network:
- corrupt project state:

## Test plan

- unit:
- golden render:
- MFR:
- GPU:
- cross-version:
- installer:
