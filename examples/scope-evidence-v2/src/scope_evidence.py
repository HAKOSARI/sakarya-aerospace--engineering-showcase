from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path


VALID_SUBSYSTEMS = {
    "EO_CAMERA",
    "IR_CAMERA",
    "GIMBAL",
    "LASER_RANGEFINDER",
    "MISSION_COMPUTER",
}


@dataclass(frozen=True)
class EvidenceRecord:
    evidence_id: str
    test_id: str
    requirement_id: str
    interface_version: str
    config_hash: str
    date: str
    result: str
    human_approval: dict | None
    tested_scope: frozenset[str]
    assumptions: tuple[str, ...]


@dataclass(frozen=True)
class RequirementRecord:
    requirement_id: str
    requirement_scope: frozenset[str]
    title: str


@dataclass(frozen=True)
class SystemConfig:
    config_id: str
    system_scope: frozenset[str]
    notes: str


def _normalize_scope(values: list[str] | None) -> frozenset[str]:
    if not values:
        return frozenset()
    normalized = []
    for item in values:
        if item not in VALID_SUBSYSTEMS:
            raise ValueError(f"Unknown subsystem in scope: {item}")
        normalized.append(item)
    return frozenset(normalized)


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def parse_evidence(records: list[dict]) -> list[EvidenceRecord]:
    parsed = []
    for item in records:
        parsed.append(
            EvidenceRecord(
                evidence_id=item["evidence_id"],
                test_id=item["test_id"],
                requirement_id=item["requirement_id"],
                interface_version=item["interface_version"],
                config_hash=item["config_hash"],
                date=item["date"],
                result=item["result"],
                human_approval=item.get("human_approval"),
                tested_scope=_normalize_scope(item.get("tested_scope", [])),
                assumptions=tuple(item.get("assumptions", [])),
            )
        )
    return parsed


def parse_requirements(records: list[dict]) -> list[RequirementRecord]:
    parsed = []
    for item in records:
        parsed.append(
            RequirementRecord(
                requirement_id=item["requirement_id"],
                requirement_scope=_normalize_scope(item.get("requirement_scope", [])),
                title=item["title"],
            )
        )
    return parsed


def parse_system_configs(entries: list[dict]) -> list[SystemConfig]:
    parsed = []
    for item in entries:
        parsed.append(
            SystemConfig(
                config_id=item["config_id"],
                system_scope=_normalize_scope(item.get("system_scope", [])),
                notes=item.get("notes", ""),
            )
        )
    return parsed


def _check_scope_evidence_rule(evidence_scope: frozenset[str], current_scope: frozenset[str]) -> str:
    """Conservative scope rule for a public demo."""
    if not evidence_scope:
        return "REVIEW"

    if evidence_scope == current_scope:
        return "REUSE"

    if current_scope.issuperset(evidence_scope):
        added = current_scope - evidence_scope
        if added:
            return "REVERIFY"
        return "REUSE"

    if evidence_scope.intersection(current_scope):
        return "REVERIFY"

    return "REVIEW"


def assess_evidence_for_requirement(
    evidence: EvidenceRecord,
    requirement: RequirementRecord,
    current_scope: frozenset[str],
) -> str:
    """Gate on result validity before scope logic."""
    if evidence.result == "FAIL":
        return "REVIEW"

    if evidence.result == "INCONCLUSIVE":
        return "REVIEW"

    if evidence.human_approval is not None:
        # Approval is a record, not automatic acceptance.
        pass

    if evidence.requirement_id != requirement.requirement_id:
        return "REVIEW"

    if current_scope != requirement.requirement_scope:
        # Requirement expects a specific scope; if current system does not match it, new evidence may be needed.
        return "REVERIFY"

    return _check_scope_evidence_rule(evidence.tested_scope, current_scope)


def find_best_match(
    evidence_records: list[EvidenceRecord],
    requirement: RequirementRecord,
    current_scope: frozenset[str],
) -> EvidenceRecord | None:
    best_match = None
    for record in evidence_records:
        if record.requirement_id != requirement.requirement_id:
            continue
        if record.tested_scope == current_scope:
            return record
        if record.tested_scope.issubset(current_scope):
            if best_match is None:
                best_match = record
    return best_match


def assess_against_archive(
    evidence_records: list[EvidenceRecord],
    requirement: RequirementRecord,
    current_scope: frozenset[str],
) -> tuple[str, EvidenceRecord | None]:
    if not current_scope:
        return "REVIEW", None

    match = find_best_match(evidence_records, requirement, current_scope)
    if match is not None:
        decision = assess_evidence_for_requirement(match, requirement, current_scope)
        return decision, match

    # No direct evidence for this scope at all.
    return "REVERIFY", None


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    evidence_data = load_json(root / "data" / "evidence_archive.json")
    requirement_data = load_json(root / "data" / "requirements.json")
    config_data = load_json(root / "data" / "system_configs.json")

    evidence_records = parse_evidence(evidence_data["evidence_records"])
    requirements = parse_requirements(requirement_data["requirements"])
    configs = parse_system_configs(config_data["system_configs"])

    for config in configs:
        for requirement in requirements:
            decision, match = assess_against_archive(evidence_records, requirement, config.system_scope)
            print(f"{config.config_id} | {requirement.requirement_id} | {decision} | {match.evidence_id if match else 'none'}")


if __name__ == "__main__":
    main()
