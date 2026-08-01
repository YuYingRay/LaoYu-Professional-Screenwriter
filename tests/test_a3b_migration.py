from __future__ import annotations

import csv
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MAP = ROOT / "governance" / "a3b-skill-dedup-map.tsv"


class A3bMigrationTests(unittest.TestCase):
    def test_three_semantic_migrations_have_human_decisions(self) -> None:
        with MAP.open(encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle, delimiter="\t"))
        self.assertEqual({row["item_id"] for row in rows}, {"A3B-BIBLE", "A3B-SCENE", "A3B-REVIEW"})
        for row in rows:
            for field in [
                "source_location",
                "responsibility",
                "target_anchor",
                "retained_or_adapted",
                "reviewer",
                "review_decision",
                "review_rationale",
            ]:
                self.assertTrue(row[field].strip(), f"{row['item_id']}:{field}")
            self.assertIn(row["review_decision"], {"RECOMMEND", "CONDITIONAL_RECOMMEND"})

    def test_each_target_anchor_resolves_exactly_once(self) -> None:
        with MAP.open(encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle, delimiter="\t"))
        for row in rows:
            for target in row["target_anchor"].split(" | "):
                relative, heading = target.split("::", 1)
                lines = (ROOT / relative).read_text(encoding="utf-8").splitlines()
                self.assertEqual(lines.count(heading), 1, target)

    def test_skill_keeps_decision_entries_and_routes_details(self) -> None:
        text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        bible = text.split("## Full Bible 最小核心域", 1)[1].split("## 结构与场景", 1)[0]
        scene = text.split("## 结构与场景", 1)[1].split("## 竖屏短剧", 1)[0]
        review = text.split("## 对抗式审查", 1)[1].split("## 重写", 1)[0]
        self.assertIn("references/story-bible-templates.md", bible)
        self.assertIn("templates/story-bible.md", bible)
        self.assertIn("templates/scene-card.md", scene)
        self.assertIn("references/adversarial-review-rubric.md", review)
        self.assertIn("不可合并", review)


if __name__ == "__main__":
    unittest.main()
