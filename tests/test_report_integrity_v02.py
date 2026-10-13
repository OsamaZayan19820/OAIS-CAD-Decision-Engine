"""The completion marker must bind the report as well as the DXF."""
import json
import pytest
from oais_cad.publish_solids_v02 import publish_solid_plan
from oais_cad.verify_release_v02 import verify_release
from oais_cad.v02 import IntentError

SPEC={"units":"mm","walls":[{"id":"A","start":[0,0],"end":[1000,0],"thickness":200}],"openings":[]}

def test_report_tampering_is_rejected(tmp_path):
    release=tmp_path/"release"
    publish_solid_plan(SPEC,release)
    assert verify_release(release)["verified"] is True
    report_path=release/"wall_solids_report_v02.json"
    report=json.loads(report_path.read_text())
    report["input_sha256"]="0"*64
    report_path.write_text(json.dumps(report))
    with pytest.raises(IntentError,match="checksum"):
        verify_release(release)

def test_old_unbound_marker_is_rejected(tmp_path):
    release=tmp_path/"release"
    report=publish_solid_plan(SPEC,release)
    (release/"_OAIS_COMPLETE").write_text(report["dxf_sha256"])
    with pytest.raises(IntentError):
        verify_release(release)
