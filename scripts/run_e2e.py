#!/usr/bin/env python3
"""Execute the invariant matrix through the real project and aggregate CLIs."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any, Callable

from run_protocol import create_run, write_content_digests
from validate_project import canonical_digest


SKILL_ROOT = Path(__file__).resolve().parents[1]
SCHEMA = SKILL_ROOT / "governance" / "control-schema.json"
MATRIX_PATH = SKILL_ROOT / "tests" / "e2e-invariant-matrix.json"
FIXTURES = {
    "feature": SKILL_ROOT / "tests" / "feature-project-fixture",
    "vertical": SKILL_ROOT / "tests" / "vertical-project-fixture",
    "production": SKILL_ROOT / "tests" / "production-ready-fixture",
}


def replace(path: Path, old: str, new: str) -> None:
    text = path.read_text(encoding="utf-8")
    if old not in text:
        raise AssertionError(f"mutation precondition missing in {path}: {old}")
    path.write_text(text.replace(old, new, 1), encoding="utf-8", newline="\n")


def mutate_orphan_scene(root: Path) -> None:
    path = root / "script" / "master" / "script.fountain"
    path.write_text(path.read_text(encoding="utf-8") + "\n/* SC-999 */\n", encoding="utf-8", newline="\n")


def mutate_baseline(root: Path) -> None:
    replace(root / "production" / "handoff" / "handoff.md", "PROJECT-FEATURE-v1.0.0", "PROJECT-FEATURE-v9.0.0")


def mutate_placeholder(root: Path) -> None:
    path = root / "production" / "handoff" / "handoff.md"
    path.write_text(path.read_text(encoding="utf-8") + "\n[[UNFILLED-E2E]]\n", encoding="utf-8", newline="\n")


def mutate_unaccept_p1(root: Path) -> None:
    replace(root / "development" / "review-reports" / "REVIEW-001.md", "status: ACCEPTED_RISK", "status: OPEN")


def mutate_delete_rights(root: Path) -> None:
    (root / "governance" / "rights-register.md").unlink()


MUTATIONS: dict[str, Callable[[Path], None]] = {
    "orphan_scene": mutate_orphan_scene,
    "baseline_drift": mutate_baseline,
    "locked_placeholder": mutate_placeholder,
    "unaccept_p1": mutate_unaccept_p1,
    "delete_rights": mutate_delete_rights,
}


def refresh_run(root: Path) -> None:
    manifest = (root / "governance" / "project-manifest.md").read_text(encoding="utf-8")
    match = re.search(r"^test_run_id:\s*(\S+)", manifest, re.MULTILINE)
    if not match:
        return
    run_id = match.group(1)
    write_content_digests(root, SCHEMA)
    create_run(root, run_id, SCHEMA, command="e2e isolated mutation")


def artifact_text(artifact_id: str, artifact_type: str, upstream: list[str] | None = None) -> str:
    return (
        "---\n"
        f"artifact_id: {artifact_id}\nartifact_type: {artifact_type}\n"
        "project_id: PROJECT-CHANGE-001\nproject_baseline: BASELINE-B\n"
        "artifact_version: v2.0.0\nstatus: DRAFT\nowner: E2E\n"
        f"upstream_ids: [{', '.join(upstream or [])}]\n---\n# {artifact_id}\n"
    )


def build_change_project(root: Path, omit: str | None) -> None:
    paths = {
        "BIBLE-CHANGE-001": root / "development" / "story-bible.md",
        "DEL-CHANGE-OUTLINE-001": root / "development" / "outline.md",
        "ASSET-CHANGE-001": root / "assets" / "downstream.md",
        "DEL-CHANGE-HANDOFF-001": root / "production" / "handoff" / "handoff.md",
    }
    for path in paths.values():
        path.parent.mkdir(parents=True, exist_ok=True)
    notices = root / "governance" / "notices"
    notices.mkdir(parents=True)
    (root / "governance" / "project-manifest.md").write_text(
        "---\nartifact_id: PROJECT-CHANGE-001\nartifact_type: PROJECT_MANIFEST\n"
        "project_id: PROJECT-CHANGE-001\nproject_baseline: BASELINE-A\n"
        "candidate_baseline: BASELINE-B\nartifact_version: v1.0.0\n"
        "status: DRAFT\nowner: E2E\nupstream_ids: []\n---\n",
        encoding="utf-8", newline="\n",
    )
    paths["BIBLE-CHANGE-001"].write_text(artifact_text("BIBLE-CHANGE-001", "STORY_BIBLE"), encoding="utf-8", newline="\n")
    paths["DEL-CHANGE-OUTLINE-001"].write_text(artifact_text("DEL-CHANGE-OUTLINE-001", "OUTLINE", ["BIBLE-CHANGE-001"]), encoding="utf-8", newline="\n")
    paths["ASSET-CHANGE-001"].write_text(artifact_text("ASSET-CHANGE-001", "ASSET", ["DEL-CHANGE-OUTLINE-001"]), encoding="utf-8", newline="\n")
    paths["DEL-CHANGE-HANDOFF-001"].write_text(artifact_text("DEL-CHANGE-HANDOFF-001", "PRODUCTION_HANDOFF"), encoding="utf-8", newline="\n")

    affected = [item for item in paths if item != omit]
    records: list[str] = []
    record_ids: list[str] = []
    for index, artifact_id in enumerate(affected, 1):
        record_id = f"CHG-{index:03d}"
        record_ids.append(record_id)
        records.append(
            "```change-record\n"
            f"record_id: {record_id}\nartifact_id: {artifact_id}\n"
            "old_version: v1.0.0\nnew_version: v2.0.0\n"
            f"old_digest: sha256:{index:064x}\n"
            f"new_digest: {canonical_digest(paths[artifact_id])}\n"
            "disposition: CONTENT_CHANGED\nreason: E2E migration.\n```\n"
        )
    (notices / "NOTICE-CHANGE-001.md").write_text(
        "---\nartifact_id: NOTICE-CHANGE-001\nartifact_type: NOTICE\n"
        "project_id: PROJECT-CHANGE-001\nproject_baseline: BASELINE-B\n"
        "artifact_version: v1.0.0\nstatus: DRAFT\nowner: E2E\n"
        "upstream_ids: [BIBLE-CHANGE-001]\nnotice_status: VERIFIED\n"
        f"affected_ids: [{', '.join(affected)}]\naffected_paths: [development/**, assets/**, production/**]\n"
        "coupling: [UPSTREAM, BASELINE]\nchanged_baseline: BASELINE-B\n"
        f"change_records: [{', '.join(record_ids)}]\nverification_refs: [RUN-E2E-CHANGE]\n"
        "---\n# E2E-CHANGE\n\n" + "\n".join(records),
        encoding="utf-8", newline="\n",
    )


def run_command(command: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command, cwd=SKILL_ROOT, text=True, encoding="utf-8", errors="replace",
        capture_output=True, check=False,
    )


def assert_expected(row: dict[str, Any], result: subprocess.CompletedProcess[str], label: str) -> None:
    expected_exit = row[f"{label}_exit"]
    if result.returncode != expected_exit:
        raise AssertionError(f"{row['id']} {label} exit {result.returncode} != {expected_exit}\n{result.stdout}\n{result.stderr}")
    code = row["expected_code"]
    if code is None:
        return
    normalized = (result.stdout + result.stderr).replace("\\", "/")
    expected = f"{row['expected_severity']} {code} {row['expected_path']}"
    if label == "check_all":
        expected = f"{row['expected_severity']} {code} {row['expected_path']}"
    if expected not in normalized:
        raise AssertionError(f"{row['id']} missing {expected} in {label} output:\n{normalized}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--keep-temp", action="store_true")
    args = parser.parse_args()
    matrix = json.loads(MATRIX_PATH.read_text(encoding="utf-8"))
    temp_roots: list[Path] = []
    try:
        for name, fixture in FIXTURES.items():
            baseline = run_command([
                sys.executable, str(SKILL_ROOT / "scripts" / "validate_project.py"),
                str(fixture), "--baseline", "active", "--mode", "strict",
            ])
            if baseline.returncode:
                raise AssertionError(f"{name} baseline failed:\n{baseline.stdout}\n{baseline.stderr}")

        for row in matrix:
            target_parent = Path(tempfile.mkdtemp(prefix="psw-e2e-"))
            temp_roots.append(target_parent)
            target = target_parent / f"{row['id'].lower()}-project"
            if row["source"] == "change":
                omit_map = {
                    "complete_change": None,
                    "omit_outline": "DEL-CHANGE-OUTLINE-001",
                    "omit_asset": "ASSET-CHANGE-001",
                    "omit_handoff": "DEL-CHANGE-HANDOFF-001",
                }
                build_change_project(target, omit_map[row["mutation"]])
            else:
                shutil.copytree(FIXTURES[row["source"]], target)
                MUTATIONS[row["mutation"]](target)
                refresh_run(target)

            project = run_command([
                sys.executable, str(SKILL_ROOT / "scripts" / "validate_project.py"),
                str(target), "--baseline", row["baseline"], "--mode", "strict",
            ])
            aggregate = run_command([
                sys.executable, str(SKILL_ROOT / "scripts" / "check_all.py"), str(SKILL_ROOT),
                "--project-only", str(target), "--baseline", row["baseline"], "--mode", "strict",
            ])
            assert_expected(row, project, "project")
            assert_expected(row, aggregate, "check_all")
            actual_ci = "PASS" if aggregate.returncode == 0 else "FAIL"
            if actual_ci != row["ci_conclusion"]:
                raise AssertionError(f"{row['id']} CI conclusion {actual_ci} != {row['ci_conclusion']}")
            print(f"PASS: {row['id']} invariant")
    finally:
        if not args.keep_temp:
            for path in temp_roots:
                shutil.rmtree(path, ignore_errors=True)
    print(f"PASS: {len(matrix)} E2E invariant rows through project and aggregate CLIs")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
