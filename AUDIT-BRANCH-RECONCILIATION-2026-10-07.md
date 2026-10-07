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

## Native/source review branch: transfer in progress

`audit/source-review-native-builds-2026-10-06` has one unique commit,
`31fba783df86cb2eff4eba86a897591123857ca3`, touching 55 files including generated
MASTER/MANIFEST. It must remain until the remaining unique material is reconciled.

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

Remaining queue: compare GPU/audio/AEIO/Artisan/native-panel workflow details,
compatibility/ScriptUI/ownership errata and manifest/bootstrap/staging additions
with current chapters and integration examples. Similar coverage or missing exact
lines alone is not proof that useful content has been transferred. **Do not delete
this sixth branch yet.**
