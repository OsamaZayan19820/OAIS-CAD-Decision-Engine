# V0.2 candidate — strict wall/opening intent

This feature branch adds a **separate experimental module** with typed walls, openings, strict field checking and centerline segmentation. No structural, building-code, or clash certification is claimed.

Acceptance:
- Reject unknown units, attributes, IDs and unsupported opening types.
- Reject openings beyond wall extents or overlapping on the same wall.
- Deterministically segment wall centerlines around openings.
- Preserve V0.1 behavior on main.

Limitations:
- No wall intersection/3D solids/door swings or full collision detection.
- Wall thickness is recorded but no 2D wall-offset polygon is produced.
- No DXF export for V0.2 entities yet.
- Tests and CI must pass before merge.
