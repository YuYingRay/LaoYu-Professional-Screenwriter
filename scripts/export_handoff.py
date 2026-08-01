#!/usr/bin/env python3
"""Create a deterministic production handoff directory from a source project."""

from __future__ import annotations

import argparse
import fnmatch
import hashlib
import json
import os
import re
import shutil
import tempfile
from collections import deque
from pathlib import Path
from typing import Any


ARTIFACT_EXTENSIONS = {".md", ".fountain"}
VIRTUAL_REFERENCE_PREFIXES = ("CON-", "ASM-", "CLM-", "SRC-", "RGT-", "TP-", "RISK-")


class ExportError(Exception):
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


def reject_link_path(root: Path, path: Path) -> None:
    current = path
    while current != root:
        if current.is_symlink() or is_junction(current):
            raise ExportError("EXPORT_LINK", f"linked source path is not exportable: {current}")
        current = current.parent


def reject_nesting(source: Path, output: Path) -> None:
    source_resolved = source.resolve()
    output_resolved = output.resolve(strict=False)
    if output_resolved == source_resolved or output_resolved.is_relative_to(source_resolved) or source_resolved.is_relative_to(output_resolved):
        raise ExportError("EXPORT_NESTING", "source and output directories must not contain one another")


def source_artifacts(source: Path) -> tuple[dict[str, tuple[Path, dict[str, Any]]], dict[str, tuple[Path, dict[str, Any]]]]:
    by_id: dict[str, tuple[Path, dict[str, Any]]] = {}
    by_path: dict[str, tuple[Path, dict[str, Any]]] = {}
    for path in sorted(source.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in ARTIFACT_EXTENSIONS:
            continue
        rel = path.relative_to(source).as_posix()
        meta = metadata(path)
        artifact_id = meta.get("artifact_id")
        if not artifact_id:
            continue
        if artifact_id in by_id:
            raise ExportError("EXPORT_DUPLICATE_ID", f"duplicate artifact_id: {artifact_id}")
        by_id[str(artifact_id)] = (path, meta)
        by_path[rel] = (path, meta)
    return by_id, by_path


def derive_export_set(source: Path, baseline: str, selector: str, schema: dict[str, Any]) -> dict[str, tuple[Path, dict[str, Any]]]:
    scope = schema["export_scope"]
    if selector not in scope["selectors"]:
        raise ExportError("EXPORT_SELECTOR", f"unsupported selector: {selector}")
    by_id, by_path = source_artifacts(source)
    excluded_patterns = scope["fixed_exclude"]
    required_types = set(scope["required_artifact_types"][selector])
    eligible = {
        artifact_id: (path, meta)
        for artifact_id, (path, meta) in by_id.items()
        if meta.get("project_baseline") == baseline
        and not excluded(path.relative_to(source).as_posix(), excluded_patterns)
    }
    seeds = {
        artifact_id for artifact_id, (_, meta) in eligible.items()
        if meta.get("artifact_type") in required_types
    }
    present_types = {eligible[item][1].get("artifact_type") for item in seeds}
    missing_types = sorted(required_types - present_types)
    if missing_types:
        raise ExportError("EXPORT_REQUIRED_TYPE", "missing required artifact type(s): " + ", ".join(missing_types))

    selected = set(seeds)
    queue = deque(sorted(seeds))
    while queue:
        artifact_id = queue.popleft()
        meta = eligible[artifact_id][1]
        upstream = meta.get(scope["closure_edge"], [])
        upstream_ids = [upstream] if isinstance(upstream, str) else list(upstream)
        for reference in upstream_ids:
            reference = str(reference)
            target = by_id.get(reference)
            if target is None:
                if reference.startswith(VIRTUAL_REFERENCE_PREFIXES):
                    continue
                raise ExportError("EXPORT_BROKEN_REFERENCE", f"unknown upstream artifact: {reference}")
            target_path, target_meta = target
            target_rel = target_path.relative_to(source).as_posix()
            if excluded(target_rel, excluded_patterns):
                continue
            if target_meta.get("project_baseline") != baseline:
                raise ExportError("EXPORT_BASELINE_DRIFT", f"upstream artifact is outside baseline: {reference}")
            if reference not in selected:
                selected.add(reference)
                queue.append(reference)

    result: dict[str, tuple[Path, dict[str, Any]]] = {}
    for artifact_id in selected:
        path, meta = eligible[artifact_id]
        reject_link_path(source, path)
        result[path.relative_to(source).as_posix()] = (path, meta)
    return dict(sorted(result.items()))


def manifest_bytes(manifest: dict[str, Any]) -> bytes:
    return (json.dumps(manifest, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def export(source: Path, output: Path, baseline: str, selector: str, schema_path: Path) -> dict[str, Any]:
    source = source.resolve()
    output = output.resolve(strict=False)
    if not source.is_dir():
        raise ExportError("EXPORT_SOURCE", f"source directory does not exist: {source}")
    reject_nesting(source, output)
    if output.exists():
        raise ExportError("EXPORT_OUTPUT_EXISTS", f"output already exists: {output}")
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    expected = derive_export_set(source, baseline, selector, schema)
    project_ids = {meta.get("project_id") for _, meta in expected.values()}
    if len(project_ids) != 1:
        raise ExportError("EXPORT_PROJECT_DRIFT", "export set does not have exactly one project_id")

    entries: list[dict[str, str]] = []
    payload: dict[str, bytes] = {}
    for relative, (path, meta) in expected.items():
        data = normalized_bytes(path)
        payload[relative] = data
        entries.append({
            "path": relative,
            "artifact_id": str(meta["artifact_id"]),
            "artifact_type": str(meta["artifact_type"]),
            "digest": digest_bytes(data),
        })
    manifest = {
        "format_version": "v1.0.0",
        "schema_id": schema["schema_id"],
        "project_id": next(iter(project_ids)),
        "baseline": baseline,
        "selector": selector,
        "entries": entries,
    }
    encoded_manifest = manifest_bytes(manifest)
    package_hex = hashlib.sha256(encoded_manifest).hexdigest()

    output.parent.mkdir(parents=True, exist_ok=True)
    temporary = Path(tempfile.mkdtemp(prefix=f".{output.name}-", dir=output.parent))
    try:
        for relative, data in payload.items():
            destination = temporary / Path(relative)
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(data)
        (temporary / "handoff-manifest.json").write_bytes(encoded_manifest)
        (temporary / "manifest.sha256").write_text(
            f"{package_hex}  handoff-manifest.json\n", encoding="utf-8", newline="\n"
        )
        (temporary / "package.sha256").write_text(
            f"sha256:{package_hex}\n", encoding="utf-8", newline="\n"
        )
        temporary.replace(output)
    except Exception:
        shutil.rmtree(temporary, ignore_errors=True)
        raise
    return {
        "result": "PASS",
        "output": str(output),
        "entry_count": len(entries),
        "package_hash": f"sha256:{package_hex}",
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
        result = export(args.source, args.output, args.baseline, args.selector, args.schema.resolve())
    except (ExportError, OSError, UnicodeError, json.JSONDecodeError) as exc:
        code = exc.code if isinstance(exc, ExportError) else "EXPORT_IO"
        result = {"result": "FAIL", "findings": [{"code": code, "message": str(exc)}]}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["result"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
