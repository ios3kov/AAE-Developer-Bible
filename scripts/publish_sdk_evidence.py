#!/usr/bin/env python3
"""Owner-authorized v1.2.2 source-only publisher; imports have no side effects."""
import gzip
import hashlib
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tarfile
import time
import urllib.error
import urllib.parse
import urllib.request
import zipfile

REPO = 'ios3kov/AAE-Developer-Bible'
TAG = 'v1.2.2'
BASE = '0ea8131bcb599fc52df5c7cf6d1d7057bf4d1352'
ROOT = Path(__file__).resolve().parents[1]


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def verified_jobs(jobs, required):
    selected = [j for j in jobs if j.get('name') in required]
    require(len(selected) == len(required) and {j['name'] for j in selected} == required and
            all(j.get('status') == 'completed' and j.get('conclusion') == 'success' for j in selected),
            'Missing, duplicated, skipped or failed required exact-source job')


def verify_archive(data, kind, expected, prefix):
    actual = {}
    if kind == 'zip':
        with zipfile.ZipFile(io.BytesIO(data)) as archive:
            for item in archive.infolist():
                if item.is_dir():
                    continue
                require(item.filename.startswith(prefix), 'Wrong ZIP prefix')
                name = item.filename[len(prefix):]
                require(name in expected and name not in actual, 'Unexpected/duplicate ZIP member')
                actual[name] = (archive.read(item), ((item.external_attr >> 16) & 0o777) or 0o644)
    else:
        with tarfile.open(fileobj=io.BytesIO(data), mode='r:gz') as archive:
            for item in archive:
                if item.isdir():
                    continue
                require(item.isfile() and item.name.startswith(prefix), 'Unexpected TAR type/path')
                name = item.name[len(prefix):]
                require(name in expected and name not in actual, 'Unexpected/duplicate TAR member')
                actual[name] = (archive.extractfile(item).read(), item.mode & 0o777)
    require(actual == expected, 'Source archive differs from exact Git tree bytes/modes')


OWNER_EVIDENCE = 'evidence/native-sdk-2026-10-10'
OWNER_REPORT_SHA256 = 'bd396e6b12f9b7f989a8903863a3b83018fce642e9167d1e30de5fc8b9a9bfbe'


def validate_owner_evidence(root):
    """Validate received/redacted historical evidence, not perform a new SDK compile."""
    report_path = Path(root) / OWNER_EVIDENCE / 'native-compile-report.redacted.json'
    data = report_path.read_bytes()
    require(hashlib.sha256(data).hexdigest() == OWNER_REPORT_SHA256, 'Owner evidence bytes changed')
    report = json.loads(data)
    provenance = json.loads((report_path.parent / 'provenance.json').read_text())
    require(report['source']['git_sha'] == BASE and report['source']['dirty'] is False, 'Wrong tested source')
    require(report['summary'] == {'translation_units': 13, 'failed': 0, 'status': 'PASS'}, 'Wrong compiler summary')
    require(len(report['results']) == 13 and len({r['source'] for r in report['results']}) == 13, 'Wrong compiler result set')
    require(all(r['status'] == 'PASS' and type(r['returncode']) is int and r['returncode'] == 0 and not r['stdout_tail'] and not r['stderr_tail'] for r in report['results']), 'Failed or inconsistent compiler result')
    require(provenance['tested_source_git_sha'] == BASE and provenance['public_report']['sha256'] == OWNER_REPORT_SHA256, 'Provenance mismatch')
    require(provenance['original_report']['sha256'] == '7b0668a5c0a45692c7e7f966459f64c89e2477cb2a02b789ab0b20471b2c7569' and provenance['original_report']['included'] is False, 'Original identity mismatch')
    require(b'/var/folders/' not in data and b'/Users/' not in data, 'Private path in public report')
    return report


def main():
    sys.path.insert(0, str(ROOT))
    from scripts.ci_native_gate import affected, changed_paths
    target = os.environ['GITHUB_SHA']
    require(os.environ['GITHUB_REPOSITORY'] == REPO and os.environ['GITHUB_REF'] == 'refs/heads/main', 'Wrong repository/ref')
    def git(*args):
        return subprocess.check_output(['git', *args], cwd=ROOT, timeout=60)
    require(git('rev-parse', 'HEAD').decode().strip() == target, 'Wrong checkout')
    require(not affected(changed_paths(ROOT, BASE, target)), 'This patch authorizes no changed native SDK inputs')
    validate_owner_evidence(ROOT)
    require(not git('status', '--porcelain').strip(), 'Release checkout must be clean')
    subprocess.run([sys.executable, 'scripts/build_docs.py', '--check'], cwd=ROOT, check=True)
    headers = {'Authorization': 'Bearer ' + os.environ['GH_TOKEN'], 'Accept': 'application/vnd.github+json',
               'X-GitHub-Api-Version': '2022-11-28'}
    def api(path, data=None, method=None):
        request = urllib.request.Request('https://api.github.com/repos/' + REPO + path, headers=headers,
                                        data=None if data is None else json.dumps(data).encode(),
                                        method=method or ('GET' if data is None else 'POST'))
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                return json.load(response)
        except urllib.error.HTTPError as error:
            if error.code == 404 and data is None:
                return None
            raise RuntimeError('GitHub API HTTP ' + str(error.code)) from None
    required = {'Validate': {'portable-checks', 'macos-path-regression'},
                'Native SDK gate': {'native-sdk-gate'}, 'Regenerate docs': {'regenerate'}}
    ci = {}
    for _ in range(75):
        runs = api('/actions/runs?' + urllib.parse.urlencode({'head_sha': target, 'event': 'push', 'per_page': 100}))['workflow_runs']
        for name, jobs_required in required.items():
            matches = [r for r in runs if r['name'] == name and r['head_sha'] == target]
            if matches:
                run = max(matches, key=lambda r: r['id'])
                if run['status'] == 'completed':
                    require(run['conclusion'] == 'success', 'CI failed: ' + name)
                    jobs = api('/actions/runs/' + str(run['id']) + '/jobs?per_page=100')['jobs']
                    verified_jobs(jobs, jobs_required)
                    ci[name] = {'run_id': run['id'], 'url': run['html_url'], 'source_git_sha': target,
                                'jobs': [{'name': j['name'], 'conclusion': j['conclusion']} for j in jobs]}
        if set(ci) == set(required):
            break
        time.sleep(8)
    require(set(ci) == set(required), 'Timed out waiting for exact-source CI')
    require(api('/branches/main')['commit']['sha'] == target, 'Main moved before release')
    subprocess.run([sys.executable, 'scripts/build_docs.py', '--check'], cwd=ROOT, check=True)
    prefix = 'AAE-Developer-Bible-1.2.2/'
    expected = {}
    for item in git('ls-tree', '-rz', target).split(b'\0'):
        if item:
            meta, name = item.split(b'\t', 1)
            mode, kind, sha = meta.decode().split()
            require(kind == 'blob' and mode in {'100644', '100755'}, 'Special source member not supported')
            expected[name.decode()] = (git('cat-file', 'blob', sha), int(mode, 8) & 0o777)
    assets = {'AAE-Developer-Bible-1.2.2.zip': git('archive', '--format=zip', '--prefix=' + prefix, target),
              'AAE-Developer-Bible-1.2.2.tar.gz': gzip.compress(git('-c', 'tar.umask=0022', 'archive', '--format=tar', '--prefix=' + prefix, target), mtime=0)}
    for name, data in assets.items():
        verify_archive(data, 'zip' if name.endswith('.zip') else 'tar', expected, prefix)
    evidence = {'schema_version': 1, 'version': '1.2.2', 'tag': TAG, 'commit': target,
                'tree': git('rev-parse', 'HEAD^{tree}').decode().strip(), 'ci': ci,
                'committed_generated_freshness': 'PASS', 'archive_tree_bytes_and_modes': 'PASS',
                'native_compilation': 'PROJECT-REPORTED: 13/13 syntax/type PASS on owner Mac at ' + BASE,
                'native_compilation_by_this_workflow': 'NOT_RUN',
                'owner_evidence': {'tested_source_git_sha': BASE, 'public_report_sha256': OWNER_REPORT_SHA256, 'origin': 'owner-supplied local report; only temporary paths redacted'},
                'ae_host_runtime': 'NOT_RUN', 'sdk_ci_provisioning': 'Required before changed-native runs; not established by this release',
                'archives': {n: {'sha256': hashlib.sha256(b).hexdigest(), 'bytes': len(b)} for n, b in assets.items()}}
    assets['native-compile-report.redacted.json'] = (ROOT / OWNER_EVIDENCE / 'native-compile-report.redacted.json').read_bytes()
    assets['native-evidence-provenance.json'] = (ROOT / OWNER_EVIDENCE / 'provenance.json').read_bytes()
    evidence['owner_evidence']['provenance_sha256'] = hashlib.sha256(assets['native-evidence-provenance.json']).hexdigest()
    assets['release-evidence.json'] = (json.dumps(evidence, indent=2, sort_keys=True) + '\n').encode()
    assets['SHA256SUMS.txt'] = ''.join(hashlib.sha256(b).hexdigest() + '  ' + n + '\n' for n, b in sorted(assets.items())).encode()
    def tag_commit(ref):
        obj = ref['object']
        if obj['type'] == 'tag':
            obj = api('/git/tags/' + obj['sha'])['object']
        require(obj['type'] == 'commit', 'Unexpected tag type')
        return obj['sha']
    ref = api('/git/ref/tags/' + TAG)
    if ref:
        require(tag_commit(ref) == target, 'Existing tag points elsewhere; never replace it')
    else:
        tag = api('/git/tags', {'tag': TAG, 'message': 'AAE Developer Bible 1.2.2', 'object': target, 'type': 'commit'})
        api('/git/refs', {'ref': 'refs/tags/' + TAG, 'sha': tag['sha']})
    release = api('/releases/tags/' + TAG)
    if release is None:
        import re
        body = (ROOT / 'RELEASE-1.2.2.md').read_text()
        body = re.sub(r'\]\(([^\s)]+)\)', lambda m: m[0] if ':' in m[1] or m[1].startswith('#') else '](https://github.com/' + REPO + '/blob/' + TAG + '/' + m[1] + ')', body)
        body += '\n\nExact release commit: `' + target + '`\n'
        release = api('/releases', {'tag_name': TAG, 'target_commitish': target, 'name': 'AAE Developer Bible v1.2.2 — SDK evidence', 'body': body, 'draft': True, 'prerelease': False})
    require(release['tag_name'] == TAG and not release['prerelease'], 'Unexpected release')
    listed = api('/releases/' + str(release['id']) + '/assets?per_page=100')
    require(len({a['name'] for a in listed}) == len(listed) and all(a['name'] in assets for a in listed), 'Unknown or duplicate assets; preserve and stop')
    for name, data in assets.items():
        existing = next((a for a in listed if a['name'] == name), None)
        if existing is None:
            require(release['draft'], 'Published release missing assets; do not mutate it')
            url = 'https://uploads.github.com/repos/' + REPO + '/releases/' + str(release['id']) + '/assets?' + urllib.parse.urlencode({'name': name})
            request = urllib.request.Request(url, data=data, headers={**headers, 'Content-Type': 'application/octet-stream'}, method='POST')
            with urllib.request.urlopen(request, timeout=60) as response:
                existing = json.load(response)
        require(existing['state'] == 'uploaded' and existing['size'] == len(data) and existing.get('digest') == 'sha256:' + hashlib.sha256(data).hexdigest(), 'Uploaded digest/size mismatch')
    require(api('/branches/main')['commit']['sha'] == target and tag_commit(api('/git/ref/tags/' + TAG)) == target, 'Publication identity moved')
    if release['draft']:
        release = api('/releases/' + str(release['id']), {'draft': False, 'make_latest': 'true'}, 'PATCH')
    require(not release['draft'] and not release['prerelease'], 'Not published stable')
    print(release['html_url'], target)


if __name__ == '__main__':
    main()
