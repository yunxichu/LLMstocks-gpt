"""Basic A-share metadata: ticker list, market cap snapshot, single-stock info."""

from __future__ import annotations

import akshare as ak
import pandas as pd

from ._client import rate_limited

# Ticker normalization: AKShare uses 6-digit codes; we standardize to <code>.<SH|SZ|BJ>


def normalize_ticker(code: str) -> str:
    """Convert '600519' -> '600519.SH', '000001' -> '000001.SZ', '430090' -> '430090.BJ'."""
    code = str(code).split(".")[0].zfill(6)
    if code.startswith(("60", "68", "9")):  # 60xxxx 主板, 68xxxx 科创, 9xxxxx B股
        return f"{code}.SH"
    if code.startswith(("00", "30", "20")):  # 00xxxx 主板, 30xxxx 创业板, 20xxxx B股
        return f"{code}.SZ"
    if code.startswith(("4", "8")):  # 北交所
        return f"{code}.BJ"
    return code


def strip_suffix(ticker: str) -> str:
    """Return the 6-digit code from '600519.SH' -> '600519'."""
    return ticker.split(".")[0]


def market_segment(ticker: str) -> str:
    """Classify ticker into sh_main / sz_main / chinext / star / bj_se."""
    code = strip_suffix(ticker)
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
def list_a_stocks_realtime() -> pd.DataFrame:
    """All A-share realtime snapshot.

    Columns include (Chinese):
      代码, 名称, 最新价, 涨跌幅, 总市值, 流通市值, 市盈率-动态, 市净率, 量比, 换手率, ...
    """
    return ak.stock_zh_a_spot_em()


@rate_limited
def stock_individual_info(ticker: str) -> dict:
    """Single-stock basics: 上市日期, 总股本, 流通股, 行业, 总市值 (snapshot)."""
    code = strip_suffix(ticker)
    df = ak.stock_individual_info_em(symbol=code)
    return dict(zip(df["item"], df["value"]))


@rate_limited
def list_a_stock_codes() -> pd.DataFrame:
    """All A-share code -> name mapping (lightweight; no quotes)."""
    return ak.stock_info_a_code_name()
