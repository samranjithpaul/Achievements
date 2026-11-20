import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from scripts.catalog import CATALOG, load_catalog


class CatalogTests(unittest.TestCase):
    def setUp(self):
        self.entries = load_catalog()

    def assert_invalid(self, entries, message):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "catalog.json"
            path.write_text(json.dumps(entries), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, message):
                load_catalog(path)

    def test_catalog_has_counter_and_experimental_examples(self):
        entries = {entry["id"]: entry for entry in self.entries}
        self.assertEqual(entries["pull-shark"]["thresholds"]["base"], 2)
        self.assertEqual(entries["open-sourcerer"]["thresholds"], {})

    def test_rejects_duplicate_id(self):
        self.assert_invalid(self.entries + [self.entries[0]], "duplicate ID")

    def test_rejects_missing_or_unordered_tiers(self):
        for tiers, message in (
            ({"bronze": 4}, "consecutive tiers"),
            ({"base": 4, "bronze": 2}, "strictly increase"),
            ({"base": True}, "positive integers"),
        ):
            with self.subTest(tiers=tiers):
                entries = copy.deepcopy(self.entries)
                entries[0]["thresholds"] = tiers
                self.assert_invalid(entries, message)

    def test_rejects_non_https_source(self):
        self.entries[0]["sources"] = ["http://example.com"]
        self.assert_invalid(self.entries, "invalid HTTPS source")

    def test_cli_filters_entries(self):
        result = subprocess.run(
            [sys.executable, str(CATALOG.parents[1] / "scripts" / "catalog.py"),
             "--status", "experimental"],
            check=True,
            capture_output=True,
            text=True,
        )
        self.assertIn("Open Sourcerer [experimental]", result.stdout)
        self.assertNotIn("Pull Shark", result.stdout)


if __name__ == "__main__":
    unittest.main()
