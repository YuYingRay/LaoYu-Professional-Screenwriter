from __future__ import annotations

import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"


def write_project(root: Path, *, candidate: str | None, artifact_baseline: str) -> None:
    (root / "governance").mkdir(parents=True)
    (root / "story").mkdir(parents=True)
    candidate_line = f"candidate_baseline: {candidate}\n" if candidate else ""
    (root / "governance" / "project-manifest.md").write_text(
        "---\n"
        "artifact_id: PROJECT-TOY-001\n"
        "artifact_type: PROJECT_MANIFEST\n"
        "project_id: PROJECT-TOY-001\n"
        "project_baseline: BASELINE-A\n"
        f"{candidate_line}"
        "artifact_version: v0.1.0\n"
        "status: DRAFT\n"
        "owner: TEST\n"
        "upstream_ids: []\n"
        "---\n",
        encoding="utf-8",
        newline="\n",
    )
    (root / "story" / "story-bible.md").write_text(
        "---\n"
        "artifact_id: BIBLE-TOY-001\n"
        "artifact_type: STORY_BIBLE\n"
        "project_id: PROJECT-TOY-001\n"
        f"project_baseline: {artifact_baseline}\n"
        "artifact_version: v0.1.0\n"
        "status: DRAFT\n"
        "owner: TEST\n"
        "upstream_ids: []\n"
        "---\n",
        encoding="utf-8",
        newline="\n",
    )


def load_run_protocol():
    path = SCRIPTS / "run_protocol.py"
    spec = importlib.util.spec_from_file_location("run_protocol", path)
    if spec is None or spec.loader is None:
        raise AssertionError("run protocol module cannot be loaded")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class BootstrapGateTests(unittest.TestCase):
    def test_validate_project_selects_active_or_candidate_baseline(self) -> None:
        with tempfile.TemporaryDirectory(prefix="psw-baseline-test-") as temp_dir:
            root = Path(temp_dir)
            write_project(root, candidate="BASELINE-B", artifact_baseline="BASELINE-B")

            candidate = subprocess.run(
                [sys.executable, str(SCRIPTS / "validate_project.py"), str(root), "--baseline", "candidate"],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(candidate.returncode, 0, candidate.stdout + candidate.stderr)

            active = subprocess.run(
                [sys.executable, str(SCRIPTS / "validate_project.py"), str(root), "--baseline", "active", "--json"],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertNotEqual(active.returncode, 0)
            self.assertIn("BASELINE_DRIFT", active.stdout)

    def test_candidate_mode_fails_closed_without_candidate_baseline(self) -> None:
        with tempfile.TemporaryDirectory(prefix="psw-baseline-test-") as temp_dir:
            root = Path(temp_dir)
            write_project(root, candidate=None, artifact_baseline="BASELINE-A")
            result = subprocess.run(
                [sys.executable, str(SCRIPTS / "validate_project.py"), str(root), "--baseline", "candidate", "--json"],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("CANDIDATE_BASELINE_MISSING", result.stdout)

    def test_lint_audit_reports_but_does_not_block(self) -> None:
        with tempfile.TemporaryDirectory(prefix="psw-lint-audit-") as temp_dir:
            copy = Path(temp_dir) / "skill"
            shutil.copytree(
                ROOT,
                copy,
                ignore=shutil.ignore_patterns(".git", "__pycache__", "*.pyc"),
            )
            contract = copy / "governance" / "control-plane-contract.md"
            contract.write_text(
                contract.read_text(encoding="utf-8").replace("finding_id", "finding_id_manual", 1),
                encoding="utf-8",
                newline="\n",
            )
            result = subprocess.run(
                [sys.executable, str(copy / "scripts" / "lint_repo.py"), str(copy), "--mode", "audit"],
                text=True,
                capture_output=True,
                check=False,
            )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("GENERATED_BLOCK_DRIFT", result.stdout)
        self.assertNotIn("control-plane-file-map.md is missing", result.stdout)

    def test_minimum_template_instantiation_passes(self) -> None:
        result = subprocess.run(
            [sys.executable, str(SCRIPTS / "test_template_instantiation.py"), str(ROOT)],
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("PASS: minimum template instantiation", result.stdout)

    def test_candidate_check_all_chains_bootstrap_tools(self) -> None:
        result = subprocess.run(
            [sys.executable, str(SCRIPTS / "check_all.py"), str(ROOT), "--baseline", "candidate", "--mode", "audit"],
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("PASS: lint_repo audit", result.stdout)
        self.assertIn("PASS: feature fixture active baseline", result.stdout)
        self.assertIn("PASS: vertical fixture active baseline", result.stdout)
        self.assertIn("PASS: minimum template instantiation", result.stdout)

    def test_check_all_is_independent_of_callers_working_directory(self) -> None:
        with tempfile.TemporaryDirectory(prefix="psw-check-cwd-") as temp_dir:
            result = subprocess.run(
                [sys.executable, str(SCRIPTS / "check_all.py"), str(ROOT), "--baseline", "candidate", "--mode", "audit"],
                cwd=temp_dir,
                text=True,
                capture_output=True,
                check=False,
            )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_toy_run_preflight_create_final_is_non_recursive(self) -> None:
        protocol = load_run_protocol()
        with tempfile.TemporaryDirectory(prefix="psw-run-test-") as temp_dir:
            root = Path(temp_dir)
            write_project(root, candidate=None, artifact_baseline="BASELINE-A")
            artifact = root / "story" / "story-bible.md"
            text = artifact.read_text(encoding="utf-8")
            text = text.replace("status: DRAFT", "status: LOCKED")
            text = text.replace("owner: TEST", "owner: TEST\nreviewer: TEST\napprover: TEST\ntest_run_id: RUN-TOY-001\nconformance_level: HUMAN_REVIEWED\nlock_scope: FULL\ncontent_digest: PENDING")
            artifact.write_text(text, encoding="utf-8", newline="\n")

            schema = ROOT / "governance" / "control-schema.json"
            preflight = protocol.preflight(root, "RUN-TOY-001", schema)
            self.assertEqual(preflight["result"], "PASS")
            before = protocol.source_snapshot_digest(root, schema)
            run_path = protocol.create_run(root, "RUN-TOY-001", schema, command="bootstrap-test")
            after = protocol.source_snapshot_digest(root, schema)
            self.assertEqual(before, after)

            final = protocol.final_check(root, run_path, schema)
            self.assertEqual(final["result"], "PASS")
            run = json.loads(run_path.read_text(encoding="utf-8"))
            for field in [
                "run_id",
                "source_snapshot_digest",
                "artifact_digests",
                "profile",
                "command",
                "validator_digest",
                "schema_digest",
                "findings",
                "result",
                "timestamp",
            ]:
                self.assertIn(field, run)


if __name__ == "__main__":
    unittest.main()
