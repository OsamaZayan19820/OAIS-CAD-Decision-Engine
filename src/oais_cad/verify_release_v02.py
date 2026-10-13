"""Independent fail-closed reader for published V0.2 solid DXF artifacts."""
import hashlib
import json
from pathlib import Path

from .v02 import IntentError

EXPECTED={"wall_solids_v02.dxf","wall_solids_report_v02.json","_OAIS_COMPLETE"}

def verify_release(destination):
    root=Path(destination)
    if not root.is_dir() or root.is_symlink():
        raise IntentError("Release directory missing or unsafe")
    entries=list(root.iterdir())
    if {p.name for p in entries}!=EXPECTED or any(not p.is_file() or p.is_symlink() for p in entries):
        raise IntentError("Incomplete or unexpected release artifacts")
    try:
        marker=(root/"_OAIS_COMPLETE").read_text(encoding="ascii")
        report=json.loads((root/"wall_solids_report_v02.json").read_text(encoding="utf-8"))
        data=(root/"wall_solids_v02.dxf").read_bytes()
    except (UnicodeError,ValueError,OSError) as exc:
        raise IntentError("Unreadable release") from exc
    digest=hashlib.sha256(data).hexdigest()
    if len(marker)!=64 or marker!=digest or report.get("dxf_sha256")!=digest:
        raise IntentError("Release checksum mismatch")
    if report.get("status")!="PASS_2D_SOLID_STRIPS_ONLY" or report.get("dxf_roundtrip")!="PASS" or report.get("architectural_approval") is not False:
        raise IntentError("Invalid release status or approval claim")
    if not isinstance(report.get("strip_count"),int) or isinstance(report["strip_count"],bool) or report["strip_count"]<=0:
        raise IntentError("Invalid strip count")
    import ezdxf
    try:
        doc=ezdxf.readfile(root/"wall_solids_v02.dxf")
        entities=list(doc.modelspace())
    except Exception as exc:
        raise IntentError("DXF cannot be parsed") from exc
    if len(entities)!=report["strip_count"] or any(e.dxftype()!="LWPOLYLINE" or not e.closed or e.dxf.layer!="OAIS_WALL_SOLIDS_2D" for e in entities):
        raise IntentError("DXF geometry or entity count mismatch")
    return {"verified":True,"sha256":digest,"strip_count":len(entities),"architectural_approval":False}
