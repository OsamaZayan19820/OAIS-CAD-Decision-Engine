"""Fail CI if third-party audit requirements drift from project metadata."""
from pathlib import Path
import tomllib

ROOT=Path(__file__).resolve().parents[1]

def test_audit_requirements_match_project_dependencies():
    project=tomllib.loads((ROOT/"pyproject.toml").read_text(encoding="utf-8"))
    declared=set(project["project"]["dependencies"])
    for group in project["project"].get("optional-dependencies",{}).values():
        declared.update(group)
    audited={
        line.strip() for line in (ROOT/"requirements-audit.txt").read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    }
    assert audited==declared, f"Dependency audit drift: missing={declared-audited}, extra={audited-declared}"
