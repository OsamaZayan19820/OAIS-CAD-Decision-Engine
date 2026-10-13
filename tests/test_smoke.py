import json
import pytest
from oais_cad.engine import validate,generate,ValidationError

def sample():
    return {"units":"mm","rooms":[{"name":"A","x":0,"y":0,"width":3000,"height":4000},{"name":"B","x":3000,"y":0,"width":2000,"height":4000}]}

def test_valid_plan():
    assert len(validate(sample())) == 2

def test_roundtrip(tmp_path):
    result=generate(sample(),tmp_path)
    assert result["dxf_roundtrip_entities"]==2
    assert result["total_area_m2"]==20
    assert result["regulatory_approval"] is False
    assert json.loads((tmp_path/"report.json").read_text())["status"]=="PASS_GEOMETRY_ONLY"

@pytest.mark.parametrize("change",[
    {"units":"cm"},
    {"rooms":[]},
    {"unexpected":1},
])
def test_invalid_top_level(change):
    spec=sample()
    spec.update(change)
    with pytest.raises(ValidationError):
        validate(spec)

def test_overlap_rejected():
    spec=sample()
    spec["rooms"][1]["x"]=1000
    with pytest.raises(ValidationError,match="Overlapping"):
        validate(spec)

def test_unknown_room_field_rejected():
    spec=sample()
    spec["rooms"][0]["doors"]=[]
    with pytest.raises(ValidationError):
        validate(spec)

def test_nonfinite_rejected():
    spec=sample()
    spec["rooms"][0]["width"]=float("nan")
    with pytest.raises(ValidationError):
        validate(spec)
