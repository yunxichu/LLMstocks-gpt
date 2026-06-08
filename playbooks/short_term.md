# Short-Term Stock Analysis Playbook

> **⚠️ V1 DEPRECATED (since PLAN v0.5)**
>
> This playbook depends on China-mainland-only data sources (龙虎榜, 主力资金流,
> 涨停板梯队, 个股资金流) which are NOT accessible from overseas environments
> (USA / VPN'd). All endpoints route through 东财 (East Money), which blocks
> non-Mainland IPs.
>
> **V1 status (since v0.5)**: short-term analysis is DEFERRED. `/analyze` defaults
> to `long_term` only. Do not invoke this playbook until V2 brings a境内 MCP
> proxy (see PLAN.md §1 V2 roadmap).
>
> This file is kept as a complete reference for the V2 implementation.
>
> ---

> Triggered by: `/analyze <ticker>` (短期视角) or `/lhb` follow-up
> Output: a short-term stock card written to `predictions/locked/<date>/<prediction_id>.yaml`
> + accompanying raw markdown reasoning.

This playbook is for **A-share specific** short-term (T+5) analysis driven by
龙虎榜 / 资金流 / 题材联动 / 催化剂. It is distinct from `long_term.md`:

- Long-term looks at chokepoint + financials over T+20 (vs 中证 800)
- Short-term looks at flow + sentiment + catalyst over T+5 (vs 中证 1000)

References:
- `references/research-rubric.md` — for confidence calibration (use cautiously; short-term is noisy)
- `references/pattern-library.md` — Category B patterns (公募抱团扩散, 业绩预告超预期, 龙虎榜机构留痕, 龙头-补涨)
- `references/a-share-data-sources.md` — LHB rules, news triage

---

## 0. Important Disclaimers (Read First)

**Short-term A-share trading has structurally low alpha for non-professionals.**
You are competing with quant funds, dedicated 游资 desks, and HFTs.

This playbook is a **research tool**, not a get-rich shortcut. Use it to:
- Build intuition for short-term flows
- Validate or refute short-term signals before getting excited
- Generate disciplined predictions for forward-test validation

The default verdict should lean toward **"insufficient signal" or "watch only"**.
Concrete buy-side signals should be rare.

**Hard rule**: every short-term card must have explicit `invalidation` 
conditions. "Buy and hope" is not allowed.

---

## 1. Applicable Scope

Use when:
- User asks `/analyze <ticker>` and specifically wants short-term view
- After `/lhb` flags a ticker as having interesting flow
- User suspects a fast catalyst (业绩预告 / 政策 / 突发事件)

Do NOT use when:
- The query is fundamental thesis-driven — use `long_term.md`
- 股价已经连续 4+ 个涨停 — too late for entry analysis, treat as risk monitoring
- 已经触发 ST / 退市警示 — skip entirely

---

## 2. Required Data

### 2.1 Must fetch
- **个股最近 60 日量价** — 收盘 / 量能 / 振幅 / 涨跌停状态. Via `data.ashare.price.stock_daily`.
- **个股最近 30 日资金流** — 主力净流入持续性, 5/10/20 日累计. Via `data.ashare.fund_flow.stock_fund_flow`.
- **个股最近 30 日 LHB 上榜记录** — 包括营业部买卖详情. Via `data.ashare.lhb.lhb_history_for_ticker`.
- **当日全市场 LHB** (if querying after market close) — 找同板块上榜股. Via `data.ashare.lhb.lhb_daily`.
- **板块资金流** — 该股所在板块今日 + 近 5 日资金净流入. Via `data.ashare.fund_flow.sector_fund_flow`.
- **个股最近 90 天公告** — 业绩预告 / 减持 / 解禁 / 重大合同 / 异动公告. Via Tushare MCP (`anns`).
- **最近 6 个月解禁数据** — 30 天内解禁规模. Via Tushare (`share_float`).
- **基准 entry_close** — 中证 1000 (000852.SH) on `entry_close_date`. Via `data.ashare.benchmark`.
- **个股 entry_close** — 最近交易日收盘 (前复权).

### 2.2 Should fetch
- **同板块涨幅排名** — 板块强度，龙头 vs 补涨股位置.
- **业绩预告 / 业绩快报** — 是否最近发布或将发布.
- **大股东 / 高管最近 6 个月减持公告** — 短线负面信号.
- **互动易最近回复** — 是否有管理层透露的微小信号.

### 2.3 Optional
- **历史 LHB 营业部白名单匹配** — 知名游资营业部 vs 机构专用席位识别. (需自行维护营业部白名单).
- **同概念股联动数据** — 板块内涨幅前 5 名.

---

## 3. Analysis Workflow

### Step 1 — Verify state and freshness
- Confirm 当前未停牌、未 ST。
- 当前股价在 60 日什么分位？(高位 / 中位 / 低位)
- 最近 5 日是否有涨停 / 跌停？打开情况？

### Step 2 — Classify the trigger
What made the user (or you) want to analyze this stock short-term?
- (A) **龙虎榜异动** — LHB 上榜后被发现
- (B) **资金流异常** — 主力连续多日大幅净流入
- (C) **公告/业绩催化** — 业绩预告超预期、重大合同、政策利好
- (D) **题材联动** — 同板块龙头大涨，跟涨股
- (E) **技术形态** — 突破 / 缩量上涨 / 阶段底部

不同 trigger 适用不同子流程。如果分不清楚 trigger，**默认输出 watch-only**。

### Step 3 — Flow analysis
- 主力 5 日 / 10 日 / 20 日净流入累计
- 持续性：连续多少天主力净流入为正？
- 比例：主力净流入 / 当日成交额是多少（>5% 算显著）？
- 大单 + 超大单 vs 中单 + 小单：是大资金主导还是散户主导？

**陷阱**：单日大幅净流入不是信号，连续才是。3 日内多次反复，往往是博弈中。

### Step 4 — LHB seat analysis (if applicable)
如果近 30 日上榜过：
- **机构专用席位**（标注为"机构专用"）— 这是最有效的机构信号
- **知名游资席位**（需对照白名单：上海溧阳路、华泰深圳益田路、华鑫上海茂名路、东方财富拉萨等）— 短线效应大但持续性差
- **散户营业部**（普通营业部 + 不在游资白名单）— 信号噪声大
- 当日总买卖净额是机构主导还是游资主导？
- 同一只票连续上榜 = 资金博弈激烈 = 短期波动大

**关键判断**：
- 机构买 + 游资跟 = 较强短期信号
- 机构卖 + 游资买 = 警惕（游资接刀）
- 全是游资 = 短线博弈，胜率低
- 机构连续买 = 强信号但要看资金量是否真大

### Step 5 — Sector / theme strength
- 该股所在板块今日涨幅排名（前 5？前 10？）
- 板块龙头今日表现（涨停？大涨？开始回落？）
- 该股在板块内的位置（龙头？二线？补涨？最末）

**A-share short-term truth**: 板块强度比单股强度更可靠。在弱板块里抓涨停股，往往是接最后一棒。

### Step 6 — Catalyst freshness
近 90 天公告与新闻：
- 是否有具体的、未充分定价的催化（业绩预告超预期 / 重大订单 / 政策 / 重组）？
- 催化剂时点 — 是已发生但未被市场充分消化 / 即将发生 / 已经被炒过？
- 催化兑现路径清晰吗？

**陷阱**：把"老催化"当"新催化"。如果消息已经在板块内传开，往往龙头已涨完，跟涨股进入风险区。

### Step 7 — Risk filters (硬约束)
**任何一项命中即降低 confidence 至 < 0.4 或不出 buy 信号**：
- [ ] 30 天内有大额解禁（占流通股 > 5%）？
- [ ] 6 个月内有大股东 / 高管减持公告？
- [ ] 控股股东股权质押比例 > 80% 且最近股价跌幅 > 15%？
- [ ] 商誉 / 净资产 > 50%（潜在减值雷）？
- [ ] 当前股价位于 60 日 90% 分位以上（已涨太多）？
- [ ] 连续 3 个交易日涨停未开板（追涨胜率低）？
- [ ] 近 6 个月业绩预告与最终披露偏差 > 30%？
- [ ] 板块今日资金净流出？
- [ ] 公司性质属于 ST / *ST / 退市风险警示？

### Step 8 — Score using the rubric (modified for short-term)
短期用简化评分，重点 4 维 (各 0-5)：
1. **Flow signal strength** — 资金流 / LHB 信号强度
2. **Catalyst clarity** — 催化剂明确度 + 新鲜度
3. **Sector tailwind** — 板块强度
4. **Risk filter** — 风险硬约束有几项命中（反向计分）

满分 20。建议阈值：
- ≥ 14: 较强信号，可出短期 long 思路
- 10-13: 弱信号，watch only
- < 10: 不出信号

### Step 9 — Define invalidation
**这是短期 playbook 最重要的一步**。
明确什么时候算"我错了"。短期失效条件要具体、可观察：
- 跌破某个具体日均线（如"跌破 10 日均线"）
- 涨停板被严重打开（"涨停被打开后未能 V 回"）
- 板块次日资金净流出 > X 亿
- 龙虎榜机构次日上榜卖出
- 公告反转（业绩雷 / 监管 / 减持）

**不要写**："止损 -5%" 这种价格止损 — 太机械。要写**信号**层面的失效条件。

### Step 10 — Write the card
Fill `templates/stock_card.yaml`:
- `prediction_type: short_term`
- LOCK area: prediction_horizon_days = 5, benchmark = "000852.SH"
- `short_term` section: every applicable subsection
- `long_term: null`
- `invalidation` field is mandatory and specific

写入 raw.md，然后 lock。

---

## 4. Judgment Framework

### 4.1 Confidence calibration (短期偏保守)
- `confidence ≥ 0.7`: 多个信号共振（机构 LHB + 主力连续净流入 + 板块强 + 明确催化）+ 风险过滤无命中
- `confidence 0.5-0.69`: 主要信号成立，但某些维度弱
- `confidence < 0.5`: 不要 lock 为 buy 类预测；output 为 watch only 或拒绝

### 4.2 Prediction horizon
- Default: `prediction_horizon_days: 5`
- Benchmark: `000852.SH` (中证 1000)
- 不要做 < 3 天的预测（噪声主导）
- 不要做 > 10 天的"短期" — 改用 long_term playbook

### 4.3 Success / failure criteria
- **success_criteria** default: "T+5 收盘相对中证 1000 超额 > 0%"
- **failure_criteria** default: "T+5 个股绝对收益 < -8% 或相对中证 1000 < -5%"
- 失败标准比中长期严格（短线下行快）

### 4.4 Invalidation conditions
至少 3 条，必须具体可观察。示例：
- "次日开盘缺口 > -3% 且 30 分钟内未补回"
- "跌破 10 日均线"
- "板块次日大幅回落，板块涨幅排名跌出前 20"
- "T+1 LHB 机构席位反向上榜（净卖）"
- "公告披露重大利空"

---

## 5. A-Share Short-Term Specific Notes

### 5.1 涨跌停制度
- 主板 ±10%, 创业板 / 科创板 ±20%, 北交所 ±30%, ST 股 ±5%
- 涨停封板后无法买入（除非打开）；预测当日涨停的股价"目标"是无意义的
- 持续涨停后突然打开 = 多空换手剧烈，警惕

### 5.2 T+1 settlement
- 当日买入次日才能卖
- 短期预测时点最好选盘后，给次日盘前留判断空间

### 5.3 集合竞价
- 9:25 开盘价由集合竞价决定
- 大幅高开后转跌往往是诱多

### 5.4 涨停封单 & 龙头判定
- 真正的板块龙头是首板涨停最早、连板最高、封单最大的那只
- 如果你分析的不是龙头，胜率显著降低
- "首板/二板/三板" 概念决定接力难度

### 5.5 主力 vs 散户 fund flow 解读
- AKShare 的"主力净流入"是按单笔金额分类（大单 > 100 万、超大单 > 1000 万）
- 主力 + 超大单为正且持续 = 大资金介入
- 主力为负但股价上涨 = 散户拉抬，警惕
- 主力为正但股价下跌 = 大资金筹码出货
- 注意：盘中数据有滞后；盘后数据更稳

---

## 6. Lock-In & Output

Same as `long_term.md` Section 5 (Lock-In Requirements) — all LOCK area fields 
required, prediction_id format `<6digit>-<yyyymmdd>-<HHMMSS>-st`.

After lock, prediction is immutable. T+5 evaluation runs automatically via 
`tools/update_tracking.py`.

---

## 7. Common Failure Modes (短期特有)

- 追涨连板高位股 — 接最后一棒
- 把游资接力当机构进入
- 板块龙头大涨后追跟涨股
- 业绩预告披露当日追涨 — 兑现可能已经定价
- 把单日资金净流入当持续信号
- 忽略 30 天内解禁 / 减持窗口
- 在主板交易日盘中下单（错过集合竞价）
- 把"我看好"当 buy 信号 — 这是 thesis 不是 trade

---

## 8. Pre-Test Discipline

前瞻测试期间禁止修改本 playbook（参见 `long_term.md` §7）。
