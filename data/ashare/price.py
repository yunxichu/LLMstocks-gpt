"""Stock price (quote) fetchers for individual A-shares."""

from __future__ import annotations

from datetime import date

import akshare as ak
import pandas as pd

from ._client import rate_limited
from .basic import strip_suffix


@rate_limited
def stock_daily(
    ticker: str,
    start: date | None = None,
    end: date | None = None,
    adjust: str = "qfq",
) -> pd.DataFrame:
    """Daily OHLCV for a single A-share.

    adjust: '' = unadjusted, 'qfq' = 前复权 (default), 'hfq' = 后复权.
    Columns: 日期, 股票代码, 开盘, 收盘, 最高, 最低, 成交量, 成交额, 振幅, 涨跌幅, 涨跌额, 换手率
    """
    code = strip_suffix(ticker)
    kwargs = {
        "symbol": code,
        "period": "daily",
        "adjust": adjust,
    }
    if start:
        kwargs["start_date"] = start.strftime("%Y%m%d")
    if end:
        kwargs["end_date"] = end.strftime("%Y%m%d")
    return ak.stock_zh_a_hist(**kwargs)


def stock_close_on(ticker: str, trade_date: date, adjust: str = "qfq") -> float:
    """Closing price of a stock on a specific trade date.

    Adjust mode notes:
      - For tracking forward-test returns, use 'qfq' (前复权) consistently so
        dividends / splits don't fake-drop the price.
    """
    df = stock_daily(ticker, start=trade_date, end=trade_date, adjust=adjust)
    if df is None or df.empty:
        raise ValueError(f"No price data for {ticker} on {trade_date}")
    df["日期"] = pd.to_datetime(df["日期"]).dt.date
    matched = df[df["日期"] == trade_date]
    if matched.empty:
        raise ValueError(f"No price data for {ticker} on {trade_date}")
    return float(matched["收盘"].iloc[0])
