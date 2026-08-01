from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path


CANDIDATE_RE = re.compile(r"(?<!\[)\[([^\[\]\r\n]{1,200})\]")
CHECKBOX_RE = re.compile(r"(?m)^- \[[ xX]\]")
MARKDOWN_LINK_RE = re.compile(r"!?\[[^\]\r\n]+\]\([^\)\r\n]*\)")
LIST_LINE_RE = re.compile(
    r"^(upstream_ids|evidence_refs|affected_ids|affected_paths|coupling|migration_tasks):\s*(\[.*\])\s*$"
)
FIXED_CHANGELOG_LABELS = {"ARCH-001", "ARCH-002", "ARCH-003", "Unreleased", "v0.1.0"}
REGEX_CLASSES = {"0-9", "0-9A-Za-z"}
SOURCE_SUFFIXES = {".md", ".fountain"}
MAP_RELATIVE = Path("governance/placeholder-migration-map.json")
ENTRIES_RELATIVE = Path("governance/placeholder-migration-entries.tsv")
ENTRY_FIELDS = ["path", "line", "column", "token", "old", "new", "action", "reason"]


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest().upper()


def run_git(root: Path, *args: str) -> bytes:
    return subprocess.check_output(["git", *args], cwd=root)


def source_paths(root: Path, source_ref: str) -> list[Path]:
    names = run_git(root, "ls-tree", "-r", "--name-only", source_ref).decode("utf-8").splitlines()
    return [Path(name) for name in names if Path(name).suffix.lower() in SOURCE_SUFFIXES]


def working_paths(root: Path) -> list[Path]:
    names = run_git(root, "ls-files", "*.md", "*.fountain").decode("utf-8").splitlines()
    return [Path(name) for name in names]


def classify(path: Path, line: str, start: int, end: int, token: str) -> tuple[str, str]:
    marker = line[start:end]
    if token in {"", " ", "x", "X"}:
        return "PRESERVE", "markdown-checkbox"
    if line[end : end + 1] in {"(", "["} or line.lstrip().startswith(marker + ":"):
        return "PRESERVE", "markdown-link-syntax"
    list_match = LIST_LINE_RE.match(line.strip())
    if list_match and list_match.group(2) == marker:
        return "PRESERVE", "frontmatter-list-syntax"
    posix = path.as_posix()
    if posix.endswith("change-log.md") and token in FIXED_CHANGELOG_LABELS:
        return "PRESERVE", "fixed-changelog-label"
    if posix == "governance/open-questions.md" and token in REGEX_CLASSES:
        return "PRESERVE", "regex-character-class"
    return "MIGRATE", "fillable-slot"


def scan(path: Path, text: str) -> list[dict[str, object]]:
    results: list[dict[str, object]] = []
    offset = 0
    for line_number, line in enumerate(text.splitlines(keepends=True), 1):
        bare = line.rstrip("\r\n")
        for match in CANDIDATE_RE.finditer(bare):
            action, reason = classify(path, bare, match.start(), match.end(), match.group(1))
            old = match.group(0)
            results.append(
                {
                    "path": path.as_posix(),
                    "line": line_number,
                    "column": match.start() + 1,
                    "start": offset + match.start(),
                    "end": offset + match.end(),
                    "token": match.group(1),
                    "old": old,
                    "new": f"[[{match.group(1)}]]" if action == "MIGRATE" else old,
                    "action": action,
                    "reason": reason,
                }
            )
        offset += len(line)
    return results


def protected_counts(texts: dict[Path, str], suffix: str) -> dict[str, int]:
    checkbox = sum(len(CHECKBOX_RE.findall(text)) for path, text in texts.items() if path.suffix == ".md")
    links = sum(len(MARKDOWN_LINK_RE.findall(text)) for path, text in texts.items() if path.suffix == ".md")
    lists = sum(
        1
        for text in texts.values()
        for line in text.splitlines()
        if LIST_LINE_RE.match(line.strip())
    )
    return {
        f"checkbox_markers_{suffix}": checkbox,
        f"markdown_links_{suffix}": links,
        f"frontmatter_list_lines_{suffix}": lists,
    }


def write_entries(path: Path, entries: list[dict[str, object]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=ENTRY_FIELDS, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        for entry in entries:
            writer.writerow({field: entry[field] for field in ENTRY_FIELDS})


def read_entries(path: Path) -> list[dict[str, object]]:
    with path.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    for row in rows:
        row["line"] = int(row["line"])
        row["column"] = int(row["column"])
    return rows


def build_and_apply(root: Path, source_ref: str) -> int:
    paths = source_paths(root, source_ref)
    source_texts: dict[Path, str] = {}
    after_texts: dict[Path, str] = {}
    entries: list[dict[str, object]] = []
    file_records: list[dict[str, object]] = []

    for path in paths:
        source_bytes = run_git(root, "show", f"{source_ref}:{path.as_posix()}")
        source_text = source_bytes.decode("utf-8")
        source_texts[path] = source_text
        found = scan(path, source_text)
        entries.extend(found)

        migrated = [entry for entry in found if entry["action"] == "MIGRATE"]
        after = source_text
        for entry in reversed(migrated):
            start = int(entry["start"])
            end = int(entry["end"])
            if after[start:end] != entry["old"]:
                raise RuntimeError(f"source span drift: {path}:{entry['line']}")
            after = after[:start] + str(entry["new"]) + after[end:]
        after_texts[path] = after

        if migrated:
            working = (root / path).read_bytes()
            normalized = working.replace(b"\r\n", b"\n")
            if normalized != source_bytes:
                raise RuntimeError(f"working file differs from {source_ref}: {path}")
            newline = "\r\n" if b"\r\n" in working else "\n"
            output = after if newline == "\n" else after.replace("\n", "\r\n")
            (root / path).write_bytes(output.encode("utf-8"))
            file_records.append(
                {
                    "path": path.as_posix(),
                    "before_sha256": sha256(source_bytes),
                    "after_sha256": sha256(after.encode("utf-8")),
                    "migrated_occurrences": len(migrated),
                }
            )

    before_counts = protected_counts(source_texts, "before")
    after_counts = protected_counts(after_texts, "after")
    map_data = {
        "work_package": "WP3b-placeholders",
        "source_ref": source_ref,
        "rule": "Each listed MIGRATE occurrence changes only [slot] to [[slot]]; PRESERVE entries are syntax or fixed facts.",
        "summary": {
            "candidate_occurrences": len(entries),
            "migrated_occurrences": sum(entry["action"] == "MIGRATE" for entry in entries),
            "preserved_occurrences": sum(entry["action"] == "PRESERVE" for entry in entries),
            "changed_files": len(file_records),
        },
        "protected_counts": {**before_counts, **after_counts},
        "files": file_records,
        "entries_file": ENTRIES_RELATIVE.as_posix(),
    }
    map_path = root / MAP_RELATIVE
    write_entries(root / ENTRIES_RELATIVE, entries)
    map_path.write_text(json.dumps(map_data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(
        "APPLIED: "
        f"{map_data['summary']['migrated_occurrences']} placeholders across "
        f"{map_data['summary']['changed_files']} files; "
        f"preserved {map_data['summary']['preserved_occurrences']} classified occurrences"
    )
    return 0


def validate_map_shape(data: dict[str, object], entries: list[dict[str, object]]) -> list[str]:
    errors: list[str] = []
    summary = data.get("summary")
    protected = data.get("protected_counts")
    if not isinstance(summary, dict) or not isinstance(protected, dict):
        return ["map is missing summary or protected_counts"]
    if data.get("entries_file") != ENTRIES_RELATIVE.as_posix():
        errors.append("map points to the wrong entries file")
    actions = Counter(entry.get("action") for entry in entries)
    if actions["MIGRATE"] != summary.get("migrated_occurrences"):
        errors.append("migrated occurrence count drift")
    if actions["PRESERVE"] != summary.get("preserved_occurrences"):
        errors.append("preserved occurrence count drift")
    for key in ("checkbox_markers", "frontmatter_list_lines", "markdown_links"):
        if protected.get(f"{key}_before") != protected.get(f"{key}_after"):
            errors.append(f"protected syntax changed: {key}")
    for entry in entries:
        if not isinstance(entry.get("line"), int) or not isinstance(entry.get("column"), int):
            errors.append(f"invalid occurrence position: {entry.get('path')} {entry.get('token')}")
        if entry.get("action") == "MIGRATE" and entry.get("new") != f"[[{entry.get('token')}]]":
            errors.append(f"invalid replacement: {entry.get('path')} {entry.get('token')}")
    return errors


def check(root: Path, snapshot: bool) -> int:
    map_path = root / MAP_RELATIVE
    if not map_path.is_file():
        print(f"FAIL: missing {MAP_RELATIVE}", file=sys.stderr)
        return 1
    entries_path = root / ENTRIES_RELATIVE
    if not entries_path.is_file():
        print(f"FAIL: missing {ENTRIES_RELATIVE}", file=sys.stderr)
        return 1
    data = json.loads(map_path.read_text(encoding="utf-8"))
    entries = read_entries(entries_path)
    errors = validate_map_shape(data, entries)

    for path in working_paths(root):
        text = (root / path).read_text(encoding="utf-8")
        for entry in scan(path, text):
            if entry["action"] == "MIGRATE":
                errors.append(f"legacy placeholder remains: {path}:{entry['line']} {entry['old']}")

    if snapshot:
        entries_by_path: dict[str, list[dict[str, object]]] = defaultdict(list)
        for entry in entries:
            if entry["action"] == "MIGRATE":
                entries_by_path[entry["path"]].append(entry)
        for record in data["files"]:
            path = root / record["path"]
            current = path.read_bytes().replace(b"\r\n", b"\n")
            if sha256(current) != record["after_sha256"]:
                errors.append(f"post-migration snapshot drift: {record['path']}")
                continue
            restored = current.decode("utf-8")
            grouped = Counter(
                (str(entry["new"]), str(entry["old"])) for entry in entries_by_path[record["path"]]
            )
            for (new, old), count in grouped.items():
                if restored.count(new) < count:
                    errors.append(f"replacement count drift: {record['path']} {new}")
                    break
                restored = restored.replace(new, old, count)
            if sha256(restored.encode("utf-8")) != record["before_sha256"]:
                errors.append(f"migration is not reversible: {record['path']}")

    if errors:
        for error in errors:
            print(f"FAIL: {error}", file=sys.stderr)
        return 1
    print(f"PASS: placeholder migration map ({data['summary']['migrated_occurrences']} migrated)")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Build or verify the explicit WP3b placeholder migration map.")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--apply", action="store_true")
    mode.add_argument("--check", action="store_true")
    parser.add_argument("root", type=Path)
    parser.add_argument("--source-ref", default="phase-2-complete-v1.0.7")
    parser.add_argument("--snapshot", action="store_true")
    args = parser.parse_args()
    root = args.root.resolve()
    if args.apply:
        return build_and_apply(root, args.source_ref)
    return check(root, args.snapshot)


if __name__ == "__main__":
    raise SystemExit(main())
