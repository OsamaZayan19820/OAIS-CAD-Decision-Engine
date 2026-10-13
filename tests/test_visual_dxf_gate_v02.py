import json
from pathlib import Path
import pytest
from oais_cad.export_solids_v02 import export_solid_plan
from oais_cad.visual_dxf_gate_v02 import verify
from oais_cad.v02 import IntentError

def test_real_dxf_and_svg_geometry(tmp_path):
    source=Path(__file__).resolve().parents[1]/"examples"/"v02_walls.json"
    spec=json.loads(source.read_text())
    export_solid_plan(spec,tmp_path)
    result=verify(spec,tmp_path/"wall_solids_v02.dxf")
    assert result["status"]=="PASS_2D_GEOMETRY_ONLY"
    assert result["strips"]==3

def test_rejects_missing_dxf(tmp_path):
    source=Path(__file__).resolve().parents[1]/"examples"/"v02_walls.json"
    spec=json.loads(source.read_text())
    with pytest.raises(Exception):
        verify(spec,tmp_path/"missing.dxf")
