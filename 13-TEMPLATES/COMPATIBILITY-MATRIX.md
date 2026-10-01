# Compatibility matrix template

## Product identity

- Product/version:
- Build:
- Git SHA:
- Candidate/package hash:
- Date:
- Owner:

## Status vocabulary

Use only:

- PASS — required scenario executed and evidence retained;
- FAIL — required scenario executed and failed;
- BLOCKED — environment/dependency prevented execution;
- NOT RUN — no evidence;
- UNSUPPORTED — product policy does not support this cell;
- LAB — beta/experimental observation, not production support.

Do not use blank cells as PASS.

## Host/platform matrix

| AE version/build | Release channel | macOS arm64 | macOS x86_64 | Windows x64 | Windows ARM64 | Evidence ID | Notes |
|---|---|---|---|---|---|---|---|
| | GA | | | | | | |
| | GA | | | | | | |
| | Beta | LAB | LAB | LAB | LAB | | beta evidence only |

## Capability matrix

For each supported platform/host cell:

| Capability | CPU | GPU | MFR off | MFR on | Save/reopen | Evidence ID | Notes |
|---|---|---|---|---|---|---|---|
| basic render | | | | | | | |
| 8-bpc | | | | | | | |
| 16-bpc | | | | | | | |
| 32-bpc | | | | | | | |
| alpha | | | | | | | |
| ROI/origin | | | | | | | |
| old project migration | | | | | | | |
| cancel/error path | | | | | | | |

Remove rows not claimed by the product; do not leave them implicitly supported.

## Panel/scripting matrix if shipped

| Scenario | Status | Evidence ID | Notes |
|---|---|---|---|
| panel fresh install/open | | | |
| host bridge handshake | | | |
| command success | | | |
| structured error | | | |
| stale response ignored | | | |
| panel reload | | | |
| AE restart | | | |
| component version mismatch | | | |

## Installer matrix

| Platform | Fresh install | Upgrade N-1 → N | Uninstall | Reinstall | Failure rollback | Evidence ID |
|---|---|---|---|---|---|---|
| macOS | | | | | | |
| Windows x64 | | | | | | |
| Windows ARM64 if claimed | | | | | | |

## Environment record

For every PASS/FAIL evidence record store:

- exact AE version/build;
- exact OS version/build;
- CPU architecture;
- GPU/driver where relevant;
- binary/package hash;
- fixture hash/version;
- test command or manual procedure;
- observed result.

## Release support statement

### Tested

List only matrix cells with PASS evidence:

### Unsupported

### Known limitations

### Not tested / pending

## Stop rule

A public support claim must map to at least one PASS cell for the required scenario. If evidence is missing, either run the test or narrow the claim.
