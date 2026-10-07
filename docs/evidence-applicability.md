# Evidence Applicability

Evidence is useful only when its provenance and applicability can be reconstructed.

A minimal evidence record should answer:

- **What requirement** was being verified?
- **What method** was used?
- **What article/model/software** produced the evidence?
- **Which configuration/version** was active?
- **What inputs and assumptions** were used?
- **What environment** was used?
- **What acceptance criterion** was applied?
- **What result** was obtained?
- **Who/what generated the record and when?**
- **Can the result be reproduced or independently reviewed?**

## Evidence classes used in this showcase

| Class | Meaning |
|---|---|
| SOURCE | External or program source used as an input |
| DERIVED_ANALYSIS | Calculation/model-derived engineering evidence |
| SYNTHETIC_SIMULATION | Evidence produced from explicitly synthetic inputs |
| SIL | Software-in-the-Loop evidence |
| HIL | Hardware-in-the-Loop evidence |
| BENCH | Controlled bench evidence |
| GROUND | Ground/environmental evidence |
| FLIGHT | Flight evidence |

A class label describes **where evidence came from**. It does not, by itself, prove that the evidence is sufficient for a particular requirement.

## Configuration is part of the evidence

Consider a test report that passed on `CFG-A`. The system is now `CFG-B`.

That report is not automatically invalid, and it is not automatically reusable. The engineer must determine whether the changed characteristics intersect the assumptions, interfaces or dependencies that made the old evidence valid.

This is why configuration-aware traceability is central to the public demonstrator.
