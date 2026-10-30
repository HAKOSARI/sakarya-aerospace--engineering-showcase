# Contributing

This repository is a curated public engineering showcase.

Contributions should be technically clear, reproducible where practical, and explicit about assumptions and evidence provenance.

Before proposing a change:

1. Keep examples synthetic or based on clearly public information.
2. Do not include customer, supplier, controlled or proprietary internal data.
3. Distinguish formal verification methods (Inspection, Analysis, Demonstration, Test) from environments such as SIL, HIL, bench or flight.
4. Do not claim certification, qualification, accreditation or flight-worthiness unless the public evidence actually supports that claim.
5. State assumptions, configuration, acceptance criteria and limitations.
6. Add or update tests for executable examples.

Pull Requests are preferred for non-trivial changes so that the reasoning and review history remain visible.

## Your first 30–90 minutes

1. Pick an unassigned [good first issue](https://github.com/HAKOSARI/sakarya-aerospace--engineering-showcase/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22). Comment with your proposed scope before starting.
2. Fork the repository, create a topic branch, and make **one** small, reviewable change.
3. For Python changes, run `python -m pytest -q tests/test_camera_evidence.py tests/test_scope_evidence.py` from `examples/change-impact-demo`. For documentation changes, check links and explain what you changed.
4. Open a PR describing **problem, change, test evidence, and limitations**. A maintainer will review; review timing is not guaranteed.

### Suggested 30-minute workshop

- **0–5 min:** Read the public README Quick Start and distinguish synthetic software evidence from engineering acceptance.
- **5–10 min:** Choose a `good first issue` and fork the repository.
- **10–20 min:** Make one small documentation improvement or add a synthetic test.
- **20–27 min:** Run applicable checks and open a PR with the exact commands and results.
- **27–30 min:** Review the PR description and identify follow-up questions. Maintainer approval is required for merge.

The R1–R7 camera implementation from [PR #2](https://github.com/HAKOSARI/sakarya-aerospace--engineering-showcase/pull/2) is already included on `main` through the integration history; it is not an unmerged draft dependency. Use the current `main` files and tests as the reference baseline.

### Suggested starter tasks

- **30 min:** Improve one confusing R1–R7 term in the README; link to the reference code and explain why.
- **45–60 min:** Add a synthetic boundary-case assertion (e.g. scope, future date) without weakening existing tests.
- **60–90 min:** Improve keyboard accessibility or explanatory copy in the no-install browser demo.

Never paste private laboratory files, real customer datasets, export-controlled material, API tokens, or personal data into public issues or PRs. Contributions are voluntary; no reward, internship, employment, or merge acceptance is promised.
