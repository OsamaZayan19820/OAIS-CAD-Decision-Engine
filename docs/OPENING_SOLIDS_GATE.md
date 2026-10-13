# V0.2 Opening Solid Geometry — candidate gate

Each wall is represented as a union of non-overlapping rectangular strips
between opening intervals. An opening removes its complete width across
the wall thickness in **2D plan only**.

Validation tests include: full-width void, zero openings, diagonal wall area
conservation, clearance within an opening, and unresolved solid overlaps.

This module is a standalone candidate and **is not yet wired into the DXF
exporter**. No automatic junction approval is provided.

Limitations: no door leaf, window frame, lintel, height, jamb, load bearing,
3D topology, construction compliance, or real AutoCAD visual verification.

Promotion requires successful CI for the exact commit, independent review
of opening geometry, and explicit human decision.
