import sys
import unittest
from copy import deepcopy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from analyzer import evaluate, evidence_applicability, markdown_report

def baseline():
    return {
        "id": "TC-01", "overhead_fraction": 0.10,
        "producer": {"format": "GRAY8", "transport": "GIGE", "frame_rate_fps": 15, "frame_size_bytes": 40000},
        "consumer": {"accepted_formats": ["GRAY8"], "transport": "GIGE",
                     "capacity_mbps": 800, "processing_rate_fps": 20, "buffer_frames": 3,
                     "buffer_policy": "DROP_OLDEST", "drop_tolerance_pct": 5,
                     "max_latency_ms": 150,
                     "latency_components": [{"worst_ms": 10, "source": "MEASURED"},
                                            {"worst_ms": 30, "source": "MEASURED"}]}
    }

class CompatibilityTests(unittest.TestCase):
    def test_01_compatible(self):
        self.assertEqual(evaluate(baseline())["overall"], "COMPATIBLE")

    def test_02_format_mismatch(self):
        s = baseline()
        s["producer"]["format"] = "RGB24"
        s["consumer"]["converter_available"] = True
        self.assertEqual(evaluate(s)["overall"], "REVIEW")

    def test_03_bandwidth_deficit(self):
        s = baseline()
        s["producer"].update(frame_rate_fps=30, frame_size_bytes=1228800)
        s["consumer"]["capacity_mbps"] = 0.9
        self.assertEqual(evaluate(s)["overall"], "INCOMPATIBLE")

    def test_04_rate_overflow(self):
        s = baseline()
        s["producer"]["frame_rate_fps"] = 60
        s["consumer"]["processing_rate_fps"] = 15
        self.assertEqual(evaluate(s)["overall"], "INCOMPATIBLE")
        self.assertIn("75.00%", next(c["reason"] for c in evaluate(s)["checks"] if c["check"] == "buffer"))

    def test_05_latency_exceeded(self):
        s = baseline()
        s["consumer"]["latency_components"][1]["worst_ms"] = 160
        self.assertEqual(evaluate(s)["overall"], "INCOMPATIBLE")

    def test_06_protocol_mismatch(self):
        s = baseline()
        s["consumer"]["transport"] = "CAN"
        self.assertEqual(evaluate(s)["overall"], "INCOMPATIBLE")

    def test_07_incomplete(self):
        s = baseline()
        del s["consumer"]["buffer_policy"]
        self.assertEqual(evaluate(s)["overall"], "REVIEW")

    def test_08_evidence_review(self):
        evidence = {"config_same": False, "contract_same": True, "scope_same": True,
                    "assumptions_valid": True, "traceability_complete": True}
        self.assertEqual(evidence_applicability(evidence)["decision"], "REVIEW")

    def test_evidence_reuse_candidate(self):
        evidence = {"config_same": True, "contract_same": True, "scope_same": True,
                    "assumptions_valid": True, "traceability_complete": True}
        self.assertEqual(evidence_applicability(evidence)["decision"], "REUSE")

    def test_evidence_reverify(self):
        evidence = {"config_same": True, "contract_same": False, "scope_same": True,
                    "assumptions_valid": True, "traceability_complete": True}
        self.assertEqual(evidence_applicability(evidence)["decision"], "REVERIFY")

    def test_missing_producer(self):
        s = baseline()
        s["producer"] = None
        self.assertEqual(evaluate(s)["overall"], "REVIEW")

    def test_deterministic_reports(self):
        s = baseline()
        self.assertEqual(evaluate(s), evaluate(deepcopy(s)))
        self.assertIn("COMPATIBLE", markdown_report(evaluate(s)))

if __name__ == "__main__":
    unittest.main()
