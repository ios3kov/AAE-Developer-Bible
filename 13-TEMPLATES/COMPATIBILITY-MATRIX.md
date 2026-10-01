# Compatibility matrix template

## Product artifact

- product version:
- build:
- git SHA:
- binary/package hashes:
- AE SDK:
- protocol/schema versions:

## Status vocabulary

Use:

- PASS — required test executed and passed;
- FAIL — executed and failed;
- BLOCKED — named dependency/environment unavailable;
- NOT_RUN — required but not executed;
- LAB — exploratory/beta observation only.

Do not use a blank cell to mean both unsupported and untested.

## Host/platform matrix

| AE exact version/build | OS exact version | CPU arch | Install/load | CPU render | GPU backend | MFR | Save/reopen | Installer | Status/evidence |
|---|---|---|---|---|---|---|---|---|---|
| | macOS | arm64 | | | | | | | |
| | macOS | x86_64 | | | | | | | |
| | Windows | x64 | | | | | | | |
| | Windows | ARM64 | | | | | | | |

Add rows for every claimed AE/OS combination.

## Bit depth matrix

| Environment ID | 8-bpc | 16-bpc | 32-bpc | Alpha | HDR | Evidence |
|---|---|---|---|---|---|---|
| | | | | | | |

## Feature matrix

| Environment ID | SmartFX ROI | MFR | CPU fallback | GPU | CEP/UXP panel | AEGP | Notes |
|---|---|---|---|---|---|---|---|
| | | | | | | | |

## Installer matrix

| Platform | Fresh | N-1 -> N | Uninstall | Reinstall | AE running | No AE | Evidence |
|---|---|---|---|---|---|---|---|
| macOS | | | | | | | |
| Windows x64 | | | | | | | |
| Windows ARM64 | | | | | | | |

## Project migration

| Fixture | Created with product | Created with AE | Open | Render | Save/reopen | Evidence |
|---|---|---|---|---|---|---|
| legacy-1 | | | | | | |

## Beta

Beta rows are LAB until the corresponding GA environment is tested.

Example:

| AE exact version/build | OS | Arch | Status |
|---|---|---|---|
| 27.x Beta | | | LAB |

Never turn a beta-only observation into a production support claim.

## Unsupported combinations

List explicitly:

- combination:
- reason:
- behavior expected from installer/plug-in:
- user-facing message/documentation:

## Release conclusion

Supported matrix for this exact artifact:

Unsupported:

Blocked/not run:

Evidence root/location:
