#!/usr/bin/env python3
"""Create and verify non-recursive validation RUN evidence."""

from __future__ import annotations

import argparse
import fnmatch
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


MD_DIGEST_RE = re.compile(rb"^content_digest:[^\r\n]*(?:\r?\n|$)", re.MULTILINE)
FOUNTAIN_DIGEST_RE = re.compile(rb"^/\*\s*CONTENT_DIGEST:.*?\*/(?:\r?\n|$)", re.MULTILINE)
VALID_DIGEST_RE = re.compile(r"^sha256:[0-9a-f]{64}$")
RUN_REQUIRED_FIELDS = {
    "run_id",
    "source_snapshot_digest",
    "artifact_digests",
    "profile",
    "command",
    "validator_digest",
    "schema_digest",
    "findings",
    "result",
    "timestamp",
}


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
    data = MD_DIGEST_RE.sub(b"content_digest: <excluded>\n", data)
    return FOUNTAIN_DIGEST_RE.sub(b"/* CONTENT_DIGEST: <excluded> */\n", data)


def content_digest(path: Path) -> str:
    return "sha256:" + hashlib.sha256(canonical_bytes(path)).hexdigest()


def file_sha256(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def source_snapshot_digest(root: Path, schema_path: Path) -> str:
    files = managed_files(root, schema_path)
    entries: list[bytes] = []
    for path in files:
        rel = path.relative_to(root).as_posix().encode("utf-8")
        digest = content_digest(path).encode("ascii")
        encoded = len(rel).to_bytes(8, "big") + rel + len(digest).to_bytes(8, "big") + digest
        entries.append(hashlib.sha256(encoded).digest())
    payload = len(files).to_bytes(8, "big") + b"".join(entries)
    return "sha256:" + hashlib.sha256(payload).hexdigest()


def _scalar(value: str) -> str | list[str]:
    value = value.strip()
    if value.startswith("[") and value.endswith("]"):
        return [item.strip().strip("'\"") for item in value[1:-1].split(",") if item.strip()]
    return value.strip("'\"")


def metadata(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    result: dict[str, Any] = {}
    if lines and lines[0].strip() == "---":
        for line in lines[1:]:
            if line.strip() == "---":
                break
            if ":" in line and not line.startswith(" "):
                key, value = line.split(":", 1)
                result[key.strip()] = _scalar(value)
    for key, value in re.findall(r"/\*\s*([A-Z_]+):\s*(.*?)\s*\*/", text):
        result[key.lower()] = _scalar(value)
    return result


def _finding(code: str, path: str, message: str = "") -> dict[str, str]:
    return {"code": code, "path": path, "message": message}


def _locked_artifact_findings(root: Path, run_id: str, schema_path: Path, *, allow_pending: bool) -> list[dict[str, str]]:
    findings: list[dict[str, str]] = []
    for path in managed_files(root, schema_path):
        meta = metadata(path)
        if meta.get("status") != "LOCKED":
            continue
        rel = path.relative_to(root).as_posix()
        if meta.get("test_run_id") != run_id:
            findings.append(_finding("RUN_ID_MISMATCH", rel, "LOCKED artifact test_run_id differs from RUN"))
        digest = meta.get("content_digest")
        if allow_pending and digest == "PENDING":
            continue
        if not isinstance(digest, str) or not VALID_DIGEST_RE.fullmatch(digest):
            findings.append(_finding("INVALID_CONTENT_DIGEST", rel, "LOCKED artifact digest is not sha256:<64 lowercase hex>"))
        elif digest != content_digest(path):
            findings.append(_finding("DIGEST_MISMATCH", rel, "LOCKED artifact digest differs from canonical content"))
    return findings


def preflight(root: Path, run_id: str, schema_path: Path) -> dict[str, Any]:
    findings = _locked_artifact_findings(root, run_id, schema_path, allow_pending=True)
    return {"profile": "preflight", "findings": findings, "result": "PASS" if not findings else "FAIL"}


def write_content_digests(root: Path, schema_path: Path) -> None:
    for path in managed_files(root, schema_path):
        text = path.read_text(encoding="utf-8")
        digest = content_digest(path)
        if re.search(r"^content_digest:", text, flags=re.MULTILINE):
            updated = re.sub(r"^content_digest:.*$", f"content_digest: {digest}", text, flags=re.MULTILINE)
        elif re.search(r"^/\*\s*CONTENT_DIGEST:", text, flags=re.MULTILINE):
            updated = re.sub(
                r"^/\*\s*CONTENT_DIGEST:.*?\*/$",
                f"/* CONTENT_DIGEST: {digest} */",
                text,
                flags=re.MULTILINE,
            )
        else:
            continue
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
        "profile": "final",
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
    findings: list[dict[str, str]] = []
    if not run_path.is_file():
        return {"profile": "final", "findings": [_finding("RUN_MISSING", str(run_path))], "result": "FAIL"}
    try:
        run = json.loads(run_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return {"profile": "final", "findings": [_finding("RUN_INVALID", str(run_path), str(exc))], "result": "FAIL"}

    for field in sorted(RUN_REQUIRED_FIELDS - set(run)):
        findings.append(_finding("RUN_FIELD_MISSING", str(run_path), field))
    run_id = run.get("run_id")
    if not isinstance(run_id, str) or not run_id:
        findings.append(_finding("RUN_ID_INVALID", str(run_path)))
        run_id = "<invalid>"
    elif run_path.stem != run_id:
        findings.append(_finding("RUN_FILE_ID_MISMATCH", str(run_path)))
    if run.get("profile") != "final":
        findings.append(_finding("RUN_PROFILE_MISMATCH", str(run_path)))
    if run.get("result") != "PASS":
        findings.append(_finding("RUN_RESULT_NOT_PASS", str(run_path)))
    if not isinstance(run.get("findings"), list) or run.get("findings"):
        findings.append(_finding("RUN_FINDINGS_NOT_EMPTY", str(run_path)))
    if run.get("schema_digest") != file_sha256(schema_path.resolve()):
        findings.append(_finding("SCHEMA_DIGEST_MISMATCH", schema_path.as_posix()))
    if run.get("validator_digest") != file_sha256(Path(__file__).resolve()):
        findings.append(_finding("VALIDATOR_DIGEST_MISMATCH", Path(__file__).resolve().as_posix()))

    current_snapshot = source_snapshot_digest(root, schema_path)
    if run.get("source_snapshot_digest") != current_snapshot:
        findings.append(_finding("SOURCE_SNAPSHOT_MISMATCH", root.as_posix()))
    current = {
        path.relative_to(root).as_posix(): content_digest(path)
        for path in managed_files(root, schema_path)
    }
    if run.get("artifact_digests") != current:
        findings.append(_finding("ARTIFACT_DIGEST_MISMATCH", root.as_posix()))
    findings.extend(_locked_artifact_findings(root, run_id, schema_path, allow_pending=False))
    return {"profile": "final", "findings": findings, "result": "PASS" if not findings else "FAIL"}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", type=Path)
    parser.add_argument("--schema", type=Path)
    parser.add_argument("--profile", choices=["preflight", "create", "final"], required=True)
    parser.add_argument("--run-id")
    parser.add_argument("--run", type=Path)
    parser.add_argument("--command", default="")
    args = parser.parse_args()
    root = args.root.resolve()
    schema = (args.schema or root / "governance" / "control-schema.json").resolve()
    if args.profile in {"preflight", "create"} and not args.run_id:
        parser.error("--run-id is required for preflight/create")
    if args.profile == "preflight":
        result = preflight(root, args.run_id, schema)
    elif args.profile == "create":
        path = create_run(root, args.run_id, schema, command=args.command)
        result = {"profile": "create", "run_path": str(path), "result": "PASS"}
    else:
        run_path = (args.run or root / "runs" / f"{args.run_id or ''}.json").resolve()
        result = final_check(root, run_path, schema)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["result"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
