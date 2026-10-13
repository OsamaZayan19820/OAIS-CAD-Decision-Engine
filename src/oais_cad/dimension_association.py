"""Conservative candidate matching: proximity is not proof of a dimension."""
import math


class AssociationError(ValueError):
    pass


def _bbox(value):
    if not isinstance(value, (list, tuple)) or len(value) != 4:
        raise AssociationError("bbox must contain four coordinates")
    if any(isinstance(x, bool) or not isinstance(x, (int, float)) or not math.isfinite(x) for x in value):
        raise AssociationError("Invalid bbox coordinate")
    x0, y0, x1, y1 = value
    if x0 > x1 or y0 > y1:
        raise AssociationError("Reversed bbox")
    return value


def associate_label_candidates(labels, vectors, radius=25):
    """Return nearby vector candidates only; never certify leader association."""
    if isinstance(radius, bool) or not isinstance(radius, (int, float)) or not math.isfinite(radius) or radius <= 0:
        raise AssociationError("Invalid search radius")
    result = []
    for label in labels:
        box = _bbox(label["bbox"])
        cx, cy = (box[0]+box[2])/2, (box[1]+box[3])/2
        candidates = []
        for vector in vectors:
            vb = _bbox(vector["bbox"])
            dx = max(vb[0]-cx, 0, cx-vb[2])
            dy = max(vb[1]-cy, 0, cy-vb[3])
            distance = math.hypot(dx, dy)
            if distance <= radius:
                candidates.append({"vector_id": vector["id"], "distance_page_units": round(distance, 4)})
        candidates.sort(key=lambda x: (x["distance_page_units"], x["vector_id"]))
        result.append({"label": label["text"], "label_bbox": list(box),
                       "candidates": candidates, "status": "REVIEW",
                       "association_verified": False, "measured_clearance": None,
                       "reason": "Proximity alone cannot prove dimension leader or CAD semantics"})
    return result
