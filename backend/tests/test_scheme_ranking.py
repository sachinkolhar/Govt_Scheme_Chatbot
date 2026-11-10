import pandas as pd

from backend.search.ranking import rank_candidates


def test_existing_checker_is_used_without_claiming_definite_eligibility():
    row = pd.Series({"scheme_name": "Age Scheme", "eligibility": "Applicants aged 18 to 30 years may apply.", "tags": ""})
    assert rank_candidates([(row, 0.1)], {"age": 24})[0].eligibility_status == "POSSIBLY_ELIGIBLE"
    assert rank_candidates([(row, 0.1)], {"age": 35}, query="Age Scheme", scheme_names=["Age Scheme"])[0].eligibility_status == "NOT_ELIGIBLE"


def test_missing_profile_data_is_insufficient_not_ineligible():
    row = pd.Series({"scheme_name": "Age Scheme", "eligibility": "Applicants aged 18 to 30 years may apply."})
    result = rank_candidates([(row, 0.1)], {})[0]
    assert result.eligibility_status == "INSUFFICIENT_INFORMATION"
    assert result.missing_information == ["age"]


def test_broad_results_return_top_three_and_explicit_name_is_prioritized():
    rows = [(pd.Series({"scheme_name": f"Scheme {i}", "eligibility": ""}), float(i)) for i in range(5, 0, -1)]
    assert len(rank_candidates(rows, query="farmer schemes")) == 3
    ranked = rank_candidates(rows, query="Tell me Scheme 5", scheme_names=["Scheme 5"])
    assert ranked[0].scheme["scheme_name"] == "Scheme 5"
    assert ranked[0].to_dict()["eligibility_status"] == "INSUFFICIENT_INFORMATION"
