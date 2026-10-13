#!/usr/bin/env bash
# Generate and validate a candidate hash-locked third-party environment.
# Run in a disposable trusted Python 3.10 or 3.11 environment.
set -euo pipefail
python -m pip install 'pip-tools==7.5.1'
python -m piptools compile --generate-hashes --resolver=backtracking --output-file requirements-locked-candidate.txt requirements-audit.txt
python -m venv .lock-verify-venv
.lock-verify-venv/bin/python -m pip install --require-hashes --only-binary=:all: -r requirements-locked-candidate.txt
.lock-verify-venv/bin/python -m pip check
.lock-verify-venv/bin/python -m pip install 'pip-audit==2.9.0'
.lock-verify-venv/bin/python -m pip_audit --strict --progress-spinner off -r requirements-locked-candidate.txt
echo "Candidate dependency lock installed and audited. HUMAN REVIEW REQUIRED before promotion."
