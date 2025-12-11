# tests/test_estimators.py
from estimators import ScenarioLoad, estimate_cost_usd, estimate_total_wallclock_minutes
from data_examples import MODEL_OPTIONS


def test_scenario_load_total_requests():
    load = ScenarioLoad(requests_per_day=100, days=10)
    assert load.total_requests == 1000


def test_cost_zero_for_free_model():
    model = MODEL_OPTIONS["oss_small"]
    load = ScenarioLoad(requests_per_day=1000, days=30)
    cost = estimate_cost_usd(model, load)
    assert cost == 0.0


def test_cost_scales_with_requests():
    model = MODEL_OPTIONS["managed_premium"]
    load_small = ScenarioLoad(requests_per_day=100, days=1)
    load_large = ScenarioLoad(requests_per_day=1000, days=10)

    cost_small = estimate_cost_usd(model, load_small)
    cost_large = estimate_cost_usd(model, load_large)

    assert cost_large > cost_small
    assert cost_large >= 10 * cost_small  # rough monotonic sanity check


def test_wallclock_positive():
    model = MODEL_OPTIONS["oss_medium"]
    load = ScenarioLoad(requests_per_day=500, days=2)
    minutes = estimate_total_wallclock_minutes(model, load)
    assert minutes > 0
