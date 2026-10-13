# OAIS CAD V0.2 — closure and decision matrix

## Verified gates (historical)
- CI #68: independent release reader, PASS.
- CI #71: fault-injection and thread contention, PASS.
- CI #74: cross-process contention on GitHub-hosted runner, PASS.

## Candidate gates awaiting exact-commit CI
- Non-destructive recovery inspection of absent, partial, valid,
  file-target, and symlink-target releases.

## What V0.2 does
- Parse strict millimeter wall/opening intent.
- Generate centerline DXF and 2D wall strips with full-thickness gaps.
- Detect footprint overlap and fail closed on positive-area collision.
- Round-trip check DXF entities, coordinates, layers and closure.
- Publish optional solid output via exclusive directory reservation,
  completion marker, and independent SHA-256 reader.
- Reject competing local process publishers and injected failures.

## What V0.2 does NOT do
- Full CAD authoring, 3D walls, doors/windows with elevation, joins,
  lintels, structural checks, regulatory approval, or CAD desktop validation.
- Cross-host/distributed lock or power-loss recovery.
- Tamper-proof cryptographic source attestation.
- Automatic stale-directory cleanup.
- Unattended merge, public release or engineering sign-off.

## Human closure decision
Technical candidate may be reviewed only after latest CI PASS.
Main merge and public release remain HOLD pending explicit approval.
