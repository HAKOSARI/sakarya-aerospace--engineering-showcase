# Case Study 02: Multi-System Scope & Evidence Reusability

This example is deliberately small and synthetic. It is not flight-test evidence and it does not claim certification or airworthiness.

## Problem

A past verification result may be valid for a narrower system scope, but it is no longer automatically applicable once the system scope expands.

Example:
- Old evidence was generated for: `EO_CAMERA`
- New configuration includes: `EO_CAMERA`, `IR_CAMERA`, `GIMBAL`
- The old evidence did not exercise the newly introduced subsystem behaviors.

This is a realistic engineering issue: old evidence can still be relevant, but it may no longer be sufficient for the wider scope.

## Rule

The public showcase uses a conservative rule:

- If the tested scope is equal to the current system scope, and the evidence assumptions still match -> REUSE
- If the current scope adds new subsystems not covered by the old evidence -> REVERIFY
- If scope changes are ambiguous or partially covered -> REVIEW

This is intentionally a small rule for a public demonstration. It is not a certification decision.

## Synthetic data model

System scope is represented as a set of system elements.

Example:
- Old evidence scope: `{"EO_CAMERA"}`
- New system scope: `{"EO_CAMERA", "IR_CAMERA", "GIMBAL"}`

The evidence is not reusable without a fresh scope check.

## Proposed decision rule

`R7 — Scope expansion invalidates old evidence`

If `tested_scope != current_scope`, then do not assume evidence still applies. If the added scope introduces new interfaces, timing, or coordination constraints, the correct engineering disposition is `REVERIFY`.

## Example result

- `EO_CAMERA` -> `EO_CAMERA` -> REUSE
- `EO_CAMERA` -> `EO_CAMERA + IR_CAMERA` -> REVERIFY
- `EO_CAMERA + IR_CAMERA` -> `EO_CAMERA + IR_CAMERA` -> REUSE
- Missing or ambiguous scope metadata -> REVIEW

## Scope of this prototype

This directory is intentionally limited to a tiny rule and deterministic synthetic checks. It is not a full multi-sensor model or a flight qualification package.
