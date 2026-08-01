from __future__ import annotations

import shutil
import tempfile
import unittest
from pathlib import Path

from scripts.validate_project import validate


ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "tests" / "feature-project-fixture"


class A4EvidenceChainTests(unittest.TestCase):
    def test_r03_wording_is_identical_at_both_locations(self) -> None:
        text = (ROOT / "examples" / "vertical-drama-example.md").read_text(encoding="utf-8")
        canonical = "旧门禁卡可开启档案室一次，但会留下访问日志"
        self.assertEqual(text.count(canonical), 2)
        self.assertNotIn("旧门禁卡可开启一次维护访问", text)

    def test_feature_fixture_has_structured_claim_and_nine_field_findings(self) -> None:
        findings = validate(FIXTURE, baseline_mode="active")
        self.assertFalse(findings, "\n".join(f"{item.code}: {item.message}" for item in findings))
        bible = (FIXTURE / "story" / "story-bible.md").read_text(encoding="utf-8")
        review = (FIXTURE / "reviews" / "REVIEW-001.md").read_text(encoding="utf-8")
        self.assertIn("```continuity-claim", bible)
        self.assertEqual(review.count("```finding"), 2)

    def test_deleting_evidence_ref_fails_with_stable_code(self) -> None:
        with tempfile.TemporaryDirectory(prefix="psw-a4-") as temp_dir:
            project = Path(temp_dir) / "fixture"
            shutil.copytree(FIXTURE, project)
            bible = project / "story" / "story-bible.md"
            text = bible.read_text(encoding="utf-8")
            text = "\n".join(
                line for line in text.splitlines() if not line.startswith("evidence_ref:")
            ) + "\n"
            bible.write_text(text, encoding="utf-8", newline="\n")
            result = validate(project, baseline_mode="active")
        self.assertIn("CONTINUITY_EVIDENCE_REF", {item.code for item in result})

    def test_missing_scene_and_review_record_are_detected(self) -> None:
        with tempfile.TemporaryDirectory(prefix="psw-a4-") as temp_dir:
            project = Path(temp_dir) / "fixture"
            shutil.copytree(FIXTURE, project)
            bible = project / "story" / "story-bible.md"
            text = bible.read_text(encoding="utf-8").replace(
                "SCRIPT-v1.0.0#SC-002", "SCRIPT-v1.0.0#SC-999"
            ).replace("REVIEW-001#FIND-CONT-001", "REVIEW-001#FIND-MISSING")
            bible.write_text(text, encoding="utf-8", newline="\n")
            result = validate(project, baseline_mode="active")
        codes = {item.code for item in result}
        self.assertIn("CONTINUITY_EVIDENCE_SCENE", codes)
        self.assertIn("CONTINUITY_REVIEW_REF", codes)

    def test_validator_does_not_use_story_keywords_as_semantic_proxy(self) -> None:
        source = (ROOT / "scripts" / "validate_project.py").read_text(encoding="utf-8")
        self.assertNotIn("旧伤", source)
        self.assertNotIn("右手", source)


if __name__ == "__main__":
    unittest.main()
