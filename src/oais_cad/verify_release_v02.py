"""Independent fail-closed reader for published V0.2 solid DXF artifacts."""
import hashlib
import json
from pathlib import Path

from .v02 import IntentError

EXPECTED={"wall_solids_v02.dxf","wall_solids_report_v02.json","_OAIS_COMPLETE"}
MAX_BYTES={"wall_solids_v02.dxf":32*1024*1024,"wall_solids_report_v02.json":2*1024*1024,"_OAIS_COMPLETE":4096}

def verify_release(destination):
    root=Path(destination)
    if not root.is_dir() or root.is_symlink():
        raise IntentError("Release directory missing or unsafe")
    entries=list(root.iterdir())
    if {p.name for p in entries}!=EXPECTED or any(not p.is_file() or p.is_symlink() for p in entries):
        raise IntentError("Incomplete or unexpected release artifacts")
    # Refuse oversized artifacts before loading or parsing untrusted content.
    # These are V0.2 policy limits, not a guarantee against resource exhaustion.
    try:
        if any((root/name).stat().st_size>limit for name,limit in MAX_BYTES.items()):
            raise IntentError("Release artifact exceeds size limit")
    except OSError as exc:
        raise IntentError("Unreadable release metadata") from exc
    try:
        marker=json.loads((root/"_OAIS_COMPLETE").read_text(encoding="ascii"))
        report_bytes=(root/"wall_solids_report_v02.json").read_bytes()
        report=json.loads(report_bytes.decode("utf-8"))
        data=(root/"wall_solids_v02.dxf").read_bytes()
    except (UnicodeError,ValueError,OSError) as exc:
        raise IntentError("Unreadable release") from exc
    digest=hashlib.sha256(data).hexdigest()
    if (not isinstance(marker,dict) or marker.get("protocol")!=2
        or marker.get("dxf_sha256")!=digest
        or marker.get("report_sha256")!=hashlib.sha256(report_bytes).hexdigest()
        or report.get("dxf_sha256")!=digest):
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
