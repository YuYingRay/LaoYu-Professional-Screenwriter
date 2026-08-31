from __future__ import annotations

import csv
import json
import re
import unittest
from pathlib import Path

from scripts.run_protocol import managed_files


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


class DirectoryStructureSingleSourceTests(unittest.TestCase):
    def test_struct_layered_has_one_canonical_reference(self) -> None:
        path = ROOT / "references" / "project-directory-structure.md"
        text = path.read_text(encoding="utf-8")
        self.assertIn("# STRUCT-LAYERED 项目目录规范", text)
        for directory in [
            "governance/", "development/", "script/", "production/", "assets/", "archive/"
        ]:
            self.assertIn(directory, text)

    def test_three_conflicting_trees_are_replaced_with_pointer(self) -> None:
        for path in [
            "references/story-bible-templates.md",
            "references/ai-production-handoff.md",
            "references/short-drama-playbook.md",
        ]:
            text = (ROOT / path).read_text(encoding="utf-8")
            self.assertIn("references/project-directory-structure.md", text, path)
        self.assertNotIn("00_admin/", (ROOT / "references/story-bible-templates.md").read_text(encoding="utf-8"))
        self.assertNotIn("01_script/", (ROOT / "references/ai-production-handoff.md").read_text(encoding="utf-8"))

    def test_schema_run_payload_uses_layered_roots(self) -> None:
        import json

        schema = json.loads((ROOT / "governance" / "control-schema.json").read_text(encoding="utf-8"))
        includes = set(schema["run_payload"]["include"])
        self.assertTrue({"governance/**", "development/**", "script/**", "production/**", "assets/**", "archive/**"} <= includes)
        self.assertFalse({"story/**", "structure/**", "scenes/**", "episodes/**", "reviews/**"} & includes)
        self.assertIn("development/review-reports/**", schema["export_scope"]["fixed_exclude"])

    def test_both_fixtures_are_legal_layered_subsets(self) -> None:
        expected = {
            "feature-project-fixture": [
                "development/story-bible.md",
                "development/feature-outline.md",
                "development/scene-cards/SC-001.md",
                "development/review-reports/REVIEW-001.md",
                "script/master/script.fountain",
                "production/handoff/handoff.md",
            ],
            "vertical-project-fixture": [
                "development/story-bible.md",
                "development/season-outline.md",
                "development/episode-outlines/EP-001.md",
                "development/scene-cards/SC-101.md",
                "development/review-reports/REVIEW-001.md",
                "script/master/script.fountain",
                "production/handoff/handoff.md",
            ],
        }
        legacy = {"story", "structure", "scenes", "episodes", "reviews"}
        for fixture, paths in expected.items():
            root = ROOT / "tests" / fixture
            self.assertFalse(legacy & {path.name for path in root.iterdir()}, fixture)
            for path in paths:
                self.assertTrue((root / path).is_file(), f"{fixture}/{path}")

    def test_directory_migration_map_covers_three_conflicts(self) -> None:
        path = ROOT / "governance" / "wp5-directory-structure-map.tsv"
        with path.open(encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle, delimiter="\t"))
        self.assertEqual(len(rows), 3)
        self.assertEqual({row["decision"] for row in rows}, {"REPLACE_WITH_STRUCT_LAYERED_POINTER"})


class ChangeLevelSingleSourceTests(unittest.TestCase):
    duplicate_sources = [
        "README.md",
        "references/story-bible-templates.md",
        "templates/story-bible.md",
        "templates/governance/project-manifest.md",
        "governance/project-manifest.md",
        "templates/governance/upstream-notices.md",
        "governance/upstream-notices.md",
    ]

    def test_contract_holds_all_four_change_levels_and_gates(self) -> None:
        text = (ROOT / "governance" / "control-plane-contract.md").read_text(encoding="utf-8")
        self.assertEqual(text.count("### 7.2 变更等级与最低门禁"), 1)
        for required in [
            "L1：表达级",
            "L2：局部剧情级",
            "L3：结构级",
            "L4：项目级",
            "项目只能加严",
        ]:
            self.assertIn(required, text)

    def test_previous_definitions_are_contract_pointers(self) -> None:
        for path in self.duplicate_sources:
            if not (ROOT / path).exists():
                self.assertEqual(path, "README.md")
                continue
            text = (ROOT / path).read_text(encoding="utf-8")
            self.assertIn("control-plane-contract.md#72-变更等级与最低门禁", text, path)
            self.assertNotIn("| L1 表达级 | 非事实性的台词压缩", text, path)
            self.assertNotIn("### L1：表层变更", text, path)
            self.assertNotIn("## L1：文字或表达级", text, path)

    def test_change_level_map_covers_every_previous_definition(self) -> None:
        path = ROOT / "governance" / "wp5-change-level-map.tsv"
        with path.open(encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle, delimiter="\t"))
        self.assertEqual({row["source_path"] for row in rows}, set(self.duplicate_sources))
        self.assertEqual({row["decision"] for row in rows}, {"REPLACE_WITH_CONTRACT_POINTER"})


class NoticeSingleSourceTests(unittest.TestCase):
    def test_schema_and_contract_point_to_one_notice_template(self) -> None:
        import json

        schema = json.loads((ROOT / "governance" / "control-schema.json").read_text(encoding="utf-8"))
        registered = [path for path in schema["template_closure"] if path.endswith("notice.md")]
        self.assertEqual(registered, ["templates/notice.md"])
        template = (ROOT / "templates" / "notice.md").read_text(encoding="utf-8")
        self.assertIn("governance/notices/NOTICE-<scope>-<NNN>-<slug>.md", template)
        self.assertIn("文件名必须以 frontmatter 的 `artifact_id` 开头", template)

    def test_notice_instances_have_one_directory_and_hyphenated_names(self) -> None:
        notice_dir = ROOT / "governance" / "notices"
        names = {path.name for path in notice_dir.glob("NOTICE-*.md")}
        self.assertIn("NOTICE-CONTRACT-001.md", names)
        self.assertIn("NOTICE-LIC-001-formal-licensor.md", names)
        self.assertFalse((ROOT / "governance" / "upstream-notices").exists())
        self.assertFalse(any("_" in name for name in names))

    def test_notice_migration_map_records_template_rule_and_instance_move(self) -> None:
        path = ROOT / "governance" / "wp5-notice-source-map.tsv"
        with path.open(encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle, delimiter="\t"))
        self.assertEqual(len(rows), 2)
        self.assertEqual(
            {row["decision"] for row in rows},
            {"MERGE_NAMING_RULE_INTO_TEMPLATE", "MOVE_INSTANCE_TO_CANONICAL_DIRECTORY"},
        )


class ControlPlaneMapBoundaryTests(unittest.TestCase):
    def test_stale_manual_control_plane_map_is_removed(self) -> None:
        self.assertFalse((ROOT / "governance" / "control-plane-file-map.md").exists())
        validator = (ROOT / "scripts" / "validate_skill.py").read_text(encoding="utf-8")
        self.assertNotIn("control-plane-file-map.md", validator)


class SkillTriggerBoundaryTests(unittest.TestCase):
    def test_frontmatter_description_is_two_sentences_and_contextual(self) -> None:
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        description = next(line for line in skill.splitlines() if line.startswith("description: "))
        value = description.removeprefix("description: ")
        self.assertEqual(value.count("."), 2)
        self.assertIn("screenwriting, story-development, or screen-production context", value)
        self.assertNotIn("review, ultrathink, or adversarial review", value)

    def test_openai_metadata_matches_the_same_trigger_boundary(self) -> None:
        metadata = (ROOT / "agents" / "openai.yaml").read_text(encoding="utf-8")
        self.assertIn("剧本与影视故事语境", metadata)
        self.assertIn("ultrathink as a review trigger only within this context", metadata)


class PackageReadmeBoundaryTests(unittest.TestCase):
    def test_root_readme_is_repository_source_only(self) -> None:
        readme = ROOT / "README.md"
        self.assertTrue(readme.is_file())
        schema = json.loads((ROOT / "governance" / "control-schema.json").read_text(encoding="utf-8"))
        rule = next(item for item in schema["ownership"]["rules"] if item["id"] == "OWN-REPOSITORY-README")
        self.assertEqual(rule["patterns"], ["README.md"])
        self.assertEqual(rule["owner"], "repo-source")
        self.assertFalse(rule["project_validation"])
        self.assertFalse(rule["model_load"])
        self.assertFalse(rule["run_payload"])
        self.assertNotIn("README.md", schema["ownership"]["reserved_install_names"])

    def test_root_readme_is_excluded_from_run_payload(self) -> None:
        schema_path = ROOT / "governance" / "control-schema.json"
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        self.assertIn("README.md", schema["run_payload"]["exclude"])
        managed = {path.relative_to(ROOT).as_posix() for path in managed_files(ROOT, schema_path)}
        self.assertNotIn("README.md", managed)

    def test_non_root_reserved_readmes_are_removed_or_renamed(self) -> None:
        self.assertFalse((ROOT / "LICENSES" / "README.md").exists())
        self.assertFalse((ROOT / "tests" / "README.md").exists())
        self.assertTrue((ROOT / "tests" / "testing-guide.md").is_file())
        self.assertEqual(list(ROOT.rglob("README.md")), [ROOT / "README.md"])

    def test_runtime_sources_remain_canonical_with_repository_readme(self) -> None:
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        for required in [
            "## 使用边界",
            "未经结构开发就直接索要",
            "## 典型输入与产出顺序",
            "长片开发",
            "竖屏付费短剧",
            "场景或对白重写",
            "tests/testing-guide.md",
        ]:
            self.assertIn(required, skill)
        rubric = (ROOT / "references" / "adversarial-review-rubric.md").read_text(encoding="utf-8")
        self.assertIn("## 7.7.1 场景与对白重写七问", rubric)
        self.assertIn("这场如何迫使下一场发生", rubric)

    def test_readme_migration_map_records_every_disposition(self) -> None:
        path = ROOT / "governance" / "wp5-readme-boundary-map.tsv"
        with path.open(encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle, delimiter="\t"))
        self.assertEqual(
            {row["source_path"] for row in rows},
            {"README.md", "tests/README.md", "LICENSES/README.md", "governance/upstream-notices/README.md"},
        )
        self.assertIn("EXPORT_MAINTAINER_CONTENT", {row["decision"] for row in rows})
        self.assertIn("RENAME_TESTING_GUIDE", {row["decision"] for row in rows})

    def test_readme_migration_map_has_no_local_absolute_paths(self) -> None:
        path = ROOT / "governance" / "wp5-readme-boundary-map.tsv"
        text = path.read_text(encoding="utf-8")
        self.assertIsNone(re.search(r"(?m)(?:^|\t)[A-Za-z]:[\\/]", text))


class ExportPackageUsageTests(unittest.TestCase):
    def test_handoff_reference_uses_the_implemented_export_cli(self) -> None:
        text = (ROOT / "references" / "ai-production-handoff.md").read_text(encoding="utf-8")
        section = text.split("## 15.3 确定性导出包使用说明", 1)[1]
        for required in [
            "governance/control-schema.json",
            "export_scope",
            "project / season / episode",
            "expected set == manifest set == actual output set",
            "输出目录必须位于源项目 payload 树之外",
            "WP4b",
            "scripts/export_handoff.py",
            "scripts/verify_handoff.py",
            "只有 verifier 返回 `PASS`",
            "不得手工复制后宣称 VERIFIED",
        ]:
            self.assertIn(required, section)
        self.assertNotIn("尚未提供可执行 exporter/verifier", section)


def assert_in_order(test: unittest.TestCase, text: str, clauses: list[str]) -> None:
    cursor = -1
    for clause in clauses:
        with test.subTest(clause=clause):
            position = text.find(clause, cursor + 1)
            test.assertGreater(position, cursor, clause)
            cursor = position


class DirectorModuleContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        cls.director = (ROOT / "references" / "cinematography-director.md").read_text(
            encoding="utf-8"
        )
        cls.handoff = (ROOT / "references" / "ai-production-handoff.md").read_text(
            encoding="utf-8"
        )

    def test_multi_beat_video_routes_through_sequence_design_before_prompt(self) -> None:
        assert_in_order(
            self,
            self.skill,
            [
                "多节拍",
                "Director Sequence Card",
                "Camera Direction Card",
                "模型执行 Prompt",
            ],
        )

    def test_scene_beat_shot_segment_objects_are_not_interchangeable(self) -> None:
        for clause in [
            "`Scene`",
            "`Beat`",
            "`Sequence`",
            "`Shot`",
            "`Segment`",
            "一个 Segment 可承载一个 Shot",
            "一个 Sequence 可由一个或多个 Segment",
        ]:
            with self.subTest(clause=clause):
                self.assertIn(clause, self.director)

    def test_continuous_take_requires_a_timed_attention_path(self) -> None:
        for clause in [
            "Timed Attention Path",
            "观众先看什么",
            "获得什么可见事实",
            "观看距离/景别如何变化",
            "不能覆盖全部 ESSENTIAL 信息",
            "回到多 Shot Coverage",
        ]:
            with self.subTest(clause=clause):
                self.assertIn(clause, self.director)

    def test_native_multi_shot_requires_entry_evidence_or_explicit_poc(self) -> None:
        for clause in [
            "NATIVE_MULTI_SHOT",
            "INDEPENDENT_SHOTS",
            "平台入口",
            "预注册 Shot/关键切点数量",
            "一条成功样本只证明可行性",
            "明确标为 POC",
        ]:
            with self.subTest(clause=clause):
                self.assertIn(clause, self.director)

    def test_editability_has_structured_direction_critical_cuts_and_recovery(self) -> None:
        for clause in [
            "DIRECTOR_CRITICAL",
            "Screen Direction Map",
            "Camera Side",
            "Entry / Exit",
            "Recovery Plan",
            "ESSENTIAL Beat",
        ]:
            with self.subTest(clause=clause):
                self.assertIn(clause, self.director)

    def test_handoff_compiles_story_logic_before_generation_prompt(self) -> None:
        assert_in_order(
            self,
            self.handoff,
            [
                "Beat Map",
                "Coverage Map",
                "Edit Map",
                "Shot Design",
                "Segment Packing",
                "Director Sequence Card",
                "模型执行 Prompt",
            ],
        )

    def test_review_uses_hard_veto_context_isolation_and_human_final_judgment(self) -> None:
        for clause in [
            "不可抵消硬门",
            "上下文隔离",
            "独立模型只能作为辅助证据",
            "余老师保留最终审美和生产裁决",
        ]:
            with self.subTest(clause=clause):
                self.assertIn(clause, self.director)


if __name__ == "__main__":
    unittest.main()
