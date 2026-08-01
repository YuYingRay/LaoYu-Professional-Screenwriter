#!/usr/bin/env python3
"""Validate a project against the Professional Screenwriter control-plane contract."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any


ARTIFACT_STATUSES = {
    "DRAFT", "IN_REVIEW", "APPROVED", "LOCKED", "SUPERSEDED", "BLOCKED"
}
CONFORMANCE_LEVELS = {
    "STRUCTURAL_CONFORMANCE", "TRACEABILITY_CONFORMANCE",
    "HUMAN_REVIEWED", "PRODUCTION_READY"
}
ARTIFACT_PREFIXES = {
    "PROJECT_MANIFEST": "PROJECT-",
    "STORY_BIBLE": "BIBLE-",
    "SCRIPT_MASTER": "SCRIPT-",
    "SCENE_CARD": "SC-",
    "REVIEW": "REVIEW-",
    "NOTICE": "NOTICE-",
    "PRODUCTION_HANDOFF": "DEL-",
    "OUTLINE": "DEL-",
    "SEASON_MAP": "DEL-",
    "VERTICAL_EPISODE": "EP-",
}
PLACEHOLDER_RE = re.compile(
    r"\[\[[^\[\]\r\n]{1,200}\]\]|\[填写|\[PROJECT_ID\]|\[ID\]|\[ROLE\]|\bTBD\b|待定|见最新版本"
)
SCENE_RE = re.compile(r"\bSC-\d{3,}\b")


@dataclass
class Finding:
    severity: str
    code: str
    path: str
    message: str


def scalar(value: str) -> Any:
    value = value.strip()
    if value in {"[]", ""}:
        return []
    if value.startswith("[") and value.endswith("]"):
        return [item.strip().strip("'\"") for item in value[1:-1].split(",") if item.strip()]
    return value.strip("'\"")


def metadata(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    result: dict[str, Any] = {}
    lines = text.splitlines()
    if lines and lines[0].strip() == "---":
        for line in lines[1:]:
            if line.strip() == "---":
                break
            if ":" in line and not line.startswith(" "):
                key, value = line.split(":", 1)
                result[key.strip()] = scalar(value)
    for key, value in re.findall(r"/\*\s*([A-Z_]+):\s*(.*?)\s*\*/", text):
        parsed = scalar(value)
        if key == "UPSTREAM_IDS" and isinstance(parsed, str):
            parsed = [item.strip() for item in parsed.split(",") if item.strip()]
        result[key.lower()] = parsed
    return result


def canonical_digest(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    text = re.sub(r"^content_digest:\s*.*$", "content_digest: <excluded>", text, flags=re.MULTILINE)
    text = re.sub(r"^/\*\s*CONTENT_DIGEST:.*?\*/$", "/* CONTENT_DIGEST: <excluded> */", text, flags=re.MULTILINE)
    return "sha256:" + hashlib.sha256(text.encode("utf-8")).hexdigest()


def set_digest(path: Path, digest: str) -> None:
    text = path.read_text(encoding="utf-8")
    if re.search(r"^content_digest:", text, flags=re.MULTILINE):
        text = re.sub(r"^content_digest:\s*.*$", f"content_digest: {digest}", text, flags=re.MULTILINE)
    elif re.search(r"^/\*\s*CONTENT_DIGEST:", text, flags=re.MULTILINE):
        text = re.sub(r"^/\*\s*CONTENT_DIGEST:.*?\*/$", f"/* CONTENT_DIGEST: {digest} */", text, flags=re.MULTILINE)
    else:
        raise ValueError(f"No content_digest field in {path}")
    path.write_text(text, encoding="utf-8", newline="\n")


def validate(root: Path, write_digests: bool = False, baseline_mode: str = "active") -> list[Finding]:
    findings: list[Finding] = []
    files = sorted(p for p in root.rglob("*") if p.suffix.lower() in {".md", ".fountain"})
    manifest_path = root / "governance" / "project-manifest.md"
    if not manifest_path.exists():
        return [Finding("P0", "MISSING_MANIFEST", str(manifest_path), "project-manifest.md is required")]

    metas: dict[Path, dict[str, Any]] = {p: metadata(p) for p in files}
    manifest = metas[manifest_path]
    project_id = manifest.get("project_id")
    active_baseline = manifest.get("project_baseline")
    if not project_id or not active_baseline:
        findings.append(Finding("P0", "MANIFEST_METADATA", str(manifest_path), "project_id and project_baseline are required"))
    if baseline_mode == "candidate":
        baseline = manifest.get("candidate_baseline")
        if not baseline:
            findings.append(Finding("P0", "CANDIDATE_BASELINE_MISSING", str(manifest_path), "candidate_baseline is required for candidate validation"))
    else:
        baseline = active_baseline
    if manifest.get("artifact_type") != "PROJECT_MANIFEST":
        findings.append(Finding("P1", "MANIFEST_TYPE", str(manifest_path), "artifact_type must be PROJECT_MANIFEST"))

    artifact_ids: dict[str, Path] = {}
    scene_card_ids: set[str] = set()
    script_scene_ids: set[str] = set()

    for path, meta in metas.items():
        if path.name in {"input-brief.md", "README.md", "change-log.md", "control-plane-file-map.md"}:
            continue
        if not meta:
            continue
        rel = str(path.relative_to(root))
        required = ["artifact_id", "artifact_type", "project_id", "project_baseline", "artifact_version", "status", "owner", "upstream_ids"]
        for field in required:
            value = meta.get(field)
            if field not in meta or value is None or value == "":
                findings.append(Finding("P0", "MISSING_FIELD", rel, f"missing required field: {field}"))
        aid = meta.get("artifact_id")
        atype = meta.get("artifact_type")
        if aid:
            if aid in artifact_ids:
                findings.append(Finding("P0", "DUPLICATE_ID", rel, f"duplicate artifact_id: {aid}"))
            artifact_ids[aid] = path
            prefix = ARTIFACT_PREFIXES.get(str(atype))
            if prefix and not str(aid).startswith(prefix):
                findings.append(Finding("P1", "ID_PREFIX", rel, f"{atype} must use prefix {prefix}: {aid}"))
        if project_id and meta.get("project_id") != project_id:
            findings.append(Finding("P0", "PROJECT_DRIFT", rel, "project_id differs from manifest"))
        expected_baseline = active_baseline if path == manifest_path else baseline
        if expected_baseline and meta.get("project_baseline") != expected_baseline:
            findings.append(Finding("P0", "BASELINE_DRIFT", rel, "project_baseline differs from manifest"))
        if meta.get("status") not in ARTIFACT_STATUSES:
            findings.append(Finding("P1", "STATUS_ENUM", rel, f"invalid artifact status: {meta.get('status')}"))
        if meta.get("conformance_level") and meta.get("conformance_level") not in CONFORMANCE_LEVELS:
            findings.append(Finding("P1", "CONFORMANCE_ENUM", rel, f"invalid conformance level: {meta.get('conformance_level')}"))
        if re.search(r"\bUN-\d+\b", path.read_text(encoding="utf-8")):
            findings.append(Finding("P1", "LEGACY_NOTICE_ID", rel, "legacy UN-* notice ID found; use NOTICE-*"))
        if meta.get("status") in {"LOCKED", "APPROVED"}:
            text = path.read_text(encoding="utf-8")
            for field in ["reviewer", "approver", "test_run_id", "conformance_level"]:
                if field not in meta or meta[field] in {None, "", "HUMAN_REVIEW_REQUIRED"}:
                    findings.append(Finding("P0", "LOCK_GATE", rel, f"{field} is required for {meta.get('status')}"))
            if meta.get("status") == "LOCKED":
                digest = meta.get("content_digest")
                if not digest or not str(digest).startswith("sha256:"):
                    findings.append(Finding("P0", "DIGEST_MISSING", rel, "LOCKED artifact requires sha256 content_digest"))
                elif write_digests:
                    set_digest(path, canonical_digest(path))
                elif digest != canonical_digest(path):
                    findings.append(Finding("P0", "DIGEST_MISMATCH", rel, "content_digest does not match canonical content"))
            if PLACEHOLDER_RE.search(text):
                findings.append(Finding("P0", "PLACEHOLDER_LOCKED", rel, "placeholder remains in approved/locked artifact"))
        if atype == "SCENE_CARD" and aid:
            scene_card_ids.add(str(aid))
        if atype == "SCRIPT_MASTER":
            script_scene_ids.update(SCENE_RE.findall(path.read_text(encoding="utf-8")))

    for path, meta in metas.items():
        if not meta or path.name in {"input-brief.md", "README.md", "change-log.md"}:
            continue
        refs = meta.get("upstream_ids", [])
        if isinstance(refs, str):
            refs = [refs]
        for ref in refs:
            if ref not in artifact_ids and not str(ref).startswith(("CON-", "ASM-", "CLM-", "SRC-", "RGT-", "TP-", "RISK-")):
                findings.append(Finding("P1", "BROKEN_REFERENCE", str(path.relative_to(root)), f"unknown upstream_id: {ref}"))

    if script_scene_ids != scene_card_ids:
        missing = sorted(scene_card_ids - script_scene_ids)
        orphan = sorted(script_scene_ids - scene_card_ids)
        if missing:
            findings.append(Finding("P1", "SCENE_NOT_IN_SCRIPT", "script", f"scene cards not mapped in script: {', '.join(missing)}"))
        if orphan:
            findings.append(Finding("P0", "ORPHAN_SCRIPT_SCENE", "script", f"script scenes without Scene Cards: {', '.join(orphan)}"))

    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", type=Path)
    parser.add_argument("--write-digests", action="store_true")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--baseline", choices=["active", "candidate"], default="active")
    args = parser.parse_args()
    findings = validate(
        args.root.resolve(), write_digests=args.write_digests, baseline_mode=args.baseline
    )
    if args.json:
        print(json.dumps([asdict(item) for item in findings], ensure_ascii=False, indent=2))
    else:
        if not findings:
            print(f"PASS: {args.root.resolve()}")
        else:
            for item in findings:
                print(f"{item.severity} {item.code} {item.path}: {item.message}")
    return 1 if any(item.severity == "P0" for item in findings) else 0


if __name__ == "__main__":
    raise SystemExit(main())
