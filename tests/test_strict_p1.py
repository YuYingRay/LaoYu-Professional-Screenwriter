from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from scripts.validate_project import validate


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts" / "validate_project.py"


def write_project(root: Path, *, status: str, acceptance: str = "") -> None:
    governance = root / "governance"
    reviews = root / "development" / "review-reports"
    governance.mkdir(parents=True)
    reviews.mkdir(parents=True)
    (governance / "project-manifest.md").write_text(
        "---\nartifact_id: PROJECT-P1-001\nartifact_type: PROJECT_MANIFEST\n"
        "project_id: PROJECT-P1-001\nproject_baseline: BASELINE-A\n"
        "artifact_version: v1.0.0\nstatus: DRAFT\nowner: TEST\nupstream_ids: []\n---\n",
        encoding="utf-8",
        newline="\n",
    )
    (reviews / "REVIEW-001.md").write_text(
        "---\nartifact_id: REVIEW-001\nartifact_type: REVIEW\n"
        "project_id: PROJECT-P1-001\nproject_baseline: BASELINE-A\n"
        "artifact_version: v1.0.0\nstatus: DRAFT\nowner: TEST\nupstream_ids: []\n"
        "findings: [FIND-P1-001]\n---\n"
        "```finding\n"
        "finding_id: FIND-P1-001\nseverity: P1\nevidence_location: SC-001\n"
        "failure_mechanism: A production dependency is unresolved.\n"
        "downstream_impact: Delivery can drift.\nminimum_fix: Resolve the dependency.\n"
        "verification_method: Re-run the project gate.\nowner: TEST\n"
        f"status: {status}\n{acceptance}```\n",
        encoding="utf-8",
        newline="\n",
    )


def cli(root: Path, mode: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(VALIDATOR), str(root), "--mode", mode],
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        check=False,
    )


class StrictP1Tests(unittest.TestCase):
    def test_unaccepted_p1_is_visible_in_audit_and_blocks_strict(self) -> None:
        with tempfile.TemporaryDirectory(prefix="psw-p1-open-") as temp_dir:
            root = Path(temp_dir)
            write_project(root, status="OPEN")
            self.assertEqual(cli(root, "audit").returncode, 0)
            strict = cli(root, "strict")
            self.assertNotEqual(strict.returncode, 0)
            self.assertIn("P1 UNACCEPTED_P1", strict.stdout)

    def test_accepted_risk_requires_all_four_acceptance_fields(self) -> None:
        with tempfile.TemporaryDirectory(prefix="psw-p1-incomplete-") as temp_dir:
            root = Path(temp_dir)
            write_project(root, status="ACCEPTED_RISK", acceptance="acceptance_owner: TEST\n")
            result = validate(root)
            self.assertIn("P1_ACCEPTANCE_FIELD", {item.code for item in result})

    def test_complete_accepted_risk_does_not_block_strict(self) -> None:
        with tempfile.TemporaryDirectory(prefix="psw-p1-accepted-") as temp_dir:
            root = Path(temp_dir)
            write_project(
                root,
                status="ACCEPTED_RISK",
                acceptance=(
                    "acceptance_owner: PRODUCER\n"
                    "acceptance_until: 2026-12-31\n"
                    "compensation_plan: Keep the fallback asset available.\n"
                    "reverification_plan: Re-run before production release.\n"
                ),
            )
            result = cli(root, "strict")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
