from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "validate.yml"


class CiContractTests(unittest.TestCase):
    def test_workflow_matches_the_frozen_matrix_and_single_entry(self) -> None:
        text = WORKFLOW.read_text(encoding="utf-8")
        for required in [
            "push:",
            "pull_request:",
            "ubuntu-latest",
            "windows-latest",
            '"3.11"',
            '"3.13"',
            "sha256sum -c manifest.sha256",
        ]:
            self.assertIn(required, text)
        python_commands = re.findall(r"run:\s*(python -X utf8[^\r\n]+)", text)
        self.assertEqual(python_commands, ["python -X utf8 scripts/check_all.py ."])


if __name__ == "__main__":
    unittest.main()
