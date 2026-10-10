from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import json


@dataclass(frozen=True)
class EvidenceRecord:
    evidence_id: str
    tested_scope: frozenset[str]
    environment: str
    assumptions: tuple[str, ...]
    result: str


@dataclass(frozen=True)
class SystemConfig:
    config_id: str
    system_scope: frozenset[str]
    notes: str


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def parse_evidence(records: list[dict]) -> list[EvidenceRecord]:
    return [
        EvidenceRecord(
            evidence_id=item["evidence_id"],
            tested_scope=frozenset(item["tested_scope"]),
            environment=item["environment"],
            assumptions=tuple(item.get("assumptions", [])),
            result=item["result"],
        )
        for item in records
    ]


def parse_system_configs(entries: list[dict]) -> list[SystemConfig]:
    return [
        SystemConfig(
            config_id=item["config_id"],
            system_scope=frozenset(item["system_scope"]),
            notes=item.get("notes", ""),
        )
        for item in entries
    ]


def assess_scope_reuse(evidence: EvidenceRecord, current_config: SystemConfig) -> str:
    """Return REUSE, REVIEW or REVERIFY based on scope coverage."""
    if not evidence.tested_scope:
        return "REVIEW"

    if evidence.tested_scope == current_config.system_scope:
        return "REUSE"

    if current_config.system_scope.issuperset(evidence.tested_scope):
        added = current_config.system_scope - evidence.tested_scope
        if added:
            return "REVERIFY"
        return "REUSE"

    if current_config.system_scope != evidence.tested_scope:
        return "REVIEW"

    return "REUSE"


def find_matching_evidence(
    evidence_records: list[EvidenceRecord],
    current_config: SystemConfig,
) -> EvidenceRecord | None:
    for record in evidence_records:
        if record.tested_scope == current_config.system_scope:
            return record
    return None


def assess_scope_against_archive(
    evidence_records: list[EvidenceRecord],
    current_config: SystemConfig,
) -> tuple[str, EvidenceRecord | None]:
    """Find the matching evidence record; if not found, the new scope has no direct coverage."""
    matching = find_matching_evidence(evidence_records, current_config)
    if matching is not None:
        return "REUSE", matching

    for record in evidence_records:
        if record.tested_scope.issubset(current_config.system_scope):
            return "REVIEW", record

    return "REVERIFY", None


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    evidence_data = load_json(root / "data" / "evidence_archive.json")
    config_data = load_json(root / "data" / "system_configs.json")

    evidence_records = parse_evidence(evidence_data["evidence_records"])
    configs = parse_system_configs(config_data["system_configs"])

    for config in configs:
        decision, match = assess_scope_against_archive(evidence_records, config)
        print(f"{config.config_id}: {decision} | match={match.evidence_id if match else 'none'}")


if __name__ == "__main__":
    main()
