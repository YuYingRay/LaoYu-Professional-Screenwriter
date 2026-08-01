from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE_FIXTURE = ROOT / "tests" / "production-ready-fixture"
EXPORTER = ROOT / "scripts" / "export_handoff.py"
VERIFIER = ROOT / "scripts" / "verify_handoff.py"
SCHEMA = ROOT / "governance" / "control-schema.json"


def invoke(script: Path, source: Path, output: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            sys.executable, str(script), str(source), str(output),
            "--baseline", "PROJECT-PROD-v1.0.0", "--selector", "project",
            "--schema", str(SCHEMA),
        ],
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        check=False,
    )


def result_json(result: subprocess.CompletedProcess[str]) -> dict[str, object]:
    return json.loads(result.stdout)


def rewrite_sidecars(output: Path, manifest: dict[str, object]) -> None:
    data = (json.dumps(manifest, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")
    (output / "handoff-manifest.json").write_bytes(data)
    digest = hashlib.sha256(data).hexdigest()
    (output / "manifest.sha256").write_text(f"{digest}  handoff-manifest.json\n", encoding="utf-8", newline="\n")
    (output / "package.sha256").write_text(f"sha256:{digest}\n", encoding="utf-8", newline="\n")


class HandoffExportTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory(prefix="psw-export-")
        self.root = Path(self.temp.name)
        self.source = self.root / "source"
        shutil.copytree(SOURCE_FIXTURE, self.source)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def export(self, name: str = "output") -> Path:
        output = self.root / name
        result = invoke(EXPORTER, self.source, output)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(result_json(result)["result"], "PASS")
        return output

    def verify(self, output: Path) -> subprocess.CompletedProcess[str]:
        return invoke(VERIFIER, self.source, output)

    def test_two_exports_are_byte_deterministic_and_verify(self) -> None:
        first = self.export("first")
        second = self.export("second")
        self.assertEqual((first / "handoff-manifest.json").read_bytes(), (second / "handoff-manifest.json").read_bytes())
        self.assertEqual((first / "package.sha256").read_bytes(), (second / "package.sha256").read_bytes())
        verified = self.verify(first)
        self.assertEqual(verified.returncode, 0, verified.stdout + verified.stderr)

    def test_line_endings_do_not_change_package_hash(self) -> None:
        first = self.export("lf")
        story = self.source / "development" / "story-bible.md"
        story.write_bytes(story.read_bytes().replace(b"\n", b"\r\n"))
        second = self.export("crlf")
        self.assertEqual((first / "package.sha256").read_bytes(), (second / "package.sha256").read_bytes())

    def test_verifier_derives_expected_set_when_payload_and_manifest_share_an_omission(self) -> None:
        output = self.export()
        manifest_path = output / "handoff-manifest.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        omitted = "governance/rights-register.md"
        manifest["entries"] = [item for item in manifest["entries"] if item["path"] != omitted]
        (output / omitted).unlink()
        rewrite_sidecars(output, manifest)
        result = self.verify(output)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("EXPORT_SET_MISMATCH", result.stdout)

    def test_tamper_add_delete_and_rename_all_fail(self) -> None:
        mutations = {
            "tamper": lambda output: (output / "development" / "story-bible.md").write_text("tampered\n", encoding="utf-8"),
            "add": lambda output: (output / "extra.md").write_text("extra\n", encoding="utf-8"),
            "delete": lambda output: (output / "script" / "master" / "script.fountain").unlink(),
            "rename": lambda output: (output / "governance" / "rights-register.md").rename(output / "governance" / "rights-renamed.md"),
        }
        for name, mutation in mutations.items():
            with self.subTest(name=name):
                output = self.export(name)
                mutation(output)
                result = self.verify(output)
                self.assertNotEqual(result.returncode, 0, name)

    def test_manifest_path_escape_fails_even_with_recomputed_sidecars(self) -> None:
        output = self.export()
        manifest = json.loads((output / "handoff-manifest.json").read_text(encoding="utf-8"))
        manifest["entries"][0]["path"] = "../escape.md"
        rewrite_sidecars(output, manifest)
        result = self.verify(output)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("EXPORT_PATH_ESCAPE", result.stdout)

    def test_source_and_output_nesting_are_rejected_in_both_directions(self) -> None:
        nested_output = self.source / "production" / "exports" / "package"
        first = invoke(EXPORTER, self.source, nested_output)
        self.assertNotEqual(first.returncode, 0)
        self.assertIn("EXPORT_NESTING", first.stdout)

        container = self.root / "container"
        nested_source = container / "source"
        shutil.copytree(SOURCE_FIXTURE, nested_source)
        second = invoke(EXPORTER, nested_source, container)
        self.assertNotEqual(second.returncode, 0)
        self.assertIn("EXPORT_NESTING", second.stdout)

    def test_linked_payload_is_rejected_when_platform_allows_links(self) -> None:
        output = self.export()
        payload = output / "development" / "story-bible.md"
        target = output / "development" / "story-bible-target.md"
        payload.rename(target)
        try:
            os.symlink(target, payload)
        except OSError as exc:
            self.skipTest(f"links unavailable: {exc}")
        result = self.verify(output)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("EXPORT_LINK", result.stdout)


if __name__ == "__main__":
    unittest.main()
