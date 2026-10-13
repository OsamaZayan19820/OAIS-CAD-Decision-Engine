# OAIS CAD Decision Engine

**From intent to verifiable geometry.**

An open-source, evidence-driven prototype for generating 2D CAD drawings from structured requirements and validating geometry before export.

## V0.1 status

- Python geometry and validation pipeline
- DXF export, SVG previews, JSON decision reports
- MCP adapter prototype
- Fail-closed validation and regression tests
- **Pilot only**: no structural, building-code, or AutoCAD interoperability certification

## Source release

The V0.1 source package has been prepared and tested locally (24 passing tests). The source code and CI workflow will be added as separate commits. **This README does not imply the code has already been published.**

## Principles

1. Decision authority is not evidence authority.
2. Unknown or unsupported requirements fail closed.
3. No arbitrary model-generated CAD scripts are executed.
4. Geometry validation does not imply regulatory approval.
5. Every export should be traceable to its input specification.

## License

MIT, subject to inclusion of the LICENSE file in the published source release.
