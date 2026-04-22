from typing import Any

from pydantic import BaseModel


class AnalyzeResponse(BaseModel):
    top_vendor: str
    ranking: list[dict[str, Any]]
    explanation: str
    negotiation: str
    external_signals: dict[str, Any]
    risk_summary: dict[str, float]
    decision_summary: dict[str, Any]
    history: list[dict[str, Any]]
