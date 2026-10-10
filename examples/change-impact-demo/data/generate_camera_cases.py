"""Generate reproducible, explicitly SYNTHETIC EO-camera evidence examples."""
from __future__ import annotations

import json
import random
from datetime import date
from pathlib import Path

SEED = 20261010
BASELINE_DATE = "2026-10-10"


def generate(seed: int = SEED) -> dict:
    rng = random.Random(seed)
    cases = [
        ("reuse_candidate", "EO-REQ-001", ["DISPLAY"], "IF-B", "CFG-B", "2026-09-20", "PASS", False, "REUSE", "R6"),
        ("changed_dependency", "EO-REQ-002", ["CAMERA_CODEC"], "IF-B", "CFG-B", "2026-09-20", "PASS", False, "REVERIFY", "R2"),
        ("changed_interface", "EO-REQ-003", ["POWER"], "IF-A", "CFG-B", "2026-09-20", "PASS", False, "REVERIFY", "R3"),
        ("old_evidence", "EO-REQ-004", ["DISPLAY"], "IF-B", "CFG-B", "2024-09-20", "PASS", False, "REVIEW", "R5"),
        ("missing_version", "EO-REQ-005", ["DISPLAY"], None, "CFG-B", "2026-09-20", "PASS", False, "REVIEW", "R4"),
        ("failed_evidence", "EO-REQ-006", ["DISPLAY"], "IF-B", "CFG-B", "2026-09-20", "FAIL", True, "REVIEW", "R1"),
        ("unapproved_candidate", "EO-REQ-007", ["DISPLAY"], "IF-B", "CFG-B", "2026-09-20", "PASS", False, "REUSE", "R6"),
        ("changed_config", "EO-REQ-008", ["DISPLAY"], "IF-B", "CFG-A", "2026-09-20", "PASS", False, "REVERIFY", "R3"),
        ("inconclusive", "EO-REQ-009", ["DISPLAY"], "IF-B", "CFG-B", "2026-09-20", "INCONCLUSIVE", False, "REVIEW", "R1"),
    ]
    records = []
    for index, (name, req_id, dependencies, version, config, recorded, result, approval, expected, rule) in enumerate(cases, 1):
        records.append({
            "scenario": name, "synthetic": True, "req_id": req_id,
            "dependencies": dependencies, "evidence_id": f"SYN-EV-{index:03d}",
            "test_id": f"SYN-TST-{index:03d}", "interface_version": version,
            "config_hash": config, "date": recorded, "result": result,
            "human_approval": approval, "requirement_scope": ["EO_CAMERA"], "tested_scope": ["EO_CAMERA"], "expected_outcome": expected,
            "expected_rule_id": rule, "sample_sequence": rng.randint(1000, 9999),
        })
    return {
        "synthetic": True, "notice": "Educational fabricated data; NOT flight tests, qualification or certification.",
        "seed": seed,
        "baseline": {
            "changed_items": ["CAMERA_CODEC"], "interface_version": "IF-B",
            "config_hash": "CFG-B", "evaluation_date": BASELINE_DATE,
            "max_evidence_age_days": 365,
        },
        "cases": records,
    }


def main() -> None:
    destination = Path(__file__).with_name("camera_cases.synthetic.json")
    destination.write_text(json.dumps(generate(), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"Wrote {destination} (SYNTHETIC, seed={SEED})")


if __name__ == "__main__":
    main()
