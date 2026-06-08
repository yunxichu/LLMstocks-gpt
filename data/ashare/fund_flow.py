"""Main-force fund flow data."""

from __future__ import annotations

import akshare as ak
import pandas as pd

from ._client import rate_limited
from .basic import strip_suffix


def _market_suffix(ticker: str) -> str:
    """Return 'sh' or 'sz' for AKShare's `market` argument."""
    suffix = ticker.split(".")[-1].lower()
    if suffix == "sh":
        return "sh"
    if suffix == "sz":
        return "sz"
    if suffix == "bj":
        return "bj"
    raise ValueError(f"Cannot determine market from ticker: {ticker}")


@rate_limited
def stock_fund_flow(ticker: str) -> pd.DataFrame:
    """Daily main-force fund flow for a single stock.

    Columns include (Chinese):
      日期, 收盘价, 涨跌幅,
      主力净流入-净额, 主力净流入-净占比,
      超大单净流入-净额, 超大单净流入-净占比,
      大单净流入-净额, 大单净流入-净占比,
      中单净流入-净额, 中单净流入-净占比,
      小单净流入-净额, 小单净流入-净占比
    """
    code = strip_suffix(ticker)
    market = _market_suffix(ticker)
    return ak.stock_individual_fund_flow(stock=code, market=market)


@rate_limited
def sector_fund_flow() -> pd.DataFrame:
    """Today's sector-level fund flow ranking (concept / industry)."""
    return ak.stock_sector_fund_flow_rank()


@rate_limited
def market_fund_flow() -> pd.DataFrame:
    """Whole-market fund flow daily series."""
    return ak.stock_market_fund_flow()
