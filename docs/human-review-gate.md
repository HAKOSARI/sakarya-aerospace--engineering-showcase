# Human Review Gate

Automated checks can produce useful verification evidence. They do not, by themselves, authorize an engineering decision or a merge.

This showcase therefore separates **evidence generation** from **engineering authority**.

## Review model

A Pull Request can be reviewed using evidence from the four formal verification methods where appropriate:

- **Inspection** — inspect the changed code, documentation, traceability, security boundary and consistency.
- **Analysis** — evaluate assumptions, dependency logic, evidence applicability and whether the proposed engineering reasoning is defensible.
- **Demonstration** — show the proposed capability operating so reviewers can understand the intended behavior.
- **Test** — execute controlled checks against defined expected outcomes.

A review is not a fifth verification method. It is a decision activity that considers the available evidence.

## Example gate

```text
Proposed change
    ↓
Automated checks
    ↓
Evidence available
    ↓
Human review
    ├── Inspection findings
    ├── Analysis findings
    ├── Demonstration evidence (when useful)
    └── Test evidence
    ↓
Decision
    ├── APPROVE
    ├── REQUEST CHANGES
    └── DO NOT MERGE
```

A green CI result means that the configured automated checks passed. It does **not** mean that every engineering assumption is correct, every requirement is covered, or the change is suitable for certification, qualification, airworthiness or operational use.

## Relationship to REUSE / REVIEW / REVERIFY

These concepts belong to different layers:

| Layer | Outcomes |
|---|---|
| Evidence applicability / disposition | REUSE, REVIEW, REVERIFY |
| Formal verification method | Inspection, Analysis, Demonstration, Test |
| Engineering authority | Approve, request changes, reject / do not merge |

Keeping these layers separate makes the reasoning traceable and prevents an automated PASS from being mistaken for engineering approval.
