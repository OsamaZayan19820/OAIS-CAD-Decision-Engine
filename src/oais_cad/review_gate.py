"""Independent review gate for centerline wall intersections (pilot)."""
from .v02 import compile_intent, IntentError

EPS=1e-8

def _cross(a,b):
    return a[0]*b[1]-a[1]*b[0]

def _sub(a,b):
    return (a[0]-b[0],a[1]-b[1])

def _point_on_segment(p,a,b):
    ab=_sub(b,a)
    ap=_sub(p,a)
    if abs(_cross(ab,ap))>EPS*max(1.,abs(ab[0])+abs(ab[1])):
        return False
    return min(a[0],b[0])-EPS<=p[0]<=max(a[0],b[0])+EPS and min(a[1],b[1])-EPS<=p[1]<=max(a[1],b[1])+EPS

def intersection_kind(a,b,c,d):
    """Classify centerline intersection: NONE, TOUCH, CROSS, OVERLAP."""
    r=_sub(b,a)
    s=_sub(d,c)
    den=_cross(r,s)
    q=_sub(c,a)
    if abs(den)<=EPS:
        if abs(_cross(q,r))>EPS:
            return "NONE"
        # Collinear: overlap interval on the dominant axis.
        axis=0 if abs(r[0])>=abs(r[1]) else 1
        left=max(min(a[axis],b[axis]),min(c[axis],d[axis]))
        right=min(max(a[axis],b[axis]),max(c[axis],d[axis]))
        if right-left>EPS:
            return "OVERLAP"
        if abs(right-left)<=EPS and (_point_on_segment(c,a,b) or _point_on_segment(d,a,b) or _point_on_segment(a,c,d) or _point_on_segment(b,c,d)):
            return "TOUCH"
        return "NONE"
    t=_cross(q,s)/den
    u=_cross(q,r)/den
    if -EPS<=t<=1+EPS and -EPS<=u<=1+EPS:
        if EPS<t<1-EPS and EPS<u<1-EPS:
            return "CROSS"
        return "TOUCH"
    return "NONE"

def review_intersections(spec):
    compiled=compile_intent(spec)
    walls=list(compiled["walls"].values())
    findings=[]
    for i,a in enumerate(walls):
        for b in walls[i+1:]:
            kind=intersection_kind((a.x1,a.y1),(a.x2,a.y2),(b.x1,b.y1),(b.x2,b.y2))
            if kind!="NONE":
                findings.append({"walls":[a.id,b.id],"type":kind,"severity":"HOLD" if kind in ("CROSS","OVERLAP") else "REVIEW"})
    return findings

def require_no_unsafe_intersections(spec):
    findings=review_intersections(spec)
    if any(f["severity"]=="HOLD" for f in findings):
        raise IntentError("Unresolved crossing or overlapping wall centerlines")
    return findings
