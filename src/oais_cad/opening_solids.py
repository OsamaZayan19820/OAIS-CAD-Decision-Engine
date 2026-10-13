"""Conservative rectangular solid strips split by opening intervals.

2D plan footprint is a set of rectangles along each wall centerline.
Openings remove a full-thickness span; no jamb, lintel, door swing or
3D structural validation is implied.
"""
from .v02 import compile_intent
from .solid_geometry import classify_footprints

def solid_strips(spec):
    compiled=compile_intent(spec)
    result={}
    for wid,w in compiled["walls"].items():
        openings=sorted((o["offset"],o["offset"]+o["width"]) for o in compiled["openings"] if o["wall_id"]==wid)
        ux=(w.x2-w.x1)/w.length
        uy=(w.y2-w.y1)/w.length
        nx=-uy*w.thickness/2
        ny=ux*w.thickness/2
        spans=[]
        cursor=0.
        for start,end in openings+[(w.length,w.length)]:
            if start>cursor:
                p=(w.x1+cursor*ux,w.y1+cursor*uy)
                q=(w.x1+start*ux,w.y1+start*uy)
                spans.append([(p[0]+nx,p[1]+ny),(q[0]+nx,q[1]+ny),
                              (q[0]-nx,q[1]-ny),(p[0]-nx,p[1]-ny)])
            cursor=end
        result[wid]=spans
    return result

def review_opening_solids(spec):
    strips=solid_strips(spec)
    ids=list(strips)
    findings=[]
    for i,a in enumerate(ids):
        for b in ids[i+1:]:
            for ai,poly_a in enumerate(strips[a]):
                for bi,poly_b in enumerate(strips[b]):
                    kind=classify_footprints(poly_a,poly_b)
                    if kind!="SEPARATE":
                        findings.append({
                            "walls":[a,b],"strip_indices":[ai,bi],
                            "type":kind,
                            "severity":"HOLD" if kind=="OVERLAP" else "REVIEW",
                            "approved":False
                        })
    return {"strips":strips,"findings":findings}
