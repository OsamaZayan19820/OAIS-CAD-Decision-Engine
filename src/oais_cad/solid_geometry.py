"""Conservative wall footprints in millimetres; no design approval.

Axis-aligned or diagonal centerlines become rectangular footprints with
square ends. Pairwise positive-area overlaps are HOLD, including legitimate
junctions until a human approves a documented junction policy.
"""
import math
from .v02 import compile_intent, IntentError

def footprint(w):
    dx=w.x2-w.x1
    dy=w.y2-w.y1
    nx=-dy/w.length*w.thickness/2
    ny=dx/w.length*w.thickness/2
    return [(w.x1+nx,w.y1+ny),(w.x2+nx,w.y2+ny),
            (w.x2-nx,w.y2-ny),(w.x1-nx,w.y1-ny)]

def _axes(poly):
    for i in range(len(poly)):
        a,b=poly[i],poly[(i+1)%len(poly)]
        dx,dy=b[0]-a[0],b[1]-a[1]
        length=math.hypot(dx,dy)
        yield (-dy/length,dx/length)

def _project(poly,axis):
    values=[p[0]*axis[0]+p[1]*axis[1] for p in poly]
    return min(values),max(values)

def classify_footprints(a,b,tolerance_mm=1e-7):
    """SAT: OVERLAP / TOUCH / SEPARATE; conservative floating tolerance."""
    if not isinstance(tolerance_mm,(int,float)) or isinstance(tolerance_mm,bool) or not math.isfinite(tolerance_mm) or tolerance_mm<0:
        raise IntentError("Invalid tolerance")
    touch=False
    for axis in list(_axes(a))+list(_axes(b)):
        a0,a1=_project(a,axis)
        b0,b1=_project(b,axis)
        depth=min(a1,b1)-max(a0,b0)
        if depth < -tolerance_mm:
            return "SEPARATE"
        if depth <= tolerance_mm:
            touch=True
    return "TOUCH" if touch else "OVERLAP"

def review_wall_solids(spec):
    walls=list(compile_intent(spec)["walls"].values())
    footprints={w.id:footprint(w) for w in walls}
    findings=[]
    for i,a in enumerate(walls):
        for b in walls[i+1:]:
            kind=classify_footprints(footprints[a.id],footprints[b.id])
            if kind!="SEPARATE":
                findings.append({"walls":[a.id,b.id],"type":kind,
                                 "severity":"HOLD" if kind=="OVERLAP" else "REVIEW"})
    return {"footprints":footprints,"findings":findings}

def require_no_solid_overlap(spec):
    result=review_wall_solids(spec)
    if any(f["severity"]=="HOLD" for f in result["findings"]):
        raise IntentError("Unresolved positive-area wall footprint overlap")
    return result
