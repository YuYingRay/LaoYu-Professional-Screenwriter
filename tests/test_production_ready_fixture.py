from __future__ import annotations

import shutil
import tempfile
import unittest
from pathlib import Path

from scripts import run_protocol
from scripts.validate_project import validate


ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "tests" / "production-ready-fixture"
SCHEMA = ROOT / "governance" / "control-schema.json"
RUN = "RUN-PRODUCTION-READY"


def codes(root: Path) -> set[str]:
    return {item.code for item in validate(root)}


class ProductionReadyFixtureTests(unittest.TestCase):
    def test_complete_evidence_chain_passes(self) -> None:
        self.assertEqual(codes(FIXTURE), set())
        self.assertEqual(
            run_protocol.final_check(FIXTURE, FIXTURE / "runs" / f"{RUN}.json", SCHEMA)["result"],
            "PASS",
        )

    def test_deleting_any_required_evidence_fails(self) -> None:
        evidence_paths = [
            "development/story-bible.md",
            "development/review-reports/REVIEW-PROD-001.md",
            "script/master/script.fountain",
            "governance/rights-register.md",
            "production/handoff/handoff.md",
            f"runs/{RUN}.json",
        ]
        for relative in evidence_paths:
            with self.subTest(relative=relative), tempfile.TemporaryDirectory(prefix="psw-prod-evidence-") as temp_dir:
                target = Path(temp_dir) / FIXTURE.name
                shutil.copytree(FIXTURE, target)
                (target / relative).unlink()
                self.assertTrue(codes(target), relative)

    def test_deleting_compatibility_record_fails(self) -> None:
        with tempfile.TemporaryDirectory(prefix="psw-prod-compat-") as temp_dir:
            target = Path(temp_dir) / FIXTURE.name
            shutil.copytree(FIXTURE, target)
            handoff = target / "production" / "handoff" / "handoff.md"
            text = handoff.read_text(encoding="utf-8")
            start = text.index("```compatibility")
            end = text.index("```", start + 3) + 3
            handoff.write_text(text[:start] + text[end:], encoding="utf-8", newline="\n")
            self.assertIn("PRODUCTION_EVIDENCE_REF", codes(target))


if __name__ == "__main__":
    unittest.main()
