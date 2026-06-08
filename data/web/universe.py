"""A-share investable universe construction.

yfinance does NOT have a "list all A-shares" API. We bootstrap the universe
from a static seed CSV (committed to the repo) and enrich it lazily via
yfinance.

The seed list is intended to be a one-time pull from a public source and
checked in. To refresh the seed (e.g., when new IPOs land), edit
`config/a_share_seed.csv` manually or replace with a fresh pull.

Note: this layer is for V1 (the curated investable universe ~1500-3000 names).
A fully complete A-share universe (~5000+) would require an unofficial seed
source or a one-time AKShare pull from a China-located machine.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent.parent  # E:\LLMstocks
SEED_CSV = ROOT / "config" / "a_share_seed.csv"


def load_seed() -> pd.DataFrame:
    """Load the committed seed list of A-share tickers.

    Expected columns: ticker, name, market_segment.
    If the seed file is missing, raise with a clear instruction.
    """
    if not SEED_CSV.exists():
        raise FileNotFoundError(
            f"Seed file not found: {SEED_CSV}\n"
            f"Bootstrap it once from a public source. Options:\n"
            f"  1. Pull from a China-located machine: \n"
            f"       python -c \"import akshare as ak; "
            f"ak.stock_info_a_code_name().to_csv('{SEED_CSV}', index=False)\"\n"
            f"  2. Use a public GitHub mirror of A-share ticker lists\n"
            f"     (e.g., search 'a-share ticker list csv' on GitHub)\n"
            f"  3. Manually curate a watchlist of ~50-200 names you actually care about\n"
            f"     — for personal research this is often enough."
        )
    return pd.read_csv(SEED_CSV, encoding="utf-8-sig")
