# Sakarya Aerospace — Engineering Showcase

[![Showcase CI](https://github.com/HAKOSARI/sakarya-aerospace--engineering-showcase/actions/workflows/showcase-ci.yml/badge.svg)](https://github.com/HAKOSARI/sakarya-aerospace--engineering-showcase/actions/workflows/showcase-ci.yml) [![Synthetic Camera Evidence Tests](https://github.com/HAKOSARI/sakarya-aerospace--engineering-showcase/actions/workflows/camera-evidence-tests.yml/badge.svg)](https://github.com/HAKOSARI/sakarya-aerospace--engineering-showcase/actions/workflows/camera-evidence-tests.yml) [![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)

**Open engineering • Reproducible synthetic evidence • Human-reviewed decisions**

**The problem:** A UAV EO-camera interface changes. Which existing verification evidence may be reused, which needs review, and which must be rerun?

**Try it in 5 minutes:** [Open the no-install R1–R7 browser demo](examples/change-impact-demo/web/index.html) (on GitHub, click **Download raw file** and open it locally; a hosted demo is not yet deployed). Choose a scenario, change a configuration or scope field, then press **Evaluate**. The page is entirely client-side and uses fabricated examples. For an audited executable reference, run the Python tests below.

**Run the reference engine (Python 3.10+):**

```bash
cd examples/change-impact-demo
python data/generate_camera_cases.py
python -m pytest -q tests/test_camera_evidence.py tests/test_scope_evidence.py
```

**First contribution in 30 minutes:** Read [CONTRIBUTING.md](CONTRIBUTING.md), choose a [good first issue](https://github.com/HAKOSARI/sakarya-aerospace--engineering-showcase/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22), and open a small PR with a reproducible change. Start with a documentation clarification or an additional synthetic test.

**Current public baseline:** R1–R7 synthetic EO-camera advisory rules, 34 camera tests, 3 showcase tests and 11 selected mutation checks were verified for [PR #12](https://github.com/HAKOSARI/sakarya-aerospace--engineering-showcase/pull/12) before merge. This is **software verification of invented cases**, not aircraft certification, airworthiness, HIL/flight-test evidence, customer evidence, or engineering acceptance. The browser demo is an educational reimplementation; the Python module is the reference behavior.

---
## Focus

- Systems Engineering
- Requirements & bidirectional traceability
- Interface and dependency reasoning
- Change-impact analysis
- Verification-method selection
- Simulation and Software-in-the-Loop (SIL)
- Evidence provenance and configuration awareness
- Reproducible engineering workflows

## Traceability

A verification result should be reconstructable in both directions:

**Mission Need → Requirement → Method → Environment → Verification Case → Evidence → Result → Engineering Decision**

and

**Engineering Decision → Result → Evidence → Verification Case → Environment → Method → Requirement → Mission Need**

Missing links are engineering information, too: a requirement without a verification case, evidence tied to an obsolete configuration, or a changed interface whose dependent requirements have not been reconsidered.

## Explore the showcase

| Area | What it demonstrates |
|---|---|
| [Verification Intelligence](docs/verification-intelligence.md) | Requirement → method → environment → evidence → decision reasoning |
| [Bidirectional Traceability](docs/traceability-demo.md) | Walking a verification claim forward and backward |
| [Interface Change Impact](docs/interface-change-impact.md) | Why a seemingly small subsystem/interface change can invalidate evidence |
| [Evidence Applicability](docs/evidence-applicability.md) | Provenance, configuration and evidence-reuse reasoning |
| [Mission Computer Latency](examples/mission-computer-latency.md) | Why a quantitative timing requirement needs a precise verification definition |
| [Executable Change-Impact Demo](examples/change-impact-demo/README.md) | Synthetic REUSE / REVIEW / REVERIFY demonstrator with tests |
| [Human Review Gate](docs/human-review-gate.md) | Why automated PASS evidence is not the same as engineering approval |

### Showcase architecture

```mermaid
flowchart LR
    N[Mission / Stakeholder Need] --> R[Requirement]
    R --> I[Interfaces & Dependencies]
    I --> C[Change]
    C --> X[Impact Analysis]
    X --> M[Verification Method]
    M --> V[Verification Case / Environment]
    V --> E[Evidence]
    E --> D[Engineering Decision]
    D -->|trace back| R
```

The executable demo is intentionally small enough to audit by eye. The goal is not to hide engineering judgment behind software; it is to make the reasoning chain visible, reviewable and reproducible.

## Open-source collaboration

This public showcase is licensed under the **Apache License 2.0**. External contributors are welcome to fork the repository, develop changes on their own branches, and propose them back through Pull Requests.

A public contribution never receives automatic access to the private Sakarya Aerospace verification laboratory. Public-to-private transfer is a separate, deliberate engineering decision.

## Public demo philosophy

Examples in this repository are intentionally simplified and use synthetic data. They demonstrate engineering reasoning and workflow design.

They are **not** flight-test evidence, hardware-qualification evidence, certification evidence, customer-program evidence, or a claim of accredited-laboratory status.

Internal R&D artifacts, proprietary source material, customer information, controlled data, credentials, and private program evidence are excluded from this public repository.

## Verification vocabulary

The formal verification methods used here are:

- **Inspection** — examination or review.
- **Analysis** — analytical or mathematical evaluation, including appropriately justified modeling/simulation.
- **Demonstration** — showing a capability or operation without the detailed measurement expected from a formal test.
- **Test** — controlled operation of a product, prototype, or test article to obtain detailed verification data.

SIL, HIL, bench, environmental test and flight test are verification **environments or implementation levels**, not additional formal verification methods.

## Current public demonstrator

**Change → Impact → Verification Decision → Evidence**

The demonstrator is being developed around three advisory outcomes:

- **REUSE** — existing evidence remains applicable with justification.
- **REVIEW** — engineering review is required because applicability is uncertain.
- **REVERIFY** — new verification evidence is required.

These are engineering recommendations for human review, not autonomous certification decisions.

---

**Sakarya Aerospace / SUHAVX**  
Systems Engineering • Verification Intelligence • Simulation • Digital Engineering
