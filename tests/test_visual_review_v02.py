import json
from pathlib import Path
from xml.etree import ElementTree
from oais_cad.visual_review_v02 import render
from oais_cad.opening_solids import solid_strips

def test_svg_matches_strips():
    source = Path(__file__).resolve().parents[1] / "examples" / "v02_walls.json"
    spec = json.loads(source.read_text())
    root = ElementTree.fromstring(render(spec))
    polygons = root.findall("{http://www.w3.org/2000/svg}polygon")
    expected = sum(map(len, solid_strips(spec).values()))
    assert len(polygons) == expected == 3
    assert "NOT APPROVED FOR CONSTRUCTION" in render(spec)
