#!/usr/bin/env python3

import tempfile
import unittest
from pathlib import Path

from scripts import host_cycle
from scripts import materialize_sdk_examples


class HostCycleSafetyTests(unittest.TestCase):
    def make_plugin(self, root: Path, name: str, marker: str) -> Path:
        plugin = root / name
        (plugin / "Contents").mkdir(parents=True)
        (plugin / "Contents" / "marker.txt").write_text(marker)
        return plugin

    def make_aerender(self, root: Path, body: str) -> Path:
        script = root / "aerender-mock"
        script.write_text("#!/usr/bin/env python3\n" + body)
        script.chmod(0o755)
        return script

    def test_success_commits_new_plugin_and_requires_output(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            src_root = root / "src"
            install_root = root / "install"
            src_root.mkdir()
            install_root.mkdir()

            plugin = self.make_plugin(src_root, "Test.plugin", "new")
            self.make_plugin(install_root, "Test.plugin", "old")
            project = root / "test.aep"
            project.write_text("fixture")
            output = root / "render.png"

            aerender = self.make_aerender(
                root,
                "import pathlib, sys\n"
                "out = pathlib.Path(sys.argv[sys.argv.index('-output') + 1])\n"
                "out.write_text('rendered')\n",
            )

            report = host_cycle.run_cycle(
                plugin,
                install_root,
                output,
                aerender=aerender,
                project=project,
                timeout_seconds=2,
            )

            self.assertEqual(report["install"]["status"], "committed")
            self.assertTrue(report["install"]["had_previous_install"])
            self.assertEqual(report["render"]["status"], "passed")
            self.assertEqual(
                (install_root / "Test.plugin" / "Contents" / "marker.txt").read_text(),
                "new",
            )
            self.assertEqual((plugin / "Contents" / "marker.txt").read_text(), "new")

    def test_nonzero_render_rolls_back_previous_plugin(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            src_root = root / "src"
            install_root = root / "install"
            src_root.mkdir()
            install_root.mkdir()

            plugin = self.make_plugin(src_root, "Test.plugin", "new")
            self.make_plugin(install_root, "Test.plugin", "old")
            project = root / "test.aep"
            project.write_text("fixture")
            output = root / "render.png"
            aerender = self.make_aerender(root, "raise SystemExit(7)\n")

            with self.assertRaises(host_cycle.HostCycleError) as cm:
                host_cycle.run_cycle(
                    plugin,
                    install_root,
                    output,
                    aerender=aerender,
                    project=project,
                    timeout_seconds=2,
                )

            report = cm.exception.report
            self.assertEqual(report["render"]["status"], "failed")
            self.assertEqual(report["render"]["returncode"], 7)
            self.assertTrue(report["install"]["rolled_back"])
            self.assertEqual(
                (install_root / "Test.plugin" / "Contents" / "marker.txt").read_text(),
                "old",
            )

    def test_timeout_rolls_back_previous_plugin(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            src_root = root / "src"
            install_root = root / "install"
            src_root.mkdir()
            install_root.mkdir()

            plugin = self.make_plugin(src_root, "Test.plugin", "new")
            self.make_plugin(install_root, "Test.plugin", "old")
            project = root / "test.aep"
            project.write_text("fixture")
            output = root / "render.png"
            aerender = self.make_aerender(
                root, "import time\ntime.sleep(1)\n"
            )

            with self.assertRaises(host_cycle.HostCycleError) as cm:
                host_cycle.run_cycle(
                    plugin,
                    install_root,
                    output,
                    aerender=aerender,
                    project=project,
                    timeout_seconds=0.05,
                )

            self.assertEqual(cm.exception.report["render"]["status"], "timeout")
            self.assertEqual(
                (install_root / "Test.plugin" / "Contents" / "marker.txt").read_text(),
                "old",
            )

    def test_missing_output_is_failure_and_rolls_back(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            src_root = root / "src"
            install_root = root / "install"
            src_root.mkdir()
            install_root.mkdir()

            plugin = self.make_plugin(src_root, "Test.plugin", "new")
            self.make_plugin(install_root, "Test.plugin", "old")
            project = root / "test.aep"
            project.write_text("fixture")
            output = root / "render.png"
            aerender = self.make_aerender(root, "raise SystemExit(0)\n")

            with self.assertRaises(host_cycle.HostCycleError) as cm:
                host_cycle.run_cycle(
                    plugin,
                    install_root,
                    output,
                    aerender=aerender,
                    project=project,
                    timeout_seconds=2,
                )

            self.assertEqual(cm.exception.report["render"]["status"], "missing_output")
            self.assertEqual(
                (install_root / "Test.plugin" / "Contents" / "marker.txt").read_text(),
                "old",
            )

    def test_source_destination_collision_is_rejected_without_deletion(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            install_root = root / "install"
            install_root.mkdir()
            plugin = self.make_plugin(install_root, "Test.plugin", "only-copy")
            output = root / "render.png"

            with self.assertRaises(host_cycle.HostCycleError):
                host_cycle.run_cycle(plugin, install_root, output)

            self.assertEqual(
                (plugin / "Contents" / "marker.txt").read_text(), "only-copy"
            )


class MaterializeSafetyTests(unittest.TestCase):
    def make_examples(self, root: Path, source_name: str = "Panelator.cpp") -> Path:
        examples = root / "Examples"
        (examples / "Headers").mkdir(parents=True)
        (examples / "Headers" / "AE_GeneralPlug.h").write_text("header")
        sample = examples / "AEGP" / "Panelator"
        sample.mkdir(parents=True)
        (sample / source_name).write_text("int sample = 1;")
        return examples

    def test_materialize_replaces_target_without_touching_source(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            examples = self.make_examples(root)
            source = examples / "AEGP" / "Panelator"
            out = root / "out"
            target = out / "native-panel"
            target.mkdir(parents=True)
            (target / "old.txt").write_text("old")

            written = materialize_sdk_examples.materialize(
                examples, out, ["native-panel"]
            )

            self.assertEqual(written, [target.resolve()])
            self.assertTrue((source / "Panelator.cpp").exists())
            self.assertTrue((target / "Panelator.cpp").exists())
            self.assertFalse((target / "old.txt").exists())
            self.assertTrue((target / "AAE-BIBLE-BASE.txt").exists())

    def test_overlapping_source_and_destination_is_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            examples = self.make_examples(root)
            source = examples / "AEGP" / "Panelator"

            with self.assertRaises(ValueError):
                materialize_sdk_examples.materialize(
                    examples, source, ["native-panel"]
                )

            self.assertTrue((source / "Panelator.cpp").exists())

    def test_partial_sample_fails_before_existing_target_is_changed(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            examples = self.make_examples(root, "Wrong.cpp")
            out = root / "out"
            target = out / "native-panel"
            target.mkdir(parents=True)
            (target / "old.txt").write_text("keep")

            with self.assertRaises(ValueError):
                materialize_sdk_examples.materialize(
                    examples, out, ["native-panel"]
                )

            self.assertEqual((target / "old.txt").read_text(), "keep")


if __name__ == "__main__":
    unittest.main()
