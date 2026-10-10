"""Synthetic R7 scope-coverage contract tests; expected values are design targets."""
import sys
from dataclasses import replace
from datetime import timedelta
from itertools import combinations
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "data"))
from camera_evidence import RULE_IDS, assess_cases, recommend  # noqa: E402
from generate_camera_cases import generate  # noqa: E402
from test_camera_evidence import build  # noqa: E402

EO, IR, GIMBAL, LASER = "EO_CAMERA", "IR_CAMERA", "GIMBAL", "LASER_RANGEFINDER"
VOCAB = (EO, IR, GIMBAL, LASER)
def fs(*items):
    return frozenset(items)

BASELINE, GENERATED = build(generate())
TEMPLATE = GENERATED[0]
STALE_DATE = BASELINE.evaluation_date - timedelta(days=BASELINE.max_evidence_age_days + 1)

def make_case(req_scope, tested_scope, req_id="REQ-S", case_overrides=None, **evidence_overrides):
    evidence = replace(TEMPLATE.evidence, tested_scope=tested_scope, **evidence_overrides)
    return replace(TEMPLATE, req_id=req_id, requirement_scope=req_scope,
                   evidence=evidence, **(case_overrides or {}))

def result_of(case):
    rec = recommend(case, BASELINE)
    return rec.outcome, rec.rule_id

SCENARIOS = [
    pytest.param(fs(EO, IR), fs(EO, IR), {}, {}, ("REUSE", "R6"), id="S01"),
    pytest.param(fs(EO, IR), fs(EO), {}, {}, ("REVERIFY", "R7"), id="S02"),
    pytest.param(fs(EO, IR), fs(EO, IR, GIMBAL), {}, {}, ("REUSE", "R6"), id="S03"),
    pytest.param(fs(EO, IR), fs(EO, LASER), {}, {}, ("REVERIFY", "R7"), id="S04"),
    pytest.param(fs(EO, IR), None, {}, {}, ("REVIEW", "R4"), id="S05a"),
    pytest.param(fs(EO, IR), fs(), {}, {}, ("REVIEW", "R4"), id="S05b"),
    pytest.param(fs(EO, IR), fs(EO, "UNKNOWN_SUBSYSTEM"), {}, {}, ("REVIEW", "R4"), id="S05c"),
    pytest.param(fs(), fs(EO), {}, {}, ("REVIEW", "R4"), id="S05d"),
    pytest.param(fs(EO, IR), fs(EO), {"result": "FAIL"}, {}, ("REVIEW", "R1"), id="S06"),
    pytest.param(fs(EO, IR), fs(EO), {"date": STALE_DATE}, {}, ("REVIEW", "R5"), id="S06b"),
    pytest.param(fs(EO, IR), fs(EO), {"interface_version": "ICD-CAM-OTHER"}, {}, ("REVERIFY", "R3"), id="S07"),
    pytest.param(fs(EO, IR), fs(EO), {}, {"dependencies": BASELINE.changed_items}, ("REVERIFY", "R2"), id="S07b"),
]

@pytest.mark.parametrize("req_scope,tested_scope,evidence_overrides,case_overrides,expected", SCENARIOS)
def test_scenario_table(req_scope, tested_scope, evidence_overrides, case_overrides, expected):
    assert result_of(make_case(req_scope, tested_scope, case_overrides=case_overrides, **evidence_overrides)) == expected

S08_CASES = [
    make_case(fs(EO), fs(EO), req_id="REQ-A"),
    make_case(fs(EO, IR), fs(EO), req_id="REQ-B"),
    make_case(fs(EO, IR), None, req_id="REQ-C"),
]
S08_EXPECTED = {"REQ-A": ("REUSE", "R6"), "REQ-B": ("REVERIFY", "R7"), "REQ-C": ("REVIEW", "R4")}

def by_requirement(cases):
    recs = assess_cases(cases, BASELINE)
    return {c.req_id: (r.outcome, r.rule_id) for c, r in zip(cases, recs)}

def test_s08_independent():
    assert by_requirement(S08_CASES) == S08_EXPECTED

def test_s08_order_independent():
    assert by_requirement(list(reversed(S08_CASES))) == S08_EXPECTED
    assert by_requirement(S08_CASES[1:] + S08_CASES[:1]) == S08_EXPECTED

def test_s08_removal_independent():
    for removed in S08_CASES:
        remaining = [c for c in S08_CASES if c is not removed]
        assert by_requirement(remaining) == {k: v for k, v in S08_EXPECTED.items() if k != removed.req_id}

def test_s09_no_union_across_records():
    eo_only = make_case(fs(EO, IR), fs(EO), req_id="REQ-S09", evidence_id="EV-S09-A")
    ir_only = make_case(fs(EO, IR), fs(IR), req_id="REQ-S09", evidence_id="EV-S09-B")
    recs = assess_cases([eo_only, ir_only], BASELINE)
    assert [(r.outcome, r.rule_id) for r in recs] == [("REVERIFY", "R7")] * 2
    joint = make_case(fs(EO, IR), fs(EO, IR), req_id="REQ-S09", evidence_id="EV-S09-C")
    assert result_of(joint) == ("REUSE", "R6")

SUBSETS = [fs(*c) for r in range(1, len(VOCAB) + 1) for c in combinations(VOCAB, r)]

def test_all_225_nonempty_scope_pairs():
    for requirement_scope in SUBSETS:
        for tested_scope in SUBSETS:
            expected = ("REUSE", "R6") if requirement_scope <= tested_scope else ("REVERIFY", "R7")
            assert result_of(make_case(requirement_scope, tested_scope)) == expected

def test_template_is_reuse_candidate():
    assert result_of(TEMPLATE) == ("REUSE", "R6")

def test_r7_registered():
    assert "R7" in RULE_IDS

def test_scope_gap_never_auto_accepted_with_human_approval_recorded():
    case = make_case(fs(EO, IR), fs(EO), human_approval=True)
    rec = recommend(case, BASELINE)
    assert (rec.outcome, rec.rule_id, rec.accepted) == ("REVERIFY", "R7", False)
