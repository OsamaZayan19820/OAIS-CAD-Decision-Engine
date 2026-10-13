import pytest
from oais_cad.pdf_vectors import extract_vector_evidence
from oais_cad.pdf_evidence_gate import EvidenceError


def test_extract_vector_paths_rotated_pdf(tmp_path):
    fitz = pytest.importorskip("fitz")
    file = tmp_path / "synthetic.pdf"
    doc = fitz.open()
    page = doc.new_page(width=300, height=200)
    shape = page.new_shape()
    shape.draw_rect(fitz.Rect(20, 30, 120, 90))
    shape.finish(color=(0,0,0))
    shape.commit()
    page.set_rotation(270)
    doc.save(file)
    doc.close()
    result = extract_vector_evidence(file)
    p = result["pages"][0]
    assert p["rotation"] == 270
    assert p["path_count"] >= 1
    assert p["paths"][0]["inside_display_page"]
    assert p["paths"][0]["semantic_type"] == "UNKNOWN"
    assert p["paths"][0]["measurement_status"] == "NOT_MEASURED"
    assert result["engineering_approval"] is False


def test_vector_path_limit(tmp_path):
    fitz = pytest.importorskip("fitz")
    file = tmp_path / "synthetic.pdf"
    doc = fitz.open()
    page = doc.new_page()
    for i in range(3):
        page.draw_line(fitz.Point(10,10+i*10), fitz.Point(100,10+i*10))
    doc.save(file)
    doc.close()
    with pytest.raises(EvidenceError, match="limit"):
        extract_vector_evidence(file, max_paths_per_page=1)


def test_reject_invalid_limit():
    with pytest.raises(EvidenceError):
        extract_vector_evidence("unused.pdf", max_paths_per_page=0)
