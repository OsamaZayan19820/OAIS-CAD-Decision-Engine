# OAIS CAD — Value proof gate v0

## Claim boundary

A green GitHub CI result proves that the included automated tests passed. It
does **not** establish real-plan measurement accuracy, legal compliance, aisle
identification, scale calibration, or permission to release engineering work.

## Stage A: reproducible synthetic arithmetic

Run `pytest -q tests/test_value_proof.py`. The 30-case test checks known,
independently specified PDF-page-unit separations between axis-aligned segments.
The acceptance threshold is at least 95% within 0.01 PDF page units, with zero
unsupported certifications. These are proposed engineering test thresholds,
not regulatory standards. The suite also tests absent, wrong and unsafe evidence.

## Stage B: blinded real-plan study (NOT YET DONE)

An authorized engineer must prepare at least three distinct real-world plans
and 30 reference measurements, with drawing revision, page, reference scale,
measurement endpoints, tolerance, and evidence of boundary identity. Keep source
drawings in private storage. Freeze reference labels before executing the engine.
Compare eligible predictions against the reference and separately count:
coverage, measurement error, false positives, unsupported certification, and
reviewer time. Report rejected/unknown cases rather than excluding them silently.

## Go/no-go

PASS in Stage A permits Stage B only. Stage B requires independently checked
reference data, declared tolerance, at least 95% accuracy on eligible measured
cases, 100% provenance, zero unsupported compliance/clearance approvals and
a documented reviewer decision. If these cannot be established, HOLD. No
automatic approval, production release or public release of proprietary plans.
