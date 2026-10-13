import pytest
from oais_cad.clearance_geometry import GeometryGateError, parallel_segment_gap


def test_parallel_horizontal_gap_is_not_certified():
    result=parallel_segment_gap((0,10,100,10),(20,30,90,30))
    assert result["gap_page_units"]==20
    assert result["overlap_page_units"]==70
    assert result["certified_clearance"] is False
    assert result["scale_verified"] is False


def test_parallel_vertical_gap():
    result=parallel_segment_gap((10,0,10,100),(30,20,30,90))
    assert result["gap_page_units"]==20
    assert result["orientation"]=="vertical"


def test_crossing_lines_rejected():
    result=parallel_segment_gap((0,0,100,0),(50,-10,50,10))
    assert result["gap_page_units"] is None


def test_disjoint_parallel_lines_rejected():
    result=parallel_segment_gap((0,0,10,0),(20,20,30,20))
    assert result["gap_page_units"] is None


def test_same_line_not_clearance():
    result=parallel_segment_gap((0,0,10,0),(0,0,10,0))
    assert result["gap_page_units"] is None


@pytest.mark.parametrize("segment",[(0,0,float("nan"),1),(0,0,True,1),(0,0,1)])
def test_invalid_segment(segment):
    with pytest.raises(GeometryGateError):
        parallel_segment_gap(segment,(0,1,1,1))


def test_invalid_tolerance():
    with pytest.raises(GeometryGateError):
        parallel_segment_gap((0,0,1,0),(0,1,1,1),tolerance=0)
