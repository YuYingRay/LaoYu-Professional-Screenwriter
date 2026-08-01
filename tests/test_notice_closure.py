from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from scripts.validate_project import canonical_digest, validate


def artifact_text(
    artifact_id: str,
    artifact_type: str,
    *,
    upstream: list[str] | None = None,
    schema_refs: list[str] | None = None,
    version: str = "v2.0.0",
) -> str:
    upstream_value = ", ".join(upstream or [])
    schema_line = f"schema_refs: [{', '.join(schema_refs)}]\n" if schema_refs else ""
    return (
        "---\n"
        f"artifact_id: {artifact_id}\n"
        f"artifact_type: {artifact_type}\n"
        "project_id: PROJECT-CHANGE-001\n"
        "project_baseline: BASELINE-B\n"
        f"artifact_version: {version}\n"
        "status: DRAFT\n"
        "owner: TEST\n"
        f"upstream_ids: [{upstream_value}]\n"
        f"{schema_line}"
        "---\n"
        f"# {artifact_id}\n"
    )


def write_change_project(
    root: Path,
    *,
    affected_ids: list[str],
    coupling: list[str],
    changed_baseline: str | None = None,
    changed_schema_sections: list[str] | None = None,
    no_content_change: set[str] | None = None,
) -> None:
    (root / "governance" / "notices").mkdir(parents=True, exist_ok=True)
    (root / "development" / "scene-cards").mkdir(parents=True, exist_ok=True)
    (root / "production" / "handoff").mkdir(parents=True, exist_ok=True)
    (root / "assets").mkdir(parents=True, exist_ok=True)
    (root / "governance" / "project-manifest.md").write_text(
        "---\nartifact_id: PROJECT-CHANGE-001\nartifact_type: PROJECT_MANIFEST\n"
        "project_id: PROJECT-CHANGE-001\nproject_baseline: BASELINE-A\n"
        "candidate_baseline: BASELINE-B\nartifact_version: v1.0.0\nstatus: DRAFT\n"
        "owner: TEST\nupstream_ids: []\n---\n",
        encoding="utf-8", newline="\n",
    )
    paths = {
        "BIBLE-CHANGE-001": root / "development" / "story-bible.md",
        "DEL-OUTLINE-001": root / "development" / "outline.md",
        "SC-001": root / "development" / "scene-cards" / "SC-001.md",
        "DEL-HANDOFF-001": root / "production" / "handoff" / "handoff.md",
        "ASSET-PROP-001": root / "assets" / "prop.md",
    }
    paths["BIBLE-CHANGE-001"].write_text(
        artifact_text("BIBLE-CHANGE-001", "STORY_BIBLE"), encoding="utf-8", newline="\n"
    )
    paths["DEL-OUTLINE-001"].write_text(
        artifact_text("DEL-OUTLINE-001", "OUTLINE", upstream=["BIBLE-CHANGE-001"]),
        encoding="utf-8", newline="\n",
    )
    paths["SC-001"].write_text(
        artifact_text("SC-001", "SCENE_CARD", upstream=["DEL-OUTLINE-001"]),
        encoding="utf-8", newline="\n",
    )
    paths["DEL-HANDOFF-001"].write_text(
        artifact_text("DEL-HANDOFF-001", "PRODUCTION_HANDOFF"), encoding="utf-8", newline="\n"
    )
    paths["ASSET-PROP-001"].write_text(
        artifact_text("ASSET-PROP-001", "ASSET", schema_refs=["export_scope"]),
        encoding="utf-8", newline="\n",
    )

    no_change = no_content_change or set()
    records: list[str] = []
    for index, artifact_id in enumerate(affected_ids, start=1):
        digest = canonical_digest(paths[artifact_id])
        disposition = "NO_CONTENT_CHANGE" if artifact_id in no_change else "CONTENT_CHANGED"
        old_digest = digest if disposition == "NO_CONTENT_CHANGE" else "sha256:" + f"{index:064x}"[-64:]
        reason = "Baseline selector hit; bytes already compatible." if disposition == "NO_CONTENT_CHANGE" else "Migrated content."
        records.append(
            "```change-record\n"
            f"record_id: CHG-{index:03d}\n"
            f"artifact_id: {artifact_id}\n"
            "old_version: v1.0.0\n"
            "new_version: v2.0.0\n"
            f"old_digest: {old_digest}\n"
            f"new_digest: {digest}\n"
            f"disposition: {disposition}\n"
            f"reason: {reason}\n"
            "```\n"
        )
    baseline_line = f"changed_baseline: {changed_baseline}\n" if changed_baseline else ""
    sections_line = (
        f"changed_schema_sections: [{', '.join(changed_schema_sections or [])}]\n"
        if changed_schema_sections else ""
    )
    notice = root / "governance" / "notices" / "NOTICE-CHANGE-001.md"
    notice.write_text(
        "---\nartifact_id: NOTICE-CHANGE-001\nartifact_type: NOTICE\n"
        "project_id: PROJECT-CHANGE-001\nproject_baseline: BASELINE-B\n"
        "artifact_version: v1.0.0\nstatus: DRAFT\nowner: TEST\n"
        "upstream_ids: [BIBLE-CHANGE-001]\nnotice_status: VERIFIED\n"
        f"affected_ids: [{', '.join(affected_ids)}]\n"
        "affected_paths: [development/**, production/**, assets/**]\n"
        f"coupling: [{', '.join(coupling)}]\n"
        "verification_refs: [RUN-CHANGE-001]\n"
        f"{baseline_line}{sections_line}"
        f"change_records: [{', '.join(f'CHG-{index:03d}' for index in range(1, len(records) + 1))}]\n"
        "---\n# E2E-CHANGE\n\n"
        + "\n".join(records),
        encoding="utf-8", newline="\n",
    )


def codes(root: Path) -> set[str]:
    return {item.code for item in validate(root, baseline_mode="candidate")}


class NoticeClosureTests(unittest.TestCase):
    def test_transitive_reverse_closure_passes_and_omission_fails(self) -> None:
        with tempfile.TemporaryDirectory(prefix="psw-change-") as temp_dir:
            root = Path(temp_dir)
            expected = ["BIBLE-CHANGE-001", "DEL-OUTLINE-001", "SC-001"]
            write_change_project(root, affected_ids=expected, coupling=["UPSTREAM"])
            self.assertFalse(any(code.startswith("NOTICE_AFFECTED") for code in codes(root)))
            write_change_project(root, affected_ids=expected[:-1], coupling=["UPSTREAM"])
            self.assertIn("NOTICE_AFFECTED_SET_MISSING", codes(root))

    def test_baseline_selector_finds_unconnected_artifact(self) -> None:
        with tempfile.TemporaryDirectory(prefix="psw-change-baseline-") as temp_dir:
            root = Path(temp_dir)
            expected = [
                "BIBLE-CHANGE-001", "DEL-OUTLINE-001", "SC-001",
                "DEL-HANDOFF-001", "ASSET-PROP-001",
            ]
            write_change_project(
                root, affected_ids=expected[:-2], coupling=["UPSTREAM", "BASELINE"],
                changed_baseline="BASELINE-B",
            )
            self.assertIn("NOTICE_AFFECTED_SET_MISSING", codes(root))

    def test_schema_selector_finds_declared_section_reference(self) -> None:
        with tempfile.TemporaryDirectory(prefix="psw-change-schema-") as temp_dir:
            root = Path(temp_dir)
            expected = ["BIBLE-CHANGE-001", "DEL-OUTLINE-001", "SC-001", "ASSET-PROP-001"]
            write_change_project(
                root, affected_ids=expected[:-1], coupling=["UPSTREAM", "SCHEMA"],
                changed_schema_sections=["export_scope"],
            )
            self.assertIn("NOTICE_AFFECTED_SET_MISSING", codes(root))

    def test_each_affected_artifact_requires_versioned_record_or_reasoned_no_change(self) -> None:
        with tempfile.TemporaryDirectory(prefix="psw-change-record-") as temp_dir:
            root = Path(temp_dir)
            expected = ["BIBLE-CHANGE-001", "DEL-OUTLINE-001", "SC-001"]
            write_change_project(
                root, affected_ids=expected, coupling=["UPSTREAM"],
                no_content_change={"SC-001"},
            )
            self.assertFalse(any(code.startswith("NOTICE_CHANGE") for code in codes(root)))
            notice = root / "governance" / "notices" / "NOTICE-CHANGE-001.md"
            notice.write_text(
                notice.read_text(encoding="utf-8").replace("new_version: v2.0.0", "new_version: v1.0.0", 1),
                encoding="utf-8", newline="\n",
            )
            self.assertIn("NOTICE_CHANGE_VERSION", codes(root))


if __name__ == "__main__":
    unittest.main()
