#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.services.vendor_ranking_service import (
    VendorRankingError,
    parse_weight_spec,
    rank_vendors_from_csv,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Rank vendors using weighted scoring from a CSV input.",
    )
    parser.add_argument("input_csv", help="Path to input vendor CSV")
    parser.add_argument(
        "-o",
        "--output",
        default="ranked_vendors.csv",
        help="Path to output ranked CSV (default: ranked_vendors.csv)",
    )
    parser.add_argument(
        "--vendor-column",
        default="vendor_id",
        help="Vendor identifier column name (default: vendor_id)",
    )
    parser.add_argument(
        "--weights",
        default=None,
        help=(
            "Comma-separated metric weights, e.g. "
            "'unit_price:-0.5,on_time_rate:0.3,quality_score:0.2'. "
            "Negative weight means lower metric values rank better."
        ),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        weights = parse_weight_spec(args.weights)
        ranked = rank_vendors_from_csv(
            csv_path=args.input_csv,
            vendor_column=args.vendor_column,
            weights=weights,
        )
    except VendorRankingError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    ranked.to_csv(args.output, index=False)
    print(f"Ranked {len(ranked)} vendors -> {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
