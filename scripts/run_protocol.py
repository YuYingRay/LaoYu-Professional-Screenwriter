#!/usr/bin/env python3
"""Minimal reusable preflight -> RUN -> final protocol for Phase 2 rehearsal."""

from __future__ import annotations

import fnmatch
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CONTENT_DIGEST_RE = re.compile(rb"^content_digest:[^\r\n]*(?:\r?\n|$)", re.MULTILINE)


def load_schema(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def managed_files(root: Path, schema_path: Path) -> list[Path]:
    schema = load_schema(schema_path)
    payload = schema["run_payload"]
    extensions = set(payload["managed_extensions"])
    result: list[Path] = []
    for path in root.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in extensions:
            continue
        rel = path.relative_to(root).as_posix()
        if not any(fnmatch.fnmatchcase(rel, pattern) for pattern in payload["include"]):
            continue
        if any(fnmatch.fnmatchcase(rel, pattern) for pattern in payload["exclude"]):
            continue
        result.append(path)
    return sorted(result, key=lambda item: item.relative_to(root).as_posix())


def canonical_bytes(path: Path) -> bytes:
    data = path.read_bytes().replace(b"\r\n", b"\n")
    return CONTENT_DIGEST_RE.sub(b"content_digest: <excluded>\n", data)


def content_digest(path: Path) -> str:
    return "sha256:" + hashlib.sha256(canonical_bytes(path)).hexdigest()


def file_sha256(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def source_snapshot_digest(root: Path, schema_path: Path) -> str:
    entries: list[bytes] = []
    files = managed_files(root, schema_path)
    for path in files:
        rel = path.relative_to(root).as_posix().encode("utf-8")
        digest = content_digest(path).encode("ascii")
        encoded = len(rel).to_bytes(8, "big") + rel + len(digest).to_bytes(8, "big") + digest
        entries.append(hashlib.sha256(encoded).digest())
    payload = len(files).to_bytes(8, "big") + b"".join(entries)
    return "sha256:" + hashlib.sha256(payload).hexdigest()


def metadata(path: Path) -> dict[str, str]:
    lines = path.read_text(encoding="utf-8").splitlines()
    result: dict[str, str] = {}
    if not lines or lines[0].strip() != "---":
        return result
    for line in lines[1:]:
        if line.strip() == "---":
            break
        if ":" in line and not line.startswith(" "):
            key, value = line.split(":", 1)
            result[key.strip()] = value.strip()
    return result


def preflight(root: Path, run_id: str, schema_path: Path) -> dict[str, Any]:
    findings: list[dict[str, str]] = []
    for path in managed_files(root, schema_path):
        meta = metadata(path)
        if meta.get("status") != "LOCKED":
            continue
        if meta.get("test_run_id") != run_id:
            findings.append({"code": "RUN_ID_MISMATCH", "path": path.relative_to(root).as_posix()})
        digest = meta.get("content_digest")
        if digest != "PENDING" and digest != content_digest(path):
            findings.append({"code": "DIGEST_MISMATCH", "path": path.relative_to(root).as_posix()})
    return {"profile": "preflight", "findings": findings, "result": "PASS" if not findings else "FAIL"}


def write_content_digests(root: Path, schema_path: Path) -> None:
    for path in managed_files(root, schema_path):
        text = path.read_text(encoding="utf-8")
        if not re.search(r"^content_digest:", text, flags=re.MULTILINE):
            continue
        digest = content_digest(path)
        updated = re.sub(r"^content_digest:.*$", f"content_digest: {digest}", text, flags=re.MULTILINE)
        path.write_text(updated, encoding="utf-8", newline="\n")


def create_run(root: Path, run_id: str, schema_path: Path, *, command: str) -> Path:
    check = preflight(root, run_id, schema_path)
    if check["result"] != "PASS":
        raise ValueError(f"preflight failed: {check['findings']}")
    write_content_digests(root, schema_path)
    files = managed_files(root, schema_path)
    run = {
        "run_id": run_id,
        "source_snapshot_digest": source_snapshot_digest(root, schema_path),
        "artifact_digests": {
            path.relative_to(root).as_posix(): content_digest(path) for path in files
        },
        "profile": "preflight",
        "command": command,
        "validator_digest": file_sha256(Path(__file__).resolve()),
        "schema_digest": file_sha256(schema_path.resolve()),
        "findings": check["findings"],
        "result": "PASS",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    run_dir = root / "runs"
    run_dir.mkdir(exist_ok=True)
    path = run_dir / f"{run_id}.json"
    path.write_text(json.dumps(run, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    return path


def final_check(root: Path, run_path: Path, schema_path: Path) -> dict[str, Any]:
    run = json.loads(run_path.read_text(encoding="utf-8"))
    findings: list[dict[str, str]] = []
    if run.get("schema_digest") != file_sha256(schema_path.resolve()):
        findings.append({"code": "SCHEMA_DIGEST_MISMATCH", "path": str(schema_path)})
    if run.get("validator_digest") != file_sha256(Path(__file__).resolve()):
        findings.append({"code": "VALIDATOR_DIGEST_MISMATCH", "path": str(Path(__file__).resolve())})
    current_snapshot = source_snapshot_digest(root, schema_path)
    if run.get("source_snapshot_digest") != current_snapshot:
        findings.append({"code": "SOURCE_SNAPSHOT_MISMATCH", "path": str(root)})
    current = {
        path.relative_to(root).as_posix(): content_digest(path)
        for path in managed_files(root, schema_path)
    }
    if run.get("artifact_digests") != current:
        findings.append({"code": "ARTIFACT_DIGEST_MISMATCH", "path": str(root)})
    return {"profile": "final", "findings": findings, "result": "PASS" if not findings else "FAIL"}
