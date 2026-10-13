# OAIS CAD V0.2 — reproducible demo

Install from the feature branch:
```bash
python -m pip install -e '.[dev]'
python -m pytest -q
python -m oais_cad.demo_v02 --out build/oais_demo_v02
```

Expected outputs:
- `build/oais_demo_v02/wall_solids_v02.dxf`
- `build/oais_demo_v02/wall_solids_report_v02.json`
- `build/oais_demo_v02/_OAIS_COMPLETE`

The demo uses a 5000 mm wall, 200 mm thickness and a 900 mm full-thickness
opening. Two closed 2D wall strips must result, with combined plan area
820000 mm². The script verifies the release marker, SHA-256 and DXF entity
properties. It refuses to overwrite the output directory. To rerun,
choose a fresh `--out` path.

External CAD desktop compatibility and human engineering approval remain
UNVERIFIED. This demonstration does not grant release or merge approval.
