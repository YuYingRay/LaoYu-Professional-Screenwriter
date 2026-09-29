import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from check_prompt_contract import check


class PromptContractTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.file = self.root / "current.json"
        self.data = {"prompt_contract": {"headings": ["全局", "逐图绑定", "镜头描述"]},
                     "execution_allowed": False,
                     "inputs": [{"id": "A", "video_prompt_path": "PROMPT.txt", "status": "DRAFT"}]}
        self.text = "全局\n五秒单镜。\n逐图绑定\n图1为实际首帧。\n镜头描述\n抬眼后停步。"

    def run_check(self):
        self.file.write_text(json.dumps(self.data, ensure_ascii=False), encoding="utf-8")
        (self.root / "PROMPT.txt").write_text(self.text, encoding="utf-8")
        return check(self.file)

    def test_project_specific_structure_passes(self):
        self.assertEqual(self.run_check(), [])

    def test_prose_regression_fails(self):
        self.text = "以图1为首帧，人物抬眼，镜头缓慢前移。"
        self.assertTrue(self.run_check())

    def test_reordered_or_repeated_sections_fail(self):
        for text in ["镜头描述\n动作\n全局\n格式\n逐图绑定\n图1", self.text + "\n全局\n重复"]:
            with self.subTest(text=text):
                self.text = text
                self.assertTrue(self.run_check())

    def test_empty_section_fails(self):
        self.text = self.text.replace("图1为实际首帧。", "")
        self.assertTrue(self.run_check())

    def test_two_current_versions_for_same_task_fail(self):
        self.data["inputs"].append(dict(self.data["inputs"][0]))
        self.assertTrue(self.run_check())

    def test_multiple_paths_in_one_task_fail(self):
        self.data["inputs"][0]["video_prompt_path"] = ["long.txt", "short.txt"]
        self.assertTrue(self.run_check())

    def test_missing_current_file_fails(self):
        self.data["inputs"][0]["video_prompt_path"] = "missing.txt"
        self.assertTrue(self.run_check())

    def test_format_pass_does_not_release_draft(self):
        self.data["execution_allowed"] = True
        self.assertTrue(self.run_check())
        self.data["inputs"][0]["status"] = "APPROVED"
        self.assertEqual(self.run_check(), [])


if __name__ == "__main__":
    unittest.main()
