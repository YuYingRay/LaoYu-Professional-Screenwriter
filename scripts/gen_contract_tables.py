#!/usr/bin/env python3
"""Render the contract's machine-authoritative tables from control-schema.json."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


START_MARKER = "<!-- GENERATED:schema START -->"
END_MARKER = "<!-- GENERATED:schema END -->"


def load_schema(path: Path) -> dict[str, Any]:
    schema = json.loads(path.read_text(encoding="utf-8"))
    required = {
        "contract_id",
        "artifact_statuses",
        "notice_statuses",
        "id_prefixes",
        "required_fields",
        "finding_required_fields",
        "notice",
        "ownership",
        "run_payload",
        "export_scope",
        "baseline_impact_selectors",
    }
    missing = sorted(required - schema.keys())
    if missing:
        raise ValueError(f"schema missing required keys: {', '.join(missing)}")
    return schema


def code_list(values: list[str]) -> str:
    return ", ".join(f"`{value}`" for value in values) if values else "—"


def render_schema_tables(schema: dict[str, Any]) -> str:
    base = schema["required_fields"]["base"]
    by_status = schema["required_fields"]["by_status"]
    by_type = schema["required_fields"]["by_type"]

    lines = [
        START_MARKER,
        "",
        f"> 生成源：`governance/control-schema.json`（`{schema['schema_id']}`）。",
        "> 本区块禁止手改；运行 `python -X utf8 scripts/gen_contract_tables.py . --check` 对账。",
        "",
        "### 状态必填字段",
        "",
        "| 状态 | 基本字段 | 状态附加字段 |",
        "|---|---|---|",
    ]
    for status in schema["artifact_statuses"]:
        lines.append(f"| `{status}` | {code_list(base)} | {code_list(by_status[status])} |")

    lines.extend([
        "",
        "### 类型附加字段",
        "",
        "| Artifact 类型 | 附加字段 |",
        "|---|---|",
    ])
    for artifact_type in sorted(by_type):
        lines.append(f"| `{artifact_type}` | {code_list(by_type[artifact_type])} |")

    lines.extend([
        "",
        "### ID 前缀",
        "",
        "| 前缀 | Artifact 类型 | 示例 |",
        "|---|---|---|",
    ])
    for artifact_type, item in sorted(
        schema["id_prefixes"].items(), key=lambda pair: (pair[1]["prefix"], pair[0])
    ):
        lines.append(f"| `{item['prefix']}` | `{artifact_type}` | `{item['example']}` |")

    lines.extend([
        "",
        "### Review Finding 九字段",
        "",
        code_list(schema["finding_required_fields"]),
        "",
        "### Notice 状态与耦合",
        "",
        f"notice_status：{code_list(schema['notice_statuses'])}",
        "",
        f"coupling：{code_list(schema['notice']['coupling_values'])}",
        "",
        "| `notice_status` | 附加必填字段 |",
        "|---|---|",
    ])
    for constraint in schema["notice"]["constraints"]:
        lines.append(
            f"| `{constraint['notice_status']}` | {code_list(constraint['require'])} |"
        )
    lines.extend([
        "",
        END_MARKER,
    ])
    return "\n".join(lines)


def generated_span(text: str) -> tuple[int, int]:
    start = text.find(START_MARKER)
    end = text.find(END_MARKER)
    if start < 0 or end < 0 or end < start:
        raise ValueError("GENERATED_BLOCK_MISSING")
    end += len(END_MARKER)
    if text.find(START_MARKER, start + len(START_MARKER)) >= 0 or text.find(END_MARKER, end) >= 0:
        raise ValueError("GENERATED_BLOCK_MULTIPLE")
    return start, end


def replace_generated_block(text: str, block: str) -> str:
    start, end = generated_span(text)
    return text[:start] + block + text[end:]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", nargs="?", type=Path, default=Path("."))
    parser.add_argument("--schema", type=Path)
    parser.add_argument("--contract", type=Path)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--write", action="store_true")
    args = parser.parse_args(argv)

    root = args.root.resolve()
    schema_path = (args.schema or root / "governance" / "control-schema.json").resolve()
    contract_path = (args.contract or root / "governance" / "control-plane-contract.md").resolve()
    try:
        schema = load_schema(schema_path)
        expected = render_schema_tables(schema)
        current = contract_path.read_text(encoding="utf-8")
        start, end = generated_span(current)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(str(exc))
        return 1

    actual = current[start:end]
    if args.write:
        if actual != expected:
            contract_path.write_text(
                replace_generated_block(current, expected), encoding="utf-8", newline="\n"
            )
            print(f"UPDATED: {contract_path}")
        else:
            print(f"PASS: generated block already current in {contract_path}")
        return 0

    if actual != expected:
        print(f"GENERATED_BLOCK_DRIFT: {contract_path}")
        return 1
    print(f"PASS: generated block matches {schema_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
