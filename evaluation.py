# evaluation.py
from __future__ import annotations
from typing import Dict


def normalize_score(score: float) -> float:
    """Clamp a score to [0,1]."""
    return max(0.0, min(1.0, score))


def rubric_score(metrics: Dict[str, float]) -> float:
    """
    Combine metrics into a single 0–1 "business readiness" score.

    Heuristic:
      - +0.6 * groundedness
      - +0.3 * response_quality
      - -0.3 * hallucination_risk
    Then clamp to [0,1].
    """
    groundedness = metrics.get("groundedness", 0.0)
    response_quality = metrics.get("response_quality", 0.0)
    hallucination_risk = metrics.get("hallucination_risk", 0.0)

    raw = (
        0.6 * groundedness
        + 0.3 * response_quality
        - 0.3 * hallucination_risk
    )
    return normalize_score(raw)
