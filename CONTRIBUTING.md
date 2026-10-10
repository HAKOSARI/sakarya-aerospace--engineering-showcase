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

## First contribution — student quick start

You do **not** need to be added as a repository collaborator to contribute. A GitHub account is sufficient.

1. Browse the [roadmap](ROADMAP.md) and [open issues](https://github.com/HAKOSARI/sakarya-aerospace--engineering-showcase/issues). Start with an issue tagged `good first issue`.
2. Leave a short comment on the issue indicating what you would like to try. Ask questions when requirements are unclear.
3. Use **Fork** on GitHub, then clone your fork. Create a separate branch for your change.
4. Make one small improvement: clarify a paragraph, translate terminology, improve a diagram, add a *synthetic* test or describe an onboarding blocker.
5. If you changed Python code, run the relevant documented tests. Include commands/results you actually ran; do not claim CI passed before it runs.
6. Push your branch and open a Pull Request to this repository. Link the issue number and describe what changed, how it was checked and any limitations.
7. Respond to review feedback. Maintainers decide whether and when changes merge.

For readers new to GitHub, you can make a documentation edit using GitHub's web interface on your fork; a Pull Request can be created from that branch without local development tools.

### Try the Python demo (optional)

The simple change-impact example is available on `main` under `examples/change-impact-demo/`. From the repository root, with a working Python 3 installation:

```bash
python -m unittest discover -s examples/change-impact-demo/tests -p 'test_change_impact.py' -v
```

The camera-specific R1–R6 example currently lives in [draft PR #2](https://github.com/HAKOSARI/sakarya-aerospace--engineering-showcase/pull/2), rather than being assumed present on `main`. To work on its tests, select that branch explicitly and follow its README.

### Suggested 30-minute first-contribution workshop

- **0–5 min:** Explain the synthetic demonstration and why PASS is not engineering acceptance.
- **5–10 min:** Open an issue, read scope and expected result, fork the public repository.
- **10–20 min:** Make one small documentation/diagram change or run the simple demo tests.
- **20–27 min:** Open a Pull Request, cite the issue and state what was verified.
- **27–30 min:** Review one PR together and identify follow-up questions.

The workshop is optional and is not a promise of employment, internship, academic credit or endorsement.

### Contribution rights and review

By submitting material, you confirm you have the right to contribute it under this repository's Apache-2.0 license; include attribution for third-party material where required. Do not include confidential, customer, controlled or private-laboratory material.

A DCO `Signed-off-by` policy is **not currently required**. If the maintainers decide to introduce one, the policy and instructions must first be documented and communicated.

CI test success is not engineering approval, qualification or certification. Human review is required for decisions and merges.
