---
description: A-share single-stock long-term deep analysis (chokepoint + Bayesian)
argument-hint: <ticker>
---

You are about to analyze an A-share stock and produce a **locked, forward-test prediction**.

> **v0.5 note**: Only `long_term` analysis is active. Short-term and `/lhb` are
> deferred to V2 (require境内 data access). If user explicitly asks for short-term,
> tell them it's deferred and offer long-term instead, OR run a partial
> "watch only" non-locked analysis using just yfinance quote data.

## Input
`$ARGUMENTS` — typically just `<ticker>` (e.g. `600519`).
If user adds `short`, explain V1 deprecation per the v0.5 note above.

## Required reading (do this first, every time)

1. The playbook: `playbooks/long_term.md`
2. References:
   - `playbooks/references/research-rubric.md` — 16-dim scoring (v0.5)
   - `playbooks/references/pattern-library.md` — chokepoint patterns
   - `playbooks/references/a-share-data-sources.md` — yfinance + WebFetch priorities
3. The output template: `templates/stock_card.yaml`
4. Current date + trading calendar: `data.web.calendar.today_or_previous_trading_day()`

## Data fetching strategy (v0.5)

**Quantitative (Python via `data.web.*`):**
```python
from data.web import a_share, benchmark, calendar
info = a_share.stock_info("600519.SH")
financials = a_share.fundamental_snapshot("600519.SH")
hist = a_share.stock_history("600519.SH", period="2y")
benchmark_close = benchmark.benchmark_close_on("000300.SH", entry_date)
```

**Qualitative (Claude WebFetch):**
```python
from data.web import announcement
urls = announcement.disclosure_urls_for("600519.SH")
# Then use WebFetch tool on urls["cninfo"], urls["exchange"]
```

Search 巨潮 for keywords (业绩预告, 减持, 解禁, 股权质押, 重大合同):
```python
announcement.cninfo_search_url("600519 减持")
```

US sector leaders for cross-market context:
```python
from data.web import us_stocks
nvda = us_stocks.stock_info("NVDA")
```

## Workflow

Follow `playbooks/long_term.md` Step 1 through Step 15. Do not skip steps.

If a data source is unreachable, note the gap in `open_checks` and lower
confidence. Do NOT fabricate data.

## Output

Write two files under `predictions/locked/<YYYY-MM-DD>/`:
- `<prediction_id>.yaml` — structured stock card (per `templates/stock_card.yaml`)
- `<prediction_id>.raw.md` — human-readable reasoning (per `research-rubric.md`)

Where `<prediction_id>` = `<6-digit-code>-<yyyymmdd>-<HHMMSS>-lt` 
(e.g., `600519-20260608-203015-lt`).

`lock.analyzed_at` must be ISO 8601 with `+08:00`.

## Lock the prediction

After writing both files, run:

```powershell
python tools/lock_prediction.py predictions/locked/<YYYY-MM-DD>/<prediction_id>.yaml
```

This validates the LOCK area, hashes the raw.md, and appends to
`predictions/index.csv`. **After this, neither file may be edited.**

## If anything is unclear

- Missing data source: report which one and don't fabricate
- Conflicting evidence: note both in `open_checks`, lower confidence
- Cannot satisfy LOCK area completeness: don't lock; explain what's missing
- yfinance returns empty for a ticker: it may be a北交所 ('.BJ') ticker (not
  supported by yfinance in v0.5) or recently delisted — report to user

## Hard constraints

- Output `trade_disclosure_status: thesis_only` (this project does not trade)
- Do not write precise entry/target/stop prices or position sizing
- Do not store research report bodies (only metadata)
- Do not edit any previously locked prediction
- Set `long_term.smart_money.*` and `long_term.research_consensus.*` to null
  (data unavailable in v0.5; rubric reduced from 18 to 16 dimensions)
