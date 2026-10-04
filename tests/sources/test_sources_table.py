import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location('source_table', ROOT/'scripts/generate_sources_table.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


class SourceTableTests(unittest.TestCase):
    def setUp(self):
        self.data = m.load_registry()

    def rejected(self, mutate):
        data = copy.deepcopy(self.data)
        mutate(data)
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp)/'registry.json'
            path.write_text(json.dumps(data))
            with self.assertRaises(ValueError):
                m.load_registry(path)

    def test_sdk_identity_cannot_be_abbreviated(self):
        self.rejected(lambda d: d['claims'][0].update(identity='afec075...'))

    def test_missing_boundary_and_review_record_rejected(self):
        self.rejected(lambda d: d['claims'][0].update(host=''))
        self.rejected(lambda d: d['claims'][0].update(record='../../outside.md'))

    def test_documentation_ci_cannot_be_native_evidence(self):
        self.rejected(lambda d: d['regenerations'][0].update(evidence='SDK-SOURCE-REVIEW'))
        self.rejected(lambda d: d['claims'][0].update(evidence='VALIDATED'))

    def test_invalid_date_or_provenance_digest_rejected(self):
        self.rejected(lambda d: d['claims'][0].update(review_date='2026-02-30'))
        self.rejected(lambda d: d['regenerations'][0].update(content_sha256='d8e0...'))

    def test_stale_table_check_fails_without_overwriting(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp)/'table.md'
            path.write_text('stale')
            r = subprocess.run(['python3',str(ROOT/'scripts/generate_sources_table.py'),'--check','--output',str(path)],capture_output=True)
            self.assertEqual(r.returncode,1)
            self.assertEqual(path.read_text(),'stale')
            path.write_text(m.render(self.data))
            r = subprocess.run(['python3',str(ROOT/'scripts/generate_sources_table.py'),'--check','--output',str(path)],capture_output=True)
            self.assertEqual(r.returncode,0,r.stderr)


if __name__ == '__main__':
    unittest.main()
