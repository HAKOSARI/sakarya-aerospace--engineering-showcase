"""Synthetic EO-camera evidence disposition rules.

Educational decision support only. Never issues certification, qualification,
airworthiness, or acceptance decisions. No real flight or customer data.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Literal

Outcome = Literal["REUSE", "REVIEW", "REVERIFY"]
EvidenceResult = Literal["PASS", "FAIL", "INCONCLUSIVE"]


@dataclass(frozen=True)
class Evidence:
    evidence_id: str
    test_id: str
    interface_version: str | None
    config_hash: str | None
    date: date | None
    result: EvidenceResult
    human_approval: bool = False


@dataclass(frozen=True)
class RequirementCase:
    req_id: str
    dependencies: frozenset[str]
    evidence: Evidence


@dataclass(frozen=True)
class ChangeBaseline:
    changed_items: frozenset[str]
    interface_version: str
    config_hash: str
    evaluation_date: date
    max_evidence_age_days: int = 365  # Synthetic policy, NOT an aerospace standard.


@dataclass(frozen=True)
class Recommendation:
    req_id: str
    outcome: Outcome
    rule_id: str
    rationale: str
    human_approval_recorded: bool
    accepted: bool = False  # Never inferred by this advisory engine.


RULE_IDS = frozenset({"R1", "R2", "R3", "R4", "R5", "R6"})


def recommend(case: RequirementCase, baseline: ChangeBaseline) -> Recommendation:
    """Return a provisional per-requirement disposition, never an acceptance.

    Priority:
      R1: failed/inconclusive evidence -> REVIEW and anomaly handling
      R2: known changed dependency -> REVERIFY
      R3: known interface/config mismatch -> REVERIFY
      R4: missing provenance or date -> REVIEW
      R5: stale/future evidence -> REVIEW
      R6: matching PASS evidence -> REUSE candidate (not acceptance)

    A recorded human_approval flag is metadata, not proof of authorized sign-off.
    """
    e = case.evidence
    if e.result != "PASS":
        outcome, rule, why = "REVIEW", "R1", "Failed or inconclusive evidence; investigate anomaly or gap"
    elif case.dependencies & baseline.changed_items:
        outcome, rule, why = "REVERIFY", "R2", "Changed traced requirement dependency"
    elif (e.interface_version is not None and e.interface_version != baseline.interface_version) or (
        e.config_hash is not None and e.config_hash != baseline.config_hash
    ):
        outcome, rule, why = "REVERIFY", "R3", "Evidence interface or configuration differs from target baseline"
    elif not e.evidence_id or not e.test_id or not e.interface_version or not e.config_hash or e.date is None:
        outcome, rule, why = "REVIEW", "R4", "Incomplete evidence identity, version, configuration or date"
    elif e.date > baseline.evaluation_date or (baseline.evaluation_date - e.date).days > baseline.max_evidence_age_days:
        outcome, rule, why = "REVIEW", "R5", "Evidence date outside synthetic applicability window"
    else:
        outcome, rule, why = "REUSE", "R6", "Candidate only: PASS, matching baseline and no traced change"
    return Recommendation(case.req_id, outcome, rule, why, e.human_approval)


def assess_cases(cases: list[RequirementCase], baseline: ChangeBaseline) -> list[Recommendation]:
    """Classify each requirement independently; never aggregate into one verdict."""
    return [recommend(case, baseline) for case in cases]
