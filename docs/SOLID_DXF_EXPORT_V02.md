# V0.2 wall-solid DXF export — isolated candidate

API: `from oais_cad.export_solids_v02 import export_solid_plan`

The new exporter is deliberately separate from the existing centerline CLI.
It writes closed LWPOLYLINE entities on `OAIS_WALL_SOLIDS_2D`,
round-trips the file with ezdxf, checks entity count, vertex coordinates,
closure and layer, and reports SHA-256 hashes.

Positive-area overlaps across walls are HOLD; touching geometry is REVIEW
and remains unapproved. Openings remove a full-thickness 2D span.

**Not certified**: no 3D solids, heights, window sill, lintel, door swings,
union/boolean construction details, building code, or AutoCAD desktop test.

Do not replace the existing centerline export, merge, or promote without
CI and explicit human review.
