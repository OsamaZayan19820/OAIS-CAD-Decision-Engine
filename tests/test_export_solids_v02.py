import json
import hashlib
import pytest
from oais_cad.export_solids_v02 import export_solid_plan
from oais_cad.v02 import IntentError

def wall(i,a,b,t=200):
    return {"id":i,"start":list(a),"end":list(b),"thickness":t}

def spec(walls,openings=None):
    return {"units":"mm","walls":walls,"openings":openings or []}

def test_export_and_hashes(tmp_path):
    s=spec([wall("A",(0,0),(5000,0))],[{"id":"D","wall_id":"A","type":"door","offset":1000,"width":900}])
    report=export_solid_plan(s,tmp_path)
    data=(tmp_path/"wall_solids_v02.dxf").read_bytes()
    assert report["strip_count"]==2
    assert report["dxf_sha256"]==hashlib.sha256(data).hexdigest()
    assert json.loads((tmp_path/"wall_solids_report_v02.json").read_text())==report
    assert report["architectural_approval"] is False

def test_overlap_fail_closed_without_files(tmp_path):
    s=spec([wall("A",(0,0),(1000,0)),wall("B",(500,-200),(500,200))])
    with pytest.raises(IntentError,match="HOLD"):
        export_solid_plan(s,tmp_path)
    assert not (tmp_path/"wall_solids_v02.dxf").exists()

def test_no_drawable_solids_rejected(tmp_path):
    s=spec([wall("A",(0,0),(1000,0))],[{"id":"D","wall_id":"A","type":"door","offset":0,"width":1000}])
    with pytest.raises(IntentError,match="No drawable"):
        export_solid_plan(s,tmp_path)
