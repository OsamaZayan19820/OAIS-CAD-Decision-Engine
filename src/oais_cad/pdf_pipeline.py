"""Unified fail-closed PDF evidence pipeline. No compliance or clearance claims."""
import hashlib
import json
from pathlib import Path

from .pdf_reader import read_pdf_evidence
from .pdf_vectors import extract_vector_evidence
from .dimension_association import associate_label_candidates
from .pdf_line_candidates import line_gap_candidates


def run_pdf_pipeline(source, output_dir, tokens=(), radius=25, max_paths_per_page=50000,
                     max_lines=2000, max_pairs=100000):
    path = Path(source)
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    text = read_pdf_evidence(path, tokens=tokens)
    vectors = extract_vector_evidence(path, max_paths_per_page=max_paths_per_page)
    lines = line_gap_candidates(path, max_lines=max_lines, max_pairs=max_pairs)
    if not (len(text["pages"]) == len(vectors["pages"]) == len(lines["pages"])):
        raise ValueError("Page count mismatch between evidence readers")
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    pages = []
    for text_page, vector_page, line_page in zip(text["pages"], vectors["pages"], lines["pages"]):
        if (text_page["page"] != vector_page["page"] or
                text_page["page"] != line_page["page"] or
                text_page["rotation"] != vector_page["rotation"]):
            raise ValueError("Page provenance mismatch")
        labels = [{"text": word["text"], "bbox": word["bbox"]}
                  for word in text_page["words"] if word["inside_display_page"]]
        nearby = associate_label_candidates(labels, vector_page["paths"], radius=radius)
        pages.append({"page": text_page["page"], "rotation": text_page["rotation"],
                      "labels": len(labels), "vector_paths": vector_page["path_count"],
                      "candidate_associations": nearby,
                      "straight_line_count": line_page["line_count"],
                      "gap_candidates": line_page["gap_candidates"],
                      "gap_units": "PDF_PAGE_UNITS",
                      "scale_verified": False,
                      "semantic_boundaries_verified": False,
                      "dimension_association": "UNVERIFIED",
                      "clearance": "NOT_MEASURED", "compliance": "NOT_ASSESSED"})
    report = {"schema": "oais.pdf.pipeline.v0", "source_sha256": digest,
              "pages": pages, "decision": "REVIEW", "engineering_approval": False}
    (output / "evidence_pipeline.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    return report
