from __future__ import annotations

import re
import unittest
from pathlib import Path

from scripts import test_template_instantiation


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "templates" / "feature-screenplay.fountain"
SCENE_ID_LINE = re.compile(r"^/\*\s*(SC-\d{3})\s*\*/$")
SCENE_HEADING = re.compile(r"^\.(?:内景|外景|内外景|外内景)\b")


class FeatureTemplateTests(unittest.TestCase):
    def test_required_machine_metadata_occurs_once(self) -> None:
        text = TEMPLATE.read_text(encoding="utf-8")
        for field in ["ARTIFACT_ID", "PROJECT_ID", "OWNER"]:
            self.assertEqual(len(re.findall(rf"^/\* {field}:", text, re.MULTILINE)), 1, field)

    def test_every_scene_heading_has_one_stable_scene_id(self) -> None:
        lines = TEMPLATE.read_text(encoding="utf-8").splitlines()
        scene_ids: list[str] = []
        headings = 0
        for index, line in enumerate(lines):
            if not SCENE_HEADING.match(line):
                continue
            headings += 1
            previous = index - 1
            while previous >= 0 and not lines[previous].strip():
                previous -= 1
            match = SCENE_ID_LINE.fullmatch(lines[previous]) if previous >= 0 else None
            self.assertIsNotNone(match, f"scene heading at line {index + 1} has no Scene ID")
            scene_ids.append(match.group(1))
        self.assertEqual(headings, 28)
        self.assertEqual(scene_ids, [f"SC-{number:03d}" for number in range(1, 29)])

    def test_feature_instantiation_generates_matching_scene_cards(self) -> None:
        self.assertTrue(hasattr(test_template_instantiation, "instantiate_feature"))
        findings = test_template_instantiation.instantiate_feature(ROOT, "candidate")
        self.assertFalse(findings, "\n".join(f"{item.code}: {item.message}" for item in findings))


if __name__ == "__main__":
    unittest.main()
