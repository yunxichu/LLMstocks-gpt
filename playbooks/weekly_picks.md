# Weekly Picks Playbook (5 AI + 5 全市场 + 5 AVOID — 15 picks total)

> Triggered by: `/picks`
> Frequency: 每周日 / 用户手动触发
> Output: 一份含 3 类 × 5 支共 15 支的清单 + 市场背景 + 交互式 HTML 报告

This is the **PRIMARY pipeline** of the project. v1.1 起产出 3 类 picks:
1. **AI 相关推荐 (ai_picks, 5 支)** — 限 AI 相关主题
2. **全市场推荐 (market_picks, 5 支)** — 非 AI 主题（含 watchlist 单独名）
3. **过热不推荐 (avoid_picks, 5 支)** — 不限主题

每只 pick 经过 18 类 red flag 全扫 + evidence_log 强制溯源。最终 lock + 渲染
HTML 报告（点击式可展开详细分析）。

> **v1.1 升级**: AI picks 引入 `ai_supply_chain_review`，把 12M 估值和 3-5Y
> AI 结构性可选性分开判断。selection 顺序: AVOID → AI 结构性瓶颈 → 全市场
> (不重叠)。

### AI Themes 定义

`AI_THEMES = {ai-compute, advanced-packaging, pcb-substrate, optical-cpo, semi-equipment, data-center-power, cooling, robotics, domestic-software}`

非 AI themes: energy-storage, solid-state-battery, low-altitude, military-tech, biotech-ai。

每只 ai_picks 的 `theme` 字段必须在 AI_THEMES; market_picks 的 `theme`
必须不在 AI_THEMES (或为空表示 watchlist 单独名)。

---

## 0. Hard requirements (cannot skip)

- **Red flag scan is MANDATORY** for every short-listed candidate (see Stage 4 + `references/red-flags.md`)
- 每只 ai/market pick: `red_flags_checked = [1..18]` AND `red_flags_triggered` 0 HIGH + ≤1 MEDIUM
- 每只 avoid pick: `red_flags_triggered ≥ 1 HIGH 或 ≥ 2 MEDIUM`，每条带具体 evidence
- 没有 "watchlist only / neutral" 选项；必须 verdict (AI / 全市场 / AVOID)
- 不能 fabricate；数据缺失要写 open_checks 并降 confidence
- **v0.7: 每只 pick 必须有 `evidence_log`**，至少 **3 个 type='hard'** entries
  (yfinance 字段值 / WebFetch 公告标题+URL+日期 / 公开文件引用)。任何非 hard
  的 claim 必须显式标记 `type: soft` 或 `type: pending_verify`。lock_picks.py
  强制校验。
- **★ v1.0 target price discipline**:
  - 每只 AI / market BUY 或 WATCH 必须填写 `target_price_review`。
  - target price 必须包含研究报告矩阵、FY2026/FY2027 EPS 或净利预测桥、估值方法、目标价分歧、上修/下修触发器、证据等级。
  - 如果没有至少 3 个可信研报/一致预期输入，`target_price_review.status` 必须是 `provisional`，不能写成 `research_grade`。
  - 每只 AVOID 必须填写 `valuation_red_flag.fair_value_or_risk_range`，说明为什么现价透支。
- **★ v1.1 AI supply-chain boom discipline**:
  - 每只 `ai_picks` 必须填写 `ai_supply_chain_review`。
  - 必须分开写 `near-term 12M target` 与 `3-5Y structural option`。
  - 高估值不能机械等于 AVOID；若 `ai_bottleneck_score >= 80` 且有硬证据证明瓶颈、客户/产能和财务传导，可进入 WATCH/BUY。
  - 但如果当前价格已经接近或超过结构性牛市情景，仍然必须标 WATCH/AVOID，不能用“AI 会很大”替代估值。
- **★ v0.8 NEW: 3 类约束**
  - `ai_picks` 必须 5 支（或更少有诚实理由），每只 `theme` 必须 ∈ AI_THEMES
  - `market_picks` 必须 5 支，每只 `theme` 必须 ∉ AI_THEMES (或空表示 watchlist)
  - `ai_picks` 与 `market_picks` 的 ticker 不能重叠
  - `avoid_picks` 必须 5 支，不限主题
- **★ v0.8 NEW: 必须生成 HTML 报告** via `python tools/render_picks_html.py
  predictions/picks/<date>/picks_<HHMMSS>.yaml`

---

## 1. Required reading

1. This playbook (you're reading it)
2. `references/red-flags.md` — 18 category checklist (强制使用)
3. `references/pattern-library.md` — 14 类模式（用于 strategy 分类）
4. `references/research-rubric.md` — 单股评分维度（v0.5 16 维）
5. `references/a-share-data-sources.md` — yfinance + WebFetch 来源
6. `references/valuation-target-price.md` — 目标价 / 估值强制标准
7. `references/ai-supply-chain-boom-framework.md` — AI 爆发与供应链瓶颈估值标准
8. `templates/picks_card.yaml` — 输出模板
9. `templates/valuation_card.yaml` — 目标价估值子模板

---

## 2. Data interfaces

```python
from data.web import a_share, benchmark, calendar, us_stocks, announcement
from datetime import date

entry_date = calendar.today_or_previous_trading_day()
benchmark_entry = benchmark.benchmark_close_on('000300.SH', entry_date)

# Per-ticker
info = a_share.stock_info('600519.SH')
fs = a_share.fundamental_snapshot('600519.SH')
hist = a_share.stock_history('600519.SH', period='1y')
entry_close = a_share.stock_close_on('600519.SH', entry_date)
urls = announcement.disclosure_urls_for('600519.SH')
# Then use WebFetch on urls['cninfo'] or 新浪财经 announcement page
```

---

## 3. Workflow (7 stages)

### Stage 1: 候选池构建 (target 30-80 tickers)

Sources to combine:

| Source | How |
|---|---|
| User watchlist | Read `watchlist/watchlist.yaml` |
| Active themes | Read `config/themes.yaml`, expand each active theme to its representative tickers |
| US sector leaders' A-share peers | Check NVDA / AMD / TSLA / AVGO / ASML / TSM 1-month price action; if a US sector ran +20% with no A-share peer move, surface A-share peers |
| AI capex leaders | Check NVDA / MSFT / GOOGL / META / AMZN / AVGO / TSM / SK hynix latest results and guidance |
| WebFetch 财联社 hot news (last 7 days) | `https://www.cls.cn/` — note tickers mentioned in major stories |
| WebFetch 新浪财经 hot stocks | `https://finance.sina.com.cn/realstock/company/sh000001/nc.shtml` (热门股) |
| Recent earnings outliers (last 14 days) | WebFetch 巨潮 / 新浪 announcement search for "业绩预告" + 业绩快报 outliers |

**Goal**: 30-80 unique tickers. Save provisional list to scratch buffer (no
file yet) — final list goes into picks_card.yaml later.

If watchlist + themes already give >50 tickers, you can skip news-based
expansion to save tokens.

### Stage 2: 批量初评 (yfinance only — fast, no WebFetch)

For each candidate (no WebFetch yet, just yfinance):

```python
info = a_share.stock_info(ticker)
fs = a_share.fundamental_snapshot(ticker)
hist = a_share.stock_history(ticker, period='6mo')

# Compute light signals:
# - is_st (from info.shortName)
# - market_cap, pe_ttm, pb
# - 5y revenue CAGR (from annual_income)
# - 5y net income CAGR
# - OCF/NI ratio (last 3 years average) — red flag #2
# - goodwill/equity (latest year) — red flag #4
# - 60d cumulative return — red flag #17
# - net_margin trend
# - debt/equity
```

For each, compute **initial score** (0-100) where:
- +20 for revenue CAGR > 15%
- +20 for ROE > 20% AND stable
- +15 for FCF/NI > 80%
- +15 for net cash position
- −30 for is_st
- −30 for OCF/NI < 50% (4y avg)
- −20 for goodwill/equity > 40%
- −20 for 60d return > 50% (overheated signal)
- −15 for negative 3-year revenue CAGR
- −10 for debt/assets > 50%

Output: candidates ranked by initial_score, with red flag pre-tags.

### Stage 3: 短列表 (15-20 tickers)

- **BUY short-list (~10)**: highest initial_score AND no preliminary HIGH red flags
- **AVOID short-list (~10)**: lowest initial_score OR preliminary HIGH red flags

Some candidates may overlap (e.g., 综合分数高但触发某红旗); resolve by routing to
the more-confident side. Deduplicate.

Total short-list: ~15-20 tickers.

### Stage 4: 深度扫描 (WebFetch each — the slow stage)

For each short-listed ticker, run the **full 18-category red flag scan** from
`references/red-flags.md`. Specifically:

1. WebFetch new浪 announcement page: `https://vip.stock.finance.sina.com.cn/corp/go.php/vCB_AllBulletin/stockid/<6digit>.phtml`
   - 搜近 90 天公告标题，匹配 red flag #1 (业绩雷) / #5 (减持) / #6 (解禁) / #7 (质押) / #9 (审计) / #11 (高管离任) / #12 (定增) keywords
2. yfinance-derived red flags (already computed in Stage 2): #2 (OCF/NI) / #3 (应收 / 存货) / #4 (商誉) / #13 (ST) / #17 (估值过热)
3. WebFetch 财联社 / 第一财经 for industry policy (#14) and 海外/地缘 (#15) on tickers in relevant sectors
4. WebFetch 雪球热度榜 (xueqiu.com/hots) for #18 (散户狂热) — optional

For each candidate, fill in:

```yaml
red_flags_checked: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]  # 全 18 项
red_flags_triggered:
  - category: "5 大股东减持"
    severity: HIGH
    evidence: "2026-05-22 公告：控股股东拟减持 1.5% 总股本"
    detection_method: "WebFetch:新浪财经公告页"
  - category: "17 估值过热"
    severity: MEDIUM
    evidence: "近 60 日累计涨幅 +52%，PE 38x（5y 90 分位）"
    detection_method: "yfinance + 自算"
```

This is verbose by design — forces auditable, fact-based red flag identification.

### Stage 4b: Evidence collection (★ v0.7 强制要求)

After red flag scan, build the `evidence_log` for each short-listed candidate
**before** writing the picks card. This catches the common failure mode where
thesis narrative uses unverified market consensus ("Tesla Optimus 供应链",
"NVIDIA 代工", "HVDC 跨界") as if they were facts.

For each candidate, build evidence_log with:

1. **All yfinance fields used** → type=hard
   ```yaml
   - type: hard
     source: "yfinance.stock_info.trailingPE"
     content: "25.3"
     used_in: [thesis]
   ```

2. **All WebFetch findings** → type=hard
   ```yaml
   - type: hard
     source: "WebFetch:https://vip.stock.finance.sina.com.cn/.../300274.phtml"
     content: "2026-05-11 解禁相关公告 (规模未读全文)"
     date: "2026-06-08"
     used_in: [red_flag, why_now]
   ```

3. **Any market consensus / industry common knowledge** → **type=soft (显式)**
   ```yaml
   - type: soft
     source: "market_consensus"
     content: "公司是 Tesla Optimus 量产供应链 — 市场广泛报道，但公司公告未直接披露 Tesla 客户名称"
     used_in: [thesis]
   ```

4. **Pending verify** — 公告 metadata 拿到但未读全文
   ```yaml
   - type: pending_verify
     source: "WebFetch:<url>"
     content: "2026-04-25 Q1 业绩预告 (标题已确认, 具体数字未读)"
     used_in: [why_now]
   ```

**Minimum bar**: each pick needs ≥3 hard entries. lock_picks.py rejects fewer.

**Rule of thumb for hard vs soft**:
- 财务比率, 价格涨幅, 估值倍数 → HARD (yfinance)
- 具体公告日期 + 标题 → HARD (WebFetch)
- "公司是 X 龙头" → 至少 yfinance.stock_info.longBusinessSummary 引一段才算 HARD; 否则 SOFT
- "受益于 X 主题" → SOFT unless 公司在公告/IR 网页明确披露过该业务规模
- "Tesla / NVIDIA / Apple 的供应商" → SOFT unless 公司年报/招股书直接披露客户名 (大多数情况只能 SOFT)
- "行业政策即将出台" / "美联储将降息" → SOFT
- "解禁/减持/质押公告" → HARD (公告日期 + URL 已拿到), 但具体规模可能 PENDING_VERIFY 如果未读全文

### Stage 4c: AI supply-chain boom review (★ v1.1 强制要求)

For every AI candidate, build `ai_supply_chain_review` according to
`references/ai-supply-chain-boom-framework.md`.

Minimum output:

```yaml
ai_supply_chain_review:
  status: complete | partial | unavailable
  structural_horizon_years: 3-5
  chain_node: hbm | advanced-packaging | substrate | pcb | optical | server | power | cooling | semiconductor-equipment | software | robotics | other
  ai_demand_evidence: []
  bottleneck_evidence: []
  customer_capacity_evidence: []
  financial_translation: {}
  bottleneck_score: {}
  bottleneck_score_total: 0
  scarcity_premium: {}
  structural_verdict: structural_buy | watch | avoid
  thesis_breakers: []
  open_checks: []
```

Required source checks:

1. Hyperscaler / AI leader demand:
   - NVIDIA, Microsoft, Alphabet, Meta, Amazon, Broadcom, TSMC, SK hynix.
2. Bottleneck evidence:
   - TrendForce / SEMI / WSTS / IEA / Uptime / company filings.
3. Company-level translation:
   - annual report, quarterly report, IR record, utilization, capex, customer
     qualification, backlog, gross margin, or product ASP.

Scoring:

- `ai_bottleneck_score >= 85`: strategic bottleneck; scarcity premium can be large.
- `70-84`: strong AI node; BUY/WATCH depends on price.
- `55-69`: plausible beneficiary; no multiple override unless near-term earnings are also improving.
- `<55`: theme exposure only; normal valuation discipline applies.

### Stage 4d: Target price valuation (★ v1.0 + v1.1 强制要求)

For every AI / market candidate that may become BUY or WATCH, build
`target_price_review` according to `references/valuation-target-price.md`.

Minimum output:

```yaml
target_price_review:
  status: research_grade | provisional | unavailable
  horizon_months: 12
  current_price: 0.0
  base_target: 0.0
  target_range: [0.0, 0.0]
  upside_pct: 0.0
  selected_method:
    primary: PE | PEG | PB_ROE | EV_EBITDA | EV_Sales | DCF | SOTP | other
    cross_checks: []
    justification: ""
  eps_forecast_bridge:
    latest_actual: {}
    fy2026_forecast: {}
    fy2027_forecast: {}
    bridge_logic: {}
    confidence: high | medium | low
  research_report_matrix:
    status: complete | partial | unavailable
    reports: []
  consensus_cross_check: {}
  revision_triggers:
    upward: []
    downward: []
  evidence_grade: {}
  open_checks: []
```

Rules:

- Do not issue a precise target price from `current_price / forward_PE` alone.
- If Wind / Choice / FactSet / LSEG I/B/E/S / Bloomberg is unavailable, write this explicitly and use `provisional`.
- Broker research is never copied into the repo. Store only metadata and short paraphrased assumptions.
- If a BUY has less than 15% upside to base target, it must have `evidence_quality=high`; otherwise route to WATCH.
- For AI candidates, attach `structural_option_value` and `ai_scarcity_premium` when the chain review allows a scarcity premium.
- For AVOID candidates, build `valuation_red_flag` with fair-value/risk range, method, and reversal conditions.

### Stage 5: 选 5 AVOID + 5 AI + 5 全市场 (顺序 important)

**v1.1 selection order**: AVOID 先选 → AI 结构性瓶颈 BUY 再选 → 全市场 BUY 最后选 (在
非 AI 剩余 + 已 ban 的 AI ticker 之外)。**目的：确保 3 list 不重叠** + 让最严重
的警惕信号先被锁定再做 BUY 配对。

#### Step 5a: AVOID 5 支 (任意主题, 高知名度 × 严重度优先)

- 必要条件: `red_flags_triggered` ≥ 1 HIGH 或 ≥ 2 MEDIUM
- 排序: 红旗严重度 + 投资者关注度（市值 + 近期媒体提及频率）
- 取前 5。5 只覆盖不同 red flag 类型 (不要 5 只都是 OVERHEATED)
- 标 `theme` 字段为信息性（哪个 theme 出问题）

#### Step 5b: AI Picks 5 支 (限 AI_THEMES, 不在 AVOID list)

- AI_THEMES = {ai-compute, advanced-packaging, pcb-substrate, optical-cpo, semi-equipment, data-center-power, cooling, robotics, domestic-software}
- 候选来源: Stage 3 BUY 候选中 theme ∈ AI_THEMES 的
- 必要条件: `red_flags_triggered` 0 HIGH + ≤1 MEDIUM
- 排除: 已在 AVOID list 中的 ticker
- 排序: initial_score × strategy multiplier × AI bottleneck multiplier
  - CHOKEPOINT ×1.2（小盘隐性卡点优先）
  - QUALITY_COMPOUNDER ×1.0
  - VALUE ×1.0
  - SPECIAL_SITUATION ×1.1
  - AI bottleneck score ≥85 ×1.25
  - AI bottleneck score 70-84 ×1.10
  - AI bottleneck score <55 ×0.70
- 取前 5
- 5 只之间 sub-theme (compute / advanced packaging / PCB / optical / power / cooling / software / robotics) 分布合理

#### Step 5c: Market Picks 5 支 (非 AI_THEMES, 不与 AI / AVOID 重叠)

- 候选来源: Stage 3 BUY 候选中 theme ∉ AI_THEMES (or watchlist 无主题股)
- 必要条件: 同 AI picks
- 排除: 已在 AVOID 或 AI Picks 中的 ticker
- 排序: 同 AI picks
- 取前 5
- sector 分布合理（覆盖 energy / solid-state-battery / military-tech /
  biotech-ai / low-altitude / watchlist consumer 等）

#### 不足 5 支的处理

如果某类候选 < 5 (因 red flag 过滤太多 or 候选池窄)，**诚实输出 fewer**:
- AVOID < 5: 警告"该周风险信号较少, 高位过热不集中"
- AI < 5: 警告"AI 板块普遍过热 / 不符合 BUY 标准"
- 市场 < 5: 警告"非 AI 板块缺乏明确 catalyst"

不要凑数。

### Stage 6: 输出 + Lock + HTML + Track

写**三份**文件:

1. `predictions/picks/<yyyy-mm-dd>/picks_<HHMMSS>.yaml` — structured 15-name card (per `templates/picks_card.yaml`, 3 lists)
2. `predictions/picks/<yyyy-mm-dd>/picks_<HHMMSS>.raw.md` — human-readable Markdown report
3. **v0.8 NEW**: `predictions/picks/<yyyy-mm-dd>/picks_<HHMMSS>.html` — self-contained interactive HTML report

Lock command:
```powershell
python tools/lock_picks.py predictions/picks/<yyyy-mm-dd>/picks_<HHMMSS>.yaml
```

This validates:
- All required LOCK fields filled
- `ai_picks` ≤ 5 + each theme ∈ AI_THEMES
- `market_picks` ≤ 5 + each theme ∉ AI_THEMES
- ai_picks ∩ market_picks ticker set = ∅
- `avoid_picks` ≤ 5 + each ≥1 HIGH or ≥2 MEDIUM red flag
- Every entry has `red_flags_checked = [1..18]` + valid `evidence_log` (≥3 hard)
- Every AI / market entry has `target_price_review` with status, EPS bridge,
  research-report matrix, valuation method, target range, and revision triggers
- Every AI entry has `ai_supply_chain_review` with bottleneck score, chain node,
  demand/bottleneck/customer evidence, financial translation, scarcity premium
  policy, structural verdict, and thesis breakers
- Every AVOID entry has `valuation_red_flag.fair_value_or_risk_range`
- Computes SHA-256 of raw.md, records playbook_version
- Appends 15 rows to `predictions/picks_index.csv`

HTML render command (after lock):
```powershell
python tools/render_picks_html.py predictions/picks/<yyyy-mm-dd>/picks_<HHMMSS>.yaml
```

生成 self-contained HTML — 含 3 个 section + 每只 pick 可点击展开 (详细分析 /
证据链 / red flag 扫描)。HTML 文件可发邮件或打开浏览器查看。

Tracking: `update_tracking.py` 自动跟踪 ai_picks + market_picks + avoid_picks
全部 15 个 ticker 的 T+1/5/10/20 表现。

---

## 4. Judgment Framework

### 4.1 BUY confidence calibration
- `≥ 0.7`: 多 strategy 共振 + 红旗全清 + 明确近期 catalyst；AI 类还需瓶颈分 >=70
- `0.5-0.7`: 主 strategy 强 + 红旗清 + 中期 catalyst
- `0.4-0.5`: 偏好但 catalyst 弱 → 仍可入 BUY，标 "long-term hold"
- `< 0.4`: 不应进 BUY 清单（即使 red flag 都清，也是 "watch")

注意: 老 v0.5 茅台例（confidence 0.42 / quality compounder）在 v0.6 应该输出为
**BUY (long-term hold)**，因为 quality strategy 不要求 catalyst clarity。

### 4.2 AVOID confidence calibration
- `≥ 0.7`: 多红旗共振（如减持 + 估值过热 + 题材熄火）
- `0.5-0.7`: 单条 HIGH 红旗 + 关注度高
- `0.4-0.5`: 2 个 MEDIUM 红旗
- `< 0.4`: 不应进 AVOID 清单

### 4.3 Forward-test parameters
- **prediction_horizon_days**: 20 (T+20)
- **benchmark**: 000300.SH (沪深 300)
- **BUY 成功**: T+20 个股相对沪深 300 超额 > 0
- **AVOID 成功**: T+20 个股相对沪深 300 落后（即"规避有理"）— 个股跑输沪深 300 即算 AVOID 成功

### 4.4 失效 / 提前结案
- 个股停牌 > 5 个交易日
- ST 警示
- 出现新的重大 thesis-breaking 事件
- 对 AI BUY：核心瓶颈解除、关键客户砍单、产能爬坡失败、或 capex/折旧吞掉毛利率
- 对 AVOID：如个股出现明显反转（如重磅利好公告 + 涨停），可标 AVOID 失败提前结案

---

## 5. Output Format

### 5.1 Structured (picks_card.yaml)

See `templates/picks_card.yaml` — 含 LOCK area + 15 entries (5 AI + 5 market + 5 AVOID),
each with required fields including `red_flags_checked` (all 18) and
`red_flags_triggered` (specific list with evidence).

### 5.2 Human-readable (raw.md)

```markdown
# Weekly Picks — <YYYY-MM-DD>

## 市场背景 (1 段)
<最近 7 天宏观 + 板块强弱 + 任何重大事件>

## 看好 5 支 (BUY)

### 1. <TICKER> <NAME> | Strategy: <CHOKEPOINT/QUALITY/VALUE/SPECIAL>
**Thesis**: <一句话>
**Why now**: <一句话；近期 catalyst 或估值机会>
**Key tracking indicator**: <T+20 期间最该看什么>
**Red flag scan**: 全 18 项 checked, 0 triggered (or 1 LOW: <description>)
**Risk**: <一句话 - 最大不确定性>
**Confidence**: 0.XX

### 2. ...

## 警惕 5 支 (AVOID)

### 1. <TICKER> <NAME> | 主要原因: <category from red-flags.md>
**Concern**: <一句话>
**Evidence**: <具体证据 + 来源>
**Why investor 容易踩**: <为什么散户容易追这只 - 例如龙头股+热门题材>
**What would reverse**: <一句话 - 什么信号说明 AVOID 失败>
**Confidence**: 0.XX

### 2. ...

## 附录: 候选池规模 / 短列表 / 入选过程
<透明记录：候选池多大、短列表怎么得到、为什么这 5 BUY/5 AVOID>

## Open checks
- ...
```

---

## 6. Pre-Test Discipline

**前瞻测试期间禁止修改本 playbook**。任何修改记入 `PLAN.md` §9.4 并标注"样本污染"。

定期 review (月度 `/review`):
- BUY 命中率 (T+20 跑赢沪深 300 比例)
- AVOID 规避率 (T+20 跑输沪深 300 比例)
- 综合 alpha = BUY 命中率 - (1 - AVOID 规避率)

---

## 7. Common Failure Modes (避免)

- ❌ Skipping red flag scan to save tokens — 暴雷漏检的代价远大于 token
- ❌ Putting popular hot stocks in BUY just because they're trending — strategy 是 "看好"，不是"跟风"
- ❌ Putting obscure microcaps in AVOID — 散户都没听过的票，警告价值低
- ❌ 5 BUY 全是同一板块 / 同一 strategy — 缺乏多样性
- ❌ AVOID 描述含 "可能" / "或许" 不给具体证据 — AVOID 必须有 hard evidence
- ❌ 跳过 stage 4 直接用 stage 2 结果 — 没有 WebFetch 的 picks 必然漏掉公告类 flag

---

## 8. V1 vs V2 Coverage

V1 (current v0.6 with v0.5 data layer):
- 强 red flag 覆盖 (财务驱动 + 公告驱动)
- 弱: 龙虎榜、公募季报、即时资金流（V2 deferred）

V2 (境内 MCP 后):
- 加入 LHB 数据 → 散户狂热 #18 量化
- 加入公募季报 → smart money 维度恢复
- 加入即时资金流 → 短期 BUY/AVOID 信号更敏锐
- 可以做 short-term picks (T+5)
