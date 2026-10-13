from oais_cad.junction_policy import classify_junctions

def wall(i,a,b,t=200):
    return {"id":i,"start":list(a),"end":list(b),"thickness":t}

def spec(a,b):
    return {"units":"mm","walls":[a,b],"openings":[]}

def test_t_candidate_remains_hold():
    result=classify_junctions(spec(wall("A",(0,0),(1000,0)),wall("B",(500,0),(500,500))))
    assert result[0]["candidate"]=="T_CANDIDATE"
    assert result[0]["decision"]=="HOLD"
    assert result[0]["approved"] is False

def test_x_crossing_remains_hold():
    result=classify_junctions(spec(wall("A",(0,0),(1000,0)),wall("B",(500,-500),(500,500))))
    assert result[0]["candidate"]=="X_CROSSING"
    assert result[0]["decision"]=="HOLD"

def test_collinear_overlap_remains_hold():
    result=classify_junctions(spec(wall("A",(0,0),(1000,0)),wall("B",(500,0),(1500,0))))
    assert result[0]["candidate"]=="COLLINEAR_OVERLAP"
    assert result[0]["decision"]=="HOLD"

def test_no_junctions():
    assert classify_junctions(spec(wall("A",(0,0),(1000,0)),wall("B",(0,400),(1000,400))))==[]

def test_endpoint_candidate():
    result=classify_junctions(spec(wall("A",(0,0),(1000,0)),wall("B",(1000,0),(1000,1000))))
    assert result[0]["candidate"]=="ENDPOINT_JUNCTION"
    assert result[0]["approved"] is False
