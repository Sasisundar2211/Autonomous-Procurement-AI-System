import pandas as pd
import pytest

from src.services.vendor_ranking_service import (
    VendorRankingError,
    parse_weight_spec,
    rank_vendors,
)


def test_rank_vendors_with_weight_direction():
    df = pd.DataFrame(
        [
            {"vendor_id": "A", "unit_price": 90, "quality_score": 80, "on_time_rate": 95},
            {"vendor_id": "A", "unit_price": 90, "quality_score": 80, "on_time_rate": 95},
            {"vendor_id": "B", "unit_price": 110, "quality_score": 95, "on_time_rate": 90},
        ]
    )

    ranked = rank_vendors(
        df,
        weights={"unit_price": -0.5, "quality_score": 0.3, "on_time_rate": 0.2},
    )

    assert ranked.iloc[0]["vendor_id"] == "A"
    assert ranked.iloc[0]["rank"] == 1
    assert ranked.iloc[1]["vendor_id"] == "B"
    assert ranked.iloc[1]["rank"] == 2


def test_parse_weight_spec_validation():
    with pytest.raises(VendorRankingError):
        parse_weight_spec("unit_price")

    with pytest.raises(VendorRankingError):
        parse_weight_spec("unit_price:foo")


def test_rank_vendors_requires_vendor_column():
    df = pd.DataFrame([{"supplier": "A", "unit_price": 100}])
    with pytest.raises(VendorRankingError):
        rank_vendors(df, vendor_column="vendor_id")
