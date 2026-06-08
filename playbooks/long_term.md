# Long-Term Stock Analysis Playbook

> **v0.6 status**: AUXILIARY (no longer the primary pipeline). The PRIMARY
> deliverable is now the weekly 5 BUY + 5 AVOID picks via `/picks`. This
> playbook handles **single-stock deep dives** when the user wants to drill
> into one specific ticker (often after seeing it in a picks list).
>
> Use this when:
> - User asks `/analyze <ticker>` for a deep view of one stock
> - User wants the full 16-dim rubric output for a name in their watchlist
> - Picks list flagged a ticker as BUY/AVOID and user wants full chokepoint /
>   Bayesian analysis to confirm
>
> For weekly portfolio-style output → use `/picks` instead.

> Triggered by: `/analyze <ticker>` (中长期视角)
> Output: a long-term stock card written to `predictions/locked/<date>/<prediction_id>.yaml`
> + accompanying raw markdown reasoning at `<prediction_id>.raw.md`, then locked
> via `tools/lock_prediction.py`.

This is the core playbook. It distills:

- **Serenity chokepoint method** — supply-chain bottleneck identification, multi-layer
  mapping, demand→financial translation, Bayesian conviction update
- **A-share specifics, adapted for overseas access** — 政策催化, 业绩窗口, 减持/解禁 (via WebFetch),
  trade vs thesis discipline
- **Forward-test discipline** — predictions are locked at creation, never retro-edited

> **v0.5 data-layer note**: This playbook uses **yfinance + Claude WebFetch** only.
> No China-mainland-only APIs (Tushare, AKShare East-Money). The trade-off is
> documented in PLAN.md §0.2 — short-term analysis is deferred to V2, and the
> rubric loses 2 dimensions (smart_money_quality + research_consensus). Bayesian
> evidence still flows from official announcements via Claude WebFetch to
> 巨潮资讯 / SSE / SZSE.

References:
- `references/research-rubric.md` — 16-dim scoring (v0.5: down from 18)
- `references/pattern-library.md` — 14 reusable patterns
- `references/a-share-data-sources.md` — yfinance + WebFetch source priority

---

## 0. Applicable Scope

Use when:
- User asks `/analyze <ticker>` for a mid- to long-term view (target horizon: T+20 trading days, ~1 month)
- User asks "should this be on our long-term watchlist?"
- User compares 2-5 long-term candidates (run once per ticker, then synthesize)

Do NOT use when:
- The query is purely short-term (V1 deprecated)
- Ticker is 北交所 (BJ suffix; yfinance does not cover; defer to V2)

---

## 1. Required Data (fetch before reasoning)

All sources below are reachable from any environment with internet (US / EU /
CN+VPN). No China-mainland-only API dependency.

### 1.1 Must fetch (cannot output a card without these)

| Data | How to fetch | Notes |
|---|---|---|
| Stock basic info | `data.web.a_share.stock_info(ticker)` | name, sector, industry, marketCap, trailingPE, priceToBook, currency, longBusinessSummary |
| Annual financials (3-5 years) | `data.web.a_share.stock_financials(ticker)` | Income statement |
| Annual cashflow | `data.web.a_share.stock_cashflow(ticker)` | FCF derivation |
| Annual balance sheet | `data.web.a_share.stock_balance_sheet(ticker)` | Debt, assets, equity |
| Quarterly financials (4-6 q) | `data.web.a_share.stock_financials(ticker, quarterly=True)` | Recent trends |
| Price history (5y, qfq) | `data.web.a_share.stock_history(ticker, period='5y')` | For estimating estimated valuation percentiles |
| Today's close + benchmark close | `data.web.a_share.stock_close_on(...)` + `data.web.benchmark.benchmark_close_on('000300.SH', date)` | For LOCK area entry_close |
| Recent public announcements | **Claude WebFetch** to `data.web.announcement.disclosure_urls_for(ticker)` URLs | 业绩预告 / 减持 / 解禁 / 重大合同 / 定增 from 巨潮 + 交易所 |
| Convenient bundle | `data.web.a_share.fundamental_snapshot(ticker)` | All financial data in one call |

### 1.2 Should fetch (via Claude WebFetch — these are public web pages)

| Source | Why |
|---|---|
| 巨潮资讯 search by keyword | 找业绩预告/解禁/减持等近 6 个月公告 |
| 行业新闻（财联社、21 经济报道、第一财经、新京报） | demand-shock evidence + 政策动向 |
| 政策文件（发改委、工信部、财政部新发文） | policy catalyst |
| 互动易（深交所） / e 互动（上交所） | 管理层语言（lower authority than 公告） |
| 美股行业龙头 financials/quote via `data.web.us_stocks` | 行业景气对照 (NVDA / AMD / TSLA / AVGO / MU etc.) |

### 1.3 Optional

- SEC EDGAR 13F filings (Claude WebFetch to sec.gov) — 顶级投资人对中概股 ADR 持仓变动，作为侧面信号
- 香港交易所披露易 (HKEXnews) — 双重上市公司 H 股披露
- Industry-specific data: TrendForce / SEMI / DigiTimes for semiconductors; IFR for robotics; etc.

### 1.4 No longer used (deprecated since v0.5)

- ~~Tushare MCP (financials, valuation, holdings, research, restrictions, kpl_list)~~
- ~~AKShare East-Money endpoints (LHB, fund_flow, research, restrictions)~~
- ~~公募季报重仓 / QFII 季度持仓~~
- ~~分析师评级 + 目标价数据库~~
- ~~主力资金流 / 涨停板梯队~~

These data points either have no overseas substitute or are short-term-only.
See PLAN.md §0.2.

---

## 2. Analysis Workflow

Follow steps **in order**. Skipping is allowed only if the data is genuinely
unavailable; in that case write the gap into `open_checks`.

### Step 1 — Verify and normalize
- Normalize ticker (`600519.SH`, `000001.SZ`). 北交所 (`.BJ`) suffix → reject (V2 only).
- Confirm market segment via `data.web.a_share.market_segment(ticker)`.
- Determine `entry_close_date` via `data.web.calendar.today_or_previous_trading_day()`.
- Pull `entry_close` via `data.web.a_share.stock_close_on(ticker, entry_close_date)`.
- Pull `benchmark_entry_close` via `data.web.benchmark.benchmark_close_on('000300.SH', entry_close_date)`.

### Step 2 — Identify the demand shock (don't start from the ticker)
- What end-market wave does this company purport to ride? (AI compute / robotics / 储能 / 半导体 / 光通信 / ...)
- 时点 — 是 already happening / 加速期 / 早期 / 远期?
- Why now — what specifically changed in the last 6-12 months?

If you cannot name a specific demand shock, the analysis is weak. Mark
`demand_shock.why_now` as low confidence and put in `open_checks`.

### Step 3 — Map the supply chain backward
- From end product to component to material to equipment to capacity owner.
- 至少 3 层深度.
- Identify exactly which node this company occupies in `supply_chain.target_node`.
- Reference `pattern-library.md` to classify which Category-A pattern applies.

### Step 4 — Set the prior
- Initial probability that this company is a true chokepoint (not just thematically adjacent).
- Anchor in **physical reality**: BOM role / customer need / capacity / substitutes.

### Step 5 — Dig down at least 3 layers
- Don't stop at the obvious bottleneck.
- Move from GPU/HBM/电力 into 2nd / 3rd-order nodes.

### Step 6 — Find the chokepoint
- **Scarcity**: supply scarce, slow expansion, capacity-locked?
- **Switching cost / qualification friction**: 客户认证周期 (典型 6-18 个月)?
- **Architecture specificity**: tied to a specific architecture (CPO / 800VDC / advanced packaging)?
- **Capacity expansion constraints**: 资本开支大 / 技术壁垒 / 政策限制?

### Step 7 — Translate demand to financials
- Same demand shock material to this company at its size?
- Estimate: revenue, gross margin, backlog, multiple impact.
- Concrete units when possible.

**v0.5 data**: use `fundamental_snapshot(ticker)` for annual + quarterly financials.

### Step 8 — Test market access and pricing vacuum
- Market cap (smaller = more sensitive to demand shock)
- Analyst coverage signals: **Claude WebFetch** to 财联社/雪球 看是否被反复报道 (公募季报数据已不可得)
- Liquidity (从 `stock_history` 计算 daily turnover)
- "Is this name structurally hard to own for large funds?" 仍是有效问题

> v0.5 note: lacking 公募季报 means we cannot quantify institutional ownership
> changes. We approximate via media coverage frequency and absence of analyst
> coverage — both observable via WebFetch.

### Step 9 — Test mispricing
- Current market framing vs alternative framing
- Forward P/E vs growth path (from `stock_info.trailingPE` + financials growth)
- Replacement value (from balance sheet)

### Step 10 — Bayesian update with current evidence (via WebFetch)
For each recent (90 day) announcement, news, or filing:

1. Use `data.web.announcement.disclosure_urls_for(ticker)` to get 巨潮 / 交易所 URLs
2. Claude WebFetch those pages
3. Read recent announcement titles + summaries
4. For each item, classify (see `a-share-data-sources.md` News-to-Evidence Triage):
   - **Thesis-confirming**: 业绩超预期 / 大客户合同 / 产能投产 / 政策落地
   - **Thesis-weakening**: 业绩雷 / 大额减持 / 定增 / 监管处罚
   - **Neutral / noise**: 股价异动 / 重复老消息

Adjust posterior direction (up / down / flat). Note thesis-breaking evidence.

### Step 11 — Track capital rotation (observable from public sources)

**v0.5 reframe**: without 公募季报 / 北向 quarterly data, we use observable proxies:
- **Same-theme US leaders' stock performance** — `data.web.us_stocks.stock_history` for NVDA / AMD / etc. If US leaders rerated and A-share peers haven't, that's a rotation signal
- **A-share theme index performance** (中证 行业指数 via yfinance if available)
- **Recent financial-media narrative shifts** (WebFetch 财联社 / 21 经济报道 关键词搜)

### Step 12 — Score using the rubric (16 dimensions, 80 total)
Run through 16 dimensions in `references/research-rubric.md`. Score 0-5 each. 
- Total ≥ 55: compelling
- Total 40-54: worth deeper DD
- Total 25-39: watchlist
- Total < 25: mostly narrative

A single dimension scoring 0 in **evidence quality** or **disclosure transparency** 
overrides the total.

### Step 13 — Apply A-share risk filters (hard checks via WebFetch)

Before locking, run these binary checks. **Each requires Claude WebFetch** to
巨潮 / 交易所披露 (no direct API in v0.5):

- [ ] 大股东 / 高管最近 6 个月有大幅减持公告？(巨潮搜 "减持" + ticker)
- [ ] 商誉 / 净资产 > 50%? (从 `balance_sheet` 计算)
- [ ] 业绩雷历史 — 最近 2 年业绩预告与最终披露偏差 > 30%? (WebFetch 巨潮的"业绩预告"和年报对比)
- [ ] 未来 30 天有大额解禁? (WebFetch 巨潮搜 "解禁")
- [ ] ST / 退市风险警示? (`stock_info.shortName` 含 "ST" or "*ST" 或 WebFetch 验证)
- [ ] 控股股东股权质押 > 80%? (WebFetch 巨潮搜 "股权质押")
- [ ] 财务造假 / 监管处罚记录? (WebFetch 监管处罚搜索)

任何一项命中即在 `concerns` 中明确列出,并按命中数下调 confidence。

### Step 14 — Write the card
Fill `templates/stock_card.yaml`:
- `prediction_type: long_term`
- LOCK area: all required fields with current data
- `long_term` section: every applicable subsection
  - **v0.5**: `smart_money` 子段设为 null 或空字典（数据不可得）；`research_consensus` 同理
- `short_term: null`
- `open_checks`: 至少 2-3 条

Also write the raw reasoning markdown alongside (`<prediction_id>.raw.md`).

### Step 15 — Lock the prediction
Run `python tools/lock_prediction.py <yaml_path>` to:
- Validate LOCK area completeness
- Compute SHA-256 of `<prediction_id>.raw.md`
- Fill `lock.claude_output_hash` and `lock.playbook_version`

After locking, the card is immutable.

---

## 3. Judgment Framework

### 3.1 Confidence calibration (v0.5 — adjusted for reduced rubric)
- `confidence ≥ 0.75`: rubric ≥ 55 + chokepoint clear + Bayesian net positive
- `confidence 0.55-0.74`: rubric 45-54 + 2 of 3 strong
- `confidence 0.4-0.54`: rubric 30-44 + thesis plausible but key gaps
- `confidence < 0.4`: do not lock; extend `open_checks` instead

> v0.5 note: confidence thresholds are slightly lower than the 18-dim version
> because we have less data. Compensate by being more conservative on the
> downside (lower confidence + more invalidation conditions).

### 3.2 Prediction horizon: T+20 (default for long_term)
- **success_criteria** default: "T+20 收盘相对沪深 300 超额 > 0%"
- **failure_criteria** default: "T+20 收盘相对沪深 300 < -5% 或个股绝对收益 < -10%"

For explicitly longer thesis (e.g., 3-month), optionally set `prediction_horizon_days: 60`.

### 3.3 Invalidation conditions
Default set (always include):
- "停牌 > 5 个交易日"（可通过 yfinance 检测 — 连续 NaN）
- "突发监管 / 退市风险 / ST 警示"
- "重大财务造假 / 审计被质疑"

Add 2-3 thesis-specific ones based on what you write in Bayesian update.

---

## 4. Output Requirements

### 4.1 Files written
- `predictions/locked/<yyyy-mm-dd>/<prediction_id>.yaml` — structured card
- `predictions/locked/<yyyy-mm-dd>/<prediction_id>.raw.md` — raw reasoning

### 4.2 stock_card.yaml field strategy
- All `lock.*` fields filled (cannot leave blank, lock_prediction.py will reject)
- `long_term.smart_money.*` → set to null in v0.5 (no overseas substitute)
- `long_term.research_consensus.*` → set to null in v0.5
- All other long_term fields filled to the best of available evidence

### 4.3 raw.md structure
Use the human-readable template in `research-rubric.md`. Include:
- Verdict + confidence + rationale (1 paragraph)
- Demand shock + chain map (1-2 paragraphs)
- Chokepoint analysis (1-2 paragraphs)
- Evidence table (with claim / source / strength)
- News & disclosure update table (last 90 days, **via WebFetch**)
- Bayesian update prose
- Financial / valuation snapshot
- Mispricing argument
- Catalysts + risks
- 16-dim rubric scoring table (compact)
- Open checks

---

## 5. Lock-In Requirements (强制)

Before lock:
- `lock.prediction_id` matches `<6digit>-<yyyymmdd>-<HHMMSS>-lt`
- `lock.analyzed_at` ISO 8601 with `+08:00`
- `lock.entry_close_date` is a real trading day (verify via `data.web.calendar.is_trading_day`)
- `lock.entry_close` and `lock.benchmark_entry_close` are floats > 0
- `lock.success_criteria` and `lock.failure_criteria` concrete
- `lock.invalidation_conditions` has ≥ 3 entries

After lock: no edits. If error found, create a new prediction with new ID,
note supersession in `open_checks` of both.

---

## 6. Notes & Gotchas

### 6.1 数据时点 (avoid look-ahead even in live analysis)
- 财报数据看 yfinance 的 columns (period-end dates) — but the actual 公告日 may be 1-2 months later. If today is 4 月 15 日, the FY 报表 data point exists in yfinance but the actual disclosure window is 4 月 30 日前. Cross-check with 巨潮披露日.

### 6.2 yfinance limitations
- A 股 financial 数据来自 Yahoo 的 vendor (Morningstar)，**A 股部分指标可能 stale by 1-2 quarters** vs 巨潮原始披露
- PE / PB 是 trailing snapshot，没有时间序列分位 — 自己用历史股价 + 历史 EPS 算
- 没有 institutional_holders（A 股 yfinance 数据空），所以 smart_money 维度 deprecated

### 6.3 北向资金降级（仍生效）
- 不要查 / 引用"今天北向净买入"
- 北向只有季度数据，且 v0.5 我们也不直接查（无 API）；可通过 WebFetch 巨潮的"沪深股通持股变动"披露看

### 6.4 当心 anti-patterns（全部列在 `pattern-library.md`）
- "政策利好 = chokepoint" 错；政策只是必要条件
- "题材联动 = 基本面拐点" 错；联动只是热度
- "是英伟达 / 大客户的供应商 = 重大收入" 错；要看实际营收占比
- "看好 = 我持仓" 错；区分 thesis 和 disclosure

### 6.5 合规与版权
- 不存储研报全文 — 只取标题 / 评级 / 目标价
- WebFetch 的内容仅供研究，不复制原文
- 不对外分发
- 输出 `trade_disclosure_status: thesis_only`（不持仓不下单）
- 操作指南只写框架（建仓方式 / 跟踪指标 / 失效条件），不写精确价位

---

## 7. Pre-Test Discipline

**During the forward-test window**, do NOT modify this playbook. Any change 
contaminates the sample. If you absolutely must change (critical bug), 
record in `PLAN.md` §9.4 with explicit "样本污染" tag.

Save methodology improvements for the next test round (post-review).
