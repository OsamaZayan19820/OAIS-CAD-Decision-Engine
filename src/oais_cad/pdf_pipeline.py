"""Unified fail-closed PDF evidence pipeline. No compliance or clearance claims."""
import hashlib
import json
from pathlib import Path

from .pdf_reader import read_pdf_evidence
from .pdf_vectors import extract_vector_evidence
from .dimension_association import associate_label_candidates


def run_pdf_pipeline(source, output_dir, tokens=(), radius=25, max_paths_per_page=50000):
    path = Path(source)
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    text = read_pdf_evidence(path, tokens=tokens)
    vectors = extract_vector_evidence(path, max_paths_per_page=max_paths_per_page)
    if len(text["pages"]) != len(vectors["pages"]):
        raise ValueError("Page count mismatch between evidence readers")
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    pages = []
    for text_page, vector_page in zip(text["pages"], vectors["pages"]):
        if text_page["page"] != vector_page["page"] or text_page["rotation"] != vector_page["rotation"]:
            raise ValueError("Page provenance mismatch")
        labels = [{"text": word["text"], "bbox": word["bbox"]}
                  for word in text_page["words"] if word["inside_display_page"]]
        nearby = associate_label_candidates(labels, vector_page["paths"], radius=radius)
        pages.append({"page": text_page["page"], "rotation": text_page["rotation"],
                      "labels": len(labels), "vector_paths": vector_page["path_count"],
                      "candidate_associations": nearby,
                      "dimension_association": "UNVERIFIED",
                      "clearance": "NOT_MEASURED", "compliance": "NOT_ASSESSED"})
    report = {"schema": "oais.pdf.pipeline.v0", "source_sha256": digest,
              "pages": pages, "decision": "REVIEW", "engineering_approval": False}
    (output / "evidence_pipeline.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    return report
