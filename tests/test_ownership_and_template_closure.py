from __future__ import annotations

import copy
import json
import tempfile
import unittest
from pathlib import Path
from subprocess import CompletedProcess
from unittest.mock import patch

from scripts.ownership import (
    _ignored_paths,
    analyze_ownership,
    classify_path,
    hygiene_findings,
    template_closure_findings,
)
from scripts.validate_project import validate


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "governance" / "control-schema.json"


def schema() -> dict:
    return json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))


def write_manifest(root: Path) -> None:
    governance = root / "governance"
    governance.mkdir(parents=True)
    (governance / "project-manifest.md").write_text(
        "---\n"
        "artifact_id: PROJECT-TEST-001\n"
        "artifact_type: PROJECT_MANIFEST\n"
        "project_id: PROJECT-TEST-001\n"
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


class OwnershipTests(unittest.TestCase):
    def test_excluded_cache_precedes_tooling_owner(self) -> None:
        record, findings = classify_path(
            "scripts/__pycache__/module.pyc",
            schema()["ownership"],
            tracked=False,
            ignored=True,
        )
        self.assertEqual(record.owner, "excluded")
        self.assertEqual(record.matched_rules, ("OWN-EXCLUDED",))
        self.assertEqual(findings, [])

    def test_gitignored_host_runtime_is_excluded_without_allowlist(self) -> None:
        data = schema()["ownership"]
        self.assertEqual(data["untracked_allowlist"], [])
        record, findings = classify_path(
            ".claude/scheduled_tasks.lock",
            data,
            tracked=False,
            ignored=True,
        )
        self.assertEqual(record.owner, "excluded")
        self.assertEqual(findings, [])

    def test_ignored_path_query_uses_nul_protocol(self) -> None:
        completed = CompletedProcess(
            args=[], returncode=0,
            stdout=".claude/scheduled_tasks.lock\0scripts/__pycache__/module.pyc\0",
            stderr="",
        )
        with patch("scripts.ownership.subprocess.run", return_value=completed) as run:
            ignored = _ignored_paths(
                ROOT,
                [".claude/scheduled_tasks.lock", "scripts/__pycache__/module.pyc"],
            )
        command = run.call_args.args[0]
        self.assertIn("-z", command)
        self.assertIn("\0", run.call_args.kwargs["input"])
        self.assertEqual(
            ignored,
            {".claude/scheduled_tasks.lock", "scripts/__pycache__/module.pyc"},
        )

    def test_overlap_reports_multi_owned_file(self) -> None:
        data = schema()
        duplicate = copy.deepcopy(data["ownership"]["rules"][2])
        duplicate["id"] = "OWN-TEMPLATE-DUPLICATE"
        data["ownership"]["rules"].append(duplicate)
        with tempfile.TemporaryDirectory(prefix="psw-owner-") as temp_dir:
            root = Path(temp_dir)
            (root / "templates").mkdir()
            path = root / "templates" / "sample.md"
            path.write_text("sample", encoding="utf-8")
            report = analyze_ownership(root, data, tracked_paths={"templates/sample.md"})
        self.assertIn("MULTI_OWNED_FILE", {item.code for item in report.findings})

    def test_arbitrary_untracked_file_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory(prefix="psw-owner-") as temp_dir:
            root = Path(temp_dir)
            (root / "notes.txt").write_text("unowned", encoding="utf-8")
            report = analyze_ownership(root, schema(), tracked_paths=set())
        self.assertIn("UNDECLARED_INSTALL_CONTENT", {item.code for item in report.findings})

    def test_undeclared_empty_directory_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory(prefix="psw-owner-") as temp_dir:
            root = Path(temp_dir)
            (root / "mystery").mkdir()
            report = analyze_ownership(root, schema(), tracked_paths=set())
        self.assertIn("UNDECLARED_EMPTY_DIR", {item.code for item in report.findings})

    def test_fixture_owner_is_specific_and_does_not_overlap(self) -> None:
        with tempfile.TemporaryDirectory(prefix="psw-owner-") as temp_dir:
            root = Path(temp_dir)
            path = root / "tests" / "alpha-fixture" / "story" / "bible.md"
            path.parent.mkdir(parents=True)
            path.write_text("fixture", encoding="utf-8")
            report = analyze_ownership(
                root, schema(), tracked_paths={"tests/alpha-fixture/story/bible.md"}
            )
        record = next(item for item in report.records if item.path.endswith("bible.md"))
        self.assertEqual(record.owner, "fixture-project:alpha-fixture")
        self.assertFalse(report.findings)

    def test_installation_root_validation_only_scans_root_project_owner(self) -> None:
        with tempfile.TemporaryDirectory(prefix="psw-owner-") as temp_dir:
            root = Path(temp_dir)
            write_manifest(root)
            (root / "governance" / "control-schema.json").write_text(
                json.dumps(schema(), ensure_ascii=False), encoding="utf-8"
            )
            templates = root / "templates"
            templates.mkdir()
            (templates / "invalid.md").write_text(
                "---\nstatus: LOCKED\n---\n[[UNFILLED]]\n", encoding="utf-8"
            )
            findings = validate(root, baseline_mode="candidate")
        self.assertFalse(any(item.path.endswith("invalid.md") for item in findings))


class TemplateClosureTests(unittest.TestCase):
    def test_every_template_is_registered_or_declared_fragment(self) -> None:
        findings = template_closure_findings(ROOT, schema())
        self.assertFalse(findings, "\n".join(f"{item.code}: {item.path}" for item in findings))

    def test_unregistered_template_reports_stable_code(self) -> None:
        with tempfile.TemporaryDirectory(prefix="psw-template-closure-") as temp_dir:
            root = Path(temp_dir)
            templates = root / "templates"
            templates.mkdir()
            (templates / "new.md").write_text("new", encoding="utf-8")
            findings = template_closure_findings(root, schema())
        self.assertIn("UNTESTED_TEMPLATE", {item.code for item in findings})

    def test_feature_scenario_requires_matching_scene_cards(self) -> None:
        entry = schema()["template_closure"]["templates/feature-screenplay.fountain"]
        self.assertEqual(entry["kind"], "scenario")
        self.assertEqual(entry["scene_card_policy"], "match_script_scenes")

    def test_readme_is_not_hidden_by_project_validator(self) -> None:
        source = (ROOT / "scripts" / "validate_project.py").read_text(encoding="utf-8")
        self.assertNotIn('"README.md"', source)

    def test_hygiene_audit_is_clean_after_readme_boundary_migration(self) -> None:
        findings = hygiene_findings(ROOT, schema())
        self.assertEqual(findings, [])


class StrictHygieneTests(unittest.TestCase):
    def test_schema_enables_strict_ownership(self) -> None:
        self.assertEqual(schema()["ownership"]["enforcement"], "strict")

    def test_real_installation_ownership_is_clean(self) -> None:
        report = analyze_ownership(ROOT, schema())
        self.assertEqual(report.findings, ())


if __name__ == "__main__":
    unittest.main()
