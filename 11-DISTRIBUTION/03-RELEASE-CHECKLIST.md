# Release checklist

A release is the exact artifact that passed these gates. Rebuilding after approval creates a new candidate.

Это reader-product checklist, не обязательные host gates Bible. Filled
[documentation/source lesson versus product release](../13-TEMPLATES/examples/WORKED-EXAMPLE.md)
оставляет runtime claims BLOCKED/NOT_RUN; actual artifact gate references source,
binary/package/loaded identity и retained observations. Для macOS documented
stapling/re-archive transition хранит submitted/final hashes; changed executable
payload требует новой candidate validation, не просто прежнего version label.

## Source and provenance

- [ ] release commit/tag fixed
- [ ] working tree clean
- [ ] product/build/schema/protocol versions correct
- [ ] AE SDK version/build recorded
- [ ] compiler/toolchain versions recorded
- [ ] dependency versions/licenses recorded
- [ ] artifact manifest generated
- [ ] SHA-256 checksums stored
- [ ] rollback artifact retained

## Code quality

- [ ] compiler warnings reviewed
- [ ] no Debug-only dependency in Release
- [ ] no debug backdoor/test endpoint
- [ ] exceptions contained at host ABI boundaries
- [ ] malformed external input fails closed
- [ ] secrets absent from source/package/log defaults

## PiPL / registration

- [ ] PiPL entry point matches exported symbol
- [ ] PiPL architecture declarations match actual binaries
- [ ] PiPL capability flags agree with runtime setup
- [ ] version/category/name metadata correct
- [ ] Windows PiPL resource generated from intended .r source

## Effect correctness

- [ ] 8-bpc
- [ ] 16-bpc
- [ ] 32-bpc if claimed
- [ ] alpha/transparency
- [ ] extreme parameter values
- [ ] animated parameters
- [ ] unusual/odd frame sizes
- [ ] nonzero origins where relevant
- [ ] partial/empty ROI where relevant
- [ ] cancellation
- [ ] save/reopen
- [ ] old project migration
- [ ] corrupted/unsupported persisted state handled safely

## MFR

- [ ] MFR off passes
- [ ] MFR on passes if claimed
- [ ] concurrent-frame stress passes
- [ ] no unsafe mutable global render state
- [ ] sequence/thread-local state ownership reviewed
- [ ] no lock held across unsafe host calls
- [ ] cancellation/error cleanup passes

## GPU

- [ ] CPU path passes
- [ ] every claimed GPU backend passes
- [ ] CPU/GPU output diff within defined tolerance
- [ ] unsupported GPU fallback works
- [ ] GPU setup/setdown lifecycle passes
- [ ] GPU error/cancel path passes
- [ ] large/odd frame stress passes

## AEGP / panels / scripting if shipped

- [ ] command/menu registration lifecycle passes
- [ ] shutdown/death hook passes
- [ ] panel opens after fresh install
- [ ] panel survives host restart/reopen
- [ ] bridge protocol version checked
- [ ] malformed/unknown command rejected
- [ ] stale async response ignored safely
- [ ] ExtendScript failure returns structured error
- [ ] no unbounded evalScript polling
- [ ] CEP/UXP shell version matches native/script component

## macOS build

- [ ] arm64 slice
- [ ] x86_64 slice if claimed
- [ ] every native dependency has required slice
- [ ] unexpected dylib dependency absent
- [ ] Release dSYM archived
- [ ] binary hash recorded

## macOS signing/distribution

- [ ] final nested code signed
- [ ] final plug-in signed with intended Developer ID identity
- [ ] production entitlements reviewed
- [ ] no accidental get-task-allow
- [ ] signature verification passes
- [ ] notarization accepted
- [ ] notary submission/log archived
- [ ] ticket stapled where applicable
- [ ] quarantined clean-machine install/load passes
- [ ] package not modified after signing/notarization

## Windows build

- [ ] x64 build passes
- [ ] ARM64 build passes if claimed
- [ ] every dependency matches target architecture
- [ ] no accidental Debug CRT/development dependency
- [ ] exported/imported symbol review passes
- [ ] PDB archived per architecture
- [ ] binary hash recorded

## Windows signing

- [ ] .aex signed
- [ ] helper DLL/EXE signed
- [ ] SHA-256 file digest explicit
- [ ] RFC3161 timestamp policy applied
- [ ] signature verifies with intended publisher identity
- [ ] installer signed
- [ ] installer signature verifies
- [ ] signed payload not mutated afterward

## Host support matrix

For every cell claimed "tested":

- [ ] exact AE version/build recorded
- [ ] exact OS version recorded
- [ ] CPU architecture recorded
- [ ] install path recorded
- [ ] plug-in discovered by AE
- [ ] core operation executed
- [ ] golden render/project scenario passes
- [ ] restart/reopen passes

## Installer — macOS and Windows

- [ ] fresh install
- [ ] upgrade N-1 -> N
- [ ] uninstall
- [ ] reinstall
- [ ] multiple AE versions
- [ ] no AE installed behavior defined
- [ ] insufficient permission behavior correct
- [ ] AE-running/locked-file behavior correct
- [ ] only product-owned files removed
- [ ] user presets/projects/data preserved by policy
- [ ] installer log contains actionable result
- [ ] rollback/failure does not leave mixed-version payload

## Compatibility

- [ ] support matrix accurate
- [ ] oldest supported project fixture opens
- [ ] persisted sequence/schema migration passes
- [ ] unsupported old schema fails safely
- [ ] panel/native protocol mismatch produces clear recovery
- [ ] removed OS/architecture no longer appears in package/docs

## Security/licensing

- [ ] no network licensing in render hot path
- [ ] offline/server-down behavior tested
- [ ] render farm/headless policy tested
- [ ] helper IPC validates size/version/opcode
- [ ] update artifact signature/hash verified
- [ ] secrets absent from logs
- [ ] privacy/telemetry behavior reviewed

## Release assets

- [ ] changelog
- [ ] known issues
- [ ] support matrix
- [ ] install/uninstall instructions
- [ ] checksums/build manifest
- [ ] symbol archive internal location recorded
- [ ] rollback artifact retained
- [ ] source/license notices included as required

## Stop rule

If a required checkbox has no evidence, either:

1. run the missing validation, or
2. remove/narrow the capability claim.

Do not convert "not tested" into "passed" because documentation or CI site generation is green.
