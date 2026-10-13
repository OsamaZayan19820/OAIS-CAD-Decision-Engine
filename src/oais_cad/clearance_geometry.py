"""Geometric separation of axis-aligned segments, not certified aisle clearance."""
import math


class GeometryGateError(ValueError):
    pass


def _segment(value):
    if not isinstance(value, (tuple, list)) or len(value) != 4:
        raise GeometryGateError("Expected four segment coordinates")
    if any(isinstance(v, bool) or not isinstance(v, (int, float)) or not math.isfinite(v) for v in value):
        raise GeometryGateError("Non-finite or invalid segment")
    return tuple(float(v) for v in value)


def parallel_segment_gap(a, b, tolerance=1e-6):
    """Only axis-aligned, overlapping, distinct segments yield a geometric gap.

    Returned gap is in PDF page units, NOT metres; semantics and scale remain unverified.
    """
    if isinstance(tolerance, bool) or not isinstance(tolerance, (int, float)) or not math.isfinite(tolerance) or tolerance <= 0:
        raise GeometryGateError("Invalid tolerance")
    x1,y1,x2,y2 = _segment(a)
    u1,v1,u2,v2 = _segment(b)
    horizontal_a = abs(y2-y1) <= tolerance and abs(x2-x1) > tolerance
    horizontal_b = abs(v2-v1) <= tolerance and abs(u2-u1) > tolerance
    vertical_a = abs(x2-x1) <= tolerance and abs(y2-y1) > tolerance
    vertical_b = abs(u2-u1) <= tolerance and abs(v2-v1) > tolerance
    if horizontal_a and horizontal_b:
        overlap = min(max(x1,x2),max(u1,u2)) - max(min(x1,x2),min(u1,u2))
        gap = abs(y1-v1)
        orientation = "horizontal"
    elif vertical_a and vertical_b:
        overlap = min(max(y1,y2),max(v1,v2)) - max(min(y1,y2),min(v1,v2))
        gap = abs(x1-u1)
        orientation = "vertical"
    else:
        return {"status":"REVIEW", "reason":"NOT_PARALLEL_AXIS_ALIGNED",
                "gap_page_units":None, "certified_clearance":False}
    if overlap <= tolerance or gap <= tolerance:
        return {"status":"REVIEW", "reason":"NO_POSITIVE_OVERLAP_OR_GAP",
                "gap_page_units":None, "certified_clearance":False}
    return {"status":"GEOMETRIC_CANDIDATE", "orientation":orientation,
            "overlap_page_units":round(overlap,6), "gap_page_units":round(gap,6),
            "scale_verified":False, "semantic_boundaries_verified":False,
            "certified_clearance":False}
