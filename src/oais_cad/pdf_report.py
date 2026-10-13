"""Evidence-only SVG/JSON report for PDF plan labels. No compliance verdicts."""
import json
from pathlib import Path
from xml.sax.saxutils import escape
from .pdf_reader import read_pdf_evidence


def make_pdf_report(source, output_dir, tokens=()):
    data = read_pdf_evidence(source, tokens=tokens)
    target = Path(output_dir)
    target.mkdir(parents=True, exist_ok=True)
    summary = {"schema": "oais.pdf.evidence.v0", "decision": "REVIEW",
               "engineering_approval": False, "pages": []}
    for page in data["pages"]:
        summary["pages"].append({
            "page": page["page"], "rotation": page["rotation"],
            "word_count": len(page["words"]),
            "in_bounds": sum(w["inside_display_page"] for w in page["words"]),
            "out_of_bounds": sum(not w["inside_display_page"] for w in page["words"]),
            "dimension_association": "UNVERIFIED",
            "compliance": "NOT_ASSESSED"})
        width, height = page["display_width"], page["display_height"]
        parts = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width:g} {height:g}" width="{width:g}" height="{height:g}">',
                 '<rect width="100%" height="100%" fill="white"/>',
                 '<g fill="none" stroke="#d24c38" stroke-width="0.8">']
        for word in page["words"]:
            x0, y0, x1, y1 = word["bbox"]
            parts.append(f'<rect x="{x0:.3f}" y="{y0:.3f}" width="{x1-x0:.3f}" height="{y1-y0:.3f}"/>')
        parts.append('</g><g fill="#253858" font-size="7">')
        for word in page["words"]:
            x0, y0, _, _ = word["bbox"]
            parts.append(f'<text x="{x0:.3f}" y="{max(7,y0-2):.3f}">{escape(word["text"])}</text>')
        parts.append('</g></svg>')
        (target / f'page_{page["page"]:03d}_evidence.svg').write_text(
            "\n".join(parts), encoding="utf-8")
    (target / "report.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    return summary
