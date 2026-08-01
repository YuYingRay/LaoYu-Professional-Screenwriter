from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "templates" / "production-handoff.md"


class ProductionHandoffStructureTests(unittest.TestCase):
    def test_handoff_has_the_six_minimum_data_structures(self) -> None:
        text = TEMPLATE.read_text(encoding="utf-8")
        for heading in [
            "## 2. 镜头与关键帧清单",
            "## 3. 资产清单",
            "## 4. 角色与场景连续性约束",
            "## 5. 声音、字幕与 UI 清单",
            "## 6. AI / 实拍执行说明与失败降级",
            "## 7. 权利、来源与人工复核",
            "## 8. 子交付物 ID 与嵌入规则",
        ]:
            self.assertIn(heading, text)

    def test_handoff_can_answer_the_five_execution_questions(self) -> None:
        text = TEMPLATE.read_text(encoding="utf-8")
        required_columns = [
            "关键动作",
            "关键帧 / 输入资产",
            "失败触发",
            "最小降级方案",
            "人工复核人",
            "批准决定",
            "证据路径",
            "规范 ID",
        ]
        for column in required_columns:
            self.assertIn(column, text, column)

    def test_subdeliverables_use_contract_prefixes(self) -> None:
        text = TEMPLATE.read_text(encoding="utf-8")
        for prefix in ["SHOT-[[ID]]", "AUDIO-[[ID]]", "SUB-[[ID]]", "RGT-[[ID]]", "SRC-[[ID]]"]:
            self.assertIn(prefix, text)

    def test_methodology_remains_in_the_reference(self) -> None:
        reference = (ROOT / "references" / "ai-production-handoff.md").read_text(encoding="utf-8")
        for heading in ["# 5. 镜头表", "# 6. 关键帧与分镜", "# 7. 提示词架构"]:
            self.assertIn(heading, reference)


if __name__ == "__main__":
    unittest.main()
