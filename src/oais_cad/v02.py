"""V0.2 strict intent contract and wall/opening geometry. Units: mm."""
import math
from dataclasses import dataclass

class IntentError(ValueError):
    pass

def number(v, positive=False):
    if isinstance(v,bool) or not isinstance(v,(int,float)) or not math.isfinite(v) or (positive and v<=0):
        raise IntentError("Invalid numeric dimension")
    if abs(v)>1e7:
        raise IntentError("Dimension outside supported range")
    return float(v)

def exact(obj, fields):
    if not isinstance(obj,dict) or set(obj)!=set(fields):
        raise IntentError(f"Expected fields: {sorted(fields)}")

@dataclass(frozen=True)
class Wall:
    id: str
    x1: float
    y1: float
    x2: float
    y2: float
    thickness: float
    length: float

def compile_intent(spec):
    exact(spec,{"units","walls","openings"})
    if spec["units"]!="mm":
        raise IntentError("Only mm supported")
    if not isinstance(spec["walls"],list) or not isinstance(spec["openings"],list):
        raise IntentError("Expected arrays")
    if len(spec["walls"])>500 or len(spec["openings"])>1000:
        raise IntentError("Entity count exceeded")
    walls={}
    for w in spec["walls"]:
        exact(w,{"id","start","end","thickness"})
        wid=w["id"]
        if not isinstance(wid,str) or not wid or len(wid)>80 or wid in walls:
            raise IntentError("Invalid or duplicate wall ID")
        for p in (w["start"],w["end"]):
            if not isinstance(p,list) or len(p)!=2:
                raise IntentError("Invalid wall coordinate")
        x1,y1=map(number,w["start"])
        x2,y2=map(number,w["end"])
        thickness=number(w["thickness"],True)
        length=math.hypot(x2-x1,y2-y1)
        if length<1 or thickness>length:
            raise IntentError("Degenerate or invalid wall")
        walls[wid]=Wall(wid,x1,y1,x2,y2,thickness,length)
    openings=[]
    intervals={}
    for op in spec["openings"]:
        exact(op,{"id","wall_id","type","offset","width"})
        oid=op["id"]
        if not isinstance(oid,str) or not oid or len(oid)>80 or any(a["id"]==oid for a in openings):
            raise IntentError("Invalid or duplicate opening ID")
        if op["type"] not in ("door","window") or op["wall_id"] not in walls:
            raise IntentError("Unsupported opening or unknown wall")
        wall=walls[op["wall_id"]]
        offset=number(op["offset"])
        width=number(op["width"],True)
        if offset<0 or offset+width>wall.length+1e-8:
            raise IntentError("Opening outside wall")
        group=intervals.setdefault(wall.id,[])
        if any(min(offset+width,b)>max(offset,a)+1e-8 for a,b in group):
            raise IntentError("Overlapping openings")
        group.append((offset,offset+width))
        openings.append({"id":oid,"wall_id":wall.id,"type":op["type"],"offset":offset,"width":width})
    return {"walls":walls,"openings":openings}

def wall_segments(spec):
    compiled=compile_intent(spec)
    segments=[]
    for wid,wall in compiled["walls"].items():
        gaps=sorted((o["offset"],o["offset"]+o["width"]) for o in compiled["openings"] if o["wall_id"]==wid)
        cursor=0.
        for a,b in gaps+[(wall.length,wall.length)]:
            if a>cursor:
                ux=(wall.x2-wall.x1)/wall.length
                uy=(wall.y2-wall.y1)/wall.length
                segments.append({"wall_id":wid,"start":[wall.x1+cursor*ux,wall.y1+cursor*uy],"end":[wall.x1+a*ux,wall.y1+a*uy],"thickness":wall.thickness})
            cursor=b
    return segments
