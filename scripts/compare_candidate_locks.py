"""Compare two reviewed pip-tools lock candidates; do not auto-promote."""
import hashlib
import re
import sys
from pathlib import Path

PACKAGE = re.compile(r"^([A-Za-z0-9][A-Za-z0-9_.-]*)==([^\s;\\]+)", re.MULTILINE)

def inspect(path):
    data = Path(path).read_bytes()
    text = data.decode("utf-8")
    packages = {}
    for name, version in PACKAGE.findall(text):
        key = re.sub(r"[-_.]+", "-", name).lower()
        if key in packages:
            raise ValueError(f"duplicate package {key}: {path}")
        packages[key] = version
    if not packages:
        raise ValueError(f"empty lock: {path}")
    return packages, hashlib.sha256(data).hexdigest()

def compare(left, right):
    a, sha_a = inspect(left)
    b, sha_b = inspect(right)
    return {
        "left_sha256": sha_a,
        "right_sha256": sha_b,
        "left_count": len(a),
        "right_count": len(b),
        "left_only": {k: a[k] for k in sorted(a.keys() - b.keys())},
        "right_only": {k: b[k] for k in sorted(b.keys() - a.keys())},
        "version_differences": {
            k: [a[k], b[k]]
            for k in sorted(a.keys() & b.keys())
            if a[k] != b[k]
        },
    }

if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit("usage: compare_candidate_locks.py PY310_LOCK PY311_LOCK")
    import json
    print(json.dumps(compare(sys.argv[1], sys.argv[2]), indent=2, sort_keys=True))
