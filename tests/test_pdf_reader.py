import pytest
from oais_cad.pdf_reader import read_pdf_evidence


def test_generated_pdf_rotated_coordinates(tmp_path):
    fitz = pytest.importorskip("fitz")
    path = tmp_path / "synthetic.pdf"
    doc = fitz.open()
    page = doc.new_page(width=300, height=200)
    page.insert_text((30, 60), "1.80")
    page.set_rotation(270)
    doc.save(path)
    doc.close()
    result = read_pdf_evidence(path, tokens={"1.80"})
    assert len(result["pages"]) == 1
    p = result["pages"][0]
    assert p["rotation"] == 270
    assert p["display_width"] == 200
    assert len(p["words"]) == 1
    assert p["words"][0]["inside_display_page"]
    assert p["words"][0]["dimension_association"] == "UNVERIFIED"
    assert result["engineering_approval"] is False


def test_reject_non_pdf(tmp_path):
    fitz = pytest.importorskip("fitz")
    p = tmp_path / "notpdf.txt"
    p.write_text("not a pdf")
    with pytest.raises(Exception):
        read_pdf_evidence(p)
