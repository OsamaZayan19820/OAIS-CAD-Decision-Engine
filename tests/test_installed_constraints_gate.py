"""Adversarial tests for the installed dependency constraint gate."""
import importlib.util
from importlib.metadata import PackageNotFoundError
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "check_installed_constraints.py"
spec = importlib.util.spec_from_file_location("dependency_gate", SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

def test_rejects_incompatible_installed_version(tmp_path):
    manifest = tmp_path / "pyproject.toml"
    manifest.write_text('[project]\ndependencies = ["example-package>=2,<3"]\n')
    failures = module.check_constraints(manifest, lambda name: "1.0")
    assert len(failures) == 1 and "required" in failures[0]

def test_rejects_missing_installed_dependency(tmp_path):
    manifest = tmp_path / "pyproject.toml"
    manifest.write_text('[project]\ndependencies = ["example-package>=2,<3"]\n')
    def missing(name):
        raise PackageNotFoundError(name)
    failures = module.check_constraints(manifest, missing)
    assert len(failures) == 1 and "not installed" in failures[0]

def test_accepts_compatible_installed_version(tmp_path):
    manifest = tmp_path / "pyproject.toml"
    manifest.write_text('[project]\ndependencies = ["example-package>=2,<3"]\n')
    assert module.check_constraints(manifest, lambda name: "2.5") == []
