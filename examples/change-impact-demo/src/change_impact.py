"""Synthetic change-impact demonstrator.

This module is intentionally simple and transparent. It does not make
certification, qualification, safety, or airworthiness decisions.
"""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Requirement:
    req_id: str
    title: str
    dependencies: frozenset[str]
    evidence_config: str


@dataclass(frozen=True)
class Change:
    change_id: str
    changed_items: frozenset[str]
    new_config: str


@dataclass(frozen=True)
class Decision:
    req_id: str
    outcome: str
    rationale: str


def assess(requirements: list[Requirement], change: Change) -> list[Decision]:
    decisions: list[Decision] = []

    for requirement in requirements:
        touched = sorted(requirement.dependencies & change.changed_items)

        if touched:
            decisions.append(
                Decision(
                    requirement.req_id,
                    "REVERIFY",
                    "Changed traced dependency: " + ", ".join(touched),
                )
            )
        elif requirement.evidence_config != change.new_config:
            decisions.append(
                Decision(
                    requirement.req_id,
                    "REVIEW",
                    (
                        f"Evidence belongs to {requirement.evidence_config}; "
                        f"current configuration is {change.new_config}"
                    ),
                )
            )
        else:
            decisions.append(
                Decision(
                    requirement.req_id,
                    "REUSE",
                    "No traced dependency changed and evidence configuration matches",
                )
            )

    return decisions


def load_requirements(path: Path) -> list[Requirement]:
    with path.open(newline="", encoding="utf-8") as handle:
        rows = csv.DictReader(handle)
        return [
            Requirement(
                req_id=row["req_id"],
                title=row["title"],
                dependencies=frozenset(filter(None, row["dependencies"].split(";"))),
                evidence_config=row["evidence_config"],
            )
            for row in rows
        ]


def load_change(path: Path) -> Change:
    with path.open(newline="", encoding="utf-8") as handle:
        row = next(csv.DictReader(handle))
    return Change(
        change_id=row["change_id"],
        changed_items=frozenset(filter(None, row["changed_items"].split(";"))),
        new_config=row["new_config"],
    )


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    requirements = load_requirements(root / "data" / "requirements.csv")
    change = load_change(root / "data" / "change.csv")

    print(f"Change: {change.change_id} -> {change.new_config}")
    for decision in assess(requirements, change):
        print(f"{decision.req_id}: {decision.outcome} | {decision.rationale}")


if __name__ == "__main__":
    main()
