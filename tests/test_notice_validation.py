from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from scripts.validate_project import validate


def write_project(root: Path, notice_lines: list[str]) -> None:
    governance = root / "governance"
    notices = governance / "notices"
    notices.mkdir(parents=True)
    (governance / "project-manifest.md").write_text(
        "---\n"
        "artifact_id: PROJECT-NOTICE-001\n"
        "artifact_type: PROJECT_MANIFEST\n"
        "project_id: PROJECT-NOTICE-001\n"
        "project_baseline: CONTRACT-v0.1.0\n"
        "candidate_baseline: CONTRACT-v0.2.0\n"
        "artifact_version: v0.1.0\n"
        "status: DRAFT\n"
        "owner: TEST\n"
        "upstream_ids: []\n"
        "---\n",
        encoding="utf-8",
        newline="\n",
    )
    (notices / "NOTICE-001.md").write_text(
        "---\n"
        "artifact_id: NOTICE-001\n"
        "artifact_type: NOTICE\n"
        "project_id: PROJECT-NOTICE-001\n"
        "project_baseline: CONTRACT-v0.2.0\n"
        "artifact_version: v0.1.0\n"
        "status: DRAFT\n"
        "owner: TEST\n"
        "upstream_ids: []\n"
        + "\n".join(notice_lines)
        + "\n---\n",
        encoding="utf-8",
        newline="\n",
    )


def codes(lines: list[str]) -> set[str]:
    with tempfile.TemporaryDirectory(prefix="psw-notice-") as temp_dir:
        root = Path(temp_dir)
        write_project(root, lines)
        return {item.code for item in validate(root, baseline_mode="candidate")}


class NoticeValidationTests(unittest.TestCase):
    def test_notice_status_uses_its_own_enum(self) -> None:
        result = codes([
            "notice_status: ACTIVE",
            "affected_ids: [PROJECT-NOTICE-001]",
            "affected_paths: [governance/**]",
            "coupling: [SCHEMA]",
        ])
        self.assertIn("NOTICE_STATUS_ENUM", result)

    def test_coupling_uses_its_own_enum(self) -> None:
        result = codes([
            "notice_status: OPEN",
            "affected_ids: [PROJECT-NOTICE-001]",
            "affected_paths: [governance/**]",
            "coupling: [COSMETIC]",
        ])
        self.assertIn("NOTICE_COUPLING_ENUM", result)

    def test_notice_state_requires_its_coupled_fields(self) -> None:
        result = codes([
            "notice_status: IN_PROGRESS",
            "affected_ids: [PROJECT-NOTICE-001]",
            "affected_paths: [governance/**]",
            "coupling: [SCHEMA]",
        ])
        self.assertIn("NOTICE_STATE_FIELD", result)

    def test_valid_in_progress_notice_passes_notice_checks(self) -> None:
        result = codes([
            "notice_status: IN_PROGRESS",
            "affected_ids: [PROJECT-NOTICE-001]",
            "affected_paths: [governance/**]",
            "coupling: [SCHEMA]",
            "migration_tasks: [MIG-001]",
        ])
        self.assertFalse(any(code.startswith("NOTICE_") for code in result), result)


if __name__ == "__main__":
    unittest.main()
