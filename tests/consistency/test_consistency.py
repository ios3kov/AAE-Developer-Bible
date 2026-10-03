import importlib.util
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
def module(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / 'scripts' / (name + '.py'))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
check = module('check_docs_consistency')
build = module('build_docs')

class ConsistencyTests(unittest.TestCase):
    def test_current_repository(self):
        self.assertEqual(check.check(), [])

    def test_prefix_and_exclusive_envelopes(self):
        valid = {'protocol':1, 'requestId':'r1', 'command':'renameSelected', 'payload':{'prefix':'x'}}
        check.validate_envelope(valid)
        for mutation in [dict(valid, protocol=2), dict(valid, payload={'prefix':4}), dict(valid, payload={'suffix':'x'}),
                         {'protocol':1, 'requestId':'r1', 'ok':True, 'result':{'changed':0}, 'error':{}}]:
            with self.assertRaises(ValueError): check.validate_envelope(mutation)

    def test_nested_nav_removal_is_detected(self):
        texts = {p: (ROOT / p).read_text() for p in ['mkdocs.yml','NAVIGATION.md','CHAPTER-COMPLETION-TRACKER.md']}
        self.assertEqual(check.navigation_errors(texts), [])
        texts['mkdocs.yml'] = texts['mkdocs.yml'].replace('      - "Auxiliary Channels": 02-EFFECT-PLUGINS/08-AUXILIARY-CHANNELS.md\n', '')
        self.assertTrue(any('08-AUXILIARY' in x for x in check.navigation_errors(texts)))

    def test_evidence_boundary_and_unrecorded_claim(self):
        registry = {'required_boundaries':{'page.md':'RUNTIME-NOT-CLAIMED'}}
        self.assertEqual(check.evidence_errors({'page.md':'Historical PASS\nRUNTIME-NOT-CLAIMED'}, registry), [])
        self.assertTrue(check.evidence_errors({'page.md':'CURRENT-RUNTIME: PASS'}, registry))
        self.assertTrue(check.evidence_errors({'page.md':'removed'}, registry))

    def test_digest_relocatable_sensitive_and_output_independent(self):
        old = build.ROOT
        try:
            with tempfile.TemporaryDirectory() as a, tempfile.TemporaryDirectory() as b:
                for d in [a,b]:
                    Path(d,'README.md').write_text('source')
                    Path(d,build.MASTER).write_text(d)
                    Path(d,'MANIFEST.sha256').write_text(d)
                paths = list(map(Path,['README.md',build.MASTER,'MANIFEST.sha256']))
                build.ROOT = Path(a); first = build.source_digest(paths)
                build.ROOT = Path(b); self.assertEqual(first,build.source_digest(paths))
                Path(b,'README.md').write_text('changed'); self.assertNotEqual(first,build.source_digest(paths))
                Path(b,'README.md').unlink()
                with self.assertRaises(FileNotFoundError): build.source_digest(paths)
        finally: build.ROOT = old

    def test_generated_drift_detected_and_repeated_generation_stable(self):
        old = build.ROOT
        try:
            with tempfile.TemporaryDirectory() as td:
                build.ROOT = Path(td); Path(td,'README.md').write_text('# source')
                files = [Path('README.md'),Path(build.MASTER),Path('MANIFEST.sha256')]
                first = build.generated(files)
                for name,value in first.items(): Path(td,name).write_text(value)
                self.assertEqual(first,build.generated(files))
                Path(td,'README.md').write_text('# changed')
                self.assertNotEqual(first,build.generated(files))
        finally: build.ROOT = old

    def test_source_staging_and_frozen_check_lanes(self):
        old = build.ROOT
        try:
            with tempfile.TemporaryDirectory() as source, tempfile.TemporaryDirectory() as stage:
                build.ROOT = Path(source); Path(source,'README.md').write_text('# source')
                with patch.object(build, 'tracked_files', return_value=[Path('README.md')]):
                    with patch('sys.argv',['build_docs','--output-root',stage]):
                        self.assertEqual(build.main(),0)
                    self.assertFalse(Path(source,build.MASTER).exists())
                    self.assertTrue(Path(stage,'docs',build.MASTER).is_file())
                    with patch('sys.argv',['build_docs','--check','--output-root',stage]):
                        self.assertEqual(build.main(),0)
                        for name in build.GENERATED:
                            p = Path(stage,name); original = p.read_text()
                            p.write_text('tampered')
                            self.assertEqual(build.main(),1)
                            p.write_text(original)
        finally: build.ROOT = old

    def test_lane_classification_does_not_reject_source_pr_drift(self):
        import sys
        with patch.dict(sys.modules, {'build_docs':build}):
            lane = module('docs_lane')
        self.assertEqual(lane.classify(['README.md','MANIFEST.sha256']), 'source')
        self.assertEqual(lane.classify(['MANIFEST.sha256',build.MASTER]), 'frozen')
        self.assertEqual(lane.classify([]), 'source')

    def test_chapter_schema_divergence_is_detected(self):
        texts = {p:(ROOT / p).read_text() for p in check.CEP_PAGES}
        self.assertEqual(check.cep_errors(texts), [])
        path = check.CEP_PAGES[0]
        texts[path] = texts[path].replace('"prefix": "Bible_"', '"suffix": "Bible_"')
        self.assertTrue(any(path in error for error in check.cep_errors(texts)))
