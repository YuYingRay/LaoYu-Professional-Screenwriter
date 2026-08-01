#!/usr/bin/env python3
"""Run repository-level invariants for the Professional Screenwriter Skill."""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", type=Path)
    args = parser.parse_args()
    root = args.root.resolve()
    errors: list[str] = []

    skill = root / "SKILL.md"
    if not skill.exists():
        errors.append("SKILL.md is missing")
    else:
        text = skill.read_text(encoding="utf-8")
        if "license: MIT" in text:
            errors.append("SKILL.md still declares MIT")
        if "control-plane-contract.md" not in text:
            errors.append("SKILL.md does not route to control-plane-contract.md")
        if "NOT_APPLICABLE" not in text:
            errors.append("SKILL.md does not define NOT_APPLICABLE semantics")

    license_file = root / "LICENSES" / "skill-license.md"
    if not license_file.exists():
        errors.append("LICENSES/skill-license.md is missing")
    else:
        license_text = license_file.read_text(encoding="utf-8")
        for required_text in [
            "LaoYu-Professional-Screenwriter",
            "YuYingRay",
            "https://github.com/YuYingRay/LaoYu-Professional-Screenwriter",
            "CC BY 4.0",
        ]:
            if required_text not in license_text:
                errors.append(f"license metadata missing: {required_text}")

    required = [
        "governance/control-plane-contract.md",
        "governance/control-schema.json",
        "templates/production-handoff.md",
        "scripts/validate_project.py",
        "scripts/run_e2e.py",
        "scripts/gen_contract_tables.py",
        "scripts/lint_repo.py",
        "scripts/check_all.py",
        "scripts/test_template_instantiation.py",
        "agents/openai.yaml",
        "tests/feature-project-fixture/governance/project-manifest.md",
        "tests/vertical-project-fixture/governance/project-manifest.md",
    ]
    for rel in required:
        if not (root / rel).exists():
            errors.append(f"required resource missing: {rel}")

    metadata_files = [
        "governance/project-manifest.md",
        "governance/source-links.md",
        "governance/upstream-notices.md",
        "governance/change-log.md",
        "templates/story-bible.md",
        "templates/scene-card.md",
        "templates/episode-outline.md",
        "templates/vertical-episode.md",
        "templates/review-report.md",
        "templates/production-handoff.md",
        "templates/notice.md",
    ]
    for rel in metadata_files:
        path = root / rel
        if path.exists() and not path.read_text(encoding="utf-8").lstrip().startswith("---"):
            errors.append(f"formal artifact template lacks metadata frontmatter: {rel}")

    openai = root / "agents" / "openai.yaml"
    if openai.exists():
        text = openai.read_text(encoding="utf-8")
        if "$professional-screenwriter" not in text:
            errors.append("agents/openai.yaml default_prompt must mention $professional-screenwriter")

    for path in root.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in {".md", ".fountain", ".yaml"}:
            continue
        text = path.read_text(encoding="utf-8")
        rel = str(path.relative_to(root))
        if re.search(r"\[web:\d+\]", text):
            errors.append(f"internal web artifact remains: {rel}")
        if re.search(r"\bUN-\d+\b", text):
            errors.append(f"legacy UN-* notice ID remains: {rel}")

    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        return 1

    print(f"PASS: skill invariants for {root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
