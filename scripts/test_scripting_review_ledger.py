import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


class ReviewLedgerTests(unittest.TestCase):
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


if __name__ == '__main__':
    unittest.main()
