"""Validate authored plan structure only; no Adobe rendering is simulated."""
import json
from pathlib import Path
import unittest


class EvidencePlanTests(unittest.TestCase):
    def test_unexecuted_plan_cannot_advertise_observations(self):
        root = Path(__file__).resolve().parents[1]
        plan = json.loads((root / '13-TEMPLATES/examples/gain-evidence-plan.json').read_text())
        self.assertEqual(plan['kind'], 'ILLUSTRATIVE')
        self.assertEqual(plan['status'], 'NOT_RUN')
        self.assertEqual(plan['rawEvidence'], [])
        for key in ('sourceCommit', 'artifactSha256', 'hostBuild', 'loadedImageIdentity'):
            self.assertIsNone(plan[key])
        self.assertTrue((root / plan['sourcePath']).is_file())
        for scenario in plan['scenarios']:
            self.assertEqual(scenario['status'], 'NOT_RUN')
            self.assertIsNone(scenario.get('observedRGBA', scenario.get('observed')))

    def test_predeclared_integer_expectations(self):
        root = Path(__file__).resolve().parents[1]
        plan = json.loads((root / '13-TEMPLATES/examples/gain-evidence-plan.json').read_text())
        for scenario in plan['scenarios']:
            if 'fixture' not in scenario:
                continue
            fixture = scenario['fixture']
            maximum = {8: 255, 16: 32768}[fixture['depth']]
            rgba = fixture['inputRGBA']
            expected = [int(min(maximum, max(0, c * fixture['gain']))) for c in rgba[:3]]
            expected.append(rgba[3])
            self.assertEqual(scenario['expectedRGBA'], expected)


if __name__ == '__main__':
    unittest.main()
