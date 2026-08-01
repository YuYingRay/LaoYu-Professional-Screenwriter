from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PRE_WP2B_TEMPLATE_SHA256 = {
    "project-manifest.md": "A0311A7CC3175DEAD528CE35B32C17A1406F2F885F5D428095CBB798A4A003B1",
    "source-links.md": "EE14A7309E9C4ECCEB504629CFB1CBCB83D9D4FF2F589B76B547D4854C7C065E",
    "upstream-notices.md": "5CFC171E52A121E2AEF44F2BED7F8E08D1BCE53ADA476F4D14EBC43342399ABE",
    "change-log.md": "401B5E6A7A6DD0CC885353D099562FFC6B49EC7C93B6FBF9E72ACD4689D3F1DD",
}


def frontmatter(path: Path) -> dict[str, str]:
    lines = path.read_text(encoding="utf-8").splitlines()
    result: dict[str, str] = {}
    if not lines or lines[0].strip() != "---":
        return result
    for line in lines[1:]:
        if line.strip() == "---":
            break
        if ":" in line and not line.startswith(" "):
            key, value = line.split(":", 1)
            result[key.strip()] = value.strip()
    return result


class CandidateContractTests(unittest.TestCase):
    def test_contract_is_in_review_and_generated_from_schema(self) -> None:
        contract = ROOT / "governance" / "control-plane-contract.md"
        meta = frontmatter(contract)
        self.assertEqual(meta["project_baseline"], "CONTRACT-v0.2.0")
        self.assertEqual(meta["artifact_version"], "v0.2.0")
        self.assertEqual(meta["status"], "IN_REVIEW")
        self.assertEqual(meta["review_decision"], "PENDING")
        self.assertNotIn("LOCKED", contract.read_text(encoding="utf-8").split("## 0.", 1)[0])

        generated = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "gen_contract_tables.py"), str(ROOT), "--check"],
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(generated.returncode, 0, generated.stdout + generated.stderr)

    def test_contract_explicitly_allows_single_person_review_and_approval(self) -> None:
        text = (ROOT / "governance" / "control-plane-contract.md").read_text(encoding="utf-8")
        self.assertIn("单人项目", text)
        self.assertIn("reviewer", text)
        self.assertIn("approver", text)
        self.assertIn("可以是同一人", text)

    def test_migration_notice_is_verified_and_coupled(self) -> None:
        notice = ROOT / "governance" / "notices" / "NOTICE-CONTRACT-001.md"
        meta = frontmatter(notice)
        self.assertEqual(meta["artifact_id"], "NOTICE-CONTRACT-001")
        self.assertEqual(meta["status"], "IN_REVIEW")
        self.assertEqual(meta["notice_status"], "VERIFIED")
        self.assertIn("SCHEMA", meta["coupling"])
        self.assertIn("BASELINE", meta["coupling"])
        self.assertNotEqual(meta["affected_paths"], "[]")
        self.assertNotEqual(meta["migration_tasks"], "[]")
        self.assertNotEqual(meta["verification_refs"], "[]")
        self.assertNotEqual(meta["change_records"], "[]")

    def test_real_manifest_keeps_active_and_declares_candidate(self) -> None:
        meta = frontmatter(ROOT / "governance" / "project-manifest.md")
        self.assertEqual(meta["artifact_id"], "PROJECT-PROFESSIONAL-SCREENWRITER")
        self.assertEqual(meta["project_id"], "PROJECT-PROFESSIONAL-SCREENWRITER")
        self.assertEqual(meta["project_baseline"], "CONTRACT-v0.1.0")
        self.assertEqual(meta["candidate_baseline"], "CONTRACT-v0.2.0")

    def test_four_blank_governance_templates_are_separate(self) -> None:
        template_root = ROOT / "templates" / "governance"
        migration = json.loads(
            (ROOT / "governance" / "placeholder-migration-map.json").read_text(encoding="utf-8")
        )
        migration_files = {record["path"]: record for record in migration["files"]}
        for name, expected_digest in PRE_WP2B_TEMPLATE_SHA256.items():
            path = template_root / name
            self.assertTrue(path.is_file(), name)
            self.assertIn("PROJECT-[[SLUG]]", path.read_text(encoding="utf-8"), name)
            record = migration_files[path.relative_to(ROOT).as_posix()]
            self.assertEqual(record["before_sha256"], expected_digest, name)
            self.assertNotEqual(record["after_sha256"], expected_digest, name)
        self.assertNotIn("[[SLUG]]", frontmatter(ROOT / "governance" / "project-manifest.md")["project_id"])

    def test_root_governance_instances_use_concrete_identity(self) -> None:
        for name in ["project-manifest.md", "source-links.md", "upstream-notices.md", "change-log.md"]:
            meta = frontmatter(ROOT / "governance" / name)
            self.assertEqual(meta["project_id"], "PROJECT-PROFESSIONAL-SCREENWRITER", name)
            self.assertEqual(meta["owner"], "LaoYu-Professional-Screenwriter", name)

    def test_project_validator_no_longer_skips_contract(self) -> None:
        source = (ROOT / "scripts" / "validate_project.py").read_text(encoding="utf-8")
        skip_line = next(line for line in source.splitlines() if "input-brief.md" in line)
        self.assertNotIn("control-plane-contract.md", skip_line)

    def test_candidate_aggregate_gate_is_strict_clean(self) -> None:
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "check_all.py"), str(ROOT), "--baseline", "candidate", "--mode", "strict", "--skip-unit-tests", "--skip-e2e"],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("PASS: lint_repo strict", result.stdout)


if __name__ == "__main__":
    unittest.main()
