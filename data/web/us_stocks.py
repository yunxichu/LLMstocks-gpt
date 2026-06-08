"""US stock data via yfinance — for cross-market reference.

Used to compare A-share supply-chain candidates against US sector leaders
(NVDA, AMD, TSLA, AVGO, etc.).
"""

from __future__ import annotations

import pandas as pd
import yfinance as yf

from .yf_client import rate_limited


@rate_limited
def stock_info(ticker: str) -> dict:
    """US stock basic info."""
    return yf.Ticker(ticker).info


@rate_limited
def stock_history(ticker: str, period: str = "1y") -> pd.DataFrame:
    return yf.Ticker(ticker).history(period=period, auto_adjust=True)


@rate_limited
def stock_financials(ticker: str, quarterly: bool = False) -> pd.DataFrame:
    tk = yf.Ticker(ticker)
    return tk.quarterly_financials if quarterly else tk.financials


@rate_limited
def stock_cashflow(ticker: str, quarterly: bool = False) -> pd.DataFrame:
    tk = yf.Ticker(ticker)
    return tk.quarterly_cashflow if quarterly else tk.cashflow


@rate_limited
def institutional_holders(ticker: str) -> pd.DataFrame | None:
    """US 13F top institutional holders (snapshot, not 13F filings).

    For full 13F detail, use Claude WebFetch to SEC EDGAR or sec-api.io.
    """
    return yf.Ticker(ticker).institutional_holders
