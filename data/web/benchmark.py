"""Benchmark indexes via yfinance (for forward-test relative-return evaluation).

Supports both A-share benchmarks (中证 800/1000 etc.) and global benchmarks
(S&P 500, Nasdaq 100, VIX) for cross-market context.
"""

from __future__ import annotations

from datetime import date

import pandas as pd
import yfinance as yf

from .yf_client import rate_limited

# Our standardized ticker -> yfinance symbol
#
# yfinance vendor coverage of A-share indexes is UNEVEN. As of v0.5 testing
# (June 2026), only the following A-share indexes have full daily history:
#   ✓ 000300.SS (沪深 300)            — full history, RECOMMENDED long-term benchmark
#   ✓ 000001.SS (上证综指)            — full history
#   ✓ 399001.SZ (深证成指)            — full history
#   ✗ 000906.SS (中证 800)            — 1 row only, NOT usable for tracking
#   ✗ 000852.SS (中证 1000)           — 1 row only
#   ✗ 000905.SS (中证 500)            — 1 row only
#   ✗ 399006.SZ (创业板指)            — 1 row only
#
# As fallbacks, the corresponding ETFs DO have full history:
#   ✓ 510300.SS (沪深 300 ETF), 510500.SS (中证 500 ETF), 510050.SS (上证 50 ETF)
#   ✓ 159915.SZ (创业板 ETF)
BENCHMARK_MAP: dict[str, str] = {
    # A-share indexes (verified full-history)
    "000300.SH": "000300.SS",   # 沪深 300 — long-term default (v0.5 hotfix; was 中证 800)
    "000001.SH": "000001.SS",   # 上证综指
    "399001.SZ": "399001.SZ",   # 深证成指
    # A-share ETF fallbacks (use when index data is incomplete)
    "510300.SH": "510300.SS",   # 沪深 300 ETF
    "510500.SH": "510500.SS",   # 中证 500 ETF
    "510050.SH": "510050.SS",   # 上证 50 ETF
    "159915.SZ": "159915.SZ",   # 创业板 ETF
    # Index entries that exist but have only 1-row vendor coverage (kept for reference)
    "000906.SH": "000906.SS",   # 中证 800 — DEFER (vendor returns 1 row only)
    "000852.SH": "000852.SS",   # 中证 1000 — DEFER
    "000905.SH": "000905.SS",   # 中证 500 — DEFER (use 510500.SH ETF instead)
    # US (for cross-market reference)
    "SPX": "^GSPC",             # S&P 500
    "NDX": "^NDX",              # Nasdaq 100
    "DJI": "^DJI",              # Dow Jones
    "VIX": "^VIX",              # Volatility
    "US10Y": "^TNX",            # 10-year Treasury yield
}

_CACHE: dict[str, pd.DataFrame] = {}


@rate_limited
def _fetch(yf_symbol: str) -> pd.DataFrame:
    # Use a long start date instead of period='max' — some A-share indexes
    # reject period='max' (Yahoo returns "must be one of: 1d, 5d") while still
    # accepting explicit start/end ranges.
    df = yf.Ticker(yf_symbol).history(
        start="2005-01-01", end=None, auto_adjust=False
    )
    if df.empty:
        return df
    # Normalize index to date (drop time + timezone)
    df.index = pd.to_datetime(df.index).tz_localize(None).normalize().date  # type: ignore[assignment]
    return df


def benchmark_history(benchmark_ticker: str) -> pd.DataFrame:
    """Full daily history for a benchmark index.

    Columns: Open, High, Low, Close, Volume, Dividends, Stock Splits
    Index: python date (no time component)
    """
    yf_symbol = BENCHMARK_MAP.get(benchmark_ticker)
    if not yf_symbol:
        raise ValueError(
            f"Unknown benchmark: {benchmark_ticker}. "
            f"Supported: {list(BENCHMARK_MAP)}"
        )
    if yf_symbol not in _CACHE or _CACHE[yf_symbol].empty:
        _CACHE[yf_symbol] = _fetch(yf_symbol)
    return _CACHE[yf_symbol]


def benchmark_close_on(benchmark_ticker: str, trade_date: date) -> float:
    """Closing price of a benchmark on a specific date.

    If trade_date is not exactly in the index (e.g., weekend), returns the
    most recent close on or before trade_date.
    """
    df = benchmark_history(benchmark_ticker)
    if df.empty:
        raise ValueError(f"No benchmark data for {benchmark_ticker}")
    if trade_date in df.index:
        return float(df.loc[trade_date, "Close"])
    valid = df.index[df.index <= trade_date]
    if len(valid) == 0:
        raise ValueError(f"No benchmark data on or before {trade_date}")
    return float(df.loc[valid[-1], "Close"])


def refresh_cache() -> None:
    """Force refresh all benchmark caches (call once per trading day)."""
    _CACHE.clear()
