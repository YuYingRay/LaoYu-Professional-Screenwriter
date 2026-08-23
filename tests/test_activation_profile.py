from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts" / "validate_project.py"
FIXTURE = ROOT / "tests" / "activation-state-fixture"


def run_validator(project: Path, baseline: str | None = None) -> subprocess.CompletedProcess[str]:
    command = [sys.executable, str(VALIDATOR), str(project), "--mode", "strict", "--json"]
    if baseline:
        command.extend(["--baseline", baseline])
    return subprocess.run(command, text=True, capture_output=True, check=False)


def write_toy_project(root: Path, candidate_line: str, artifact_baseline: str) -> None:
    (root / "governance").mkdir(parents=True)
    (root / "development").mkdir(parents=True)
    (root / "governance" / "project-manifest.md").write_text(
        "---\nartifact_id: PROJECT-AUTO-001\nartifact_type: PROJECT_MANIFEST\n"
        "project_id: PROJECT-AUTO-001\nproject_baseline: BASELINE-A\n"
        f"{candidate_line}artifact_version: v0.1.0\nstatus: DRAFT\nowner: TEST\nupstream_ids: []\n---\n",
        encoding="utf-8",
        newline="\n",
    )
    (root / "development" / "story-bible.md").write_text(
        "---\nartifact_id: BIBLE-AUTO-001\nartifact_type: STORY_BIBLE\n"
        f"project_id: PROJECT-AUTO-001\nproject_baseline: {artifact_baseline}\n"
        "artifact_version: v0.1.0\nstatus: DRAFT\nowner: TEST\nupstream_ids: []\n---\n",
        encoding="utf-8",
        newline="\n",
    )


class ActivationProfileTests(unittest.TestCase):
    def test_auto_selector_accepts_both_states(self) -> None:
        cases = [
            ("candidate_baseline: BASELINE-B\n", "BASELINE-B"),
            ("candidate_baseline : BASELINE-B\n", "BASELINE-B"),
            ("", "BASELINE-A"),
        ]
        for candidate_line, artifact_baseline in cases:
            with self.subTest(candidate_line=candidate_line), tempfile.TemporaryDirectory() as temp_dir:
                root = Path(temp_dir)
                write_toy_project(root, candidate_line, artifact_baseline)
                result = run_validator(root)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_auto_selector_rejects_malformed_candidate_state(self) -> None:
        malformed = [
            "candidate_baseline: \n",
            "candidate_baseline: [BASELINE-B]\n",
            "candidate_baseline: BASELINE-B\ncandidate_baseline: BASELINE-C\n",
            "candidate_baseline: BASELINE-B\ncandidate_baseline : BASELINE-C\n",
        ]
        for candidate_line in malformed:
            with self.subTest(candidate_line=candidate_line), tempfile.TemporaryDirectory() as temp_dir:
                root = Path(temp_dir)
                write_toy_project(root, candidate_line, "BASELINE-B")
                result = run_validator(root)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("BASELINE_STATE_INVALID", result.stdout)

    def test_explicit_baseline_is_an_assertion_not_an_override(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            write_toy_project(root, "candidate_baseline: BASELINE-B\n", "BASELINE-B")
            result = run_validator(root, "active")
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("BASELINE_MODE_MISMATCH", result.stdout)

    def test_permanent_activation_fixture_passes_auto_strict(self) -> None:
        result = run_validator(FIXTURE)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_activation_fixture_mutations_fail_for_the_intended_reason(self) -> None:
        mutations = {
            "candidate-restored": ("governance/project-manifest.md", "project_baseline: CONTRACT-v0.2.0", "project_baseline: CONTRACT-v0.2.0\ncandidate_baseline: CONTRACT-v0.3.0", "BASELINE_DRIFT"),
            "future-notice": ("governance/notices/NOTICE-HISTORY-001.md", "project_baseline: CONTRACT-v0.1.0", "project_baseline: CONTRACT-v9.0.0", "BASELINE_DRIFT"),
            "wrong-placeholder-path": ("development/story-bible.md", "# Fixture Bible", "# Fixture Bible\n\n[[PROJECT-ID]]", "PLACEHOLDER_LOCKED"),
            "extra-placeholder": ("governance/control-plane-contract.md", "[[PROJECT-ID]]", "[[PROJECT-ID]] [[PROJECT-ID]]", "PLACEHOLDER_ALLOWLIST_DRIFT"),
        }
        for name, (relative, old, new, code) in mutations.items():
            with self.subTest(name=name), tempfile.TemporaryDirectory() as temp_dir:
                copy = Path(temp_dir) / "fixture"
                shutil.copytree(FIXTURE, copy)
                path = copy / relative
                path.write_text(path.read_text(encoding="utf-8").replace(old, new, 1), encoding="utf-8", newline="\n")
                result = run_validator(copy)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn(code, result.stdout)

    def test_active_history_requires_the_registered_ordered_chain(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            copy = Path(temp_dir) / "fixture"
            shutil.copytree(FIXTURE, copy)
            schema = json.loads((ROOT / "governance" / "control-schema.json").read_text(encoding="utf-8"))
            schema["historical_baseline_chains"]["PROJECT-ACTIVATION-FIXTURE-001"] = ["CONTRACT-v0.2.0"]
            (copy / "governance" / "control-schema.json").write_text(
                json.dumps(schema, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n"
            )
            result = run_validator(copy)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("BASELINE_DRIFT", result.stdout)

    def test_registered_active_project_validates_current_notice(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            copy = Path(temp_dir) / "fixture"
            shutil.copytree(FIXTURE, copy)
            current_notice = copy / "governance" / "notices" / "NOTICE-CURRENT-001.md"
            current_notice.write_text(
                "---\nartifact_id: NOTICE-CURRENT-001\nartifact_type: NOTICE\n"
                "project_id: PROJECT-ACTIVATION-FIXTURE-001\n"
                "project_baseline: CONTRACT-v0.2.0\nartifact_version: v0.2.0\n"
                "status: IN_REVIEW\nowner: TEST\nupstream_ids: []\n"
                "notice_status: NOT-A-REAL-STATUS\naffected_ids: []\n"
                "affected_paths: []\ncoupling: [BASELINE]\n---\n",
                encoding="utf-8",
                newline="\n",
            )
            result = run_validator(copy)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("NOTICE_STATUS_ENUM", result.stdout)


if __name__ == "__main__":
    unittest.main()
