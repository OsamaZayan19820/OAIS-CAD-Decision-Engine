"""Detect drift against reviewed, interpreter-specific candidate lock bytes.

These digests are review baselines, NOT approval to promote or release.
"""
import hashlib
import sys
from pathlib import Path

REVIEWED = {
    (3, 10): "2e6208e797722ff7ebafa735eb7a751666fa2463ffb3116ff4464ec1de667297",
    (3, 11): "6f21f07e88940a0828ea7ed57c7b4dc771a0a9dd4d7aacc9a282806b6e2dc961",
}

def verify(path, version=None):
    version = version or sys.version_info[:2]
    expected = REVIEWED.get(tuple(version))
    if expected is None:
        raise ValueError(f"unreviewed Python version: {version}")
    actual = hashlib.sha256(Path(path).read_bytes()).hexdigest()
    if actual != expected:
        raise ValueError(f"LOCK DRIFT: Python {version[0]}.{version[1]} expected {expected}, got {actual}")
    return actual

if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("usage: check_candidate_lock_drift.py LOCKFILE")
    try:
        print("Reviewed candidate lock SHA-256 verified:", verify(sys.argv[1]))
    except (ValueError, OSError) as exc:
        sys.exit(str(exc))
