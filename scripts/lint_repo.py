#!/usr/bin/env python3
"""Bootstrap repository lint; audit reports findings without blocking."""

from __future__ import annotations

import argparse
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class LintFinding:
    code: str
    message: str


def lint(root: Path) -> list[LintFinding]:
    findings: list[LintFinding] = []
    validate_skill = subprocess.run(
        [sys.executable, str(root / "scripts" / "validate_skill.py"), str(root)],
        text=True,
        capture_output=True,
        check=False,
    )
    if validate_skill.returncode != 0:
        detail = (validate_skill.stdout + validate_skill.stderr).strip()
        findings.append(LintFinding("SKILL_INVARIANT_FAILURE", detail))

    generated = subprocess.run(
        [sys.executable, str(root / "scripts" / "gen_contract_tables.py"), str(root), "--check"],
        text=True,
        capture_output=True,
        check=False,
    )
    if generated.returncode != 0:
        detail = (generated.stdout + generated.stderr).strip()
        code = "GENERATED_BLOCK_MISSING" if "GENERATED_BLOCK_MISSING" in detail else "GENERATED_BLOCK_DRIFT"
        findings.append(LintFinding(code, detail))
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", type=Path)
    parser.add_argument("--mode", choices=["audit", "strict"], default="audit")
    args = parser.parse_args()
    root = args.root.resolve()
    findings = lint(root)
    for finding in findings:
        print(f"{finding.code}: {finding.message}")
    if args.mode == "audit":
        print(f"PASS: lint_repo audit ({len(findings)} finding(s), non-blocking)")
        return 0
    if findings:
        print(f"FAIL: lint_repo strict ({len(findings)} finding(s))")
        return 1
    print("PASS: lint_repo strict")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
