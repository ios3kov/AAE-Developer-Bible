"""One-time hash-guarded preparation. Only stores blobs, never changes refs or releases."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import urllib.request

BASE = 'e796313877b996a0e8701341e682915c35c6ce94'
REPO = 'ios3kov/AAE-Developer-Bible'
TEMP = ['.github/prepare-ci-patch.py', '.github/workflows/prepare-ci-patch.yml']
updates = {}
assert os.environ['GITHUB_REPOSITORY'] == REPO
assert os.environ['GITHUB_REF'] == 'refs/heads/fix/bible-ci-gates-1.2.1'


def git(*args):
    return subprocess.check_output(['git', *args])


def original(path, expected=None):
    data = Path(path).read_bytes()
    assert data == git('show', BASE + ':' + path), 'Unexpected baseline content: ' + path
    actual = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
    assert expected is None or expected == actual, 'Original hash mismatch: ' + path
    return data.decode('utf-8')


def replace_once(text, old, new):
    assert text.count(old) == 1, 'Replacement not unique: ' + old[:100]
    return text.replace(old, new, 1)


validate = original('.github/workflows/validate.yml', '5be6cbd2129a056b6d11054065e20cacf943c5c0')
validate = replace_once(validate, 'description: Source staging or frozen generated revision',
                        'description: Identity reporting lane; committed freshness is always required')
validate = replace_once(validate,
    "      - name: Reject stale frozen outputs before regeneration\n        if: steps.docs-lane.outputs.lane == 'frozen'\n        run: python scripts/build_docs.py --check\n", '')
validate = replace_once(validate, '      - name: CEP bridge portable protocol tests (not AE host tests)\n',
    '      - name: Reject stale committed documentation before any regeneration\n        run: python scripts/build_docs.py --check\n      - name: CEP bridge portable protocol tests (not AE host tests)\n')
validate = replace_once(validate, '      - name: Documentation consistency regressions\n',
    "      - name: CI gate negative execution controls (not Adobe runtime tests)\n        run: python -m unittest discover -s tests/ci_gates -v\n      - name: Documentation consistency regressions\n")
updates['.github/workflows/validate.yml'] = validate
original('.github/workflows/regenerate-effects-catalog.yml', '34bbdb398664dbdc46a27393aa817dfe6f5bf13a')
updates['.github/workflows/regenerate-effects-catalog.yml'] = '''name: Regenerate docs
on:
  push:
    branches: [main]
  workflow_dispatch:
permissions:
  contents: read
jobs:
  regenerate:
    runs-on: ubuntu-latest
    timeout-minutes: 5
    steps:
      - uses: actions/checkout@11d5960a326750d5838078e36cf38b85af677262
        with:
          ref: ${{ github.sha }}
          persist-credentials: false
      - uses: actions/setup-python@a26af69be951a213d495a4c3e4e4022e16d87065
        with:
          python-version: '3.11'
      - name: Require committed freshness, then verify isolated generation; never repair main
        run: |
          python scripts/build_docs.py --check
          python scripts/build_docs.py --output-root "$RUNNER_TEMP/bible-regeneration"
          python scripts/build_docs.py --check --output-root "$RUNNER_TEMP/bible-regeneration"
          git diff --exit-code
'''
mkdocs = original('mkdocs.yml', 'c3638ab7eaaf86ee607f283f29c9e4f6cb025301')
mkdocs = replace_once(mkdocs, 'validation:\n  nav:\n    omitted_files: info\n',
    'validation:\n  nav:\n    omitted_files: info\n  links:\n    anchors: warn\n')
mkdocs = replace_once(mkdocs, '  - Verification: VERIFICATION.md\n',
    '  - Verification: VERIFICATION.md\n  - CI gates and SDK setup: CI-GATES.md\n  - CI correction release 1.2.1: RELEASE-1.2.1.md\n')
updates['mkdocs.yml'] = mkdocs
path = '00-START-HERE/02-ENVIRONMENT-MATRIX.md'
updates[path] = replace_once(original(path, '6087625d991cdba901346e414da7a06c2428268b'),
    '## Опубликованный host snapshot — 2026-10-08',
    '<a id="host-snapshot-2026-10-08"></a>\n\n## Опубликованный host snapshot — 2026-10-08')
verification = original('VERIFICATION.md')
updates['VERIFICATION.md'] = replace_once(verification, '# Verification purpose\n', '''# Verification purpose

## Current CI contract — 2026-10-10 / correction 1.2.1

[CI gates and reproduction](CI-GATES.md) is the current checking procedure; the dated records below are historical observations, not a fresh PASS for the present commit. Exact final checks and source identity are recorded by the GitHub run and release-evidence.json after execution, never predicted here.

| Topic | Reading the evidence correctly |
|---|---|
| Generated documentation | Every PR/push checks the committed MASTER/MANIFEST before regeneration; a repaired staging copy is not proof of committed freshness |
| Link validation | Strict MkDocs treats missing anchors as errors; explicit HTML aliases are valid |
| Native compilation | The current integration runs the real SDK runner only for changed native inputs; SDK absence then blocks it. This patch does not modify those inputs or assert a fresh Adobe compile |
| Historical compiler counts | 10 primary C++ sources + 2 forwarding entries + 1 foundation probe = 13 compiler invocations, not 13 independent implementations |
| SDK table/function totals | Older 230 / 3537 counts and later inventory counts belong to their dated parser/SDK reports; neither is a current unique-API coverage claim |
| Menu omissions | Count the actual candidate; old 46/27 figures below and in the navigation audit are historical snapshots |

---

## Historical verification ledger (dates and original scopes preserved)
''')
navigation_audit = original('NAVIGATION-AUDIT.md', 'b91a339e16730f461e4794b7c62c037938fa7fd8')
updates['NAVIGATION-AUDIT.md'] = replace_once(navigation_audit, '# Navigation audit — block 3\n', '''# Navigation audit — block 3

> Current reading note — 2026-10-10: the 46-row baseline and subsequent 27-omission result below are historical. The current candidate's omission list is emitted by MkDocs; archive/evidence/generated pages need not all appear in the main menu. Link/anchor validity is checked separately and strictly by [CI](CI-GATES.md). No historical count or browser result is replaced with a new unperformed observation.
''')
readme = original('README.md', 'dcab82e4e272bba3041406daec7f50941a8d4a02')
updates['README.md'] = replace_once(readme, '# AE Developer Bible\n', '''# AE Developer Bible

CI correction **1.2.1 — 2026-10-10**: [changes](RELEASE-1.2.1.md), [working gates and SDK setup](CI-GATES.md). Publication and exact source are established by [GitHub Release v1.2.1](https://github.com/ios3kov/AAE-Developer-Bible/releases/tag/v1.2.1) and its Evidence, not this version label. The historical edition and source-review dates below remain unchanged.
''')
changelog = original('CHANGELOG.md')
first, rest = changelog.split('\n', 1)
updates['CHANGELOG.md'] = first + '''

## 1.2.1 — 2026-10-10 — CI correctness patch

Unconditional committed MASTER/MANIFEST freshness before regeneration; strict anchor failures; read-only main regeneration; real licensed-SDK CI lane for changed native inputs with explicit BLOCKED/N/A boundaries; negative execution regressions and clearer historical counters. Native examples/SDK contract drivers and historical evidence remain unchanged. [Release notes](RELEASE-1.2.1.md), [CI/adoption](CI-GATES.md). Final run/tag/assets establish publication, not this entry.
''' + rest
for name, text in updates.items():
    Path(name).write_text(text, encoding='utf-8')
for name in TEMP:
    Path(name).unlink()
subprocess.run(['git', 'diff', '--check'], check=True)
subprocess.run([sys.executable, '-m', 'unittest', 'discover', '-s', 'tests/ci_gates', '-v'], check=True)
subprocess.run([sys.executable, '-m', 'unittest', 'discover', '-s', 'tests/consistency', '-v'], check=True)
subprocess.run([sys.executable, 'scripts/check_docs_consistency.py'], check=True)
subprocess.run([sys.executable, 'scripts/generate_sources_table.py', '--check'], check=True)
subprocess.run([sys.executable, 'scripts/build_docs.py'], check=True)
subprocess.run([sys.executable, 'scripts/build_docs.py', '--check'], check=True)
subprocess.run([sys.executable, '-m', 'mkdocs', 'build', '--strict'], check=True)
subprocess.run(['git', 'diff', '--check'], check=True)
headers = {'Authorization': 'Bearer ' + os.environ['GH_TOKEN'], 'Accept': 'application/vnd.github+json'}
entries = []
for name in sorted(set(updates) | {'MASTER-AE-DEVELOPER-BIBLE.md', 'MANIFEST.sha256'}):
    data = Path(name).read_bytes()
    payload = json.dumps({'content': data.decode('utf-8'), 'encoding': 'utf-8'}).encode()
    request = urllib.request.Request('https://api.github.com/repos/' + REPO + '/git/blobs', data=payload, headers=headers, method='POST')
    with urllib.request.urlopen(request, timeout=60) as response:
        result = json.load(response)
    expected = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
    assert result['sha'] == expected, 'Uploaded blob mismatch'
    mode = git('ls-tree', BASE, '--', name).decode().split()[0]
    entries.append({'path': name, 'mode': mode, 'type': 'blob', 'sha': expected})
entries += [{'path': name, 'mode': '100644', 'type': 'blob', 'sha': None} for name in TEMP]
print('PREPARED_ENTRIES=' + json.dumps(entries))
print('Preparation only; no refs, tags, releases or repository settings were changed.')
