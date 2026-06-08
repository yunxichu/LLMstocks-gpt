"""Dragon-tiger list (龙虎榜) data fetchers."""

from __future__ import annotations

from datetime import date

import akshare as ak
import pandas as pd

from ._client import rate_limited
from .basic import strip_suffix


@rate_limited
def lhb_daily(trade_date: date) -> pd.DataFrame:
    """Daily LHB detail for a single trade date.

    Columns include (Chinese):
      代码, 名称, 上榜日, 解读, 收盘价, 涨跌幅, 龙虎榜净买额, 龙虎榜买入额, 龙虎榜卖出额,
      龙虎榜成交额, 市场总成交额, 净买额占总成交比, 上榜原因 ...

    Use `lhb_seats(trade_date, ticker)` for per-stock buyer/seller seats.
    """
    date_str = trade_date.strftime("%Y%m%d")
    return ak.stock_lhb_detail_em(start_date=date_str, end_date=date_str)


@rate_limited
def lhb_range(start: date, end: date) -> pd.DataFrame:
    """LHB detail across a date range."""
    return ak.stock_lhb_detail_em(
        start_date=start.strftime("%Y%m%d"),
        end_date=end.strftime("%Y%m%d"),
    )


@rate_limited
def lhb_history_for_ticker(ticker: str, start: date, end: date) -> pd.DataFrame:
    """Single stock's LHB history within a date range."""
    df = lhb_range(start, end)
    if df is None or df.empty:
        return pd.DataFrame()
    code = strip_suffix(ticker)
    code_col = next((c for c in ("代码", "股票代码", "code") if c in df.columns), None)
    if not code_col:
        return df  # let caller inspect
    return df[df[code_col].astype(str).str.zfill(6) == code]


@rate_limited
def lhb_seats_buy_sell(trade_date: date, ticker: str) -> pd.DataFrame:
    """Buyer / seller seat detail for a specific stock on a specific date.

    Returns the raw EastMoney seat table. Inspect columns at runtime; typical
    fields include 营业部名称, 买入金额, 卖出金额, 净额, etc.
    """
    date_str = trade_date.strftime("%Y%m%d")
    code = strip_suffix(ticker)
    return ak.stock_lhb_stock_detail_em(symbol=code, date=date_str, flag="买入")
