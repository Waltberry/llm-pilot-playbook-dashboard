# estimators.py
from __future__ import annotations
from dataclasses import dataclass
from typing import Dict

from domain import ModelOption


@dataclass(frozen=True)
class ScenarioLoad:
    """Represents a simple load profile for a pilot."""
    requests_per_day: int
    days: int

    @property
    def total_requests(self) -> int:
        return self.requests_per_day * self.days


def estimate_cost_usd(
    model: ModelOption,
    load: ScenarioLoad,
) -> float:
    """
    Estimate token-based cost for a given model and load.
    cost = (total_tokens / 1000) * cost_per_1k_tokens
    """
    total_tokens = load.total_requests * model.est_tokens_per_request
    return (total_tokens / 1000.0) * model.est_cost_per_1k_tokens_usd


def estimate_latency_seconds_per_request(model: ModelOption) -> float:
    """Return base latency in seconds."""
    return model.est_latency_ms / 1000.0


def estimate_total_wallclock_minutes(model: ModelOption, load: ScenarioLoad) -> float:
    """
    Naive upper bound: all requests are serialized.
    For a more realistic scenario, you can divide by an assumed concurrency factor.
    """
    total_seconds = estimate_latency_seconds_per_request(model) * load.total_requests
    return total_seconds / 60.0


def scenario_summary(model: ModelOption, load: ScenarioLoad) -> Dict[str, float]:
    """Bundle common metrics for UI consumption."""
    cost = estimate_cost_usd(model, load)
    latency = estimate_latency_seconds_per_request(model)
    wallclock = estimate_total_wallclock_minutes(model, load)
    return {
        "total_requests": load.total_requests,
        "avg_latency_s": latency,
        "total_wallclock_min": wallclock,
        "est_cost_usd": cost,
    }
