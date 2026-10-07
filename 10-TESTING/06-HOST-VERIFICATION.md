# Host verification in After Effects

A plug-in is not verified because it compiles, links or passes unit tests. Host verification means the exact built artifact was installed into a named After Effects build and the required behavior was observed.

## Evidence ladder

Use distinct labels:

```text
DOCUMENTED
 -> source/API contract reviewed

COMPILED
 -> compiler accepted the source

LINKED
 -> native binary/resource bundle produced

LOAD-VERIFIED
 -> AE discovered and loaded the exact artifact

BEHAVIOR-VERIFIED
 -> declared scenario produced the expected result

STRESS-VERIFIED
 -> repeated/concurrent/error scenarios passed

RELEASE-VERIFIED
 -> packaged/signed installer artifact passed clean-machine acceptance
```

Never collapse these into one "works" status.

## Test identity

Concrete [expected Gain inputs/outputs](../13-TEMPLATES/examples/gain-evidence-plan.json)
give semantic RGBA values, not raw PF_Pixel byte ordering. Calibrate the actual
export/decode chain (precision, straight/premultiplied alpha, profile) with known
control frames before accepting comparisons; an RGBA16 PNG cannot prove raw float
HDR equality. Record actual selector/backend and complete decoded frame set, not
just the project GPU/MFR option or a successful launcher exit.

Every host result must record:

- Bible/source commit;
- product/example version;
- binary/package SHA-256;
- Adobe SDK version/build;
- AE exact version/build;
- OS exact version;
- architecture;
- CPU/GPU where relevant;
- MFR state;
- test fixture/project identity;
- timestamp;
- observed result.

If the artifact hash is missing, later investigators cannot prove what was actually tested.

## Load verification

Minimum load check:

1. install exact artifact using intended install path;
2. launch AE from a clean state;
3. confirm module appears/loads;
4. confirm no startup error;
5. create/open the intended fixture;
6. invoke the feature once;
7. quit AE cleanly.

For effects, record whether the effect appears in the expected menu/category and whether an instance can be added.

For AEGP/panel tools, record menu/panel registration and command execution.

## Functional verification

Functional tests must check observable output, not just "no crash".

Examples:

### Effect

- parameter defaults;
- parameter change;
- animated values;
- 8/16/32 bpc where claimed;
- alpha;
- odd dimensions;
- ROI/partial render where applicable;
- save/reopen;
- duplicate/copy/paste instance;
- render queue output.

### AEGP

- command registration;
- update/enable state;
- operation on valid project;
- behavior with no project/selection;
- undo behavior;
- shutdown/unload path.

### Script/panel

- panel launch;
- command dispatch;
- malformed request;
- reload;
- stale response;
- project switch;
- AE shutdown/restart.

## Negative verification

A required feature is not accepted until important failure cases are observed.

Test:

- missing input;
- invalid project state;
- unsupported format/depth;
- permission error;
- helper process absent;
- protocol mismatch;
- user cancellation;
- resource exhaustion where safely reproducible.

The expected result should be defined before running the test.

## Save/reopen

Many integration bugs only appear after serialization.

For project-visible state:

```text
create state
 -> save
 -> quit AE
 -> relaunch
 -> reopen
 -> verify state
 -> render/operate again
```

Do not treat an in-session result as persistence verification.

## Repeated runs

At least one scenario should be repeated enough to expose lifetime bugs:

- add/remove effect repeatedly;
- open/close projects;
- render repeatedly;
- enable/disable MFR where applicable;
- panel reload;
- helper restart;
- AE quit/relaunch.

Record iteration count.

## Evidence artifact

Each host run should produce a compact report, for example:

```yaml
artifact_sha256: ...
source_commit: ...
ae_version: ...
os: ...
arch: ...
sdk: ...
fixture: ...
scenario: minimal_gain_16bpc
result: PASS
observed: "Gain 0 produced black with preserved alpha"
attachments:
  - output.png
  - ae-log.txt
```

Screenshots are supporting evidence, not a substitute for exact binary identity and written observations.

## Failure reporting

A failure report should contain:

- first failing step;
- expected behavior;
- actual behavior;
- crash/hang/error text;
- minimal reproducer;
- whether issue reproduces after clean restart;
- whether previous known-good artifact passes.

Do not overwrite a failed result with a later success. Preserve both and link the fix commit.

## Release implication

Only behavior verified against the exact packaged release candidate can be promoted to release evidence.

A developer build copied manually into MediaCore is useful engineering evidence, but it is not installer/release verification.
