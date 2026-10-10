# CI gates and publication — 1.2.1

## Committed documentation, not a repaired copy

Every `Validate` push/PR/manual run executes `python scripts/build_docs.py --check` against the checkout **before** any regeneration. A stale MASTER or MANIFEST is a failing check, including source-only and mixed changes. `docs_lane.py` reports historical lane/identity information only; selecting `source` cannot waive this check.

Regenerate locally with `python scripts/build_docs.py`, commit MASTER and MANIFEST with the source changes, then rerun Validate. The existing read-only PR regeneration workflow can supply a generated Git bundle; inspect/apply it to the exact source branch before merge. Its success is not the freshness gate. The main `Regenerate docs` workflow is now read-only and checks freshness before staging; it cannot silently repair main after validation or race a release.

MkDocs keeps intentional menu omissions informational but sets `validation.links.anchors: warn`; `mkdocs build --strict` therefore fails on nonexistent anchors. Explicit HTML IDs remain valid. The host-snapshot ID is explicit for GitHub and MkDocs. `tests/ci_gates` runs actual negative builds and verifies the workflow invokes the pre-regeneration gate unconditionally. No historical audit is silently rewritten.

## Licensed native SDK

`Native SDK gate` always reports its classification. Changes to native C/C++ headers/sources/resources in the template/cookbook/foundation/reference roots, existing SDK compiler runners or SDK contract tools/manifests invoke the real `18-SDK-HEADER-TOOLS/run-macos.sh`: inventory → required contracts → cookbook symbols → compiler/type checks. Renames/deletions are included. A first push or manual dispatch without a comparison base checks all native inputs. Non-native changes explicitly report NOT_APPLICABLE, not a new compiler PASS.

For hosted macOS CI the owner supplies a licensed ZIP through secret `AE_SDK_ARCHIVE_URL` and variables `AE_SDK_ARCHIVE_SHA256` and `AE_SDK_HEADERS_SHA256`. Both exact digests are checked; no SDK is obtained from an unofficial mirror or redistributed. The header identity is the existing `scripts.check_native.sdk_header_manifest(Examples)` algorithm over Headers and Util. Missing configuration/SDK, mismatched identity, unavailable base, timeout or failing runner gives a nonzero exit. A fork without SDK access cannot obtain a false PASS for native changes.

The runner uses the SDK 25.6 contract manifest already in this repository. New SDK generations require a separately reviewed pin/contract adoption. Compiler checks do not link a plugin or run AE. Local use: `AE_SDK_HEADERS_SHA256=<reviewed digest> python scripts/ci_native_gate.py --force --sdk /licensed/SDK/Examples`. The ZIP is extracted only into a disposable directory with bounded regular members; no setup script from it is executed.

The new CI integration is tested with synthetic fixtures and real compiler rejection controls. That is not a new licensed SDK or AE observation. This documentation/tooling-only release does not modify native consumer/driver/contract inputs, so its native compile is NOT_APPLICABLE. Owner SDK provisioning remains necessary before the first changed-native run can pass. The release publisher also compares native inputs with its pinned release base; a merge with unrelated before-SHA cannot hide native release changes.

## Required publication checks

The versioned publisher checks committed generated outputs again, waits for exact-source `Validate` and `Native SDK gate`, rejects skipped/failed/missing required jobs, verifies source archives and uploaded digests, and only then publishes the tag/release. Old releases and tags are not replaced. Repository server protection is separate: a green workflow is not proof that branch rulesets are enabled; this change does not alter account or protection settings.

Sources checked 2026-10-10: [MkDocs validation](https://www.mkdocs.org/user-guide/configuration/#validation), [GitHub Actions security](https://docs.github.com/en/actions/reference/security/secure-use). Local regressions and CI results, not these documents, establish the actual behavior of this repository.
