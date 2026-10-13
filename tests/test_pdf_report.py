import json
import pytest
from oais_cad.pdf_report import make_pdf_report


def test_evidence_report_synthetic_pdf(tmp_path):
    fitz = pytest.importorskip("fitz")
    source = tmp_path / "synthetic.pdf"
    doc = fitz.open()
    page = doc.new_page(width=300, height=200)
    page.insert_text((30, 60), "1.80")
    page.set_rotation(270)
    doc.save(source)
    doc.close()
    result = make_pdf_report(source, tmp_path / "output", tokens={"1.80"})
    assert result["decision"] == "REVIEW"
    assert result["engineering_approval"] is False
    assert result["pages"][0]["word_count"] == 1
    assert result["pages"][0]["in_bounds"] == 1
    svg = (tmp_path / "output/page_001_evidence.svg").read_text()
    assert "<rect " in svg
    assert "1.80" in svg
    saved = json.loads((tmp_path / "output/report.json").read_text())
    assert saved == result
