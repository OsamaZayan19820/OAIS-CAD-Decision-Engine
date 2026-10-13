"""Adversarial mutation of an opened artifact during verification."""
import os
import pytest
from oais_cad.publish_solids_v02 import publish_solid_plan
from oais_cad.verify_release_v02 import verify_release
from oais_cad.v02 import IntentError

SPEC={"units":"mm","walls":[{"id":"A","start":[0,0],"end":[1000,0],"thickness":200}],"openings":[]}

def test_in_place_mutation_during_read_is_rejected(tmp_path,monkeypatch):
    root=tmp_path/"release"
    publish_solid_plan(SPEC,root)
    real_fdopen=os.fdopen
    class MutatingReader:
        def __init__(self,stream):
            self.stream=stream
        def __enter__(self):
            self.stream.__enter__()
            return self
        def __exit__(self,*args):
            return self.stream.__exit__(*args)
        def read(self,*args,**kwargs):
            data=self.stream.read(*args,**kwargs)
            if b"SECTION" in data:
                with (root/"wall_solids_v02.dxf").open("r+b") as writer:
                    writer.truncate(0)
            return data
    def intercepted(fd,*args,**kwargs):
        stream=real_fdopen(fd,*args,**kwargs)
        return MutatingReader(stream)
    monkeypatch.setattr(os,"fdopen",intercepted)
    with pytest.raises(IntentError,match="changed during read"):
        verify_release(root)

def test_unchanged_release_passes(tmp_path):
    root=tmp_path/"release"
    publish_solid_plan(SPEC,root)
    assert verify_release(root)["verified"] is True
