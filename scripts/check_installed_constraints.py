"""Verify installed direct dependency versions against project metadata."""
import sys
try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path
from packaging.requirements import Requirement

ROOT = Path(__file__).resolve().parents[1]

def check_constraints(project_file=ROOT / "pyproject.toml", get_version=version):
    project = tomllib.loads(Path(project_file).read_text(encoding="utf-8"))["project"]
    requirements = list(project["dependencies"])
    for group in project.get("optional-dependencies", {}).values():
        requirements.extend(group)
    failures = []
    for raw in requirements:
        req = Requirement(raw)
        if req.marker is not None and not req.marker.evaluate():
            continue
        try:
            installed = get_version(req.name)
        except PackageNotFoundError:
            failures.append(f"{req.name}: not installed")
            continue
        if installed not in req.specifier:
            failures.append(f"{req.name}: installed {installed}, required {req.specifier}")
        else:
            print(f"OK {req.name}=={installed} satisfies {req.specifier}")
    return failures

if __name__ == "__main__":
    failures = check_constraints()
    if failures:
        print("Dependency constraints failed:\n" + "\n".join(failures), file=sys.stderr)
        sys.exit(1)
