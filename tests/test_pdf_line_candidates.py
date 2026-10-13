import pytest
from oais_cad.pdf_line_candidates import line_gap_candidates


def test_synthetic_rotated_pdf_gap_is_unverified(tmp_path):
    fitz = pytest.importorskip("fitz")
    source = tmp_path / "synthetic.pdf"
    doc = fitz.open()
    page = doc.new_page(width=300,height=200)
    page.draw_line((20,30),(150,30))
    page.draw_line((30,50),(140,50))
    page.set_rotation(270)
    doc.save(source)
    doc.close()
    result = line_gap_candidates(source)
    p = result["pages"][0]
    assert p["line_count"] == 2
    assert len(p["gap_candidates"]) == 1
    assert abs(p["gap_candidates"][0]["gap_page_units"] - 20) < 0.001
    assert p["gap_candidates"][0]["certified_clearance"] is False
    assert result["engineering_approval"] is False


def test_line_limit_rejects_large_document(tmp_path):
    fitz = pytest.importorskip("fitz")
    source = tmp_path / "many.pdf"
    doc = fitz.open()
    page = doc.new_page()
    page.draw_line((10,10),(100,10))
    page.draw_line((10,20),(100,20))
    doc.save(source)
    doc.close()
    with pytest.raises(ValueError, match="Line limit"):
        line_gap_candidates(source,max_lines=1)


def test_bad_limits_before_optional_dependency():
    with pytest.raises(ValueError):
        line_gap_candidates("missing.pdf",max_lines=0)
    with pytest.raises(ValueError):
        line_gap_candidates("missing.pdf",max_pairs=0)
