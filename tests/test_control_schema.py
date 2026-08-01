from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "governance" / "control-schema.json"
GENERATOR_PATH = ROOT / "scripts" / "gen_contract_tables.py"


def load_generator():
    spec = importlib.util.spec_from_file_location("gen_contract_tables", GENERATOR_PATH)
    if spec is None or spec.loader is None:
        raise AssertionError("generator module cannot be loaded")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class ControlSchemaTests(unittest.TestCase):
    def test_schema_contains_every_frozen_authority_domain(self) -> None:
        schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))

        self.assertEqual(schema["contract_id"], "CONTRACT-v0.2.0")
        self.assertEqual(
            set(schema["artifact_statuses"]),
            {"DRAFT", "IN_REVIEW", "APPROVED", "LOCKED", "SUPERSEDED", "BLOCKED"},
        )
        self.assertEqual(len(schema["finding_required_fields"]), 9)
        self.assertEqual(schema["id_prefixes"]["VERTICAL_EPISODE"]["prefix"], "EP-")
        self.assertIn("coupling", schema["required_fields"]["by_type"]["NOTICE"])
        self.assertEqual(schema["ownership"]["fallback"]["untracked"], "deny_unless_allowlisted")
        self.assertEqual(schema["ownership"]["untracked_allowlist"], [])
        self.assertIn("runs/**", schema["run_payload"]["exclude"])
        self.assertEqual(schema["export_scope"]["closure_edge"], "upstream_ids")
        self.assertEqual(schema["production_ready"]["minimum_project_stage"], "PREP")
        self.assertEqual(
            {item["id"] for item in schema["baseline_impact_selectors"]},
            {"BASELINE_MATCH", "SCHEMA_SECTION_REF"},
        )

    def test_status_matrix_matches_frozen_plan(self) -> None:
        schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        matrix = schema["required_fields"]["by_status"]

        self.assertEqual(matrix["DRAFT"], [])
        self.assertEqual(matrix["IN_REVIEW"], ["review_id", "review_decision", "evidence_refs"])
        self.assertEqual(matrix["APPROVED"], ["reviewer", "approver", "test_run_id", "conformance_level"])
        self.assertEqual(matrix["LOCKED"], ["lock_scope", "content_digest"])
        self.assertEqual(matrix["SUPERSEDED"], ["superseded_by"])
        self.assertEqual(matrix["BLOCKED"], ["blocked_reason"])

    def test_generated_tables_are_deterministic_and_schema_derived(self) -> None:
        generator = load_generator()
        schema = generator.load_schema(SCHEMA_PATH)

        first = generator.render_schema_tables(schema)
        second = generator.render_schema_tables(schema)

        self.assertEqual(first, second)
        self.assertIn("<!-- GENERATED:schema START -->", first)
        self.assertIn("| `IN_REVIEW` |", first)
        self.assertIn("| `EP-` | `VERTICAL_EPISODE` |", first)
        self.assertIn("finding_id", first)
        self.assertIn("| `IN_PROGRESS` |", first)
        self.assertIn("migration_tasks", first)
        self.assertIn("<!-- GENERATED:schema END -->", first)

    def test_check_rejects_a_hand_edited_generated_block(self) -> None:
        generator = load_generator()
        schema = generator.load_schema(SCHEMA_PATH)
        block = generator.render_schema_tables(schema)

        with tempfile.TemporaryDirectory(prefix="psw-schema-test-") as temp_dir:
            contract = Path(temp_dir) / "contract.md"
            contract.write_text(f"before\n\n{block}\n\nafter\n", encoding="utf-8", newline="\n")
            clean = subprocess.run(
                [sys.executable, str(GENERATOR_PATH), "--schema", str(SCHEMA_PATH), "--contract", str(contract), "--check"],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(clean.returncode, 0, clean.stdout + clean.stderr)

            contract.write_text(
                contract.read_text(encoding="utf-8").replace("finding_id", "finding_id_manual", 1),
                encoding="utf-8",
                newline="\n",
            )
            dirty = subprocess.run(
                [sys.executable, str(GENERATOR_PATH), "--schema", str(SCHEMA_PATH), "--contract", str(contract), "--check"],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertNotEqual(dirty.returncode, 0)
            self.assertIn("GENERATED_BLOCK_DRIFT", dirty.stdout + dirty.stderr)


if __name__ == "__main__":
    unittest.main()
