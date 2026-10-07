# Evidence and acceptance

This chapter defines what a PASS means in the Bible.

## Evidence unit

A test result is only useful when it identifies:

- requirement/capability;
- artifact under test;
- environment;
- procedure/command;
- expected result;
- observed result;
- terminal status;
- retained evidence.

Template:

~~~yaml
id: MFR-001
capability: multi-frame rendering
artifact:
  version: 1.2.3
  git_sha: ...
  sha256: ...
environment:
  ae: ...
  os: ...
  arch: ...
procedure:
  fixture: mfr-stress.aep
  command: ...
expected:
  - deterministic output
  - no crash/deadlock
observed:
  - ...
status: PASS
evidence:
  - render hash/report
  - log
~~~

## Status vocabulary

The [filled lesson plan](../13-TEMPLATES/examples/gain-evidence-plan.json) remains
NOT_RUN even though unrelated portable tests and historical syntax checks pass.
Its [illustrative failed frame-set example](../13-TEMPLATES/examples/WORKED-EXAMPLE.md)
is a teaching scenario, not observed Gain behavior. BLOCKED requires a named missing
prerequisite; NOT_RUN must not automatically be rewritten BLOCKED for a greener table.

Use a small vocabulary:

- NOT_RUN — required test exists but was not executed;
- BLOCKED — cannot execute because a named dependency/environment is unavailable;
- FAIL — executed and acceptance criterion failed;
- PASS — executed and criterion passed;
- OBSERVED — exploratory observation without complete acceptance assertion.

Do not use "probably", "seems fine" or "green" as a release status.

## Documentation review is separate

A chapter can be source-reviewed while implementation acceptance remains NOT_RUN.

Likewise a compiler can accept a sample while host load remains NOT_RUN.

Keep separate dimensions:

~~~text
documentation/source evidence
implementation state
compiler/build evidence
host behavior evidence
release/package evidence
~~~

This prevents a documentation CI job from accidentally becoming "plug-in tested".

## Artifact identity

Every PASS belongs to one exact artifact.

If the binary changes, even from the same git commit:

- assign a new hash;
- do not reuse the old PASS automatically.

If packaging changes but the inner binary does not, installer/package acceptance still needs the new package artifact identity.

## Environment identity

At minimum:

- AE exact version/build;
- OS exact version/build where relevant;
- CPU architecture;
- GPU/backend/driver for GPU tests;
- MFR setting;
- SDK/toolchain for build evidence.

"Latest AE" is not a reproducible environment name.

## Expected result first

Write expected result before running the candidate when practical.

Bad:

> Rendered image looked close enough.

Good:

> Max absolute RGB error <= 1/32768 and alpha exact for fixture X.

Predeclared thresholds reduce biased acceptance.

## Negative tests

Acceptance includes failure behavior.

Examples:

- missing dependency;
- unsupported architecture;
- malformed sequence data;
- invalid panel command;
- allocation failure where injectable;
- cancellation;
- notarization/signature failure;
- locked file during upgrade.

A product that only works when nothing goes wrong is not release-ready.

## Evidence storage

Keep machine-readable result plus human-readable summary.

Suggested:

~~~text
evidence/
└── 1.2.3/
    ├── manifest.json
    ├── mac-arm64-ae26/
    │   ├── results.json
    │   ├── logs/
    │   └── renders/
    └── win-x64-ae26/
        └── ...
~~~

Do not commit proprietary/customer content to a public repository. Store references/hashes in the public report when raw evidence must stay private.

## Manual tests

Manual tests are valid evidence if they are reproducible and recorded.

A manual result should include:

- exact steps;
- tester/date;
- artifact hash;
- environment;
- observed outcome;
- screenshot/video only as supporting evidence, not the sole assertion when pixels/data can be measured.

## Flaky tests

A flaky test is not a PASS.

Classify:

- product nondeterminism;
- host/environment instability;
- harness defect.

Until resolved, affected capability remains blocked or failed according to the release policy.

## Acceptance gate

A capability is accepted only when:

1. implementation exists;
2. required build/package succeeds;
3. named test set passes;
4. no blocker from a higher-risk lane remains;
5. documentation support claim matches tested scope.

## Evidence invalidation

Re-run when:

- source affecting feature changes;
- compiler/toolchain materially changes;
- SDK changes;
- AE major/minor support changes;
- OS architecture changes;
- installer/signing payload changes;
- GPU backend/critical dependency changes.

Use risk judgment for unrelated documentation-only edits, but never transfer a PASS to a different binary by convenience.

## Bible rule

When this repository says host-verified, the corresponding record must name the actual host run.

When it says source-reviewed, that must not be read as host-verified.
