"""Adversarial filesystem fixtures for descriptor-based release verification."""
import os
import pytest
from oais_cad.publish_solids_v02 import publish_solid_plan
from oais_cad.verify_release_v02 import verify_release
from oais_cad.v02 import IntentError

SPEC={"units":"mm","walls":[{"id":"A","start":[0,0],"end":[1000,0],"thickness":200}],"openings":[]}

def test_symlink_member_rejected(tmp_path):
    root=tmp_path/"release"
    publish_solid_plan(SPEC,root)
    report=root/"wall_solids_report_v02.json"
    copy=tmp_path/"copy.json"
    copy.write_bytes(report.read_bytes())
    report.unlink()
    report.symlink_to(copy)
    with pytest.raises(IntentError):
        verify_release(root)

def test_hardlink_member_rejected(tmp_path):
    root=tmp_path/"release"
    publish_solid_plan(SPEC,root)
    os.link(root/"wall_solids_v02.dxf",tmp_path/"alias.dxf")
    with pytest.raises(IntentError,match="Unsafe release member"):
        verify_release(root)

def test_regular_release_still_passes(tmp_path):
    root=tmp_path/"release"
    publish_solid_plan(SPEC,root)
    assert verify_release(root)["verified"] is True
