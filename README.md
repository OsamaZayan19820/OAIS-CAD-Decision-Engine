# OAIS CAD Decision Engine

**From structured intent to verifiable 2D geometry.**

Public pilot of a fail-closed Python CAD generator. It accepts a narrowly defined JSON room-rectangle specification in **millimetres**, rejects unknown fields and overlapping rooms, generates a DXF drawing, re-parses that drawing and writes a JSON evidence report with an input SHA-256 digest.

## Quick start

```bash
python -m pip install -e '.[dev]'
python -m pytest -q
python -m oais_cad.cli examples/two_rooms.json build/
```

Outputs: `build/layout.dxf` and `build/report.json`.

## Supported V0.1 subset

- Axis-aligned rectangles only; room adjacency is permitted
- Explicit units: mm
- DXF R2010 export and entity-count roundtrip check
- Rejection of malformed, overlapping or unsupported geometry
- JSON trace of input hash, area and entity count

## Not supported / not claimed

- Doors, windows, structural elements, complex room boundaries, regulatory compliance
- AutoCAD desktop integration or complete MCP interoperability
- Automated design approval or demonstrated superiority to other CAD repositories

The original larger 24-test source bundle was tested locally but **has not been fully migrated to GitHub**. The code in this repository is a **smaller independent functional subset**, and its own CI result must be checked separately.

## Security

No model-generated scripts are executed. The validator rejects unrecognized fields instead of silently ignoring them.

## License

MIT. See [LICENSE](LICENSE).
