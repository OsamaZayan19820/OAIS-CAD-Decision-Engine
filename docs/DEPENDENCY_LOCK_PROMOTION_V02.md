# Dependency lock promotion — controlled procedure

Status: HOLD — no hash-locked environment has yet been produced or validated.

## Scope
- Python 3.10 and 3.11 on ubuntu-24.04, matching the current CI matrix.
- Runtime: ezdxf and transitive dependencies.
- Development/test: pytest, conditional tomli, and transitive dependencies.
- Audit tooling: pip-audit and its dependencies must also be assessed separately.

## Required evidence before promotion
1. Resolve dependencies in a trusted, clean build environment for each supported Python version.
2. Generate a complete transitive dependency lock with package versions and artifact SHA-256 hashes, using a reviewed lockfile generator. Never fabricate hashes.
3. Verify artifacts originate from approved package indexes and record wheel/platform markers.
4. Install from the lock using pip --require-hashes in an isolated environment; prohibit fallback to unpinned downloads.
5. Run pip check, pip-audit, full regression tests and CAD export smoke tests against that exact locked environment.
6. Verify audit input covers the *installed* external dependency closure, not just direct project requirements.
7. Review differences between Python 3.10 and 3.11 resolution; archive lock generation command, tool version, and CI run evidence.
8. Require human review before making lockfiles governing or merging into main.

## Fail-closed rules
- Missing hash, unresolved transitive dependency, unsupported wheel, or audit error => HOLD.
- Unavailable vulnerability service => HOLD, not PASS.
- An unreviewed dependency upgrade => HOLD.
- Do not treat pip freeze as a hash lock or an SBOM.
- Do not claim bit-for-bit reproducibility from version pins alone.

## Current evidence
CI #143 passed for Python 3.10 and 3.11 before installed-environment checks.
CI #145 includes pip check and installed version recording; its final result must be verified independently.
