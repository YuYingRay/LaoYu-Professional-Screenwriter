from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "governance" / "control-schema.json"
TEMPLATES = {
    "PROJECT_MANIFEST": "templates/governance/project-manifest.md",
    "SOURCE_REGISTER": "templates/governance/source-links.md",
    "NOTICE_INDEX": "templates/governance/upstream-notices.md",
    "CHANGE_LOG": "templates/governance/change-log.md",
    "STORY_BIBLE": "templates/story-bible.md",
    "OUTLINE": "templates/episode-outline.md",
    "VERTICAL_EPISODE": "templates/vertical-episode.md",
    "SCENE_CARD": "templates/scene-card.md",
    "REVIEW": "templates/review-report.md",
    "NOTICE": "templates/notice.md",
    "PRODUCTION_HANDOFF": "templates/production-handoff.md",
}


def frontmatter_line(path: Path, key: str) -> str:
    prefix = f"{key}:"
    return next(line for line in path.read_text(encoding="utf-8").splitlines() if line.startswith(prefix))


def render_ids(values: list[str]) -> str:
    return "[]" if not values else "[" + ", ".join(f'"{value}"' for value in values) + "]"


class UpstreamDefaultTests(unittest.TestCase):
    def test_schema_defines_each_formal_template_default(self) -> None:
        schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
        defaults = schema["upstream_defaults"]
        self.assertEqual(set(defaults), set(TEMPLATES) | {"SCRIPT_MASTER"})
        self.assertEqual(defaults["PROJECT_MANIFEST"], [])
        self.assertEqual(defaults["STORY_BIBLE"], ["[[PROJECT-ID]]"])
        self.assertEqual(
            defaults["PRODUCTION_HANDOFF"],
            ["[[BIBLE-ID]]", "[[SCRIPT-ID]]", "[[REVIEW-ID]]"],
        )
        self.assertEqual(defaults["SCRIPT_MASTER"], ["[[BIBLE-ID]]", "[[OUTLINE-ID]]"])

    def test_template_frontmatter_is_rendered_from_schema_defaults(self) -> None:
        defaults = json.loads(SCHEMA.read_text(encoding="utf-8"))["upstream_defaults"]
        for artifact_type, relative in TEMPLATES.items():
            line = frontmatter_line(ROOT / relative, "upstream_ids")
            self.assertEqual(line, f"upstream_ids: {render_ids(defaults[artifact_type])}", relative)

    def test_contract_keeps_one_directional_dependency_rule(self) -> None:
        contract = (ROOT / "governance" / "control-plane-contract.md").read_text(encoding="utf-8")
        self.assertIn("### Template upstream 默认值", contract)
        self.assertIn("只声明 `upstream_ids`", contract)
        self.assertIn("不允许人工维护两套", contract)

    def test_open_notice_tracks_upstream_default_migration(self) -> None:
        notice = (ROOT / "governance" / "notices" / "NOTICE-CONTRACT-001.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("MIG-WP3B-UPSTREAM", notice)


if __name__ == "__main__":
    unittest.main()
