import json
import unittest
from pathlib import Path
from audit_expression_inventory import headings

ROOT = Path(__file__).resolve().parent.parent


class ExpressionInventoryTests(unittest.TestCase):
    def test_overloads_and_namespaces_preserved(self):
        self.assertEqual(headings("### key()\n### key()\n### PathProperty.points()\n"
                                  "#### Description\n## Methods\n"),
                         ["key()", "key()", "PathProperty.points()"])

    def test_reviewed_pages_are_unique_and_hash_pinned(self):
        inventory = json.loads((ROOT / "expression-api-inventory-2026-10-08.json").read_text())
        ledger = json.loads((ROOT / "expression-api-reviewed-2026-10-08.json").read_text())
        known = {r["source_path"]: r for r in inventory["records"]}
        self.assertEqual(ledger["source_revision"], inventory["source_revision"])
        paths = [r["source_path"] for r in ledger["reviews"]]
        self.assertEqual(len(paths), len(set(paths)))
        self.assertEqual(set(paths), set(known), "Pinned page review must be exhaustive")
        self.assertEqual(inventory["source_pages"], len(known))
        self.assertEqual(inventory["headings"], sum(len(r["headings"]) for r in known.values()))
        for r in ledger["reviews"]:
            self.assertEqual(r["source_sha256"], known[r["source_path"]]["source_sha256"])
            self.assertTrue(r["operation"])
            self.assertTrue((ROOT / r["coverage_page"]).is_file())
        self.assertIn("runtime NOT_RUN", ledger["evidence"])


if __name__ == "__main__":
    unittest.main()
