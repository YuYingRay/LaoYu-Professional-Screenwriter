from __future__ import annotations

import json
import shutil
import tempfile
import unittest
from pathlib import Path

from scripts import run_protocol


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_SOURCE = ROOT / "governance" / "control-schema.json"
RUN_ID = "RUN-MUTATION-001"


def replace_line(path: Path, key: str, value: str) -> None:
    lines = path.read_text(encoding="utf-8").splitlines()
    path.write_text(
        "\n".join(value if line.startswith(key) else line for line in lines) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def write_project(root: Path) -> tuple[Path, Path, Path]:
    governance = root / "governance"
    development = root / "development"
    governance.mkdir(parents=True)
    development.mkdir(parents=True)
    schema = governance / "control-schema.json"
    shutil.copyfile(SCHEMA_SOURCE, schema)
    (governance / "project-manifest.md").write_text(
        "---\n"
        "artifact_id: PROJECT-RUN-001\n"
        "artifact_type: PROJECT_MANIFEST\n"
        "project_id: PROJECT-RUN-001\n"
        "project_baseline: BASELINE-A\n"
        "artifact_version: v1.0.0\n"
        "status: DRAFT\n"
        "owner: TEST\n"
        "upstream_ids: []\n"
        "---\n",
        encoding="utf-8",
        newline="\n",
    )
    artifact = development / "story-bible.md"
    artifact.write_text(
        "---\n"
        "artifact_id: BIBLE-RUN-001\n"
        "artifact_type: STORY_BIBLE\n"
        "project_id: PROJECT-RUN-001\n"
        "project_baseline: BASELINE-A\n"
        "artifact_version: v1.0.0\n"
        "status: LOCKED\n"
        "owner: TEST\n"
        "upstream_ids: [PROJECT-RUN-001]\n"
        "reviewer: TEST\n"
        "approver: TEST\n"
        f"test_run_id: {RUN_ID}\n"
        "conformance_level: HUMAN_REVIEWED\n"
        "lock_scope: FULL\n"
        "content_digest: PENDING\n"
        "---\n"
        "# Story Bible\n",
        encoding="utf-8",
        newline="\n",
    )
    run_path = run_protocol.create_run(root, RUN_ID, schema, command="mutation-test")
    return schema, artifact, run_path


class RunProtocolTests(unittest.TestCase):
    def test_preflight_create_final_is_non_recursive_and_complete(self) -> None:
        with tempfile.TemporaryDirectory(prefix="psw-run-full-") as temp_dir:
            root = Path(temp_dir)
            governance = root / "governance"
            development = root / "development"
            governance.mkdir(parents=True)
            development.mkdir(parents=True)
            schema = governance / "control-schema.json"
            shutil.copyfile(SCHEMA_SOURCE, schema)
            artifact = development / "story-bible.md"
            artifact.write_text(
                "---\nartifact_id: BIBLE-RUN-001\nartifact_type: STORY_BIBLE\n"
                "project_id: PROJECT-RUN-001\nproject_baseline: BASELINE-A\n"
                "artifact_version: v1.0.0\nstatus: LOCKED\nowner: TEST\nupstream_ids: []\n"
                "reviewer: TEST\napprover: TEST\ntest_run_id: RUN-MUTATION-001\n"
                "conformance_level: HUMAN_REVIEWED\nlock_scope: FULL\ncontent_digest: PENDING\n---\n",
                encoding="utf-8", newline="\n",
            )
            self.assertEqual(run_protocol.preflight(root, RUN_ID, schema)["result"], "PASS")
            before = run_protocol.source_snapshot_digest(root, schema)
            run_path = run_protocol.create_run(root, RUN_ID, schema, command="full-test")
            after = run_protocol.source_snapshot_digest(root, schema)
            self.assertEqual(before, after)
            self.assertEqual(run_protocol.final_check(root, run_path, schema)["result"], "PASS")
            run = json.loads(run_path.read_text(encoding="utf-8"))
            self.assertEqual(run["profile"], "final")
            self.assertEqual(run["result"], "PASS")
            self.assertEqual(run["findings"], [])
            self.assertNotIn("runs/", "\n".join(run["artifact_digests"]))

    def test_ten_mutations_invalidate_an_existing_run(self) -> None:
        def mutate_run(path: Path, key: str, value: object) -> None:
            data = json.loads(path.read_text(encoding="utf-8"))
            data[key] = value
            path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")

        mutations = {
            "test_run_id": (
                lambda root, schema, artifact, run: replace_line(artifact, "test_run_id:", "test_run_id: RUN-OTHER-001"),
                "RUN_ID_MISMATCH",
            ),
            "schema": (
                lambda root, schema, artifact, run: replace_line(schema, '  "schema_version":', '  "schema_version": "v9.9.9",'),
                "SCHEMA_DIGEST_MISMATCH",
            ),
            "validation_profile": (
                lambda root, schema, artifact, run: mutate_run(run, "profile", "preflight"),
                "RUN_PROFILE_MISMATCH",
            ),
            "managed_untracked_file": (
                lambda root, schema, artifact, run: (root / "development" / "extra.md").write_text("extra\n", encoding="utf-8"),
                "SOURCE_SNAPSHOT_MISMATCH",
            ),
            "artifact_body": (
                lambda root, schema, artifact, run: artifact.write_text(artifact.read_text(encoding="utf-8") + "changed\n", encoding="utf-8", newline="\n"),
                "SOURCE_SNAPSHOT_MISMATCH",
            ),
            "missing_run": (
                lambda root, schema, artifact, run: run.unlink(),
                "RUN_MISSING",
            ),
            "illegal_digest": (
                lambda root, schema, artifact, run: replace_line(artifact, "content_digest:", "content_digest: sha256:bad"),
                "INVALID_CONTENT_DIGEST",
            ),
            "rename": (
                lambda root, schema, artifact, run: artifact.rename(artifact.with_name("renamed-bible.md")),
                "SOURCE_SNAPSHOT_MISMATCH",
            ),
            "split_or_merge": (
                lambda root, schema, artifact, run: (root / "development" / "part-2.md").write_text("part\n", encoding="utf-8"),
                "SOURCE_SNAPSHOT_MISMATCH",
            ),
            "exclude_rule": (
                lambda root, schema, artifact, run: replace_line(schema, '    "self_exclusion":', '    "self_exclusion": "runs/**",\n    "mutation_marker": true'),
                "SCHEMA_DIGEST_MISMATCH",
            ),
        }

        for name, (mutation, expected_code) in mutations.items():
            with self.subTest(name=name), tempfile.TemporaryDirectory(prefix=f"psw-run-{name}-") as temp_dir:
                root = Path(temp_dir)
                schema, artifact, run_path = write_project(root)
                mutation(root, schema, artifact, run_path)
                result = run_protocol.final_check(root, run_path, schema)
                self.assertEqual(result["result"], "FAIL")
                self.assertIn(expected_code, {item["code"] for item in result["findings"]})

    def test_snapshot_binds_paths_and_file_count(self) -> None:
        with tempfile.TemporaryDirectory(prefix="psw-run-paths-") as temp_dir:
            root = Path(temp_dir)
            schema, artifact, _ = write_project(root)
            before = run_protocol.source_snapshot_digest(root, schema)
            artifact.rename(artifact.with_name("same-content-new-name.md"))
            after = run_protocol.source_snapshot_digest(root, schema)
            self.assertNotEqual(before, after)


if __name__ == "__main__":
    unittest.main()
