"""Verify that installed direct dependencies satisfy project metadata constraints."""
import sys
try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path
from packaging.requirements import Requirement

root = Path(__file__).resolve().parents[1]
project = tomllib.loads((root / "pyproject.toml").read_text(encoding="utf-8"))["project"]
requirements = list(project["dependencies"])
for group in project.get("optional-dependencies", {}).values():
    requirements.extend(group)

failures = []
for raw in requirements:
    req = Requirement(raw)
    if req.marker is not None and not req.marker.evaluate():
        continue
    try:
        installed = version(req.name)
    except PackageNotFoundError:
        failures.append(f"{req.name}: not installed")
        continue
    if installed not in req.specifier:
        failures.append(f"{req.name}: installed {installed}, required {req.specifier}")
    else:
        print(f"OK {req.name}=={installed} satisfies {req.specifier}")

if failures:
    print("Dependency constraints failed:\n" + "\n".join(failures), file=sys.stderr)
    sys.exit(1)
