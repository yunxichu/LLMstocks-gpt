"""Trading calendar utilities for A-shares."""

from __future__ import annotations

from datetime import date, datetime
from typing import Iterable

import akshare as ak
import pandas as pd

from ._client import rate_limited

_CACHE: dict[str, list[date]] = {}


@rate_limited
def _fetch_calendar() -> list[date]:
    df = ak.tool_trade_date_hist_sina()
    series = pd.to_datetime(df["trade_date"]).dt.date
    return sorted(series.tolist())


def trading_calendar() -> list[date]:
    """All historical and known-future A-share trading dates."""
    if "calendar" not in _CACHE:
        _CACHE["calendar"] = _fetch_calendar()
    return _CACHE["calendar"]


def is_trading_day(d: date) -> bool:
    return d in set(trading_calendar())


def previous_trading_day(d: date) -> date:
    """Most recent trading day strictly before d."""
    for td in reversed(trading_calendar()):
        if td < d:
            return td
    raise ValueError(f"No previous trading day before {d}")


def next_trading_day(d: date) -> date:
    """Earliest trading day strictly after d."""
    for td in trading_calendar():
        if td > d:
            return td
    raise ValueError(f"No next trading day after {d}")


def trading_days_between(start: date, end: date) -> list[date]:
    """All trading days in [start, end] inclusive."""
    return [td for td in trading_calendar() if start <= td <= end]


def add_trading_days(d: date, n: int) -> date:
    """Trading day that is n trading days after d.

    n > 0: forward. n < 0: backward. n == 0: returns d itself if it is a trading
    day, otherwise the next trading day after d.
    """
    cal = trading_calendar()
    if n == 0:
        return d if d in set(cal) else next_trading_day(d)
    # Find index of d (or the nearest)
    if d in set(cal):
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
    """Today if it's a trading day, else the previous trading day."""
    today = datetime.now().date()
    return today if is_trading_day(today) else previous_trading_day(today)
