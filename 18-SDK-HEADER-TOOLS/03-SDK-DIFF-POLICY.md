# SDK diff policy

An SDK upgrade is a compatibility change, not merely a compiler upgrade.

Before changing product calls, compare the native contracts.

## Inputs

Pin:

- old accepted SDK inventory/identity;
- candidate SDK inventory/identity;
- diff tool version;
- target host versions;
- product native API families in use.

Do not diff two directories of unknown provenance.

## Diff classes

### Added suite/table/function

Potential opportunity.

Before use:

- determine first host/runtime availability;
- decide whether minimum supported AE moves;
- or add runtime feature detection/fallback;
- compile against the candidate SDK;
- test absence on the oldest supported host.

Header availability does not imply an older host provides the suite.

### Removed suite/table/function

Potential blocker.

Investigate:

- replacement API;
- supported older suite generation;
- compatibility adapter;
- product feature removal.

Do not keep calling a removed function through an unsafe cast.

### Changed signature

High risk.

Review:

- parameter types;
- pointer constness;
- enum/width;
- time units;
- ownership transfer;
- callback lifetime;
- thread contract;
- return/error semantics.

A one-token type change can represent a major lifetime rule change.

### Struct/table layout changed

Treat as ABI-sensitive.

Do not reinterpret a smaller/older table as a newer table.

If the API provides size/version fields, validate before accessing extended members.

### Macro/version constant changed

Check:

- whether it is compile-only metadata;
- whether host behavior changed;
- release notes;
- sample changes;
- PiPL/capability implications.

Do not assume a version-macro bump is cosmetic.

### Header unchanged

Still run host regression.

AE behavior, loader policy, GPU drivers, OS security and implementation semantics can change without a public C header diff.

## Samples can move independently

Classify sample diffs separately:

- updated API usage;
- project/build-system changes;
- resource/PiPL change;
- platform/signing change;
- utility helper change.

A sample can lag behind a header or intentionally preserve compatibility.

Record the discrepancy instead of silently choosing whichever is convenient.

## Product impact table

For each relevant diff, record:

| Change | Product call site | Risk | Compatibility decision | Test |
|---|---|---|---|---|
| | | | | |

This makes the SDK upgrade reviewable.

## Minimum-host decision

A new API can lead to three valid strategies:

1. raise minimum supported AE;
2. runtime-gate the new capability;
3. keep using the older supported API.

Choose explicitly.

Do not accidentally raise the minimum host by linking documentation/source against a newer suite generation.

## Compiler matrix

Compile at least:

- primary macOS architecture;
- additional macOS architecture if shipped;
- Windows x64;
- Windows ARM64 if shipped.

Each dependency must exist for the same targets.

A candidate SDK is not accepted from one-platform syntax success.

## Host regression

Run the capability matrix affected by the SDK change.

Examples:

- render/pixel changes → golden render;
- MFR flags/sequence changes → concurrency stress;
- GPU suite change → setup/render/setdown + equivalence;
- AEGP stream change → project/keyframe fixtures;
- panel/build change → load/open/restart;
- installer path/signing guidance → clean install.

## Acceptance package

New SDK version is accepted only when the project has:

- candidate inventory;
- diff artifact;
- manual review for high-risk changes;
- updated compile matrix;
- affected host regressions;
- updated support statement;
- recorded unresolved differences.

## Rollback

Keep the previous accepted SDK/toolchain recipe until the candidate baseline is accepted.

Do not make every branch depend on a new SDK before its compatibility work is complete.

## Stop rule

Compiler errors are evidence, not instructions to cast harder.

When the new SDK exposes a changed contract, change the adapter/architecture deliberately or stay on the previous supported API.

See [header-first rules](04-HEADER-FIRST-RULES.md).
