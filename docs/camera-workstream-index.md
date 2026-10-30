# SUHAVX — Camera & EO/IR Public Navigation

> Public-safe engineering navigation only. The detailed internal workstream is maintained in a separate **private** repository; access to it requires authorization.

## Public engineering references

- **Case Study 01:** synthetic EO-camera evidence applicability and change-impact decisions. Existing camera engine rule order is R1→R2→R3→R4→R5→R6.
- **Case Study 02:** R7 composite-scope comparison is a **design proposal**, not implemented or CI-verified. The proposed rule compares the required subsystem scope to the scope exercised together within a single evidence record. REUSE remains advisory and never automatic acceptance.
- **Mutation experiment:** PR #9 run [#5](https://github.com/HAKOSARI/sakarya-aerospace--engineering-showcase/actions/runs/38042059836) completed successfully for R1–R6 mutation checks only (six core mutants and one canary); this does not verify R7 or a physical camera.
- **Two distinct engines:** the simplified `change_impact.py` demo uses REVIEW for configuration mismatch; the synthetic `camera_evidence.py` engine uses REVERIFY / R3 for a known interface or configuration mismatch.

## Confidentiality boundary

Supplier SDKs, thermal camera model selection, commercial correspondence, actual hardware configuration, private evaluation notes and internal action tracking are **not published here**. Detailed internal tracking is managed in the private Sakarya Aerospace Virtual Verification & Evidence Laboratory repository. Publishing only selected, reviewed, synthetic examples is intentional.

## Verification caution

No actual camera, UAV, bench, HIL, ground or flight validation is asserted by this navigation page. No R7 tests or CI results are claimed. No PR is merged by this documentation update.
