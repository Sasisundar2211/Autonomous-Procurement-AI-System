# src/agents/price_detector.py
import pandas as pd
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from sqlalchemy import create_engine, inspect, text
from src.tools.llm_client import summarize_drift_with_gemini

# Use the same database URL as the ingestor, with a fallback
db_url = os.getenv("DATABASE_URL", "sqlite:///data/procure.db")
engine = create_engine(db_url)

_EXPECTED_COLS = ['po_id', 'vendor_id', 'item_id', 'unit_price', 'qty', 'total', 'date',
                  'contract_id', 'contract_unit_price', 'price_drift', 'gemini_summary']

def _empty_result():
    return pd.DataFrame(columns=_EXPECTED_COLS)

def detect_public_only(drift_threshold: float | None = None):
    """
    Detects price drifts in public data.
    
    A "drift" is when a purchase order's unit price is significantly higher than
    the agreed-upon price in the contract.
    """
    if drift_threshold is None:
        drift_threshold = 1.05
    else:
        drift_threshold = 1 + (drift_threshold / 100.0)

    inspector = inspect(engine)
    if not inspector.has_table("pos") or not inspector.has_table("contracts"):
        print("Database tables not found. Please run the ingestor first.")
        return _empty_result()

    # Perform the JOIN and drift calculation directly in SQL to avoid loading
    # full tables into Python memory and doing a pandas merge.
    sql = text("""
        SELECT
            p.*,
            c.contract_unit_price,
            CAST(p.unit_price AS REAL) / c.contract_unit_price AS price_drift
        FROM pos p
        INNER JOIN contracts c ON CAST(p.contract_id AS TEXT) = CAST(c.contract_id AS TEXT)
        WHERE c.contract_unit_price > 0
          AND CAST(p.unit_price AS REAL) / c.contract_unit_price > :threshold
        ORDER BY price_drift DESC
    """)

    try:
        with engine.connect() as conn:
            drifts = pd.read_sql(sql, conn, params={"threshold": drift_threshold})
    except Exception as e:
        print(f"Error reading from database: {e}")
        return _empty_result()

    if drifts.empty:
        return _empty_result()

    # Add Gemini summary column, defaulting to static message
    drifts['gemini_summary'] = "Drift detected (AI summary skipped for speed)"

    # Summarize only the top 5 drifts; run API calls in parallel to reduce latency
    top_indices = list(drifts.index[:5])

    def _summarize(idx):
        row = drifts.loc[idx]
        return idx, summarize_drift_with_gemini(row['contract_unit_price'], row['unit_price'])

    with ThreadPoolExecutor(max_workers=min(5, len(top_indices))) as executor:
        futures = {executor.submit(_summarize, idx): idx for idx in top_indices}
        for future in as_completed(futures):
            idx, summary = future.result()
            drifts.at[idx, 'gemini_summary'] = summary

    # Add any expected columns that are absent (keeps the schema stable)
    for col in _EXPECTED_COLS:
        if col not in drifts.columns:
            drifts[col] = None

    # Replace NaN/Inf with None for JSON serialization
    drifts = drifts.replace([float('inf'), float('-inf')], None)
    drifts = drifts.where(pd.notnull(drifts), None)

    return drifts[_EXPECTED_COLS]

def evaluate_with_private_labels():
    # ... (not implemented for now)
    pass