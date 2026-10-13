"""Fail-closed, directory-level publication of a new solid DXF export.

Destination MUST NOT exist. Build and verify in a sibling temporary
directory, then rename it into place. Existing output is never overwritten.
Same-filesystem rename is atomic on common local POSIX filesystems;
network filesystems and concurrent writers require separate coordination.
"""
import json
import os
import tempfile
from pathlib import Path

from .v02 import IntentError
from .export_solids_v02 import export_solid_plan

def publish_solid_plan(spec, destination):
    target=Path(destination)
    parent=target.parent.resolve()
    if target.exists() or target.is_symlink():
        raise IntentError("Destination already exists; overwrite forbidden")
    parent.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=".oais-stage-",dir=parent) as tmp:
        staged=Path(tmp)/"release"
        report=export_solid_plan(spec,staged)
        expected={"wall_solids_v02.dxf","wall_solids_report_v02.json"}
        if {p.name for p in staged.iterdir()}!=expected:
            raise IntentError("Unexpected staging artifacts")
        if not all((staged/name).is_file() and (staged/name).stat().st_size>0 for name in expected):
            raise IntentError("Missing or empty staging artifact")
        if json.loads((staged/"wall_solids_report_v02.json").read_text(encoding="utf-8"))!=report:
            raise IntentError("Staging report mismatch")
        if target.exists() or target.is_symlink():
            raise IntentError("Destination appeared during staging")
        # This is a single directory publication; it is not an overwrite
        # primitive and must not be used without external writer locking.
        os.rename(staged,target)
        return report
