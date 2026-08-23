from __future__ import annotations

import hashlib
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def run(*command: str, cwd: Path) -> None:
    result = subprocess.run(command, cwd=cwd, text=True, capture_output=True, check=False)
    if result.returncode:
        raise AssertionError(result.stdout + result.stderr)


class LfReproducibilityTests(unittest.TestCase):
    def test_policy_makes_text_bytes_checkout_independent(self) -> None:
        attributes = ROOT / ".gitattributes"
        self.assertTrue(attributes.is_file())
        policy = attributes.read_text(encoding="utf-8")
        for pattern in ["*", "*.md", "*.py", "*.json", "*.yaml", "*.yml", "*.tsv", "*.fountain", "*.sha256", "LICENSE", ".gitignore", ".gitattributes"]:
            self.assertIn(pattern, policy)

        with tempfile.TemporaryDirectory(prefix="psw-lf-") as temp_dir:
            temp = Path(temp_dir)
            source = temp / "source"
            source.mkdir()
            run("git", "init", cwd=source)
            (source / ".gitattributes").write_bytes(attributes.read_bytes())
            names = ["sample.md", "sample.py", "sample.json", "sample.yaml", "sample.yml", "sample.tsv", "sample.fountain", "sample.sha256", "LICENSE", ".gitignore"]
            for name in names:
                (source / name).write_bytes(b"alpha\nbeta\n")
            run("git", "add", "-A", cwd=source)
            run("git", "-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid", "commit", "-m", "fixture", cwd=source)

            manifests: list[dict[str, str]] = []
            for value in ["true", "false"]:
                checkout = temp / f"checkout-{value}"
                run("git", "-c", f"core.autocrlf={value}", "clone", "--no-local", str(source), str(checkout), cwd=temp)
                manifest: dict[str, str] = {}
                for name in [".gitattributes", *names]:
                    data = (checkout / name).read_bytes()
                    self.assertNotIn(b"\r\n", data, f"{value}: {name}")
                    manifest[name] = hashlib.sha256(data).hexdigest()
                manifests.append(manifest)
            self.assertEqual(manifests[0], manifests[1])


if __name__ == "__main__":
    unittest.main()
