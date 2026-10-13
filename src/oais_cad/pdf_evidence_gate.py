"""Evidence-only PDF geometry normalization. No compliance conclusions."""
import math


class EvidenceError(ValueError):
    pass


def rotate_point(x, y, width, height, rotation):
    """Map unrotated PDF page coordinates to displayed coordinates."""
    values = (x, y, width, height)
    if any(isinstance(v, bool) or not isinstance(v, (int, float)) or not math.isfinite(v) for v in values):
        raise EvidenceError("Non-finite or invalid coordinate")
    if width <= 0 or height <= 0:
        raise EvidenceError("Invalid page dimensions")
    if rotation not in (0, 90, 180, 270):
        raise EvidenceError("Unsupported page rotation")
    if rotation == 0:
        return (x, y)
    if rotation == 90:
        return (height - y, x)
    if rotation == 180:
        return (width - x, height - y)
    return (y, width - x)


def normalize_bbox(bbox, width, height, rotation):
    if not isinstance(bbox, (tuple, list)) or len(bbox) != 4:
        raise EvidenceError("Expected four bbox coordinates")
    x0, y0, x1, y1 = bbox
    if x0 > x1 or y0 > y1:
        raise EvidenceError("Reversed bbox")
    points = [rotate_point(x, y, width, height, rotation)
              for x, y in ((x0, y0), (x1, y0), (x1, y1), (x0, y1))]
    xs, ys = zip(*points)
    result = (min(xs), min(ys), max(xs), max(ys))
    display_width, display_height = (height, width) if rotation in (90, 270) else (width, height)
    within = (result[0] >= 0 and result[1] >= 0 and
              result[2] <= display_width and result[3] <= display_height)
    return {"bbox": result, "inside_display_page": within,
            "dimension_association": "UNVERIFIED", "compliance": "NOT_ASSESSED"}


def reconcile_areas(total, components, tolerance=0.01):
    values = [total, tolerance, *components.values()]
    if any(isinstance(v, bool) or not isinstance(v, (int, float)) or not math.isfinite(v) for v in values):
        raise EvidenceError("Invalid area")
    if total < 0 or tolerance < 0 or any(v < 0 for v in components.values()):
        raise EvidenceError("Negative area")
    gap = round(total - sum(components.values()), 6)
    return {"gap_m2": gap, "status": "REVIEW" if abs(gap) > tolerance else "RECONCILED",
            "cause": "UNKNOWN" if abs(gap) > tolerance else "NONE",
            "engineering_approval": False}
