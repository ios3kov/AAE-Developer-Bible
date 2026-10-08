import json
import unittest
from pathlib import Path
from audit_uxp_inventory import members

ROOT = Path(__file__).resolve().parent.parent


class UxpInventoryTests(unittest.TestCase):
    def test_properties_not_parameters_and_method_kinds(self):
        text = """## Properties
| Name | Type | Access | Min Version | Description |
| file | *string* | RW | 27.0 | path |
## Instance Methods
### save
#### Parameters
| path | *string* | filename |
## Static Methods
### create
"""
        self.assertEqual([r['name'] for r in members(text)], ['file', 'save', 'create'])
        self.assertEqual(members(text)[0]['min_version'], '27.0')

    def test_reviews_unique_and_hash_pinned(self):
        inventory = json.loads((ROOT / 'uxp-api-inventory-2026-10-08.json').read_text())
        ledger = json.loads((ROOT / 'uxp-api-reviewed-2026-10-08.json').read_text())
        known = {r['source_path']: r for r in inventory['records']}
        self.assertEqual(ledger['source_revision'], inventory['source_revision'])
        paths = [r['source_path'] for r in ledger['reviews']]
        self.assertEqual(len(paths), len(set(paths)))
        for r in ledger['reviews']:
            self.assertEqual(r['source_sha256'], known[r['source_path']]['source_sha256'])
            self.assertTrue(r['operation'])
            self.assertTrue((ROOT / r['coverage_page']).is_file())
        self.assertIn('runtime NOT_RUN', ledger['evidence'])


if __name__ == '__main__':
    unittest.main()
