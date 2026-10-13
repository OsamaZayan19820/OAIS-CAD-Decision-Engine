"""Review-only classification of wall junction candidates.

This module never authorizes intersections or overrides the solid geometry
HOLD gate. A geometrical junction candidate is not design approval.
"""
import math
from .v02 import compile_intent
from .solid_geometry import review_wall_solids
from .review_gate import intersection_kind

def classify_junctions(spec):
    compiled=compile_intent(spec)
    walls=list(compiled["walls"].values())
    solid=review_wall_solids(spec)
    classifications=[]
    for f in solid["findings"]:
        a=compiled["walls"][f["walls"][0]]
        b=compiled["walls"][f["walls"][1]]
        axis_kind=intersection_kind((a.x1,a.y1),(a.x2,a.y2),
                                    (b.x1,b.y1),(b.x2,b.y2))
        if axis_kind=="CROSS":
            candidate="X_CROSSING"
        elif axis_kind=="OVERLAP":
            candidate="COLLINEAR_OVERLAP"
        elif axis_kind=="TOUCH":
            ends_a=((a.x1,a.y1),(a.x2,a.y2))
            ends_b=((b.x1,b.y1),(b.x2,b.y2))
            # Determine whether the touching endpoint of either line lies
            # strictly within the other line segment.
            def interior(p,w):
                vx=w.x2-w.x1; vy=w.y2-w.y1
                t=((p[0]-w.x1)*vx+(p[1]-w.y1)*vy)/(w.length*w.length)
                cross=(p[0]-w.x1)*vy-(p[1]-w.y1)*vx
                return 1e-8<t<1-1e-8 and abs(cross)<=1e-8*max(1,w.length)
            candidate="T_CANDIDATE" if any(interior(p,b) for p in ends_a) or any(interior(p,a) for p in ends_b) else "ENDPOINT_JUNCTION"
        else:
            candidate="THICKNESS_ONLY_CONTACT"
        classifications.append({
            "walls":f["walls"],"solid_type":f["type"],
            "centerline_type":axis_kind,"candidate":candidate,
            "decision":"HOLD" if f["severity"]=="HOLD" else "REVIEW",
            "approved":False
        })
    return classifications
