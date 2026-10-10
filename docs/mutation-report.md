# Mutation Experiment Report — Synthetic EO Camera R1–R6

**Scope:** Seven manually selected mutants (including one execution canary), tested against the synthetic advisory decision engine in draft PR #9, stacked on draft PR #2. This is a software test experiment, not aerospace qualification, certification, airworthiness or engineering acceptance.

## Verified GitHub Actions execution

- [Successful mutation workflow run 38042059836](https://github.com/HAKOSARI/sakarya-aerospace--engineering-showcase/actions/runs/38042059836)
- [Raw results artifact 11666432206](https://github.com/HAKOSARI/sakarya-aerospace--engineering-showcase/actions/runs/38042059836/artifacts/11666432206)
- Artifact ZIP SHA-256: `32ff6801e468e446a11f95052b13de7751e875366b291aa6e811dae1281c4fac`
- Commit tested: `9a50d635922e8aec64c91a630fe4337033a77084`
- GitHub Actions job conclusion: **success**. The synthetic camera test workflow and Showcase CI on the same commit also concluded **success**.
- The runner checks a green baseline, equal testcase counts, zero skips, compilation, a JUnit assertion-based kill and an exact canary message.

## Mutant outcomes

| Rule | Mutant | Actual outcome | Assertion failures reported | Notes |
|---|---|---|---:|---|
| Canary | CANARY | KILLED | 7 | Verifies copied decision engine was executed; exact message checked |
| R1 | R1_disable | KILLED | 2 | Failed/inconclusive evidence |
| R2 | R2_disable | KILLED | 2 | Changed dependency |
| R3 | R3_unsafe_reuse | KILLED | 2 | Mismatched interface/config must not be reused |
| R4 | R4_drop_config_hash | KILLED | 1 | Missing config hash; dedicated independent test added |
| R5 | R5_disable | KILLED | 3 | Stale/future evidence |
| R6 | R6_wrong_label | KILLED | 2 | Reuse recommendation label |

**Observed totals: 7 KILLED, 0 SURVIVED, 0 CRASHED/ERROR/INVALID/TIMEOUT** in the selected catalog. Excluding the canary, **6/6 selected rule mutants were killed**. The assertion counts are from the GitHub Actions console; individual test identities and JUnit failure heads are preserved in the JSON artifact, not independently reproduced in this summary.

## Finding and resolution

Earlier [run 38041864370](https://github.com/HAKOSARI/sakarya-aerospace--engineering-showcase/actions/runs/38041864370) produced **6 KILLED and 1 SURVIVED**: `R4_drop_config_hash` was not detected by the original tests. A targeted test, `test_missing_config_hash_requires_review_even_with_other_evidence_valid`, was added. The subsequent verified run killed that mutant with one assertion failure. The surviving mutant was retained as a reproducible regression guard.

## Limits and follow-up

This is **not** an exhaustive mutation score. It depends on the deliberately selected mutants; other logical operators, R5 date boundaries, R1/R2 precedence, rule-ID-only mutations and human-approval mutations remain future student contribution opportunities (Issue #7). One assertion-based killer for R4 is not yet the preferred two independent lines of defense for critical rules. The engine makes advisory REUSE/REVIEW/REVERIFY recommendations only; it never accepts or certifies a real system.

**Review status:** Technical experiment verified; PR #9 remains Draft and unmerged. No private laboratory content was used. Final owner approval and additional student review are still required before any merge.
