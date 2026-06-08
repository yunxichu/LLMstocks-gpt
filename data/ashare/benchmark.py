"""Benchmark index data for forward-test relative-return evaluation."""

from __future__ import annotations

from datetime import date

import akshare as ak
import pandas as pd

from ._client import rate_limited

# Map our standardized ticker to AKShare's east-money symbol.
BENCHMARK_CODES: dict[str, str] = {
    "000300.SH": "sh000300",  # 沪深 300 (large cap)
    "000905.SH": "sh000905",  # 中证 500 (mid cap)
    "000906.SH": "sh000906",  # 中证 800 (large + mid; long-term benchmark)
    "000852.SH": "sh000852",  # 中证 1000 (small/mid; short-term benchmark)
}

_CACHE: dict[str, pd.DataFrame] = {}


@rate_limited
def _fetch_benchmark(ak_symbol: str) -> pd.DataFrame:
    df = ak.stock_zh_index_daily_em(symbol=ak_symbol)
    df["date"] = pd.to_datetime(df["date"]).dt.date
    return df


def benchmark_history(benchmark_ticker: str) -> pd.DataFrame:
    """Full daily history for a benchmark index.

    Columns: date, open, close, high, low, volume, amount
    """
    if benchmark_ticker not in BENCHMARK_CODES:
        raise ValueError(
            f"Unknown benchmark: {benchmark_ticker}. "
            f"Supported: {list(BENCHMARK_CODES)}"
        )
    ak_symbol = BENCHMARK_CODES[benchmark_ticker]
    if ak_symbol not in _CACHE:
        _CACHE[ak_symbol] = _fetch_benchmark(ak_symbol)
    return _CACHE[ak_symbol]


def benchmark_close_on(benchmark_ticker: str, trade_date: date) -> float:
    """Closing price of a benchmark on a specific trade date.

    Raises ValueError if the date is not a trading day or data not available.
    """
    df = benchmark_history(benchmark_ticker)
    matched = df[df["date"] == trade_date]
    if matched.empty:
        raise ValueError(
            f"No benchmark close for {benchmark_ticker} on {trade_date}"
        )
    return float(matched["close"].iloc[0])


def refresh_cache() -> None:
    """Force refresh all benchmark caches (call once per trading day)."""
    _CACHE.clear()
