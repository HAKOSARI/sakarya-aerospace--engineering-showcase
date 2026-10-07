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
