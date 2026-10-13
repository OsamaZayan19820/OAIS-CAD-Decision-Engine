# V0.2 Junction Review Policy — PROVISIONAL

A geometry classifier is **not** an engineering design approval.

The module `junction_policy.py` adds descriptive categories:
- X_CROSSING
- COLLINEAR_OVERLAP
- T_CANDIDATE
- ENDPOINT_JUNCTION
- THICKNESS_ONLY_CONTACT

It preserves the conservative HOLD/REVIEW decision from the wall-solid
checker and never automatically approves T or L joints.

Human design authority must specify permitted junction types, corner
treatment, wall priority, tolerance, and opening interaction before an
authorization gate can be implemented.

DATA VOID: 2D wall union topology, 3D constructability, regulatory checks,
physical clearances, and real AutoCAD round-trip.

Next gate: add adversarial numeric tests and a separately versioned
human-approved junction policy, then connect to export only after review.
