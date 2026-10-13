# Measurement Spine — V0.2 (evidence-based, not an approval score)

## Gates
1. Install: Python package and declared dependencies resolve.
2. Syntax: `python -m compileall -q src tests`.
3. Regression: `python -m pytest -q`.
4. Export smoke: V0.2 CLI writes nonempty DXF/SVG/JSON.
5. Human decision: inspect the draft PR and approve separately; CI cannot authorize design.

## Signals
| Signal | Evidence | Failure response |
|---|---|---|
| Evidence Integrity | CI run tied to exact commit | HOLD if mismatched |
| Claim Discipline | Report says centerline-only | HOLD unsupported certification |
| Context Relevance | Branch scoped to CAD | reject cross-project changes |
| Handoff Completeness | CLI, example, tests, docs | HOLD if missing |
| Decision Readiness | CI + geometry + human review | HOLD before human approval |
| Regression | Tests, syntax and export smoke | HOLD on any failed gate |

## Current limitations
- DXF exports centerlines and opening gaps, not wall solids.
- Solid overlap and junction review modules are independent of export.
- Junction labels are candidates only and never authorize intersections.
- SAT tolerance is fixed and not calibrated against CAD engines.
- Geometry tests are necessary but insufficient for building-code approval.

## Promotion rule
A green CI run permits further evaluation, not merging or release.
Human approval is required for changes to junction policy, geometry tolerances
and any promotion beyond this branch.
