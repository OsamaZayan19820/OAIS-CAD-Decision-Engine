"""Reject oversized untrusted release artifacts before reading or parsing."""
import pytest
from oais_cad.publish_solids_v02 import publish_solid_plan
from oais_cad.verify_release_v02 import verify_release, MAX_BYTES
from oais_cad.v02 import IntentError

SPEC={"units":"mm","walls":[{"id":"A","start":[0,0],"end":[1000,0],"thickness":200}],"openings":[]}

@pytest.mark.parametrize("name",sorted(MAX_BYTES))
def test_oversized_artifact_fails_closed(tmp_path,name):
    root=tmp_path/"release"
    publish_solid_plan(SPEC,root)
    with (root/name).open("ab") as stream:
        stream.truncate(MAX_BYTES[name]+1)
    with pytest.raises(IntentError,match="size limit"):
        verify_release(root)

def test_normal_release_still_verifies(tmp_path):
    root=tmp_path/"release"
    publish_solid_plan(SPEC,root)
    assert verify_release(root)["verified"] is True
