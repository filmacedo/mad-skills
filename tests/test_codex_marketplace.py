import json
import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]


class CodexMarketplaceTests(unittest.TestCase):
    def test_personal_marketplace_exposes_all_plugins(self) -> None:
        marketplace_path = REPOSITORY_ROOT / ".agents/plugins/marketplace.json"
        self.assertTrue(
            marketplace_path.is_file(),
            "Codex marketplace manifest is missing",
        )

        marketplace = json.loads(marketplace_path.read_text())
        self.assertEqual(marketplace["name"], "filipe-skills")
        self.assertEqual(marketplace["interface"]["displayName"], "Personal")

        expected_paths = {
            "chief-of-staff": "./plugins/chief-of-staff",
            "inbox-assistant": "./plugins/inbox-assistant",
            "mad-engineering": "./plugins/mad-engineering",
        }
        self.assertEqual(
            [plugin["name"] for plugin in marketplace["plugins"]],
            list(expected_paths),
        )
        for plugin in marketplace["plugins"]:
            self.assertEqual(
                plugin["source"],
                {"source": "local", "path": expected_paths[plugin["name"]]},
            )
            self.assertEqual(
                plugin["policy"],
                {"installation": "AVAILABLE", "authentication": "ON_INSTALL"},
            )
            self.assertEqual(plugin["category"], "Productivity")


if __name__ == "__main__":
    unittest.main()
