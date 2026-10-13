"""Negative security tests for hash-lock candidate validator."""
import importlib.util
from pathlib import Path

script = Path(__file__).resolve().parents[1] / "scripts" / "check_candidate_lock.py"
spec = importlib.util.spec_from_file_location("lock_check", script)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
GOOD = "sample==1.2.3 \\\n    --hash=sha256:" + "a" * 64 + "\n"

def test_accepts_valid_hash_pin():
    assert module.validate(GOOD) == []

def test_rejects_unhashed_pin():
    assert module.validate("sample==1.2.3\n")

def test_rejects_unpinned_requirement():
    assert module.validate("sample>=1 --hash=sha256:" + "a" * 64)

def test_rejects_remote_direct_reference():
    assert module.validate("https://example.invalid/pkg.whl\n")

def test_rejects_duplicate_pin():
    assert module.validate(GOOD + GOOD)

def test_rejects_invalid_hash():
    assert module.validate("sample==1.2.3 --hash=sha256:abc\n")

def test_rejects_standalone_hash_directive():
    assert module.validate("--hash=sha256:" + "a" * 64 + "\n")

def test_rejects_hash_continuation_with_invalid_digest():
    assert module.validate("sample==1.2.3 \\\n    --hash=sha256:abc\n")

def test_rejects_extra_option_in_continuation():
    assert module.validate("sample==1.2.3 \\\n    --index-url=https://example.invalid/simple\n")
