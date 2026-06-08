"""A-share data via yfinance (works from outside Mainland China).

Ticker convention:
  Our standard:  '600519.SH' (上交所), '000001.SZ' (深交所)
  yfinance:      '600519.SS', '000001.SZ'
  Note: yfinance does NOT support 北交所 ('.BJ'). Filter those out.
"""

from __future__ import annotations

from datetime import date, timedelta

import pandas as pd
import yfinance as yf

from .yf_client import rate_limited


def to_yf(ticker: str) -> str:
    """'600519.SH' -> '600519.SS'; '000001.SZ' stays."""
    code, suffix = ticker.split(".")
    s = suffix.upper()
    if s == "SH":
        return f"{code}.SS"
    if s == "SZ":
        return f"{code}.SZ"
    if s == "BJ":
        raise ValueError(
            f"北交所 {ticker} 暂不支持（yfinance 不覆盖）。"
            f"如需关注 BJ 股，等到 V2 配境内数据源。"
        )
    raise ValueError(f"Unknown suffix in ticker: {ticker}")


def from_yf(yf_ticker: str) -> str:
    """'600519.SS' -> '600519.SH'."""
    code, suffix = yf_ticker.split(".")
    s = suffix.upper()
    if s == "SS":
        return f"{code}.SH"
    if s == "SZ":
        return f"{code}.SZ"
    return yf_ticker


def market_segment(ticker: str) -> str:
    code = ticker.split(".")[0]
    if code.startswith("60"):
        return "sh_main"
    if code.startswith("68"):
        return "star"
    if code.startswith("30"):
        return "chinext"
    if code.startswith("00"):
        return "sz_main"
    if code.startswith(("4", "8")):
        return "bj_se"
    return "unknown"


@rate_limited
def stock_info(ticker: str) -> dict:
    """Basic info: shortName, sector, industry, marketCap, trailingPE,
    priceToBook, currency, country, longBusinessSummary, etc.

    Returns a dict; missing keys default to None when accessed.
    """
    return yf.Ticker(to_yf(ticker)).info


@rate_limited
def stock_history(
    ticker: str,
    period: str = "1y",
    interval: str = "1d",
    auto_adjust: bool = True,
) -> pd.DataFrame:
    """OHLCV history.

    period: '1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max'
    auto_adjust: when True (default), Close is split + dividend adjusted
                 (equivalent to 前复权 for forward-test cumulative returns).

    Columns: Open, High, Low, Close, Volume, Dividends, Stock Splits
    Index: timezone-aware DatetimeIndex (Shanghai time)
    """
    return yf.Ticker(to_yf(ticker)).history(
        period=period, interval=interval, auto_adjust=auto_adjust
    )


def stock_close_on(ticker: str, trade_date: date, adjust: str = "qfq") -> float:
    """Closing price on a specific date. Raises if not a trading day or no data.

    adjust: 'qfq' (default; auto_adjust=True) or 'none' (auto_adjust=False).
    """
    auto_adj = adjust == "qfq"
    # Pull a tight window around the target date
    end = trade_date + timedelta(days=5)
    yf_t = to_yf(ticker)
    df = _history_in_range(yf_t, trade_date, end, auto_adj)
    if df.empty:
        raise ValueError(f"No price data for {ticker} around {trade_date}")
    df_dates = pd.to_datetime(df.index).date
    mask = df_dates == trade_date
    if not mask.any():
        raise ValueError(f"No close on exact date {trade_date} for {ticker}")
    return float(df.loc[mask, "Close"].iloc[0])


@rate_limited
def _history_in_range(
    yf_ticker: str, start: date, end: date, auto_adjust: bool
) -> pd.DataFrame:
    return yf.Ticker(yf_ticker).history(
        start=start.isoformat(), end=end.isoformat(), auto_adjust=auto_adjust
    )


@rate_limited
def stock_financials(ticker: str, quarterly: bool = False) -> pd.DataFrame:
    """Income statement (annual or quarterly).

    Returns DataFrame with rows = line items, columns = period-end timestamps.
    """
    tk = yf.Ticker(to_yf(ticker))
    return tk.quarterly_financials if quarterly else tk.financials


@rate_limited
def stock_cashflow(ticker: str, quarterly: bool = False) -> pd.DataFrame:
    """Cash flow statement."""
    tk = yf.Ticker(to_yf(ticker))
    return tk.quarterly_cashflow if quarterly else tk.cashflow


@rate_limited
def stock_balance_sheet(ticker: str, quarterly: bool = False) -> pd.DataFrame:
    """Balance sheet."""
    tk = yf.Ticker(to_yf(ticker))
    return tk.quarterly_balance_sheet if quarterly else tk.balance_sheet


@rate_limited
def stock_earnings_dates(ticker: str, limit: int = 12) -> pd.DataFrame:
    """Upcoming + past earnings announcement dates with estimates / actuals."""
    return yf.Ticker(to_yf(ticker)).get_earnings_dates(limit=limit)


# --- Aggregated convenience snapshot for /analyze ---


def fundamental_snapshot(ticker: str) -> dict:
    """Compact bundle of everything long_term.md needs in one call.

    Returns:
      {
        "info": dict,
        "annual_income": DataFrame,
        "annual_cashflow": DataFrame,
        "annual_balance": DataFrame,
        "quarterly_income": DataFrame,
      }
    """
    return {
        "info": stock_info(ticker),
        "annual_income": stock_financials(ticker, quarterly=False),
        "annual_cashflow": stock_cashflow(ticker, quarterly=False),
        "annual_balance": stock_balance_sheet(ticker, quarterly=False),
        "quarterly_income": stock_financials(ticker, quarterly=True),
    }
