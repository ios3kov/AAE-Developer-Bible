import hashlib
import json
import unittest
from pathlib import Path

from audit_public_guide_inventory import PROFILES, page_entries, source_record

ROOT = Path(__file__).resolve().parents[1]


def blob(path, raw=b"# Page\n"):
    sha = hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()
    return {"path": path, "sha": sha, "size": len(raw), "type": "blob", "mode": "100644"}


class PublicGuideInventoryTests(unittest.TestCase):
    def test_page_scope_includes_navigation_and_history(self):
        entries = [blob("readme.md"), blob("docs/index.md"), blob("docs/history.md"),
                   blob("docs/_global/readme.md"), blob("docs/image.png")]
        tree = {"sha": "tree-sha", "truncated": False, "tree": entries}
        self.assertEqual([e["path"] for e in page_entries(tree, "tree-sha")],
                         ["docs/_global/readme.md", "docs/history.md", "docs/index.md"])

    def test_incomplete_wrong_tree_or_nonregular_sources_are_rejected(self):
        for tree in [
            {"sha": "tree-sha", "truncated": True, "tree": []},
            {"sha": "commit-sha", "truncated": False, "tree": []},
            {"sha": "tree-sha", "truncated": False,
             "tree": [blob("docs/page.md"), blob("docs/page.md")]},
            {"sha": "tree-sha", "truncated": False,
             "tree": [{**blob("docs/link.md"), "mode": "120000"}]},
        ]:
            with self.assertRaises(ValueError):
                page_entries(tree, "tree-sha")

    def test_exact_bytes_reject_added_newline_or_changed_size(self):
        raw = "# Текст".encode("utf-8")
        entry = blob("docs/page.md", raw)
        record = source_record(entry, raw)
        self.assertEqual(record["bytes"], len(raw))
        self.assertEqual(record["lines"], 1)
        self.assertEqual(record["source_sha256"], hashlib.sha256(raw).hexdigest())
        with self.assertRaises(ValueError):
            source_record(entry, raw + b"\n")
        with self.assertRaises(ValueError):
            source_record({**entry, "size": 0}, raw)

    def assert_full_page_review(self, profile, prefix, expected_pages):
        inventory = json.loads((ROOT / (prefix + "-inventory-2026-10-08.json")).read_text())
        ledger = json.loads((ROOT / (prefix + "-reviewed-2026-10-08.json")).read_text())
        repository, revision, tree_sha = PROFILES[profile]
        self.assertEqual(inventory["repository"], repository)
        self.assertEqual(inventory["source_revision"], revision)
        self.assertEqual(inventory["tree_sha"], tree_sha)
        self.assertIs(inventory["tree_truncated"], False)
        self.assertEqual(ledger["repository"], repository)
        self.assertEqual(ledger["source_revision"], revision)
        self.assertEqual(ledger["tree_sha"], tree_sha)
        known = {r["source_path"]: r for r in inventory["records"]}
        reviewed = {r["source_path"]: r for r in ledger["reviews"]}
        self.assertEqual(len(known), len(inventory["records"]))
        self.assertEqual(len(reviewed), len(ledger["reviews"]))
        self.assertEqual(inventory["source_pages"], expected_pages)
        self.assertEqual(ledger["source_pages"], expected_pages)
        self.assertEqual(len(known), expected_pages)
        self.assertEqual(set(known), set(reviewed), "No page is closed by omission")
        for path, review in reviewed.items():
            self.assertIs(review["full_page_reviewed"], True, path)
            self.assertEqual(review["source_sha256"], known[path]["source_sha256"], path)
            self.assertEqual(review["git_blob_sha"], known[path]["git_blob_sha"], path)
            self.assertEqual(review["bytes"], known[path]["bytes"], path)
            self.assertEqual(review["lines"], known[path]["lines"], path)
            self.assertTrue(review["operation"].strip(), path)
            self.assertTrue((ROOT / review["coverage_page"]).is_file(), path)

    def test_native_full_page_review_matches_exact_inventory(self):
        self.assert_full_page_review("native", "native-guide", 89)

    def test_extendscript_full_page_review_matches_exact_inventory(self):
        self.assert_full_page_review("extendscript", "extendscript-runtime", 73)


if __name__ == "__main__":
    unittest.main()
