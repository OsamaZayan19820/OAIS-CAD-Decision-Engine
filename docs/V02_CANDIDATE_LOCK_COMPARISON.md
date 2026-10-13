# OAIS-CAD — Candidate Lock Comparison (CI #189)

Status: **EVIDENCE ONLY — NOT APPROVED FOR PROMOTION**

Source: https://github.com/OsamaZayan19820/OAIS-CAD-Decision-Engine/actions/runs/38446534276
Commit generating the lock artifacts: `f1f274d22c7114e50817a8c9866cb005894c7a4f`

## Verified extracted payloads

| Interpreter | Artifact ID | Lock file bytes | SHA-256 of extracted lock text | Pinned packages |
|---|---:|---:|---|---:|
| Python 3.10 | 11838078090 | 20809 | `2e6208e797722ff7ebafa735eb7a751666fa2463ffb3116ff4464ec1de667297` | 12 |
| Python 3.11 | 11838362740 | 15711 | `6f21f07e88940a0828ea7ed57c7b4dc771a0a9dd4d7aacc9a282806b6e2dc961` | 10 |

The above SHA-256 values are for the **extracted lockfile bytes**, not the artifact ZIP.

## Package differences

- Python 3.10 only: `exceptiongroup==1.3.1`, `tomli==2.5.0`.
- Python 3.10 `numpy==2.2.6`; Python 3.11 `numpy==2.4.6`.
- Python 3.10 `fonttools==4.65.0`; Python 3.11 `fonttools==4.66.1`.
- All other eight common package versions match, including `ezdxf==1.4.4` and `pytest==9.1.1`.
- The `tomli` entry is conditional on `python_version < "3.11"`.

## Decision implications

- Separate interpreter-specific lockfiles are required for reproducibility of these **observed resolutions**.
- Successful CI candidate installs do not independently authenticate package publishers, establish stable index state, or prove external CAD interoperability.
- Archive retention is limited. The two lockfiles must be preserved in a governed repository change and independently reviewed before promotion.
- **HOLD** on adopting these lockfiles as governing; **HOLD** on main merge and release.
