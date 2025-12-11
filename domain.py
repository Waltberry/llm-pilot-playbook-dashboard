# domain.py
from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List


@dataclass(frozen=True)
class ModelOption:
    """Represents a logical model choice (not tied to any vendor)."""
    id: str
    display_name: str
    provider_type: str  # e.g. "open_source", "managed_api"
    est_tokens_per_request: int  # rough average
    est_latency_ms: int          # base latency per request
    est_cost_per_1k_tokens_usd: float  # hypothetical cost


@dataclass(frozen=True)
class UseCase:
    id: str
    name: str
    pattern: str  # "RAG", "Summarization", "Classification"
    description: str


@dataclass(frozen=True)
class Industry:
    id: str
    name: str
    description: str


@dataclass(frozen=True)
class PilotScenario:
    """A specific combo: Industry + Use case."""
    industry: Industry
    use_case: UseCase
    supported_models: List[ModelOption]
