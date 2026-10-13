"""Fault-injection and competing-writer tests for publication V0.2."""
import threading
from concurrent.futures import ThreadPoolExecutor
from unittest.mock import patch
import pytest
from oais_cad.publish_solids_v02 import publish_solid_plan
from oais_cad.verify_release_v02 import verify_release
from oais_cad.v02 import IntentError

def spec():
    return {"units":"mm","walls":[{"id":"A","start":[0,0],"end":[1000,0],"thickness":200}],"openings":[]}

def test_concurrent_writers_one_wins(tmp_path):
    target=tmp_path/"release"
    barrier=threading.Barrier(2)
    def writer(_):
        barrier.wait(timeout=10)
        try:
            publish_solid_plan(spec(),target)
            return "PUBLISHED"
        except IntentError:
            return "REJECTED"
    with ThreadPoolExecutor(max_workers=2) as pool:
        results=list(pool.map(writer,range(2)))
    assert sorted(results)==["PUBLISHED","REJECTED"]
    assert verify_release(target)["verified"] is True

def test_write_failure_rolls_back(tmp_path):
    target=tmp_path/"release"
    original_open=type(target).open
    def broken_open(path,*args,**kwargs):
        if path.name=="_OAIS_COMPLETE":
            raise OSError("injected marker write failure")
        return original_open(path,*args,**kwargs)
    with patch("pathlib.Path.open",new=broken_open):
        with pytest.raises(OSError,match="injected"):
            publish_solid_plan(spec(),target)
    assert not target.exists()
    assert not list(tmp_path.glob(".oais-stage-*"))

def test_incomplete_reservation_is_not_accepted(tmp_path):
    target=tmp_path/"release"
    target.mkdir()
    (target/"wall_solids_v02.dxf").write_bytes(b"partial")
    with pytest.raises(IntentError,match="Incomplete"):
        verify_release(target)
    with pytest.raises(IntentError,match="exists"):
        publish_solid_plan(spec(),target)
