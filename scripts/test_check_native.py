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

    def test_empty_source_tree_fails_closed(self):
        with tempfile.TemporaryDirectory() as td:
            with self.assertRaises(ValueError):
                check_native.collect_sources(Path(td))


if __name__ == "__main__":
    unittest.main()
