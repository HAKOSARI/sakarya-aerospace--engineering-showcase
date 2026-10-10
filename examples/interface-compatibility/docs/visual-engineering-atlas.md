# Visual engineering atlas — synthetic UAV integration

> Conceptual research diagrams, not validated hardware architecture, design assurance, or airworthiness evidence. All arrows are hypotheses to test. Mermaid diagrams render directly in GitHub and remain editable as text.

## 1. Subsystem topology

```mermaid
flowchart TB
  EO["EO / IR payload"] -->|Video + timestamps| MC["Mission computer"]
  MC -->|Control setpoints| G["Gimbal controller"]
  G -->|Pose + status| MC
  MC -->|Telemetry / mission data| DL["Data link"]
  FC["Flight controller"] <-->|State / authorized commands| MC
  P["Power distribution"] -->|Electrical power| EO
  P -->|Electrical power| MC
  P -->|Electrical power| G
  TH["Thermal environment"] -.->|Temperature influence| MC
  TH -.->|Temperature influence| EO
```

## 2. Cross-domain causal chain (research hypothesis)

```mermaid
flowchart LR
  A["Higher sensor workload"] --> B["Compute utilization"]
  B --> C["Power dissipation"]
  C --> D["Junction temperature"]
  D --> E{"Thermal throttling?"}
  E -->|Yes| F["Processing time increases"]
  E -->|No| G["Nominal throughput"]
  F --> H["Queue age / frame drops"]
  H --> I["Stale target state"]
  I --> J["Tracking error risk"]
  J -.->|May drive reconfiguration| A
```

## 3. Evidence coverage and decision graph

```mermaid
flowchart TD
  R["Requirement scope"] --> D["Missing = required minus tested"]
  T["Tested scope"] --> D
  D --> Q{"Missing subsystems?"}
  Q -->|Yes| V["REVERIFY candidate"]
  Q -->|Unknown scope| W["REVIEW"]
  Q -->|No| K["Check contract, config, assumptions, traceability"]
  K -->|Unresolved| W
  K -->|Changed / invalid| V
  K -->|Sufficient| U["REUSE candidate — human review"]
```

## 4. Verification feedback loop

```mermaid
flowchart LR
  M["Synthetic system model"] --> S["Generate cross-domain scenarios"]
  S --> X["Run simulation / checks"]
  X --> F["Observe failures and uncertainty"]
  F --> E["Map to requirements and evidence"]
  E --> P["Prioritize new tests"]
  P --> M
```

## Visual conventions

- Solid arrows: declared or modeled flow, with an explicit edge label.
- Dashed arrows: hypothesized influence, not established causality.
- Decision diamonds: explicit branch conditions.
- Evidence decisions are advisory; no diagram alone proves compatibility.

## Next visualization candidates

Parameter dependency matrix; temporal sequence diagram; configuration/evidence traceability graph; thermal-power-performance envelope; scenario coverage heatmap; counterexample/failure propagation graph. Each should be linked to a test fixture or a clearly labeled research hypothesis.
