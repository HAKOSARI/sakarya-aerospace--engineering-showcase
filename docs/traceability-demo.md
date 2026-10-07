# Traceability Demo — Follow the Evidence

This public demo explains the core idea behind the Sakarya Aerospace verification-intelligence workflow.

## The detective question

Suppose an engineering report says:

> **PASS**

A systems engineer should be able to ask:

1. Which requirement was closed?
2. Which configuration was evaluated?
3. Which verification method was used?
4. In which environment was it performed?
5. Which procedure or case generated the result?
6. Where is the evidence?
7. Which assumptions and limitations apply?
8. Is that evidence still valid after a system change?

That chain is **traceability**.

## Forward trace

Mission Need  
→ System Requirement  
→ Subsystem / Interface Requirement  
→ Verification Method  
→ Verification Environment  
→ Verification Case  
→ Evidence  
→ Result  
→ Engineering Decision

## Reverse trace

Engineering Decision  
→ Result  
→ Evidence  
→ Verification Case  
→ Verification Environment  
→ Verification Method  
→ Requirement  
→ Mission Need

Traceability is useful because missing links become visible.

Examples:

- a requirement with no verification case,
- a test result with no requirement,
- evidence generated for an obsolete configuration,
- a changed interface whose dependent requirements were not reconsidered.

## Change-impact question

The public demonstrator will eventually answer a bounded question:

> **What changed, what depends on it, and what must be verified again?**

Candidate outputs are REUSE, REVIEW, or REVERIFY. These are engineering recommendations and require human review; they are not autonomous certification decisions.
