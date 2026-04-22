from __future__ import annotations

from datetime import datetime, timezone

import pandas as pd

from app.services.external_signals import collect_external_signals
from app.services.llm import generate_explanation
from app.services.memory import get_history, store_decision
from app.services.negotiation import negotiation_strategy
from app.services.risk_model import predict_risk, train_model
from app.services.scoring import rank_vendors
from app.utils.preprocess import preprocess_vendor_data


def run_pipeline(df: pd.DataFrame) -> dict:
    # Data Agent
    cleaned = preprocess_vendor_data(df)

    # Risk Agent
    model = train_model(cleaned)
    risk_scores = predict_risk(model, cleaned)

    # Decision Agent
    ranked = rank_vendors(cleaned, risk_scores)
    top = ranked.iloc[0]

    # LLM Agent
    explanation = generate_explanation(str(top["vendor"]), top)

    # Negotiation Agent
    negotiation = negotiation_strategy(top)

    external_signals = collect_external_signals(
        vendor_name=str(top["vendor"]),
        vendor_country=top.get("vendor_country") if "vendor_country" in ranked.columns else None,
    )

    decision = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "top_vendor": str(top["vendor"]),
        "top_score": float(top["final_score"]),
        "risk_score": float(top["risk_score"]),
        "negotiation": negotiation,
    }
    store_decision(decision)

    risk_summary = {
        "average_risk": float(ranked["risk_score"].mean()),
        "max_risk": float(ranked["risk_score"].max()),
        "min_risk": float(ranked["risk_score"].min()),
    }

    decision_summary = {
        "pipeline_steps": [
            "Data Agent: validated and cleaned vendor data",
            "Risk Agent: predicted vendor risk using RandomForest",
            "Decision Agent: computed weighted multi-step score",
            "LLM Agent: generated business explanation",
            "Negotiation Agent: generated action recommendation",
        ],
        "selected_vendor": str(top["vendor"]),
        "selected_score": float(top["final_score"]),
        "selected_risk": float(top["risk_score"]),
    }

    return {
        "top_vendor": str(top["vendor"]),
        "ranking": ranked.to_dict(orient="records"),
        "explanation": explanation,
        "negotiation": negotiation,
        "external_signals": external_signals,
        "risk_summary": risk_summary,
        "decision_summary": decision_summary,
        "history": get_history(),
    }
