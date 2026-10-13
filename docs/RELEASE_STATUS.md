# Release status

**V0.1 — PILOT / NOT PRODUCTION**

The complete Python source, examples, tests and generated DXF/SVG artifacts are available in the prepared V0.1 release archive, but **have not yet been uploaded into this repository**.

## Verified locally in the prepared archive
- 24 unit/regression tests passed.
- DXF export was parsed back programmatically.
- Input hash is captured in the decision report.

## Not verified
- AutoCAD GUI round-trip.
- Regulatory/building code compliance.
- End-to-end MCP client interoperability.
- Benchmarked superiority to other CAD MCP projects.

## Publication gate
Do not advertise this repository as executable until `pyproject.toml`, `src/`, `tests/`, `examples/`, and `.github/workflows/ci.yml` have been uploaded and CI has passed on GitHub.
