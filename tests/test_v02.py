import pytest
from oais_cad.v02 import compile_intent,wall_segments,IntentError

def example():
    return {"units":"mm","walls":[{"id":"W1","start":[0,0],"end":[5000,0],"thickness":200}],"openings":[{"id":"D1","wall_id":"W1","type":"door","offset":1000,"width":900}]}

def test_wall_split():
    segments=wall_segments(example())
    assert len(segments)==2
    assert segments[0]["end"]==[1000,0]
    assert segments[1]["start"]==[1900,0]

def test_unsupported_field():
    x=example();x["openings"][0]["swing"]="left"
    with pytest.raises(IntentError):compile_intent(x)

def test_overlap():
    x=example();x["openings"].append({"id":"D2","wall_id":"W1","type":"door","offset":1500,"width":1000})
    with pytest.raises(IntentError,match="Overlapping"):compile_intent(x)

def test_outside():
    x=example();x["openings"][0]["offset"]=4900
    with pytest.raises(IntentError,match="outside"):compile_intent(x)

def test_bad_wall_reference():
    x=example();x["openings"][0]["wall_id"]="missing"
    with pytest.raises(IntentError):compile_intent(x)

def test_units():
    x=example();x["units"]="m"
    with pytest.raises(IntentError):compile_intent(x)
