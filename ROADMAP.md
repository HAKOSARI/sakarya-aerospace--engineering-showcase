# Public Engineering Showcase — Roadmap

**Status:** Community-facing proposals and demonstrators, not an approved aerospace verification programme.

## Mission

Make evidence-based systems engineering decisions explainable and reviewable: **change → affected requirements → verification method → evidence provenance → REUSE / REVIEW / REVERIFY recommendation → human engineering review**.

A PASS result is not automatic acceptance. All public examples use synthetic data and do not establish flight qualification, certification or airworthiness.

## Available today

- Public systems-engineering explanations and traceability walkthroughs.
- Small executable navigation-interface change-impact demonstrator.
- Synthetic UAV EO-camera interface case, R1–R6 advisory engine, nine seeded scenarios and automated tests **under review in [draft PR #2](../../pull/2)**. Until PR #2 merges, these files may only be present on its development branch; do not assume they are on `main`.

## Ways to contribute

| Entry point | Work | Issue |
| --- | --- | --- |
| Beginner | Translate / improve documentation and technical terminology | [#3](../../issues/3) |
| Beginner | Create or generate an inspectable rule-flow diagram | [#4](../../issues/4) |
| Intermediate | Propose a second synthetic subsystem case (data link or mission computer) | [#5](../../issues/5) |
| Intermediate / advanced | Specify and test candidate R7+ decision rules | [#6](../../issues/6) |
| Advanced | Automate isolated R1–R6 mutation experiments and clean reruns | [#7](../../issues/7) |

## Suggested phases

1. **Onboarding and review:** improve contributor guidance, terminology and diagrams; collect technical feedback.
2. **Evidence quality:** complete independent mutation tests and improve invariant coverage before broadening the rule set.
3. **Synthetic breadth:** review a new data-link or mission-computer interface case; keep scope and assumptions explicit.
4. **Community validation:** review external issues/PRs, improve reproducibility, and publish what was tested and what remains conceptual.

These are directions, **not delivery commitments**. No R7+ implementation, new subsystem qualification, real flight testing or accredited verification is claimed.

## Contribution process

1. Read [CONTRIBUTING.md](CONTRIBUTING.md) and select an open issue; comment with your proposed scope.
2. Fork the public repository, create a branch, and make one focused change.
3. Include synthetic examples, tests and limitations where relevant.
4. Open a Pull Request referencing the issue; maintainers review before merging.

Do **not** include private laboratory files, customer/supplier proprietary information, controlled data or credentials. The private verification laboratory is not part of this community workspace.

## Licensing and provenance

Public code is Apache-2.0 licensed. Contributors must have rights to submit their work; third-party content needs compatible licensing and attribution. A possible DCO / `Signed-off-by` requirement is **under consideration, not currently mandatory**; repository owners should decide and document the policy before enforcement.

**Success measure:** meaningful outside feedback, the first reviewed external issue and the first well-scoped external PR — not just stars.
