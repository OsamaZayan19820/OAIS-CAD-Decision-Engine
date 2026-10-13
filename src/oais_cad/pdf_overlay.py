"""Render evidence locations over the original PDF page, without geometry claims."""
from pathlib import Path
from .pdf_reader import read_pdf_evidence


def render_evidence_overlay(pdf_path, output_dir, tokens=(), zoom=1.5):
    if isinstance(zoom, bool) or not isinstance(zoom, (int, float)) or not (0.5 <= zoom <= 4):
        raise ValueError("zoom outside safe range")
    try:
        import fitz
    except ImportError as exc:
        raise RuntimeError("PyMuPDF required for PDF overlays") from exc
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    evidence = read_pdf_evidence(pdf_path, tokens=tokens)
    paths = []
    with fitz.open(pdf_path) as document:
        for index, page in enumerate(document):
            pix = page.get_pixmap(matrix=fitz.Matrix(zoom, zoom), alpha=False)
            image = fitz.Pixmap(pix)
            # Draw in rotated display-page coordinates using pixel-space scaling.
            # The original page is rendered first; no annotations modify the source.
            overlay = fitz.open()
            target = overlay.new_page(width=page.rect.width, height=page.rect.height)
            target.insert_image(target.rect, pixmap=image)
            shape = target.new_shape()
            for word in evidence["pages"][index]["words"]:
                if not word["inside_display_page"]:
                    continue
                rect = fitz.Rect(*word["bbox"])
                shape.draw_rect(rect)
            shape.finish(color=(1, 0.18, 0.1), width=0.8)
            shape.commit()
            output_file = output / f"page_{index + 1:03d}_overlay.png"
            target.get_pixmap(matrix=fitz.Matrix(zoom, zoom), alpha=False).save(output_file)
            paths.append(str(output_file))
            overlay.close()
    return {"decision": "REVIEW", "engineering_approval": False,
            "dimension_association": "UNVERIFIED", "files": paths}
