import json
import pytest
from oais_cad.pdf_pipeline import run_pdf_pipeline


def test_pipeline_rotated_synthetic_pdf(tmp_path):
    fitz = pytest.importorskip("fitz")
    source = tmp_path / "synthetic.pdf"
    doc = fitz.open()
    page = doc.new_page(width=300, height=200)
    page.insert_text((30, 60), "1.80")
    page.draw_line(fitz.Point(20, 50), fitz.Point(120, 50))
    page.draw_line(fitz.Point(20, 70), fitz.Point(120, 70))
    page.set_rotation(270)
    doc.save(source)
    doc.close()
    result = run_pdf_pipeline(source, tmp_path / "out", tokens=["1.80"])
    assert result["decision"] == "REVIEW"
    assert result["engineering_approval"] is False
    assert len(result["source_sha256"]) == 64
    assert result["pages"][0]["labels"] == 1
    assert result["pages"][0]["vector_paths"] >= 1
    assert result["pages"][0]["straight_line_count"] == 2
    assert len(result["pages"][0]["gap_candidates"]) == 1
    assert result["pages"][0]["gap_candidates"][0]["gap_page_units"] == 20
    assert result["pages"][0]["gap_candidates"][0]["certified_clearance"] is False
    assert result["pages"][0]["scale_verified"] is False
    assert result["pages"][0]["dimension_association"] == "UNVERIFIED"
    assert result["pages"][0]["clearance"] == "NOT_MEASURED"
    assert result["pages"][0]["candidate_associations"][0]["association_verified"] is False
    saved = json.loads((tmp_path / "out/evidence_pipeline.json").read_text())
    assert saved == result


def test_pipeline_fails_closed_on_pair_limit(tmp_path):
    fitz = pytest.importorskip("fitz")
    source = tmp_path / "pairs.pdf"
    doc = fitz.open()
    page = doc.new_page()
    for y in (20, 40, 60):
        page.draw_line((20, y), (120, y))
    doc.save(source)
    doc.close()
    with pytest.raises(ValueError, match="Pair limit"):
        run_pdf_pipeline(source, tmp_path / "out", max_pairs=1)
    assert not (tmp_path / "out/evidence_pipeline.json").exists()
