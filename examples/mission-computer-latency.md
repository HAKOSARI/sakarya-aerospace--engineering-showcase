# Synthetic Example — Mission-Computer Latency

> **Public demonstration only. Synthetic data. Not measured hardware evidence.**

## Example requirement

**DEMO-REQ-001**  
The mission computer shall process incoming navigation messages with an average processing latency of no more than 20 ms under the defined demo configuration.

This requirement is intentionally simplified. A real requirement would also define the timing start/end events, message population, sample size, input rate, hardware/software configuration, computational load, clock accuracy, treatment of invalid/dropped messages, and any tail-latency criterion.

## Method reasoning

If a representative or real mission computer is exercised under controlled stimuli and detailed latency measurements are collected, the primary formal verification method can be **Test**.

A synthetic Monte Carlo model that does not exercise the real mission computer is **Analysis**. It may support reasoning about uncertainty or margins, but it is not hardware test evidence.

A simple demonstration that messages are processed does not by itself close a quantitative ≤20 ms requirement.

## Traceability skeleton

Mission Need  
→ DEMO-REQ-001  
→ Test / supporting Analysis  
→ Representative test environment / synthetic simulation environment  
→ Verification case  
→ Measured dataset or synthetic dataset  
→ Statistical result  
→ Engineering decision

## Why this matters

The important output is not merely a number. The important output is a number whose source, configuration, assumptions, method, environment and applicability can be reconstructed.
