import json
import unittest
from pathlib import Path

from scope_evidence import (
    EvidenceRecord,
    SystemConfig,
    assess_scope_against_archive,
    assess_scope_reuse,
    parse_evidence,
    parse_system_configs,
)


class ScopeEvidenceTests(unittest.TestCase):
    def test_same_scope_reuses_old_evidence(self):
        evidence = EvidenceRecord(
            evidence_id="EO-SIL-001",
            tested_scope=frozenset({"EO_CAMERA"}),
            environment="SIL",
            assumptions=("EO camera only",),
            result="PASS",
        )
        config = SystemConfig(
            config_id="CFG-01",
            system_scope=frozenset({"EO_CAMERA"}),
            notes="Single sensor",
        )
        self.assertEqual(assess_scope_reuse(evidence, config), "REUSE")

    def test_expanded_scope_requires_reverify(self):
        evidence = EvidenceRecord(
            evidence_id="EO-SIL-001",
            tested_scope=frozenset({"EO_CAMERA"}),
            environment="SIL",
            assumptions=("EO camera only",),
            result="PASS",
        )
        config = SystemConfig(
            config_id="CFG-02",
            system_scope=frozenset({"EO_CAMERA", "IR_CAMERA"}),
            notes="Expanded scope adds IR camera",
        )
        self.assertEqual(assess_scope_reuse(evidence, config), "REVERIFY")

    def test_direct_match_in_archive_is_reuse(self):
        evidence_records = parse_evidence([
            {
                "evidence_id": "EOIR-SIL-002",
                "tested_scope": ["EO_CAMERA", "IR_CAMERA"],
                "environment": "SIL",
                "assumptions": ["EO and IR synchronized"],
                "result": "PASS",
            }
        ])
        config = SystemConfig(
            config_id="CFG-02",
            system_scope=frozenset({"EO_CAMERA", "IR_CAMERA"}),
            notes="Scope matches archived evidence",
        )
        decision, match = assess_scope_against_archive(evidence_records, config)
        self.assertEqual(decision, "REUSE")
        self.assertEqual(match.evidence_id, "EOIR-SIL-002")

    def test_unknown_scope_requires_reverify(self):
        evidence_records = parse_evidence([
            {
                "evidence_id": "EO-SIL-001",
                "tested_scope": ["EO_CAMERA"],
                "environment": "SIL",
                "assumptions": ["EO camera only"],
                "result": "PASS",
            }
        ])
        config = SystemConfig(
            config_id="CFG-03",
            system_scope=frozenset({"EO_CAMERA", "IR_CAMERA", "GIMBAL"}),
            notes="Scope expansion beyond archived evidence",
        )
        decision, match = assess_scope_against_archive(evidence_records, config)
        self.assertEqual(decision, "REVERIFY")
        self.assertIsNone(match)

    def test_incomplete_scope_requests_human_review(self):
        evidence = EvidenceRecord(
            evidence_id="AMB-001",
            tested_scope=frozenset(),
            environment="SIL",
            assumptions=(),
            result="PASS",
        )
        config = SystemConfig(
            config_id="CFG-04",
            system_scope=frozenset(),
            notes="No scope metadata",
        )
        self.assertEqual(assess_scope_reuse(evidence, config), "REVIEW")


if __name__ == "__main__":
    unittest.main()
