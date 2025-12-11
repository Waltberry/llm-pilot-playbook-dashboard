# tests/test_evaluation.py
from evaluation import normalize_score, rubric_score


def test_normalize_score_clamps_values():
    assert normalize_score(-0.5) == 0.0
    assert normalize_score(0.5) == 0.5
    assert normalize_score(1.5) == 1.0


def test_rubric_score_in_0_1_range():
    metrics = {
        "groundedness": 0.9,
        "response_quality": 0.8,
        "hallucination_risk": 0.1,
    }
    score = rubric_score(metrics)
    assert 0.0 <= score <= 1.0


def test_rubric_penalizes_hallucinations():
    base = {
        "groundedness": 0.9,
        "response_quality": 0.9,
        "hallucination_risk": 0.1,
    }
    worse = dict(base)
    worse["hallucination_risk"] = 0.5

    base_score = rubric_score(base)
    worse_score = rubric_score(worse)
    assert worse_score < base_score
