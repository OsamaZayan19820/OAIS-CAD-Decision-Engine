"""Extract traceable PDF vector primitives; never infer CAD semantics."""
import math
from .pdf_evidence_gate import EvidenceError, normalize_bbox


def extract_vector_evidence(pdf_path, max_paths_per_page=50000):
    if isinstance(max_paths_per_page, bool) or not isinstance(max_paths_per_page, int) or not 1 <= max_paths_per_page <= 100000:
        raise EvidenceError("Invalid path limit")
    try:
        import fitz
    except ImportError as exc:
        raise RuntimeError("PyMuPDF required for vector extraction") from exc
    pages = []
    with fitz.open(pdf_path) as doc:
        if not doc.is_pdf:
            raise EvidenceError("PDF required")
        for page_index, page in enumerate(doc):
            drawings = page.get_drawings()
            if len(drawings) > max_paths_per_page:
                raise EvidenceError("Vector path limit exceeded")
            paths = []
            for index, drawing in enumerate(drawings):
                bbox = drawing.get("rect")
                if bbox is None:
                    continue
                coords = tuple(float(v) for v in bbox)
                if any(not math.isfinite(v) for v in coords):
                    raise EvidenceError("Non-finite vector bbox")
                mapped = normalize_bbox(coords, page.mediabox.width, page.mediabox.height, page.rotation)
                paths.append({"id": f"p{page_index+1}-v{index+1}",
                              "source_page": page_index+1, "source_path_index": index,
                              "bbox": list(mapped["bbox"]),
                              "inside_display_page": mapped["inside_display_page"],
                              "item_types": sorted({str(item[0]) for item in drawing.get("items", [])}),
                              "semantic_type": "UNKNOWN", "measurement_status": "NOT_MEASURED"})
            pages.append({"page": page_index+1, "rotation": page.rotation,
                          "path_count": len(drawings), "paths_with_bbox": len(paths),
                          "paths": paths})
    return {"schema": "oais.pdf.vectors.v0", "pages": pages,
            "decision": "REVIEW", "engineering_approval": False}
