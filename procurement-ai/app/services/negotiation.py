from __future__ import annotations

import pandas as pd


def negotiation_strategy(row: pd.Series) -> str:
    suggestions: list[str] = []

    if float(row.get("price", 0)) > 1000:
        suggestions.append("Request 10% discount")
    if float(row.get("delivery_days", 0)) > 7:
        suggestions.append("Add delay penalty clause")
    if float(row.get("risk_score", 0)) > 0.6:
        suggestions.append("Add performance guarantee with milestone-based payments")

    if not suggestions:
        return "Accept current terms"

    return "; ".join(suggestions)
