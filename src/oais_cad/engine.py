"""Constrained 2D rectangle-plan validator and DXF exporter (millimetres)."""
import hashlib
import json
import math
from pathlib import Path

class ValidationError(ValueError):
    pass

def _positive_number(value, label):
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or value <= 0:
        raise ValidationError(f"{label}: expected finite positive number")
    return float(value)

def validate(spec):
    if not isinstance(spec, dict) or set(spec) != {"units", "rooms"}:
        raise ValidationError("Expected only units and rooms")
    if spec["units"] != "mm":
        raise ValidationError("Only millimetres (mm) supported")
    rooms = spec["rooms"]
    if not isinstance(rooms, list) or not rooms:
        raise ValidationError("rooms must be a nonempty list")
    if len(rooms) > 200:
        raise ValidationError("Too many rooms")
    result = []
    names = set()
    for i, room in enumerate(rooms):
        if not isinstance(room, dict) or set(room) != {"name", "x", "y", "width", "height"}:
            raise ValidationError(f"room {i}: unsupported or missing attributes")
        name = room["name"]
        if not isinstance(name, str) or not name.strip() or len(name) > 80 or name in names:
            raise ValidationError("Invalid or duplicate room name")
        names.add(name)
        x, y = room["x"], room["y"]
        if any(isinstance(v, bool) or not isinstance(v, (int, float)) or not math.isfinite(v) for v in (x,y)):
            raise ValidationError("Invalid coordinates")
        w = _positive_number(room["width"], "width")
        h = _positive_number(room["height"], "height")
        if max(abs(x), abs(y), w, h) > 1e7:
            raise ValidationError("Coordinate bounds exceeded")
        result.append({"name":name,"x":float(x),"y":float(y),"width":w,"height":h})
    for i, a in enumerate(result):
        for b in result[i+1:]:
            ox = min(a["x"]+a["width"],b["x"]+b["width"]) - max(a["x"],b["x"])
            oy = min(a["y"]+a["height"],b["y"]+b["height"]) - max(a["y"],b["y"])
            if ox > 1e-8 and oy > 1e-8:
                raise ValidationError(f"Overlapping rooms: {a['name']} / {b['name']}")
    return result

def generate(spec, output_dir):
    rooms = validate(spec)
    import ezdxf
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    document = ezdxf.new("R2010")
    document.header["$INSUNITS"] = 4
    model = document.modelspace()
    for r in rooms:
        x,y,w,h = (r[k] for k in ("x","y","width","height"))
        model.add_lwpolyline([(x,y),(x+w,y),(x+w,y+h),(x,y+h)],close=True)
    dxf = out / "layout.dxf"
    document.saveas(dxf)
    # Verify serialization independently by parsing the generated file.
    parsed = ezdxf.readfile(dxf)
    actual = len(parsed.modelspace().query("LWPOLYLINE"))
    if actual != len(rooms):
        raise ValidationError("DXF roundtrip entity count mismatch")
    canonical = json.dumps(spec,sort_keys=True,separators=(",",":"),allow_nan=False).encode()
    report = {"status":"PASS_GEOMETRY_ONLY","input_sha256":hashlib.sha256(canonical).hexdigest(),"units":"mm","rooms":len(rooms),"total_area_m2":sum(r["width"]*r["height"] for r in rooms)/1e6,"dxf_roundtrip_entities":actual,"regulatory_approval":False}
    (out/"report.json").write_text(json.dumps(report,indent=2),encoding="utf-8")
    return report
