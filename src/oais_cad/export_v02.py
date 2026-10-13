"""V0.2 DXF + SVG exports with geometric round-trip verification.

Draws wall centerline segments only. Openings are omitted spans, not
architectural door swings or window symbols. No building-code approval.
"""
import hashlib
import json
import math
from pathlib import Path
from xml.etree import ElementTree as ET

from .v02 import IntentError, compile_intent, wall_segments

def _near(a, b, tolerance=1e-6):
    return math.isclose(a, b, rel_tol=0, abs_tol=tolerance)

def export_plan(spec, destination):
    compiled = compile_intent(spec)
    segments = wall_segments(spec)
    if not segments:
        raise IntentError("No drawable wall segments")
    # Check the segmented centerlines account for all opening lengths.
    total = sum(w.length for w in compiled["walls"].values())
    missing = sum(o["width"] for o in compiled["openings"])
    drawn = sum(math.dist(s["start"], s["end"]) for s in segments)
    if not _near(drawn, total - missing):
        raise IntentError("Wall/opening length conservation failed")

    import ezdxf
    doc = ezdxf.new("R2010")
    doc.header["$INSUNITS"] = 4
    doc.layers.new("OAIS_WALL_CENTERLINES")
    model = doc.modelspace()
    for s in segments:
        model.add_line(s["start"], s["end"], dxfattribs={"layer": "OAIS_WALL_CENTERLINES"})

    # Render a standalone SVG using the same geometry, with no embedded scripts.
    coords = [p for s in segments for p in (s["start"], s["end"])]
    minx = min(p[0] for p in coords)
    maxx = max(p[0] for p in coords)
    miny = min(p[1] for p in coords)
    maxy = max(p[1] for p in coords)
    pad = 200.
    width = max(maxx - minx, 1.)
    height = max(maxy - miny, 1.)
    root = ET.Element("svg", {
        "xmlns": "http://www.w3.org/2000/svg",
        "viewBox": f"0 0 {width+2*pad:g} {height+2*pad:g}",
    })
    for s in segments:
        x1,y1 = s["start"]
        x2,y2 = s["end"]
        ET.SubElement(root,"line",{
            "x1":f"{x1-minx+pad:.6f}","y1":f"{maxy-y1+pad:.6f}",
            "x2":f"{x2-minx+pad:.6f}","y2":f"{maxy-y2+pad:.6f}",
            "stroke":"#173f73","stroke-width":"25","stroke-linecap":"butt"
        })
    # Build in memory and validate DXF bytes before committing final outputs.
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        temp = Path(td) / "layout.dxf"
        doc.saveas(temp)
        parsed = ezdxf.readfile(temp)
        entities = list(parsed.modelspace().query("LINE"))
        if len(entities) != len(segments):
            raise IntentError("DXF round-trip entity count mismatch")
        for expected, actual in zip(segments, entities):
            for point, vec in ((expected["start"],actual.dxf.start),
                               (expected["end"],actual.dxf.end)):
                if not (_near(point[0],vec.x) and _near(point[1],vec.y)):
                    raise IntentError("DXF round-trip coordinate mismatch")
            if actual.dxf.layer != "OAIS_WALL_CENTERLINES":
                raise IntentError("DXF layer mismatch")
        dxf_bytes = temp.read_bytes()

    canonical = json.dumps(spec,sort_keys=True,separators=(",",":"),allow_nan=False).encode("utf-8")
    report = {
        "status":"PASS_CENTERLINE_GEOMETRY_ONLY",
        "units":"mm",
        "input_sha256":hashlib.sha256(canonical).hexdigest(),
        "wall_count":len(compiled["walls"]),
        "opening_count":len(compiled["openings"]),
        "segment_count":len(segments),
        "drawn_length_mm":round(drawn,6),
        "excluded_opening_length_mm":round(missing,6),
        "dxf_roundtrip":"PASS",
        "structural_or_code_approval":False,
        "scope":"wall centerlines only; openings represented as gaps"
    }
    output=Path(destination)
    output.mkdir(parents=True,exist_ok=True)
    (output/"layout_v02.dxf").write_bytes(dxf_bytes)
    ET.ElementTree(root).write(output/"preview_v02.svg",encoding="utf-8",xml_declaration=True)
    (output/"report_v02.json").write_text(json.dumps(report,indent=2),encoding="utf-8")
    return report
