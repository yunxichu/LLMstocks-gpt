# A-Share Data Sources & News Triage

> **v0.5 update**: This reference is rewritten for **overseas-accessible** data
> only. We use yfinance for quantitative data (quotes, financials, valuation)
> and Claude WebFetch for qualitative evidence (announcements, news, policy
> documents). No China-mainland-only APIs (Tushare, AKShare 东财) are required.
>
> Trade-off: data points that have no overseas substitute (龙虎榜, 主力资金流,
> 公募季报重仓, A 股研报评级) are deferred to V2 when we may add a境内 MCP proxy.

---

## Core principle

**Fetch live news and disclosures via Claude WebFetch.** Chokepoint research
depends on Bayesian updates. Recent announcements, financings, customer wins,
subsidies, earnings calls, dilution, and negative reports materially change
the posterior probability that a company is a true bottleneck.

**Quantitative data via yfinance** (works from overseas), **qualitative data via
WebFetch** to public Chinese disclosure portals (also reachable from overseas
since they are public websites, not APIs).

---

## Source Priority (v0.5)

| Priority | Source | Access | What it tells you |
|---:|---|---|---|
| 1 | 交易所披露 (SSE / SZSE), 巨潮资讯 CNINFO | Claude WebFetch | 年报 / 半年报 / 季报 / 定增 / 关联交易 / 重大合同 / 业绩预告 / 减持 / 股权质押 |
| 2 | 公司财务数据 (income, cashflow, balance) | yfinance (`data.web.a_share`) | Annual + quarterly statements (3-5 yr history) |
| 3 | 公司基本信息 (sector, industry, marketCap, PE, PB) | yfinance (`data.web.a_share.stock_info`) | Snapshot — note PE/PB are trailing TTM |
| 4 | 公司 IR 页, 业绩说明会, 路演纪要 | Claude WebFetch | Segment detail, backlog, capacity, guidance |
| 5 | 政策文件 (发改委, 工信部, 财政部, 行业主管部门) | Claude WebFetch | Strategic criticality, 国家战略/补贴 backstop |
| 6 | 客户 / 供应商技术文档, 产品页, BOM | Claude WebFetch | Supply-chain role, qualification language |
| 7 | 互动平台 (上证 e 互动, 深交所互动易) | Claude WebFetch | 管理层回复 (lower authority than 公告) |
| 8 | 美股龙头 financials/quote | yfinance (`data.web.us_stocks`) | Sector context (NVDA / TSLA / AMD etc.) |
| 9 | 美股 13F 持仓 (SEC EDGAR) | Claude WebFetch | 顶级投资人对中概股 ADR 持仓 |
| 10 | 财经媒体 (财联社, 第一财经, 21 经济报道) | Claude WebFetch | Timely leads, requires verification |
| 11 | 社交媒体 (雪球, 微博, 股吧, 知乎) | Claude WebFetch | Idea generation only; verify before trusting |

---

## Key Web Endpoints (for Claude WebFetch)

### 交易所与披露平台
- 巨潮资讯网：http://www.cninfo.com.cn — 上市公司公告统一披露平台（**最常用**）
  - 按代码搜：`http://www.cninfo.com.cn/new/disclosure/stock?stockCode=<code>`
  - 全文搜索：`http://www.cninfo.com.cn/new/fulltextSearch?keyWord=<keyword>`
- 上海证券交易所：http://www.sse.com.cn — 上市公司信息披露
  - 按代码：`http://www.sse.com.cn/disclosure/listedinfo/announcement/?productId=<code>`
- 深圳证券交易所：http://www.szse.cn — 信息披露
  - 按代码：`http://www.szse.cn/disclosure/listed/notice/index.html?code=<code>`
- 北京证券交易所：https://www.bse.cn

### 互动平台
- 上证 e 互动：http://sns.sseinfo.com — 投资者向上市公司提问
- 深交所互动易：http://irm.cninfo.com.cn — 同上

### 政策与监管
- 中国证监会：http://www.csrc.gov.cn — 监管政策、处罚决定
- 发改委：https://www.ndrc.gov.cn — 产业政策
- 工信部：https://www.miit.gov.cn — 行业政策、专项扶持
- 国家市场监督管理总局：https://www.samr.gov.cn — 反垄断、并购审批

### 财经媒体
- 财联社：https://www.cls.cn
- 第一财经：https://www.yicai.com
- 21 世纪经济报道：https://www.21jingji.com
- 新京报：https://www.bjnews.com.cn

### 美股 13F
- SEC EDGAR：https://www.sec.gov/edgar
- 13F 全文搜索：https://efts.sec.gov/LATEST/search-index?q=<query>&forms=13F

### 港股
- 香港交易所披露易：https://www1.hkexnews.hk

---

## URL helpers in code

`data.web.announcement` module provides:

```python
from data.web import announcement

# All disclosure URLs for one ticker
announcement.disclosure_urls_for("600519.SH")
# -> {"cninfo": "...", "exchange": "..."}

# Search 巨潮 for a keyword
announcement.cninfo_search_url("业绩预告")

# SEC EDGAR 13F search
announcement.sec_edgar_search_url("Kweichow Moutai")
```

Pass any of these to Claude's `WebFetch` tool to read the page.

---

## A-Share Specific Disclosure Events to Track

| Event | Disclosure timing | Why it matters | Where to find (WebFetch) |
|---|---|---|---|
| 年报 | 次年 1 月 31 日前预约，4 月 30 日前完成 | 全面财务 + 全年业务进展 | 巨潮 / 交易所 |
| 一季报 | 4 月 30 日前 | Q1 业绩验证年度 guidance | 巨潮 |
| 半年报 | 8 月 31 日前 | 中报最详细 | 巨潮 |
| 三季报 | 10 月 31 日前 | 决定全年节奏 | 巨潮 |
| 业绩预告 | 1 月底 / 7 月中 / 10 月中（披露规则触发） | 业绩拐点的提前信号；偏差大就是雷 | 巨潮 / 搜 "业绩预告" |
| 业绩快报 | 年报披露前 1 个月内（自愿） | 比预告更精确 | 巨潮 |
| 定增公告 | 不定期 | 稀释 + 资金用途 + 价格 | 巨潮 / 搜 "非公开发行" |
| 重大合同 | 不定期 | 客户/订单证据 | 巨潮 |
| 解禁 | 公告披露解禁日 | 30 日窗口承压 | 巨潮 / 搜 "限售股上市" |
| 大股东 / 高管减持 | 提前 15 日公告 | 强负面信号 | 巨潮 / 搜 "减持" |
| 股权质押 | 即时公告 | 控股股东资金压力 | 巨潮 / 搜 "股权质押" |
| 异动公告 | 涨跌幅或股价异常时 | 监管关注信号 | 巨潮 |

---

## News-to-Evidence Triage

Classify every news item Claude reads into one of three categories. Default to
"noise" if uncertain — false confirmation is worse than missed evidence.

### Thesis-confirming
- 客户认证 / 大订单签订
- 业绩超预期（业绩预告 / 业绩快报）
- 政策落地 / 补贴公布 / 试点城市公布
- 产能投产 / 良率突破
- 重要专利 / 标准制定
- 战略合作（与有名客户 / 政府）

### Thesis-weakening
- 替代技术验证成熟
- 客户自研 / 转向竞争对手
- ramp 失败 / 良率不达标
- 毛利下行 / 价格战
- 大额定增（稀释）
- 业绩雷 / 业绩远低于预告
- 管理层动荡
- 监管处罚

### Neutral / Noise
- 单纯股价上涨 / 下跌新闻
- 热门帖讨论
- 重复的老新闻
- 无来源的小道消息
- 跟主题相邻但与公司无关

格式（每条重要新闻）：
```
Item -> Source URL -> Date -> Thesis impact -> Evidence strength -> Follow-up check
```

---

## CRITICAL: 北向资金数据约束（仍然适用）

**2024-05-13 起**：沪深股通的实时买入/卖出/总成交金额不再披露。

**2024-08-19 起**：北向资金由按日公布改为按季度公布。

**影响**：
- 任何"北向今天净买入 XX 亿、加仓某股"的实时信号已不存在
- 不要依赖北向做短期信号
- 北向数据现在仅作为**季度级别的中长期参考**

在 v0.5 中，可通过 WebFetch 巨潮的"沪深股通持股变动"季度披露访问，但优先级低
（季度延迟 + 不可作为短期信号）。

---

## V2 Deferred (when境内 MCP proxy is added)

These data points are not currently available in v0.5 due to overseas access
constraints. They will be revisited in V2:

- **龙虎榜 (LHB)** — 营业部买卖明细
- **主力资金流** — 个股 / 板块 daily
- **涨停板梯队** — 开盘啦数据
- **公募基金季报重仓股** — 季度披露
- **QFII / 社保 / 养老金持仓变动** — 季度
- **A 股研报评级与目标价** — 机构研报数据库
- **业绩预告与一致预期对比** — 需要 sell-side consensus 数据
- **两融余额** — 两融数据
- **大宗交易** — 折溢价信息

V2 path: 部署一台境内云服务器（阿里云轻量 ¥10/月）跑 Tushare + AKShare MCP，
Claude Code 用 remote MCP 调用。

---

## Industry Information Sources (常用)

| 行业 | 主要信源 (via WebFetch) |
|---|---|
| 半导体 | SEMI 中国 (semi.org/cn), 中国半导体行业协会, ICinsights |
| AI 算力 | NVIDIA / AMD 财报, OpenAI 博客, 中国信通院 |
| 光通信 | LightReading, 中国信通院光通信白皮书 |
| 新能源 | 中汽协, 中国电池联盟, 储能行业协会 |
| 机器人 | 高工机器人, IFR 国际机器人联合会 |
| 医药 | 药智数据, NMPA 药品审评中心 |
| 国防 | 中国船舶报, 中航工业, 国防科工局公开发布 |

---

## Minimum Live Analysis Standard

Before any stock card is locked:

1. Verify ticker / market / latest filing period via yfinance `stock_info`
2. WebFetch 巨潮按代码搜，看最近 3-6 个月官方披露 (small caps / fast-moving sectors: 12 月)
3. WebFetch 检查是否有近期定增 / 减持 / 解禁 / 重大合同
4. At least one source that validates the supply-chain role (公告 / 客户官网 / 行业报告)
5. Explicitly write down unresolved gaps in `open_checks`

---

## Compliance & Copyright Notes

- **不存储研报全文** — 只取标题 / 评级 / 目标价 / 发布日期
- **WebFetch 内容仅供研究** — 不在 raw.md 中直接复制超过摘录长度的原文
- Tushare 商用需授权（v0.5 已不使用 Tushare）
- 任何对外分发都要重新评估
