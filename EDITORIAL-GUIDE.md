# AE Developer Bible — Editorial Guide

Updated: **2026-10-02**

This is the **canonical writing and editing policy** for AE Developer Bible.

If wording in another planning/status document conflicts with this guide, this guide wins.

AE Developer Bible is a practical, research-backed knowledge base for After Effects developers. It is **not** a plug-in QA program and does not need to build or host-test every source example to be editorially complete.

---

# 1. Mission

Bible should help a developer answer:

- what kind of extension to build;
- which After Effects API family owns the problem;
- what lifecycle/ownership/threading rules apply;
- which SDK suites/selectors/entry points matter;
- how platform/build/debug/test/release workflows should be designed;
- what is documented fact, SDK-reviewed fact, runtime observation, reconstruction or recommendation;
- what can go wrong and how to reason about it.

Quality target:

> **complete + accurate + practical + internally consistent + evidence-aware documentation.**

---

# 2. Mandatory work mode: write in logical blocks

> **Finish one logical block → commit it to GitHub → validate it → send the user a short status → only then start the next logical block.**

Do **not** silently continue into the next topic after finishing a block.

## What is a logical block

A logical block is a group of chapters/files that form one coherent developer topic and can be reviewed as one unit.

Examples:

- AEGP compositions + layers + render frames + render queue;
- Memory + Undo + Persistent Data + Lifetime/Threading;
- CEP bridge + native/script communication;
- macOS build/sign/package workflow;
- Windows debug/sign/package workflow;
- GPU architecture + CPU/GPU equivalence;
- Streams + properties + keyframes;
- AEIO import/export lifecycle;
- Artisan renderer lifecycle.

A block is defined by one technical theme and one completion boundary, not by file count.

## Block completion rule

Before a block is called complete:

1. all related chapters in the block are read together;
2. contradictions are removed;
3. SDK/version boundaries are explicit;
4. ownership/threading/failure semantics are covered where relevant;
5. related recipes/examples are reconciled;
6. cross-links are valid;
7. evidence labels are correct;
8. changes are committed to `main`;
9. `Validate` passes;
10. `mkdocs build --strict` passes;
11. generated docs/manifest regenerate successfully;
12. only then send the user a block status.

## Required status after each block

The status must be short and include:

- block name;
- what was added/corrected;
- important contradictions/findings;
- validation result;
- current Git HEAD;
- next proposed logical block.

Recommended format:

```text
Готов блок: <название>

Сделано:
- ...
- ...

Проверки:
- Validate ✅
- mkdocs --strict ✅
- Regenerate docs ✅

HEAD: <sha>

Следующий логичный блок: <название>
```

After this report, **stop and wait for the user's next instruction before starting the next block**.

---

# 3. What Bible completion means

Bible is editorially complete when:

- major extension families are covered;
- practical workflows are covered;
- version-sensitive native claims have a known SDK/source basis;
- evidence levels are explicit;
- recipes/examples do not contradict chapters;
- unknowns and limitations are stated;
- platform/build/test/release guidance is usable;
- navigation/cross-links/provenance are consistent;
- generated documentation passes strict validation.

Bible completion does **not** require:

- compiling every C++ file;
- building every example;
- running every example inside AE;
- Windows/macOS builds of all reference code;
- signing/notarizing demo binaries;
- clean-machine installation of demo binaries;
- exhaustive MFR/GPU host QA of every snippet;
- finishing the entire bundled-effect reverse-engineering atlas.

Those are product-validation tasks unless Bible explicitly claims such a runtime result.

---

# 4. Chapter completeness standard

A practical core chapter should answer, where applicable:

1. What is this?
2. When should it be used?
3. When should it not be used?
4. Who calls whom?
5. What is the lifecycle?
6. What state exists and who owns it?
7. What must be released/disposed/checkin'd?
8. What can become invalid/stale?
9. What threading/main-thread rules apply?
10. What version/platform boundaries exist?
11. What failure modes matter?
12. What production workflow is recommended?
13. What common anti-patterns exist?
14. What should a product test?
15. Which recipes/templates/source examples are related?
16. What evidence level supports the chapter?

Not every chapter needs all sixteen headings literally, but every relevant question must be answered somewhere obvious.

---

# 5. Evidence vocabulary

## DOCUMENTED

Backed by current public/canonical documentation.

## SDK-CONTRACT-REVIEWED

Version-sensitive native statement checked against the actual target SDK headers/samples.

## SOURCE EXAMPLE

Source demonstrates a pattern or integration shape. It does **not** imply compiled, linked, loaded, runtime-correct or release-ready.

## PROJECT-REPORTED

A result recorded by another concrete project/test history. Scope it to that project/build/environment.

## RUNTIME-OBSERVED

A concrete runtime result was actually observed and recorded for a specific artifact/environment.

## RECONSTRUCTED

A conclusion derived from evidence/reverse engineering. Never present it as a documented public contract.

## RUNTIME-NOT-CLAIMED

Bible explains a source/API pattern but does not assert host execution. This is a valid final editorial state, not an automatic TODO.

## Evidence identity and historical records

Compiler and runtime results belong to the source/artifact that was actually checked. A usable record identifies the date, source commit or file hashes, SDK/compiler or AE build, platform, commands/scenario and result. For a binary result, record the tested artifact identity separately from the documentation commit.

An older PASS does not transfer to modified code. If a historical report lacks source identity, preserve its reported result and mark the identity gap; do not infer the tested source from the commit that published the report. Current code remains SOURCE EXAMPLE / RUNTIME-NOT-CLAIMED unless matching evidence exists.

Dated source reviews retain their original hashes, ranges, findings and NOT RUN results. Add a dated correction when a later review changes a conclusion or planning rule. Historical references to stages or Gates describe the old process; current work is tracked in [the completion plan](COMPLETION-PLAN.md) and [the chapter tracker](CHAPTER-COMPLETION-TRACKER.md).

In active chapter/example guidance, use RUNTIME-NOT-CLAIMED instead of an unexplained “host test pending/required” label. Product-validation scenarios must say which reader-product claim they test. They do not become mandatory Bible tasks.

---

# 6. Source hierarchy

## Claim registry and build provenance

[Block 5 table](BLOCK-5-SOURCES.md) is generated from reviewed claim records in `sources/claim-registry.json`. Keep SDK baseline, host support, panel runtime and platform policy separate. Technical source identities (SDK bytes / upstream snapshot / dated vendor page) must not be replaced with Bible source/generated Git SHAs. Documentation CI provenance is a separate historical table, not API or runtime evidence. Generator/schema checks cannot certify source truth; review the claim and its exact applicability before adding a record.

## Native compile-time/API facts

Priority:

1. exact target SDK headers;
2. utility headers / SuiteHandler from the same SDK;
3. official sample from the same SDK distribution;
4. current public guide;
5. historical/community sources.

## Ownership/lifetime

A prototype is not enough. Use header comments, paired cleanup APIs, official sample cleanup, public guide and runtime evidence only when relevant.

## Platform/security/distribution facts

Use current Adobe/Apple/Microsoft documentation and preserve review date/version boundary.

## Migration/roadmap facts

Use current official announcements and mark them as dated planning facts.

---

# 7. Header-first native rules

- exact declaration comes from the target SDK header;
- suite generations are real contracts, not decorative labels;
- public suite-version macro may not match struct suffix numerically;
- enum parameters must not be replaced by bool/int merely because conversion compiles;
- old samples may use old suite generations;
- never cast old suite tables into newer generations;
- validate size/version before optional tail fields;
- compile availability and runtime availability are separate;
- missing runtime evidence means no runtime claim, not incomplete documentation.

---

# 8. Handling conflicts and errata

When header, sample, guide or historical code disagree:

1. stop;
2. identify exact SDK/version;
3. classify mismatch: typo, stale HTML, historical suite, API change, simplified sample, unresolved;
4. choose the source appropriate to the claim;
5. document version boundary;
6. update all related chapters/recipes;
7. preserve useful historical findings;
8. mark superseded conclusions explicitly.

Never choose the source merely because it makes the snippet easier.

---

# 9. SDK baseline policy

Current primary native baseline:

**Adobe After Effects SDK 25.6 build 61**

Current recorded contract audit:

- **35/35 required contracts present**;
- **39/39 cookbook call-sites resolved**;
- **0 required parser diagnostics**.

Later SDK research must remain explicitly version-gated.

---

# 10. Recipes and source examples

Recipes should optimize for correct API shape, clear ownership, explicit lifecycle, safe cleanup, clear version boundary and readability.

Rules:

- prefer exact named enum/constants;
- show paired cleanup;
- show invalidation/re-query when relevant;
- do not cache opaque refs without documented lifetime;
- do not hide thread requirements;
- do not present a sample shortcut as a universal production rule;
- distinguish current SDK baseline from compatibility-shaped older source;
- label later-version features explicitly.

---

# 11. Runtime/build evidence policy

Compilation and host execution are evidence classes, not universal editorial requirements.

If Bible says compiled/loaded/runtime-observed, concrete evidence must be tied to source/artifact identity, environment, version/build and result.

If that evidence does not exist, use source/documented wording instead.

Never upgrade a chapter to runtime-observed because docs CI is green, a stub test passes, a historical sample exists, or another project behaved similarly.

---

# 12. Ownership and lifetime writing rules

Whenever a chapter introduces a handle/ref/resource, document:

- who creates it;
- who owns it;
- whether ownership transfers;
- exact cleanup function;
- validity duration;
- invalidation triggers;
- thread permission;
- persistence rules.

Do not write generic "free the handle" prose when APIs use different cleanup families such as Dispose, FreeMemHandle, CheckinFrame, ReleaseSuite, EndUndoGroup or EndAddKeyframes.

---

# 13. Threading writing rules

Never infer thread safety from object lifetime, suite availability, const pointer, native/C++ implementation or worker ownership.

If exact thread permission is not documented, do not invent it.

Conservative architecture guidance may recommend pure background compute, late host-ref resolution, host-safe mutation, no product mutex across opaque host calls and immutable/per-frame MFR state. Mark recommendations as recommendations.

---

# 14. Error/failure writing rules

For nontrivial workflows cover:

- acquisition failure;
- partial initialization;
- stale target;
- operation failure;
- cleanup failure;
- cancellation;
- shutdown;
- retry/idempotence where relevant.

Preserve primary error separately from cleanup error.

Do not imply Undo is database rollback.

Do not imply RAII repairs a wrong ownership assumption.

---

# 15. Platform/version writing rules

Keep separate SDK baseline, AE support range, compiler/toolchain, OS policy, CPU architecture, GPU backend, panel runtime and signing/release policy.

Do not infer product compatibility from one SDK version.

Dated facts require date/version boundary.

---

# 16. Research appendices

Reverse-engineering and case-study sections are valuable but non-blocking.

Rules:

- preserve provenance;
- distinguish observed/reconstructed/documented;
- keep private/internal API research out of supported SDK recipes;
- mark superseded hypotheses;
- do not let unfinished atlas work block core Bible readiness.

---

# 17. Style rules

Prefer diagrams, tables, call flows, failure examples, production patterns and anti-patterns.

Technical API names stay in English exactly as defined. Russian explanatory prose is the current primary editorial language.

Avoid absolute words such as always/never/guaranteed/thread-safe/stable forever unless the source contract supports them.

Every code-like example should make clear whether it is exact call shape, pseudocode, source example, later-version note or reconstructed behavior.

---

# 18. Cross-link rules

Every block completion checks related chapters, recipe links, template links, source-review records, renamed files and navigation.

Use explicit README.md links for directories when MkDocs strict mode requires it.

No block is complete with broken strict links.

---

# 19. Provenance rules

For exact SDK/source review preserve enough information to reconstruct the conclusion:

- SDK version/build;
- file path/source sample;
- source hash where formal review uses hashes;
- review date;
- version boundary.

Do not redistribute proprietary Adobe SDK headers.

---

# 20. Canonical support documents

This guide contains the **rules**.

Other files have narrower roles:

- `README.md` — public mission/entry point;
- `COMPLETION-PLAN.md` — current roadmap;
- `COMPLETION-CHECKLIST.md` — progress/checklist;
- `STATUS.md` — current status;
- `VERIFICATION.md` — evidence ledger;
- `FINAL-COVERAGE-AUDIT.md` — coverage matrix;
- `SOURCES.md` — source registry;
- `18-SDK-HEADER-TOOLS/04-HEADER-FIRST-RULES.md` — detailed native source-policy reference;
- `14-NATIVE-INTEGRATIONS/13-DOCS-ERRATA.md` — concrete errata/conflict record.

If these files repeat a rule, the canonical formulation belongs here.

---

# 21. Stop rule

For every work session:

```text
choose one logical block
→ finish it
→ reconcile related files
→ validate docs
→ commit to main
→ send user status
→ STOP
```

Start the next block only after the user asks to continue or approves the next block.

This workflow is mandatory for continued development of AE Developer Bible.
