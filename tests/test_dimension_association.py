import pytest
from oais_cad.dimension_association import AssociationError, associate_label_candidates


def test_nearest_candidates_are_not_approved():
    labels=[{"text":"1.80","bbox":[10,10,20,20]}]
    vectors=[{"id":"v1","bbox":[21,11,30,19]},{"id":"v2","bbox":[100,100,120,120]}]
    result=associate_label_candidates(labels,vectors,radius=10)
    assert [x["vector_id"] for x in result[0]["candidates"]]==["v1"]
    assert result[0]["association_verified"] is False
    assert result[0]["measured_clearance"] is None
    assert result[0]["status"]=="REVIEW"


def test_no_candidates_remains_review():
    result=associate_label_candidates([{"text":"0.75","bbox":[1,1,2,2]}],[],radius=1)
    assert result[0]["candidates"]==[]
    assert result[0]["status"]=="REVIEW"


@pytest.mark.parametrize("radius",[0,-1,float("nan"),True])
def test_reject_bad_radius(radius):
    with pytest.raises(AssociationError):
        associate_label_candidates([],[],radius=radius)


def test_reject_nonfinite_bbox():
    with pytest.raises(AssociationError):
        associate_label_candidates([{"text":"x","bbox":[0,0,float("inf"),1]}],[])
