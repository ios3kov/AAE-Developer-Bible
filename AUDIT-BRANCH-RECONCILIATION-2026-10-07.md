# Remaining audit branches — selective reconciliation

Compared with clean main `feccc33` on 2026-10-07 after fetching origin. Review uses
`git log main..branch` and `git diff main...branch`: a whole branch-tip diff against
main would reintroduce superseded files. This record tracks transfer decisions,
not new SDK compilation or AE runtime evidence.

## Export-only branches: review complete

Each branch has exactly one commit not in main, adding only its dated export
workflow. There are no chapter/source/test additions to transfer. Do not revive
one-off CI exports or their older source baselines.

| Branch after `audit/` | Unique commit | Only changed file under `.github/workflows/` |
|---|---|---|
| editorial-final-scan-2026-10-01 | `fd71c33` | `editorial-final-scan.yml` |
| editorial-model-scan-2026-10-01 | `a5bb398` | `editorial-model-scan.yml` |
| editorial-model-scan2-2026-10-01 | `43a4120` | `editorial-model-scan2.yml` |
| gate4-exact-sdk-2026-10-01 | `81dd429` | `gate4-exact-source-export.yml` |
| gate4-source-export-2026-10-01 | `dfbc99e` | `gate4-source-export.yml` |

These five branches are eligible for removal after publishing this review.
They were removed from origin after publishing selective transfer `6a3fc0f`.

## Cookbook companion reconciliation

Read project/item, layer, effect, keyframe, frame-render and render-queue chapters
alongside all six corresponding C++ recipe files. Clarified partial output counts/
handles, LayerID truncation, apply-versus-cleanup failure, static OneD restrictions,
caller-only time/value validation, exception gaps in batch/value cleanup and the
render helper's borrowed-options/null-cancel/consumer boundaries. Queue chapter
already states missing STOPPED preflight, path readback and compensation accurately.
No source implementation changed and no new native compile/AE result is implied.

## Native/source review branch: review complete

`audit/source-review-native-builds-2026-10-06` has one unique commit,
`31fba783df86cb2eff4eba86a897591123857ca3`, touching 55 files including generated
MASTER/MANIFEST. Remaining unique material was reconciled selectively below; the
commit is retained as immutable provenance, not merged as an old tree.

Transferred in the first selective block:

- CEP user folder correction in chapters 07/11: `%AppData%` already includes Roaming.
- SignTool warning exit code, verification policy and deliberate signer selection;
  [vendor reference](https://learn.microsoft.com/en-us/windows/win32/seccrypto/signtool)
  reread on 2026-10-07. No Windows execution claimed.
- Lifecycle arrows are not a guaranteed callback trace; snapshot cancellation and
  post-shutdown host-call boundaries.
- Whole-Examples materialization as optional `--workspace` mode, keeping current
  source-shell API and its safety regressions. Two added portable tests cover
  relative dependencies, existing-output refusal and SDK overlap.

Not transferred blindly:

- The branch's per-user native MediaCore rejection is based on the installer page
  alone. [Sample Projects](https://ae-plugins.docsforadobe.dev/intro/sample-projects/)
  explicitly recommends the per-user path for macOS development; reread on
  2026-10-07 alongside the installer/debugger pages. Keep current development versus
  release distinction, without inventing host load evidence.
- Historical native link evidence is already preserved in [BUILD-EVIDENCE](BUILD-EVIDENCE.md)
  with exact source continuity and limitations. Do not replace it with an apparent
  current-main build PASS or restore the old build driver automatically.
- Old release-gate/claims reports, acceptance duplicate, CEP protocol/tests and
  generated outputs are not restored. Current editorial policy, chapter tracker,
  evidence plan and protocol tests are authoritative. Branch protocol uses different
  envelope fields and prefix limits.
- SmartFX's blanket parameter-checkin guidance must not replace the current
  phase-specific contract: pre-render auto-checkin versus render explicit checkin.

Final topic comparison and decisions:

| Audit material | Current destination / decision |
|---|---|
| GPU capability/device/backend/CPU parity | GPU chapter sections1–12 and Metal walkthrough cover negotiation, failure and ownership; platform GPU chapters retain current sample limitations. No old generic workflow duplicated. |
| Sound format/range/random access | Audio chapter sections3–10 and bounded DSP walkthrough cover bytes, format, scheduling and absence of matching bundled dispatcher. Do not restore an unsupported sample assertion. |
| AEIO registration/options/defaults/sample | AEIO overview exact IO route and sections1–17 plus native registration chapter cover options/default codes and partial registration. Keep current exact callback findings. |
| Artisan normal/interactive/context/workflow | Artisan overview sections1–19 and exact Artie route distinguish renderer/context/interactive behavior; sample limitations retained. No extra renderer implementation promised. |
| ScriptUI/JSX Undo/indexed group invalidation | ScriptUI architecture/chunk/generation/Panel-vs-Window route, object-model invalidation and scripting Undo/partial failure already expanded; current authored rig and portable tests authoritative. |
| Panelator match name/container/worker shutdown | Native panel sections1–24 and source record cover exact table, borrowed platform containers, recreation and teardown omissions. |
| Compatibility identity/matrix | Kept suite gating and added explicit illustrative-matrix label, separate identity table and unsupported-before-mutation walkthrough. |
| RAII reset/owner preconditions | Added same-handle reset and alias-owner hazards visible in current AegpOwners.h; suite lifetime and diagnostic limits already explicit. |
| SmartFX/audio/PiPL errata | Consolidated bounded findings in current errata chapter; no obsolete prose overwrites current contracts. |
| CEP manifest/bootstrap | Current reviewed integration walkthrough intentionally requires user-supplied target manifest/dependencies; old bundled manifest asserts an untested range and bootstrap uses older protocol. Do not revive them. |
| HTML/XML/CJS staging | Added source staging extensions and HTML-as-download policy with regression test; avoids collision with MkDocs chapter index. |
| Old tests/link checker/host runner/build driver | Current protocol/consistency and safe-tooling tests supersede old tests. Current host runner has transactional restore and missing-output checks; do not regress to old process-only success. Historical driver remains at immutable commit. |
| Status/reports/nav/generated files | Current guide/tracker/ledger/evidence plan are authoritative; no stale release gates, duplicate acceptance or generated blob imported. |

All 55 changed paths fall into transferred corrections, current authoritative
coverage or explicit non-transfer decisions above and in the first-block list.
The final audit branch is eligible for removal after publication and checks.
