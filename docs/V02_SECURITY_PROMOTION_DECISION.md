# OAIS-CAD v0.2 — Security Promotion Decision Record

Status: **HOLD — draft, non-governing until human approval**
Scope: `feature/v0.2-intent-geometry`; no merge to main, no public release.

## Decision frame
Decide whether the candidate CAD exporter and release-verification pipeline may be promoted beyond the development branch. Evidence must include reproducible CAD regressions, negative security tests, dependency integrity, and independent human authorization.

## Verified evidence
- CI #171: all four jobs passed, including candidate lock generation/install/regression on Python 3.10 and 3.11. https://github.com/OsamaZayan19820/OAIS-CAD-Decision-Engine/actions/runs/38445600406
- CI #173: all four jobs passed; candidate lock artifact upload step succeeded for both Python versions. https://github.com/OsamaZayan19820/OAIS-CAD-Decision-Engine/actions/runs/38445802514
- CI #179: failed after adding a structural lock validator; pytest reported 100 passed, one failed. Both candidate-lock jobs failed because the validator incorrectly rejected valid hash continuation lines. https://github.com/OsamaZayan19820/OAIS-CAD-Decision-Engine/actions/runs/38446013973
- The follow-up parser fix and adversarial regression tests require fresh CI evidence before acceptance.

## Risk and authority gates
1. **Supply chain:** Candidate lock generated at CI runtime; archived evidence is not an approved, committed, stable, per-interpreter lock. Toolchain provenance and independent review remain open.
2. **Tampering:** SHA-256 release marker detects accidental edits but is not authenticated. A malicious actor with write access can replace both payload and marker. No cryptographic signing or trusted publisher identity.
3. **CAD:** Internal DXF/geometry regressions do not substitute for external CAD interoperability and engineering acceptance tests.
4. **CI:** A green historical run does not override a failing later run. Promotion requires the latest relevant commit to pass all jobs.
5. **Human authority:** Maintainer must explicitly approve lock promotion and any merge/release.

## Evidence classification
- FACT: Historical CI #171 and #173 passed; #179 failed.
- FACT: Candidate lock artifacts were uploaded in #173; their contents were not independently inspected in this record.
- ASSUMPTION: Current dependency resolution remains available and consistent.
- DATA_VOID: Independent external CAD validation, cryptographic provenance, final committed lock, independent human approval.

## Decision
**HOLD** for merge/release. **GO** only for isolated branch testing and evidence collection.
Next action: confirm corrected parser and negative tests on both Python versions; inspect archived candidate locks and compare dependency sets; perform independent CAD checks; request human promotion decision.
