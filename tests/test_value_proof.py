import pytest
from oais_cad.clearance_geometry import parallel_segment_gap
from oais_cad.value_proof import assess_reference_cases


def _cases(n=30):
    cases = []
    for i in range(n):
        expected = 10 + i
        gate = parallel_segment_gap((0, 0, 100, 0), (10, expected, 90, expected))
        cases.append({"expected_gap_page_units": expected,
                      "actual_gap_page_units": gate["gap_page_units"],
                      "certified_clearance": gate["certified_clearance"]})
    return cases


def test_thirty_independent_synthetic_reference_values():
    result = assess_reference_cases(_cases())
    assert result["case_count"] == 30
    assert result["correct_count"] == 30
    assert result["accuracy"] == 1.0
    assert result["numeric_gate"] == "PASS"
    assert result["engineering_approval"] is False
    assert result["field_validated"] is False


def test_fails_closed_for_unverified_certification():
    cases = _cases()
    cases[0]["certified_clearance"] = True
    result = assess_reference_cases(cases)
    assert result["numeric_gate"] == "HOLD"
    assert result["unverified_certification_count"] == 1


def test_missing_case_or_wrong_gap_blocks():
    cases = _cases(29)
    assert assess_reference_cases(cases)["numeric_gate"] == "HOLD"
    cases = _cases()
    cases[0]["actual_gap_page_units"] = 999
    cases[1]["actual_gap_page_units"] = None
    assert assess_reference_cases(cases)["numeric_gate"] == "HOLD"


@pytest.mark.parametrize("case",[
    {"expected_gap_page_units": float("nan"), "actual_gap_page_units": 1},
    {"expected_gap_page_units": 1, "actual_gap_page_units": float("inf")},
    {"expected_gap_page_units": True, "actual_gap_page_units": 1},
])
def test_invalid_evidence_rejected(case):
    with pytest.raises(ValueError):
        assess_reference_cases([case])


def test_empty_evidence_is_hold():
    result = assess_reference_cases([])
    assert result["numeric_gate"] == "HOLD"
    assert result["accuracy"] is None
