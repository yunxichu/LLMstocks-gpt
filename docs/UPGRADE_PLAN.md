# LLMstocks-gpt 升级计划

> 版本：v1.1-draft
> 创建：2026-06-08  
> 目标：在原 LLMstocks 的轻量 Claude 选股 SOP 上，新增三条硬证据轴：主流机构评测、顶级投资人持仓、产业链供需分析；并加入 AI 爆发期的供应链瓶颈估值框架。最终输出仍然是可锁定、可复盘、可追溯的股票研究清单，而不是不可验证的主观推荐。

---

## 1. 我们要升级什么

原项目已经具备：

- 每周 picks 工作流：AI 推荐 / 全市场推荐 / 过热不推荐。
- 18 类红旗扫描：业绩、现金流、应收存货、减持、解禁、质押、监管、估值过热等。
- evidence_log：每只股票必须留下硬证据、软证据、待核验证据。
- SHA-256 锁定和 T+1/5/10/20 前瞻跟踪。
- HTML 报告输出。

LLMstocks-gpt 要新增：

- **机构评测轴**：吸收主流机构的评级、估值框架、盈利预测、信用风险、ESG / 治理风险，但不复制或分发受版权保护的研报全文。
- **顶级投资人轴**：追踪长期业绩强、风格稳定、持仓披露可靠的投资人和基金经理，识别增持、减持、首次建仓、集中度和拥挤交易。
- **产业链供需轴**：从公司公告、行业协会、海关、统计局、产业组织、上下游上市公司披露中建立“需求、供给、价格、库存、产能、订单”证据链。
- **研报级估值轴**：每个目标价必须有最新财报锚、3-5 个可信研报/一致预期输入、FY2026/FY2027 EPS 或净利预测桥、估值方法、目标价分歧、上修/下修触发器和证据等级。
- **AI 结构性瓶颈轴**：对 AI 类股票新增 3-5 年结构性可选性判断，识别 HBM、先进封装、PCB/载板、光模块、服务器、电力、液冷、半导体设备、软件等节点的真实瓶颈和稀缺性溢价。
- **综合判断轴**：把上面三类证据与基本面、估值、红旗扫描合并，输出明确的 BUY / WATCH / AVOID 判断及置信度。

---

## 2. 核心原则

1. **证据优先，不做玄学选股**  
   所有关键判断必须能追到 URL、公告标题、文件号、披露日期、数据表、机构名称或数据供应商。

2. **机构观点只作为输入，不作为结论**  
   券商、Morningstar、FactSet、S&P、MSCI、Bloomberg、Refinitiv、Wind、Choice 等来源可以影响评分，但不能替代自己的供需和财务判断。

3. **聪明钱不是神谕**  
   13F、基金季报、港股披露、公募重仓都有滞后、口径、持仓范围和策略约束。只能作为“资本验证”和“拥挤风险”信号。

4. **产业链供需必须能落到指标**  
   不能只写“AI 需求旺盛”。必须落到出货量、订单、库存、价格、资本开支、产能利用率、良率、交付周期、毛利率或上下游确认。

5. **不碰版权雷区**  
   可以记录机构名称、日期、评级、目标价、摘要级要点和自己的归纳；不得把付费研报全文、图表、模型原样存入仓库。

6. **先做研究系统，再做股票清单**  
   在数据源和评分规则没有落地前，不输出伪精确的强推荐。

7. **目标价必须可审计**  
   目标价不能只来自 `forward PE` 或单一券商观点。必须说明 EPS/净利如何预测、为什么给这个估值倍数、外部目标价分歧在哪里、哪些财报指标会触发上修或下修。

8. **AI 不按普通周期机械估值**
   AI 基础设施建设正在表现为全球 capex 军备竞赛，不能只用短期 PE 把所有 AI 链条高估值标的打成 AVOID。必须额外判断它是否控制真实瓶颈、瓶颈能持续多久、能否落实到收入/毛利/现金流，以及当前价格是否已经超过结构性牛市情景。

---

## 3. 目标输出

每次 `/picks` 升级为三类清单：

| 输出 | 数量 | 目的 |
|---|---:|---|
| `ai_picks` | 5 | AI / 半导体 / 算力 / 光模块 / 机器人 / 软件等科技链高确定性候选 |
| `market_picks` | 5 | 非 AI 主题中供需改善、机构观点改善、聪明钱验证的候选 |
| `avoid_picks` | 5 | 过热、供需转差、机构下修、聪明钱撤退或红旗明显的候选 |

每只股票必须新增这些字段：

```yaml
institutional_view:
  consensus_rating: buy|hold|sell|mixed|unavailable
  rating_trend: improving|stable|deteriorating|unavailable
  valuation_gap: discount|fair|premium|unavailable
  sources: []

smart_money:
  top_holders: []
  recent_changes: []
  conviction_score: 0-100
  crowding_risk: low|medium|high|unavailable
  limitations: []

supply_demand:
  chain_role: upstream|midstream|downstream|platform|equipment|materials|unknown
  demand_signals: []
  supply_signals: []
  price_inventory_signals: []
  bottleneck_or_surplus: bottleneck|balanced|surplus|unknown

ai_supply_chain_review:
  status: complete|partial|unavailable
  structural_horizon_years: 3-5
  chain_node: hbm|advanced-packaging|substrate|pcb|optical|server|power|cooling|semiconductor-equipment|software|robotics|other
  ai_demand_evidence: []
  bottleneck_evidence: []
  customer_capacity_evidence: []
  financial_translation: {}
  bottleneck_score: {}
  bottleneck_score_total: 0
  scarcity_premium: {}
  structural_verdict: structural_buy|watch|avoid

gpt_scorecard:
  fundamentals: 0-20
  institutional: 0-15
  smart_money: 0-15
  supply_demand: 0-25
  valuation: 0-10
  catalyst_timing: 0-10
  evidence_quality: 0-10
  total: 0-100
  verdict: BUY|WATCH|AVOID

target_price_review:
  status: research_grade|provisional|unavailable
  horizon_months: 12
  base_target: null
  target_range: [null, null]
  selected_method: {}
  eps_forecast_bridge: {}
  research_report_matrix: {}
  consensus_cross_check: {}
  revision_triggers: {}
  evidence_grade: {}
```

---

## 4. 数据源设计

### 4.1 机构评测

**优先级 A：可授权、可溯源的机构数据**

- FactSet / Refinitiv / Bloomberg：一致预期、目标价、评级变化、EPS 修正、行业 KPI。
- Wind / Choice / iFinD：A 股卖方评级、盈利预测、机构覆盖、行业比较。
- Morningstar：护城河、估值、资本配置、星级框架。
- S&P Global Ratings / Moody's / Fitch：主体信用、债务风险、行业信用压力。
- MSCI / Sustainalytics：ESG、治理、可持续风险。

**优先级 B：公开可取的替代来源**

- 上市公司公告中的业绩预告、订单、产能、客户、资本开支。
- 交易所互动平台中的已披露口径，但只作为 soft evidence。
- 公开新闻发布会、监管问询函、行业协会报告。

**落地规则**

- 若没有授权数据库，先只记录公开机构方法论和公司披露，不抓取付费研报全文。
- 评级趋势比单次评级更重要：`上调 > 首次覆盖买入 > 维持 > 下调 > 终止覆盖`。
- 盈利预测修正优先看最近 30/90 天方向，而不是静态目标价。
- 至少 2 个独立机构观点才能形成 `institutional_view.rating_trend`，否则标 `unavailable`。

### 4.2 顶级投资人持仓

**美股 / ADR / 海外链条**

- SEC EDGAR 13F：机构投资经理季度披露美股多头持仓。
- SEC 13D / 13G：5% 以上受益所有权披露。
- 公司 proxy / annual report：大股东、内部人、董事会持股。

**A 股 / 港股**

- 公募基金季报、半年报、年报：重仓股、行业配置、组合集中度。
- 港交所披露易：权益披露、港股大股东变化。
- 上市公司定期报告：前十大流通股东、QFII、社保、保险、公募、私募进入退出。
- 中证指数、基金公告、基金公司官网：基金产品持仓和基金经理风格。

**顶级投资人定义**

先建立 `config/super_investors.yaml`，每个投资人或基金经理必须有：

- 代表账户或基金。
- 投资风格：价值、成长、质量、周期、科技、事件驱动等。
- 可验证长期业绩或行业声誉。
- 披露来源和披露延迟。
- 适用市场：US / A-share / HK / global。
- 风格风险：高换手、集中持股、行业偏置、衍生品不可见等。

**信号解释**

- 高质量信号：顶级投资人首次建仓、连续增持、仓位进入组合前 10、多个风格不同的投资人同时持有。
- 中等信号：持仓稳定但仓位不高，或只有单一投资人持有。
- 负面信号：连续减持、退出前十大、拥挤交易解散、只剩短线资金。
- 明确限制：13F 最多有 45 天披露延迟，只看部分多头证券，不显示空头、很多海外资产和实时仓位。

### 4.3 产业链供需

每个候选必须先回答“它在产业链上赚哪一段的钱”：

- 上游：材料、能源、设备、IP、核心零部件。
- 中游：制造、代工、封测、组装、系统集成。
- 下游：品牌、渠道、终端需求、应用场景。
- 平台：软件、云、数据、生态。

**需求侧指标**

- 行业出货量、订单、招标、装机、资本开支、客户库存、终端销量。
- 下游龙头的 capex、inventory、backlog、guidance。
- 政策需求：补贴、招标、国产替代、出口限制、能源转型。

**供给侧指标**

- 新增产能、扩产节奏、产能利用率、良率、交付周期。
- 同业资本开支是否过热。
- 原材料、设备、工艺瓶颈是否缓解或加剧。
- 价格：产品 ASP、原材料成本、加工费、库存价格、招标价。

**必须避免的弱论证**

- “属于 AI 概念，所以受益”。
- “某客户是英伟达 / 特斯拉 / 华为供应链”但无公告或客户验证。
- “机构看好”但没有报告日期、评级动作、预测修正。
- “聪明钱买了”但没有披露文件、季度、仓位变化。

### 4.4 研报级目标价

每只 BUY / WATCH 必须有 `target_price_review`。最低要求：

- 最新年报、季报、业绩预告或投资者关系记录作为财务锚。
- 最近 90 天 3-5 个可信研报/一致预期输入；若无法取得授权数据，则状态必须标为 `provisional`。
- FY2026/FY2027 EPS 或净利预测桥，不能只用 `当前价 / forward PE`。
- 至少一种主估值法和一种交叉验证：PE、PEG、PB-ROE、EV/EBITDA、EV/Sales、DCF、SOTP 等按行业选择。
- 外部目标价最高/中位/均值/最低，以及自己的 base/bull/bear。
- 上修和下修触发器。
- 证据等级：财报、研报、行业数据、一致预期分别标 `hard|soft|pending_verify|unavailable`。

详见 `playbooks/references/valuation-target-price.md` 和 `templates/valuation_card.yaml`。

### 4.5 AI 爆发期供应链瓶颈

AI 类股票不能只回答“是不是 AI 概念”，必须回答：

- 下游 capex 是否真实加速：NVIDIA、Microsoft、Alphabet、Meta、Amazon、Broadcom、TSMC、SK hynix 等结果或指引。
- 供应链节点是否真瓶颈：HBM、CoWoS/2.5D/3D 封装、IC 载板、PCB、光模块、电力、液冷、设备、软件生态。
- 公司是否占住该节点：公告、年报、季报、投资者关系记录、客户验证、产能利用率、订单、capex、毛利率。
- 财务是否能兑现：收入桥、ASP、毛利率、扣非利润、现金流、折旧、定增摊薄。
- 当前股价是否仍低于结构性牛市情景。

新增 `playbooks/references/ai-supply-chain-boom-framework.md`，并在
`templates/picks_card.yaml`、`templates/valuation_card.yaml`、`tools/lock_picks.py`
中强制 AI picks 填写 `ai_supply_chain_review`。

---

## 5. 综合评分与决策

### 5.1 硬门槛

一只 BUY 候选必须满足：

- 0 个 HIGH red flag。
- 最多 1 个 MEDIUM red flag，且已解释为何不影响核心 thesis。
- `evidence_log` 至少 5 条 hard evidence。
- `supply_demand` 至少有需求侧和供给侧各 1 条 hard evidence。
- 机构评测或聪明钱至少有一条可追溯证据；如果没有，必须解释为什么仍然入选。

一只 AVOID 候选满足任一：

- 触发 HIGH red flag。
- 2 个以上 MEDIUM red flags。
- 供需转差但股价 / 估值仍按高景气定价。
- 机构连续下修或聪明钱撤退，且基本面没有反证。
- 题材拥挤、估值过热、证据质量低。

### 5.2 权重

| 维度 | 分数 | 判断重点 |
|---|---:|---|
| 基本面质量 | 20 | 盈利、现金流、ROIC、资产负债、治理 |
| 机构评测 | 15 | 评级趋势、盈利预测修正、估值差、信用风险 |
| 顶级投资人 | 15 | 建仓/增持、仓位集中度、投资人质量、拥挤风险 |
| 产业链供需 | 25 | 需求强度、供给约束、价格/库存、订单可见度 |
| 估值 | 10 | 与增长、周期位置、同行相比是否留安全边际 |
| 催化与时点 | 10 | 财报、政策、订单、价格、行业数据窗口 |
| 证据质量 | 10 | hard evidence 数量、来源等级、交叉验证程度 |

**判定**

- `BUY`: 总分 >= 75，且通过硬门槛。
- `WATCH`: 60-74，或证据不错但时点/估值不够。
- `AVOID`: < 60，或触发任一 AVOID 硬门槛。

---

## 6. 实施阶段

### Phase 0：复制与基线确认（已完成）

- 复制 `yunxichu/LLMstocks` 现有框架到 `LLMstocks-gpt`。
- 保留原始 playbooks、tools、templates、predictions 示例。
- 新增本升级计划，明确 v1.0 方向。

### Phase 1：数据源目录与证据规范

新增文件：

- `playbooks/references/institutional-evidence.md`
- `playbooks/references/smart-money.md`
- `playbooks/references/supply-demand.md`
- `playbooks/references/valuation-target-price.md`
- `config/source_registry.yaml`
- `config/super_investors.yaml`
- `config/industry_chain_map.yaml`
- `config/valuation_sources.yaml`

验收标准：

- 每类来源写清楚：可信等级、授权要求、可抓字段、延迟、局限。
- 每条证据必须能标 `hard|soft|pending_verify`。

### Phase 2：Schema 升级

修改：

- `templates/picks_card.yaml`
- `templates/valuation_card.yaml`
- `tools/lock_picks.py`
- `tools/render_picks_html.py`

验收标准：

- lock 工具强制校验 `institutional_view`、`smart_money`、`supply_demand`、`target_price_review`、`gpt_scorecard`。
- HTML 报告新增三块折叠区：机构、聪明钱、供需链。

### Phase 3：数据工具层

新增模块：

- `data/institutional/`
  - `consensus.py`
  - `ratings.py`
  - `source_registry.py`
- `data/smart_money/`
  - `sec_13f.py`
  - `fund_holdings.py`
  - `holder_changes.py`
- `data/supply_chain/`
  - `chain_map.py`
  - `customs.py`
  - `nbs.py`
  - `industry_indicators.py`

验收标准：

- SEC EDGAR 能按 CIK 拉 13F 文件索引，并解析 information table。
- A 股先用公司公告 + 定期报告 + 手工 source registry，后续再接 Wind/Choice/AKShare。
- 供需模块先以人工维护的 `industry_chain_map.yaml` 驱动，不强行自动识别产业链。

### Phase 4：Playbook 升级

修改：

- `playbooks/weekly_picks.md`
- `playbooks/long_term.md`
- `.claude/commands/picks.md`
- `.claude/commands/analyze.md`

新增强制流程：

```text
Stage 1: 候选池构建
Stage 2: yfinance / 公告 / 行业数据初筛
Stage 3: 机构评测扫描
Stage 4: 顶级投资人持仓扫描
Stage 5: 产业链供需扫描
Stage 6: 18 类红旗扫描
Stage 7: 综合评分与反证审查
Stage 8: 选 5 + 5 + 5，锁定并生成 HTML
```

验收标准：

- 每只 BUY 都有“为什么现在买”与“什么证据会推翻我”。
- 每只 AVOID 都有“为什么不碰”与“什么情况会解除风险”。

### Phase 5：前瞻测试与复盘

修改：

- `tools/update_tracking.py`
- `playbooks/review.md`

新增复盘维度：

- 机构上修命中率。
- 聪明钱共振命中率。
- 供需判断命中率。
- BUY 相对沪深 300 / 对应行业指数超额。
- AVOID 相对行业指数回撤或跑输幅度。
- 证据质量与结果的关系。

验收标准：

- T+20 后能判断哪一类证据真正贡献 alpha。
- 如果机构、聪明钱、供需三轴互相冲突，复盘要记录当时如何取舍。

---

## 7. 第一版可执行清单

优先级从高到低：

1. 更新 `templates/picks_card.yaml`，加入三条新证据轴。
2. 写 `playbooks/references/*.md`，把证据标准讲清楚。
3. 写 `config/source_registry.yaml`，先列 SEC EDGAR、公司公告、NBS、GACC、WSTS、交易所公告、基金公告。
4. 写 `config/super_investors.yaml`，先用 10-20 个全球 / 中国代表投资人做可验证样例。
5. 改 `weekly_picks.md`，把 6-stage 升级成 8-stage。
6. 改 `lock_picks.py`，没有机构/聪明钱/供需字段就拒绝锁定。
7. 改 HTML 报告，把三轴证据做成可展开区块。
8. 跑一份 dry-run，不输出真实推荐，只验证字段、证据和评分是否完整。
9. 再跑第一份 v1.0 picks 并锁定。

---

## 8. 参考资料入口

这些不是完整数据源，只是 v1.0 设计时优先参考的官方或机构入口：

- SEC Developer Resources: https://www.sec.gov/about/developer-resources
- SEC Form 13F FAQ: https://www.sec.gov/rules-regulations/staff-guidance/frequently-asked-questions-about-form-13f
- Morningstar Equity Research Methodology: https://www.morningstar.com/content/dam/marketing/shared/research/methodology/705988Morningstar_Equity_Research_Methodology.pdf
- FactSet Consensus Estimates DataFeed: https://insight.factset.com/resources/factset-consensus-estimates-datafeed
- MSCI ESG Ratings: https://www.msci.com/data-and-analytics/sustainability-solutions/esg-ratings
- National Bureau of Statistics of China: https://www.stats.gov.cn/english/index.html
- China Customs Statistics: https://english.customs.gov.cn/Statistics/Statistics
- WSTS semiconductor market data: https://www.wsts.org/

---

## 9. 重要免责

本项目输出是个人研究信号和前瞻测试记录，不构成投资建议，不自动下单，不承诺收益。任何股票进入 BUY 也只是“研究上值得进一步关注”，不是交易指令。
