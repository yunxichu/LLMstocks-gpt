# A-Share Research Rubric

Use this rubric when:
- Producing a formal long-term stock card (`/analyze`)
- Comparing multiple candidates within a basket (`/screen`, `/theme`)
- Doing a periodic `/review` to assess how well past predictions held up

Adapted from Serenity's 15-dimension chokepoint rubric; A-share-specific
dimensions added (policy alignment, disclosure transparency).

> **v1.1 note**: AI-related candidates must add the dedicated
> `ai_supply_chain_review` from `ai-supply-chain-boom-framework.md`. The
> original chokepoint rubric remains useful, but AI names now receive a
> separate 0-100 bottleneck score before valuation.

---

## Scoring scale

Score each dimension `0` to `5`. Use half points when useful. Total possible: **80** (16 dimensions × 5).

### Interpretation

| Total | Interpretation |
|---|---|
| 55+ | Compelling chokepoint candidate; still verify current facts |
| 40-54 | Worth deeper due diligence |
| 25-39 | Watchlist only unless new evidence appears |
| < 25 | Mostly narrative |

These ranges are heuristics, not thresholds. A single low score in a critical
dimension (e.g., evidence quality = 0) should override a high total.

---

## Scorecard (16 dimensions)

| # | Dimension | 0-1 | 2-3 | 4-5 |
|---|---|---|---|---|
| 1 | **End-demand shock** | Vague theme | Clear demand wave, uncertain timing | Specific near-term buildout, strong capex/customer pull |
| 2 | **Chain specificity** | Generic supplier | Plausible chain node | Exact BOM/process/material/equipment node identified |
| 3 | **Layer depth** | Obvious first-order winner only | Second-order node identified | Multi-layer map with overlooked 2nd/3rd-order chokepoint |
| 4 | **Bottleneck strength** | Many substitutes | Some concentration or qualification friction | Scarce capacity, high switching cost, long qualification, quasi-monopoly, critical material |
| 5 | **Architecture lock-in** | Commodity exposure | Some design-specific exposure | Tied to a new architecture/standard that changes supplier economics |
| 6 | **Evidence quality** | Social claims only | Company materials + secondary support | 公告/年报/客户文件/政府文件/财报电话会 + 多重佐证 |
| 7 | **News/disclosure freshness** | No recent disclosure check | Some recent news checked | Recent 巨潮/SSE/SZSE 公告 (via WebFetch) + news triaged |
| 8 | **Mispricing** | Already obvious/expensive | Some undercoverage or valuation gap | Small/ignored asset with large future relevance and plausible rerating path |
| 9 | **Demand-to-financial translation** | Theme cannot move numbers | Plausible but rough revenue/margin impact | Concrete unit, revenue, backlog, or consensus-beat path |
| 10 | **Bayesian update quality** | No update criteria | Some positive/negative evidence listed | Clear prior, posterior direction, and thesis-breaking evidence |
| 11 | **Financial durability** | Weak balance sheet or heavy dilution | Mixed but survivable | Balance sheet + backlog + cash flow reduce blow-up risk |
| 12 | **Catalyst path** | None | Medium-term proof points | Near-term earnings / customer launch / standard transition / 业绩预告 / index event |
| 13 | **Downside control** | Binary or fraud-like | Volatile but analyzable | 重置价值/账面现金/订单/战略价值 limits downside |
| 14 | **Reflexivity/liquidity risk** | Microcap mania only | High volatility but real thesis | Liquidity/ownership considered without being the core thesis |
| 15 | **Institutional rotation** (v0.5: observable proxy) | No capital-flow view | Plausible sector rotation | US leaders rerated, A-share peers lag; media-observable rotation signal |
| 16 | **Policy alignment** (A 股特化) | Pure thematic; no policy backing | Some policy mention | 明确的政策清单/补贴/国家战略支持，且能影响公司收入 |
| 17 | **Disclosure transparency** (A 股特化) | History of restatements / 业绩雷 / 关联交易频繁 | Clean but limited segment detail | 财报清晰 / 业绩预告与最终披露一致 / 互动易回复实质 / 无重大违规 |

> Numbering goes 1-17 but only 16 active rows (the old #17 "Smart money quality"
> is removed in v0.5; #18 "Disclosure transparency" was renumbered to #17).

---

## A-Share-Specific Failure Modes

Reject or heavily discount ideas where:

- 把"政策利好"当 chokepoint 的全部（最常见错误，政策只是必要条件）
- 把题材联动当 alpha（联动是热度，不是 chokepoint）
- 忽略大股东 / 高管减持公告
- 忽略解禁压力（30 日内解禁特别注意）
- 把游资龙虎榜买入当机构介入
- 业绩预告与最终财报历史性偏差大（业绩雷高风险股）
- 公司互动易回复模糊 / 充满 boilerplate 的（治理质量弱）
- 商誉占净资产比例过高（隐藏减值雷）
- 控股股东股权质押比例 > 80% 且股价持续下跌
- 频繁定增 / 关联交易频繁
- 无法回答 "why this company, not the obvious giant?"
- 唯一边缘是某网红 / 大 V 提过
- 仅靠"市场会注意到"作为催化剂

---

## AI Mega-Cycle Overlay (v1.1)

Use this overlay for any candidate tagged:

`ai-compute`, `advanced-packaging`, `pcb-substrate`, `optical-cpo`,
`semi-equipment`, `data-center-power`, `cooling`, `robotics`,
`domestic-software`.

Do not score AI names only with traditional PE discipline. First ask whether
the company controls a scarce node in the AI infrastructure buildout.

Required overlay:

| Overlay Item | Required Question |
|---|---|
| Capex pull | Which AI leader or hyperscaler capex/result proves demand is rising now? |
| Exact node | Is this HBM, CoWoS/advanced packaging, substrate, PCB, optical, server, power, cooling, equipment, or software? |
| Bottleneck | Is capacity constrained, pre-booked, qualification-limited, power-limited, or architecture-limited? |
| Customer/capacity proof | Does the company disclose utilization, capex, orders, qualification, customer type, or product ramp? |
| Financial bridge | How does the node change revenue, ASP, gross margin, EPS, cash flow, or ROIC? |
| Scarcity premium | Can the stock deserve a multiple premium versus normal sector valuation? Why? |
| Thesis breaker | What would prove AI demand is not translating to this company? |

Decision impact:

- `ai_bottleneck_score >= 85`: high PE alone should not force AVOID; evaluate
  structural option value and current price versus bull case.
- `70-84`: strong WATCH/BUY candidate if near-term valuation is not already
  near the structural bull case.
- `55-69`: do not give a multiple override unless earnings are also improving.
- `<55`: treat as normal theme exposure; strict valuation applies.

---

## Trade Disclosure Labels (when extracting others' disclosures)

This project does NOT trade. All system output is "thesis_only" by convention.

But when extracting other investors' disclosures (大 V 持仓、基金季报、北向季度数据),
use these labels:

| Label | Trigger language (中) | Include as trade? |
|---|---|---|
| Explicit long | 买入 / 持有 / 重仓 / 主仓 | Yes |
| Add/increase | 加仓 / 增持 / 加大持仓 | Yes |
| Sell/reduce | 减持 / 卖出 / 减仓 / 清仓 | Yes |
| No position | 不持有 / 已经退出 | Yes, as non-holding |
| Thesis-only | 看好 / 长期看好 / 推荐 / 目标价 X 元 | No |
| Basket disclosure | 这一类我都持有 / 这个赛道我配了 | Yes, low confidence |
| Retrospective | 我之前重仓过 / 去年加的 | Yes, timing uncertain |

Never conflate "看好" with "持有".

---

## Stock Card Output Template

Use `templates/stock_card.yaml` as the canonical structure. For human-readable
reasoning, include this as part of the raw markdown alongside the YAML:

```markdown
# [Ticker] [Name] — Chokepoint Analysis

## Verdict
[One-sentence thesis + confidence + tradeable_now or watchlist]

## Market Context
- Listing venue / 货币 / 最近披露期 / 新闻窗口

## Demand Shock
- End market / Timing / Why now

## Supply-Chain Map
Buyer/system -> module -> component -> material -> [this company's node]

## Chokepoint
- Scarcity / Switching cost / Architecture / Capacity constraints

## Evidence
| Claim | Source | Strength |
|---|---|---|

## News and Disclosure Update (近 6 个月)
| Date | Source | Item | Impact | Strength | Follow-up |
|---|---|---|---|---|---|

## Bayesian Update
- Prior / Positive evidence / Negative evidence / Posterior / Thesis-breaking evidence

## Financial Quality & Valuation
[ROE / FCF / 负债 / PE 分位 / 估值信号]

## Smart Money
[基金季报变动 / QFII / 社保 / 名牌经理]

## Research Consensus
[评级方向 / 目标价中位 / 与当前价空间]

## Mispricing
[当前市场框架 vs 我们的框架 / 估值缺口]

## Market Microstructure
[覆盖 / 流动性 / 持股约束 / 反身性]

## Catalysts
- Near-term: ...
- Medium-term: ...

## Risks & Disconfirmers
- Technical substitution / Customer concentration / Dilution / Regulatory / 减持 / 解禁 / ST 风险

## Tracking Indicators
- ...

## Reassessment Triggers
- ...

## Open Checks (要再核实的事实)
- ...

## Trade Disclosure
thesis_only (个人研究，不持仓)
```

---

## Evidence Priorities (A-Share, v0.5)

Prefer primary/current sources in this order. **All accessible from overseas
via Claude WebFetch + yfinance (no China-mainland API needed).**

1. **交易所披露** (via WebFetch) — SSE/SZSE 公告, 巨潮资讯 (cninfo.com.cn), 公司年报/半年报/季报
2. **公司 IR + 财报数据** — yfinance financials/cashflow/balance_sheet
3. **互动平台** (via WebFetch) — 上证 e 互动 (sns.sseinfo.com), 深交所互动易 (irm.cninfo.com.cn)
4. **政策文件** (via WebFetch) — 发改委 (ndrc.gov.cn) / 工信部 (miit.gov.cn) / 行业主管部门
5. **客户/供应商技术文档** (via WebFetch) — 产品页, BOM, qualification 语言
6. **财经媒体** (via WebFetch) — 第一财经 (yicai.com)、财联社 (cls.cn)、21 经济报道 (21jingji.com)；作为线索
7. **美股龙头对照** — yfinance (NVDA / TSLA / AMD / AVGO etc.) for sector context
8. **美股 13F** (via WebFetch) — sec.gov EDGAR for top investor holdings in 中概股
9. **社交媒体** — 雪球、微博、股吧；仅作线索

**Deprecated in v0.5** (no longer used): Tushare API, AKShare 东财接口（含研报评级、龙虎榜、主力资金流、公募季报重仓、QFII 持仓）。

---

## Minimum Live Analysis Standard

Before issuing a current view on a company:

1. 验证 ticker、市场、最新披露季度
2. 检查最近 3-6 个月官方披露（小盘股或快速变化板块 12 个月）
3. 检查是否有定增 / 减持 / 解禁 / 重大合同 / 监管事件
4. 至少一个能验证供应链角色的来源
5. 明确写出未解决的疑问，不要用叙述填补
