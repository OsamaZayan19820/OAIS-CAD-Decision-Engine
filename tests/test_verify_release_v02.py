import json
import pytest
from oais_cad.publish_solids_v02 import publish_solid_plan
from oais_cad.verify_release_v02 import verify_release
from oais_cad.v02 import IntentError

def example():
    return {"units":"mm","walls":[{"id":"A","start":[0,0],"end":[1000,0],"thickness":200}],"openings":[]}

def test_valid_release(tmp_path):
    root=tmp_path/"release"
    publish_solid_plan(example(),root)
    assert verify_release(root)["verified"] is True

def test_missing_marker_rejected(tmp_path):
    root=tmp_path/"release"
    publish_solid_plan(example(),root)
    (root/"_OAIS_COMPLETE").unlink()
    with pytest.raises(IntentError,match="Incomplete"):
        verify_release(root)

def test_corrupted_dxf_rejected(tmp_path):
    root=tmp_path/"release"
    publish_solid_plan(example(),root)
    with (root/"wall_solids_v02.dxf").open("ab") as f:
        f.write(b"corruption")
    with pytest.raises(IntentError,match="checksum"):
        verify_release(root)

def test_tampered_report_rejected(tmp_path):
    root=tmp_path/"release"
    publish_solid_plan(example(),root)
    path=root/"wall_solids_report_v02.json"
    report=json.loads(path.read_text())
    report["architectural_approval"]=True
    path.write_text(json.dumps(report))
    with pytest.raises(IntentError,match="approval"):
        verify_release(root)

def test_unexpected_file_rejected(tmp_path):
    root=tmp_path/"release"
    publish_solid_plan(example(),root)
    (root/"rogue.txt").write_text("x")
    with pytest.raises(IntentError,match="unexpected"):
        verify_release(root)
