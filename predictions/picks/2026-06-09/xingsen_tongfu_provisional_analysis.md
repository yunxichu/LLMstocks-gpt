# 兴森科技、通富微电专项分析

> 日期：2026-06-09  
> 价格基准：yfinance 最新可得 A 股行情，均为 2026-06-08 收盘  
> 输出性质：`provisional`，不是锁定预测，不构成投资建议  
> 研究目标：按照升级后的 LLMstocks-gpt 框架，对两家先进 PCB / 先进封装相关公司做财报锚定、机构预测对照、产业链供需判断、目标价估值和风险触发器。

---

## 0. 结论先行

| 结论 | 股票 | 当前价 | 12M 基础目标 | 合理区间 | 牛市情景 | 核心判断 |
|---|---:|---:|---:|---:|---:|---|
| AVOID / 不追 | 兴森科技 `002436.SZ` | 37.00 | 26 | 22-28 | 34-37 | 产业逻辑成立，但利润基数低、2026E PE 约 148x，当前价格已把 2027-2028 年的乐观放量提前定价。 |
| WATCH / 不追 | 通富微电 `002156.SZ` | 62.26 | 52 | 46-56 | 65-70 | 基本面优于兴森，先进封装、AMD 相关业务、资本开支都在验证，但现价已高于公开目标价高点，风险收益不够好。 |

一句话：**两家公司都在 AI 硬件链条上，但现在不是“看到产业趋势就买”的位置。通富微电可以继续跟踪，兴森科技更像高波动成长权证；新仓优先等回撤或财报继续兑现。**

---

## 1. 证据等级和限制

本次没有 Wind / Choice / Bloomberg / FactSet / LSEG I/B/E/S 授权终端，也没有完整读取全部付费研报全文。因此：

- 公司公告、年报、一季报、投资者关系记录：`hard`
- SIA/WSTS、Prismark、TrendForce 等行业机构公开数据：`hard / institutional`
- 公开可访问研报摘要、F10 盈利预测汇总、yfinance analyst target：`soft`
- 涉及 AMD 订单比例、3nm 多芯片验证、客户导入等若来自券商摘要：`soft / pending_verify`

这意味着本报告可以给出可计算的目标价和判断，但结论仍标记为 `provisional`，不能标记为仓库规则中的 `research_grade`。

---

## 2. 产业链供需背景

AI 算力链条的供需结论是：**真实紧张，但紧张环节之间的股票估值差异很大。**

- SIA 公布 2025 年全球半导体销售额达到 7,917 亿美元，同比增长 25.6%，并预计 2026 年接近 1 万亿美元；逻辑和存储是 2025 年增长最快的两类产品。
- WSTS 2025 年秋季预测显示，2026 年全球半导体市场预计达到 9,754.6 亿美元，同比增长 26.3%，其中 Logic 和 Memory 继续领涨。
- Prismark 披露，AI 服务器、高速网络和先进载板推动 2025 年 PCB 市场从 736 亿美元增至约 858 亿美元；HDI、高多层板和载板都明显受益。
- TrendForce 2026-04-30 的产业观察指出，AI 需求导致 3nm/2nm 晶圆、2.5D/3D 先进封装、CoWoS、载板、PCB、HBM、SSD 等环节同时紧张，先进封装瓶颈至少到 2027 年才有望缓和。

对兴森科技和通富微电的映射：

```text
AI 服务器 / GPU / ASIC / HBM
-> 先进封装、FCBGA/ABF 载板、高多层 PCB、HDI、测试板需求提升
-> 兴森科技受益于 PCB + IC 载板 + FCBGA 小批量导入
-> 通富微电受益于先进封装、FCBGA、Chiplet、Bumping、晶圆测试和高端封测订单
-> 但重资产扩产和高估值会把“产业正确”变成“股价未必正确”
```

---

## 3. 兴森科技：产业逻辑不错，但现价明显透支

### 3.1 财报锚点

最新硬数据：

- 2025 年报：营业收入 71.95 亿元，同比增长 23.68%；归母净利润 1.35 亿元，同比增长 168.05%；扣非归母净利润 1.41 亿元，同比增长 172.03%；EPS 0.08 元；毛利率 19.57%。
- 2026Q1：营业收入 18.18 亿元，同比增长 15.10%；归母净利润 1,874.47 万元，同比增长 100.00%；扣非归母净利润 2,817.39 万元，同比增长 308.32%；经营现金流 -2.47 亿元；EPS 0.01 元。
- 管理层 2026-05-08 交流：北京兴斐 1.6T 光模块产品板处于量产爬坡并同步做多家客户验证；CSP 封装基板产能利用率处于高位；FCBGA 仍处于小批量生产阶段，量产取决于行业需求、客户进展和供应商管理策略。

我的理解：

```text
收入已经恢复
-> 毛利率和扣非利润确实改善
-> 但归母利润体量仍很小，Q1 EPS 只有 0.01
-> FCBGA 和高端光模块 PCB 是未来期权，不是已经完全落进利润表的确定利润
```

### 3.2 机构预测矩阵

```yaml
research_report_matrix:
  status: partial
  lookback_days: 90
  reports:
    - institution: "中航证券"
      date: "2026-06-04 / 2026-05-22"
      rating: "buy"
      target_price: null
      fy2026_eps: 0.23
      fy2027_eps: 0.39
      fy2028_eps: 0.63
      fy2026_net_profit: "3.96亿元"
      fy2027_net_profit: "6.69亿元"
      valuation_method: "PE"
      evidence_type: "soft"
      source: "公开F10/研报摘要"
    - institution: "国海证券"
      date: "2026-05-24"
      rating: "buy"
      target_price: null
      fy2026_eps: 0.27
      fy2027_eps: 0.44
      fy2028_eps: 0.68
      fy2026_net_profit: "4.56亿元"
      fy2027_net_profit: "7.48亿元"
      valuation_method: "PE"
      evidence_type: "soft"
      source: "公开F10摘要"
    - institution: "长城证券"
      date: "2026-05-21"
      rating: "buy"
      target_price: null
      fy2026_eps: 0.23
      fy2027_eps: 0.42
      fy2028_eps: 0.66
      fy2026_net_profit: "3.81亿元"
      fy2027_net_profit: "7.14亿元"
      valuation_method: "PE"
      evidence_type: "soft"
      source: "公开F10摘要"
    - institution: "华鑫证券"
      date: "2026-05-05"
      rating: "buy"
      target_price: null
      fy2026_eps: 0.26
      fy2027_eps: 0.44
      fy2028_eps: 0.76
      fy2026_revenue: "86.75亿元"
      fy2027_revenue: "103.70亿元"
      valuation_method: "PE"
      evidence_type: "soft"
      source: "东方财富研报摘要"
    - institution: "公开预测汇总"
      date: "2026-06-08"
      rating: "mostly_buy"
      target_price: null
      fy2026_eps: 0.25
      fy2027_eps: 0.44
      fy2028_eps: 0.68
      fy2026_net_profit: "4.29亿元"
      fy2027_net_profit: "7.55亿元"
      fy2028_net_profit: "11.56亿元"
      valuation_method: "consensus"
      evidence_type: "soft"
      source: "F10盈利预测汇总"
```

机构侧的共识非常一致：未来三年利润会高速修复。但关键问题是，**即便按机构均值，当前 37 元对应 2026E PE 约 148x，2027E PE 约 84x，估值已经远高于“刚验证拐点”的安全区。**

### 3.3 估值计算

基本输入：

```yaml
price: 37.00
shares: "约16.997亿股"
market_cap: "约628.9亿元"
fy2025_eps: 0.08
fy2026_consensus_eps: 0.25
fy2027_consensus_eps: 0.44
fy2028_consensus_eps: 0.68
fy2026_consensus_revenue: "约87.4亿元"
fy2026_consensus_net_profit: "约4.29亿元"
```

主方法：PE 估值

```text
base = 2027E EPS 0.44 * 60x = 26.4 元
range = 2027E EPS 0.39-0.49 * 55-60x ≈ 21.5-29.4 元
```

为什么用 2027E 而不是 2026E：

- 兴森科技 2026 年仍是产能爬坡和利润修复初期，单看 2026E 会被低利润基数扭曲。
- 12M 目标价可以前看 2027 年盈利，但不能直接把 2028 年最乐观利润全部贴现到今天。

交叉验证 1：PS

```text
2026E revenue = 87.4亿元
合理 PS = 4.5-5.5x
合理市值 = 393-481亿元
每股价值 = 23.1-28.3 元
```

交叉验证 2：PB / ROE

```text
2026E BVPS ≈ 3.24元
2026E ROE ≈ 8.2%，2027E ROE ≈ 12.8%
合理 PB = 7.0-8.5x
每股价值 = 22.7-27.5 元
```

目标价：

```yaml
own_target_price:
  bear: "16-18"
  base: "26"
  fair_range: "22-28"
  bull: "34-37"
```

牛市情景需要同时满足：

- 2026 年 EPS 明显超过 0.27 元；
- 2027 年 EPS 上修到 0.55 元以上；
- FCBGA 从小批量进入可规模确认收入；
- CSP/BT 载板涨价和高位稼动率能转化为 24% 以上毛利率；
- 海外大客户或 AI 核心客户量产突破有公告或财报验证。

否则，37 元已经不是“合理成长溢价”，而是把 2028 年高增长提前折现。

### 3.4 判断

兴森科技我给 `AVOID / 不追`，不是因为公司没有产业价值，而是因为现在价格相对财报兑现太急。

我会这样处理：

- 新仓：不买。
- 如果已经持有：只适合高风险账户保留小仓位跟踪，不能按低估值成长股持有。
- 观察价：28 元以下重新进入观察；26 元附近才有相对合理风险收益。
- 强上修条件：2026H1 扣非利润、经营现金流、FCBGA 客户导入显著超预期。

---

## 4. 通富微电：基本面更强，但价格也不便宜

### 4.1 财报锚点

最新硬数据：

- 2025 年报：营业收入 279.21 亿元，同比增长 16.92%；归母净利润 12.19 亿元，同比增长 79.86%；扣非归母净利润 8.41 亿元，同比增长 35.34%；EPS 0.80 元。
- 2026Q1：营业收入 74.82 亿元，同比增长 22.80%；归母净利润 3.29 亿元，同比增长 224.55%；扣非归母净利润 1.72 亿元，同比增长 64.78%；经营现金流 9.42 亿元，同比下降 35.43%；EPS 0.2168 元；ROE 2.10%。
- Q1 非经常性损益约 1.57 亿元，其中金融资产/金融负债公允价值变动收益约 1.83 亿元，对归母利润有明显增厚。因此更应该看扣非利润能否持续爬升。
- Q1 股东结构：大基金一期持股 6.47%，大基金二期相关主体持股 0.95%，香港中央结算持股 4.63%，华夏国证半导体芯片 ETF 等在前十大股东中。

我的理解：

```text
通富的收入和利润已经比兴森更扎实
-> 先进封装不是纯概念，已经进入资本开支、产能、客户和利润表验证阶段
-> 但 Q1 利润有非经常性收益增厚，且重资产扩产会带来折旧、负债和现金流压力
-> 所以它值得跟踪，但不能忽视现价已接近牛市情景
```

### 4.2 机构预测矩阵

```yaml
research_report_matrix:
  status: partial
  lookback_days: 90
  reports:
    - institution: "开源证券"
      analyst: "陈蓉芳/祁海超"
      date: "2026-05-06"
      rating: "buy"
      target_price: null
      fy2026_eps: 0.98
      fy2027_eps: 1.22
      fy2028_eps: 1.54
      fy2026_net_profit: "14.89亿元"
      fy2027_net_profit: "18.51亿元"
      fy2028_net_profit: "23.41亿元"
      valuation_method: "PE"
      core_assumptions:
        - "2026Q1淡季超预期"
        - "3nm多芯片产品封装通过验证"
        - "2026年资本开支91亿元"
      evidence_type: "soft"
      source: "公开研报摘要/PDF"
    - institution: "华泰证券"
      date: "2026-04-19"
      rating: "buy"
      target_price: 56.30
      fy2026_eps: null
      fy2027_eps: null
      valuation_method: "PB_ROE"
      core_assumptions:
        - "先进封装产能扩张"
        - "以BPS和PB估值"
      evidence_type: "soft"
      source: "公开研报列表及市场摘要"
    - institution: "申万宏源"
      date: "2026-04/05附近公开摘要"
      rating: "outperform"
      target_price: null
      fy2026_net_profit: "15.32亿元"
      fy2027_net_profit: "17.37亿元"
      fy2028_net_profit: "19.51亿元"
      valuation_method: "PE"
      evidence_type: "soft"
      source: "公开摘要"
    - institution: "公开预测汇总"
      date: "2026-06附近"
      rating: "mostly_buy"
      target_price: null
      fy2026_eps: 1.02
      fy2026_net_profit: "15.52亿元"
      valuation_method: "consensus"
      evidence_type: "soft"
      source: "F10盈利预测汇总"
    - institution: "yfinance analyst proxy"
      date: "2026-06-08"
      rating: "buy"
      target_low: 25.14
      target_mean: 41.21
      target_median: 41.70
      target_high: 56.30
      analyst_count: 4
      valuation_method: "external_target_proxy"
      evidence_type: "soft"
      source: "yfinance"
```

机构侧对通富的共识比兴森更“落地”：通富已经有 12 亿以上归母利润、实际先进封装收入和持续资本开支。但现价 62.26 元已经高于公开可见目标价高点 56.30 元。

### 4.3 估值计算

基本输入：

```yaml
price: 62.26
shares: "约15.18亿股"
market_cap: "约944.9亿元"
fy2025_eps: 0.80
fy2026_consensus_eps: 1.02
fy2027_reference_eps: 1.22
fy2028_reference_eps: 1.54
fy2026_consensus_net_profit: "约15.5亿元"
```

主方法：PE 估值

```text
base_1 = 2026E EPS 1.02 * 50x = 51.0 元
base_2 = 2027E EPS 1.22 * 42x = 51.2 元
base target ≈ 52 元
```

为什么给 50x 以内：

- 通富是重资产封测企业，不是纯软件/平台型企业。
- 2026-2028 年利润增长大约 22%-26%，不是 50%+ 的利润爆发。
- ROE 仍处在 9%-11% 区间，不能长期支撑过高 PB。
- Q1 表观利润中非经常性收益占比不低，需要扣非利润继续验证。

交叉验证 1：PB

```text
2026E BVPS 约 11.0-11.3 元
合理 PB = 4.6-5.0x
每股价值 ≈ 50.6-56.5 元
```

交叉验证 2：PS

```text
2026E revenue ≈ 330.7亿元
合理 PS = 2.2-2.6x
合理市值 ≈ 728-860亿元
每股价值 ≈ 48-57 元
```

目标价：

```yaml
own_target_price:
  bear: "36-42"
  base: "52"
  fair_range: "46-56"
  bull: "65-70"
```

牛市情景需要同时满足：

- 2026 年 EPS 上修到 1.20-1.30 元；
- 扣非利润增速高于表观利润，非经常性收益占比下降；
- 先进封装新增产能爬坡顺利，折旧没有吞噬毛利率；
- AMD 或其他高性能计算客户订单确定性继续增强；
- 定增/资本开支带来的摊薄和负债压力可控。

如果只是按当前公开预测，62 元上方已经不便宜；如果要合理看 70 元，需要市场愿意给 2026E 55x 以上 PE，或者 2027E 57x PE，这需要更强的业绩上修。

### 4.4 判断

通富微电我给 `WATCH / 不追`。

它比兴森更值得放在长期跟踪名单里，因为：

- 收入、利润、现金流和客户结构更扎实；
- 先进封装扩产和高端技术路线更直接；
- 国家产业资本和半导体 ETF 持仓带来一定资金锚；
- 2026Q1 已经验证中高端产品收入增长。

但我仍不建议在 62 元附近新建重仓：

- 当前价高于 yfinance/公开研报目标价高点 56.30；
- 现价约等于 2026E 61x PE、2027E 51x PE；
- 资本开支大幅提升，未来折旧、财务费用、定增摊薄都需要进入模型；
- 若市场从“先进封装缺口”切到“扩产后价格竞争”，估值压缩会很快。

我会这样处理：

- 新仓：等 50-55 元区间，或者等 EPS 预测上修到 1.25 元以上。
- 已持有：可以保留核心仓，但不追涨加仓。
- 观察点：2026H1 扣非利润、毛利率、在建工程转固、定增进度、AMD/高性能计算相关业务披露。

---

## 5. 二者对比

| 项目 | 兴森科技 | 通富微电 |
|---|---|---|
| 产业位置 | PCB、IC 载板、CSP/FCBGA、ATE 测试板 | OSAT、先进封装、FCBGA、Chiplet、Bumping、晶圆测试 |
| 2025 收入 | 71.95 亿元 | 279.21 亿元 |
| 2025 归母净利 | 1.35 亿元 | 12.19 亿元 |
| 2026Q1 扣非利润 | 0.28 亿元 | 1.72 亿元 |
| 利润质量 | 仍在低位修复 | 更扎实，但 Q1 有非经常性收益增厚 |
| 当前估值 | 2026E PE 约 148x | 2026E PE 约 61x |
| 主要风险 | FCBGA 量产慢、利润兑现慢、估值过高 | 资本开支、折旧、客户集中、定增摊薄、行业竞争 |
| 我的优先级 | 低 | 中 |

如果一定二选一，**通富微电优先于兴森科技**。但更严格的答案是：两者当前都不适合追价，通富是“好公司偏贵”，兴森是“好赛道、高预期、低兑现”。

---

## 6. 模型输出

```yaml
run_output:
  date: "2026-06-09"
  status: "provisional"
  universe:
    - "002436.SZ"
    - "002156.SZ"
  decisions:
    - symbol: "002436.SZ"
      name: "兴森科技"
      action: "AVOID / 不追"
      current_price: 37.00
      target_price_12m_base: 26
      fair_value_range: "22-28"
      bull_case: "34-37"
      downside_to_base: "-29.7%"
      reason:
        - "AI PCB/IC载板逻辑成立"
        - "2026E EPS均值仅约0.25元"
        - "现价对应2026E PE约148x"
        - "FCBGA仍处于小批量阶段，利润兑现不足以支撑当前价格"
      upgrade_triggers:
        - "2026H1 EPS/扣非利润显著超过机构均值"
        - "FCBGA获得明确规模量产订单"
        - "经营现金流转正且毛利率继续上行"
    - symbol: "002156.SZ"
      name: "通富微电"
      action: "WATCH / 不追"
      current_price: 62.26
      target_price_12m_base: 52
      fair_value_range: "46-56"
      bull_case: "65-70"
      downside_to_base: "-16.5%"
      reason:
        - "先进封装和高端封测业务兑现程度更高"
        - "2025和2026Q1财报明显强于兴森"
        - "现价高于公开目标价高点56.30元"
        - "资本开支、折旧、非经常性收益和定增摊薄需要继续验证"
      upgrade_triggers:
        - "2026E EPS上修到1.25元以上"
        - "扣非利润增速继续高于收入增速"
        - "先进封装新增产能良率和稼动率超预期"
```

---

## 7. 主要资料来源

- 兴森科技投资者关系年度报告页：`https://www.chinafastprint.com/report/annual`
- 兴森科技投资者关系季度报告页：`https://shop.chinafastprint.com/report/quarterly`
- 兴森科技 2026Q1 公告转载页：`https://money.finance.sina.com.cn/corp/view/vCB_AllBulletinDetail.php?id=12191002&stockid=002436`
- 兴森科技 2026-05-08 投资者关系活动记录表：`https://static.cninfo.com.cn/finalpage/2026-05-08/1225285130.PDF`
- 兴森科技盈利预测汇总：`https://webf10.gw.com.cn/SZ/B16/SZ002436_B16.html`
- 通富微电 2025 年年度报告全文：`https://static.cninfo.com.cn/finalpage/2026-04-17/1225112762.PDF`
- 通富微电 2026 年第一季度报告：`https://disc.static.szse.cn/disc/disk03/finalpage/2026-04-30/50eb95fe-4e0a-4d69-a60d-9a7529443ab5.PDF`
- 通富微电 2025-05-20 投资者关系活动记录表：`https://static.cninfo.com.cn/finalpage/2025-05-20/1223606511.PDF`
- 通富微电开源证券公开研报页：`https://data.eastmoney.com/report/zw_stock.jshtml?infocode=AP202605061821995959`
- SIA 2026-02-06：`https://www.semiconductors.org/global-annual-semiconductor-sales-increase-25-6-to-791-7-billion-in-2025/`
- WSTS Autumn 2025 Forecast：`https://www.wsts.org/esraCMS/extension/media/f/WST/7310/WSTS_FC-Release-2025_11.pdf`
- Prismark What's New：`https://www.prismark.com/what-s-new`
- TrendForce 2026-04-30：`https://www.trendforce.com/presscenter/news/20260430-13028.html`
- yfinance：2026-06-08 收盘行情、估值和 analyst target proxy。
