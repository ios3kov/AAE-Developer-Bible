"""Historical owner evidence integrity; no fresh Adobe SDK or AE execution."""
import hashlib
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from scripts import publish_sdk_evidence as pub


class OwnerEvidenceTests(unittest.TestCase):
    def test_received_report_and_provenance_match(self):
        report = pub.validate_owner_evidence(ROOT)
        self.assertEqual(report['kind'], 'native-syntax-type-check')
        self.assertEqual(report['sdk']['header_count'], 81)
        self.assertEqual(report['sdk']['header_manifest_sha256'], '796b373fb93fe857d59b6ecd78ec2c23298b78fb4648046e7a7d401687d1860c')
        for entry in report['results']:
            self.assertIn('-fsyntax-only', entry['command'])
            self.assertIn('-std=c++17', entry['command'])

    def test_sources_match_the_tested_commit_not_a_future_commit(self):
        report = pub.validate_owner_evidence(ROOT)
        for entry in report['results']:
            if entry['source'] == '<generated>/foundation.cpp':
                data = ''.join('#include "' + name + '"\n' for name in (
                    'AEConfig.h', 'PicaSuiteRef.h', 'AegpOwners.h', 'UndoScope.h',
                    'HostCallbackGuard.h', 'BibleAegpCommon.h')).encode()
            else:
                data = subprocess.check_output(['git', 'show', pub.BASE + ':' + entry['source']], cwd=ROOT, timeout=20)
            self.assertEqual(hashlib.sha256(data).hexdigest(), entry['source_sha256'])

    def test_changed_report_or_provenance_is_rejected(self):
        folder = ROOT / pub.OWNER_EVIDENCE
        for name in ('native-compile-report.redacted.json', 'provenance.json'):
            with tempfile.TemporaryDirectory() as temp:
                out = Path(temp) / pub.OWNER_EVIDENCE
                out.mkdir(parents=True)
                for source in folder.iterdir():
                    (out / source.name).write_bytes(source.read_bytes())
                item = json.loads((out / name).read_text())
                if name.startswith('native-compile'):
                    item['summary']['failed'] = 1
                else:
                    item['tested_source_git_sha'] = '0' * 40
                (out / name).write_text(json.dumps(item))
                with self.assertRaises(RuntimeError):
                    pub.validate_owner_evidence(Path(temp))

    def test_publisher_remains_version_scoped_and_does_not_change_tested_identity(self):
        self.assertEqual(pub.TAG, 'v1.2.2')
        self.assertEqual(pub.BASE, '0ea8131bcb599fc52df5c7cf6d1d7057bf4d1352')
        source = (ROOT / 'scripts/publish_sdk_evidence.py').read_text()
        self.assertIn('validate_owner_evidence(ROOT)', source)
        self.assertIn("'native_compilation_by_this_workflow': 'NOT_RUN'", source)
        self.assertIn("assets['native-compile-report.redacted.json']", source)
        required = {'docs', 'mac'}
        for jobs in ([], [{'name': 'docs', 'status': 'completed', 'conclusion': 'success'}],
                     [{'name': n, 'status': 'completed', 'conclusion': 'skipped'} for n in required]):
            with self.assertRaises(RuntimeError):
                pub.verified_jobs(jobs, required)

    def test_release_archives_reject_modified_evidence(self):
        expected = {'report.json': (b'owner-evidence', 0o644)}
        output = io.BytesIO()
        with zipfile.ZipFile(output, 'w') as archive:
            info = zipfile.ZipInfo('release/report.json')
            info.external_attr = 0o644 << 16
            archive.writestr(info, b'modified')
        with self.assertRaises(RuntimeError):
            pub.verify_archive(output.getvalue(), 'zip', expected, 'release/')


if __name__ == '__main__':
    unittest.main()
