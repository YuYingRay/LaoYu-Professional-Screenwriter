from __future__ import annotations

import csv
import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MAP = ROOT / "governance" / "placeholder-migration-map.json"
ENTRIES = ROOT / "governance" / "placeholder-migration-entries.tsv"
CHECKER = ROOT / "scripts" / "migrate_placeholders.py"


class PlaceholderMigrationTests(unittest.TestCase):
    def test_explicit_map_is_complete_and_reversible(self) -> None:
        result = subprocess.run(
            [sys.executable, str(CHECKER), "--check", str(ROOT)],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("PASS: placeholder migration map", result.stdout)

    def test_map_records_both_migrations_and_protected_syntax(self) -> None:
        data = json.loads(MAP.read_text(encoding="utf-8"))
        with ENTRIES.open(encoding="utf-8", newline="") as handle:
            entries = list(csv.DictReader(handle, delimiter="\t"))
        actions = {entry["action"] for entry in entries}
        self.assertEqual(actions, {"MIGRATE", "PRESERVE"})
        self.assertEqual(len(entries), data["summary"]["candidate_occurrences"])
        self.assertEqual(data["entries_file"], "governance/placeholder-migration-entries.tsv")
        self.assertGreater(data["summary"]["migrated_occurrences"], 0)
        self.assertGreater(data["summary"]["preserved_occurrences"], 0)
        self.assertEqual(data["protected_counts"]["checkbox_markers_before"],
                         data["protected_counts"]["checkbox_markers_after"])
        self.assertEqual(data["protected_counts"]["frontmatter_list_lines_before"],
                         data["protected_counts"]["frontmatter_list_lines_after"])
        self.assertEqual(data["protected_counts"]["markdown_links_before"],
                         data["protected_counts"]["markdown_links_after"])

    def test_canonical_slots_use_double_brackets(self) -> None:
        template = (ROOT / "templates" / "scene-card.md").read_text(encoding="utf-8")
        self.assertIn("PROJECT-[[SLUG]]-001", template)
        self.assertIn("SC-[[NNN]]", template)
        self.assertNotIn("PROJECT-[SLUG]-001", template)

    def test_nested_final_list_slots_are_not_missed(self) -> None:
        expected = {
            "episode-outline.md": "BIBLE-[[VERSION]]",
            "review-report.md": "SCRIPT-[[VERSION]]",
            "scene-card.md": "DEL-[[OUTLINE-ID]]",
            "vertical-episode.md": "DEL-SEASON-[[NNN]]",
        }
        for name, token in expected.items():
            text = (ROOT / "templates" / name).read_text(encoding="utf-8")
            self.assertIn(token, text, name)
        repair_map = ROOT / "governance" / "placeholder-migration-repair-map.tsv"
        with repair_map.open(encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle, delimiter="\t"))
        self.assertEqual(len(rows), 4)

    def test_open_notice_tracks_placeholder_migration(self) -> None:
        notice = (ROOT / "governance" / "notices" / "NOTICE-CONTRACT-001.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("MIG-WP3B-PLACEHOLDERS", notice)
        self.assertIn("placeholder-migration-map.json", notice)


if __name__ == "__main__":
    unittest.main()
