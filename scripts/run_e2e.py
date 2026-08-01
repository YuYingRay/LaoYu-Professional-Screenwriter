#!/usr/bin/env python3
"""Run baseline and adversarial E2E checks for the two bundled fixtures."""

from __future__ import annotations

import argparse
import shutil
import tempfile
from pathlib import Path

from validate_project import validate


SKILL_ROOT = Path(__file__).resolve().parents[1]
FIXTURES = {
    "feature": SKILL_ROOT / "tests" / "feature-project-fixture",
    "vertical": SKILL_ROOT / "tests" / "vertical-project-fixture",
}


def assert_clean(name: str, root: Path) -> None:
    findings = validate(root)
    if findings:
        details = "\n".join(f"{f.severity} {f.code}: {f.message}" for f in findings)
        raise AssertionError(f"{name} baseline should pass:\n{details}")


def assert_failure(name: str, root: Path, code: str) -> None:
    findings = validate(root)
    codes = {item.code for item in findings}
    if code not in codes:
        details = "\n".join(f"{f.severity} {f.code}: {f.message}" for f in findings)
        raise AssertionError(f"{name} should contain {code}; got:\n{details}")


def mutate_orphan_scene(root: Path) -> None:
    path = root / "script" / "script.fountain"
    path.write_text(path.read_text(encoding="utf-8") + "\n/* SC-999 */\n", encoding="utf-8")


def mutate_baseline(root: Path) -> None:
    path = root / "production" / "handoff.md"
    text = path.read_text(encoding="utf-8")
    path.write_text(text.replace("PROJECT-FEATURE-v1.0.0", "PROJECT-FEATURE-v9.0.0"), encoding="utf-8")


def mutate_placeholder(root: Path) -> None:
    path = root / "production" / "handoff.md"
    path.write_text(path.read_text(encoding="utf-8") + "\n[[未填写字段]]\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--keep-temp", action="store_true")
    args = parser.parse_args()

    for name, fixture in FIXTURES.items():
        assert_clean(f"{name} baseline", fixture)

    mutations = [
        ("feature orphan scene", FIXTURES["feature"], mutate_orphan_scene, "ORPHAN_SCRIPT_SCENE"),
        ("feature baseline drift", FIXTURES["feature"], mutate_baseline, "BASELINE_DRIFT"),
        ("vertical locked placeholder", FIXTURES["vertical"], mutate_placeholder, "PLACEHOLDER_LOCKED"),
    ]
    temp_roots: list[Path] = []
    try:
        for name, fixture, mutation, expected_code in mutations:
            target = Path(tempfile.mkdtemp(prefix="ps-e2e-")) / fixture.name
            shutil.copytree(fixture, target)
            temp_roots.append(target.parent)
            mutation(target)
            assert_failure(name, target, expected_code)
            print(f"PASS: {name} blocked by {expected_code}")
    finally:
        if not args.keep_temp:
            for path in temp_roots:
                shutil.rmtree(path, ignore_errors=True)
    print("PASS: feature and vertical baselines plus adversarial failure cases")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
