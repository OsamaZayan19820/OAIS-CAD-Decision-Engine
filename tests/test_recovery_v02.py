from oais_cad.recovery_v02 import inspect_release
from oais_cad.publish_solids_v02 import publish_solid_plan

def example():
    return {"units":"mm","walls":[{"id":"A","start":[0,0],"end":[1000,0],"thickness":200}],"openings":[]}

def test_absent_is_safe_to_create(tmp_path):
    assert inspect_release(tmp_path/"missing")["state"]=="ABSENT"

def test_incomplete_is_held_without_mutation(tmp_path):
    root=tmp_path/"release"
    root.mkdir()
    partial=root/"wall_solids_v02.dxf"
    partial.write_bytes(b"partial")
    state=inspect_release(root)
    assert state["state"]=="INCOMPLETE_OR_INVALID"
    assert state["action"]=="HOLD_MANUAL_REVIEW"
    assert partial.read_bytes()==b"partial"

def test_verified_release_is_preserved(tmp_path):
    root=tmp_path/"release"
    publish_solid_plan(example(),root)
    assert inspect_release(root)["state"]=="VERIFIED"
    assert inspect_release(root)["action"]=="PRESERVE"

def test_file_target_held(tmp_path):
    path=tmp_path/"release"
    path.write_text("not a directory")
    assert inspect_release(path)["state"]=="INVALID_TARGET"

def test_symlink_target_held(tmp_path):
    actual=tmp_path/"real"
    actual.mkdir()
    alias=tmp_path/"alias"
    alias.symlink_to(actual,target_is_directory=True)
    assert inspect_release(alias)["state"]=="UNSAFE_SYMLINK"
