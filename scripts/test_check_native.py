#!/usr/bin/env python3

import importlib.util
import tempfile
import unittest
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
TOOL = HERE / "check_native.py"
spec = importlib.util.spec_from_file_location("check_native", TOOL)
check_native = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = check_native
spec.loader.exec_module(check_native)


class CheckNativeTests(unittest.TestCase):
    def test_compiler_style_auto_detection(self):
        self.assertEqual(check_native.compiler_style("clang++", "auto"), "clang")
        self.assertEqual(check_native.compiler_style("/tmp/cl.exe", "auto"), "msvc")
        self.assertEqual(check_native.compiler_style("anything", "msvc"), "msvc")

    def test_clang_command_separates_sdk_and_project_includes(self):
        source = Path("/repo/test.cpp")
        cmd = check_native.build_compile_command(
            "clang",
            "clang++",
            [Path("/sdk/Headers")],
            [Path("/repo/include")],
            source,
        )
        self.assertIn("-Werror", cmd)
        self.assertEqual(cmd[cmd.index("-isystem") + 1], "/sdk/Headers")
        self.assertEqual(cmd[cmd.index("-I") + 1], "/repo/include")
        self.assertEqual(cmd[-1], str(source))

    def test_msvc_command_uses_external_sdk_headers(self):
        source = Path("C:/repo/test.cpp")
        cmd = check_native.build_compile_command(
            "msvc",
            "cl.exe",
            [Path("C:/sdk/Headers")],
            [Path("C:/repo/include")],
            source,
        )
        self.assertIn("/WX", cmd)
        self.assertIn("/Zs", cmd)
        self.assertIn("/external:IC:/sdk/Headers", cmd)
        self.assertIn("/IC:/repo/include", cmd)
        self.assertEqual(cmd[-1], str(source))

    def test_sdk_header_manifest_is_deterministic_and_sensitive(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            headers = root / "Headers"
            util = root / "Util"
            headers.mkdir()
            util.mkdir()
            (headers / "AE_Effect.h").write_text("one", encoding="utf-8")
            (util / "AEGP_SuiteHandler.h").write_text("two", encoding="utf-8")

            count1, digest1 = check_native.sdk_header_manifest(root)
            count2, digest2 = check_native.sdk_header_manifest(root)
            self.assertEqual(count1, 2)
            self.assertEqual((count1, digest1), (count2, digest2))

            (headers / "AE_Effect.h").write_text("changed", encoding="utf-8")
            count3, digest3 = check_native.sdk_header_manifest(root)
            self.assertEqual(count3, 2)
            self.assertNotEqual(digest1, digest3)

    def test_sdk_header_manifest_accepts_alias_root(self):
        with tempfile.TemporaryDirectory() as td:
            physical = Path(td).resolve() / "sdk"
            (physical / "Headers").mkdir(parents=True)
            (physical / "Headers" / "AE_Effect.h").write_text("fixture")
            alias = Path(td) / "sdk-alias"
            alias.symlink_to(physical, target_is_directory=True)
            self.assertEqual(check_native.sdk_header_manifest(alias),
                             check_native.sdk_header_manifest(physical))

    def _make_fake_tree(self, root: Path):
        sdk = root / "sdk" / "Examples"
        (sdk / "Headers" / "SP").mkdir(parents=True)
        (sdk / "Util").mkdir(parents=True)
        (sdk / "Headers" / "AE_Effect.h").write_text("/* fixture */", encoding="utf-8")
        (sdk / "Util" / "AEGP_SuiteHandler.h").write_text("/* fixture */", encoding="utf-8")

        source_dir = root / "16-WORKING-TEMPLATES" / "fixture"
        source_dir.mkdir(parents=True)
        (source_dir / "Fixture.cpp").write_text("int fixture = 1;", encoding="utf-8")

        (root / "19-NATIVE-CODE-FOUNDATION" / "code").mkdir(parents=True)
        (root / "17-NATIVE-SUITE-COOKBOOK" / "code").mkdir(parents=True)

        compiler = root / "fake-clang"
        compiler.write_text(
            "#!/usr/bin/env python3\n"
            "import sys\n"
            "if '--version' in sys.argv:\n"
            "    print('fake clang version 1.0')\n"
            "    raise SystemExit(0)\n"
            "raise SystemExit(0)\n",
            encoding="utf-8",
        )
        compiler.chmod(0o755)
        return sdk, compiler

    def test_run_checks_emits_machine_readable_identity(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            sdk, compiler = self._make_fake_tree(root)

            report, failures = check_native.run_checks(
                sdk,
                str(compiler),
                "clang",
                root=root,
            )

            self.assertEqual(failures, 0)
            self.assertEqual(report["summary"]["status"], "PASS")
            self.assertEqual(report["summary"]["translation_units"], 2)
            self.assertEqual(report["sdk"]["header_count"], 2)
            self.assertEqual(len(report["sdk"]["header_manifest_sha256"]), 64)
            self.assertIn("fake clang version 1.0", report["compiler"]["identity"])
            self.assertEqual(report["source"]["git_sha"], None)
            self.assertEqual(report["source"]["dirty"], None)
            self.assertTrue(all(len(item["source_sha256"]) == 64 for item in report["results"]))
            self.assertTrue(all(item["status"] == "PASS" for item in report["results"]))

    def test_run_checks_reports_translation_unit_failure(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            sdk, compiler = self._make_fake_tree(root)
            compiler.write_text(
                "#!/usr/bin/env python3\n"
                "import sys\n"
                "if '--version' in sys.argv:\n"
                "    print('fake clang version 1.0')\n"
                "    raise SystemExit(0)\n"
                "if any(arg.endswith('Fixture.cpp') for arg in sys.argv):\n"
                "    print('fixture failure', file=sys.stderr)\n"
                "    raise SystemExit(9)\n"
                "raise SystemExit(0)\n",
                encoding="utf-8",
            )
            compiler.chmod(0o755)

            report, failures = check_native.run_checks(
                sdk,
                str(compiler),
                "clang",
                root=root,
            )

            self.assertEqual(failures, 1)
            self.assertEqual(report["summary"]["status"], "FAIL")
            failed = [item for item in report["results"] if item["status"] == "FAIL"]
            self.assertEqual(len(failed), 1)
            self.assertEqual(failed[0]["returncode"], 9)
            self.assertIn("fixture failure", failed[0]["stderr_tail"])

    def test_clean_source_identity_gate(self):
        self.assertIsNone(
            check_native.source_identity_error({"git_sha": "abc", "dirty": False})
        )
        self.assertIn(
            "Git SHA",
            check_native.source_identity_error({"git_sha": None, "dirty": False}),
        )
        self.assertIn(
            "dirty",
            check_native.source_identity_error({"git_sha": "abc", "dirty": True}),
        )

    def test_empty_source_tree_fails_closed(self):
        with tempfile.TemporaryDirectory() as td:
            with self.assertRaises(ValueError):
                check_native.collect_sources(Path(td))


if __name__ == "__main__":
    unittest.main()
