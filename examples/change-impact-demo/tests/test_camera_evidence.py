"""Tests for the synthetic advisory engine; no real verification claims."""
import json
import re
import sys
from dataclasses import replace
from datetime import date
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "data"))

from camera_evidence import (  # noqa: E402
    ChangeBaseline, Evidence, RequirementCase, RULE_IDS, assess_cases, recommend,
)
from generate_camera_cases import generate, SEED  # noqa: E402


def build(data):
    baseline_data = data["baseline"]
    baseline = ChangeBaseline(
        changed_items=frozenset(baseline_data["changed_items"]),
        interface_version=baseline_data["interface_version"],
        config_hash=baseline_data["config_hash"],
        evaluation_date=date.fromisoformat(baseline_data["evaluation_date"]),
        max_evidence_age_days=baseline_data["max_evidence_age_days"],
    )
    cases = [
        RequirementCase(
            req_id=row["req_id"], dependencies=frozenset(row["dependencies"]),
            requirement_scope=frozenset(row["requirement_scope"]) if row.get("requirement_scope") else None,
            evidence=Evidence(
                evidence_id=row["evidence_id"], test_id=row["test_id"],
                interface_version=row["interface_version"], config_hash=row["config_hash"],
                date=date.fromisoformat(row["date"]) if row["date"] else None,
                result=row["result"], human_approval=row["human_approval"],
                tested_scope=frozenset(row["tested_scope"]) if row.get("tested_scope") else None,
            ),
        )
        for row in data["cases"]
    ]
    return baseline, cases


def test_generator_is_deterministic_and_explicitly_synthetic():
    assert generate(SEED) == generate(SEED)
    assert generate(SEED) != generate(SEED + 1)
    assert generate()["synthetic"] is True
    assert all(row["synthetic"] is True for row in generate()["cases"])


def test_all_scenarios_match_expected_outcomes_and_rule_ids():
    data = generate()
    baseline, cases = build(data)
    recommendations = assess_cases(cases, baseline)
    assert [(r.outcome, r.rule_id) for r in recommendations] == [
        (row["expected_outcome"], row["expected_rule_id"]) for row in data["cases"]
    ]
    assert len(recommendations) == len(cases)
    assert len({r.req_id for r in recommendations}) == len(cases)


def test_no_input_ever_automatically_accepts_even_with_approval_recorded():
    baseline, cases = build(generate())
    for case in cases:
        for approval in (True, False):
            for result in ("PASS", "FAIL", "INCONCLUSIVE"):
                evidence = replace(case.evidence, human_approval=approval, result=result)
                recommendation = recommend(replace(case, evidence=evidence), baseline)
                assert recommendation.accepted is False
                assert recommendation.outcome in ("REUSE", "REVIEW", "REVERIFY")


def test_fail_and_inconclusive_never_reuse():
    baseline, cases = build(generate())
    for result in ("FAIL", "INCONCLUSIVE"):
        for case in cases:
            decision = recommend(replace(case, evidence=replace(case.evidence, result=result)), baseline)
            assert decision.outcome == "REVIEW"
            assert decision.rule_id == "R1"


def test_missing_and_future_dates_route_to_review():
    baseline, cases = build(generate())
    candidate = cases[0]
    for evidence_date in (None, date(2027, 1, 1), date(2020, 1, 1)):
        decision = recommend(replace(candidate, evidence=replace(candidate.evidence, date=evidence_date)), baseline)
        assert decision.outcome == "REVIEW"


def test_document_rule_ids_exist_in_code():
    docs = [
        ROOT / "README.md",
        ROOT.parents[1] / "case-studies" / "01-uav-eo-camera-decision-architecture.md",
    ]
    documented = set()
    for path in docs:
        documented.update(re.findall(r"\bR[1-9][0-9]*\b", path.read_text(encoding="utf-8")))
    assert documented == RULE_IDS


def test_generated_dataset_round_trips_as_json():
    assert json.loads(json.dumps(generate(SEED))) == generate(SEED)


def test_mismatched_interface_or_configuration_never_reuses_evidence():
    """Independent invariant, not driven by expected outcomes in fixture rows."""
    baseline, cases = build(generate())
    for case in cases:
        for field, mismatch in (("interface_version", "IF-OTHER"), ("config_hash", "CFG-OTHER")):
            changed = replace(case.evidence, result="PASS", **{field: mismatch})
            result = recommend(replace(case, evidence=changed), baseline)
            assert result.outcome != "REUSE", (case.req_id, field)


def test_multiple_requirements_get_independent_distinct_dispositions():
    baseline, cases = build(generate())
    decisions = assess_cases([cases[0], cases[1], cases[3]], baseline)
    assert [d.req_id for d in decisions] == ["EO-REQ-001", "EO-REQ-002", "EO-REQ-004"]
    assert [d.outcome for d in decisions] == ["REUSE", "REVERIFY", "REVIEW"]


def test_canonical_json_bytes_are_reproducible():
    import hashlib

    def digest():
        payload = json.dumps(generate(SEED), sort_keys=True, separators=(",", ":")).encode("utf-8")
        return hashlib.sha256(payload).hexdigest()

    assert digest() == digest()
    assert digest() != hashlib.sha256(
        json.dumps(generate(SEED + 1), sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def test_missing_config_hash_requires_review_even_with_other_evidence_valid():
    """R4 must reject missing provenance without relying on scenario-table assertions."""
    baseline, cases = build(generate())
    candidate = cases[0]
    evidence = replace(
        candidate.evidence,
        result="PASS",
        interface_version=baseline.interface_version,
        config_hash=None,
        date=baseline.evaluation_date,
    )
    decision = recommend(
        replace(candidate, dependencies=frozenset(), evidence=evidence),
        baseline,
    )
    assert decision.outcome == "REVIEW"
    assert decision.rule_id == "R4"
    assert decision.accepted is False


BLANK_TEXT = [
    pytest.param(None, id="none"),
    pytest.param("", id="empty"),
    pytest.param("   ", id="spaces"),
    pytest.param("\t\n", id="tabs-newline"),
    pytest.param("\u00a0", id="nonbreaking-space"),
]


@pytest.mark.parametrize("field", ["evidence_id", "test_id", "interface_version", "config_hash"])
@pytest.mark.parametrize("value", BLANK_TEXT)
def test_blank_provenance_requires_review(field, value):
    baseline, cases = build(generate())
    case = replace(cases[0], dependencies=frozenset(),
                   evidence=replace(cases[0].evidence, **{field: value}))
    decision = recommend(case, baseline)
    assert (decision.outcome, decision.rule_id) == ("REVIEW", "R4")
    assert decision.accepted is False


@pytest.mark.parametrize("field", ["interface_version", "config_hash"])
@pytest.mark.parametrize("value", BLANK_TEXT)
def test_blank_target_baseline_requires_review(field, value):
    baseline, cases = build(generate())
    decision = recommend(cases[0], replace(baseline, **{field: value}))
    assert (decision.outcome, decision.rule_id) == ("REVIEW", "R4")
    assert decision.accepted is False


@pytest.mark.parametrize("field", ["interface_version", "config_hash"])
def test_matching_blank_evidence_and_baseline_are_not_reusable(field):
    baseline, cases = build(generate())
    case = replace(cases[0], evidence=replace(cases[0].evidence, **{field: "   "}))
    decision = recommend(case, replace(baseline, **{field: "   "}))
    assert (decision.outcome, decision.rule_id) == ("REVIEW", "R4")
    assert decision.accepted is False


@pytest.mark.parametrize("field", ["interface_version", "config_hash"])
@pytest.mark.parametrize("padded", [False, True], ids=["different", "padded"])
def test_nonblank_mismatch_is_not_normalized_into_a_match(field, padded):
    baseline, cases = build(generate())
    original = getattr(cases[0].evidence, field)
    value = f" {original} " if padded else "KNOWN-DIFFERENT"
    case = replace(cases[0], evidence=replace(cases[0].evidence, **{field: value}))
    decision = recommend(case, baseline)
    assert (decision.outcome, decision.rule_id) == ("REVERIFY", "R3")
    assert decision.accepted is False


@pytest.mark.parametrize("evidence_changes,changed,expected", [
    pytest.param({"result": "FAIL", "evidence_id": "   "}, True, ("REVIEW", "R1"), id="failed-first"),
    pytest.param({"result": "INCONCLUSIVE", "config_hash": ""}, True, ("REVIEW", "R1"), id="inconclusive-first"),
    pytest.param({"interface_version": ""}, True, ("REVERIFY", "R2"), id="changed-dependency-first"),
    pytest.param({"interface_version": "", "config_hash": "KNOWN-DIFFERENT"}, False, ("REVERIFY", "R3"), id="known-config-mismatch"),
    pytest.param({"interface_version": "KNOWN-DIFFERENT", "config_hash": ""}, False, ("REVERIFY", "R3"), id="known-interface-mismatch"),
])
def test_missing_text_preserves_higher_priority_decisions(evidence_changes, changed, expected):
    baseline, cases = build(generate())
    dependency = frozenset({"DEPENDENCY-X"})
    case = replace(cases[0], dependencies=dependency,
                   evidence=replace(cases[0].evidence, **evidence_changes))
    baseline = replace(baseline, changed_items=dependency if changed else frozenset())
    decision = recommend(case, baseline)
    assert (decision.outcome, decision.rule_id) == expected
    assert decision.accepted is False
