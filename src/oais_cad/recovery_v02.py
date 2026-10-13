"""Non-destructive inspection of incomplete CAD releases.

This module never deletes, overwrites or reclaims a reservation.
"""
from pathlib import Path
from .v02 import IntentError
from .verify_release_v02 import verify_release

def inspect_release(destination):
    root=Path(destination)
    if root.is_symlink():
        return {"state":"UNSAFE_SYMLINK","action":"HOLD_MANUAL_REVIEW"}
    if not root.exists():
        return {"state":"ABSENT","action":"MAY_CREATE_NEW"}
    if not root.is_dir():
        return {"state":"INVALID_TARGET","action":"HOLD_MANUAL_REVIEW"}
    try:
        result=verify_release(root)
    except (IntentError,OSError) as exc:
        return {"state":"INCOMPLETE_OR_INVALID","action":"HOLD_MANUAL_REVIEW",
                "reason":str(exc)}
    return {"state":"VERIFIED","action":"PRESERVE","verification":result}
