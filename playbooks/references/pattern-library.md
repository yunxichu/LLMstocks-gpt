# A-Share Pattern Library

Reusable archetypes for chokepoint-style A-share research. Adapted from
Serenity's pattern library with A-share-specific additions. Do not treat
these as current recommendations — they are patterns, not picks.

---

## Category A: Chokepoint patterns (adapted from Serenity)

### A.1 Material Bottleneck of the Bottleneck

Pattern: end product depends on a substrate or chemical; the substrate depends
on an even scarcer precursor.

A-share examples (illustrative, not recommendations):
- 高纯电子级特气 — 上游氯化氢 / 三氯化硼 / 六氟化硫 / 氟化氢供给集中
- 国产光刻胶 — KrF/ArF 光刻胶上游的树脂、PAG 光酸更稀缺
- 固态电池硫化物电解质 — 上游硫化锂超高纯度供应紧张

Reusable checks:
- Which material is physically required (BOM 上有名字的)?
- Who controls purity, yield, or scale?
- Can customers qualify substitutes quickly (典型周期 6-18 个月)?
- Does a tiny upstream revenue pool control a huge downstream buildout?

### A.2 Architecture Transition Supplier

Pattern: a new architecture changes the component stack, creating winners that
screeners do not recognize.

A-share examples:
- CPO 光通信 — 从可插拔光模块到 CPO 共封装，外置激光器 / FAU / 硅光成为新必备
- 800VDC 数据中心电力 — 从 12V/48V 架构转向 800V，碳化硅器件 / 高压电源模块需求剧变
- 人形机器人 — 谐波减速器 / 行星滚柱丝杠 / 六维力传感等本来低估值的工业件

Reusable checks:
- What changed in the architecture?
- Which old component becomes more valuable or newly mandatory?
- Is the supplier named in customer / technical / analyst material?
- Is revenue still too small for conventional screens to notice?

### A.3 Multi-Layer Chokepoint Map

Pattern: map a supply chain as stacked failure points instead of a flat
supplier list. Goal: find "the bottleneck inside the bottleneck."

Example layer map for AI compute (illustrative):
1. 上游材料：硅片、电子特气、靶材、光刻胶
2. 晶圆代工与封装：先进制程 / 先进封装 / HBM
3. 板级：高多层 PCB、连接器、电源管理芯片
4. 模组：服务器内存 / 加速卡组装
5. 整机：AI 服务器整机
6. 数据中心：电源 / 制冷 / 网络
7. 应用：云服务 / 大模型推理

Reusable checks:
- 至少分 5-7 层，每层问"如果产能不足，谁会停？"
- 哪一层已经被市场拥挤定价？哪一层还没？
- 上游小节点能否卡住下游大需求？
- 架构变化（如 CPO / 800VDC / 液冷）让哪层变得更重要？

### A.4 Capacity / Packaging With Strategic Backstop

Pattern: an underappreciated manufacturing node becomes strategic because
domestic supply chain (国产替代) needs it.

A-share examples:
- 半导体先进封装 — Chiplet/2.5D/3D 封装产能稀缺，国产长电、通富、华天
- 第三代半导体（SiC/GaN）功率器件 — 政策大力扶持，部分公司有 IDM 产能优势

Reusable checks:
- Is the company a foundry / packager / equipment bottleneck rather than a product brand?
- Does government funding (大基金 / 地方专项) validate criticality?
- Is book value / replacement value low relative to strategic value?
- Are customers already qualifying the node?

### A.5 Infrastructure Bottleneck Outside Semis

Pattern: AI / 数据中心 / 新能源 growth moves the bottleneck away from chips into
power, cooling, grid, or physical infrastructure.

A-share examples:
- 数据中心电力 — 变压器、开关柜、UPS、PDU、液冷
- 储能 BMS / PCS — 与电池一起被低估的电气配套
- 特高压输电 — 跨区送电的关键节点

Reusable checks:
- Which physical infrastructure is delaying deployments?
- Are lead times multi-year?
- Does the candidate have capacity in the right geography?
- Can it price through raw-material inflation?
- Is backlog growth visible?

### A.6 Forward-TAM / Low-Current-Revenue Mismatch

Pattern: current financials look small, messy, or cyclical, while future
content per system may scale sharply.

A-share examples:
- 人形机器人零部件 — 当前营收占比小，未来人形机器人量产驱动巨大增量
- 卫星互联网 — 商业航天产业链当前收入低，未来星座规模化带动剧增

Reusable checks:
- What is current revenue from the relevant segment?
- What future system volume drives content growth?
- Is the company constrained by dilution or capacity capex?
- Can it capture margin, or will customers extract the upside?

### A.7 Small-Cap Demand Shock Translation

Pattern: a product or developer behavior shift is visible to everyone, but the
market maps it to the obvious mega-cap instead of the small listed company
whose financials can actually move.

A-share examples:
- 端侧 AI 推理芯片 — 手机/PC AI 落地，市场盯英伟达不看本土小芯片设计公司
- 工业机器人触觉传感器 — 人形机器人故事大家都讲，但市场低估专门做触觉的小公司

Reusable checks:
- What exactly changed in user behavior or procurement?
- Which listed company is small enough for the demand shock to matter?
- What part of revenue is exposed to the shock?
- Can unit demand be estimated from user behavior, channel checks, or inventory?
- Does the market still categorize the company under its old identity?
- Are consensus revenue growth, forward sales, or forward P/E still anchored to the old identity?
- What would prove the trend is only temporary?

### A.8 Small-Cap Pricing Vacuum and Reflexivity

Pattern: the market ignores a small critical supplier because analysts and
large funds cannot justify the work or cannot buy enough size. When evidence
arrives, price discovery can be violent.

Reusable checks:
- Is market cap below the threshold where 公募/QFII can justify the work?
- Is research coverage thin or stale?
- Is daily 成交额 too small for institutions, creating a pricing vacuum?
- Does the thesis survive without 短挤压 / 题材炒作？
- Could liquidity also trap holders on the way down?

### A.9 Institutional Rotation Pattern

Pattern: capital rotates through layers as the market digests a buildout.

A-share rotation example (illustrative):
- Stage 1: 算力龙头 / 显性 winners （已 rerate）
- Stage 2: 光模块 / 高速连接器 / 服务器整机 （正在 rerate）
- Stage 3: 外置激光器 / 硅光 / 衬底 / 测试 / 先进封装 （部分尚未 rerate）

Reusable checks:
- Which layer already rerated?
- Which adjacent layer must scale next?
- Which suppliers are still priced as legacy 老业务?
- What evidence shows institutions started moving into the next layer (基金季报变动 / 北向季度数据 / 龙虎榜机构席位频次)?

### A.10 Bayesian Conviction Update Pattern

Pattern: treat the thesis as a hypothesis. Build a strong prior from physical
supply-chain research; update conviction as evidence arrives.

Workflow:
1. Define `H`: this company is a future bottleneck / disproportionate beneficiary
2. Build the prior from BOMs / 公告 / 客户文档 / 市场规模 / 产能图
3. Update on evidence:
   - **Positive**: 客户认证 / 大单 / 业绩超预期 / 政策落地 / 供给短缺 / 专利 / 资格 / ASP 上调 / 指数纳入
   - **Negative**: 替代品 / 客户自研 / ramp 失败 / 毛利下行 / 定增 / 管理层动荡 / 业绩雷
4. Compare posterior conviction across candidates; rotate attention based on evidence improvement, not price alone

### A.11 Disclosure and Confidence Pattern

Separate trade from thesis when reading 大 V / 基金经理 / 北向 disclosures.
See `research-rubric.md` "Trade Disclosure Labels".

---

## Category B: A-Share-Specific patterns

### B.1 Policy Catalyst Diffusion

Pattern: 国家级 / 部委级 / 地方级政策落地后，资金从政策直接受益者扩散到上下游。

Stages:
1. 政策预期阶段：传闻、十四五 / 十五五规划、政策征求意见稿
2. 政策落地：正式文件、补贴公布、试点城市公布
3. 龙头 rerate：政策直接受益者第一波涨
4. 上游/下游扩散：龙头涨完后，资金向产业链稀缺环节扩散

Reusable checks:
- 当前在哪个阶段？
- 哪些是显性受益（市场已定价）？哪些是隐性（还没）？
- 政策对公司收入的实际转化率有多少？
- 是否有政策风险（例如反向收紧）？

A 股案例（思路）：
- 半导体大基金 → 设计 / 制造 / 封测 → 设备 / 材料 / 零部件
- 储能政策 → 电池龙头 → 上游材料 / BMS / PCS

### B.2 Fund Clustering Diffusion (公募抱团扩散)

Pattern: 当公募基金抱团一只龙头股达到一定密度，资金会自然扩散到该赛道二线 / 三线公司。

Reusable checks:
- 龙头股的基金持股集中度（前 10 大基金 vs 前 50 大基金）
- 季度环比基金持有家数增长（>20 家是显著信号）
- 已经被抱团 vs 还在扩散中？
- 二线 / 三线公司的基金持仓变动是否开始显著？

### B.3 Performance Surprise Catalyst (业绩预告超预期)

Pattern: 业绩预告披露的扣非净利润同比增速远超机构一致预期，往往是中长期 thesis 的强证据。

Reusable checks:
- 一致预期增速 vs 业绩预告中值的偏离度
- 单季 vs 累计：单季 surprise 含金量更高
- 业绩归因：核心业务驱动 vs 一次性？
- 历史业绩预告与最终披露偏差大不大（衡量管理层 guidance 质量）？

时点：
- 1 月底/4 月底：年报 + 一季报业绩预告窗口
- 7 月中下旬：中报业绩预告
- 10 月中下旬：三季报业绩预告

### B.4 Restriction Window Reversal (解禁低点反弹)

Pattern: 大额解禁前股价通常承压，解禁后如果出现"靴子落地" + 业绩仍然强，可能出现反弹机会。

Reusable checks:
- 解禁规模 vs 流通股本（占比 > 20% 是大解禁）
- 解禁前 3-6 个月股价跌幅
- 解禁后是否真的高比例减持（看公告 + 限售股变动）
- 基本面是否依然支撑（业绩 + 估值 + 行业景气）

风险提示：不能把"已解禁"当 thesis；必须有独立的 chokepoint / 业绩催化。

### B.5 LHB Institutional Footprint (龙虎榜机构留痕) — **V2 DEFERRED**

> v0.5 deprecated: 龙虎榜数据来自东财，境外不可访问。本 pattern 等 V2 境内 MCP 配通后再恢复。

Pattern: 机构席位连续买入 + 游资席位未占主导，往往是机构建仓信号。
(详细 checks 见 git 历史 v0.4 版本，此处略)

### B.6 Leader-Laggard Pattern (龙头-补涨) — **V2 DEFERRED**

> v0.5 deprecated: 板块龙头判定 + 跟涨股扫描依赖中国大陆专有数据 (主力资金流, 涨停板梯队)。等 V2。

Pattern: 板块龙头连续大涨后，资金向同板块跟涨股扩散。
(详细 checks 见 git 历史 v0.4 版本，此处略)

---

## Anti-Pattern Checklist

Reject or heavily discount ideas where:

- 唯一边缘是某 KOL / 大 V 提过
- 公司仅与主题相邻，不是结构必需
- thesis 无法命名精确组件 / 材料 / 产能节点
- 停在显性卡点，不挖到二阶 / 三阶
- 替代品可在 6-12 月内被快速认证
- 公司在链条但赚不到经济（中间商命运）
- 定增 / 债务 / 治理问题能吃掉所有上行
- 催化剂路径只是"市场会注意到"
- 短挤压 / 低流通 / 题材热点比经营 thesis 更强
- 大股东 / 高管在过去 6 个月有大幅减持
- 控股股东股权质押 > 80% 且股价持续下跌
- 商誉占净资产 > 50%（隐藏减值雷）
- 业绩预告与最终披露历次大幅偏离
- 公司互动易回复全是 boilerplate

记住：好的技术不等于好的股票；总 TAM 不等于公司可捕获的 TAM；"是英伟达的供应商"
不等于显著的收入。
