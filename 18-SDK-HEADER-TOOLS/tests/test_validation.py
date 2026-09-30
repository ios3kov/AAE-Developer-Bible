import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest

TOOLS = Path(__file__).resolve().parents[1] / "tools"


def load(name):
    spec = importlib.util.spec_from_file_location(name, TOOLS / (name + ".py"))
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


inventory = load("ae_sdk_inventory")
verify = load("verify_recipe_symbols")
diff = load("diff_sdk_inventory")


class ValidationTests(unittest.TestCase):
    def test_partial_table_is_diagnostic(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "test.h"
            path.write_text("typedef struct { A_Err (*AEGP_One)(void); A_Err (OTHER_CALL *AEGP_Two)(void); } AEGP_ProbeSuite1;")
            data = inventory.inventory([str(path)])
            self.assertEqual(data["function_count"], 1)
            self.assertTrue(data["partial_candidate_tables"])
            with self.assertRaises(ValueError):
                verify.verify(data, [])

    def test_missing_and_empty_paths_fail(self):
        with tempfile.TemporaryDirectory() as tmp:
            for path in (Path(tmp), Path(tmp) / "missing"):
                with self.assertRaises(ValueError):
                    verify.source_files([path])

    def test_comments_and_strings_are_not_calls(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "test.cpp"
            path.write_text('// s->AEGP_Fake();\n"s->AEGP_Fake()";\ns->AEGP_Known();\ns->AEGP_Unknown();')
            data = {"tables": [{"functions": [{"name": "AEGP_Known"}]}]}
            count, unknown = verify.verify(data, [path])
            self.assertEqual(count, 2)
            self.assertEqual(unknown[0][1:], (4, "AEGP_Unknown"))
            path.write_text("// no real calls")
            with self.assertRaises(ValueError):
                verify.verify(data, [path])

    def test_order_change_is_reported(self):
        fields = [{"name": n, "signature": f"void (*{n})(void);"} for n in ("A", "B")]
        report = diff.compare({"Suite": fields}, {"Suite": list(reversed(fields))})
        self.assertIn("order/layout changed", report)
        self.assertNotIn("No indexed", report)

    def test_conflicting_table_versions_fail(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "index.json"
            path.write_text(json.dumps({"tables": [
                {"name": "Suite", "functions": [{"name": "A"}]},
                {"name": "Suite", "functions": [{"name": "B"}]}]}))
            with self.assertRaises(ValueError):
                diff.load(path)

    def test_large_unsupported_declaration_is_bounded(self):
        self.assertEqual(inventory.parse_functions("A_ " * 20000 + ";"), [])


if __name__ == "__main__":
    unittest.main()
