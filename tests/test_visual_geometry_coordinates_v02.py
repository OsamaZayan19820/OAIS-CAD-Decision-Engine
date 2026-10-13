import json
from pathlib import Path
from xml.etree import ElementTree as ET
import pytest
from oais_cad.visual_review_v02 import render
from oais_cad.opening_solids import solid_strips
from oais_cad.v02 import IntentError

def test_svg_polygon_coordinates_match_geometry():
    source = Path(__file__).resolve().parents[1] / "examples" / "v02_walls.json"
    spec = json.loads(source.read_text())
    expected = [poly for group in solid_strips(spec).values() for poly in group]
    points = [p for poly in expected for p in poly]
    left = min(p[0] for p in points)
    right = max(p[0] for p in points)
    bottom = min(p[1] for p in points)
    top = max(p[1] for p in points)
    scale = min(900 / max(right-left, 1), 350 / max(top-bottom, 1))
    svg = ET.fromstring(render(spec))
    actual = svg.findall("{http://www.w3.org/2000/svg}polygon")
    assert len(actual) == len(expected)
    for poly, node in zip(expected, actual):
        pairs = [tuple(map(float, point.split(","))) for point in node.attrib["points"].split()]
        assert len(pairs) == 4
        for (x,y),(px,py) in zip(poly,pairs):
            assert px == pytest.approx(80+(x-left)*scale,abs=0.001)
            assert py == pytest.approx(300-(y-bottom)*scale,abs=0.001)

def test_invalid_units_rejected():
    with pytest.raises(IntentError):
        render({"units":"meters","walls":[],"openings":[]})
