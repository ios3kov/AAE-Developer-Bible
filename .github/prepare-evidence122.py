"""Prepare exact public-evidence Git blobs only; no refs/tags/releases are modified.

The compressed transport is the inspected redacted report, not executable SDK content.
"""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import urllib.request
import zlib

BASE = '0ea8131bcb599fc52df5c7cf6d1d7057bf4d1352'
REPO = 'ios3kov/AAE-Developer-Bible'
TEMP = ['.github/prepare-evidence122.py', '.github/workflows/prepare-evidence122.yml', '.github/evidence122.report.zlib']
assert os.environ['GITHUB_REPOSITORY'] == REPO
assert os.environ['GITHUB_REF'] == 'refs/heads/release/bible-1.2.2-evidence'


def git(*args):
    return subprocess.check_output(['git', *args], timeout=60)


def replace(text, old, new):
    assert text.count(old) == 1, 'Unexpected replacement count: ' + old[:80]
    return text.replace(old, new, 1)


def write(path, text):
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding='utf-8')


seed = {'tests/ci_gates/test_owner_evidence.py', 'NATIVE-SDK-OWNER-CHECK-2026-10-10.md', 'RELEASE-1.2.2.md', 'evidence/native-sdk-2026-10-10/provenance.json'}
assert set(git('diff', '--name-only', BASE, 'HEAD').decode().splitlines()) == set(TEMP) | seed
public = zlib.decompress(Path(TEMP[2]).read_bytes())
assert len(public) == 13372 and hashlib.sha256(public).hexdigest() == 'bd396e6b12f9b7f989a8903863a3b83018fce642e9167d1e30de5fc8b9a9bfbe'
write('evidence/native-sdk-2026-10-10/native-compile-report.redacted.json', public.decode())
for name in ('README.md', 'VERIFICATION.md', 'CHANGELOG.md', 'CI-GATES.md', 'NAVIGATION.md'):
    assert Path(name).read_bytes() == git('show', BASE + ':' + name), name
p = Path('README.md')
write(p, replace(p.read_text(), '# AE Developer Bible\n', '# AE Developer Bible\n\nДополнение **1.2.2 — 2026-10-10**: [SDK-проверка на Mac владельца](NATIVE-SDK-OWNER-CHECK-2026-10-10.md) — 13 compiler syntax/type проверок PASS для коммита `0ea8131`. [Границы и выпуск](RELEASE-1.2.2.md). Проверка внутри AE и доступ GitHub CI к SDK этим результатом не подтверждаются.\n'))
p = Path('VERIFICATION.md')
write(p, replace(p.read_text(), '# Verification purpose\n', '# Verification purpose\n\n## Owner-supplied SDK compiler evidence — 2026-10-10\n\n[Запись и отчёт](NATIVE-SDK-OWNER-CHECK-2026-10-10.md): 13/13 syntax/type проверок прошли на Mac владельца для clean source `0ea8131bcb599fc52df5c7cf6d1d7057bf4d1352`. Это PROJECT-REPORTED локальный результат, не новый прогон CI/AE. Дата и SDKROOT-workaround сообщены владельцем; точное значение SDKROOT не записано. История ниже сохраняет свой исходный scope.\n'))
p = Path('CHANGELOG.md')
write(p, replace(p.read_text(), '# Changelog\n', '# Changelog\n\n## 1.2.2 — 2026-10-10 — owner-supplied SDK evidence\n\nДобавлены [owner-supplied native SDK evidence](NATIVE-SDK-OWNER-CHECK-2026-10-10.md), машинный отчёт без временных путей и его provenance/hash. 13 compiler checks PASS относятся к source `0ea8131bcb599fc52df5c7cf6d1d7057bf4d1352`, не автоматически к SHA нового релиза. Обновлены ссылки README/VERIFICATION. Native исходники, compiler drivers и архивы v1.2.1 не изменены. [Описание выпуска](RELEASE-1.2.2.md).\n'))
p = Path('evidence/native-sdk-2026-10-10/provenance.json')
provenance = json.loads(p.read_text())
provenance['publication'] = 'Included in the documentation supplement; actual tag, containing source SHA and publication status are recorded separately in GitHub Release v1.2.2 and release-evidence.json. Tested source SHA is unchanged.'
write(p, json.dumps(provenance, ensure_ascii=False, indent=2) + '\n')
p = Path('CI-GATES.md')
write(p, replace(p.read_text(), '# CI gates and publication — 1.2.1\n', '# CI gates and publication — 1.2.1\n\nEvidence supplement 1.2.2: [owner-run SDK result](NATIVE-SDK-OWNER-CHECK-2026-10-10.md) records 13/13 compiler checks on the exact v1.2.1 source. This local observation does not provision GitHub CI. The SDK-access requirements below remain applicable; the original 1.2.1 release statements retain their date/scope.\n'))
p = Path('NAVIGATION.md')
write(p, replace(p.read_text(), '# Navigation\n', '# Navigation\n\n[SDK evidence on the owner\'s Mac](NATIVE-SDK-OWNER-CHECK-2026-10-10.md) · [Evidence release 1.2.2](RELEASE-1.2.2.md).\n'))
write('RELEASE-1.2.2.md', '''# AAE Developer Bible v1.2.2 — SDK evidence

В саму книгу и архивы включены [результаты проверки на Mac владельца](NATIVE-SDK-OWNER-CHECK-2026-10-10.md), [машинный отчёт без временных путей](evidence/native-sdk-2026-10-10/native-compile-report.redacted.json) и [его происхождение/хеши](evidence/native-sdk-2026-10-10/provenance.json). README, VERIFICATION, навигация и changelog связывают эти материалы; MASTER/MANIFEST обновлены вместе с исходными документами.

## Что подтверждено отчётом

PROJECT-REPORTED: 13 проверок синтаксиса и типов C++ прошли, ошибок 0, на clean source `0ea8131bcb599fc52df5c7cf6d1d7057bf4d1352` (v1.2.1). Apple clang 21.0.0, target arm64-apple-darwin25.6.0; Adobe SDK 25.6 build 61, Headers + Util manifest содержит 81 header. Это 10 основных исходников, два forwarding entry files и один foundation-header probe, не 13 независимых реализаций.

Публичный JSON сохраняет все результаты и per-source hashes; изменены только временные пути. Исходный отчёт и SDK не публикуются. Отдельно записаны предыдущий неуспешный запуск и успешный повтор с явно переданным SDKROOT. Точное значение SDKROOT в исходном JSON отсутствует и не выдумывается.

## Границы и публикация

Native-код и существующие SDK/compiler-драйверы этим дополнением не изменяются. Проверенный SHA в отчёте не заменяется SHA документационного релиза: новый запуск компиляции/AE не заявляется. Link, PiPL/load, After Effects, MFR/GPU runtime, Windows и [доступ SDK из GitHub CI](CI-GATES.md) этим отчётом не подтверждены.

Издатель проверяет неизменность native-входов, целостность отчёта/provenance, свежесть сохранённых MASTER/MANIFEST и успешные проверки точного итогового коммита. Архивы сверяются с Git tree, загруженные файлы — по SHA-256. Тег v1.2.2, точный release SHA, результаты CI и контрольные суммы устанавливаются опубликованным GitHub Release и `release-evidence.json`, а не заранее этой записью. v1.2.1 и его assets не заменяются.
''')

old = Path('scripts/publish_ci_patch.py').read_bytes()
assert hashlib.sha1(b'blob ' + str(len(old)).encode() + b'\0' + old).hexdigest() == '66cc70ca437d6193e98d73aaa319301579b55ad5'
s = old.decode().replace('1.2.1', '1.2.2')
s = replace(s, "BASE = 'e796313877b996a0e8701341e682915c35c6ce94'", "BASE = '" + BASE + "'")
s = replace(s, "    require(not affected(changed_paths(ROOT, BASE, target)), 'This patch authorizes no changed native SDK inputs')", "    require(not affected(changed_paths(ROOT, BASE, target)), 'This patch authorizes no changed native SDK inputs')\n    validate_owner_evidence(ROOT)\n    require(not git('status', '--porcelain').strip(), 'Release checkout must be clean')")
s = replace(s, "'native_compilation': 'NOT_APPLICABLE: native inputs unchanged from v1.2.0',", "'native_compilation': 'PROJECT-REPORTED: 13/13 syntax/type PASS on owner Mac at ' + BASE,\n                'native_compilation_by_this_workflow': 'NOT_RUN',\n                'owner_evidence': {'tested_source_git_sha': BASE, 'public_report_sha256': OWNER_REPORT_SHA256, 'origin': 'owner-supplied local report; only temporary paths redacted'},")
s = replace(s, "    assets['release-evidence.json'] =", "    assets['native-compile-report.redacted.json'] = (ROOT / OWNER_EVIDENCE / 'native-compile-report.redacted.json').read_bytes()\n    assets['native-evidence-provenance.json'] = (ROOT / OWNER_EVIDENCE / 'provenance.json').read_bytes()\n    evidence['owner_evidence']['provenance_sha256'] = hashlib.sha256(assets['native-evidence-provenance.json']).hexdigest()\n    assets['release-evidence.json'] =")
s = replace(s, "        body = (ROOT / 'RELEASE-1.2.2.md').read_text().replace('](CI-GATES.md)', '](https://github.com/' + REPO + '/blob/' + TAG + '/CI-GATES.md)')", "        import re\n        body = (ROOT / 'RELEASE-1.2.2.md').read_text()\n        body = re.sub(r'\\]\\(([^\\s)]+)\\)', lambda m: m[0] if ':' in m[1] or m[1].startswith('#') else '](https://github.com/' + REPO + '/blob/' + TAG + '/' + m[1] + ')', body)")
s = replace(s, "'name': 'AAE Developer Bible v1.2.2 — CI gates'", "'name': 'AAE Developer Bible v1.2.2 — SDK evidence'")
helper = '''OWNER_EVIDENCE = 'evidence/native-sdk-2026-10-10'
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


'''
s = replace(s, 'def main():\n', helper + 'def main():\n')
write('scripts/publish_sdk_evidence.py', s)
w = Path('.github/workflows/release-1.2.1.yml').read_text().replace('1.2.1', '1.2.2').replace('scripts/publish_ci_patch.py', 'scripts/publish_sdk_evidence.py')
write('.github/workflows/release-1.2.2.yml', w)

from importlib.util import spec_from_file_location, module_from_spec
spec = spec_from_file_location('evidence_publisher', 'scripts/publish_sdk_evidence.py')
module = module_from_spec(spec)
spec.loader.exec_module(module)
report = module.validate_owner_evidence(Path.cwd())
for entry in report['results']:
    if not entry['source'].startswith('<generated>'):
        data = git('show', BASE + ':' + entry['source'])
        assert hashlib.sha256(data).hexdigest() == entry['source_sha256'], entry['source']

v = Path('.github/workflows/validate.yml')
assert v.read_bytes() == git('show', BASE + ':' + str(v))
assert 'fetch-depth: 2' in v.read_text()
write(v, v.read_text().replace('fetch-depth: 2', 'fetch-depth: 0'))

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

paths = set(git('diff', '--name-only', BASE).decode().splitlines())
paths.update(git('ls-files', '--others', '--exclude-standard').decode().splitlines())
paths.difference_update(TEMP)
entries = []
headers = {'Authorization': 'Bearer ' + os.environ['GH_TOKEN'], 'Accept': 'application/vnd.github+json'}
for name in sorted(paths):
    data = Path(name).read_bytes()
    payload = json.dumps({'content': data.decode('utf-8'), 'encoding': 'utf-8'}).encode()
    request = urllib.request.Request('https://api.github.com/repos/' + REPO + '/git/blobs', data=payload, headers=headers, method='POST')
    with urllib.request.urlopen(request, timeout=60) as response:
        result = json.load(response)
    expected = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
    assert result['sha'] == expected, 'Uploaded blob mismatch'
    original = git('ls-tree', BASE, '--', name).decode().split()
    entries.append({'path': name, 'mode': original[0] if original else '100644', 'type': 'blob', 'sha': expected})
entries += [{'path': name, 'mode': '100644', 'type': 'blob', 'sha': None} for name in TEMP]
print('PREPARED_ENTRIES=' + json.dumps(entries))
print('Only evidence/docs/publication tooling prepared; SDK, source ref, old releases and secrets unchanged.')
