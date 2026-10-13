import pytest
from oais_cad.pdf_overlay import render_evidence_overlay


def test_overlay_on_synthetic_rotated_pdf(tmp_path):
    fitz = pytest.importorskip("fitz")
    source = tmp_path / "sample.pdf"
    doc = fitz.open()
    page = doc.new_page(width=300, height=200)
    page.insert_text((30, 60), "1.80")
    page.set_rotation(270)
    doc.save(source)
    doc.close()
    result = render_evidence_overlay(source, tmp_path / "output", tokens={"1.80"})
    assert result["decision"] == "REVIEW"
    assert result["engineering_approval"] is False
    image = tmp_path / "output/page_001_overlay.png"
    assert image.exists() and image.stat().st_size > 100


def test_overlay_zoom_bounds(tmp_path):
    with pytest.raises(ValueError):
        render_evidence_overlay(tmp_path / "none.pdf", tmp_path / "output", zoom=100)
