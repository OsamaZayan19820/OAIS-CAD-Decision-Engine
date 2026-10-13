# Solid wall geometry review gate (pilot)

- Wall centerlines become square-ended rectangular 2D footprints.
- Separating Axis Theorem classifies footprint pairs as SEPARATE, TOUCH, OVERLAP.
- OVERLAP = HOLD, even at architecturally legitimate T/L junctions.
- TOUCH = REVIEW; no implicit authorization.
- Openings are **not subtracted** from footprints. A door gap in centerline geometry does not establish a void in the wall solid.
- This module is a separate validation candidate. It is not yet wired to DXF export.
- No structural, code, clearance or AutoCAD certification.

Review order: human-approved junction policy -> openings subtraction specification -> independent geometry regression -> export integration.
