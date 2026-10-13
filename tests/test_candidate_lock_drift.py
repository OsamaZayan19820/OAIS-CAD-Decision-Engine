"""Adversarial tests for reviewed candidate lock drift gate."""
import importlib.util
from pathlib import Path
import pytest

spec = importlib.util.spec_from_file_location(
    "lock_drift", Path(__file__).resolve().parents[1] / "scripts" / "check_candidate_lock_drift.py"
)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

def test_rejects_modified_lock(tmp_path):
    lock = tmp_path / "candidate.txt"
    lock.write_text("sample==1.0 --hash=sha256:" + "a" * 64)
    with pytest.raises(ValueError, match="LOCK DRIFT"):
        module.verify(lock, (3, 10))

def test_rejects_unreviewed_interpreter(tmp_path):
    lock = tmp_path / "candidate.txt"
    lock.write_text("")
    with pytest.raises(ValueError, match="unreviewed Python version"):
        module.verify(lock, (3, 12))

def test_rejects_missing_file(tmp_path):
    with pytest.raises(FileNotFoundError):
        module.verify(tmp_path / "missing.txt", (3, 11))
