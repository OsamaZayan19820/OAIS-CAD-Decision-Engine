import pytest
from oais_cad.solid_geometry import footprint,classify_footprints,review_wall_solids,require_no_solid_overlap
from oais_cad.v02 import compile_intent,IntentError

def spec(a,b):
    return {"units":"mm","walls":[a,b],"openings":[]}

def wall(name,start,end,thickness=200):
    return {"id":name,"start":list(start),"end":list(end),"thickness":thickness}

def test_footprint_area():
    w=list(compile_intent({"units":"mm","walls":[wall("A",(0,0),(1000,0))],"openings":[]})["walls"].values())[0]
    assert footprint(w)==[(0,100),(1000,100),(1000,-100),(0,-100)]

def test_parallel_clearance():
    s=spec(wall("A",(0,0),(1000,0)),wall("B",(0,300),(1000,300)))
    assert review_wall_solids(s)["findings"]==[]

def test_parallel_overlap_rejected():
    s=spec(wall("A",(0,0),(1000,0)),wall("B",(0,150),(1000,150)))
    with pytest.raises(IntentError,match="overlap"):
        require_no_solid_overlap(s)

def test_t_junction_conservative_hold():
    s=spec(wall("A",(0,0),(1000,0)),wall("B",(500,0),(500,500)))
    with pytest.raises(IntentError):
        require_no_solid_overlap(s)

def test_exact_touch_review():
    s=spec(wall("A",(0,0),(1000,0)),wall("B",(0,200),(1000,200)))
    assert review_wall_solids(s)["findings"][0]["severity"]=="REVIEW"

def test_diagonal_intersection_hold():
    s=spec(wall("A",(0,0),(1000,1000)),wall("B",(0,1000),(1000,0)))
    with pytest.raises(IntentError):
        require_no_solid_overlap(s)

def test_invalid_tolerance():
    square=[(0,0),(1,0),(1,1),(0,1)]
    with pytest.raises(IntentError):
        classify_footprints(square,square,float("nan"))
