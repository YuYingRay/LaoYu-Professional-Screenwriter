"""Schema-driven installation ownership and template-closure checks."""

from __future__ import annotations

import fnmatch
import os
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path


SUPPORTED_TEMPLATE_SCENARIOS = {
    "project-manifest",
    "draft-artifact",
    "feature-screenplay",
}


@dataclass(frozen=True)
class OwnershipFinding:
    code: str
    path: str
    message: str


@dataclass(frozen=True)
class OwnershipRecord:
    path: str
    owner: str | None
    tracked: bool
    matched_rules: tuple[str, ...]


@dataclass(frozen=True)
class OwnershipReport:
    records: tuple[OwnershipRecord, ...]
    findings: tuple[OwnershipFinding, ...]


def matches_pattern(path: str, pattern: str) -> bool:
    path = path.strip("/")
    pattern = pattern.strip("/")
    if pattern == "**/__pycache__/**":
        return "__pycache__" in path.split("/")
    if pattern.endswith("/**"):
        prefix = pattern[:-3]
        return fnmatch.fnmatchcase(path, prefix) or fnmatch.fnmatchcase(path, pattern)
    return fnmatch.fnmatchcase(path, pattern)


def _git_paths(root: Path, *args: str) -> set[str]:
    result = subprocess.run(
        ["git", *args], cwd=root, text=True, encoding="utf-8", errors="replace",
        capture_output=True, check=False,
    )
    if result.returncode != 0:
        return set()
    return {line.replace("\\", "/").strip("/") for line in result.stdout.splitlines() if line}


def _ignored_paths(root: Path, paths: list[str]) -> set[str]:
    if not paths:
        return set()
    result = subprocess.run(
        ["git", "check-ignore", "--stdin"], cwd=root, input="\n".join(paths) + "\n",
        text=True, encoding="utf-8", errors="replace", capture_output=True, check=False,
    )
    if result.returncode not in {0, 1}:
        return set()
    return {line.replace("\\", "/").strip("/") for line in result.stdout.splitlines() if line}


def _fixture_owner(path: str, owner: str) -> str:
    if owner != "fixture-project:<name>":
        return owner
    match = re.match(r"tests/([^/]+-fixture)(?:/|$)", path)
    return f"fixture-project:{match.group(1)}" if match else owner


def classify_path(
    path: str,
    ownership: dict,
    *,
    tracked: bool,
    ignored: bool = False,
) -> tuple[OwnershipRecord, list[OwnershipFinding]]:
    rules = ownership["rules"]
    matches = [
        rule for rule in rules
        if any(matches_pattern(path, pattern) for pattern in rule["patterns"])
    ]
    excluded = next((rule for rule in rules if rule["id"] == "OWN-EXCLUDED"), None)
    if ignored and excluded is not None and excluded not in matches:
        matches.append(excluded)

    findings: list[OwnershipFinding] = []
    if len(matches) > 1:
        code = ownership.get("multi_match_error", "MULTI_OWNED_FILE")
        findings.append(OwnershipFinding(
            code, path, "matches multiple ownership rules: " + ", ".join(r["id"] for r in matches)
        ))
        return OwnershipRecord(path, None, tracked, tuple(r["id"] for r in matches)), findings
    if len(matches) == 1:
        rule = matches[0]
        owner = _fixture_owner(path, rule["owner"])
        return OwnershipRecord(path, owner, tracked, (rule["id"],)), findings

    if tracked:
        owner = ownership["fallback"]["tracked"]
        return OwnershipRecord(path, owner, True, ()), findings
    if any(matches_pattern(path, item) for item in ownership.get("untracked_allowlist", [])):
        return OwnershipRecord(path, "allowed-untracked", False, ()), findings

    code = ownership["fallback"].get("untracked_error", "UNDECLARED_INSTALL_CONTENT")
    findings.append(OwnershipFinding(code, path, "untracked installation content has no owner"))
    return OwnershipRecord(path, None, False, ()), findings


def analyze_ownership(
    root: Path,
    schema: dict,
    *,
    tracked_paths: set[str] | None = None,
) -> OwnershipReport:
    root = root.resolve()
    ownership = schema["ownership"]
    files: list[str] = []
    empty_directories: list[str] = []
    for current, directories, names in os.walk(root, followlinks=False):
        current_path = Path(current)
        if current_path != root and not directories and not names:
            empty_directories.append(current_path.relative_to(root).as_posix())
        files.extend((current_path / name).relative_to(root).as_posix() for name in names)

    tracked = tracked_paths
    if tracked is None:
        tracked = _git_paths(root, "ls-files")
    else:
        tracked = {path.replace("\\", "/").strip("/") for path in tracked}
    ignored = _ignored_paths(root, files + empty_directories)

    records: list[OwnershipRecord] = []
    findings: list[OwnershipFinding] = []
    for path in sorted(files):
        record, path_findings = classify_path(
            path, ownership, tracked=path in tracked, ignored=path in ignored
        )
        records.append(record)
        findings.extend(path_findings)

    declared_empty = ownership.get("declared_empty_directories", [])
    for path in sorted(empty_directories):
        record, path_findings = classify_path(
            path, ownership, tracked=False, ignored=path in ignored
        )
        explicitly_owned = bool(record.matched_rules) and not path_findings
        explicitly_declared = any(matches_pattern(path, item) for item in declared_empty)
        if not explicitly_owned and not explicitly_declared:
            findings.append(OwnershipFinding(
                ownership.get("empty_directory_error", "UNDECLARED_EMPTY_DIR"),
                path,
                "empty directory is not declared by ownership schema",
            ))

    return OwnershipReport(tuple(records), tuple(findings))


def template_closure_findings(root: Path, schema: dict) -> list[OwnershipFinding]:
    discovered = {
        path.relative_to(root).as_posix()
        for path in (root / "templates").rglob("*")
        if path.is_file() and path.suffix.lower() in {".md", ".fountain"}
    }
    registry = schema.get("template_closure", {})
    findings: list[OwnershipFinding] = []
    for path in sorted(discovered - set(registry)):
        findings.append(OwnershipFinding("UNTESTED_TEMPLATE", path, "template has no scenario or fragment declaration"))
    for path in sorted(set(registry) - discovered):
        findings.append(OwnershipFinding("STALE_TEMPLATE_REGISTRATION", path, "registered template does not exist"))
    for path in sorted(discovered & set(registry)):
        entry = registry[path]
        kind = entry.get("kind")
        if kind == "fragment":
            if not entry.get("reason"):
                findings.append(OwnershipFinding("UNTESTED_TEMPLATE", path, "fragment declaration requires a reason"))
        elif kind == "scenario":
            if entry.get("scenario") not in SUPPORTED_TEMPLATE_SCENARIOS:
                findings.append(OwnershipFinding("UNTESTED_TEMPLATE", path, "template scenario is not implemented"))
        else:
            findings.append(OwnershipFinding("UNTESTED_TEMPLATE", path, "kind must be scenario or fragment"))
    return findings


def hygiene_findings(root: Path, schema: dict) -> list[OwnershipFinding]:
    names = set(schema["ownership"].get("reserved_install_names", []))
    return [
        OwnershipFinding("RESERVED_INSTALL_DOC", path.relative_to(root).as_posix(), "legacy package document name remains")
        for path in sorted(root.rglob("*"))
        if path.is_file()
        and path.name in names
        and ".git" not in path.relative_to(root).parts
        and "__pycache__" not in path.relative_to(root).parts
    ]
