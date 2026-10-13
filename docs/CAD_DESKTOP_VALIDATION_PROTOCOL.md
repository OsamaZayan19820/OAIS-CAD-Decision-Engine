# Independent CAD desktop validation protocol — V0.2

## Objective
Establish evidence beyond ezdxf round-trip checks. This protocol does
NOT claim an external CAD application has been tested.

## Reproducible sample input
Save as `sample.json`:
```json
{
  "units": "mm",
  "walls": [
    {"id":"W1","start":[0,0],"end":[5000,0],"thickness":200}
  ],
  "openings": [
    {"id":"D1","wall_id":"W1","type":"door","offset":1000,"width":900}
  ]
}
```

## Generate 2D solid DXF
```python
import json
from oais_cad.export_solids_v02 import export_solid_plan
spec=json.load(open("sample.json",encoding="utf-8"))
print(export_solid_plan(spec,"build/desktop_check"))
```
Output: `build/desktop_check/wall_solids_v02.dxf`.

## Independent operator checks
1. Open DXF in a separate CAD application (record name and version).
2. Verify drawing units are millimeters.
3. Verify exactly two closed polylines on `OAIS_WALL_SOLIDS_2D`.
4. Verify wall length 5000 mm, wall thickness 200 mm.
5. Verify the omitted interval is from x=1000 to x=1900 mm,
   full thickness across y=-100 to y=+100 mm.
6. Independently measure combined 2D strip area: 820000 mm².
7. Save screenshots of entity properties, dimension checks and area
   measurement; retain original DXF and report hashes.
8. Record operator, date, application/version, observed dimensions,
   PASS/FAIL and any deviations. Do not alter the reference DXF.

## Acceptance
PASS only if all observations agree within a documented measurement
tolerance chosen and approved by the operator. Any mismatch is HOLD.
This protocol is an instruction set, not proof of a completed test.
