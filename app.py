# app.py
import streamlit as st

from domain import ModelOption
from data_examples import (
    INDUSTRIES,
    USE_CASES,
    MODEL_OPTIONS,
    EXAMPLES,
    BASELINE_METRICS,
)
from estimators import ScenarioLoad, scenario_summary
from evaluation import rubric_score


st.set_page_config(
    page_title="LLM Pilot Playbook Dashboard",
    layout="wide",
)


def main() -> None:
    st.title("LLM Pilot Playbook Dashboard")
    st.caption(
        "Pre-sales style dashboard to discuss LLM pilots by industry, use case, "
        "and model strategy. All numbers are illustrative."
    )

    col1, col2, col3 = st.columns([1.5, 1.5, 2])

    # ---------- Sidebar-style selectors ----------
    with col1:
        st.subheader("1. Choose Industry")
        industry_id = st.selectbox(
            "Industry",
            options=list(INDUSTRIES.keys()),
            format_func=lambda k: INDUSTRIES[k].name,
        )
        industry = INDUSTRIES[industry_id]
        st.write(industry.description)

    with col2:
        st.subheader("2. Choose Use Case")
        use_case_id = st.selectbox(
            "Use case",
            options=list(USE_CASES.keys()),
            format_func=lambda k: USE_CASES[k].name,
        )
        use_case = USE_CASES[use_case_id]
        st.markdown(f"**Pattern:** {use_case.pattern}")
        st.write(use_case.description)

        st.subheader("Pilot Load (for estimates)")
        req_per_day = st.slider(
            "Requests per day",
            min_value=100,
            max_value=10000,
            value=1000,
            step=100,
        )
        days = st.slider(
            "Pilot duration (days)",
            min_value=7,
            max_value=90,
            value=30,
            step=7,
        )
        load = ScenarioLoad(requests_per_day=req_per_day, days=days)

    # ---------- Example I/O and metrics ----------
    with col3:
        st.subheader("3. Example Input/Output")

        example_key = (industry_id, use_case_id)
        example = EXAMPLES.get(example_key)
        if example is None:
            st.info("No curated example yet for this combination.")
        else:
            st.markdown("**Example input (truncated):**")
            st.code(example["input"], language="text")

            st.markdown("**Example model output (ideal):**")
            st.code(example["output"], language="text")

    st.markdown("---")

    # ---------- Model comparison ----------
    st.subheader("Model Strategy Comparison")

    model_ids = list(MODEL_OPTIONS.keys())
    cols = st.columns(len(model_ids))

    for col, model_id in zip(cols, model_ids):
        model: ModelOption = MODEL_OPTIONS[model_id]
        summary = scenario_summary(model, load)

        with col:
            st.markdown(f"### {model.display_name}")
            st.caption(f"Provider type: {model.provider_type}")
            st.write(f"Avg tokens / request: ~{model.est_tokens_per_request}")
            st.write(f"Avg latency / request: {summary['avg_latency_s']:.2f} s")

            st.metric(
                "Pilot cost (USD)",
                f"${summary['est_cost_usd']:.2f}",
            )
            st.metric(
                "Total wallclock (if serialized)",
                f"{summary['total_wallclock_min']:.1f} min",
            )

    st.markdown("---")

    # ---------- Evaluation metrics ----------
    st.subheader("Evaluation Metrics (Illustrative)")

    metrics = BASELINE_METRICS.get(example_key)
    if metrics is None:
        st.info("No evaluation baseline yet for this combination.")
    else:
        score = rubric_score(metrics)
        col_m1, col_m2, col_m3, col_m4 = st.columns(4)

        with col_m1:
            st.metric(
                label="Groundedness",
                value=f"{metrics['groundedness'] * 100:.0f}%",
                help="How well the answer stays within known sources."
            )
        with col_m2:
            st.metric(
                label="Hallucination risk",
                value=f"{metrics['hallucination_risk'] * 100:.0f}%",
                help="Lower is better."
            )
        with col_m3:
            st.metric(
                label="Response quality",
                value=f"{metrics['response_quality'] * 100:.0f}%",
                help="Clarity, tone, completeness."
            )
        with col_m4:
            st.metric(
                label="Business readiness score",
                value=f"{score * 100:.0f} / 100",
                help="Composite heuristic combining all metrics."
            )

    st.markdown("---")
    st.caption(
        "Note: This dashboard is offline. In a real watsonx pilot, the same structure "
        "would be wired to actual evaluation runs and logs."
    )


if __name__ == "__main__":
    main()
