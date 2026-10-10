"""Negative execution controls for the actual docs/SDK CI boundaries; no AE claims."""
import importlib.util
import json
import os
from pathlib import Path
import shutil
import stat
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
import zipfile
import yaml

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from scripts import ci_native_gate as native
from scripts.check_native import sdk_header_manifest


def run(*args, cwd=None):
    return subprocess.run(list(args), cwd=cwd, capture_output=True, text=True, timeout=45)


def initialize(root):
    for args in [('init', '-q'), ('config', 'user.name', 'CI fixture'),
                 ('config', 'user.email', 'ci@example.invalid'), ('config', 'commit.gpgsign', 'false')]:
        subprocess.run(['git', '-C', str(root), *args], check=True, capture_output=True)


def commit(root):
    subprocess.run(['git', '-C', str(root), 'add', '.'], check=True)
    subprocess.run(['git', '-C', str(root), 'commit', '-qm', 'fixture'], check=True)
    return native.git(root, 'rev-parse', 'HEAD').decode().strip()


class DocumentationGates(unittest.TestCase):
    def test_freshness_runs_before_regeneration_without_lane_condition(self):
        workflow = yaml.safe_load((ROOT / '.github/workflows/validate.yml').read_text())
        steps = workflow['jobs']['portable-checks']['steps']
        checks = [(i, s) for i, s in enumerate(steps) if s.get('run', '').strip() == 'python scripts/build_docs.py --check']
        self.assertEqual(len(checks), 1)
        index, check = checks[0]
        self.assertNotIn('if', check)
        self.assertNotIn('continue-on-error', check)
        generated = [i for i, s in enumerate(steps) if 'python scripts/build_docs.py --output-root' in s.get('run', '')]
        self.assertTrue(generated)
        self.assertLess(index, min(generated))
        config = yaml.safe_load((ROOT / 'mkdocs.yml').read_text())
        self.assertEqual(config['validation']['links']['anchors'], 'warn')
        regen = yaml.safe_load((ROOT / '.github/workflows/regenerate-effects-catalog.yml').read_text())
        self.assertEqual(regen['permissions'], {'contents': 'read'})
        self.assertNotIn('contents: write', (ROOT / '.github/workflows/regenerate-effects-catalog.yml').read_text())
        self.assertNotIn('git push', (ROOT / '.github/workflows/regenerate-effects-catalog.yml').read_text())

    def test_real_cli_rejects_source_generated_and_mixed_drift_without_repair(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / 'scripts').mkdir()
            shutil.copyfile(ROOT / 'scripts/build_docs.py', root / 'scripts/build_docs.py')
            (root / '.gitignore').write_text('docs/\nsite/\n')
            (root / 'README.md').write_text('# Source\n')
            initialize(root)
            command = [sys.executable, str(root / 'scripts/build_docs.py')]
            initial = run(*command, cwd=root)
            self.assertEqual(initial.returncode, 0, initial.stdout + initial.stderr)
            commit(root)
            self.assertEqual(run(*command, '--check', cwd=root).returncode, 0)
            snapshot = {p: (root / p).read_bytes() for p in ['README.md', 'MASTER-AE-DEVELOPER-BIBLE.md', 'MANIFEST.sha256']}
            for names in [('README.md',), ('MASTER-AE-DEVELOPER-BIBLE.md',), ('MANIFEST.sha256',),
                          ('README.md', 'MANIFEST.sha256')]:
                for p, data in snapshot.items():
                    (root / p).write_bytes(data)
                for p in names:
                    with (root / p).open('ab') as f:
                        f.write(b'\nstale fixture\n')
                before = {p: (root / p).read_bytes() for p in snapshot}
                result = run(*command, '--check', cwd=root)
                self.assertNotEqual(result.returncode, 0, names)
                self.assertIn('Stale generated files:', result.stdout)
                self.assertEqual(before, {p: (root / p).read_bytes() for p in snapshot})
            repaired = run(*command, cwd=root)
            self.assertEqual(repaired.returncode, 0, repaired.stderr)
            self.assertEqual(run(*command, '--check', cwd=root).returncode, 0)

    def test_actual_mkdocs_strict_accepts_explicit_ids_and_rejects_broken_targets(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            docs = root / 'docs'
            docs.mkdir()
            actual = yaml.safe_load((ROOT / 'mkdocs.yml').read_text())
            config = {'site_name': 'CI fixture', 'docs_dir': 'docs', 'site_dir': 'site',
                      'validation': actual['validation'], 'plugins': [], 'nav': ['index.md', 'target.md']}
            (root / 'mkdocs.yml').write_text(yaml.safe_dump(config))
            (docs / 'target.md').write_text('<a id="stable"></a>\n\n# Русский заголовок\n', encoding='utf-8')
            command = [sys.executable, '-m', 'mkdocs', 'build', '--strict', '-f', str(root / 'mkdocs.yml')]
            for target, good in [('target.md#stable', True), ('target.md#absent', False), ('missing.md', False)]:
                (docs / 'index.md').write_text('# Test\n\n[link](' + target + ')\n')
                result = run(*command, cwd=root)
                self.assertEqual(result.returncode == 0, good, result.stdout + result.stderr)
            (docs / 'index.md').write_text('[link](target.md#stable)\n')
            (docs / 'target.md').write_text('# Anchor removed\n')
            self.assertNotEqual(run(*command, cwd=root).returncode, 0)

    def test_all_six_shared_aliases_are_explicit(self):
        expected = {'NAVIGATION.md': ['route-effect', 'route-native', 'route-automation'],
                    '15-COMMUNICATION/05-SCRIPT-TO-AE.md': ['bridgetalk'],
                    '00-START-HERE/02-ENVIRONMENT-MATRIX.md': ['host-snapshot-2026-10-08'],
                    '06-SCRIPTING/01-OBJECT-MODEL.md': ['extendscript-files-runtime']}
        for path, names in expected.items():
            text = (ROOT / path).read_text()
            for name in names:
                self.assertEqual(text.count('<a id="' + name + '"></a>'), 1, (path, name))


class NativeGateTests(unittest.TestCase):
    def test_classification_keeps_docs_separate_and_covers_native_inputs(self):
        self.assertEqual(native.affected(['VERIFICATION.md', 'mkdocs.yml', 'scripts/ci_native_gate.py']), [])
        paths = ['16-WORKING-TEMPLATES/x/a.cpp', '19-NATIVE-CODE-FOUNDATION/code/a.h',
                 'scripts/check_native.py', '18-SDK-HEADER-TOOLS/run-macos.sh',
                 '18-SDK-HEADER-TOOLS/tools/verify_required_contracts.py',
                 '18-SDK-HEADER-TOOLS/sdk25.6-required-contracts.json']
        self.assertEqual(native.affected(paths), sorted(paths))

    def test_deleted_and_renamed_native_file_cannot_disappear_from_scope(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            initialize(root)
            folder = root / '16-WORKING-TEMPLATES'
            folder.mkdir()
            (folder / 'old.cpp').write_text('int x;\n')
            base = commit(root)
            (folder / 'old.cpp').rename(root / 'lesson.md')
            head = commit(root)
            self.assertIn('16-WORKING-TEMPLATES/old.cpp', native.affected(native.changed_paths(root, base, head)))
            with self.assertRaises(ValueError):
                native.changed_paths(root, 'main', head)
            with self.assertRaises(subprocess.CalledProcessError):
                native.changed_paths(root, 'f' * 40, head)

    def test_missing_licensed_sdk_is_blocked_before_network(self):
        with tempfile.TemporaryDirectory() as td, patch.dict(os.environ, {}, clear=True):
            with self.assertRaisesRegex(ValueError, 'Licensed SDK unavailable'):
                native.acquire_sdk(td)

    def test_wrong_sdk_pin_and_real_compiler_error_propagate(self):
        with tempfile.TemporaryDirectory() as td:
            temp = Path(td)
            root = temp / 'source'
            root.mkdir()
            initialize(root)
            examples = temp / 'SDK/Examples'
            (examples / 'Headers').mkdir(parents=True)
            (examples / 'Util').mkdir()
            (examples / 'Headers/AE_Effect.h').write_text('// synthetic pin fixture, not Adobe SDK\n')
            _, digest = sdk_header_manifest(examples)
            runner = root / '18-SDK-HEADER-TOOLS/run-macos.sh'
            runner.parent.mkdir()
            runner.write_text('#!/bin/bash\nset -euo pipefail\nexec c++ -std=c++17 -fsyntax-only sample.cpp\n')
            source = root / 'sample.cpp'
            source.write_text('#error intentional_native_regression\n')
            commit(root)
            with self.assertRaisesRegex(ValueError, 'identity mismatch'):
                native.run_sdk(root, examples, '0' * 64)
            with self.assertRaisesRegex(ValueError, 'must pin'):
                native.run_sdk(root, examples, '')
            self.assertNotEqual(native.run_sdk(root, examples, digest), 0)
            source.write_text('int valid_fixture = 1;\n')
            commit(root)
            self.assertEqual(native.run_sdk(root, examples, digest), 0)

    def test_archive_rejects_escaping_symlink_and_duplicate_members(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            for number, names in enumerate([['../escaped.h'], ['/absolute.h'], ['a.h', 'A.h'], ['link']]):
                archive = root / f'{number}.zip'
                with zipfile.ZipFile(archive, 'w') as z:
                    for name in names:
                        info = zipfile.ZipInfo(name)
                        if name == 'link':
                            info.external_attr = (stat.S_IFLNK | 0o777) << 16
                        z.writestr(info, b'x')
                with self.assertRaises(ValueError):
                    native.extract_sdk(archive, root / f'out{number}')
            self.assertFalse((root / 'escaped.h').exists())


if __name__ == '__main__':
    unittest.main()
