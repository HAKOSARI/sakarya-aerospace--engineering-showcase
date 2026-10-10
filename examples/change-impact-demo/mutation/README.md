# Synthetic camera mutation experiment (draft)

This folder contains a **non-blocking, manually curated** mutation experiment for the synthetic R1–R7 advisory engine. It is based on the code in draft PR #2, not on the default branch.

From the repository root, install pytest and run:

```bash
python -m pip install pytest==8.3.5
python examples/change-impact-demo/mutation/run_mutations.py --output mutation-results.json
```

The runner copies the demo into a fresh temporary directory for each mutant, verifies a green baseline, applies exactly one literal replacement, compiles the mutated module, executes the existing pytest suite, and writes JSON results. Original files are never modified. `mutation-results.json` is **not** committed as evidence until an actual execution is inspected.

Each `mutants/*.json` file defines `id`, `rule`, `file`, `old`, `new`, `desc`, `expected`, and `rationale`. To contribute: select one rule, add a focused mutant file with a unique ID, explain the behavioral defect, run the suite, and report the exact failing test names. A surviving mutant may indicate a test gap, equivalent behavior, or an underspecified requirement; do not silently remove it.

Classification is conservative: `KILLED` requires a test assertion failure; `CRASHED` indicates unexpected exceptions; `ERROR` covers test collection or execution infrastructure errors; `INVALID` includes stale replacements and syntax failures. `SURVIVED` means the test suite passed. The CANARY deliberately triggers an assertion to verify the copied code is exercised. Assertion-based canary success alone does not prove the quality of the other tests.

**Status at integration commit `bec454d`:** [run 38081602639](https://github.com/HAKOSARI/sakarya-aerospace--engineering-showcase/actions/runs/38081602639) killed 11/11 selected core mutants plus canary; no SURVIVED or INVALID reported. This is not exhaustive mutation coverage. Do not claim mutation coverage, qualification, acceptance, airworthiness or certification. All examples are synthetic; no private laboratory files are included. No employment or internship is promised.

## GitHub Actions

The experimental workflow `.github/workflows/mutation-experiment.yml` runs on relevant pull requests and preserves raw JSON/console logs as artifacts even when expected outcomes do not match. It is **not a required branch-protection check**. Review JSON mutants as executable code before approving outside contributions. The workflow uses read-only permissions and no secrets. A red job may indicate a surviving mutant, a crash, or an infrastructure problem; inspect the artifact before drawing conclusions.

## First observed execution

GitHub Actions run [38041864370](https://github.com/HAKOSARI/sakarya-aerospace--engineering-showcase/actions/runs/38041864370) completed with an expected red result: 6 mutants killed (including canary) and 1 survived (`R4_drop_config_hash`). Raw artifact: [mutation-results-raw](https://github.com/HAKOSARI/sakarya-aerospace--engineering-showcase/actions/runs/38041864370/artifacts/11666247060), ZIP SHA-256 `da80dddadfcc75d00f2e60c1d9ed0adf796f415a94872a48cc375887c701d2c8`. A focused R4 test was subsequently added; its effect on mutation results must be verified in a later run. This is not a complete mutation campaign.

## Verified follow-up

After adding the independent missing-config-hash R4 test, [run 38042059836](https://github.com/HAKOSARI/sakarya-aerospace--engineering-showcase/actions/runs/38042059836) completed successfully: **7/7 selected mutants KILLED (including canary), 0 survived**. The artifact is [here](https://github.com/HAKOSARI/sakarya-aerospace--engineering-showcase/actions/runs/38042059836/artifacts/11666432206). See [mutation report](../../../docs/mutation-report.md). This does not imply exhaustive mutation coverage.

## R7 integration evidence

At integration commit `bec454d333370fdb30c8b1cb330dbaeec27aedf7`, [mutation run #9](https://github.com/HAKOSARI/sakarya-aerospace--engineering-showcase/actions/runs/38081602639) completed successfully: all 11 selected R1–R7 core mutants and canary KILLED. Raw artifact ID `11680945329`, SHA-256 `3d766f17a911472fa1fe704d00ca5cf83a4255e856c9d17148227309d65e8064`. Historical R1–R6 results above are retained. R7/R6 ordering mutant is excluded from this selected catalog. See [mutation report](../../../docs/mutation-report.md).
