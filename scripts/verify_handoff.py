#!/usr/bin/env python3
"""Verify a handoff export by deriving its expected payload from the source project."""

from __future__ import annotations

import argparse
import fnmatch
import hashlib
import json
import os
import re
from collections import deque
from pathlib import Path, PurePosixPath
from typing import Any


ARTIFACT_EXTENSIONS = {".md", ".fountain"}
CONTROL_FILES = {"handoff-manifest.json", "manifest.sha256", "package.sha256"}
VIRTUAL_REFERENCE_PREFIXES = ("CON-", "ASM-", "CLM-", "SRC-", "RGT-", "TP-", "RISK-")


class VerifyError(Exception):
    def __init__(self, code: str, message: str):
        super().__init__(message)
        self.code = code
        self.message = message


def scalar(value: str) -> str | list[str]:
    value = value.strip()
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


def normalized_bytes(path: Path) -> bytes:
    return path.read_bytes().replace(b"\r\n", b"\n")


def digest_bytes(data: bytes) -> str:
    return "sha256:" + hashlib.sha256(data).hexdigest()


def excluded(relative: str, patterns: list[str]) -> bool:
    return any(fnmatch.fnmatchcase(relative, pattern) for pattern in patterns)


def is_junction(path: Path) -> bool:
    checker = getattr(os.path, "isjunction", None)
    return bool(checker and checker(path))


def reject_nesting(source: Path, output: Path) -> None:
    source_resolved = source.resolve()
    output_resolved = output.resolve()
    if output_resolved == source_resolved or output_resolved.is_relative_to(source_resolved) or source_resolved.is_relative_to(output_resolved):
        raise VerifyError("EXPORT_NESTING", "source and output directories must not contain one another")


def safe_relative(value: Any) -> str:
    text = str(value or "")
    path = PurePosixPath(text)
    if not text or "\\" in text or path.is_absolute() or any(part in {"", ".", ".."} for part in path.parts):
        raise VerifyError("EXPORT_PATH_ESCAPE", f"unsafe payload path: {text}")
    return path.as_posix()


def independently_derive_expected(source: Path, baseline: str, selector: str, schema: dict[str, Any]) -> dict[str, tuple[Path, dict[str, Any]]]:
    scope = schema["export_scope"]
    if selector not in scope["selectors"]:
        raise VerifyError("EXPORT_SELECTOR", f"unsupported selector: {selector}")
    artifacts: dict[str, tuple[Path, dict[str, Any]]] = {}
    for path in sorted(source.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in ARTIFACT_EXTENSIONS:
            continue
        meta = metadata(path)
        artifact_id = meta.get("artifact_id")
        if not artifact_id:
            continue
        if artifact_id in artifacts:
            raise VerifyError("EXPORT_DUPLICATE_ID", f"duplicate artifact_id: {artifact_id}")
        artifacts[str(artifact_id)] = (path, meta)

    exclusions = scope["fixed_exclude"]
    eligible: dict[str, tuple[Path, dict[str, Any]]] = {}
    for artifact_id, (path, meta) in artifacts.items():
        relative = path.relative_to(source).as_posix()
        if meta.get("project_baseline") == baseline and not excluded(relative, exclusions):
            eligible[artifact_id] = (path, meta)
    required_types = set(scope["required_artifact_types"][selector])
    selected = {
        artifact_id for artifact_id, (_, meta) in eligible.items()
        if meta.get("artifact_type") in required_types
    }
    found_types = {eligible[item][1].get("artifact_type") for item in selected}
    if found_types != required_types:
        raise VerifyError("EXPORT_REQUIRED_TYPE", "source lacks required selector artifact types")

    queue = deque(sorted(selected))
    while queue:
        current = queue.popleft()
        refs = eligible[current][1].get(scope["closure_edge"], [])
        refs = [refs] if isinstance(refs, str) else list(refs)
        for reference_value in refs:
            reference = str(reference_value)
            target = artifacts.get(reference)
            if target is None:
                if reference.startswith(VIRTUAL_REFERENCE_PREFIXES):
                    continue
                raise VerifyError("EXPORT_BROKEN_REFERENCE", f"unknown upstream artifact: {reference}")
            path, meta = target
            relative = path.relative_to(source).as_posix()
            if excluded(relative, exclusions):
                continue
            if meta.get("project_baseline") != baseline:
                raise VerifyError("EXPORT_BASELINE_DRIFT", f"upstream artifact is outside baseline: {reference}")
            if reference not in selected:
                selected.add(reference)
                queue.append(reference)
    return {
        artifacts[item][0].relative_to(source).as_posix(): artifacts[item]
        for item in sorted(selected, key=lambda artifact_id: artifacts[artifact_id][0].relative_to(source).as_posix())
    }


def actual_payload(output: Path) -> set[str]:
    result: set[str] = set()
    for current, directories, files in os.walk(output, followlinks=False):
        base = Path(current)
        for name in list(directories):
            path = base / name
            if path.is_symlink() or is_junction(path):
                raise VerifyError("EXPORT_LINK", f"linked output path: {path}")
        for name in files:
            path = base / name
            if path.is_symlink() or is_junction(path):
                raise VerifyError("EXPORT_LINK", f"linked output path: {path}")
            relative = path.relative_to(output).as_posix()
            if relative not in CONTROL_FILES:
                result.add(safe_relative(relative))
    return result


def verify(source: Path, output: Path, baseline: str, selector: str, schema_path: Path) -> dict[str, Any]:
    source = source.resolve()
    output = output.resolve()
    if not source.is_dir() or not output.is_dir():
        raise VerifyError("EXPORT_IO", "source and output directories must exist")
    reject_nesting(source, output)
    schema = json.loads(schema_path.read_text(encoding="utf-8"))

    manifest_path = output / "handoff-manifest.json"
    manifest_bytes = manifest_path.read_bytes()
    manifest = json.loads(manifest_bytes.decode("utf-8"))
    canonical_manifest = (json.dumps(manifest, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")
    if manifest_bytes != canonical_manifest:
        raise VerifyError("EXPORT_MANIFEST_CANONICAL", "handoff-manifest.json is not canonically serialized")
    manifest_hex = hashlib.sha256(manifest_bytes).hexdigest()
    if (output / "manifest.sha256").read_text(encoding="utf-8") != f"{manifest_hex}  handoff-manifest.json\n":
        raise VerifyError("EXPORT_MANIFEST_DIGEST", "manifest.sha256 does not match canonical manifest bytes")
    if (output / "package.sha256").read_text(encoding="utf-8") != f"sha256:{manifest_hex}\n":
        raise VerifyError("EXPORT_PACKAGE_DIGEST", "package.sha256 does not match canonical manifest bytes")
    if manifest.get("baseline") != baseline or manifest.get("selector") != selector or manifest.get("schema_id") != schema["schema_id"]:
        raise VerifyError("EXPORT_MANIFEST_SCOPE", "manifest scope does not match verifier inputs")

    entries = manifest.get("entries")
    if not isinstance(entries, list):
        raise VerifyError("EXPORT_MANIFEST", "manifest entries must be a list")
    manifest_entries: dict[str, dict[str, Any]] = {}
    for entry in entries:
        if not isinstance(entry, dict):
            raise VerifyError("EXPORT_MANIFEST", "manifest entry must be an object")
        relative = safe_relative(entry.get("path"))
        if relative in manifest_entries:
            raise VerifyError("EXPORT_MANIFEST", f"duplicate manifest path: {relative}")
        manifest_entries[relative] = entry

    expected = independently_derive_expected(source, baseline, selector, schema)
    expected_set = set(expected)
    manifest_set = set(manifest_entries)
    output_set = actual_payload(output)
    if expected_set != manifest_set or expected_set != output_set:
        raise VerifyError(
            "EXPORT_SET_MISMATCH",
            f"expected={sorted(expected_set)} manifest={sorted(manifest_set)} actual={sorted(output_set)}",
        )
    for relative, (source_path, source_meta) in expected.items():
        entry = manifest_entries[relative]
        source_data = normalized_bytes(source_path)
        output_data = (output / Path(relative)).read_bytes()
        expected_digest = digest_bytes(source_data)
        if output_data != source_data:
            raise VerifyError("EXPORT_PAYLOAD_MISMATCH", f"payload differs from normalized source: {relative}")
        if entry.get("digest") != expected_digest:
            raise VerifyError("EXPORT_ENTRY_DIGEST", f"manifest digest differs: {relative}")
        if entry.get("artifact_id") != source_meta.get("artifact_id") or entry.get("artifact_type") != source_meta.get("artifact_type"):
            raise VerifyError("EXPORT_ENTRY_IDENTITY", f"manifest identity differs: {relative}")
    return {
        "result": "PASS",
        "entry_count": len(expected),
        "package_hash": f"sha256:{manifest_hex}",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--baseline", required=True)
    parser.add_argument("--selector", choices=["project", "season", "episode"], required=True)
    parser.add_argument("--schema", type=Path, required=True)
    args = parser.parse_args()
    try:
        result = verify(args.source, args.output, args.baseline, args.selector, args.schema.resolve())
    except (VerifyError, OSError, UnicodeError, json.JSONDecodeError, KeyError) as exc:
        code = exc.code if isinstance(exc, VerifyError) else "EXPORT_IO"
        result = {"result": "FAIL", "findings": [{"code": code, "message": str(exc)}]}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["result"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
