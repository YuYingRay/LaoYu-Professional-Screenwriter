#!/usr/bin/env python3
"""Instantiate one formal template as the Phase 2 bootstrap smoke test."""

from __future__ import annotations

import argparse
import sys
import tempfile
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from validate_project import validate  # noqa: E402


def replace_frontmatter(text: str, frontmatter: str) -> str:
    lines = text.splitlines(keepends=True)
    if not lines or lines[0].strip() != "---":
        raise ValueError("template frontmatter is missing")
    for index, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            return frontmatter + "".join(lines[index + 1 :])
    raise ValueError("template frontmatter is not closed")


def instantiate(root: Path, baseline_mode: str) -> list:
    active = "CONTRACT-v0.1.0"
    candidate = "CONTRACT-v0.2.0"
    selected = candidate if baseline_mode == "candidate" else active
    with tempfile.TemporaryDirectory(prefix="psw-template-test-") as temp_dir:
        project = Path(temp_dir)
        (project / "governance").mkdir()
        (project / "episodes").mkdir()
        candidate_line = f"candidate_baseline: {candidate}\n" if baseline_mode == "candidate" else ""
        (project / "governance" / "project-manifest.md").write_text(
            "---\n"
            "artifact_id: PROJECT-TEMPLATE-001\n"
            "artifact_type: PROJECT_MANIFEST\n"
            "project_id: PROJECT-TEMPLATE-001\n"
            f"project_baseline: {active}\n"
            f"{candidate_line}"
            "artifact_version: v0.1.0\n"
            "status: DRAFT\n"
            "owner: TEMPLATE-TEST\n"
            "upstream_ids: []\n"
            "---\n",
            encoding="utf-8",
            newline="\n",
        )
        template = (root / "templates" / "vertical-episode.md").read_text(encoding="utf-8")
        episode_frontmatter = (
            "---\n"
            "artifact_id: EP-001\n"
            "artifact_type: VERTICAL_EPISODE\n"
            "project_id: PROJECT-TEMPLATE-001\n"
            f"project_baseline: {selected}\n"
            "artifact_version: v0.1.0\n"
            "status: DRAFT\n"
            "owner: TEMPLATE-TEST\n"
            "upstream_ids: []\n"
            "---\n"
        )
        (project / "episodes" / "EP-001.md").write_text(
            replace_frontmatter(template, episode_frontmatter), encoding="utf-8", newline="\n"
        )
        return validate(project, baseline_mode=baseline_mode)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", type=Path)
    parser.add_argument("--baseline", choices=["active", "candidate"], default="active")
    args = parser.parse_args()
    findings = instantiate(args.root.resolve(), args.baseline)
    if findings:
        for finding in findings:
            print(f"{finding.severity} {finding.code} {finding.path}: {finding.message}")
        return 1
    print(f"PASS: minimum template instantiation ({args.baseline})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
