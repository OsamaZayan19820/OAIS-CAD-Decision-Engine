#!/usr/bin/env bash
# Candidate only. Execute in a disposable, trusted Linux CI runner.
set -euo pipefail
PYTHON="${PYTHON:-python}"
"$PYTHON" -m pip install 'pip-tools==7.5.1'
"$PYTHON" -m piptools compile --generate-hashes --resolver=backtracking --output-file requirements-locked-candidate.txt requirements-audit.txt
"$PYTHON" -m venv .lock-verify-venv
VENV_PY=".lock-verify-venv/bin/python"
"$VENV_PY" -m pip install --require-hashes --only-binary=:all: -r requirements-locked-candidate.txt
"$VENV_PY" -m pip check
# Keep audit tooling separate from the locked test environment.
"$PYTHON" -m pip install 'pip-audit==2.9.0'
"$PYTHON" -m pip_audit --strict --progress-spinner off -r requirements-locked-candidate.txt
# Exercise the local source without introducing unlocked build-backend dependencies.
"$VENV_PY" -m pip check
"$VENV_PY" scripts/check_installed_constraints.py
PYTHONPATH=src "$VENV_PY" -m compileall -q src tests
PYTHONPATH=src "$VENV_PY" -m pytest -q
PYTHONPATH=src "$VENV_PY" -m oais_cad.cli_v02 examples/v02_walls.json build/locked-v02
test -s build/locked-v02/layout_v02.dxf
test -s build/locked-v02/preview_v02.svg
test -s build/locked-v02/report_v02.json
echo "Candidate hash-locked environment passed regression and export checks; human review required."
