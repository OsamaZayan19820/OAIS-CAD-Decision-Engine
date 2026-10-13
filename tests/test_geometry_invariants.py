"""Adversarial invariants for wall footprint and junction review."""
import pytest
from oais_cad.solid_geometry import classify_footprints,review_wall_solids
from oais_cad.junction_policy import classify_junctions

def w(i,a,b,t=200):
    return {"id":i,"start":list(a),"end":list(b),"thickness":t}

def s(a,b):
    return {"units":"mm","walls":[a,b],"openings":[]}

@pytest.mark.parametrize("offset,expected",[
    (199.0,"OVERLAP"),
    (200.0,"TOUCH"),
    (201.0,"SEPARATE"),
])
def test_thickness_boundary(offset,expected):
    a=[(0,-100),(1000,-100),(1000,100),(0,100)]
    b=[(0,offset-100),(1000,offset-100),(1000,offset+100),(0,offset+100)]
    assert classify_footprints(a,b)==expected

def test_pair_order_symmetry():
    a=[(0,0),(10,0),(10,10),(0,10)]
    b=[(5,5),(15,5),(15,15),(5,15)]
    assert classify_footprints(a,b)==classify_footprints(b,a)=="OVERLAP"

def test_translation_invariance():
    a=[(0,0),(10,0),(10,10),(0,10)]
    b=[(10,0),(20,0),(20,10),(10,10)]
    translated=lambda p:[(x+10000,y-7000) for x,y in p]
    assert classify_footprints(a,b)==classify_footprints(translated(a),translated(b))=="TOUCH"

def test_thickness_only_collision_is_not_authorized():
    result=classify_junctions(s(w("A",(0,0),(1000,0)),w("B",(0,150),(1000,150))))
    assert result[0]["candidate"]=="THICKNESS_ONLY_CONTACT"
    assert result[0]["decision"]=="HOLD"

def test_junction_findings_never_auto_approve():
    result=classify_junctions(s(w("A",(0,0),(1000,0)),w("B",(500,0),(500,500))))
    assert all(not item["approved"] for item in result)

def test_no_findings_for_distant_walls():
    assert review_wall_solids(s(w("A",(0,0),(1000,0)),w("B",(0,1000),(1000,1000))))["findings"]==[]
