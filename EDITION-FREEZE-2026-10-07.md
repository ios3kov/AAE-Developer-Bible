# AE Developer Bible — edition 1.1 editorial freeze

Date: **2026-10-07**. Outcome: **editorially complete**, not a plug-in product release.

## Revision identity

Technical reconciliation parent: `c8d8672` (resolve full SHA with `git rev-parse c8d8672`).
Freeze source revision is the commit containing this record and final status/checklist
changes. Generated MASTER/MANIFEST are committed with that same revision, not a
separate bot revision. Resolve exact freeze SHA using:

```sh
git log -1 --format=%H -- EDITION-FREEZE-2026-10-07.md
git show <freeze-sha>:MASTER-AE-DEVELOPER-BIBLE.md
```

The MASTER source-content SHA256 binds tracked source bytes (excluding generated
outputs); it is not a Git SHA. MANIFEST binds individual file bytes. The record
does not embed its own commit/hash, avoiding a circular identity. Later changes
require a new reviewed iteration; a later HEAD is not this freeze automatically.

## Acceptance

- All **127 core pages** individually reconciled across five axes, `C`/explicit `L`;
  chapter tracker links dated results, including final nine entry/index rows.
- First Effect, automation/ScriptUI/CEP and native/AEGP routes reconcile canonical
  chapters, actual source, recommended workflow and evidence limits.
- Native source baseline remains **SDK25.6 build61**. Later public-guide inventories
  do not masquerade as exact SDK26.5 headers. Ownership, callback/thread permission,
  mutation/invalidation, cleanup and partial failures are explicit in topic reviews.
- Filled Gain pack is ILLUSTRATIVE/NOT_RUN. Project measurements preserve separate
  native/export/Preview workloads, raw-record scope and immutable incident history.
- Owner chose no reuse license; NOTICE/vendor rights remain explicit.
- MASTER/MANIFEST regenerated, freshness and strict MkDocs checked; local portable
  sweep and static navigation checks recorded in VERIFICATION.

## Retained limits

- No new real-SDK compilation/link, AE runtime, Windows/MSVC, Universal/GPU/MFR,
  debugger/signing/notary/install or product security implementation result.
- UXP published documentation is not installed beta/GA/API-execution evidence.
  Adobe requirements reread HTTP403: older dated host matrix retained explicitly.
- BlitHook async details, bounded custom-UI/audio/source adapters and catalogue
  inventory limits remain visible; index `L` means a route, not standalone code.
- Atlas/case studies are ongoing appendices. Tool adaptation is not copied or
  silently required for edition completion. Full external-collection audit is absent.
- Final GitHub CI status is not observed here (`gh` unavailable); local checks are
  not a substitute claim of remote Validate success. Owner's `b20806b` check remains
  separate. Browser search ranking/private-profile limitations remain historical.

## Reproduce

At the exact freeze revision, with dependencies from `requirements-docs.txt`:

```sh
python scripts/build_docs.py --check
python scripts/check_docs_consistency.py
python scripts/generate_sources_table.py --check
python scripts/build_docs.py
mkdocs build --strict
git diff --exit-code -- MASTER-AE-DEVELOPER-BIBLE.md MANIFEST.sha256
```

These validate documentation/tooling identities, not plug-in host behavior. GitHub
publication is the authorized push to existing main; no SDK distribution, binary
product release, new license or release tag is implied.
