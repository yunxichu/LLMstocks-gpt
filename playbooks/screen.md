# Weekly Screen Playbook

> **v0.6 status: ABSORBED into `/picks`**. The functionality of "weekly candidate
> proposal" is now part of `playbooks/weekly_picks.md` Stage 1 + Stage 5. Use
> `/picks` as the primary weekly entry point.
>
> This file is preserved as a reference for the candidate-pool construction
> logic. `/screen` slash command currently routes to legacy behavior; consider
> using `/picks` for the official 5 BUY + 5 AVOID deliverable.

---

# Weekly Screen Playbook (LEGACY — see banner above)

> Triggered by: `/screen`
> Frequency: 每周日晚 (optional — 个人研究节奏可调)
> Output: 5-10 个值得 `/analyze` 深入的候选

> **v0.5 note**: 自 v0.5 起，不再做"5000 只 A 股全市场扫描"。yfinance 没有全
> 市场 A 股快照接口，且对个人研究来说，5000 只全扫是过度的。本 playbook 改为
> **watchlist-based + theme-driven + US-leader-driven** screening。如果你想做
> 全市场预筛，需要从公开源拉一份 a_share seed CSV（详见 `data/web/universe.py`
> 错误提示）放在 `config/a_share_seed.csv`。

---

## 0. Applicable Scope

Use weekly to:
- Surface new long-term candidates from 4 sources: existing watchlist signals, new theme catalysts, US-leader-driven rotations, and public news flow
- Propose 5-10 candidates for deeper `/analyze`
- Update `watchlist/watchlist.yaml` (running list)

Don't use for:
- Single-stock analysis — use `/analyze`
- Short-term — V1 deprecated

---

## 1. Required Data

### 1.1 Must
- `watchlist/watchlist.yaml` — current running list (may not exist yet on first run)
- `config/themes.yaml` — theme registry
- US sector leaders' recent price action — `data.web.us_stocks.stock_history` (NVDA / AMD / TSLA / AVGO / MU / ASML / TSM / etc.)

### 1.2 Should fetch (via Claude WebFetch)
- 财联社 (cls.cn) — last 7 days 主流财经新闻
- 第一财经 (yicai.com)
- 21 世纪经济报道 (21jingji.com)
- 政策动态 — 发改委、工信部新发布文件
- Industry-specific sources (SemiWiki, TrendForce, IFR, etc.)

### 1.3 Optional
- 巨潮资讯 "今日新增公告" (WebFetch http://www.cninfo.com.cn/new/disclosure)
- A 股 sector ETF performance for theme rotation hints

---

## 2. Workflow

### Step 1 — Review current watchlist
- Load `watchlist/watchlist.yaml`
- For each entry, check status:
  - `candidate` — proposed but not yet `/analyze`'d
  - `analyzed` — has a locked prediction
  - `rejected` — explicitly skipped
- Identify:
  - Candidates standing > 2 weeks未 analyze → 提示用户 either /analyze 或 reject
  - Analyzed entries with predictions closing soon → 提示用户 prepare for /review

### Step 2 — Scan US leaders for sector rotation hints
- For 8-12 representative US leaders (configurable list), fetch `stock_history(ticker, period='1mo')`
- Identify sectors with strong / weak 1-month performance
- Map US sectors → A-share themes via `config/themes.yaml`
- A US-leader rally with no A-share peer move can hint at rotation lag

Example mapping:
- NVDA / AMD / AVGO strong → A-share `ai-compute` / `optical-cpo` themes worth scanning
- TSLA / IDEX / NIDEC robotics moves → A-share `robotics` candidates
- ASML / LRCX / AMAT → `semi-equipment`

### Step 3 — Active theme detection from news flow
For each top theme in `config/themes.yaml`:
- Claude WebFetch 财联社 / 21 经济报道 search with theme keywords
- Count news-item density in last 7 days
- Tag themes with明显增长的报道频次 as "active"

Surface top 3 active themes for this week.

### Step 4 — Within-active-theme chokepoint search
For each active theme:
- Use `pattern-library.md` Category A patterns to identify what specific
  chokepoint node would benefit
- WebFetch 巨潮 / industry news to find Chinese companies operating at that node
- For 2-5 promising candidates per theme:
  - Validate ticker exists in yfinance (`stock_info` returns non-empty)
  - Quick check: market cap, sector, recent news, 是否 ST

### Step 5 — Catalyst-driven candidates (independent of theme)
WebFetch 巨潮资讯 for recent (last 7 days):
- 业绩预告 / 业绩快报披露 — filter by 扣非净利同比增速 > 50% AND vs guidance
- 重大合同公告
- 客户认证 / 资质获得公告

For each promising hit:
- Note ticker, the specific event, and projected revenue impact

### Step 6 — Apply hard exclude filters (manual since no batch API)
For each surfaced candidate (manual check via WebFetch + yfinance):
- [ ] 6 个月内大股东大幅减持公告? → exclude
- [ ] 30 天内大额解禁? → exclude
- [ ] 商誉 / 净资产 > 50%? → exclude
- [ ] 控股股东股权质押 > 80%? → exclude
- [ ] ST / 退市风险警示? → exclude

### Step 7 — Output the screen list

Maximum 10 candidates total. Less is better. Format:

```markdown
# Weekly Screen — yyyy-mm-dd

## Active Themes (top 3)
1. <theme_id> — <why active this week, with evidence>
2. ...

## US Leader Sector Hints
- <leader> +X% past month → <implied A-share theme>
- ...

## Candidates

### 1. <ticker> <name>
- **Theme**: <which theme>
- **Pattern**: <pattern_library.md category, e.g., A.2 Architecture Transition>
- **Why now**: <1 sentence>
- **Quick data**: 行业 / 市值 / sector
- **Catalyst signal**: <从哪里看到的, e.g., "巨潮 2026-06-05 业绩预告公告">
- **Risk flag**: <mild flags only; hard exclusions are filtered out>
- **Suggested next**: `/analyze <ticker>` for full long_term card

### 2. ...
```

### Step 8 — Update watchlist + archive
Append candidates to `watchlist/watchlist.yaml`:

```yaml
- ticker: 600519.SH
  added_on: <YYYY-MM-DD>
  added_by: weekly_screen
  rationale: <1 sentence>
  status: candidate  # candidate | analyzed | rejected | re-confirmed
  theme: ai-compute
  source_evidence: <URL or 巨潮 announcement ID>
```

Save the full screen report at `watchlist/history/<YYYY-MM-DD>/screen.md`.

---

## 3. Output Files

- `watchlist/history/<YYYY-MM-DD>/screen.md` — full report
- `watchlist/watchlist.yaml` — appended candidates

**不锁定预测**。锁定通过 /analyze <ticker> per candidate.

---

## 4. Notes

### 4.1 watchlist-based vs full-market screen
v0.5 的 watchlist-based 模式更适合 personal research，因为：
- 个人月度实际能 deep-analyze 的也就 5-20 只
- 全市场 5000 只 LLM 扫成本高 + 信号噪声大
- 主动 curation 比被动 screening 更聚焦

如果你之后想做全市场扫描，先 bootstrap `config/a_share_seed.csv`（详见
`data/web/universe.py` 注释），然后另写一个 `tools/full_market_screen.py`。

### 4.2 数量约束
最大 10 个候选。少而精。

### 4.3 与既有 watchlist 对比
已在 watchlist 的标的本周 signal 仍强 → 保留并标记 "re-confirmed N 周"
本周 signal 转弱 → 标 status: rejected 并写原因

### 4.4 与 /analyze 的关系
screen 出候选 → 用户决定 /analyze 哪些 → /analyze 才是 chokepoint 拆解
不要在 screen 阶段写出 thesis 细节。

### 4.5 前瞻测试纪律
前瞻测试期间不修改本 playbook。
