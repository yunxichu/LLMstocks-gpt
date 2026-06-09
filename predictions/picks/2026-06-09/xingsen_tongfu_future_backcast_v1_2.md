# 兴森科技、通富微电 Future-Backcast 重测 v1.2

> 日期：2026-06-09
> 方法：先构建 2028-2030 AI 世界，再倒推当前供应链节点和公司
> 价格基准：yfinance 2026-06-09 收盘
> 输出性质：`provisional`，不构成投资建议

---

## 0. 先定义几年后的 AI 世界

这次不从“今天这家公司估值多少”开始，而从 2028-2030 年 AI 世界倒推。

我的基础假设：

```text
AI 从训练大模型为主
-> 走向 always-on inference、reasoning、agent、video、enterprise workflow、robotics
-> AI 数据中心变成高功率密度的工业基础设施
-> GPU + 自研 ASIC + HBM + 先进封装成为主流算力架构
-> 集群性能取决于 memory bandwidth、packaging、substrate/PCB、optical/networking、power、cooling
-> 中国 AI 基础设施会更重视国产链条和可替代供应
```

这个未来世界里，真正会变大的不是一个单点，而是一整条基础设施链：

| 未来 AI 世界必须变大的东西 | 对应供应链节点 | 当前 A 股映射 |
|---|---|---|
| GPU/ASIC 训练 + 推理集群 | HBM、先进封装、晶圆、测试 | 通富微电、长电科技、长川科技等 |
| Rack-scale AI 服务器 | PCB、连接器、电源、液冷、整机 | 沪电股份、胜宏科技、工业富联等 |
| 1.6T/3.2T 网络 | 光模块、硅光、光器件、光模块 PCB | 中际旭创、新易盛、天孚通信、兴森科技等 |
| 高功率密度数据中心 | 变压器、开关、UPS、HVDC、储能、液冷 | 思源电气、金盘科技、英维克等 |
| 国产 AI 基础设施 | 国产封测、载板、设备、软件 | 通富微电、兴森科技、中微公司、金山办公等 |

核心判断：**如果几年后的 AI 是一个巨大的、持续运行的推理和 agent 基础设施，那么先进封装、电力/液冷、HBM/载板/PCB/光互联会比普通消费电子周期更值得给长期估值溢价。**

---

## 1. Future-Backcast 排序结论

| 股票 | 当前价 | Future-backcast 分 | AI 瓶颈分 | 新结论 | 12M 目标 | 12M 区间 | 3-5Y 结构性基础/牛市 |
|---|---:|---:|---:|---|---:|---:|---:|
| 通富微电 `002156.SZ` | 63.13 | 84/100 | 80/100 | 长期分批 BUY / 近端 WATCH+ | 66 | 56-72 | 90-115 |
| 兴森科技 `002436.SZ` | 37.13 | 67/100 | 63/100 | 结构性 WATCH+ / 近端不追 | 32 | 26-36 | 55-70 |

这次的结论相对 v1.1 再调整：

- **通富微电上调**：如果从 2028-2030 AI 世界倒推，先进封装是核心基础设施节点。通富不是“只等回调的观察票”，而是可以纳入长期分批配置候选。
- **兴森科技上调但不转 BUY**：未来 AI 世界确实需要更多高端 PCB、IC 载板、光模块 PCB、FCBGA，但兴森当前 FCBGA/载板兑现还早，属于期权，不是核心仓。

---

## 2. 通富微电：从未来 AI 世界倒推

### 2.1 为什么未来世界会需要它

2030 年附近的 AI 基础设施如果成立，会有几个结果：

```text
更多 GPU / ASIC
-> 更多 HBM 和 Chiplet
-> 更多 2.5D/3D / FCBGA / Bumping / wafer test / final test
-> 更多先进封装产能和良率经验
```

先进封装不是附属环节，而是 AI 芯片性能、良率、成本和交付的核心约束。TrendForce 已经把 advanced packaging、substrate、packaging materials 列入 AI 供应链扩散瓶颈。

通富的映射：

- 它在 OSAT / advanced packaging 节点；
- Q1 收入和扣非利润已经增长；
- 公开摘要显示先进封装扩产和高端产品验证；
- 大基金和半导体资金持股带来资本验证；
- 中国 AI 基础设施在出口限制下，需要本土封测和先进封装能力。

### 2.2 Future-backcast score

```yaml
future_backcast_score:
  future_demand_inevitability: 15   # AI inference/ASIC/HBM 必须扩张
  node_criticality: 19              # advanced packaging 是核心瓶颈
  company_positioning: 13           # 通富在 OSAT / advanced packaging 上位置明确
  financial_translation_path: 12    # Q1 收入和扣非利润已有传导
  scarcity_pricing_power: 8         # 稀缺，但也要面对全球和国内扩产
  domestic_strategic_value: 9       # 国产 AI 基础设施需要本土封测
  capex_survivability: 3            # 91 亿级 capex 带来折旧/现金流压力
  current_pricing_gap: 7            # 不是便宜，但还没到 3-5Y 牛市情景
future_backcast_score_total: 84
```

### 2.3 估值不应只看 12M

如果只看 12 个月：

```text
2026E EPS 约 1.02
普通先进封测合理 PE 50x 左右
普通 base = 1.02 × 50 = 51 元
```

但从 future-backcast 看，通富处在未来 AI 世界的核心节点，可以给 20%-30% 稀缺性溢价：

```text
AI-adjusted 12M PE = 60-65x
AI-adjusted 12M target = 1.02 × 62x ≈ 63 元
若 EPS 上修到 1.10，12M target ≈ 68 元
```

3-5 年结构性估值：

```text
假设 2029/2030 EPS = 1.8-2.2
合理 PE = 45-52x
结构性基础 = 1.8 × 50 = 90 元
结构性牛市 = 2.2 × 52 = 114 元
```

新判断：

```yaml
symbol: "002156.SZ"
name: "通富微电"
current_price: 63.13
near_term_view: "WATCH+"
long_term_view: "长期分批 BUY candidate"
12m_target: 66
12m_range: [56, 72]
3_5y_structural_base_bull: [90, 115]
positioning:
  - "55-60 元：更适合积极分批"
  - "60-65 元：可以小仓位建立长期跟踪仓"
  - "65 元以上：等 EPS 上修或先进封装订单再加"
```

### 2.4 通富的真正风险

通富不是没风险，而是风险集中在“未来能不能兑现到利润”：

- 大 capex 变成折旧，吞掉毛利；
- 先进封装扩产太快，行业价格竞争提前；
- 关键客户订单不及市场预期；
- 非经常性收益掩盖扣非质量；
- 定增/债务让每股收益被摊薄；
- 若先进封装价值更多留在 TSMC/ASE/Amkor 等全球龙头，A 股 OSAT 估值溢价会被压缩。

结论：**通富不是短期最便宜，但它是两者里更符合未来 AI 世界倒推逻辑的核心候选。**

---

## 3. 兴森科技：未来节点存在，但公司兑现路径更不确定

### 3.1 为什么未来世界也会需要它

未来 AI 世界并不只需要封测，还需要：

```text
更多 AI 服务器
-> 更多高速 PCB / HDI / 光模块 PCB
-> 更多 GPU/ASIC 相关封装基板
-> 更多 FCBGA / BT / ABF 类能力
```

兴森的机会在于：

- 1.6T 光模块产品板量产爬坡；
- CSP 封装基板产能利用率较高；
- FCBGA 低层/高层板良率披露较好；
- IC 载板和测试板在国产半导体链条有战略意义；
- 如果 FCBGA 从小批量转规模，估值框架会重估。

### 3.2 Future-backcast score

```yaml
future_backcast_score:
  future_demand_inevitability: 14   # AI PCB/载板需求会变大
  node_criticality: 15              # PCB/载板重要，但不如 HBM/先进封装绝对核心
  company_positioning: 10           # 兴森有相关能力，但 FCBGA 仍早期
  financial_translation_path: 6     # Q1 收入有增长，利润和现金流还弱
  scarcity_pricing_power: 7         # 高端载板有稀缺性，但竞争和扩产也存在
  domestic_strategic_value: 8       # 国产载板/测试板有战略意义
  capex_survivability: 3            # Q1 经营现金流为负，扩产压力要观察
  current_pricing_gap: 7            # 没到长期牛市，但高于 12M 合理价
future_backcast_score_total: 67
```

### 3.3 为什么它仍不是核心 BUY

兴森符合未来方向，但当前仍有三个关键断点：

1. **FCBGA 没有规模利润证明。** 现在是小批量生产和客户验证，不是已经大规模兑现。
2. **财务杠杆还没起来。** Q1 EPS 只有 0.01，归母净利只有 1874 万元。
3. **现金流压力明显。** Q1 经营现金流 -2.47 亿元，未来扩产如果继续消耗现金，会压制估值。

### 3.4 估值重算

传统近端：

```text
2027E EPS 约 0.44
普通成长 PE 60x
near-term value = 26 元
```

Future-backcast 加权：

```text
如果 FCBGA/AI PCB 兑现，2029/2030 EPS 可能到 1.1-1.3
结构性基础/牛市 = 1.1-1.3 × 50-55x = 55-70 元
但成功概率目前只能给 35%-45%
```

AI-adjusted 12M：

```text
near-term value = 26
option spread = 55 - 26 = 29
success probability = 40%
option expected value = 11.6
cashflow/capex penalty = 6
AI-adjusted 12M target ≈ 31.6 ≈ 32 元
```

新判断：

```yaml
symbol: "002436.SZ"
name: "兴森科技"
current_price: 37.13
near_term_view: "不追"
long_term_view: "结构性 WATCH+"
12m_target: 32
12m_range: [26, 36]
3_5y_structural_base_bull: [55, 70]
positioning:
  - "30 元附近：结构性期权开始有吸引力"
  - "32-36 元：适合只观察或极小仓位"
  - "37 元以上：必须等 FCBGA/扣非利润新证据"
```

### 3.5 兴森的上修条件

兴森要从 WATCH+ 变成长期 BUY，需要看到：

- FCBGA 明确规模化量产；
- 1.6T 光模块板客户验证转批量订单；
- 2026H1 / Q2 扣非利润显著超机构预测；
- 经营现金流转正；
- 毛利率持续抬升；
- 2027E EPS 从 0.44 上修到 0.60 以上。

结论：**兴森更像未来 AI 世界的“高弹性期权”，不是现在就很确定的核心基础设施股票。**

---

## 4. 从未来 AI 世界倒推后的动作

| 动作 | 通富微电 | 兴森科技 |
|---|---|---|
| 是否进入长期核心候选 | 是 | 暂否 |
| 是否可以现在开始小仓位 | 可以，偏长期分批 | 不建议，除非极小仓位 |
| 更舒服买点 | 55-60 元 | 30-32 元 |
| 关键跟踪 | 先进封装订单、扣非利润、capex 回报 | FCBGA 量产、1.6T 批量、现金流 |
| 未来 AI 世界匹配度 | 高 | 中高 |
| 当前财务兑现度 | 中高 | 低 |

最终排序：

```text
1. 通富微电
   -> 更符合几年后 AI 世界的核心节点
   -> 可以长期分批
   -> 不是因为便宜，而是因为未来节点足够关键

2. 兴森科技
   -> 未来方向正确
   -> 但当前公司兑现度不够
   -> 等量产/利润/现金流证据，不要只买期权叙事
```

---

## 5. 和上一版的区别

上一版仍然太像：

```text
今天财报和 PE
-> 加一点 AI 结构性溢价
-> 给目标价
```

这一版改成：

```text
2030 AI 世界
-> 必须变大的基础设施节点
-> 当前 A 股谁在这些节点上
-> 谁已经从节点兑现到财报
-> 当前价格是否还低于未来基础情景
```

因此：

- 通富从 `WATCH+` 变成 **长期分批 BUY candidate**；
- 兴森从 `near-term AVOID + structural WATCH` 变成 **结构性 WATCH+，但近端仍不追**。

---

## 6. Sources

- NVIDIA FY2027 Q1 results: `https://investor.nvidia.com/news/press-release-details/2026/NVIDIA-Announces-Financial-Results-for-First-Quarter-Fiscal-2027/default.aspx`
- TrendForce 2026 AI server shipment outlook: `https://www.trendforce.com/presscenter/news/20260120-12887.html`
- TrendForce 2026 AI inference rack outlook: `https://www.trendforce.com/presscenter/news/20260520-13053.html`
- TrendForce 2026 component lead-time bottlenecks: `https://www.trendforce.com/presscenter/news/20260415-13013.html`
- IEA Energy and AI: `https://www.iea.org/reports/energy-and-ai/energy-demand-from-ai`
- Uptime Institute 2026 predictions: `https://uptimeinstitute.com/about-ui/press-releases/uptime-institute-announces-five-data-center-predictions-report-for-2026`
- 兴森科技 2026Q1: `https://disc.static.szse.cn/disc/disk03/finalpage/2026-04-25/8fa0241f-fda6-4e04-b7ea-2d4e1515f3e9.PDF`
- 兴森科技 2026-05-08 IR: `https://static.cninfo.com.cn/finalpage/2026-05-08/1225285130.PDF`
- 通富微电 2026Q1: `https://disc.static.szse.cn/disc/disk03/finalpage/2026-04-30/50eb95fe-4e0a-4d69-a60d-9a7529443ab5.PDF`
- 通富微电 2025 年报: `https://static.cninfo.com.cn/finalpage/2026-04-17/1225112762.PDF`
- yfinance: 2026-06-09 price and valuation proxy.
