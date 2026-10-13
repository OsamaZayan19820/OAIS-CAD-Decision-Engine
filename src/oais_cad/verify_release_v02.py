"""Independent fail-closed reader for published V0.2 solid DXF artifacts."""
import hashlib
import json
import io
import os
import stat
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
    # Open a pinned directory descriptor and each child with O_NOFOLLOW.
    # Validate size from the opened descriptor, not a prior path stat.
    # Reject platforms without descriptor-relative no-follow semantics.
    if not hasattr(os, "O_NOFOLLOW") or not hasattr(os, "O_DIRECTORY"):
        raise IntentError("Secure file opening unsupported on this platform")
    try:
        root_fd=os.open(root,os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    except OSError as exc:
        raise IntentError("Unsafe release directory") from exc
    try:
        def read_member(name):
            try:
                fd=os.open(name,os.O_RDONLY | os.O_NOFOLLOW | getattr(os,"O_NONBLOCK",0),dir_fd=root_fd)
            except OSError as exc:
                raise IntentError("Unsafe release member") from exc
            try:
                meta=os.fstat(fd)
                if not stat.S_ISREG(meta.st_mode) or meta.st_nlink!=1:
                    raise IntentError("Unsafe release member type")
                if meta.st_size>MAX_BYTES[name]:
                    raise IntentError("Release artifact exceeds size limit")
                with os.fdopen(fd,"rb",closefd=False) as stream:
                    data=stream.read(MAX_BYTES[name]+1)
                after=os.fstat(fd)
                if (after.st_dev!=meta.st_dev or after.st_ino!=meta.st_ino
                    or after.st_size!=meta.st_size or after.st_mtime_ns!=meta.st_mtime_ns
                    or after.st_ctime_ns!=meta.st_ctime_ns):
                    raise IntentError("Release member changed during read")
                if len(data)!=meta.st_size:
                    raise IntentError("Release member changed during read")
                if len(data)>MAX_BYTES[name]:
                    raise IntentError("Release artifact exceeds size limit")
                return data
            finally:
                os.close(fd)
        marker_bytes=read_member("_OAIS_COMPLETE")
        report_bytes=read_member("wall_solids_report_v02.json")
        data=read_member("wall_solids_v02.dxf")
    finally:
        os.close(root_fd)
    try:
        marker=json.loads(marker_bytes.decode("ascii"))
        report=json.loads(report_bytes.decode("utf-8"))
    except (UnicodeError,ValueError) as exc:
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
        doc=ezdxf.read(io.StringIO(data.decode("utf-8")))
        entities=list(doc.modelspace())
    except Exception as exc:
        raise IntentError("DXF cannot be parsed") from exc
    if len(entities)!=report["strip_count"] or any(e.dxftype()!="LWPOLYLINE" or not e.closed or e.dxf.layer!="OAIS_WALL_SOLIDS_2D" for e in entities):
        raise IntentError("DXF geometry or entity count mismatch")
    return {"verified":True,"sha256":digest,"strip_count":len(entities),"architectural_approval":False}
