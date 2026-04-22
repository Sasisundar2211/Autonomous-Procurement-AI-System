from __future__ import annotations

from datetime import datetime, timezone

import requests

LOCATION_RISK_MAP = {
    "US": 0.18,
    "IN": 0.22,
    "DE": 0.12,
    "CN": 0.33,
    "BR": 0.29,
}


def fetch_currency_rate(base: str = "USD", quote: str = "INR") -> float:
    try:
        response = requests.get(f"https://open.er-api.com/v6/latest/{base}", timeout=8)
        response.raise_for_status()
        data = response.json()
        rates = data.get("rates", {})
        rate = rates.get(quote)
        if rate is None:
            raise ValueError(f"Rate for {quote} not available")
        return float(rate)
    except Exception:  # noqa: BLE001
        # Fallback keeps pipeline stable when external API is unavailable.
        return 83.0


def supplier_location_risk(vendor_country: str | None) -> float:
    if not vendor_country:
        return 0.25
    return LOCATION_RISK_MAP.get(vendor_country.strip().upper(), 0.30)


def market_signal(vendor_name: str) -> str:
    bucket = sum(ord(c) for c in str(vendor_name)) % 3
    if bucket == 0:
        return "Market stable"
    if bucket == 1:
        return "Moderate supplier price pressure"
    return "High supplier price pressure"


def collect_external_signals(vendor_name: str, vendor_country: str | None) -> dict:
    return {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "usd_inr_rate": fetch_currency_rate("USD", "INR"),
        "location_risk": supplier_location_risk(vendor_country),
        "market_signal": market_signal(vendor_name),
    }
