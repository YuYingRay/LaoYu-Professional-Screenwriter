#!/usr/bin/env python3
"""Aggregate strict gate used locally and by CI."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

from validate_project import resolve_baseline_mode


def run(label: str, command: list[str], cwd: Path) -> bool:
    result = subprocess.run(
        command, cwd=cwd, text=True, encoding="utf-8", errors="replace", capture_output=True, check=False
    )
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
    parser.add_argument("--baseline", choices=["auto", "active", "candidate"], default="auto")
    parser.add_argument("--mode", choices=["audit", "strict"], default="strict")
    parser.add_argument("--project-only", type=Path)
    parser.add_argument("--skip-unit-tests", action="store_true", help=argparse.SUPPRESS)
    parser.add_argument("--skip-e2e", action="store_true", help=argparse.SUPPRESS)
    args = parser.parse_args()
    root = args.root.resolve()
    py = sys.executable
    resolved_baseline, _ = resolve_baseline_mode(
        root / "governance" / "project-manifest.md", args.baseline
    )
    template_baseline = resolved_baseline or "active"
    if args.project_only:
        project = args.project_only.resolve()
        passed = run(
            f"project {project.name}",
            [
                py, str(root / "scripts" / "validate_project.py"), str(project),
                "--baseline", args.baseline, "--mode", args.mode,
            ],
            root,
        )
        return 0 if passed else 1

    commands = [
        ("lint_repo audit" if args.mode == "audit" else "lint_repo strict", [py, str(root / "scripts" / "lint_repo.py"), str(root), "--mode", args.mode]),
        (
            f"root project {args.baseline} baseline",
            [
                py, str(root / "scripts" / "validate_project.py"), str(root),
                "--baseline", args.baseline, "--mode", args.mode,
            ],
        ),
    ]
    if not args.skip_unit_tests:
        commands.append(("unit tests", [py, "-X", "utf8", "-m", "unittest", "discover", "-s", "tests"]))
    commands.append(("minimum template instantiation", [py, str(root / "scripts" / "test_template_instantiation.py"), str(root), "--baseline", template_baseline]))
    for fixture in sorted((root / "tests").glob("*-fixture")):
        commands.append((
            f"{fixture.name} active baseline",
            [
                py, str(root / "scripts" / "validate_project.py"), str(fixture),
                "--baseline", "active", "--mode", args.mode,
            ],
        ))
    if not args.skip_e2e:
        commands.append(("E2E invariant matrix", [py, str(root / "scripts" / "run_e2e.py")]))
    passed = True
    for label, command in commands:
        passed = run(label, command, root) and passed
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
