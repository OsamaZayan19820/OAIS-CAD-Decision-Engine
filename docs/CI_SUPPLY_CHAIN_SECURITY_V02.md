# CI supply-chain security — V0.2

Controls implemented in the development branch:
- GitHub Actions workflow and job permissions restricted to contents:read.
- Checkout and Python setup actions referenced by full commit SHA.
- Runner image explicitly ubuntu-24.04; job timeout 15 minutes.
- No secrets are needed for tests; no publishing or deployment step.

Residual risks and required review:
- The pinned action commit identities require periodic independent verification
  against upstream trusted release provenance.
- Python dependencies and build backend remain version ranges; transitive
  dependencies are NOT hash locked. This is a supply-chain DATA VOID.
- pip currently resolves packages from a package index at CI time.
- Hosted runner image can change despite its version label.
- PR workflows must not be granted write permissions or deployment secrets.
- Before promotion: use a reproducible hash-locked dependency installation,
  verify dependency licenses and advisories, and require reviewed changes to
  workflow files.

Decision: CI_HARDENING_CANDIDATE; not a production security certification.
