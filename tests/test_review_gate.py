import pytest
from oais_cad.review_gate import intersection_kind,review_intersections,require_no_unsafe_intersections
from oais_cad.v02 import IntentError

def wall(name,a,b):
    return {"id":name,"start":list(a),"end":list(b),"thickness":100}

def spec(a,b):
    return {"units":"mm","walls":[a,b],"openings":[]}

@pytest.mark.parametrize("a,b,c,d,expected",[
    ((0,0),(10,0),(5,-5),(5,5),"CROSS"),
    ((0,0),(10,0),(10,0),(10,10),"TOUCH"),
    ((0,0),(10,0),(5,0),(15,0),"OVERLAP"),
    ((0,0),(10,0),(11,0),(20,0),"NONE"),
    ((0,0),(10,0),(5,1),(5,5),"NONE"),
    ((0,0),(10,0),(10,0),(20,0),"TOUCH"),
])
def test_classification(a,b,c,d,expected):
    assert intersection_kind(a,b,c,d)==expected

def test_cross_fail_closed():
    s=spec(wall("A",(0,0),(1000,0)),wall("B",(500,-100),(500,100)))
    assert review_intersections(s)[0]["severity"]=="HOLD"
    with pytest.raises(IntentError):
        require_no_unsafe_intersections(s)

def test_endpoint_touch_review_only():
    s=spec(wall("A",(0,0),(1000,0)),wall("B",(1000,0),(1000,1000)))
    assert require_no_unsafe_intersections(s)[0]["severity"]=="REVIEW"
