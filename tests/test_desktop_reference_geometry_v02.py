"""Numerical reference for independent desktop CAD inspection."""
import math
from oais_cad.opening_solids import solid_strips

def test_reference_vertices_and_area():
    spec={"units":"mm","walls":[{"id":"W1","start":[0,0],"end":[5000,0],"thickness":200}],"openings":[{"id":"D1","wall_id":"W1","type":"door","offset":1000,"width":900}]}
    polys=solid_strips(spec)["W1"]
    assert len(polys)==2
    bounds=sorted((min(x for x,y in p),max(x for x,y in p),min(y for x,y in p),max(y for x,y in p)) for p in polys)
    assert bounds==[(0.,1000.,-100.,100.),(1900.,5000.,-100.,100.)]
    assert math.isclose(sum((b-a)*(d-c) for a,b,c,d in bounds),820000.)
