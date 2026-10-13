"""Independent DXF vs SVG geometric review for the supported 2D wall strips."""
import json
import math
from pathlib import Path
from xml.etree import ElementTree as ET
from .visual_review_v02 import render
from .opening_solids import solid_strips
from .v02 import compile_intent, IntentError

def verify(spec, dxf_path, tolerance=0.001):
    import ezdxf
    compile_intent(spec)
    strips = [p for group in solid_strips(spec).values() for p in group]
    if not strips:
        raise IntentError("No wall strips")
    doc = ezdxf.readfile(str(dxf_path))
    entities = list(doc.modelspace().query("LWPOLYLINE"))
    if len(entities) != len(strips):
        raise IntentError("DXF wall strip count mismatch")
    for expected, entity in zip(strips, entities):
        if not entity.closed or entity.dxf.layer != "OAIS_WALL_SOLIDS_2D":
            raise IntentError("DXF closure or layer mismatch")
        actual = list(entity.get_points("xy"))
        if len(actual) != 4:
            raise IntentError("DXF vertex count mismatch")
        for (x,y),(u,v) in zip(expected,actual):
            if not math.isclose(x,u,abs_tol=tolerance,rel_tol=0) or not math.isclose(y,v,abs_tol=tolerance,rel_tol=0):
                raise IntentError("DXF geometry mismatch")
    root = ET.fromstring(render(spec))
    polygons = root.findall("{http://www.w3.org/2000/svg}polygon")
    if len(polygons) != len(strips):
        raise IntentError("SVG polygon count mismatch")
    return {"status":"PASS_2D_GEOMETRY_ONLY","strips":len(strips),"dxf":"PASS","svg":"PASS","architectural_approval":False}

def verify_from_files(spec_path,dxf_path):
    spec = json.loads(Path(spec_path).read_text(encoding="utf-8"))
    return verify(spec,dxf_path)
