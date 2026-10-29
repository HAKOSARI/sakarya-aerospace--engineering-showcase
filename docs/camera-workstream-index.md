# SUHAVX — Camera & EO/IR Workstream Index

> **Status:** Navigation and handover record, not evidence of completed engineering verification. Public-safe summary only. No proprietary supplier SDKs, commercial terms, flight data or private-lab contents are included.

## Workstream ownership and boundaries

| Track | Location / reference | Verified state | Next action |
|---|---|---|---|
| Synthetic EO-camera evidence decision engine (R1–R6) | `examples/change-impact-demo/src/camera_evidence.py` on Case Study 01 branch / this branch | Implemented: `recommend()` R1→R2→R3→R4→R5→R6, `assess_cases()` per-requirement. No scope fields or R7 | Preserve baseline behavior; verify tests on exact branch/SHA |
| Demo change-impact engine | `examples/change-impact-demo/src/change_impact.py` | Separate simplified policy: configuration mismatch REVIEW, unlike camera engine R3 REVERIFY | Keep distinct; do not silently unify semantics |
| Case Study 01 | `case-studies/01-uav-eo-camera-decision-architecture.md` | Synthetic documentation and design | Keep as reference for R1–R6 |
| R1–R6 mutation experiment | Draft PR #9, branch `test/mutation-catalog-r1-r6` | GitHub Actions run #5, run ID `38042059836`, head `9a50d635922e8aec64c91a630fe4337033a77084`: mutation job success; 6 core mutants and canary KILLED; raw artifact `11666432206` | Preserve run/log/artifact links. Does **not** verify R7 or other branches |
| Case Study 02 scope coverage (R7) | This branch `case-study/composite-scope-evidence` | **Design only**. Proposed R7 after R5 before R6; missing required scope → REVERIFY/R7; absent/invalid scope → REVIEW/R4 for scope-aware evaluations | Review final design doc, commit it, implement and execute tests before PR |
| Case Study 02 scenario matrix | S01–S07, S08-A/B/C, S09 | 11 IDs in reviewed design. A separately reported CSV has 12 rows; extra ID not reconciled. No verified behavioral execution | Reconcile IDs; assert both outcome and rule ID; add permutation/removal and per-record tests |
| Supplier thermal camera evaluation | **Private supplier/engineering workspace only** | Reported USB/UVC/CVBS/MIPI options, radiometry/ARM64 SDK questions, model identity and integration uncertainty. Claims not independently hardware-tested | Confirm exact camera model, ARM64 library, pixel formats, temperature API, licensing and test evidence |
| EO/IR hardware integration | **Private engineering workspace only** | Planning / supplier diligence; not a validated physical integration | Keep actual hardware data, binaries, credentials and supplier communications private |

## Case Study 02 design targets (not passing tests)

| ID | Condition | Expected outcome | Rule |
|---|---|---|---|
| S01 | Equal requirement/tested scope | REUSE candidate | R6 |
| S02 | Required EO+IR; tested EO only | REVERIFY | R7 |
| S03 | Tested scope is a superset | REUSE candidate | R6 |
| S04 | Scopes partially overlap | REVERIFY | R7 |
| S05 | Tested scope missing or empty | REVIEW | R4 |
| S06 | FAIL evidence, scope gap | REVIEW | R1 |
| S07 | Interface mismatch, scope gap | REVERIFY | R3 |
| S08-A | Requirement A: covered | REUSE candidate | R6 |
| S08-B | Requirement B: scope gap | REVERIFY | R7 |
| S08-C | Requirement C: missing scope | REVIEW | R4 |
| S09 | Separate EO-only and IR-only evidence records | REVERIFY for each record | R7 |

Synthetic subsystem identifiers are illustrative, not actual hardware configuration values. S08 checks results per requirement under one shared baseline, including order permutation and removal invariance. S09 prohibits union of scopes across separate evidence records.

## Design/implementation gate

1. Record legacy R1–R6 outputs on the same code version.
2. Specify a scope-aware input mode so legacy records are not silently reinterpreted.
3. Validate scope values; missing/empty/invalid scope → R4 when earlier rules do not apply.
4. For valid scopes, compute `set(requirement_scope) - set(tested_scope)`. If nonempty → R7; otherwise R6 may return REUSE candidate.
5. Under proposed order R1→R2→R3→R4→R5→R7→R6, if R2 and R7 conditions both hold, returned rule ID is R2. Secondary reasons are out of scope.
6. Require traceable tests for each scenario, checking `outcome` **and** `rule_id`, plus S08/S09 invariants, legacy regression, mutation tests and actual CI logs.
7. No automatic acceptance or certification, and no PR merge without explicit owner approval.

## Verified references

- [PR #9 mutation workflow run #5](https://github.com/HAKOSARI/sakarya-aerospace--engineering-showcase/actions/runs/38042059836)
- [PR #9 raw mutation artifact](https://github.com/HAKOSARI/sakarya-aerospace--engineering-showcase/actions/runs/38042059836/artifacts/11666432206)
- [PR #2 README clarification commit](https://github.com/HAKOSARI/sakarya-aerospace--engineering-showcase/commit/760a822aa73e62ad128d5805438a2b5f50643aac)

## Chat consolidation / archival rule

This index is the **public navigation record**, not a substitute for private supplier records or raw test artifacts. Before deleting any ChatGPT conversation, confirm its unique decisions, files and references have been transferred and verified. Chat deletion is a separate user-controlled action; no chat has been deleted by this commit.
