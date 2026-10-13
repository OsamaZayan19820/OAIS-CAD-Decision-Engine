"""Review-only SVG for validated 2D CAD wall strips."""
import json
from pathlib import Path
from xml.etree import ElementTree as ET
from .opening_solids import review_opening_solids
from .v02 import compile_intent, IntentError

def render(spec):
    model = compile_intent(spec)
    result = review_opening_solids(spec)
    polygons = [poly for group in result["strips"].values() for poly in group]
    if not polygons:
        raise IntentError("No drawable wall strips")
    points = [p for poly in polygons for p in poly]
    left = min(p[0] for p in points)
    right = max(p[0] for p in points)
    bottom = min(p[1] for p in points)
    top = max(p[1] for p in points)
    scale = min(900 / max(right-left, 1), 350 / max(top-bottom, 1))
    def mapped(p):
        return (80+(p[0]-left)*scale, 300-(p[1]-bottom)*scale)
    svg = ET.Element("svg", {"xmlns":"http://www.w3.org/2000/svg", "viewBox":"0 0 1100 550"})
    ET.SubElement(svg,"rect",{"width":"1100","height":"550","fill":"#f6f8fb"})
    def label(y,value,color="#18324b"):
        node = ET.SubElement(svg,"text",{"x":"60","y":str(y),"fill":color,"font-family":"sans-serif","font-size":"18"})
        node.text = value
    label(40,"OAIS-CAD / 2D WALL REVIEW")
    label(70,"NOT APPROVED FOR CONSTRUCTION","#a34d14")
    for poly in polygons:
        coords = " ".join("%.3f,%.3f" % mapped(p) for p in poly)
        ET.SubElement(svg,"polygon",{"points":coords,"fill":"#285782","stroke":"#153b60"})
    label(465,"Walls: %d | Openings: %d | Strips: %d" % (len(model["walls"]),len(model["openings"]),len(polygons)))
    label(435,"Opening details: " + "; ".join("%s %s %g mm" % (o["id"],o["type"],o["width"]) for o in model["openings"])[:110])
    status = "HOLD: OVERLAPPING STRIPS" if any(f["severity"]=="HOLD" for f in result["findings"]) else "REVIEW ONLY: NOT AN ENGINEERING APPROVAL"
    label(500,status,"#a34d14")
    return ET.tostring(svg,encoding="unicode")

def export(spec,destination):
    output = Path(destination)
    output.parent.mkdir(parents=True,exist_ok=True)
    output.write_text(render(spec),encoding="utf-8")

if __name__ == "__main__":
    import sys
    if len(sys.argv)!=3:
        sys.exit("usage: python -m oais_cad.visual_review_v02 input.json output.svg")
    export(json.loads(Path(sys.argv[1]).read_text(encoding="utf-8")),sys.argv[2])
