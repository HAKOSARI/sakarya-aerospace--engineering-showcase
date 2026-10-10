"""Tests for the synthetic advisory engine; no real verification claims."""
import json
import re
import sys
from dataclasses import replace
from datetime import date
from pathlib import Path

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
            evidence=Evidence(
                evidence_id=row["evidence_id"], test_id=row["test_id"],
                interface_version=row["interface_version"], config_hash=row["config_hash"],
                date=date.fromisoformat(row["date"]) if row["date"] else None,
                result=row["result"], human_approval=row["human_approval"],
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


def test_committed_fixture_matches_generator():
    path = ROOT / "data" / "camera_cases.synthetic.json"
    assert json.loads(path.read_text(encoding="utf-8")) == generate(SEED)
