# V0.2 export acceptance gate

Command:

```bash
python -m pip install -e '.[dev]'
python -m pytest -q
python -m oais_cad.cli_v02 examples/v02_walls.json build/v02
```

Artifacts: layout_v02.dxf, preview_v02.svg, report_v02.json.

Verified by code: 2D centerline coordinates, missing opening spans, DXF LINE coordinates and layer on round-trip, input SHA-256.

**Not verified**: wall thickness solids, door/window symbols, intersections between distinct walls, load-bearing design, building-code compliance, AutoCAD desktop behavior, SVG/DXF visual parity in third-party CAD software. No claim of full independent geometry certification.

Human review required before merging. Keep draft PR open until CI confirms and design scope is accepted.
