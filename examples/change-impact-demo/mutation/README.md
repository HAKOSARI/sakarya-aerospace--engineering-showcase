# Synthetic camera mutation experiment (draft)

This folder contains a **non-blocking, manual** mutation experiment for the synthetic R1–R6 advisory engine. It is based on the code in draft PR #2, not on the default branch.

From the repository root, install pytest and run:

```bash
python -m pip install pytest==8.3.5
python examples/change-impact-demo/mutation/run_mutations.py --output mutation-results.json
```

The runner copies the demo into a fresh temporary directory for each mutant, verifies a green baseline, applies exactly one literal replacement, compiles the mutated module, executes the existing pytest suite, and writes JSON results. Original files are never modified. `mutation-results.json` is **not** committed as evidence until an actual execution is inspected.

Each `mutants/*.json` file defines `id`, `rule`, `file`, `old`, `new`, `desc`, `expected`, and `rationale`. To contribute: select one rule, add a focused mutant file with a unique ID, explain the behavioral defect, run the suite, and report the exact failing test names. A surviving mutant may indicate a test gap, equivalent behavior, or an underspecified requirement; do not silently remove it.

Classification is conservative: `KILLED` requires a test assertion failure; `CRASHED` indicates unexpected exceptions; `ERROR` covers test collection or execution infrastructure errors; `INVALID` includes stale replacements and syntax failures. `SURVIVED` means the test suite passed. The CANARY deliberately triggers an assertion to verify the copied code is exercised. Assertion-based canary success alone does not prove the quality of the other tests.

**Status:** Catalog and runner prepared. No mutation execution results have yet been verified. Do not claim mutation coverage, qualification, acceptance, airworthiness or certification. All examples are synthetic; no private laboratory files are included. No employment or internship is promised.
