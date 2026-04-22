import pandas as pd

REQUIRED_COLUMNS = ["vendor", "price", "delivery_days", "reliability", "defect_rate"]
NUMERIC_COLUMNS = ["price", "delivery_days", "reliability", "defect_rate"]


def preprocess_vendor_data(df: pd.DataFrame) -> pd.DataFrame:
    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {', '.join(missing)}")

    cleaned = df[REQUIRED_COLUMNS].copy()

    for col in NUMERIC_COLUMNS:
        cleaned[col] = pd.to_numeric(cleaned[col], errors="coerce")

    cleaned = cleaned.dropna(subset=REQUIRED_COLUMNS)

    if cleaned.empty:
        raise ValueError("No valid rows after preprocessing")

    return cleaned
