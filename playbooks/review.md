# Forward-Test Review Playbook

> Triggered by: `/review`
> Frequency: 每月初 + 阶段 2 末（15 个交易日测试窗口结束）
> Output: 客观复盘报告 + Playbook 改进建议（不立即改 playbook）

> **v0.8 evaluates FOUR tracks separately**:
> 1. **AI picks track** (PRIMARY v0.8): `/picks` 的 ai_picks 胜率 (T+20 跑赢沪深 300)
> 2. **Market picks track** (PRIMARY v0.8): `/picks` 的 market_picks 胜率
> 3. **AVOID picks track** (PRIMARY v0.8): `/picks` 的 avoid_picks 规避率 (T+20 跑输沪深 300)
> 4. **Single-stock track** (legacy v0.5): `/analyze` 单股 long_term 预测;
>    与 picks tracks 分开统计
>
> 综合 alpha = 胜率_AI + 胜率_market + 规避率_avoid - 2 (相对随机基线 0.5)
>
> short-term 部分 deferred (V2). 本 playbook 仅评估 long-term (T+20 vs 沪深 300)。
>
> **v0.6 picks (picks_192556)** 用 legacy buy_picks 字段，与 v0.8 picks 不混合;
> 评估时单独统计为"legacy buy"。

This is the **objective accountability** loop for forward-test discipline. You
read locked predictions + tracking records, compute metrics, cluster successes
and failures, and propose (but don't apply) playbook improvements.

**Critical**: this playbook never modifies locked predictions or tracking
data. Read-only.

---

## 0. Applicable Scope

Use to:
- Monthly: see what happened to recent predictions
- After 15-day forward-test window: trigger 阶段 3 (Playbook tuning)
- Before deciding whether to update a playbook (informs but doesn't decide)

Don't use to:
- Edit existing predictions
- Justify cherry-picking successful predictions
- Evaluate short-term (V1 deprecated)

---

## 1. Required Data

### 1.1 Must
- `predictions/locked/**/<id>.yaml` — all locked predictions
- `predictions/tracking/<id>/d*.json` — tracking records
- `predictions/index.csv` — fast index

### 1.2 Should
- Benchmark history for 沪深 300 — `data.web.benchmark.benchmark_history('000300.SH')`
- Current trading calendar — `data.web.calendar.today_or_previous_trading_day()`

---

## 2. Workflow

### Step 1 — Load all closed predictions
A prediction is **closed** when:
- `tracking/<id>/d<horizon>.json` exists, OR
- ANY tracking record has `invalidated: true`

For open predictions, include in "in-flight" section but don't include in metrics.

### Step 2 — Compute aggregate metrics (separated by track)

**Picks track (v0.6 primary)** — read `predictions/picks_index.csv` + tracking:

```
对每条 picks_index 记录：
  - 读 predictions/tracking/<picks_id>--<ticker>/d20.json
  - 提取 excess_return_cum

按 verdict 分两组：
  BUY group:
    N_buy = closed BUY 数 (有 d20 记录或 invalidated)
    胜率_BUY = (excess > 0 的 BUY 数) / N_buy   ← BUY 应该跑赢
    平均超额_BUY = mean(excess)
  
  AVOID group:
    N_avoid = closed AVOID 数
    规避率_AVOID = (excess < 0 的 AVOID 数) / N_avoid   ← AVOID 应该跑输
    AVOID 平均规避幅度 = mean(-excess)（取负，正值表示规避有理）

综合 alpha = 胜率_BUY + 规避率_AVOID - 1
  > 0: picks 有 alpha
  = 0: 随机水平
  < 0: 反向都更准
```

**Single-stock track (v0.5 legacy)** — read `predictions/index.csv` + tracking:

```
N = 已 closed long-term 预测数
N_invalidated = 中途失效数
N_evaluated = N - N_invalidated

胜率 = (excess_return_cum > 0 的预测数) / N_evaluated
平均超额收益 = mean(excess_return_cum)
中位超额收益 = median(excess_return_cum)
最大单笔回撤 = min(excess_return_cum)
标准差 = std(excess_return_cum)
IR (annualized proxy) = (mean / std) * sqrt(252 / horizon_days)
```

Read excess_return_cum from `tracking/<prediction_id>/d20.json`.

**注意**：v0.5 lock (如老茅台预测) 在 v0.6 review 中**分开统计**，不混入
picks 平均。v0.5 框架是 chokepoint-only，v0.6 是 multi-strategy + red flag，
不是同一回事。

### Step 3 — Output the metrics table

```markdown
# Forward-Test Review — yyyy-mm-dd

## Period covered
- Picks files: <list of picks_id reviewed>
- Single-stock locks reviewed: <list of prediction_id reviewed>
- Evaluation window: T+20 vs 沪深 300

## Picks Track (PRIMARY, v0.6)

### BUY picks
| Metric | Value |
|---|---|
| Closed | N_buy |
| Invalidated | N_inv (X%) |
| Evaluated | N |
| **胜率 (T+20 超额>0)** | X% |
| 平均超额 | +X% |
| 中位超额 | +X% |
| 最大单笔回撤 | -X% |
| 按 strategy 分: CHOKEPOINT 胜率 | X/Y |
| 按 strategy 分: QUALITY 胜率 | X/Y |
| 按 strategy 分: VALUE 胜率 | X/Y |
| 按 strategy 分: SPECIAL 胜率 | X/Y |

### AVOID picks
| Metric | Value |
|---|---|
| Closed | N_avoid |
| Evaluated | N |
| **规避率 (T+20 超额<0)** | X% |
| 平均规避幅度 (-excess 取正) | +X% |
| 平均损失幅度（若按 AVOID 类买入）| -X% |
| 按 primary_concern 分: OVERHEATED | X/Y |
| 按 primary_concern 分: EARNINGS_RISK | X/Y |
| 按 primary_concern 分: DILUTION | X/Y |
| 按 primary_concern 分: MANAGEMENT | X/Y |

### Combined alpha
| Metric | Value |
|---|---|
| 综合 alpha = 胜率_BUY + 规避率_AVOID - 1 | X |
| > 0 picks 有 alpha; ≈ 0 随机水平; < 0 反向更准 | - |

## Single-Stock Track (LEGACY, v0.5)

(同 v0.5 表格，分开评估老 long_term 单股 lock，不混入 picks 平均)
```

### Step 4 — Decision rule (前置阈值，事后不可改)

**Picks track** (PRIMARY)：
- 胜率_BUY > 55% AND 规避率_AVOID > 55%: **picks 有 alpha** → 阶段 3 微调
- 胜率_BUY > 55% but 规避率_AVOID ≈ 50%: **看好侧准，警惕侧弱** → 重审 red flag 触发标准
- 胜率_BUY ≈ 50% but 规避率_AVOID > 55%: **警惕侧准，看好侧弱** → 重审 BUY strategy 评分
- 胜率_BUY ≈ 50% AND 规避率_AVOID ≈ 50%: **整体无 alpha** → 反思方法论，重做
- 综合 alpha < -0.1: **反向更准** → 严重 bug

**Single-stock track** (legacy, 仅供参考):
- 平均超额 > 0 AND 胜率 > 55%: 信号有效
- 平均超额 < 0 AND 胜率 ≈ 50%: 信号无效

### Step 5 — Failure case clustering
对所有 evaluated 但 excess < 0 的预测：
- 按 catalyst type 聚类 (chokepoint / 政策 / 业绩 / 题材)
- 按 confidence bucket 聚类 (高 ≥ 0.75 / 中 0.55-0.74 / 低 < 0.55)
- 按 theme/sector 聚类
- 按 invalidation_conditions 是否触发但未提前结案

找共性。

### Step 6 — Success case clustering
对 excess > 0 且达到 success_criteria 的预测：
- 同样聚类
- 找共性：什么类型的预测在 v0.5 playbook 下最准

### Step 7 — Generate playbook improvement proposals
基于失败 + 成功的共性，提出 1-3 条 playbook 修改建议（**不立即应用**）

每条建议必须有失败 / 成功案例支撑（引用 prediction_id）。

### Step 8 — Output the review report
保存到 `watchlist/history/<yyyy-mm-dd>/review.md`。

---

## 3. Hard Discipline

### 3.1 不要修改 locked 预测
Locked 预测就是 locked。

### 3.2 不要事后挑成功的说
所有 evaluated 预测都进入统计。

### 3.3 invalidation 触发严格执行
触发即结案，不再继续等 horizon。

### 3.4 metric 标准前置定义
胜率、超额、IR 的算法写死在本 playbook。要改算法，先改 playbook + commit + 标注，
下一轮才能用新算法。

### 3.5 改 playbook 必须经过 review 流程
不要在 review 之外随便改 playbook。改完后等下一个评估周期验证。

---

## 4. Notes

### 4.1 样本量小时
首轮 review N 可能只有 5-20。统计意义弱。结论写为"初步看 / 趋势倾向"，不要写为"已证明"。

### 4.2 跨牛熊样本
多轮 review 累积样本后再下大结论。

### 4.3 与 PLAN.md 联动
- 重大决策（信号无效 → 重做 playbook）记入 PLAN §9.3 已决策
- Playbook 改动记入 §9.4 变更日志
- 新发现的风险记入 §10 风险登记册
