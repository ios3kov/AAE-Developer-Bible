# AAE Developer Bible 1.2.1 — working CI gates

Patch to v1.2.0 (`e796313877b996a0e8701341e682915c35c6ce94`). Correct the documentation checks and release path without rewriting AE development rules or claiming new host/API coverage.

- Check committed MASTER/MANIFEST on every PR/push and again before publication, before regeneration. Main regeneration can no longer silently repair stale source commits.
- Make missing MkDocs anchors fail strict builds; preserve valid explicit anchors and add a shared host-snapshot anchor for GitHub/MkDocs.
- Invoke the real pinned SDK runner on changed native inputs. Missing licensed SDK/configuration is BLOCKED; non-native changes are explicitly NOT_APPLICABLE. SDK setup and exact limits: [CI gates](CI-GATES.md).
- Test intentional stale outputs, source-only/mixed drift, broken anchors/files, native change classification, missing/wrong SDK pins and compiler/runner failures.
- Separate the current verification summary from historical counts. Thirteen historical compiler invocations are ten primary sources, two forwarding entries and one foundation probe, not thirteen independent implementations. Menu omission history remains intact.

This release changes documentation and CI/tooling only. Real Adobe SDK compilation and AE host runtime are not asserted for it; native source consumers and the existing compiler/contract runners remain unchanged. The owner must provision the licensed SDK before a future changed-native run can pass.

Exact released Git SHA, final CI and archive digests are attached as `release-evidence.json` and `SHA256SUMS.txt`. Green CI does not establish repository branch protection or the correctness of all AE examples.
