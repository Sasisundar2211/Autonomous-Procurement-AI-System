from __future__ import annotations

import pandas as pd
from sklearn.ensemble import RandomForestRegressor

FEATURE_COLUMNS = ["price", "delivery_days", "reliability", "defect_rate"]


def _normalize(series: pd.Series) -> pd.Series:
    span = series.max() - series.min()
    if span == 0:
        return pd.Series([0.5] * len(series), index=series.index)
    return (series - series.min()) / span


def _derive_risk_score(df: pd.DataFrame) -> pd.Series:
    price_risk = _normalize(df["price"])
    delivery_risk = _normalize(df["delivery_days"])
    reliability_risk = 1 - df["reliability"].clip(0, 1)
    defect_risk = _normalize(df["defect_rate"])

    score = (
        0.35 * price_risk
        + 0.30 * delivery_risk
        + 0.20 * reliability_risk
        + 0.15 * defect_risk
    )
    return score.clip(0, 1)


def train_model(df: pd.DataFrame) -> RandomForestRegressor:
    training_df = df.copy()

    if "risk_score" not in training_df.columns:
        training_df["risk_score"] = _derive_risk_score(training_df)

    x_data = training_df[FEATURE_COLUMNS]
    y_data = training_df["risk_score"].clip(0, 1)

    model = RandomForestRegressor(n_estimators=200, random_state=42)
    model.fit(x_data, y_data)
    return model


def predict_risk(model: RandomForestRegressor, df: pd.DataFrame):
    x_data = df[FEATURE_COLUMNS]
    return model.predict(x_data).clip(0, 1)
