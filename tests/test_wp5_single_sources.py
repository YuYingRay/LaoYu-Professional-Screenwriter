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


class ReviewRolesSingleSourceTests(unittest.TestCase):
    templates = [
        "templates/episode-outline.md",
        "templates/review-report.md",
        "templates/scene-card.md",
        "templates/story-bible.md",
        "templates/vertical-episode.md",
    ]
    examples = [
        "examples/dialogue-rewrite-example.md",
        "examples/feature-outline-example.md",
    ]

    def test_rubric_holds_method_report_and_domain_adaptations(self) -> None:
        text = (ROOT / "references" / "adversarial-review-rubric.md").read_text(encoding="utf-8")
        for required in [
            "# 3. 评审角色",
            "# 9. 审查报告模板",
            "## 3.5 领域适配与横切检查",
            "节奏编辑",
            "信任守门人",
            "手机可读性",
        ]:
            self.assertIn(required, text)

    def test_templates_point_to_both_distinct_rubric_responsibilities(self) -> None:
        for path in self.templates:
            text = (ROOT / path).read_text(encoding="utf-8")
            self.assertNotIn("## 怀疑观众", text, path)
            self.assertIn("adversarial-review-rubric.md#3-评审角色", text, path)
            self.assertIn("adversarial-review-rubric.md#9-审查报告模板", text, path)

    def test_examples_keep_results_but_not_normative_checklists(self) -> None:
        dialogue = (ROOT / self.examples[0]).read_text(encoding="utf-8")
        feature = (ROOT / self.examples[1]).read_text(encoding="utf-8")
        for path, text in [(self.examples[0], dialogue), (self.examples[1], feature)]:
            self.assertIn("adversarial-review-rubric.md#3-评审角色", text, path)
            self.assertIn("审查结果", text, path)
        self.assertIn("18 分钟倒计时与水压窗口", dialogue)
        self.assertIn("隧道打开但有损失", feature)

    def test_role_migration_map_has_seven_reviewed_locations(self) -> None:
        path = ROOT / "governance" / "wp5-review-role-map.tsv"
        with path.open(encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle, delimiter="\t"))
        self.assertEqual(len(rows), 7)
        self.assertEqual(
            {row["source_path"] for row in rows},
            set(self.templates + self.examples),
        )
        self.assertEqual(
            {row["decision"] for row in rows},
            {"REPLACE_WITH_POINTER", "KEEP_FILLED_RESULT_WITH_POINTER"},
        )


if __name__ == "__main__":
    unittest.main()
