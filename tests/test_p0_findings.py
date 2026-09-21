from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from scripts.validate_project import validate
from test_strict_p1 import cli, write_project


ACCEPTANCE = (
    "acceptance_owner: PRODUCER\n"
    "acceptance_until: 2026-12-31\n"
    "compensation_plan: Restrict work to development.\n"
    "reverification_plan: Resolve before leaving development.\n"
)


class P0FindingTests(unittest.TestCase):
    def test_unresolved_p0_blocks_audit_and_strict(self) -> None:
        for status in ("OPEN", "IN_PROGRESS", "REGRESSED", "UNKNOWN"):
            for mode in ("audit", "strict"):
                with self.subTest(status=status, mode=mode), tempfile.TemporaryDirectory() as temp:
                    root = Path(temp)
                    write_project(root, status=status, severity="P0")
                    result = cli(root, mode)
                    self.assertNotEqual(result.returncode, 0, result.stdout)
                    self.assertIn("P0 UNACCEPTED_P0", result.stdout)

    def test_fixed_p0_does_not_block(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            write_project(root, status="FIXED", severity="P0", stage="PRODUCTION")
            self.assertEqual(validate(root), [])

    def test_complete_p0_acceptance_is_allowed_only_in_development(self) -> None:
        for stage in ("DEVELOPMENT", "CONCEPT", "OUTLINE", "SCRIPT", "PREP",
                      "PRODUCTION", "POST", "RELEASE", "ARCHIVED", ""):
            with self.subTest(stage=stage), tempfile.TemporaryDirectory() as temp:
                root = Path(temp)
                write_project(root, status="ACCEPTED_RISK", severity="P0",
                              stage=stage, acceptance=ACCEPTANCE)
                result = cli(root, "audit")
                self.assertEqual(result.returncode, 0 if stage == "DEVELOPMENT" else 1,
                                 result.stdout + result.stderr)
                if stage != "DEVELOPMENT":
                    self.assertIn("P0 P0_ACCEPTANCE_STAGE", result.stdout)

    def test_each_missing_acceptance_field_blocks_audit(self) -> None:
        for line in ACCEPTANCE.splitlines(keepends=True):
            with self.subTest(field=line.split(":")[0]), tempfile.TemporaryDirectory() as temp:
                root = Path(temp)
                write_project(root, status="ACCEPTED_RISK", severity="P0",
                              acceptance=ACCEPTANCE.replace(line, ""))
                result = cli(root, "audit")
                self.assertNotEqual(result.returncode, 0, result.stdout)
                self.assertIn("P0 P0_ACCEPTANCE_FIELD", result.stdout)


if __name__ == "__main__":
    unittest.main()
