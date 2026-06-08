"""Cross-border accessible data layer (works from outside Mainland China).

This package replaces the legacy `data.ashare` package for v0.5+ workflows.
All sources here are reachable from the US, EU, and from Mainland China with VPN:
- yfinance (Yahoo Finance) — A-share / 港股 / 美股 quotes + financials
- Claude WebFetch — 巨潮资讯 / SSE / SZSE / HKEXnews announcements
- SEC EDGAR (public) — 13F holdings for cross-market reference

Trade-offs vs the legacy China-mainland-only layer:
  Lost (no overseas substitute):
    - 龙虎榜 (LHB)
    - 公募基金季报重仓
    - A 股研报评级共识
    - 主力资金流 / 涨停板梯队
  Retained:
    - Stock OHLCV history
    - Annual + quarterly financial statements (income, cashflow, balance sheet)
    - Basic info (sector, industry, market cap, PE, PB)
    - Benchmark indexes (沪深300/中证500/800/1000)
    - Trading calendar (derived from index history)
    - Public announcements (via Claude WebFetch to 巨潮/交易所)
"""

from .yf_client import rate_limited

__all__ = ["rate_limited"]
