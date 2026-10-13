# OAIS CAD Decision Engine — V0.2 technical handoff

## Scope and authority
Candidate technical handoff only. Branch: `feature/v0.2-intent-geometry`.
Main merge, public release, architectural certification and structural approval
are NOT authorized. Human decision remains required.

## Verified CI evidence
- Commit `d47e2738a019f12b736ac6fee0bc1b5e8bfcd44a`: CI #68 PASS — release reader.
- Commit `fdc5fadbae8c87f29a9498bcb43358dc4c812904`: CI #71 PASS — fault injection and thread contention.
- Commit `8b6283f3b678dcd4abbc69fc038d3559d1a8923f`: CI #74 PASS — cross-process contention.
- Commit `2dabed3f97ad767b30068cc09804b21965dd0b35`: CI #79 PASS — non-destructive recovery inspector.

## Reproducible review
```bash
python -m pip install -e '.[dev]'
python -m compileall -q src tests
python -m pytest -q
```

## Supported candidate interfaces
- `oais_cad.v02.compile_intent` validates millimeter wall/opening intent.
- `oais_cad.export_v02.export_plan` exports centerline DXF/SVG/report.
- `oais_cad.export_solids_v02.export_solid_plan` exports 2D strip DXF/report.
- `oais_cad.publish_solids_v02.publish_solid_plan` publishes to a new directory.
- `oais_cad.verify_release_v02.verify_release` verifies a completed release.
- `oais_cad.recovery_v02.inspect_release` inspects without deletion.

## Known limitations and DATA VOID
- No 3D, elevation, window sill, door leaf, construction joints or certified CAD compatibility.
- No external CAD desktop opening/visual comparison evidence.
- No crash-durable publication, distributed locking or stale reservation reclamation.
- SHA-256 checks integrity, not provenance or authenticity.
- Existing centerline CLI remains separate from optional solid release workflow.
- Review gates do not auto-approve legitimate T-junction overlaps.

## Closure decision
TECHNICAL_HANDOFF_CANDIDATE — subject to CI for this document commit.
Merge/public release: HOLD until explicit human authorization.
