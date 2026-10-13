# Release readiness

**Status: PUBLIC PILOT / NOT PRODUCTION.**

The repository now includes a runnable minimal subset: `src/oais_cad/engine.py`, `src/oais_cad/cli.py`, `tests/test_smoke.py`, an example, packaging metadata and CI.

The previous 24-test source archive is **not fully replicated here**. Its test result does not establish the status of this GitHub subset.

### Verification

- GitHub file writes: confirmed.
- GitHub Actions workflow file: committed.
- GitHub Actions execution: NOT YET VERIFIED.
- AutoCAD desktop round-trip: DATA VOID.
- Building-code or structural compliance: NOT EVALUATED.
- MCP integration: NOT IMPLEMENTED in this subset.
- Competitor performance comparison: NOT MEASURED.

Release requires a passing CI run, independent DXF inspection, documented scope and a human release decision.
