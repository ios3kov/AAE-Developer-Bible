# Reuse audit — FSTR Line and AE Hot Loader — 2026-10-01

This is the code-level follow-up to the initial case-study extraction in [README.md](README.md).

The purpose is narrow: identify reusable engineering patterns before Gates 5–6 create or expand reference examples. It does **not** promote either source product to a Bible host-verified reference.

## Audit baseline

| Project | Reviewed tree | Role of this tree |
|---|---|---|
| FSTR Line | `c69e3663de59dc44cbdef18042891f6dd1ce5ee6` | documentation/source snapshot; individual implementation files map to earlier commits below |
| AE Hot Loader | `cf338bcd861504d695c3181767c18bb423575814` | documentation/source snapshot after PoC success summary |

No source code from either project is copied into the Bible by this audit. Decisions below are about patterns and future adaptations.

## Evidence vocabulary

- **source mapped** — exact file and latest commit at or before the reviewed snapshot identified;
- **project-reported test** — source repository contains a test record with a result, but Bible did not independently repeat it;
- **retained CI** — GitHub still exposes the original workflow run and step outcomes;
- **host reported** — source project records a real AE observation;
- **Bible host verified** — requires a separate Bible acceptance record; none is created here.

---

# FSTR Line

## FL-01 — UI / Core / Host Adapter separation and normalized snapshots

### Source mapping

| File | Source commit |
|---|---|
| `src/core/types.ts` | `ecae7407485d1792ff085382fdc61a116d42f005` |
| `src/host/host-adapter.ts` | `ecae7407485d1792ff085382fdc61a116d42f005` |
| `src/host/fake-host-adapter.ts` | `ecae7407485d1792ff085382fdc61a116d42f005` |
| `src/core/commands.ts` | `3c1ab580d51ae982ff886095dd56649968ef8819` |

The snapshot contract contains:

- explicit `schemaVersion`;
- composition identity;
- rational frame rate;
- stable layer IDs/indexes;
- layer capability flags;
- opaque revision string.

Commands contain:

- `commandVersion`;
- `operationId`;
- composition ID + revision guard;
- semantic operation payload.

The core validates snapshots and commands before the Host Adapter touches After Effects.

### Test evidence

`docs/TEST_RECORDS/CORE-2026-09-28.md` was introduced with the same pure-core implementation commit `ecae7407...` and records:

- TypeScript build PASS;
- 13 pure core tests PASS;
- FakeHostAdapter stale-command behavior PASS;
- AE/CEP integration BLOCKED / not run.

The historical run is project-reported evidence. No retained GitHub Actions run is available for the reviewed FSTR commits.

### Transfer decision

**ADAPT.**

Transfer the architecture, not the product-specific timeline model:

```text
host state
 -> normalized immutable snapshot
 -> pure command builder/validator
 -> Host Adapter
 -> fresh snapshot
```

Do not copy FSTR's layer schema wholesale into generic Bible examples.

### Bible destinations

- `07-PANELS/`
- `15-COMMUNICATION/`
- `10-TESTING/`

### Bible-side acceptance required

- pure snapshot validation tests;
- stale revision rejection;
- wrong composition rejection;
- adapter-independent command tests;
- separate AE host test proving the chosen host identity/revision source is meaningful.

---

# FL-02 — stale-command rejection, refresh coalescing and invalidation

## Source mapping

| File | Source commit |
|---|---|
| `src/core/commands.ts` | `3c1ab580d51ae982ff886095dd56649968ef8819` |
| `src/cep/panel-controller.ts` | `3c6a6297b9b4f1b74b9c6b876b53335bc2d2207d` |
| `src/cep/auto-refresh.ts` | `b1a7f7995f537a6f3d028bc16ca6d5ec2de3da83` |
| `tests/commands.test.ts` | `3c1ab580d51ae982ff886095dd56649968ef8819` |
| `tests/panel-controller.test.ts` | `c9c0d24714583c17bb98cb9f1f1021665b76f848` |
| `tests/auto-refresh.test.ts` | `b1a7f7995f537a6f3d028bc16ca6d5ec2de3da83` |

Important implementation patterns:

- concurrent `refresh()` calls share one in-flight promise;
- generation invalidation prevents an old response from restoring obsolete state;
- previous valid projection can remain visible while a refresh fails;
- auto-refresh schedules the next read only after the previous one finishes;
- hidden/disposed/suspended panels stop scheduling;
- retry/discovery work is bounded.

### Test evidence

`CEP-AUTO-SYNC-2026-09-28.md` identifies build `fstr-cep-b1a7f7995f53`, clean source `b1a7f799...`, client and host SHA-256 values, and reports 45 local tests/build/static checks PASS.

The same record explicitly marks native AE edit → automatic panel update as **NOT RUN** for that candidate.

### Transfer decision

**ADAPT.**

These are broadly useful panel-state patterns. Keep the distinction between:

- request coalescing;
- response invalidation;
- periodic polling;
- actual host event notifications.

Do not rename polling/discovery as event-driven sync.

### Bible-side acceptance required

Portable tests:

- two simultaneous refresh requests cause one host read;
- invalidation discards in-flight result;
- stale response does not overwrite newer state;
- refresh error preserves last good projection when product policy wants that;
- disposal stops future scheduling;
- command calls are not automatically replayed after ambiguous transport failure.

Host tests:

- panel reload;
- project/comp switch;
- host edit during outstanding read;
- visibility lifecycle;
- measured cost on large comps if polling is enabled.

---

# FL-03 — FakeHostAdapter and controlled fixtures

## Source mapping

| File | Source commit |
|---|---|
| `src/host/fake-host-adapter.ts` | `ecae7407485d1792ff085382fdc61a116d42f005` |
| `tests/fake-host-adapter.test.ts` | `ecae7407485d1792ff085382fdc61a116d42f005` |
| `tests/fixtures.ts` | reviewed in the pinned tree; product-specific fixture definitions |

The fake validates the same command guard as the real adapter contract, mutates an in-memory snapshot and advances revision identity.

### Transfer decision

**ADAPT.**

The reusable idea is a contract-compatible fake, not a fake that bypasses validation.

A Bible example should use the same command/snapshot types in fake and real adapters so portable tests catch stale/wrong-target logic before AE is involved.

### Boundary

FakeHostAdapter success is **not** evidence that After Effects performs the same mutation, undo behavior or identity invalidation.

---

# FL-04 — command-hook probe and ABI correction

## Source mapping and build identity

| Evidence | Identity |
|---|---|
| `native/command-probe/CommandProbe.cpp` | source commit `f8de508293893cc68c181b59de5686388e83c538` |
| build record | `docs/TEST_RECORDS/COMMAND-PROBE-BUILD-2026-09-28.md` |
| corrected build | `20260928T184359Z-cf383a8-72414` |
| runtime | `runtime-20260928T184627Z` |
| target | AE `25.6.0.101`, macOS arm64 |

The build record preserves an invalid earlier attempt: a seven-argument entry point copied from an outdated sample caused `5027:47 Plugin ID is invalid`. The corrected probe uses the current five-argument `AEGP_PluginInitFunc` shape with a compile-time ABI assertion.

Runtime evidence for the corrected build:

- probe loaded;
- an ExtendScript-created/modified composition and layer produced no appended command callback;
- native drag/trim, add/delete/reorder, Undo/Redo, other-plugin mutation and multiple other scenarios remained NOT RUN.

### Transfer decision

**DO NOT TRANSFER AS A NOTIFICATION SOLUTION.**

Transfer only two lessons:

1. compile-time callback-signature checks are useful when old SDK samples disagree with current headers;
2. a negative probe result is scoped to its exact operation matrix.

The probe does not prove absence of all AE notification mechanisms. SYNC-001 remains a source-project limitation, not a universal AE conclusion.

---

# AE Hot Loader

## HL-01 — ScriptUI request/response protocol and AEGP Agent boundary

### Source mapping

| File | Source commit |
|---|---|
| `docs/BRIDGE_PROTOCOL.md` | `c7950f549cabf0a13daaf6bf76228340cd4cd3af` |
| `ui/AE Hot Loader.jsx` | `ffd2831493d0919d1db49bc992ff155cab362a81` |
| `agent/src/lib.rs` | `0d071d62552eef8287e3cfb7d89ed164e4034cbd` |
| `.github/workflows/mac-ci.yml` | `ab0363e9d3383d2f3c5448877f07937669577fac` |

Protocol properties:

- version field;
- request ID;
- UI publishes through a temporary request file and rename;
- Agent consumes requests from an AEGP idle hook;
- response carries the same request ID;
- UI ignores responses for another request;
- UI has an 8-second timeout.

### Retained CI

GitHub still exposes successful macOS PoC runs:

- run `36309949069` for commit `0d071d62552e...`;
- run `36337979733` for later production-plan state `9a8b6dee341a...`.

The successful workflow steps include:

- static checks;
- Rust effect core build;
- AEGP Agent build;
- C++ wrapper build;
- bundle assembly;
- ad-hoc signing/verification;
- ScriptUI presence validation;
- test-kit packaging.

An earlier run `36308472947` failed at **Static checks** and skipped subsequent build/package steps. The audit preserves that failure rather than describing the entire development line as continuously green.

### Transfer decision

**ADAPT PRINCIPLES; DO NOT COPY THE FILE PROTOCOL AS A GENERIC PRODUCTION BUS.**

Useful patterns:

- version;
- request correlation;
- single owner of AE native calls;
- publish-complete-then-consume behavior;
- main-thread/idle-hook boundary.

Limitations in this PoC:

- key/value text is product-specific;
- only one UI request is effectively active because the button is disabled;
- request/response files have no general multi-process lock/queue model;
- response replacement removes the previous response before rename;
- polling with `scheduleTask` is a ScriptUI design choice, not a universal bridge.

The Bible's JSON dispatcher and versioned IPC guidance remain the general pattern.

---

# HL-02 — loaded-module lookup and diagnostic experiments

## Source mapping

| File | Source commit |
|---|---|
| `agent/src/lib.rs` | `0d071d62552eef8287e3cfb7d89ed164e4034cbd` |
| `wrapper/AEHotLoader.cpp` | `423835faaf71684ba9b80bd84d87f1f25a9711cf` |
| `experiments/loader_trace/README.md` | `d988407da8fd873bb8f5dcfbce7e5adae233705e` |

The Agent first tries process-wide symbol resolution, then enumerates dyld images to find the already-loaded bridge image instead of assuming one hard-coded installation path.

The wrapper preserves the failed late-registration-callback research path. The production plan records:

- startup registration success;
- saved late callback returning non-success `1`;
- AEGP-from-effect startup attempt `-1102`;
- hard-coded bridge lookup failure that motivated loaded-image discovery.

### Transfer decision

**ADAPT DIAGNOSTIC LESSONS ONLY.**

Useful general debugging lesson:

```text
identify the module actually loaded by the process
 -> record real path/image identity
 -> resolve/inspect that module
 -> do not infer loaded path from installer intent
```

Do not transfer macOS dyld enumeration as a cross-platform SDK contract, and do not use it to bypass normal public API ownership/lifetime rules.

---

# HL-03 — private `ML::LoadPlugins` late-load experiment

## Evidence mapping

The source project records a live AE 25.6.0 ARM64 experiment on branch `experiment/internal-loader-probe`.

The production-plan conclusion was committed as:

- `9a8b6dee341a516a64581036ec910158cba20554` — “docs: mark Stop Criterion A passed”.

Project-reported host observations:

- internal `ML::LoadPlugins` path invoked after startup;
- test bundle loaded;
- two test effects registered;
- both appeared in Effects & Presets;
- both applied;
- RAM Preview and normal render succeeded;
- AE remained stable;
- no AE restart during the late-load test.

The effects were pass-through diagnostics.

### Acceptance boundary

This does **not** establish:

- unloading an already-loaded plug-in;
- replacing code for existing instances;
- arbitrary third-party compatibility;
- MFR/GPU/custom-UI safety;
- version portability;
- Windows behavior;
- a supported Adobe SDK contract.

The implementation path is private and version-sensitive.

### Transfer decision

**DO NOT TRANSFER INTO SUPPORTED SDK RECIPES OR SAFE INSTALLER CODE. KEEP RESEARCH-ONLY.**

It may be cited in case studies about loader research and experimental feasibility, with the exact AE/version boundary.

---

# Installer/provenance audit

## FSTR Line

`THIRD_PARTY_NOTICES.md` identifies Adobe CEP `CSInterface.js` 12.0.0 and preserves the Adobe notice.

**Decision:** do not copy that third-party file into Bible templates. Bible documentation may require developers to obtain the appropriate Adobe CEP resource for their target runtime.

## AE Hot Loader

Rust crates declare `MIT OR Apache-2.0` for the local packages and pin the external `virtualritz/after-effects` dependency revision `83dcc937...`.

**Decision:** no Rust source/dependency is copied into Bible by this audit. If a future example adopts that ecosystem, dependency licensing and version pinning need their own provenance record.

## Unsafe installer pattern

The reviewed `INSTALL.command`:

- executes `rm -rf` on existing installed native modules before copying replacements;
- removes quarantine attributes with `xattr -dr`;
- has no backup/rollback transaction.

**Decision: DO NOT TRANSFER.**

This conflicts with Bible Gate 2. The Bible safe tooling requires staging, backup, rollback and fail-closed behavior.

---

# Candidate decision register

| ID | Decision | Why |
|---|---|---|
| FL-01 | **ADAPT** | clean separation of pure model/commands from AE adapter; portable testable contract |
| FL-02 | **ADAPT** | coalescing + generation invalidation + bounded scheduling are broadly reusable |
| FL-03 | **ADAPT** | contract-compatible fake is valuable for portable tests |
| FL-04 | **EVIDENCE ONLY** | scoped negative hook result; not a supported notification mechanism |
| HL-01 | **ADAPT PRINCIPLES** | correlation/version/main-thread ownership useful; file bus remains PoC-specific |
| HL-02 | **ADAPT DIAGNOSTIC LESSON** | loaded-image identity is useful debugging practice; dyld path is platform/private detail |
| HL-03 | **RESEARCH ONLY / DO NOT TRANSFER** | private AE loader ABI, version-sensitive and unsupported |
| HL installer | **DO NOT TRANSFER** | destructive replacement/quarantine behavior violates Gate 2 |

# Portable-test status for Gate 3A

## FSTR Line

The source repository preserves detailed local test records, including 13 pure-core tests and later 45-test CEP/core builds. The relevant GitHub Actions runs are no longer retained for the reviewed commits, and this Bible audit did not execute the FSTR repository itself.

Therefore:

- source/test mapping: **COMPLETE**;
- original project-reported portable results: **PRESERVED**;
- independent Bible rerun of the FSTR snapshot: **NOT RUN**.

A future copied/adapted implementation must receive Bible-owned regression tests instead of inheriting the source project's PASS.

## AE Hot Loader

Retained CI provides independent repository workflow evidence for the build/static/package lane. It is **not an AE host test**.

The private-loader AE result remains project-reported host evidence from the source project's test history; Bible did not independently repeat it.

# Bible-side regression and host acceptance plan

For accepted adaptations:

| Pattern | Portable Bible checks | Host checks |
|---|---|---|
| snapshot + command guard | version/identity/revision/malformed cases | real AE identity/invalidation behavior |
| coalesced refresh | one read for concurrent calls, stale-response rejection | panel reload, comp/project switch, visible/hidden lifecycle |
| FakeHostAdapter | same validators/types as real adapter | never used as host evidence |
| request correlation | version/request ID/error/timeout/stale reply | panel/Agent or panel/JSX integration in AE |
| loaded-module diagnostics | path/hash/version normalization | verify actual loaded module on supported OS/AE |

Private loader work has no destination in supported example gates.

# Gate 3A remaining item

The code/test/build mapping, provenance review, transfer decisions and Bible-side acceptance requirements are now written.

One checklist item remains intentionally open: **an independent portable rerun of the selected FSTR source snapshot was not performed in this audit**. The original test records are preserved but are not relabelled as Bible-run evidence.

Gate 3A must not be closed until that distinction is either accepted as sufficient for a no-code-copy architecture transfer or the selected portable source is independently rerun in an appropriate execution environment.
