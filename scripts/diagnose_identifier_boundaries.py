#!/usr/bin/env python3
"""Non-blocking rg --pcre2 comparison for identifier boundary patterns."""

from __future__ import annotations

import json
import subprocess

try:
    from .validate_project import LEGACY_NOTICE_RE, PLACEHOLDER_RE, SCENE_RE
except ImportError:
    from validate_project import LEGACY_NOTICE_RE, PLACEHOLDER_RE, SCENE_RE


CASES = {
    "scene": (
        SCENE_RE,
        ["场景SC-101", "第SC-101场", "SC-012_PARIS"],
        ["XSC-101", "SC-101ABC", "SC-101old"],
    ),
    "notice": (
        LEGACY_NOTICE_RE,
        ["旧编号UN-003", "UN-003_old"],
        ["XUN-003", "UN-003ABC", "UN-003old"],
    ),
    "placeholder": (
        PLACEHOLDER_RE,
        ["占位TBD", "TBD_value"],
        ["XTBD", "TBDx", "TBD1"],
    ),
}


def main() -> int:
    comparisons: list[dict[str, object]] = []
    try:
        subprocess.run(["rg", "--version"], capture_output=True, check=False)
    except FileNotFoundError:
        print(json.dumps({"status": "NOT_RUN", "reason": "rg unavailable"}, ensure_ascii=False, indent=2))
        return 0

    for name, (pattern, positives, negatives) in CASES.items():
        for sample in [*positives, *negatives]:
            python_match = pattern.search(sample) is not None
            result = subprocess.run(
                ["rg", "--pcre2", "-q", pattern.pattern, "-"],
                input=sample,
                text=True,
                encoding="utf-8",
                errors="replace",
                capture_output=True,
                check=False,
            )
            if result.returncode not in {0, 1}:
                print(json.dumps({
                    "status": "NOT_RUN",
                    "reason": f"rg failed for {name}: {result.stderr.strip()}",
                }, ensure_ascii=False, indent=2))
                return 0
            comparisons.append({
                "pattern": name,
                "sample": sample,
                "python": python_match,
                "rg_pcre2": result.returncode == 0,
            })
    disagreements = [item for item in comparisons if item["python"] != item["rg_pcre2"]]
    print(json.dumps({
        "status": "DISAGREE" if disagreements else "AGREE",
        "comparisons": comparisons,
        "disagreements": disagreements,
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
