# Bug report template

Filled [illustrative failure](examples/WORKED-EXAMPLE.md) and
[project-reported crash/retry](../22-PROJECT-CASE-STUDIES/ELASTICGRIDFX-PERFORMANCE-SCOPE-2026-10-07.md).
Status, evidence origin and closure decision differ; non-reproduction is not a fix.

## Identity

- Bug ID:
- Title:
- Reporter:
- Date/time:
- Severity:
- Regression: yes / no / unknown
- First affected build:
- Last known good build:

## Summary

One sentence describing the observable failure.

## Product artifact

- Plug-in version:
- Build number:
- Git SHA:
- Binary/package SHA-256:
- Install path:
- Installer version:
- Panel/helper version if applicable:
- Protocol/schema version if relevant:

## Environment

- After Effects version/build:
- Beta/GA:
- OS version/build:
- CPU architecture:
- CPU:
- RAM:
- GPU:
- GPU driver/runtime:
- Project bit depth:
- MFR: on / off
- GPU backend: CPU / backend name
- Render path: preview / render queue / aerender / other

## Preconditions

- Project/fixture:
- Source media:
- Required preferences:
- Required account/license state:
- Fresh launch required: yes / no
- Cache state:
- Other setup:

## Reproduction

1.
2.
3.

Frequency:

- [ ] always
- [ ] often
- [ ] intermittent
- [ ] once

Approximate rate if intermittent:

## Expected

Describe measurable expected behavior.

## Actual

Describe measurable actual behavior.

Do not replace this section with only a screenshot.

## Scope/isolation

Tested:

- [ ] fresh AE launch
- [ ] clean project
- [ ] minimal fixture
- [ ] MFR off
- [ ] MFR on
- [ ] CPU path
- [ ] GPU path
- [ ] another supported AE version
- [ ] another machine
- [ ] known-good previous product build
- [ ] known-good Adobe/sample baseline where relevant

Results:

## Artifacts

Attach or reference:

- project/minimal project:
- source media:
- rendered output:
- expected output:
- pixel diff:
- product log:
- AE log:
- crash report/dump:
- thread dump for hang:
- installer log:
- screenshot/video:
- profiler trace:

## Crash/hang details

If crash:

- exception/signal:
- crashing module:
- top symbolized frames:
- matching dSYM/PDB confirmed: yes / no
- dump/report ID:

If hang:

- timeout threshold:
- thread/process sample:
- last known operation/request ID:

## State/lifetime clues

- occurs after save/reopen:
- occurs after panel reload:
- occurs after cancel:
- occurs only on repeated runs:
- occurs only after cache warmup:
- occurs only after project mutation:
- possible stale request/generation:
- possible resource acquire/release imbalance:

## Regression range

Last known good:

First known bad:

Candidate commits/change area:

## Root cause

Fill only after evidence:

## Fix

- Commit/PR:
- Why the fix addresses the root cause:
- Compatibility/migration impact:

## Verification

Required retest:

- [ ] original reproduction
- [ ] minimal reproduction
- [ ] regression fixture added
- [ ] neighboring edge cases
- [ ] MFR/GPU combination if relevant
- [ ] save/reopen if state-related
- [ ] old project fixture if migration-related
- [ ] clean install if load/installer-related

Evidence/result:

## Closure rule

Close only when the original failure is reproduced or sufficiently characterized, the root cause/fix is recorded, and the relevant regression test passes on the claimed environment.
