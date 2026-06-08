# Daily LHB (龙虎榜) Analysis Playbook

> **⚠️ V1 DEPRECATED (since PLAN v0.5)**
>
> 龙虎榜数据通过 AKShare 走东财接口，不可从境外访问。V1 状态：deferred 到 V2。
> `/lhb` slash command 当前提示 deprecated 并退出。
>
> 本文件保留作为 V2 实现的完整参考。
>
> ---

> Triggered by: `/lhb`
> Frequency: 交易日盘后 17:00+ (LHB 数据通常在 17:00-18:00 披露)
> Output: 当日异常席位组合识别 + 个股观察清单

This playbook is for **short-term signal generation** based on 龙虎榜 + 资金流
+ 板块强度 combined evidence. It does NOT directly lock predictions — it
outputs candidates for user to optionally run `/analyze <ticker>` (short-term).

---

## 0. Applicable Scope

Use after market close on a trading day to:
- Identify "机构买 + 游资跟" pattern stocks
- Identify "业绩预告 + LHB" dual-signal stocks
- Find theme breakthroughs visible in LHB

Don't use for:
- Long-term thesis — use `/analyze`
- Pre-market analysis — LHB data not yet available

---

## 1. Required Data

### 1.1 Must
- 当日全市场 LHB — Via `data.ashare.lhb.lhb_daily(today)`
- 当日板块资金流排名 — Via `data.ashare.fund_flow.sector_fund_flow()`
- 当日涨停 / 跌停统计 — Via Tushare or AKShare 涨跌停接口

### 1.2 Should
- 最近 5 天该股 LHB 历史 — Via `data.ashare.lhb.lhb_history_for_ticker`
- 当日上榜个股的资金流 — Via `data.ashare.fund_flow.stock_fund_flow`
- 当日新发布的业绩预告 / 业绩快报 — Via Tushare (`forecast`)

### 1.3 Optional
- 知名游资营业部白名单（自己维护在 `data/ashare/lhb_seat_whitelist.yaml`，TODO）

---

## 2. Workflow

### Step 1 — Pull today's LHB
- 拉今日全市场 LHB
- 如果空 (e.g., 非交易日或数据未更新)，提示用户稍后再来

### Step 2 — Classify each listed stock by trigger reason
LHB 触发原因（上榜原因字段）：
- 涨幅偏离 +7% (典型涨停 / 大涨)
- 跌幅偏离 -7%
- 振幅 15%
- 换手率 20%
- 连续 3 日累计涨跌幅偏离 20%
- 连续 3 日累计涨跌幅 ±30% (创业板 ±20%)

分类后，重点关注:
- **首板涨停且上榜** — 资金博弈最激烈
- **连板高度（2板+）** — 情绪标
- **跌停且 LHB** — 机构 / 游资抢筹？还是踩踏？

### Step 3 — Seat classification
对每只上榜股，调出买卖前 5 营业部：
- **机构专用席位** — 标注为"机构专用"的（最有效的机构信号）
- **知名游资席位** — 需对照白名单识别（短线效应大但持续性差）
- **量化席位 / 沪股通深股通席位** — 大资金但目的不明
- **散户营业部** — 普通营业部（噪声）

打标签：
- M-buy: 机构买入
- M-sell: 机构卖出
- Y-buy: 知名游资买入
- Y-sell: 知名游资卖出
- N-buy/sell: 普通 / 散户

### Step 4 — Identify high-signal patterns

| Pattern | 含义 | 后续观察 |
|---|---|---|
| 2+ M-buy, 0 M-sell | 机构集体抢筹 | 较强信号 |
| 1 M-buy + 多 Y-buy | 机构带队，游资跟进 | 中等信号 |
| M-buy + 业绩预告超预期 | 机构 + 业绩双轨 | 强信号 |
| 全是 Y-buy + Y-sell | 游资互博 | 短线博弈，胜率低 |
| M-sell + 全是 Y-buy | 机构出货游资接刀 | 警惕 |
| M-buy + 跌停 | 机构在低位抢筹 | 可能反转信号但需确认 |
| 连续 3 日 LHB | 资金博弈激烈 | 短期波动大 |

### Step 5 — Sector context
- 该股所在板块今日资金净流入排名
- 板块涨幅排名
- 同板块今日上榜股数量
- 板块龙头表现

板块强 + 个股强信号 = 较高胜率
板块弱 + 个股强信号 = 警惕（接最后一棒）

### Step 6 — Cross-reference recent disclosures
对每只候选股查近 30 天公告：
- 是否近期发布业绩预告 / 重大合同 / 政策利好 / 客户认证？
- 是否近期有减持 / 解禁 / 增发？
- 是否近期被 ST / 监管关注？

### Step 7 — Apply hard risk filters
任一命中即从候选剔除：
- [ ] 30 天内大额解禁
- [ ] 6 个月内大股东减持
- [ ] 商誉 / 净资产 > 50%
- [ ] 股权质押 > 80% 且股价大跌
- [ ] ST / 退市风险
- [ ] 当前价格已在 60 日 95% 分位以上（过热）

### Step 8 — Output the observation list

```markdown
# LHB Analysis — yyyy-mm-dd

## Market Context
- 涨停股: N 只
- 跌停股: N 只
- 板块涨幅榜前 3: ...
- 板块资金净流入前 3: ...

## High-Signal Candidates (按信号强度排序)

### 1. <ticker> <name>
- **Trigger**: <连板高度 / 涨停 / 跌停 / 异动>
- **Seat pattern**: <M-buy ×2, Y-buy ×3, no M-sell>
- **Sector**: <板块名> (today: +X%, 资金净流入 ¥XB)
- **Disclosure cross-ref**: <近期是否有业绩预告 / 合同 / 政策>
- **Risk flags**: <若有 mild flag>
- **Signal level**: 强 / 中 / 弱
- **Suggested next**: `/analyze <ticker>` (short_term)

### 2. ...

## Notable Risks (今日值得警惕的票)
- <ticker>: M-sell 集中 / 业绩雷预警 / 连续涨停打开
```

### Step 9 — Archive
保存观察清单到 `watchlist/history/yyyy-mm-dd/lhb.md`，方便后续 review。

---

## 3. Output Files

- stdout 给用户
- `watchlist/history/yyyy-mm-dd/lhb.md` 归档
- **不锁定预测**。锁定需要单独 `/analyze <ticker>` 完整流程。

---

## 4. Notes

### 4.1 LHB 信号的真实强度有限
A 股龙虎榜数据已经被深度博弈。营业部识别本身就有伪装（知名游资也会换席位）。**单独 LHB 不构成 thesis**，必须配合：
- 基本面证据
- 板块强度
- 近期催化

### 4.2 机构席位识别
"机构专用"是交易所明确标注，比游资白名单可靠。但也有局限：
- 不同机构无法区分（公募 vs 私募 vs 自营）
- 机构席位也会被滥用

### 4.3 游资白名单
若要维护，建议存在 `data/ashare/lhb_seat_whitelist.yaml`：
```yaml
known_youzi:
  - 上海溧阳路
  - 华泰深圳益田路
  - 华鑫上海茂名路
  - 东方财富拉萨
  - ...
```
初期可以不维护，由 Claude 临时判断。

### 4.4 短期预测胜率管理
LHB 衍生的短期预测胜率结构性偏低。即使所有信号都对，T+5 胜率也很难超过 60%。**保持预测稀缺性**，宁可少出。

### 4.5 前瞻测试纪律
不修改本 playbook 在测试期内。
