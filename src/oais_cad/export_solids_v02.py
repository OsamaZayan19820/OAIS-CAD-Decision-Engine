"""Separate, conservative wall-solid DXF export; no authorization."""
import hashlib
import json
import tempfile
from pathlib import Path
from .v02 import IntentError
from .opening_solids import review_opening_solids

def export_solid_plan(spec, destination):
    review=review_opening_solids(spec)
    if any(f["severity"]=="HOLD" for f in review["findings"]):
        raise IntentError("Wall solids overlap: HOLD")
    strips=review["strips"]
    count=sum(map(len,strips.values()))
    if not count:
        raise IntentError("No drawable wall solids")
    import ezdxf
    doc=ezdxf.new("R2010")
    doc.header["$INSUNITS"]=4
    doc.layers.new("OAIS_WALL_SOLIDS_2D")
    msp=doc.modelspace()
    for wall_id,polys in strips.items():
        for poly in polys:
            msp.add_lwpolyline(poly,close=True,dxfattribs={"layer":"OAIS_WALL_SOLIDS_2D"})
    with tempfile.TemporaryDirectory() as td:
        path=Path(td)/"solids.dxf"
        doc.saveas(path)
        read=ezdxf.readfile(path)
        found=list(read.modelspace().query("LWPOLYLINE"))
        if len(found)!=count:
            raise IntentError("Solid DXF entity count mismatch")
        expected=[p for polys in strips.values() for p in polys]
        for poly,entity in zip(expected,found):
            if not entity.closed or entity.dxf.layer!="OAIS_WALL_SOLIDS_2D":
                raise IntentError("DXF closure or layer mismatch")
            actual=list(entity.get_points("xy"))
            if len(actual)!=4 or any(abs(x-a)>1e-6 or abs(y-b)>1e-6 for (x,y),(a,b) in zip(actual,poly)):
                raise IntentError("Solid DXF coordinate mismatch")
        data=path.read_bytes()
    canonical=json.dumps(spec,sort_keys=True,separators=(",",":"),allow_nan=False).encode()
    report={
        "status":"PASS_2D_SOLID_STRIPS_ONLY",
        "input_sha256":hashlib.sha256(canonical).hexdigest(),
        "dxf_sha256":hashlib.sha256(data).hexdigest(),
        "strip_count":count,
        "intersection_findings":review["findings"],
        "dxf_roundtrip":"PASS",
        "architectural_approval":False,
        "scope":"2D rectangular wall strips with full-thickness opening gaps; not 3D or certified"
    }
    out=Path(destination)
    out.mkdir(parents=True,exist_ok=True)
    (out/"wall_solids_v02.dxf").write_bytes(data)
    (out/"wall_solids_report_v02.json").write_text(json.dumps(report,indent=2),encoding="utf-8")
    return report
