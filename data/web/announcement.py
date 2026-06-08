"""Announcement URL helpers for Claude WebFetch.

This module provides URL templates only. Claude fetches them directly via
the WebFetch tool (works from any environment — these are public web pages,
not APIs).

Sources:
  - 巨潮资讯 (CNINFO): centralized SSE+SZSE+BSE disclosure portal
  - 上交所 (SSE): SSE-specific announcement search
  - 深交所 (SZSE): SZSE-specific
  - 香港交易所 (HKEX): for H-shares / mainland companies dual-listed
"""

from __future__ import annotations


def cninfo_stock_url(ticker: str) -> str:
    """巨潮资讯网公司公告页（按股票代码筛选）.

    Example: ticker='600519.SH' -> URL for 贵州茅台 announcement listing.
    """
    code = ticker.split(".")[0]
    return f"http://www.cninfo.com.cn/new/disclosure/stock?stockCode={code}"


def cninfo_search_url(keyword: str) -> str:
    """巨潮资讯全文搜索 URL.

    Use to find recent announcements matching a keyword (业绩预告 / 重大合同 /
    减持 / 解禁 / 大基金).
    """
    from urllib.parse import quote
    return f"http://www.cninfo.com.cn/new/fulltextSearch?keyWord={quote(keyword)}"


def sse_disclosure_url(ticker: str) -> str:
    """上交所信息披露页（仅限沪市 60xxxx / 68xxxx）."""
    code = ticker.split(".")[0]
    return (
        f"http://www.sse.com.cn/disclosure/listedinfo/announcement/?productId={code}"
    )


def szse_disclosure_url(ticker: str) -> str:
    """深交所信息披露页（仅限深市 00xxxx / 30xxxx）."""
    code = ticker.split(".")[0]
    return f"http://www.szse.cn/disclosure/listed/notice/index.html?code={code}"


def hkex_news_url(stock_code: str) -> str:
    """港股披露易 URL (for cross-listed mainland companies)."""
    return f"https://www1.hkexnews.hk/listedco/listconews/sehk/{stock_code}.htm"


def sec_edgar_search_url(query: str) -> str:
    """SEC EDGAR full-text search (for US-listed China companies' 13F coverage)."""
    from urllib.parse import quote
    return f"https://efts.sec.gov/LATEST/search-index?q={quote(query)}&forms=13F"


def disclosure_urls_for(ticker: str) -> dict[str, str]:
    """All applicable disclosure portal URLs for a single A-share ticker.

    Returns:
      {
        "cninfo": ...,           # always
        "exchange": ...,         # SSE or SZSE depending on prefix
      }
    """
    code, suffix = ticker.split(".")
    urls = {"cninfo": cninfo_stock_url(ticker)}
    s = suffix.upper()
    if s == "SH":
        urls["exchange"] = sse_disclosure_url(ticker)
    elif s == "SZ":
        urls["exchange"] = szse_disclosure_url(ticker)
    return urls
