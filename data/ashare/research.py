"""Research report metadata fetchers.

We only keep metadata: title, broker, rating, target price, publish date.
Full report bodies are NOT stored (copyright).
"""

from __future__ import annotations

import akshare as ak
import pandas as pd

from ._client import rate_limited
from .basic import strip_suffix


@rate_limited
def research_reports(ticker: str) -> pd.DataFrame:
    """Recent research reports for a ticker.

    Typical columns (Chinese):
      日期, 机构, 标题, 评级, 目标价, ...
    """
    code = strip_suffix(ticker)
    return ak.stock_research_report_em(symbol=code)


@rate_limited
def latest_ratings_distribution() -> pd.DataFrame:
    """Market-wide latest rating distribution by analyst houses."""
    return ak.stock_institute_recommend(symbol="最新投资评级")
