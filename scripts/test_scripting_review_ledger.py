import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


class ReviewLedgerTests(unittest.TestCase):
    def test_zero_heading_pages_are_explicitly_reviewed(self):
        inventory = json.loads((ROOT / 'scripting-api-inventory-2026-10-07.json').read_text())
        ledger = json.loads((ROOT / 'scripting-zero-heading-reviewed-2026-10-08.json').read_text())
        known = {r['source_path']: r for r in inventory['records'] if not r['members']}
        paths = [r['source_path'] for r in ledger['reviews']]
        self.assertEqual(len(paths), len(set(paths)))
        self.assertEqual(set(paths), set(known))
        self.assertEqual(ledger['source_revision'], inventory['source_revision'])
        self.assertTrue((ROOT / ledger['coverage_page']).is_file())
        for r in ledger['reviews']:
            self.assertTrue(r['operation'])
            self.assertEqual(r['source_sha256'], known[r['source_path']]['source_sha256'])
        self.assertIn('runtime NOT_RUN', ledger['evidence'])

    def test_explicit_reviews_are_unique_and_pinned_to_inventory(self):
        inventory = json.loads((ROOT / 'scripting-api-inventory-2026-10-07.json').read_text())
        ledger = json.loads((ROOT / 'scripting-api-reviewed-2026-10-07.json').read_text())
        self.assertEqual(ledger['source_revision'], inventory['source_revision'])
        self.assertTrue((ROOT / ledger['coverage_page']).is_file())
        known = {(record['source_path'], member['name'])
                 for record in inventory['records'] for member in record['members']}
        reviewed = []
        for record in ledger['reviews']:
            self.assertTrue(record['operation'])
            self.assertTrue(record['members'])
            reviewed.extend((record['source_path'], name) for name in record['members'])
        self.assertEqual(len(reviewed), len(set(reviewed)))
        self.assertTrue(set(reviewed) <= known, set(reviewed) - known)
        self.assertIn('runtime NOT_RUN', ledger['evidence'])

    def test_inventory_is_partitioned_without_promoting_research(self):
        inventory = json.loads((ROOT / 'scripting-api-inventory-2026-10-07.json').read_text())
        ledger = json.loads((ROOT / 'scripting-api-reviewed-2026-10-07.json').read_text())
        known = {(r['source_path'], m['name']) for r in inventory['records']
                 for m in r['members']}
        documented = {(r['source_path'], m) for r in ledger['reviews'] for m in r['members']}
        exclusions = ledger['exclusions']
        excluded = {(r['source_path'], r['member']) for r in exclusions}
        self.assertEqual(len(excluded), len(exclusions))
        self.assertTrue(all(r['reason'] for r in exclusions))
        self.assertFalse(documented & excluded)
        self.assertEqual(documented | excluded, known)


if __name__ == '__main__':
    unittest.main()
