# Test evidence and acceptance records

Tests that leave no durable evidence are hard to trust later. This chapter defines the record format used to decide whether a capability may be called verified.

## Directory model

A project may keep reports outside the public Bible repository when they contain proprietary SDK/build material, but the structure should be stable:

```text
evidence/
  <product>/
    <version>/
      <platform>-<arch>/
        manifest.json
        host-report.md
        logs/
        outputs/
        screenshots/
```

The Bible can reference hashes and conclusions without redistributing proprietary binaries or Adobe SDK files.

## Manifest

Filled [machine-readable plan](../13-TEMPLATES/examples/gain-evidence-plan.json)
and [human-readable pack](../13-TEMPLATES/examples/WORKED-EXAMPLE.md) distinguish
expected values from null observations. For actual raw-record references see the
[project-reported JSON hashes](../22-PROJECT-CASE-STUDIES/ELASTICGRIDFX-PERFORMANCE-SCOPE-2026-10-07.md).
Those records identify private raw evidence without pretending it is publicly
reproducible. Keep evidence origin, test status and acceptance decision separate.

Recommended fields:

```json
{
  "schema": 1,
  "product": "MinimalGain",
  "version": "1.0.0-test",
  "sourceCommit": "...",
  "artifactSha256": "...",
  "sdk": "25.6 build 61",
  "ae": "25.6 ...",
  "os": "...",
  "arch": "arm64",
  "compiler": "...",
  "mfr": false,
  "gpuBackend": null
}
```

## Scenario record

Each scenario has:

- ID;
- requirement;
- setup;
- steps;
- expected result;
- observed result;
- PASS/FAIL/BLOCKED;
- attachments;
- notes/limits.

Use `BLOCKED` when the test cannot actually be run. Do not convert missing infrastructure into PASS.

## Status semantics

### PASS

The named scenario ran on the named artifact/environment and matched the acceptance criterion.

### FAIL

The scenario ran and did not meet the criterion.

### BLOCKED

The scenario is required but could not run because of missing platform, SDK, AE version, hardware or other prerequisite.

### NOT RUN

No execution was attempted.

### NOT APPLICABLE

The scenario genuinely does not apply to the product. State why.

## Evidence immutability

After a release decision, preserve the evidence bundle.

If a test is rerun:

- create a new record;
- do not edit history to make old failures disappear;
- link the superseding run.

## Golden outputs

For deterministic visual tests, retain:

- source fixture;
- output image/frame sequence;
- comparison script/tool version;
- tolerance;
- diff image or numerical metrics.

A golden image without the generation conditions is insufficient.

## Logs

Capture only useful diagnostics:

- module version/path;
- host version;
- error/crash details;
- render timing if relevant;
- helper/service diagnostics.

Avoid collecting unrelated user information.

## Automated versus manual

Automation is preferred for repeatable checks, but some AE interactions may remain manual.

Manual evidence is acceptable when it records:

- exact artifact;
- exact environment;
- explicit steps;
- observed result;
- reviewer/operator.

"Opened it and it looked fine" is not an acceptance record.

## Promotion rule

A capability table may be upgraded only when the evidence level matches the claim.

Examples:

```text
compiler-only evidence
  != host verified

one successful 8-bpc render
  != 8/16/32 verified

macOS arm64 pass
  != Windows x64 pass

developer build pass
  != installer/release candidate pass
```

## Review

Before release, a second pass should verify:

- artifact hash matches the candidate;
- environment metadata is complete;
- scenario requirement matches the claim;
- attachments/logs belong to the run;
- failures/blockers are not hidden by summary wording.
