import pytest
import json
import hashlib
from oais_cad.publish_solids_v02 import publish_solid_plan
from oais_cad.v02 import IntentError

def wall(i,a,b):
    return {"id":i,"start":list(a),"end":list(b),"thickness":200}

def spec(walls):
    return {"units":"mm","walls":walls,"openings":[]}

def test_publish_complete_directory(tmp_path):
    out=tmp_path/"release"
    result=publish_solid_plan(spec([wall("A",(0,0),(1000,0))]),out)
    assert result["dxf_roundtrip"]=="PASS"
    assert {p.name for p in out.iterdir()}=={"wall_solids_v02.dxf","wall_solids_report_v02.json","_OAIS_COMPLETE"}
    assert not list(tmp_path.glob(".oais-stage-*"))

def test_reject_existing_destination_without_overwrite(tmp_path):
    out=tmp_path/"release"
    out.mkdir()
    marker=out/"keep.txt"
    marker.write_text("original")
    with pytest.raises(IntentError,match="exists"):
        publish_solid_plan(spec([wall("A",(0,0),(1000,0))]),out)
    assert marker.read_text()=="original"

def test_failure_leaves_no_partial_release(tmp_path):
    out=tmp_path/"release"
    with pytest.raises(IntentError,match="HOLD"):
        publish_solid_plan(spec([wall("A",(0,0),(1000,0)),wall("B",(500,-300),(500,300))]),out)
    assert not out.exists()
    assert not list(tmp_path.glob(".oais-stage-*"))

def test_completion_marker_matches_report(tmp_path):
    out=tmp_path/"release"
    report=publish_solid_plan(spec([wall("A",(0,0),(1000,0))]),out)
    marker=json.loads((out/"_OAIS_COMPLETE").read_text())
    assert marker["protocol"]==2
    assert marker["dxf_sha256"]==report["dxf_sha256"]
    assert marker["report_sha256"]==hashlib.sha256((out/"wall_solids_report_v02.json").read_bytes()).hexdigest()
