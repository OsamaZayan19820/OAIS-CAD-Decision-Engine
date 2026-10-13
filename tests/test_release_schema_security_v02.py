"""Reject malformed or extended completion marker and report schemas."""
import json
import pytest
from oais_cad.publish_solids_v02 import publish_solid_plan
from oais_cad.verify_release_v02 import verify_release
from oais_cad.v02 import IntentError

SPEC={"units":"mm","walls":[{"id":"A","start":[0,0],"end":[1000,0],"thickness":200}],"openings":[]}

@pytest.mark.parametrize("mutation",[
    lambda x: [],
    lambda x: {"protocol":2.0,"dxf_sha256":x["dxf_sha256"],"report_sha256":x["report_sha256"]},
    lambda x: {**x,"unexpected":"payload"},
])
def test_bad_marker_schema_rejected(tmp_path,mutation):
    root=tmp_path/"release"
    publish_solid_plan(SPEC,root)
    path=root/"_OAIS_COMPLETE"
    path.write_text(json.dumps(mutation(json.loads(path.read_text()))))
    with pytest.raises(IntentError):
        verify_release(root)

def test_non_object_report_rejected(tmp_path):
    root=tmp_path/"release"
    publish_solid_plan(SPEC,root)
    (root/"wall_solids_report_v02.json").write_text("[]")
    with pytest.raises(IntentError):
        verify_release(root)
