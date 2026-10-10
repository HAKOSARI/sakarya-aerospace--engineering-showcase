# Change-Impact Demo

This is a deliberately small, synthetic example of configuration-aware verification reasoning.

## Scenario

A system has three demonstration requirements. Existing evidence was produced under different configurations. A navigation interface characteristic changes.

The demo asks:

> Which requirements can keep their existing evidence, which need engineering review, and which require new verification evidence?

Input files:

- `data/requirements.csv` — synthetic requirements and traced dependencies.
- `data/change.csv` — a synthetic configuration change.

Executable:

- `src/change_impact.py`

Tests:

- `tests/test_change_impact.py`

## Decision logic

The public demo uses intentionally conservative, transparent rules:

1. If a requirement directly depends on a changed item → **REVERIFY**.
2. Else if its evidence configuration differs from the new configuration → **REVIEW**.
3. Else → **REUSE** candidate.

Real engineering decisions are more nuanced. They can include interface semantics, safety classification, uncertainty, standard/customer mandates, model fidelity, environmental differences and human technical authority.

## Expected demonstration outcome

For `DEMO-CHG-001`:

- `DEMO-REQ-001` → **REVERIFY**, because it depends on `NAV_MESSAGE_RATE`.
- `DEMO-REQ-002` → **REUSE** candidate, because its traced dependencies are unchanged and its evidence is already tied to `CFG-B`.
- `DEMO-REQ-003` → **REUSE** candidate for the same limited synthetic rule set.

This output is educational engineering workflow evidence only. It is not a certification, qualification or airworthiness determination.

## Two distinct decision engines

This repository contains **two separate synthetic decision models**, with intentionally different configuration-mismatch dispositions:

| Engine | File | Known configuration mismatch |
|---|---|---|
| Original change-impact demo | `src/change_impact.py` | **REVIEW** (its simplified demo policy) |
| EO camera evidence engine (PR #2) | `src/camera_evidence.py` | **REVERIFY / R3** (its camera evidence policy) |

These are not contradictory results from one engine: they are **different policies in different modules**. Case Study 02, *Composite-System Scope Mismatch in Verification Evidence Reuse*, proposes extending the **camera evidence engine**, not changing the original demo. R7 is implemented and synthetically verified on the integration branch; see verified checks below.

## Synthetic EO camera evidence engine (PR #2)

**Implemented in this PR branch (CI status must be checked against the relevant run):** `src/camera_evidence.py` provides provisional per-requirement recommendations; `data/generate_camera_cases.py` generates a deterministic, explicitly synthetic JSON dataset using seed `20261010`; `tests/test_camera_evidence.py` contains pytest tests. The original `src/change_impact.py` remains unchanged.

| Rule | Implemented decision | Status |
|---|---|---|
| R1 | FAIL or INCONCLUSIVE evidence → REVIEW, open investigation | Implemented; tests added |
| R2 | Changed traced dependency → REVERIFY | Implemented; tests added |
| R3 | Known interface or configuration mismatch → REVERIFY | Implemented; tests added |
| R4 | Missing evidence ID, test ID, interface version, config hash or date → REVIEW | Implemented; tests added |
| R5 | Stale or future evidence date → REVIEW | Implemented; tests added |
| R6 | PASS, matching baseline, no traced change and covered scope → REUSE candidate | Implemented; tests added |
| R7 | Required subsystem scope not covered by one evidence record → REVERIFY | Implemented on integration branch; CI verified at bec454d |

R7 is evaluated after R5 and before R6. Scope fields are declared per evidence record, never unioned across records. Missing, empty or unknown scope IDs route to R4 REVIEW. Declared scope is not independently verified test coverage; all recommendations remain advisory. See `tests/test_scope_evidence.py` for synthetic scenario targets.

The 365-day evidence-age window is an **invented educational policy**, not an aviation standard. The `human_approval` flag is recorded but is **not** an authorized sign-off: the advisory engine **never accepts** a requirement. It does not execute engineering tests, validate provenance signatures, verify a real configuration hash, manage anomalies, or grant airworthiness approval.

Run locally from `examples/change-impact-demo`:

```bash
python data/generate_camera_cases.py
python -m pytest -q tests/test_camera_evidence.py tests/test_scope_evidence.py
```

The resulting `data/camera_cases.synthetic.json` is generated data. **Passing pytest means only that synthetic software assertions passed; it does not replace any real test campaign, flight testing, qualification, or certification.** This README does not claim an independently verified PR #2 CI run; consult the relevant GitHub Actions logs for execution evidence.

## Verified integration-branch checks

At commit `bec454d333370fdb30c8b1cb330dbaeec27aedf7`, [Camera Evidence #23](https://github.com/HAKOSARI/sakarya-aerospace--engineering-showcase/actions/runs/38081602625) passed 34 tests, [Showcase CI #45](https://github.com/HAKOSARI/sakarya-aerospace--engineering-showcase/actions/runs/38081602677) passed 3 tests, and [Mutation experiment #9](https://github.com/HAKOSARI/sakarya-aerospace--engineering-showcase/actions/runs/38081602639) killed all 11 selected core R1–R7 mutants plus canary. These are synthetic software checks, not real-world engineering acceptance.
