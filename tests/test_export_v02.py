import json
import pytest
import ezdxf
from xml.etree import ElementTree as ET
from oais_cad.export_v02 import export_plan
from oais_cad.v02 import IntentError

def example():
    return {"units":"mm","walls":[{"id":"W1","start":[0,0],"end":[5000,0],"thickness":200}],"openings":[{"id":"D1","wall_id":"W1","type":"door","offset":1000,"width":900},{"id":"N1","wall_id":"W1","type":"window","offset":3000,"width":1200}]}

def test_export_roundtrip(tmp_path):
    report=export_plan(example(),tmp_path)
    assert report["status"]=="PASS_CENTERLINE_GEOMETRY_ONLY"
    assert report["segment_count"]==3
    assert report["drawn_length_mm"]==2900
    assert report["excluded_opening_length_mm"]==2100
    assert report["structural_or_code_approval"] is False
    dxf=ezdxf.readfile(tmp_path/"layout_v02.dxf")
    assert len(dxf.modelspace().query("LINE"))==3
    assert len(ET.parse(tmp_path/"preview_v02.svg").getroot())==3
    assert json.loads((tmp_path/"report_v02.json").read_text())["input_sha256"]==report["input_sha256"]

def test_invalid_input_creates_no_output(tmp_path):
    spec=example()
    spec["openings"][0]["offset"]=99999
    target=tmp_path/"out"
    with pytest.raises(IntentError):
        export_plan(spec,target)
    assert not target.exists()

def test_repeated_deterministic_report(tmp_path):
    assert export_plan(example(),tmp_path/"a")==export_plan(example(),tmp_path/"b")

def test_no_drawable_wall_rejected(tmp_path):
    spec={"units":"mm","walls":[{"id":"W","start":[0,0],"end":[1000,0],"thickness":100}],"openings":[{"id":"O","wall_id":"W","type":"door","offset":0,"width":1000}]}
    with pytest.raises(IntentError,match="No drawable"):
        export_plan(spec,tmp_path/"out")
