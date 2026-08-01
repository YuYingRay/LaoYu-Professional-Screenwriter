#!/usr/bin/env python3
"""Bootstrap aggregate gate for repository, fixtures, and one template instance."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


def run(label: str, command: list[str], cwd: Path) -> bool:
    result = subprocess.run(command, cwd=cwd, text=True, capture_output=True, check=False)
    if result.stdout:
        print(result.stdout.rstrip())
    if result.stderr:
        print(result.stderr.rstrip())
    if result.returncode != 0:
        print(f"FAIL: {label} (exit {result.returncode})")
        return False
    print(f"PASS: {label}")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", type=Path)
    parser.add_argument("--baseline", choices=["active", "candidate"], default="candidate")
    parser.add_argument("--mode", choices=["audit", "strict"], default="audit")
    args = parser.parse_args()
    root = args.root.resolve()
    py = sys.executable
    commands = [
        ("lint_repo audit" if args.mode == "audit" else "lint_repo strict", [py, str(root / "scripts" / "lint_repo.py"), str(root), "--mode", args.mode]),
        ("control schema unit", [py, "-X", "utf8", "-m", "unittest", "tests.test_control_schema"]),
        ("feature fixture active baseline", [py, str(root / "scripts" / "validate_project.py"), str(root / "tests" / "feature-project-fixture"), "--baseline", "active"]),
        ("vertical fixture active baseline", [py, str(root / "scripts" / "validate_project.py"), str(root / "tests" / "vertical-project-fixture"), "--baseline", "active"]),
        ("minimum template instantiation", [py, str(root / "scripts" / "test_template_instantiation.py"), str(root), "--baseline", args.baseline]),
    ]
    passed = True
    for label, command in commands:
        passed = run(label, command, root) and passed
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
