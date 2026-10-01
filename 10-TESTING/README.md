# Testing strategy

An After Effects plug-in is not tested by saying "AE opened and the effect looked fine".

Testing must prove each public capability at the layer where that capability can actually fail.

## Evidence ladder

~~~text
pure unit test
→ adapter/contract test
→ native compile/link
→ package/install
→ AE host load
→ operation/render
→ stress/error/cancel
→ cross-version/platform matrix
~~~

A higher-level PASS does not erase a lower-level failure, and a lower-level PASS does not imply the higher level.

Examples:

- compiler success does not prove PiPL loading;
- AE loading does not prove correct pixels;
- one correct frame does not prove MFR safety;
- a signed installer does not prove upgrade/uninstall safety.

## Test layers

1. **Pure core unit tests** — algorithms/data logic without AE.
2. **Adapter tests** — conversion between SDK/host types and internal model.
3. **Contract tests** — protocol/schema/ownership validation.
4. **Native build tests** — compile, resources, link, architecture.
5. **Golden render tests** — known inputs -> measurable outputs.
6. **Host integration tests** — actual After Effects.
7. **Concurrency/stress** — MFR, repeated render, cancel, cache churn.
8. **Cross-version matrix** — every claimed AE family.
9. **Platform/architecture matrix**.
10. **Performance regression**.
11. **Installer/upgrade/uninstall**.
12. **Crash/recovery and diagnostics**.

## Capability -> evidence rule

Every capability claim must point to matching evidence:

| Claim | Minimum evidence |
|---|---|
| 8/16/32-bpc | host render fixtures at each claimed depth |
| SmartFX ROI | partial/empty ROI host tests |
| MFR supported | concurrent-frame stress |
| GPU supported | backend host run + CPU/GPU comparison + fallback |
| Apple Silicon | arm64 native host load/operation |
| Intel macOS | x86_64 host load if still claimed |
| Windows x64 | real Windows x64 build + AE host load |
| Windows ARM64 | native ARM64 host/build matrix |
| CEP panel | install/open/bridge/error/restart tests |
| installer safe | fresh/upgrade/failure/uninstall evidence |
| old projects supported | migration fixtures and save/reopen |

If the evidence does not exist, narrow the claim.

## Determinism before automation

Before writing a test harness, define what PASS means.

For a render test specify:

- input project/assets;
- frame/time;
- output format/color settings;
- expected pixel metric;
- tolerance;
- platform/AE scope.

For an installer test specify:

- initial machine state;
- old version if upgrade;
- expected files/registry/receipts;
- expected failure rollback;
- final machine state.

Automation without a deterministic assertion is only scripted activity.

## Preserve artifacts

A useful failed test keeps enough evidence to investigate:

- exact binary/package hash;
- AE/OS/toolchain versions;
- project/fixture version;
- stdout/stderr/log;
- render output/diff;
- crash dump/report;
- installer log;
- command and exit code.

Do not delete the only failing render because the CI workspace ended.

## Separate product and host failures

Always keep one minimal Adobe/sample baseline or known-good host check available.

When a failure appears, ask:

~~~text
same AE/OS
+ untouched/known-good sample
+ equivalent host action
~~~

If the host/sample also fails, that changes the investigation path. It does not automatically prove an Adobe bug, but it prevents wasting time inside unrelated product code.

## Release principle

No release capability is accepted without a named test and evidence record.

See:

- 01-TEST-MATRIX.md
- 02-RENDER-CORRECTNESS.md
- 03-MFR-STRESS.md
- 04-PERFORMANCE.md
- 05-CRASH-DIAGNOSTICS.md
- 06-EVIDENCE-AND-ACCEPTANCE.md
