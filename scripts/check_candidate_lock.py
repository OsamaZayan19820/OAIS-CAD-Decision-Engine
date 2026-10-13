"""Fail-closed structural validation of a pip-tools hash lock candidate."""
import re
import sys
from pathlib import Path

HASH = re.compile(r"^--hash=sha256:[0-9a-f]{64}$")
PIN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.-]*==[^=\s;\\]+(?:\s*;\s*.+)?$")

def validate(text):
    errors = []
    logical = []
    pending = ""
    for number, raw in enumerate(text.splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if not pending and line.startswith(("--", "-e", "-r", "-c", "git+", "http:", "https:", ".", "/")):
            errors.append(f"line {number}: disallowed directive or direct reference")
            continue
        if pending:
            pending += " " + line
        else:
            pending = line
        if pending.endswith("\\"):
            pending = pending[:-1].rstrip()
            continue
        logical.append((number, pending))
        pending = ""
    if pending:
        errors.append("unterminated continuation")
    if not logical:
        errors.append("empty lock")
    seen = set()
    for number, entry in logical:
        parts = entry.split()
        hash_start = next((i for i, token in enumerate(parts) if token.startswith("--hash=")), len(parts))
        requirement = " ".join(parts[:hash_start])
        if not parts or not PIN.fullmatch(requirement):
            errors.append(f"line {number}: package must be exactly pinned")
            continue
        name = requirement.split("==", 1)[0].lower().replace("_", "-").replace(".", "-")
        if name in seen:
            errors.append(f"line {number}: duplicate package")
        seen.add(name)
        hashes = parts[hash_start:]
        if not hashes or any(not HASH.fullmatch(h) for h in hashes):
            errors.append(f"line {number}: missing or invalid SHA-256 hash")
    return errors

if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("usage: check_candidate_lock.py LOCKFILE")
    errors = validate(Path(sys.argv[1]).read_text(encoding="utf-8"))
    if errors:
        sys.exit("Candidate lock rejected:\n" + "\n".join(errors))
    print("Candidate lock structural validation PASS")
