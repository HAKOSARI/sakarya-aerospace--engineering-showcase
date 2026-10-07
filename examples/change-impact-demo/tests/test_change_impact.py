import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from change_impact import Change, Requirement, assess


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


if __name__ == "__main__":
    unittest.main()
