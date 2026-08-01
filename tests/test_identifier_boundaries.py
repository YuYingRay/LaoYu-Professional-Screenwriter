from __future__ import annotations

import unittest

from scripts import validate_project, validate_skill


class IdentifierBoundaryTests(unittest.TestCase):
    def test_scene_ids_are_visible_next_to_cjk_and_underscore_only(self) -> None:
        positive = ["场景SC-101", "第SC-101场", "SC-012_PARIS", "SC-101"]
        negative = ["XSC-101", "SC-101ABC", "SC-101old"]
        for sample in positive:
            with self.subTest(sample=sample):
                self.assertEqual(validate_project.SCENE_RE.findall(sample), [sample.removeprefix("场景").removeprefix("第").removesuffix("场")[:6]])
        for sample in negative:
            with self.subTest(sample=sample):
                self.assertIsNone(validate_project.SCENE_RE.search(sample))

    def test_legacy_notice_ids_are_visible_next_to_cjk_and_underscore_only(self) -> None:
        positive = ["旧编号UN-003", "UN-003_old", "UN-003"]
        negative = ["XUN-003", "UN-003ABC", "UN-003old"]
        for pattern in [validate_project.LEGACY_NOTICE_RE, validate_skill.LEGACY_NOTICE_RE]:
            for sample in positive:
                with self.subTest(pattern=pattern.pattern, sample=sample):
                    self.assertIsNotNone(pattern.search(sample))
            for sample in negative:
                with self.subTest(pattern=pattern.pattern, sample=sample):
                    self.assertIsNone(pattern.search(sample))

    def test_tbd_is_visible_next_to_cjk_and_underscore_only(self) -> None:
        positive = ["占位TBD", "TBD_value", "TBD"]
        negative = ["XTBD", "TBDx", "TBD1"]
        for sample in positive:
            with self.subTest(sample=sample):
                self.assertIsNotNone(validate_project.PLACEHOLDER_RE.search(sample))
        for sample in negative:
            with self.subTest(sample=sample):
                self.assertIsNone(validate_project.PLACEHOLDER_RE.search(sample))

    def test_gate_patterns_do_not_use_word_boundaries(self) -> None:
        for pattern in [
            validate_project.SCENE_RE,
            validate_project.PLACEHOLDER_RE,
            validate_project.LEGACY_NOTICE_RE,
            validate_skill.LEGACY_NOTICE_RE,
        ]:
            self.assertNotIn(r"\b", pattern.pattern)


if __name__ == "__main__":
    unittest.main()
