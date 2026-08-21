import json
import unittest
from pathlib import Path


FIXTURES = Path(__file__).resolve().parent / "fixtures" / "classification-cases.json"

PURPOSES = {
    "human_correspondence",
    "events",
    "content",
    "updates",
    "notifications",
    "transactions",
    "cold_outreach",
    "other",
}
ATTENTION = {"act_now", "act_later", "fyi", "routine_cleanup", "suspicious"}


class FixtureContractTest(unittest.TestCase):
    def test_fixture_ids_and_expected_values_are_valid(self):
        cases = json.loads(FIXTURES.read_text(encoding="utf-8"))
        ids = [case["id"] for case in cases]
        self.assertEqual(len(ids), len(set(ids)))
        for case in cases:
            self.assertIn(case["expected"]["purpose"], PURPOSES)
            self.assertIn(case["expected"]["attention"], ATTENTION)
            self.assertIn("reason", case["expected"])


if __name__ == "__main__":
    unittest.main()
