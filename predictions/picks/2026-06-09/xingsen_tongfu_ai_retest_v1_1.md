# 兴森科技、通富微电 AI 供应链框架重测 v1.1

> 日期：2026-06-09  
> 方法：`ai-supply-chain-boom-framework.md` + `valuation-target-price.md`  
> 价格基准：yfinance 2026-06-09 收盘  
> 输出性质：`provisional`，不构成投资建议；本次没有 Wind / Choice / Bloomberg / FactSet / LSEG I/B/E/S 授权一致预期终端。

---

## 0. 重测结论

| 股票 | 当前价 | 旧结论 | 新结论 | AI 瓶颈分 | 12M 基础目标 | 12M 合理区间 | 3-5Y 结构性牛市情景 |
|---|---:|---|---|---:|---:|---:|---:|
| 兴森科技 `002436.SZ` | 37.13 | AVOID / 不追 | near-term AVOID + structural WATCH | 59/100 | 29 | 24-32 | 45-55 |
| 通富微电 `002156.SZ` | 63.13 | WATCH / 不追 | WATCH+ / structural-buy candidate | 78/100 | 60 | 52-64 | 78-90 |

本次重测后，结论发生了两个变化：

1. **不再把 AI 链条高 PE 机械判死刑。** 如果是真瓶颈、且客户/产能/财务传导可验证，可以给稀缺性溢价。
2. **通富微电的评级明显高于兴森科技。** 通富已经从先进封装节点兑现到收入和利润；兴森仍处在 PCB/载板/FCBGA 期权兑现早期。

一句话：**通富微电是“已经进入 AI 瓶颈链条、但价格略提前”的标的；兴森科技是“AI PCB/载板期权很大、但财务兑现仍弱”的标的。**

---

## 1. AI 总需求和瓶颈证据

AI 供应链的底层假设现在更强，不是普通景气复苏：

- NVIDIA FY2027 Q1 收入 816 亿美元，同比增长 85%；Data Center 收入 752 亿美元，同比增长 92%；FY2027 Q2 收入指引 910 亿美元。
- Microsoft FY2026 Q3 披露 AI 年化收入超过 370 亿美元，同比增长 123%。
- Alphabet 披露 AI 需求超过可用供给，并把 2026 年资本开支指引到 1800-1900 亿美元。
- Meta 将 2026 年资本开支指引上调至 1250-1450 亿美元，并提到组件价格和数据中心成本上升。
- TrendForce 2026-04-30 指出，AI 竞争已经造成 3nm/2nm 晶圆和 2.5D/3D 先进封装瓶颈，CoWoS 紧张向上游设备、下游 substrate、PCB、HBM、SSD 等扩散。
- TrendForce 2026-04-15 指出，AI server 优先分配产能，导致通用服务器 PCB、CPU 等核心零部件交期拉长到近一年。
- Uptime Institute 2026 预测认为，数据中心开发商无法跑赢电力短缺，AI 负载增长会继续压迫电网。

这说明本轮 AI 不只是“芯片涨价”，而是：

```text
AI capex 爆发
-> GPU/ASIC/HBM/先进封装/PCB/光模块/电力/液冷同时吃紧
-> 真瓶颈节点可以享受稀缺性溢价
-> 但必须看到客户、产能、利用率、毛利率或扣非利润兑现
```

---

## 2. 兴森科技重测

### 2.1 AI 供应链位置

```yaml
ai_supply_chain_review:
  status: partial
  structural_horizon_years: "3-5"
  chain_node: "pcb / substrate"
  ai_demand_evidence:
    - "TrendForce: AI server 和通用服务器零部件交期拉长，PCB/CPU 供给紧张"
    - "TrendForce: NVIDIA 等提前锁定 substrate、PCB、HBM、SSD 等资源"
  bottleneck_evidence:
    - "1.6T 光模块产品板处于量产爬坡"
    - "FCBGA 封装基板处于小批量生产阶段"
    - "CSP 封装基板总产能约 5 万平方米/月，新扩产能爬坡较快"
  customer_capacity_evidence:
    - "公司披露 1.6T 光模块产品板同步开展多家客户验证导入"
    - "FCBGA 低层板良率超 95%，高层板良率超 90%"
  financial_translation:
    revenue_bridge: "2026Q1 收入 18.18 亿元，同比 +15.10%，说明景气已有收入传导"
    margin_bridge: "Q1 扣非归母净利 2817.39 万元，同比 +308.32%，但利润体量仍小"
    capex_or_depreciation: "在建工程和固定资产规模大，经营现金流为 -2.47 亿元，扩张阶段消耗现金"
    utilization_or_backlog: "CSP 产能高位、1.6T 量产爬坡；但 FCBGA 尚未规模化"
    evidence_grade: "hard / soft mixed"
  bottleneck_score:
    end_market_capex: 9
    node_bottleneck: 14
    architecture_lock_in: 11
    customer_capacity: 9
    financial_translation: 6
    supply_expansion_risk: 3
    capital_validation: 2
    rerating_optionality: 5
  bottleneck_score_total: 59
  scarcity_premium:
    multiple_override_allowed: false
    allowed_premium_to_normal_multiple: "0-15%，仅在 H1/H2 利润继续验证后才允许"
  structural_verdict: "watch"
```

### 2.2 为什么不是彻底 AVOID

按旧框架，兴森科技 37 元、2026E PE 约 148x、TTM PE 约 463x，很容易直接判 AVOID。

但新框架下，需要承认它确实有结构性期权：

- AI 服务器和光模块对高阶 PCB、HDI、IC 载板、测试板的需求正在扩散；
- 1.6T 光模块板已经进入量产爬坡；
- FCBGA 面向 CPU/GPU/FPGA/ASIC 等高算力芯片，有潜在重估空间；
- CSP/BT 载板产能利用率和需求比普通 PCB 更强。

所以它不是“无效题材”，而是 **结构性 WATCH**。

### 2.3 为什么近端仍然 AVOID / 不追

关键问题是财务传导太早期：

- 2026Q1 EPS 只有 0.01 元；
- 经营现金流 -2.47 亿元；
- Q1 归母净利 1874 万元，相对 629 亿元市值太小；
- FCBGA 仍处于小批量阶段，不是已经充分贡献利润；
- 股价 60 日涨幅约 56.9%，120 日约 70.7%，市场已经提前交易了 AI 期权。

### 2.4 估值重算

外部公开预测样本：

```text
2026E EPS 约 0.23-0.27
2027E EPS 约 0.39-0.44
2028E EPS 约 0.63-0.76
```

传统 12M 估值：

```text
near_term_value = 2027E EPS 0.44 × 60x = 26.4 元
```

AI 结构性期权：

```text
structural_bull_value = 2028/2029E EPS 0.90-1.00 × 50-55x = 45-55 元
probability_of_success = 35%
option_spread = 45 - 26.4 = 18.6
expected_option_value = 18.6 × 35% = 6.5
capex_cashflow_penalty = 3.5
ai_adjusted_base = 26.4 + 6.5 - 3.5 = 29.4 元
```

新目标：

```yaml
target_price_review:
  current_price: 37.13
  near_term_base: 26
  ai_adjusted_base: 29
  target_range_12m: [24, 32]
  structural_bull_3_5y: [45, 55]
  verdict: "near-term AVOID + structural WATCH"
```

### 2.5 兴森科技新动作建议

- 新仓：仍然不追。
- 已持有：可以从“完全规避”改成“小仓位结构性观察”，但不适合重仓。
- 触发买入条件：
  - 价格回到 28-32 元；
  - 或 2026H1 EPS/扣非利润明显超预期；
  - 或 FCBGA 出现规模量产/明确客户订单；
  - 或经营现金流转正且毛利率抬升。
- 触发上修：
  - 2027E EPS 从 0.44 上修到 0.60 以上；
  - FCBGA 从小批量转入规模收入；
  - 光模块 PCB 客户验证转为批量订单。

---

## 3. 通富微电重测

### 3.1 AI 供应链位置

```yaml
ai_supply_chain_review:
  status: partial
  structural_horizon_years: "3-5"
  chain_node: "advanced-packaging"
  ai_demand_evidence:
    - "TrendForce: 2.5D/3D advanced packaging 是 AI 供应链核心瓶颈"
    - "TrendForce: CoWoS 紧张向 substrate、packaging materials 和零部件扩散"
    - "AI server / HBM / GPU / ASIC 推动封测和先进封装需求上行"
  bottleneck_evidence:
    - "通富微电 2026Q1 收入 74.82 亿元，同比 +22.80%"
    - "2026Q1 归母净利 3.29 亿元，同比 +224.55%"
    - "2026Q1 扣非归母净利 1.72 亿元，同比 +64.78%"
    - "公开研报摘要显示公司先进封装产能扩张，2026 年资本开支约 91 亿元"
    - "公开摘要提到槟城工厂 3nm 多芯片产品封装通过验证"
  customer_capacity_evidence:
    - "公司长期与 AMD 合作是公开研报反复提及的核心逻辑，但订单比例仍按 soft evidence 处理"
    - "中高端产品收入提升已在 Q1 财报体现"
  financial_translation:
    revenue_bridge: "Q1 收入 +22.80%，高于传统封测复苏斜率"
    margin_bridge: "扣非净利 +64.78%，说明中高端产品和利用率正在传导"
    capex_or_depreciation: "2026 年资本开支约 91 亿元，既是扩张证据，也是折旧/现金流压力"
    utilization_or_backlog: "公开摘要指先进封装扩产，财报已体现中高端产品收入增长"
    evidence_grade: "hard / soft mixed"
  bottleneck_score:
    end_market_capex: 9
    node_bottleneck: 18
    architecture_lock_in: 13
    customer_capacity: 13
    financial_translation: 11
    supply_expansion_risk: 5
    capital_validation: 4
    rerating_optionality: 5
  bottleneck_score_total: 78
  scarcity_premium:
    multiple_override_allowed: true
    allowed_premium_to_normal_multiple: "15-30%"
  structural_verdict: "structural_buy candidate"
```

### 3.2 为什么通富明显优于兴森

通富微电的优势是：**先进封装节点更靠近 AI 加速器核心瓶颈，且已经进财报。**

对比兴森：

| 项目 | 兴森科技 | 通富微电 |
|---|---|---|
| AI 节点 | PCB / substrate / FCBGA 期权 | OSAT / advanced packaging |
| 瓶颈强度 | 中高 | 高 |
| 财务兑现 | 低利润基数，Q1 EPS 0.01 | Q1 EPS 0.2168，扣非利润增长 |
| 现金流 | Q1 经营现金流 -2.47 亿元 | Q1 经营现金流 9.42 亿元，但同比下降 |
| 资本开支风险 | 扩产现金消耗明显 | 大 capex + 折旧压力，但收入规模更大 |
| 结构性判断 | WATCH | structural-buy candidate |

### 3.3 估值重算

基本输入：

```text
当前价 = 63.13
2025 EPS = 0.80
2026E EPS 公开预测约 1.00-1.05
2027E EPS 参考约 1.20-1.30
2028E EPS 参考约 1.50+
```

传统近端估值：

```text
normal_value_1 = 2026E EPS 1.02 × 50x = 51.0
normal_value_2 = 2027E EPS 1.22 × 42x = 51.2
normal_base ≈ 52
```

AI 稀缺性溢价：

```text
ai_bottleneck_score = 78
allowed_multiple_premium = 15-30%
AI-adjusted PE = 50x × 1.18 ≈ 59x
ai_adjusted_base = 2026E EPS 1.02 × 59x ≈ 60.2
```

结构性牛市情景：

```text
2028/2029E EPS 1.50-1.65 × 52-55x = 78-90
```

新目标：

```yaml
target_price_review:
  current_price: 63.13
  normal_base: 52
  ai_adjusted_base: 60
  target_range_12m: [52, 64]
  structural_bull_3_5y: [78, 90]
  verdict: "WATCH+ / structural-buy candidate"
```

### 3.4 通富微电新动作建议

- 新仓：63 元附近不适合重仓追，但不再归入 AVOID。
- 已持有：可以继续持有核心仓，重点看 2026H1 扣非利润和先进封装订单兑现。
- 加仓区：
  - 55 元以下：风险收益明显改善；
  - 56-60 元：适合分批观察；
  - 63 元以上：只适合在 EPS 明确上修后追加。
- 直接转 BUY 条件：
  - 2026E EPS 上修到 1.25 元以上；
  - 扣非净利增速持续高于收入增速；
  - 先进封装 capex 转化为收入和毛利，而不是只带来折旧；
  - 经营现金流保持为正，资产负债率不继续恶化。
- 下修条件：
  - Q2/Q3 扣非利润不及预期；
  - capex 折旧压力导致毛利率下降；
  - 先进封装扩产行业内过快，价格竞争提前出现；
  - 大客户订单或技术验证不及预期。

---

## 4. 二者重测排序

```text
1. 通富微电：WATCH+ / structural-buy candidate
   - 真瓶颈分 78
   - 先进封装节点更硬
   - 财务兑现更直接
   - 当前价接近 12M 合理区间上沿，不追但要重点跟踪

2. 兴森科技：near-term AVOID + structural WATCH
   - 真瓶颈分 59
   - PCB/载板/FCBGA 期权存在
   - 财务兑现弱，现金流压力高
   - 当前价高于 AI-adjusted 12M base，不追，等证据或价格
```

---

## 5. 模型输出

```yaml
run_output:
  date: "2026-06-09"
  model_framework: "LLMstocks-gpt v1.1 AI supply-chain boom"
  status: "provisional"
  decisions:
    - symbol: "002436.SZ"
      name: "兴森科技"
      current_price: 37.13
      ai_bottleneck_score: 59
      near_term_view: "AVOID / 不追"
      structural_view: "WATCH"
      ai_adjusted_12m_base_target: 29
      target_range_12m: [24, 32]
      structural_bull_3_5y: [45, 55]
      key_reason: "AI PCB/载板期权存在，但 FCBGA 尚未规模化，Q1 EPS 和现金流不足以支撑 37 元附近追价。"
      action: "不追；28-32 元或 H1 明显超预期再重新评估。"
    - symbol: "002156.SZ"
      name: "通富微电"
      current_price: 63.13
      ai_bottleneck_score: 78
      near_term_view: "WATCH+"
      structural_view: "structural-buy candidate"
      ai_adjusted_12m_base_target: 60
      target_range_12m: [52, 64]
      structural_bull_3_5y: [78, 90]
      key_reason: "先进封装是真 AI 瓶颈，且 Q1 收入、扣非利润已有兑现；但现价已在 12M 合理区间上沿。"
      action: "持有优先；55-60 元分批更舒服；63 元以上等 EPS 上修确认。"
```

---

## 6. 资料来源

- NVIDIA FY2027 Q1 results: `https://investor.nvidia.com/news/press-release-details/2026/NVIDIA-Announces-Financial-Results-for-First-Quarter-Fiscal-2027/default.aspx`
- Microsoft FY2026 Q3 results: `https://www.microsoft.com/en-us/investor/earnings/fy-2026-q3/press-release-webcast`
- Alphabet 2026 equity/capex press release: `https://s206.q4cdn.com/479360582/files/doc_news/2026/Jun/01/attachments/2026-June-Alphabet-Equity-Capital-Raise-Press-Release-PDF.pdf`
- Meta Q1 2026 results: `https://investor.atmeta.com/investor-news/press-release-details/2026/Meta-Reports-First-Quarter-2026-Results/`
- TrendForce 2026-04-30: `https://www.trendforce.com/presscenter/news/20260430-13028.html`
- TrendForce 2026-04-15 中文新闻: `https://www.trendforce.cn/presscenter/news/20260415-13012.html`
- Uptime Institute 2026 data center predictions: `https://uptimeinstitute.com/about-ui/press-releases/uptime-institute-announces-five-data-center-predictions-report-for-2026`
- 兴森科技 2026Q1: `https://disc.static.szse.cn/disc/disk03/finalpage/2026-04-25/8fa0241f-fda6-4e04-b7ea-2d4e1515f3e9.PDF`
- 兴森科技 2026-05-08 投资者关系活动记录: `https://static.cninfo.com.cn/finalpage/2026-05-08/1225285130.PDF`
- 通富微电 2026Q1: `https://disc.static.szse.cn/disc/disk03/finalpage/2026-04-30/50eb95fe-4e0a-4d69-a60d-9a7529443ab5.PDF`
- 通富微电 2025 年报: `https://static.cninfo.com.cn/finalpage/2026-04-17/1225112762.PDF`
- 通富微电公开研报摘要：`https://stock.finance.sina.com.cn/stock/go.php/vReport_Show/kind/search/rptid/829919735247/index.phtml`
- yfinance: 2026-06-09 收盘行情、估值、目标价 proxy。
