# Verification Intelligence

Verification is not only a test activity. It is the engineering discipline of connecting a claim to sufficient, applicable evidence.

The public demonstrator in this repository uses the following chain:

```text
Mission Need
  ↓
Requirement
  ↓
Verification Method
  ↓
Verification Environment / Case
  ↓
Evidence
  ↓
Result
  ↓
Engineering Decision
```

The chain must also be traversable in reverse. If someone says **PASS**, an engineer should be able to ask: *Which result? Which evidence? Which case? Which configuration? Which requirement? Which mission need?*

## Formal verification methods

We use four formal method categories:

- **Inspection** — examination, review or observation.
- **Analysis** — mathematical, analytical or model-based evaluation.
- **Demonstration** — showing that a capability or operation works, normally without the detailed measurements expected from a formal test.
- **Test** — controlled operation of a product, prototype or test article to obtain detailed verification data.

SIL, HIL, bench, environmental and flight activities are environments or implementation levels. They are not extra formal method categories.

## Evidence applicability

An old result does not remain valid merely because a file still exists. Applicability depends on what the evidence assumed and which configuration produced it.

A change-impact decision therefore asks:

1. What changed?
2. Which requirements depend on the changed characteristic?
3. Which existing evidence depended on the old characteristic or configuration?
4. Does the existing evidence still cover the requirement?
5. If not, what is the lowest sufficient verification activity that can restore coverage?

## Advisory outcomes

This showcase uses three intentionally simple outcomes:

- **REUSE** — existing evidence appears applicable, with documented justification.
- **REVIEW** — applicability is uncertain and needs engineering review.
- **REVERIFY** — existing evidence no longer covers the affected requirement; new verification evidence is needed.

These are engineering workflow recommendations. They are not certification decisions and do not replace technical authority, customer rules, program requirements or applicable standards.
