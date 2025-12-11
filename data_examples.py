# data_examples.py
from __future__ import annotations
from typing import Dict, Tuple
from domain import Industry, UseCase, ModelOption, PilotScenario

# ---------- Industries ----------
INDUSTRIES: Dict[str, Industry] = {
    "banking": Industry(
        id="banking",
        name="Banking",
        description="Retail and SME banking: credit, fraud, customer support, compliance."
    ),
    "telco": Industry(
        id="telco",
        name="Telecommunications",
        description="Network operations, billing, churn, and customer support."
    ),
    "healthcare": Industry(
        id="healthcare",
        name="Healthcare",
        description="Clinics, hospitals, and insurance: triage, documentation, and admin."
    ),
}

# ---------- Use Cases ----------
USE_CASES: Dict[str, UseCase] = {
    "call_summarization": UseCase(
        id="call_summarization",
        name="Call Summarization",
        pattern="Summarization",
        description="Turn long customer support calls into concise summaries and action items."
    ),
    "faq_qa": UseCase(
        id="faq_qa",
        name="FAQ / Policy Q&A",
        pattern="RAG",
        description="Answer questions grounded in internal policies and FAQs."
    ),
    "ticket_classification": UseCase(
        id="ticket_classification",
        name="Ticket Classification",
        pattern="Classification",
        description="Route tickets to the right team based on intent and urgency."
    ),
}

# ---------- Model Options ----------
MODEL_OPTIONS: Dict[str, ModelOption] = {
    "oss_medium": ModelOption(
        id="oss_medium",
        display_name="Open-source LLM (Medium, self-hosted)",
        provider_type="open_source",
        est_tokens_per_request=1200,
        est_latency_ms=800,
        est_cost_per_1k_tokens_usd=0.0,  # cost handled as infra, not tokens
    ),
    "oss_small": ModelOption(
        id="oss_small",
        display_name="Open-source LLM (Small, self-hosted)",
        provider_type="open_source",
        est_tokens_per_request=600,
        est_latency_ms=350,
        est_cost_per_1k_tokens_usd=0.0,
    ),
    "managed_premium": ModelOption(
        id="managed_premium",
        display_name="Managed LLM API (Premium)",
        provider_type="managed_api",
        est_tokens_per_request=1500,
        est_latency_ms=700,
        est_cost_per_1k_tokens_usd=5.0,  # purely illustrative
    ),
}

# ---------- Example Inputs/Outputs per (industry, use_case) ----------
ExampleKey = Tuple[str, str]  # (industry_id, use_case_id)

EXAMPLES: Dict[ExampleKey, Dict[str, str]] = {
    ("banking", "call_summarization"): {
        "input": (
            "Customer: I'm calling because my credit card was declined at a grocery store, "
            "even though I paid my balance yesterday...\n\n"
            "Agent: I see, let me check your account. There was a fraud hold triggered..."
        ),
        "output": (
            "Summary: Customer's credit card was declined after a fraud rule triggered. "
            "Agent verified recent payment and removed the fraud hold.\n\n"
            "Next steps: Send confirmation email, monitor for further declines in next 48 hours."
        ),
    },
    ("telco", "faq_qa"): {
        "input": (
            "Question: What is the penalty if I cancel my fibre contract before 12 months?"
        ),
        "output": (
            "Answer: Based on the current policy, early termination within the first 12 months "
            "incurs a fee equal to one month of service plus any equipment balance."
        ),
    },
    ("healthcare", "ticket_classification"): {
        "input": (
            "Message: I need to reschedule my appointment from tomorrow to next week, "
            "and I also want to ask if my insurance covers the lab tests."
        ),
        "output": (
            "Intent: Scheduling + Insurance coverage\n"
            "Routing: Front-desk scheduling + Billing team\n"
            "Priority: Medium"
        ),
    },
}

# ---------- Baseline evaluation metrics (mocked) ----------
# Simplified scores on 0–1 scale
BASELINE_METRICS: Dict[ExampleKey, Dict[str, float]] = {
    ("banking", "call_summarization"): {
        "groundedness": 0.95,
        "hallucination_risk": 0.10,
        "response_quality": 0.90,
    },
    ("telco", "faq_qa"): {
        "groundedness": 0.90,
        "hallucination_risk": 0.15,
        "response_quality": 0.88,
    },
    ("healthcare", "ticket_classification"): {
        "groundedness": 0.92,
        "hallucination_risk": 0.12,
        "response_quality": 0.89,
    },
}
