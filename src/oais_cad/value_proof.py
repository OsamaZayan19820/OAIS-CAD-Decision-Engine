"""Auditable synthetic-reference acceptance gate; never substitutes for field validation."""
import math


def assess_reference_cases(cases, *, tolerance=0.01, min_cases=30, min_accuracy=0.95):
    """Compare known PDF-unit gaps to independent reference values.

    This gate only evaluates numeric correctness and false certification on supplied
    cases. It cannot establish aisle semantics, physical scale, or field accuracy.
    """
    if isinstance(min_cases, bool) or not isinstance(min_cases, int) or min_cases < 1:
        raise ValueError("Invalid minimum case count")
    for name, value in (("tolerance", tolerance), ("min_accuracy", min_accuracy)):
        if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
            raise ValueError("Invalid " + name)
    if tolerance < 0 or not 0 <= min_accuracy <= 1:
        raise ValueError("Invalid acceptance threshold")
    results = []
    for index, case in enumerate(cases):
        if not isinstance(case, dict) or "expected_gap_page_units" not in case:
            raise ValueError("Missing independent reference")
        expected = case["expected_gap_page_units"]
        actual = case.get("actual_gap_page_units")
        if isinstance(expected, bool) or not isinstance(expected, (int, float)) or not math.isfinite(expected) or expected <= 0:
            raise ValueError("Invalid reference gap")
        if actual is not None and (isinstance(actual, bool) or not isinstance(actual, (int, float)) or not math.isfinite(actual) or actual <= 0):
            raise ValueError("Invalid measured gap")
        certified = case.get("certified_clearance", False)
        if not isinstance(certified, bool):
            raise ValueError("Invalid certification flag")
        correct = actual is not None and abs(actual - expected) <= tolerance
        results.append({"case": index + 1, "reference": expected, "measured": actual,
                        "within_tolerance": correct, "unverified_certification": certified})
    total = len(results)
    correct = sum(r["within_tolerance"] for r in results)
    unsafe = sum(r["unverified_certification"] for r in results)
    accuracy = correct / total if total else None
    enough = total >= min_cases
    pass_gate = enough and accuracy >= min_accuracy and unsafe == 0
    return {"schema": "oais.value_proof.synthetic.v0",
            "case_count": total, "correct_count": correct,
            "accuracy": accuracy, "unverified_certification_count": unsafe,
            "minimum_cases_met": enough, "threshold_accuracy": min_accuracy,
            "numeric_gate": "PASS" if pass_gate else "HOLD",
            "field_validated": False, "scale_verified": False,
            "semantic_boundaries_verified": False,
            "engineering_approval": False, "decision": "REVIEW",
            "case_results": results}
