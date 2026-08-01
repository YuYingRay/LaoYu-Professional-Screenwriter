from __future__ import annotations

import csv
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class PriorityStackSingleSourceTests(unittest.TestCase):
    original_references = [
        "adversarial-review-rubric.md",
        "ai-production-handoff.md",
        "film-series-format.md",
        "hook-paywall-engine.md",
        "screenplay-format-cn-en.md",
        "short-drama-playbook.md",
        "story-bible-templates.md",
    ]

    def test_contract_is_the_only_priority_stack_source(self) -> None:
        contract = (ROOT / "governance" / "control-plane-contract.md").read_text(encoding="utf-8")
        self.assertEqual(contract.count("### 7.1 规则冲突优先级"), 1)
        self.assertIn("不可覆盖的安全、法律、权利与技术事实", contract)

    def test_local_stacks_are_pointers_or_confirmed_absent(self) -> None:
        for name in self.original_references:
            text = (ROOT / "references" / name).read_text(encoding="utf-8")
            self.assertNotIn("> 主 SKILL.md 的安全", text, name)
        for name in self.original_references[1:6]:
            text = (ROOT / "references" / name).read_text(encoding="utf-8")
            self.assertIn("control-plane-contract.md#71-规则冲突优先级", text, name)

    def test_migration_map_covers_all_seven_references(self) -> None:
        path = ROOT / "governance" / "wp5-priority-stack-map.tsv"
        with path.open(encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle, delimiter="\t"))
        self.assertEqual({row["source_path"] for row in rows}, {
            f"references/{name}" for name in self.original_references
        })
        self.assertEqual(len(rows), 7)
        self.assertEqual(
            {row["decision"] for row in rows},
            {"MIGRATE_TO_POINTER", "NO_LOCAL_STACK"},
        )


if __name__ == "__main__":
    unittest.main()
