import pandas as pd


def normalize(series: pd.Series) -> pd.Series:
    span = series.max() - series.min()
    if span == 0:
        return pd.Series([1.0] * len(series), index=series.index)
    return (series - series.min()) / span


def rank_vendors(df: pd.DataFrame) -> pd.DataFrame:
    ranked = df.copy()

    ranked["price_score"] = 1 - normalize(ranked["price"])
    ranked["delivery_score"] = 1 - normalize(ranked["delivery_days"])
    ranked["reliability_score"] = ranked["reliability"]
    ranked["defect_score"] = 1 - ranked["defect_rate"]

    ranked["final_score"] = (
        0.4 * ranked["price_score"]
        + 0.3 * ranked["delivery_score"]
        + 0.2 * ranked["reliability_score"]
        + 0.1 * ranked["defect_score"]
    )

    return ranked.sort_values(by="final_score", ascending=False).reset_index(drop=True)
