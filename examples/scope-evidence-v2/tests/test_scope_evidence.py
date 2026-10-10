import unittest

from scope_evidence import (
    EvidenceRecord,
    RequirementRecord,
    SystemConfig,
    assess_against_archive,
    assess_evidence_for_requirement,
    parse_evidence,
    parse_requirements,
)


class ScopeEvidenceTests(unittest.TestCase):
    def test_S01_same_scope_reuse(self):
        evidence = EvidenceRecord(
            evidence_id="EO-SIL-001",
            test_id="T-EO-01",
            requirement_id="REQ-EOIR-01",
            interface_version="EOIR-V1",
            config_hash="cfg-0002",
            date="2026-09-10T00:00:00Z",
            result="PASS",
            human_approval=None,
            tested_scope=frozenset({"EO_CAMERA", "IR_CAMERA"}),
            assumptions=("EO and IR synchronized at frame level",),
        )
        requirement = RequirementRecord(
            requirement_id="REQ-EOIR-01",
            requirement_scope=frozenset({"EO_CAMERA", "IR_CAMERA"}),
            title="EO and IR streams shall be jointly evaluated",
        )
        config = SystemConfig(
            config_id="CFG-02",
            system_scope=frozenset({"EO_CAMERA", "IR_CAMERA"}),
            notes="same scope",
        )
        self.assertEqual(assess_evidence_for_requirement(evidence, requirement, config.system_scope), "REUSE")

    def test_S02_scope_expansion_requires_reverify(self):
        evidence = EvidenceRecord(
            evidence_id="EO-SIL-001",
            test_id="T-EO-01",
            requirement_id="REQ-EOIR-01",
            interface_version="EO-V1",
            config_hash="cfg-0001",
            date="2026-09-01T00:00:00Z",
            result="PASS",
            human_approval=None,
            tested_scope=frozenset({"EO_CAMERA"}),
            assumptions=("EO camera only",),
        )
        requirement = RequirementRecord(
            requirement_id="REQ-EOIR-01",
            requirement_scope=frozenset({"EO_CAMERA", "IR_CAMERA"}),
            title="EO and IR streams shall be jointly evaluated",
        )
        config = SystemConfig(
            config_id="CFG-02",
            system_scope=frozenset({"EO_CAMERA", "IR_CAMERA"}),
            notes="scope expanded",
        )
        self.assertEqual(assess_evidence_for_requirement(evidence, requirement, config.system_scope), "REVERIFY")

    def test_S03_superset_evidence_is_reuse(self):
        evidence = EvidenceRecord(
            evidence_id="EOIR-GIMBAL-SIL-003",
            test_id="T-EOIR-G-01",
            requirement_id="REQ-EOIR-02",
            interface_version="EOIR-G-V1",
            config_hash="cfg-0003",
            date="2026-09-15T00:00:00Z",
            result="PASS",
            human_approval=None,
            tested_scope=frozenset({"EO_CAMERA", "IR_CAMERA", "GIMBAL"}),
            assumptions=("full multi-system path",),
        )
        requirement = RequirementRecord(
            requirement_id="REQ-EOIR-02",
            requirement_scope=frozenset({"EO_CAMERA", "IR_CAMERA"}),
            title="Combined EO/IR system shall maintain coordinated stream evaluation",
        )
        config = SystemConfig(
            config_id="CFG-02",
            system_scope=frozenset({"EO_CAMERA", "IR_CAMERA"}),
            notes="subsystem set smaller than evidence scope",
        )
        self.assertEqual(assess_evidence_for_requirement(evidence, requirement, config.system_scope), "REUSE")

    def test_S04_partial_overlap_not_enough(self):
        evidence = EvidenceRecord(
            evidence_id="EO-SIL-001",
            test_id="T-EO-01",
            requirement_id="REQ-EOIR-01",
            interface_version="EO-V1",
            config_hash="cfg-0001",
            date="2026-09-01T00:00:00Z",
            result="PASS",
            human_approval=None,
            tested_scope=frozenset({"EO_CAMERA"}),
            assumptions=("EO camera only",),
        )
        requirement = RequirementRecord(
            requirement_id="REQ-EOIR-01",
            requirement_scope=frozenset({"EO_CAMERA", "IR_CAMERA"}),
            title="EO and IR streams shall be jointly evaluated",
        )
        config = SystemConfig(
            config_id="CFG-02",
            system_scope=frozenset({"EO_CAMERA", "IR_CAMERA"}),
            notes="partial overlap with different subsystem",
        )
        self.assertEqual(assess_evidence_for_requirement(evidence, requirement, config.system_scope), "REVERIFY")

    def test_S05_missing_scope_is_review(self):
        evidence = EvidenceRecord(
            evidence_id="AMB-001",
            test_id="T-AMB-01",
            requirement_id="REQ-EOIR-01",
            interface_version="EOIR-V1",
            config_hash="cfg-0002",
            date="2026-09-10T00:00:00Z",
            result="PASS",
            human_approval=None,
            tested_scope=frozenset(),
            assumptions=("missing scope metadata",),
        )
        requirement = RequirementRecord(
            requirement_id="REQ-EOIR-01",
            requirement_scope=frozenset({"EO_CAMERA", "IR_CAMERA"}),
            title="EO and IR streams shall be jointly evaluated",
        )
        config = SystemConfig(
            config_id="CFG-04",
            system_scope=frozenset(),
            notes="ambiguous scope",
        )
        self.assertEqual(assess_evidence_for_requirement(evidence, requirement, config.system_scope), "REVIEW")

    def test_S06_failed_evidence_is_review_before_scope_rule(self):
        evidence = EvidenceRecord(
            evidence_id="FAIL-001",
            test_id="T-FAIL-01",
            requirement_id="REQ-EOIR-01",
            interface_version="EOIR-V1",
            config_hash="cfg-0002",
            date="2026-09-10T00:00:00Z",
            result="FAIL",
            human_approval=None,
            tested_scope=frozenset({"EO_CAMERA"}),
            assumptions=("EO camera only",),
        )
        requirement = RequirementRecord(
            requirement_id="REQ-EOIR-01",
            requirement_scope=frozenset({"EO_CAMERA", "IR_CAMERA"}),
            title="EO and IR streams shall be jointly evaluated",
        )
        config = SystemConfig(
            config_id="CFG-02",
            system_scope=frozenset({"EO_CAMERA", "IR_CAMERA"}),
            notes="failed evidence should not be silently reused",
        )
        self.assertEqual(assess_evidence_for_requirement(evidence, requirement, config.system_scope), "REVIEW")

    def test_S07_interface_version_mismatch_is_reverify(self):
        evidence = EvidenceRecord(
            evidence_id="EO-SIL-001",
            test_id="T-EO-01",
            requirement_id="REQ-EOIR-01",
            interface_version="EO-V2",
            config_hash="cfg-0003",
            date="2026-09-10T00:00:00Z",
            result="PASS",
            human_approval=None,
            tested_scope=frozenset({"EO_CAMERA"}),
            assumptions=("EO camera only",),
        )
        requirement = RequirementRecord(
            requirement_id="REQ-EOIR-01",
            requirement_scope=frozenset({"EO_CAMERA", "IR_CAMERA"}),
            title="EO and IR streams shall be jointly evaluated",
        )
        config = SystemConfig(
            config_id="CFG-02",
            system_scope=frozenset({"EO_CAMERA", "IR_CAMERA"}),
            notes="interface version mismatch",
        )
        self.assertEqual(assess_evidence_for_requirement(evidence, requirement, config.system_scope), "REVERIFY")

    def test_S08_proper_scope_for_multiple_requirements(self):
        evidence = EvidenceRecord(
            evidence_id="EO-SIL-001",
            test_id="T-EO-01",
            requirement_id="REQ-EO-01",
            interface_version="EO-V1",
            config_hash="cfg-0001",
            date="2026-09-01T00:00:00Z",
            result="PASS",
            human_approval=None,
            tested_scope=frozenset({"EO_CAMERA"}),
            assumptions=("EO only",),
        )
        req_a = RequirementRecord(
            requirement_id="REQ-EO-01",
            requirement_scope=frozenset({"EO_CAMERA"}),
            title="EO only requirement",
        )
        req_b = RequirementRecord(
            requirement_id="REQ-EOIR-01",
            requirement_scope=frozenset({"EO_CAMERA", "IR_CAMERA"}),
            title="EO and IR requirement",
        )
        same_scope = SystemConfig(
            config_id="CFG-01",
            system_scope=frozenset({"EO_CAMERA"}),
            notes="single sensor",
        )
        expanded = SystemConfig(
            config_id="CFG-02",
            system_scope=frozenset({"EO_CAMERA", "IR_CAMERA"}),
            notes="multi-sensor scope",
        )
        self.assertEqual(assess_evidence_for_requirement(evidence, req_a, same_scope.system_scope), "REUSE")
        self.assertEqual(assess_evidence_for_requirement(evidence, req_b, expanded.system_scope), "REVERIFY")


if __name__ == "__main__":
    unittest.main()
