# SUHAVX — Camera & EO/IR Public Navigation

> Public-safe synthetic engineering navigation. Private supplier SDKs, correspondence, commercial records, hardware integration evidence and licenses remain in the separate private laboratory.

## Current main baseline (30 October 2026)

- **Case Study 01:** [synthetic camera decision architecture](../case-studies/01-uav-eo-camera-decision-architecture.md).
- **R1–R7 implementation:** [camera_evidence.py](../examples/change-impact-demo/src/camera_evidence.py) implements R1 → R2 → R3 → R4 → R5 → R7 → R6. Scope gaps yield REVERIFY/R7; missing or invalid scope yields REVIEW/R4 when earlier precedence rules do not apply. REUSE/R6 is a candidate only, never automatic acceptance.
- **Case Study 02 scope contract:** [test_scope_evidence.py](../examples/change-impact-demo/tests/test_scope_evidence.py) tests S01–S09 scenarios, including S05 variants, S08 per-requirement independence, S09 prohibition on unioning separate records, and 225 nonempty scope pairs. The historical **11/12 discrepancy** is explained by counting scenario identifiers versus parameterized variants; do not treat this as proof of an external CSV's completeness.
- **Historical mutation run:** [PR #9 run #5](https://github.com/HAKOSARI/sakarya-aerospace--engineering-showcase/actions/runs/38042059836) concerns earlier R1–R6 mutation checks, not R7 or hardware validation. PR #9 was subsequently closed without another merge.
- **Main camera CI:** [Camera Evidence workflow](../.github/workflows/camera-evidence-tests.yml) now runs on relevant main pushes, PR changes and manual dispatch. [Main run 41057216578](https://github.com/HAKOSARI/sakarya-aerospace--engineering-showcase/actions/runs/41057216578) passed on 30 October 2026; [Showcase CI 41057216423](https://github.com/HAKOSARI/sakarya-aerospace--engineering-showcase/actions/runs/41057216423) also passed. These are software checks, not physical camera qualification.
- **Browser demo:** [standalone demo](../examples/change-impact-demo/web/index.html) is present; CI includes Node.js checks, but a real-browser manual interaction/keyboard accessibility test has not been independently recorded here.
- **Two distinct engines:** simplified `change_impact.py` uses REVIEW for configuration mismatch; `camera_evidence.py` uses REVERIFY/R3 for a known interface or configuration mismatch.

## Open verification work

1. Establish a final, versioned Case Study 02 document and compare any external CSV/runner with the implemented scenario matrix before asserting parity.
2. Run a real browser interaction and keyboard-accessibility check; record browser version, execution date, screenshots or logs and any limitations.
3. Keep physical EO/IR integration, radiometry, ARM64 SDK compatibility and supplier license/provenance gates within the private laboratory until independently verified and approved for disclosure.

**Boundary:** No actual camera, UAV, bench, HIL, ground or flight validation is asserted by this page.
