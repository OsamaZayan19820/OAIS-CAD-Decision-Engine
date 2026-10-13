import pytest
from oais_cad.pdf_evidence_gate import EvidenceError, normalize_bbox, reconcile_areas, rotate_point


@pytest.mark.parametrize("rotation,expected", [(0,(10,20)),(90,(180,10)),(180,(90,180)),(270,(20,90))])
def test_page_rotations(rotation,expected):
    assert rotate_point(10,20,100,200,rotation)==expected


def test_rotation_270_bbox():
    result=normalize_bbox((10,20,30,40),100,200,270)
    assert result["bbox"]==(20,70,40,90)
    assert result["inside_display_page"]
    assert result["dimension_association"]=="UNVERIFIED"


def test_outside_page_not_silently_clipped():
    assert not normalize_bbox((-1,0,10,10),100,200,0)["inside_display_page"]


def test_real_plan_area_arithmetic_not_assumed_error():
    result=reconcile_areas(1253.20,{"sales":1006.71,"warehouse":241.50})
    assert result["gap_m2"]==4.99
    assert result["status"]=="REVIEW"
    assert result["cause"]=="UNKNOWN"
    assert result["engineering_approval"] is False


def test_reconciled_area():
    assert reconcile_areas(100,{"sales":80,"storage":20})["status"]=="RECONCILED"


@pytest.mark.parametrize("value", [float("nan"),float("inf"),True])
def test_reject_invalid_coordinate(value):
    with pytest.raises(EvidenceError):
        rotate_point(value,0,100,200,270)


def test_reject_invalid_rotation():
    with pytest.raises(EvidenceError):
        rotate_point(0,0,100,200,45)
