from __future__ import annotations

import csv
import hashlib
import re
import subprocess
import unittest
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MAP = ROOT / "governance" / "a5-license-boundary-map.tsv"
SOURCE_COMMIT = "e552a98"


def git_source(path: str) -> str:
    return subprocess.check_output(
        ["git", "show", f"{SOURCE_COMMIT}:{path}"], cwd=ROOT
    ).decode("utf-8")


class A5LicenseBoundaryTests(unittest.TestCase):
    def test_real_skill_license_is_byte_identical(self) -> None:
        digest = hashlib.sha256((ROOT / "LICENSES" / "skill-license.md").read_bytes()).hexdigest().upper()
        self.assertEqual(digest, "A027B1997847A63D4908EC2DB75C0401E6BFF9B10F5DD03FE8F0E744BBD63D6B")

    def test_every_legacy_line_has_exactly_one_destination(self) -> None:
        with MAP.open(encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle, delimiter="\t"))
        grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
        for row in rows:
            grouped[row["source_path"]].append(row)
        for source_path in [
            "LICENSES/README.md",
            "LICENSES/asset-rights-register.md",
            "LICENSES/third-party-notices.md",
        ]:
            source_lines = git_source(source_path).splitlines(keepends=True)
            covered: list[int] = []
            for row in grouped[source_path]:
                start, end = int(row["start_line"]), int(row["end_line"])
                covered.extend(range(start, end + 1))
                destination = (ROOT / row["destination"]).read_text(encoding="utf-8")
                marker = f"<!-- A5-SOURCE {source_path}:{start}-{end} -->"
                pattern = re.compile(re.escape(marker) + r"\n(.*?)<!-- A5-END -->", re.DOTALL)
                match = pattern.search(destination)
                self.assertIsNotNone(match, marker)
                self.assertEqual(match.group(1), "".join(source_lines[start - 1:end]))
            self.assertEqual(sorted(covered), list(range(1, len(source_lines) + 1)), source_path)
            self.assertEqual(len(covered), len(set(covered)), source_path)

    def test_licenses_contains_facts_not_slots_or_fictional_examples(self) -> None:
        for name in ["asset-rights-register.md", "third-party-notices.md"]:
            text = (ROOT / "LICENSES" / name).read_text(encoding="utf-8")
            self.assertNotIn("[[", text, name)
            for fictional in ["ASSET-MUS-004", "ASSET-UI-008", "NOTICE-021", "ACH-001"]:
                self.assertNotIn(fictional, text, name)

    def test_methods_and_blank_forms_have_separate_destinations(self) -> None:
        for path in [
            "references/asset-rights-method.md",
            "references/rights-clearance-guide.md",
            "references/third-party-rights-method.md",
            "templates/governance/asset-rights-register.md",
            "templates/governance/third-party-notices.md",
        ]:
            self.assertTrue((ROOT / path).is_file(), path)

    def test_new_blank_forms_are_declared_template_fragments(self) -> None:
        import json

        schema = json.loads((ROOT / "governance" / "control-schema.json").read_text(encoding="utf-8"))
        for path in [
            "templates/governance/asset-rights-register.md",
            "templates/governance/third-party-notices.md",
        ]:
            self.assertEqual(schema["template_closure"][path]["kind"], "fragment")

    def test_skill_routes_rights_clearance_through_one_default_entry(self) -> None:
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        row = next(line for line in skill.splitlines() if line.startswith("| 权利清理 |"))

        self.assertIn("`references/rights-clearance-guide.md`", row)
        self.assertNotIn("asset-rights-method.md", row)
        self.assertNotIn("third-party-rights-method.md", row)

    def test_guide_routes_method_files_only_from_existing_input_facts(self) -> None:
        guide = (ROOT / "references" / "rights-clearance-guide.md").read_text(
            encoding="utf-8"
        )

        required_contract = [
            "未提供具体资产或材料清单",
            "只读取本指南",
            "输入中明确存在自有或委托资产",
            "`references/asset-rights-method.md` 的相关章节",
            "输入中明确存在第三方材料",
            "`references/third-party-rights-method.md` 的相关章节",
            "输入中明确同时存在两类资产",
            "禁止默认通读任一方法文件",
            "不得依据本轮生成的交付物反向触发",
        ]
        for clause in required_contract:
            with self.subTest(clause=clause):
                self.assertIn(clause, guide)


if __name__ == "__main__":
    unittest.main()
