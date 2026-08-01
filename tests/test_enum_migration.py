from __future__ import annotations

import csv
import json
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "governance" / "control-schema.json"
MAP = ROOT / "governance" / "enum-migration-map.tsv"
CANONICAL_ENUMS = {
    "project_stages",
    "work_actions",
    "finding_statuses",
    "source_statuses",
    "mystery_statuses",
    "decision_statuses",
    "deprecation_statuses",
    "rights_statuses",
}
UNSUPPORTED_TOKENS = {
    "INTAKE",
    "ADVERSARIAL_REVIEW",
    "PRODUCTION_PACKAGE",
    "IN REVIEW",
    "ACCEPTED RISK",
    "DELIVERED",
}


def tracked_story_text() -> str:
    paths = subprocess.check_output(
        ["git", "ls-files", "*.md", "*.fountain"], cwd=ROOT, text=True, encoding="utf-8"
    ).splitlines()
    return "\n".join((ROOT / path).read_text(encoding="utf-8") for path in paths)


class EnumMigrationTests(unittest.TestCase):
    def test_domain_enums_are_schema_authority(self) -> None:
        schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
        self.assertTrue(CANONICAL_ENUMS.issubset(schema))
        self.assertIn("ARCHIVED", schema["project_stages"])
        self.assertIn("ACTIVE", schema["source_statuses"])
        self.assertIn("ARCHIVED", schema["rights_statuses"])
        self.assertEqual(schema["work_actions"][0], "DISCOVER")
        self.assertIn("ACCEPTED_RISK", schema["finding_statuses"])
        contract = (ROOT / "governance" / "control-plane-contract.md").read_text(encoding="utf-8")
        self.assertIn("### 领域枚举", contract)
        for name in CANONICAL_ENUMS:
            self.assertIn(f"`{name}`", contract)

    def test_unsupported_spellings_are_absent(self) -> None:
        text = tracked_story_text()
        for token in UNSUPPORTED_TOKENS:
            self.assertNotIn(token, text, token)

    def test_deliverable_matrix_uses_typed_control_states(self) -> None:
        text = (ROOT / "tests" / "expected-deliverables.md").read_text(encoding="utf-8")
        matrix = text.split("# 4. 交付物矩阵", 1)[1].split("\n---\n", 1)[0]
        for token in ("ACTIVE", "REVIEWED", "DELIVERED", "CLOSED/ACCEPTED"):
            self.assertNotIn(token, matrix)
        self.assertIn("APPROVED + notice_status=CLOSED", matrix)
        self.assertIn("LOCKED + PRODUCTION_READY", matrix)
        self.assertIn("LOCKED + project_stage=RELEASE", matrix)

    def test_explicit_enum_map_is_schema_resolved(self) -> None:
        schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
        with MAP.open(encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle, delimiter="\t"))
        self.assertGreater(len(rows), 0)
        self.assertEqual({row["action"] for row in rows}, {"MIGRATE", "PRESERVE"})
        for row in rows:
            self.assertIn(row["domain"], schema, row)
            self.assertIn(row["target"], schema[row["domain"]], row)

    def test_open_notice_tracks_enum_migration(self) -> None:
        notice = (ROOT / "governance" / "notices" / "NOTICE-CONTRACT-001.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("MIG-WP3B-ENUMS", notice)
        self.assertIn("enum-migration-map.tsv", notice)


if __name__ == "__main__":
    unittest.main()
