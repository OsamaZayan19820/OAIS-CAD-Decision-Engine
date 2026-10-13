import math
from oais_cad.opening_solids import solid_strips,review_opening_solids

def wall(i,a,b,t=200):
    return {"id":i,"start":list(a),"end":list(b),"thickness":t}

def spec(walls,openings=None):
    return {"units":"mm","walls":walls,"openings":openings or []}

def opening(i,wall_id,offset,width):
    return {"id":i,"wall_id":wall_id,"type":"door","offset":offset,"width":width}

def area(poly):
    return abs(sum(poly[i][0]*poly[(i+1)%4][1]-poly[(i+1)%4][0]*poly[i][1] for i in range(4)))/2

def test_opening_subtracts_full_thickness_area():
    s=spec([wall("A",(0,0),(5000,0))],[opening("D","A",1000,900)])
    polys=solid_strips(s)["A"]
    assert len(polys)==2
    assert math.isclose(sum(map(area,polys)),(5000-900)*200)

def test_no_opening_one_strip():
    assert len(solid_strips(spec([wall("A",(0,0),(5000,0))]))["A"])==1

def test_full_length_opening_no_solid():
    s=spec([wall("A",(0,0),(1000,0))],[opening("D","A",0,1000)])
    assert solid_strips(s)["A"]==[]

def test_diagonal_area_conservation():
    s=spec([wall("A",(0,0),(3000,4000))],[opening("D","A",1000,900)])
    assert math.isclose(sum(map(area,solid_strips(s)["A"])),4100*200,rel_tol=1e-12)

def test_wall_in_opening_clearance():
    s=spec([wall("A",(0,0),(5000,0)),wall("B",(1450,-100),(1450,100),100)],[opening("D","A",1000,900)])
    assert review_opening_solids(s)["findings"]==[]

def test_wall_outside_opening_is_hold():
    s=spec([wall("A",(0,0),(5000,0)),wall("B",(2100,-100),(2100,100),100)],[opening("D","A",1000,900)])
    assert any(f["severity"]=="HOLD" for f in review_opening_solids(s)["findings"])

def test_findings_never_approved():
    s=spec([wall("A",(0,0),(1000,0)),wall("B",(500,-200),(500,200))])
    assert all(not f["approved"] for f in review_opening_solids(s)["findings"])
