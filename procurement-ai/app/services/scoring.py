from __future__ import annotations

import pandas as pd


def normalize(series: pd.Series) -> pd.Series:
    span = series.max() - series.min()
    if span == 0:
        return pd.Series([0.5] * len(series), index=series.index)
    return (series - series.min()) / span


def rank_vendors(df: pd.DataFrame, risk_scores) -> pd.DataFrame:
    ranked = df.copy().reset_index(drop=True)
    ranked["risk_score"] = pd.Series(risk_scores).clip(0, 1)

    ranked["price_n"] = normalize(ranked["price"])
    ranked["delivery_n"] = normalize(ranked["delivery_days"])
    ranked["defect_n"] = normalize(ranked["defect_rate"])

    ranked["final_score"] = (
        0.3 * (1 - ranked["price_n"])
        + 0.2 * (1 - ranked["delivery_n"])
        + 0.2 * ranked["reliability"].clip(0, 1)
        + 0.1 * (1 - ranked["defect_n"])
        + 0.2 * (1 - ranked["risk_score"])
    )

    ranked["decision_band"] = pd.cut(
        ranked["final_score"],
        bins=[-1, 0.45, 0.7, 1.1],
        labels=["Low", "Medium", "High"],
    )

    return ranked.sort_values(by="final_score", ascending=False).reset_index(drop=True)
