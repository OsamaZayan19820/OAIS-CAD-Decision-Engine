"""Optional PDF text evidence reader. Does not infer dimensions or compliance."""
from .pdf_evidence_gate import normalize_bbox, EvidenceError, reconcile_areas


def read_pdf_evidence(pdf_path, tokens=()):
    """Read word locations with normalized displayed-page coordinates.

    Requires PyMuPDF (fitz), installed separately. This is evidence extraction
    only: no geometric associations, clearance measurements or approval.
    """
    try:
        import fitz
    except ImportError as exc:
        raise RuntimeError("Install PyMuPDF to read PDF evidence") from exc
    token_set = set(tokens)
    results = []
    with fitz.open(pdf_path) as document:
        if not document.is_pdf:
            raise EvidenceError("PDF input required")
        for page_index, page in enumerate(document):
            box = page.mediabox
            width, height = float(box.width), float(box.height)
            rotation = page.rotation
            items = []
            for word in page.get_text("words"):
                value = str(word[4]).strip()
                if token_set and value not in token_set:
                    continue
                evidence = normalize_bbox(tuple(word[:4]), width, height, rotation)
                items.append({"text": value, "bbox": list(evidence["bbox"]),
                              "inside_display_page": evidence["inside_display_page"],
                              "dimension_association": "UNVERIFIED"})
            results.append({"page": page_index + 1, "rotation": rotation,
                            "display_width": page.rect.width,
                            "display_height": page.rect.height,
                            "words": items, "compliance": "NOT_ASSESSED"})
    return {"pages": results, "decision": "REVIEW", "engineering_approval": False}
