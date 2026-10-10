import sys
import unittest
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from change_impact import Change, Requirement, assess, load_requirements, load_change


class ChangeImpactTests(unittest.TestCase):
    def test_changed_dependency_requires_reverification(self):
        req = Requirement(
            "R1", "Timing", frozenset({"RATE"}), "CFG-A"
        )
        change = Change("C1", frozenset({"RATE"}), "CFG-B")
        self.assertEqual(assess([req], change)[0].outcome, "REVERIFY")

    def test_unchanged_dependency_matching_config_is_reuse_candidate(self):
        req = Requirement(
            "R2", "Display", frozenset({"DISPLAY"}), "CFG-B"
        )
        change = Change("C1", frozenset({"RATE"}), "CFG-B")
        self.assertEqual(assess([req], change)[0].outcome, "REUSE")

    def test_config_mismatch_routes_to_review(self):
        req = Requirement(
            "R3", "Power", frozenset({"POWER"}), "CFG-A"
        )
        change = Change("C1", frozenset({"RATE"}), "CFG-B")
        self.assertEqual(assess([req], change)[0].outcome, "REVIEW")

    def test_load_requirements_normalizes_dependencies(self):
        csv_content = "req_id,title,dependencies,evidence_config\nR_TEST,Test, RATE ; POWER ,CFG-A\n"
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "requirements.csv"
            path.write_text(csv_content, encoding="utf-8")
            self.assertEqual(load_requirements(path)[0].dependencies, frozenset({"RATE", "POWER"}))

    def test_load_change_normalizes_changed_items(self):
        csv_content = "change_id,changed_items,new_config\nCHG_TEST, RATE ; POWER ,CFG-B\n"
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "change.csv"
            path.write_text(csv_content, encoding="utf-8")
            self.assertEqual(load_change(path).changed_items, frozenset({"RATE", "POWER"}))

    def test_assess_reverify_after_csv_normalization(self):
        with tempfile.TemporaryDirectory() as directory:
            req_path = Path(directory) / "requirements.csv"
            change_path = Path(directory) / "change.csv"
            req_path.write_text("req_id,title,dependencies,evidence_config\nR1,Test, RATE ,CFG-B\n", encoding="utf-8")
            change_path.write_text("change_id,changed_items,new_config\nC1,RATE,CFG-B\n", encoding="utf-8")
            self.assertEqual(assess(load_requirements(req_path), load_change(change_path))[0].outcome, "REVERIFY")


if __name__ == "__main__":
    unittest.main()
