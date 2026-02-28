# src/agents/price_detector.py
import pandas as pd
import os
from sqlalchemy import create_engine, inspect
from src.tools.llm_client import summarize_drift_with_gemini

# Use the same database URL as the ingestor, with a fallback
db_url = os.getenv("DATABASE_URL", "sqlite:///data/procure.db")
engine = create_engine(db_url)

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
        # Return an empty dataframe with the expected columns
        return pd.DataFrame(columns=['po_id', 'vendor_id', 'item_id', 'unit_price', 'qty', 'total', 'date', 'contract_id', 'contract_unit_price', 'price_drift', 'gemini_summary'])

    try:
        # Push the JOIN and contract filter to the database so only matched rows
        # are transferred to Python, instead of loading both full tables.
        join_sql = """
            SELECT p.*, c.contract_unit_price
            FROM pos p
            JOIN contracts c ON CAST(p.contract_id AS TEXT) = c.contract_id
            WHERE c.contract_unit_price IS NOT NULL
        """
        contracted_pos = pd.read_sql(join_sql, engine)
    except Exception as e:
        print(f"Error reading from database: {e}")
        return pd.DataFrame(columns=['po_id', 'vendor_id', 'item_id', 'unit_price', 'qty', 'total', 'date', 'contract_id', 'contract_unit_price', 'price_drift', 'gemini_summary'])

    if contracted_pos.empty:
        print("No POs with matching contracts found.")
        return pd.DataFrame(columns=['po_id', 'vendor_id', 'item_id', 'unit_price', 'qty', 'total', 'date', 'contract_id', 'contract_unit_price', 'price_drift', 'gemini_summary'])

    # Detect price drift
    contracted_pos['price_drift'] = contracted_pos['unit_price'] / contracted_pos['contract_unit_price']
    
    drifts = contracted_pos[contracted_pos['price_drift'] > drift_threshold].copy()
    
    # Add Gemini summary - OPTIMIZED: Only summarize top 5 to prevent timeout
    drifts.sort_values('price_drift', ascending=False, inplace=True)
    
    # Initialize with None
    drifts['gemini_summary'] = None
    
    # Take top 5 for AI summary
    top_5_indices = drifts.index[:5]
    
    # Apply Gemini only to top 5
    for idx in top_5_indices:
        row = drifts.loc[idx]
        drifts.at[idx, 'gemini_summary'] = summarize_drift_with_gemini(row['contract_unit_price'], row['unit_price'])
        
    # Fill the rest with a static message
    drifts['gemini_summary'] = drifts['gemini_summary'].fillna("Drift detected (AI summary skipped for speed)")

    # Ensure we return the columns the frontend expects
    cols_to_keep = ['po_id', 'vendor_id', 'item_id', 'unit_price', 'qty', 'total', 'date', 'contract_id', 'contract_unit_price', 'price_drift', 'gemini_summary']
    
    # Add missing columns with default values if they don't exist
    for col in cols_to_keep:
        if col not in drifts.columns:
            drifts[col] = None

    # Replace NaN/Inf with None for JSON serialization
    drifts = drifts.replace([float('inf'), float('-inf')], None)
    drifts = drifts.where(pd.notnull(drifts), None)

    return drifts[cols_to_keep]

def evaluate_with_private_labels():
    # ... (not implemented for now)
    pass