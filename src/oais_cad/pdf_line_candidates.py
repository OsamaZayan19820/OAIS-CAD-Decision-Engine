"""Extract actual PDF straight line items and compute unverified gap candidates."""
import math
from .clearance_geometry import parallel_segment_gap


def line_gap_candidates(pdf_path, max_lines=2000, max_pairs=100000):
    if not isinstance(max_lines, int) or isinstance(max_lines, bool) or not 1 <= max_lines <= 100000:
        raise ValueError("Invalid line limit")
    if not isinstance(max_pairs, int) or isinstance(max_pairs, bool) or not 1 <= max_pairs <= 1000000:
        raise ValueError("Invalid pair limit")
    try:
        import fitz
    except ImportError as exc:
        raise RuntimeError("PyMuPDF required for line extraction") from exc
    pages = []
    with fitz.open(pdf_path) as document:
        for page_index, page in enumerate(document):
            segments = []
            for path_index, drawing in enumerate(page.get_drawings()):
                for item_index, item in enumerate(drawing.get("items", [])):
                    if item[0] != "l":
                        continue
                    a, b = item[1:3]
                    values = (a.x, a.y, b.x, b.y)
                    if not all(math.isfinite(x) for x in values):
                        raise ValueError("Non-finite line coordinate")
                    # PDF drawing coordinates are unrotated; map endpoints to display space.
                    p1 = fitz.Point(a) * page.rotation_matrix
                    p2 = fitz.Point(b) * page.rotation_matrix
                    segments.append({"id": f"p{page_index+1}-d{path_index+1}-l{item_index+1}",
                                     "segment": [p1.x,p1.y,p2.x,p2.y]})
                    if len(segments) > max_lines:
                        raise ValueError("Line limit exceeded")
            total_pairs = len(segments) * (len(segments) - 1) // 2
            if total_pairs > max_pairs:
                raise ValueError("Pair limit exceeded")
            pairs = []
            attempted = 0
            for i, first in enumerate(segments):
                for second in segments[i+1:]:
                    attempted += 1
                    if attempted > max_pairs:
                        raise ValueError("Pair limit exceeded")
                    gap = parallel_segment_gap(first["segment"], second["segment"])
                    if gap["status"] == "GEOMETRIC_CANDIDATE":
                        pairs.append({"first_id": first["id"], "second_id": second["id"],
                                      **gap})
            pages.append({"page": page_index+1, "line_count":len(segments),
                          "pairs_evaluated":attempted, "gap_candidates":pairs})
    return {"schema":"oais.pdf.line_candidates.v0", "pages":pages,
            "units":"PDF_PAGE_UNITS", "scale_verified":False,
            "semantic_boundaries_verified":False, "decision":"REVIEW",
            "engineering_approval":False}
