"""A-share trading calendar derived from yfinance index history.

We use the 沪深 300 (000300.SS) index history as the canonical trading-day
set. All A-share markets share the same trading calendar, so any liquid
index works.
"""

from __future__ import annotations

from datetime import date, datetime
from functools import lru_cache

import pandas as pd
import yfinance as yf

from .yf_client import rate_limited


@rate_limited
def _fetch_calendar() -> list[date]:
    # 沪深 300 since inception (2005) covers all A-share trading days.
    df = yf.Ticker("000300.SS").history(period="max", auto_adjust=False)
    if df.empty:
        raise RuntimeError(
            "Failed to fetch 000300.SS history from yfinance. "
            "Verify network connectivity to query2.finance.yahoo.com."
        )
    dates = pd.to_datetime(df.index).tz_localize(None).normalize().date  # type: ignore[assignment]
    return sorted(set(dates.tolist()))


@lru_cache(maxsize=1)
def trading_calendar() -> tuple[date, ...]:
    """Cached A-share trading dates (immutable tuple)."""
    return tuple(_fetch_calendar())


def is_trading_day(d: date) -> bool:
    return d in set(trading_calendar())


def previous_trading_day(d: date) -> date:
    for td in reversed(trading_calendar()):
        if td < d:
            return td
    raise ValueError(f"No previous trading day before {d}")


def next_trading_day(d: date) -> date:
    for td in trading_calendar():
        if td > d:
            return td
    raise ValueError(f"No next trading day after {d}")


def trading_days_between(start: date, end: date) -> list[date]:
    return [td for td in trading_calendar() if start <= td <= end]


def add_trading_days(d: date, n: int) -> date:
    """Return the date that is n trading days after d (negative for before).

    If d is not itself a trading day:
      n > 0: count from next trading day after d
      n < 0: count from previous trading day before d
      n == 0: return d if it's a trading day, else next_trading_day(d)
    """
    cal = list(trading_calendar())
    cal_set = set(cal)
    if n == 0:
        return d if d in cal_set else next_trading_day(d)
    if d in cal_set:
        idx = cal.index(d)
    elif n > 0:
        idx = cal.index(next_trading_day(d))
    else:
        idx = cal.index(previous_trading_day(d))
    target = idx + n
    if target < 0 or target >= len(cal):
        raise ValueError(f"add_trading_days out of range: {d} + {n}")
    return cal[target]


def today_or_previous_trading_day() -> date:
    today = datetime.now().date()
    return today if is_trading_day(today) else previous_trading_day(today)
