"""DEPRECATED since PLAN v0.5 — China-mainland-only data layer.

This package wraps AKShare endpoints, most of which route through 东财
(EastMoney) and are not accessible from overseas environments. The active
data layer in v0.5+ is `data.web.*` (yfinance + WebFetch).

Submodules here are PRESERVED but not loaded by default — they're kept for:
1. V2 when we add a境内 MCP proxy (then this layer becomes the data path)
2. Reference / migration source

To use this layer in V1, you need:
- `pip install -e ".[ashare-legacy]"` (installs akshare)
- 国内网络 OR VPN分流 configured (NO_PROXY for eastmoney.com / sina.com.cn)

See PLAN.md §0.2 and docs/SETUP.md for details.
"""

from ._client import rate_limited

__all__ = ["rate_limited"]
