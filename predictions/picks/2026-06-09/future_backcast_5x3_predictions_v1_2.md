# Future-Backcast 5x3 股票预测 v1.2

> 日期：2026-06-09
> 方法：先定义 2028-2030 AI 世界，再倒推供应链节点和当下可兑现公司；全市场部分使用供需、财务、估值、催化综合评分
> 价格基准：yfinance 2026-06-09 收盘
> 输出性质：`provisional`，不构成投资建议；未使用 Wind / Choice / Bloomberg / FactSet / LSEG I/B/E/S 授权终端

---

## 0. 总结

这版 5x3 分成三组：

1. **AI Future-Backcast Picks**：几年后 AI 世界必须变大的基础设施节点，且公司已有财务兑现或明确产能路径。
2. **Market Picks**：非 AI 主线中，供需、财务质量、估值和催化同时较强。
3. **Avoid / 不追**：不否定赛道，但当前价格、涨幅或财务兑现与未来故事不匹配。

最终清单：

| 组别 | 股票 | 当前价 | 12M 目标 | 12M 区间 | 3-5Y 结构性情景 | 分数 | 结论 |
|---|---|---:|---:|---:|---:|---:|---|
| AI | 工业富联 `601138.SS` | 70.48 | 92 | 82-100 | 125-160 | 91 | BUY |
| AI | 通富微电 `002156.SZ` | 62.26 | 66 | 56-72 | 90-115 | 84 | 分批 BUY / WATCH+ |
| AI | 思源电气 `002028.SZ` | 177.59 | 235 | 215-255 | 320-420 | 86 | BUY |
| AI | 胜宏科技 `300476.SZ` | 314.80 | 420 | 370-460 | 650-850 | 84 | BUY / WATCH |
| AI | 中微公司 `688012.SS` | 265.47 | 330 | 300-360 | 480-620 | 80 | BUY / WATCH |
| Market | 宁德时代 `300750.SZ` | 393.02 | 555 | 520-600 | 700-850 | 88 | BUY |
| Market | 紫金矿业 `601899.SS` | 28.05 | 38 | 34-42 | 48-60 | 86 | BUY |
| Market | 万华化学 `600309.SS` | 69.75 | 92 | 84-100 | 110-130 | 78 | BUY |
| Market | 中国船舶 `600150.SS` | 34.83 | 47 | 42-52 | 60-75 | 79 | BUY |
| Market | 迈瑞医疗 `300760.SZ` | 142.74 | 210 | 190-235 | 260-320 | 77 | BUY / 修复 |
| Avoid | 绿的谐波 `688017.SS` | 428.25 | 风险区间 170-250 | - | - | 92 risk | AVOID 追高 |
| Avoid | 寒武纪 `688256.SS` | 1250.36 | 风险区间 900-1100 | - | - | 84 risk | AVOID 追高 |
| Avoid | 中际旭创 `300308.SZ` | 1154.99 | 风险区间 950-1150 | - | - | 78 risk | AVOID 追高 |
| Avoid | 新易盛 `300502.SZ` | 725.00 | 风险区间 600-700 | - | - | 75 risk | AVOID 追高 |
| Avoid | 沪电股份 `002463.SZ` | 137.00 | 风险区间 110-130 | - | - | 73 risk | AVOID 追高 |

---

## 1. 打分方法

### 1.1 AI picks

AI picks 采用 future-backcast：

```text
2028-2030 AI 世界
-> always-on inference / agent / video / robotics / enterprise workflow
-> AI factories / high-density data centers
-> GPU + ASIC + HBM + advanced packaging + PCB/substrate + optics + power + cooling
-> 倒推当前谁在这些节点上、谁已兑现到财报
```

AI 总分：

```text
AI total =
  future_backcast_score 40%
  + financial_translation 25%
  + valuation_gap 20%
  + catalyst_and_risk_control 15%
```

### 1.2 Market picks

全市场总分：

```text
Market total =
  supply_demand_score 35%
  + financial_quality 25%
  + valuation_gap 25%
  + catalyst_and_risk_control 15%
```

### 1.3 Avoid

Avoid 不是做空建议，而是“不在当前价追”：

```text
Avoid risk =
  overheat_return 30%
  + valuation_excess 30%
  + financial_translation_gap 25%
  + crowding_or_reflexivity 15%
```

---

## 2. AI Future-Backcast Picks

### 2.1 工业富联 `601138.SS`

```yaml
score:
  future_backcast: 92
  financial_translation: 94
  valuation_gap: 86
  catalyst_risk: 82
  total: 91
```

逻辑：

- 2030 AI 世界需要更多 rack-scale AI server、GPU/ASIC 服务器、交换机、CPO/高速网络和整机集成。
- 工业富联是 A 股里最直接的 AI 服务器和高速网络制造兑现标的。
- 2026Q1 营收 2510.78 亿元，同比 +56.52%；归母净利润 105.95 亿元，同比 +102.55%；经营现金流 250.24 亿元，同比 +1826.20%。
- yfinance 2026-06-09：当前 70.48 元，TTM PE 34.4，forward PE 19.8。对一个 Q1 利润翻倍、现金流大幅改善的 AI 服务器龙头，这个估值并不夸张。

估值：

```text
2026E EPS proxy = 3.57
12M base = 3.57 × 26x = 92.8
range = 82-100
3-5Y = 125-160
```

风险：

- 客户集中；
- AI 服务器毛利率低于上游芯片/光模块；
- 若 CSP capex 放缓，订单弹性会快速变化。

结论：**AI 组第一。BUY。**

---

### 2.2 通富微电 `002156.SZ`

```yaml
score:
  future_backcast: 84
  financial_translation: 76
  valuation_gap: 65
  catalyst_risk: 70
  total: 84
```

逻辑：

- 2030 AI 世界需要更多 GPU/ASIC + HBM + Chiplet + 2.5D/3D advanced packaging。
- 通富在 OSAT / advanced packaging 节点，位置比普通半导体制造更贴近 AI 瓶颈。
- 2026Q1 收入 74.82 亿元，同比 +22.80%；归母净利润 3.29 亿元，同比 +224.55%；扣非归母净利润 1.72 亿元，同比 +64.78%。
- 当前 62.26 元，12M 估值空间不大，但 3-5 年结构性价值较强。

估值：

```text
2026E EPS reference = 1.02
AI scarcity PE = 60-65x
12M base = 66
range = 56-72
3-5Y = 90-115
```

风险：

- 先进封装 capex 变折旧；
- 客户结构和订单节奏不透明；
- 非经常性收益可能抬高表观利润。

结论：**长期分批 BUY candidate，近端 WATCH+。**

---

### 2.3 思源电气 `002028.SZ`

```yaml
score:
  future_backcast: 86
  financial_translation: 82
  valuation_gap: 78
  catalyst_risk: 78
  total: 86
```

逻辑：

- 2030 AI 世界的核心限制不只在芯片，还在电力。高功率密度数据中心需要变压器、开关、并网、电力保护和储能协同。
- IEA 和 Uptime 都把数据中心电力视为中期约束。
- 思源电气受益于全球电网投资、海外订单和数据中心供电链条。
- 2026Q1 收入 45.69 亿元，同比 +41.60%；归母净利润 5.50 亿元，同比 +23.17%。
- 当前 177.59 元，forward PE 28.4；yfinance target mean 242.45。

估值：

```text
2026E EPS proxy = 6.25
base PE = 37-38x
12M base = 235
range = 215-255
3-5Y = 320-420
```

风险：

- 毛利率短期承压；
- 应收账款和海外项目交付节奏；
- 估值已反映一部分电力设备景气。

结论：**BUY。AI 电力链优先标的。**

---

### 2.4 胜宏科技 `300476.SZ`

```yaml
score:
  future_backcast: 85
  financial_translation: 86
  valuation_gap: 78
  catalyst_risk: 70
  total: 84
```

逻辑：

- 2030 AI 世界需要更高层数、更高良率、更高速率的 PCB / HDI / UBB / switching board。
- 胜宏科技 Q1 收入 55.19 亿元，同比 +27.99%；归母净利润 12.88 亿元，同比 +39.95%；经营现金流 21.17 亿元，同比 +399.38%。
- 公开研报摘要称公司覆盖 100 层以上高多层 PCB、10 阶 30 层 HDI、16 层任意互联 HDI。
- 当前 314.80 元，近 20 日回撤约 -18.7%，相对沪电股份的短期拥挤度更低。

估值：

```text
12M base = 420
range = 370-460
3-5Y = 650-850
```

风险：

- PCB 资本开支追上后，价格和毛利率可能回落；
- 高端客户集中；
- 股价波动很大。

结论：**BUY / WATCH。比沪电更适合当前纳入正向 AI 组。**

---

### 2.5 中微公司 `688012.SS`

```yaml
score:
  future_backcast: 80
  financial_translation: 80
  valuation_gap: 68
  catalyst_risk: 76
  total: 80
```

逻辑：

- 2030 中国 AI 世界如果要有更强国产算力，半导体设备是基础设施的基础设施。
- 中微公司在刻蚀/薄膜等关键设备领域具备平台化价值。
- 2026Q1 收入 29.15 亿元，同比 +34.13%；净利润 9.30 亿元，同比 +197.20%。
- 当前 265.47 元，forward PE 53.7，高但不是离谱；如果薄膜设备持续放量，平台化重估成立。

估值：

```text
2026E EPS proxy = 4.95
AI / domestic semi equipment PE = 60-70x
12M base = 330
range = 300-360
3-5Y = 480-620
```

风险：

- 半导体 capex 周期波动；
- 研发投入和产品验证周期；
- 高估值对订单和利润兑现敏感。

结论：**BUY / WATCH。国产 AI 基础设施的设备层候选。**

---

## 3. Market Picks

### 3.1 宁德时代 `300750.SZ`

```yaml
score:
  supply_demand: 90
  financial_quality: 90
  valuation_gap: 86
  catalyst_risk: 78
  total: 88
```

- 2026Q1 收入 1291.31 亿元，同比 +52.45%；归母净利润 207.38 亿元，同比 +48.52%；扣非净利润 180.93 亿元，同比 +52.95%。
- 当前 393.02 元，forward PE 16.3，yfinance target mean 556.4。
- 储能、动力电池和全球份额仍是核心逻辑。

估值：

```text
12M target = 555
range = 520-600
3-5Y = 700-850
```

结论：**Market 组第一。BUY。**

---

### 3.2 紫金矿业 `601899.SS`

```yaml
score:
  supply_demand: 88
  financial_quality: 86
  valuation_gap: 88
  catalyst_risk: 72
  total: 86
```

- 铜、金、锂等资源在电气化、AI 电力、全球通胀和货币周期中都有战略价值。
- 2026Q1 收入 984.98 亿元，同比 +24.79%；归母净利润 200.79 亿元，同比 +97.50%；经营现金流同比 +122.15%。
- 当前 28.05 元，forward PE 8.95，估值相对业绩增长偏低。

估值：

```text
12M target = 38
range = 34-42
3-5Y = 48-60
```

结论：**BUY。资源组优先。**

---

### 3.3 万华化学 `600309.SS`

```yaml
score:
  supply_demand: 76
  financial_quality: 82
  valuation_gap: 86
  catalyst_risk: 68
  total: 78
```

- 化工龙头，周期底部修复 + 全球化项目 + 成本优势。
- 2026Q1 收入 540.52 亿元，同比 +25.50%；归母净利润 37.18 亿元，同比 +20.62%；扣非净利润 35.94 亿元，同比 +18.20%。
- 当前 69.75 元，forward PE 9.55，PB 1.96。

估值：

```text
12M target = 92
range = 84-100
3-5Y = 110-130
```

结论：**BUY。周期修复 + 低估值。**

---

### 3.4 中国船舶 `600150.SS`

```yaml
score:
  supply_demand: 84
  financial_quality: 76
  valuation_gap: 78
  catalyst_risk: 70
  total: 79
```

- 船舶行业订单、交付、单船价格处于上行周期。
- 2026Q1 收入 433.12 亿元，同比 +54.90%；归母净利润同比 +251.64%；扣非净利润同比 +326.69%。
- 当前 34.83 元，forward PE 20.1，PB 1.75。

估值：

```text
12M target = 47
range = 42-52
3-5Y = 60-75
```

结论：**BUY。景气周期还在财报兑现阶段。**

---

### 3.5 迈瑞医疗 `300760.SZ`

```yaml
score:
  supply_demand: 70
  financial_quality: 84
  valuation_gap: 86
  catalyst_risk: 68
  total: 77
```

- 2026Q1 收入 83.52 亿元，同比 +1.39%；归母净利润 23.30 亿元，同比 -11.37%。短期不是高增长，但质量和估值有修复空间。
- 当前 142.74 元，forward PE 15.8，yfinance target mean 237.2。
- 国际化、IVD、新兴业务和医疗设备数字化是修复逻辑。

估值：

```text
12M target = 210
range = 190-235
3-5Y = 260-320
```

结论：**BUY / 修复。风险是短期业绩还没重新加速。**

---

## 4. Avoid / 不追

### 4.1 绿的谐波 `688017.SS`

```yaml
risk_score: 92
current_price: 428.25
fair_or_risk_range: [170, 250]
```

- 人形机器人未来很大，但当前价格把太多未来一次性计入。
- 近 20 日 +53.14%，60 日 +109.20%，120 日 +169.48%。
- TTM PE 556，forward PE 315。

结论：**AVOID 追高。等机器人订单和 EPS 真实兑现。**

---

### 4.2 寒武纪 `688256.SS`

```yaml
risk_score: 84
current_price: 1250.36
fair_or_risk_range: [900, 1100]
```

- 国产 AI 芯片是未来核心方向，但当前估值对兑现要求太高。
- 近 60 日 +69.52%，TTM PE 294，PB 61。
- 如果未来 EPS 快速兑现，结构性牛市仍可能存在；但当前不适合追。

结论：**AVOID 追高，不否定长期国产 AI 芯片方向。**

---

### 4.3 中际旭创 `300308.SZ`

```yaml
risk_score: 78
current_price: 1154.99
fair_or_risk_range: [950, 1150]
```

- 光模块是未来 AI 世界核心节点，但股价已经大幅反映。
- 近 60 日 +115.97%，当前价高于 yfinance target mean 914.43，接近 target high 1278。
- forward PE 26 不算离谱，但反身性和拥挤度很高。

结论：**AVOID 追高。核心赛道，但当前更适合等回撤。**

---

### 4.4 新易盛 `300502.SZ`

```yaml
risk_score: 75
current_price: 725.00
fair_or_risk_range: [600, 700]
```

- 未来光通信节点强，但短期价格也进入高拥挤区。
- 近 60 日 +91.41%，当前价高于 yfinance target mean 625.98。
- forward PE 20 看似不高，但市场已经交易高增长可持续。

结论：**AVOID 追高。强公司，弱买点。**

---

### 4.5 沪电股份 `002463.SZ`

```yaml
risk_score: 73
current_price: 137.00
fair_or_risk_range: [110, 130]
```

- AI PCB 是未来重要节点，沪电财务兑现也很强。
- 2026Q1 收入 62.14 亿元，同比 +53.91%；归母净利润 12.42 亿元，同比 +62.90%。
- 但当前近 60 日 +79.46%，当前价高于 yfinance target mean 110.37，接近 target high 142。

结论：**AVOID 追高。长期仍强，短线买点不舒服。**

---

## 5. 为什么这些不是简单按 PE 排序

这版排序的核心不是“低 PE 买，高 PE 卖”，而是：

```text
未来世界必然变大的节点
-> 当前公司是否处在节点上
-> 财报是否开始兑现
-> 当前价格是否仍低于未来基础情景
```

所以：

- 工业富联 PE 不低，但 AI server 兑现最直接，排第一。
- 通富微电 12M 空间不大，但 advanced packaging 是未来核心节点，进入长期候选。
- 胜宏科技和沪电股份同属 AI PCB，但胜宏当前经历回撤、目标空间更好；沪电短期更拥挤，所以一个入 AI pick，一个入 avoid chase。
- 光模块仍是好赛道，但中际、新易盛当前不是好买点。
- 寒武纪和绿的谐波属于“未来很大，但当前价格更大”的典型。

---

## 6. Sources

- NVIDIA FY2027 Q1 results: `https://investor.nvidia.com/news/press-release-details/2026/NVIDIA-Announces-Financial-Results-for-First-Quarter-Fiscal-2027/default.aspx`
- TrendForce 2026 AI server shipment outlook: `https://www.trendforce.com/presscenter/news/20260120-12887.html`
- TrendForce AI inference rack outlook: `https://www.trendforce.com/presscenter/news/20260520-13053.html`
- TrendForce component lead-time bottlenecks: `https://www.trendforce.com/presscenter/news/20260415-13013.html`
- IEA Energy and AI: `https://www.iea.org/reports/energy-and-ai/energy-demand-from-ai`
- Uptime Institute 2026 data center predictions: `https://uptimeinstitute.com/about-ui/press-releases/uptime-institute-announces-five-data-center-predictions-report-for-2026`
- 工业富联 2026Q1 财报摘要：`https://finance.sina.com.cn/stock/aigc/stockfs/2026-04-29/doc-inhwefuz0931631.shtml`
- 通富微电 2026Q1：`https://disc.static.szse.cn/disc/disk03/finalpage/2026-04-30/50eb95fe-4e0a-4d69-a60d-9a7529443ab5.PDF`
- 思源电气 2026Q1：`https://disc.static.szse.cn/disc/disk03/finalpage/2026-04-25/18741925-16e9-410f-b854-a307cac2f20d.PDF`
- 胜宏科技 2026Q1 摘要：`https://finance.sina.com.cn/stock/relnews/cn/2026-04-29/doc-inhwefve6700908.shtml`
- 中微公司 2026Q1 摘要：`https://www.ithome.com/0/944/147.htm`
- 宁德时代 2026Q1：`https://static.cninfo.com.cn/finalpage/2026-04-16/1225107946.PDF`
- 紫金矿业 2026Q1 摘要：`https://4g.stockstar.com/detail/AN2026042200018671`
- 万华化学 2026Q1：`https://money.finance.sina.com.cn/corp/view/vCB_AllBulletinDetail.php?id=12123151&stockid=600309`
- 中国船舶 2026Q1：`https://money.finance.sina.com.cn/corp/view/vCB_AllBulletinDetail.php?id=12282273&stockid=600150`
- 迈瑞医疗 2026Q1 摘要：`https://finance.sina.com.cn/stock/aiassist/yjbg/2026-04-29/doc-inhwenax0899328.shtml`
- yfinance: 2026-06-09 price, PE/PB, target proxy and return snapshot.
