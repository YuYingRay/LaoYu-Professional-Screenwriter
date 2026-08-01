#!/usr/bin/env python3
"""Bootstrap repository lint; audit reports findings without blocking."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

try:
    from .ownership import analyze_ownership, hygiene_findings, template_closure_findings
except ImportError:
    from ownership import analyze_ownership, hygiene_findings, template_closure_findings


@dataclass(frozen=True)
class LintFinding:
    code: str
    message: str
    deferred: bool = False


def lint(root: Path) -> list[LintFinding]:
    findings: list[LintFinding] = []
    validate_skill = subprocess.run(
        [sys.executable, str(root / "scripts" / "validate_skill.py"), str(root)],
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        check=False,
    )
    if validate_skill.returncode != 0:
        detail = (validate_skill.stdout + validate_skill.stderr).strip()
        findings.append(LintFinding("SKILL_INVARIANT_FAILURE", detail))

    generated = subprocess.run(
        [sys.executable, str(root / "scripts" / "gen_contract_tables.py"), str(root), "--check"],
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        check=False,
    )
    if generated.returncode != 0:
        detail = (generated.stdout + generated.stderr).strip()
        code = "GENERATED_BLOCK_MISSING" if "GENERATED_BLOCK_MISSING" in detail else "GENERATED_BLOCK_DRIFT"
        findings.append(LintFinding(code, detail))

    schema_path = root / "governance" / "control-schema.json"
    if schema_path.is_file():
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        deferred = schema["ownership"].get("enforcement") != "strict"
        report = analyze_ownership(root, schema)
        for item in [*report.findings, *template_closure_findings(root, schema), *hygiene_findings(root, schema)]:
            findings.append(LintFinding(item.code, f"{item.path}: {item.message}", deferred))
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
    blocking = [finding for finding in findings if not finding.deferred]
    if blocking:
        print(f"FAIL: lint_repo strict ({len(blocking)} blocking finding(s))")
        return 1
    deferred = sum(finding.deferred for finding in findings)
    suffix = f" ({deferred} audit finding(s), non-blocking)" if deferred else ""
    print(f"PASS: lint_repo strict{suffix}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
