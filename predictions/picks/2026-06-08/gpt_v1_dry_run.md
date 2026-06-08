# LLMstocks-gpt v1.0 dry-run 分析结果

> 日期：2026-06-08  
> 性质：研究样例 / 非锁定预测  
> 目的：按 `docs/UPGRADE_PLAN.md` 的三轴框架跑一版结果，验证“机构评测 + 顶级投资人持仓 + 产业链供需”如何进入选股判断。  
> 重要提示：本报告不是投资建议，不自动下单，不承诺收益。

---

## 0. 本轮结论

本轮更倾向于把资金放在“AI 基建确定性外溢 + 估值未极端透支”的环节，而不是继续追高光模块、人形机器人等高弹性拥挤票。

优先级最高的是：

- **宁德时代**：NEV 和储能需求仍有硬数据支撑，公司 Q1 利润和现金流质量强，机构一致预期代理信号也最完整。
- **思源电气**：电网、电力设备、数据中心供电瓶颈同时受益，财务增速和机构代理信号都强。
- **工业富联**：AI 服务器需求最直接，但机构持仓代理不如宁德/思源，且北美客户和地缘风险需要继续跟踪。
- **金山办公**：AI 办公商业化和高毛利软件属性明确，但前十大股东减持/询价转让需要作为红旗低到中级别跟踪。
- **中微公司**：半导体设备供需景气强，但估值已经不便宜，适合 BUY/WATCH 边界而非无脑重仓。

明确回避的是：**寒武纪、中际旭创、新易盛、光库科技、绿的谐波**。这些公司不一定差，但本轮共性是估值、涨幅或目标价差已经给出明显过热信号。

---

## 1. 数据与来源约束

本轮使用四类输入：

1. 公司与市场指标：`yfinance`，2026-06-08 本地抓取。
2. 产业链供需：NVIDIA、Microsoft、SEMI、WSTS、NBS、CAAM、CATL 官方/权威披露。
3. 机构评测代理：`yfinance` 可见的 analyst opinions / recommendation / target price。注意这不是 FactSet/Wind/Choice 授权数据库，只能作为中等质量代理。
4. 聪明钱代理：`yfinance.major_holders` 的机构持股比例和机构数量，以及少量公开年报/季报前十大股东片段。注意这不是完整基金季报数据库。

本轮缺口：

- 尚未接入 Wind/Choice/FactSet/Refinitiv 的正式一致预期。
- 尚未系统解析所有基金季报、社保组合、QFII、北向/港股通历史持仓。
- 未全文读取每家公司最近 90 天所有公告，因此红旗扫描是“重点红旗样例”，不是正式锁定级别。

---

## 2. 市场背景

### 2.1 AI 基建需求仍强

- NVIDIA 2026-05-20 公布 FY2027 Q1 收入 816.15 亿美元，同比 +85%；Data Center 收入 752 亿美元，同比 +92%。这直接支持 AI 服务器、网络、PCB、光通信、半导体设备等链条需求。
- Microsoft FY2026 Q2 公布 Microsoft Cloud 收入 515 亿美元，同比 +26%；Azure 和其他云服务收入同比 +39%。这说明云厂商需求仍未熄火。
- SEMI World Fab Forecast 2Q26 更新预计 2026 年全球设备支出 1,520 亿美元，同比 +24%，中国仍是全球最大支出市场。半导体设备轴仍有硬供需支撑。
- NBS 2026 年 5 月制造业 PMI 为 50.0，新订单 49.9，说明总需求并不强；但高技术制造和装备制造 PMI 分别为 52.9 和 52.1，结构性强于总体。

### 2.2 中国新能源车和储能仍有支撑，但国内车市有分化

- CAAM 口径下，2026 年 4 月中国 NEV 产量 132 万辆，同比 +5.5%；销量 134 万辆，同比 +9.7%。
- CATL 2026 Q1 披露收入 1,291.31 亿元，同比 +52.45%；归母净利润 207.38 亿元，同比 +48.52%；经营现金流 336.81 亿元。
- CATL 官方 2025 年报新闻稿引用 SNE Research：2025 年全球动力电池份额 39.2%，连续九年第一；储能电池出货份额 30.4%，连续五年第一。

---

## 3. AI 推荐 / 科技链优先关注

| 排名 | 股票 | 判断 | 总分 | 核心理由 | 主要风险 |
|---:|---|---|---:|---|---|
| 1 | 工业富联 `601138.SH` | BUY | 78 | AI 服务器最直接；yfinance 显示 TTM PE 34.4、forward PE 19.8、ROE 24.3%、营收增速 56.5%、利润增速 103.8%；公司 2025 业绩预增公告显示全年归母净利预计同比 +51% 到 +54%。 | 北美云厂商/核心客户集中；出口管制和地缘风险；机构持股比例代理仅 4.5%，更多是控股股东/产业资本属性。 |
| 2 | 金山办公 `688111.SH` | BUY/WATCH | 76 | 软件高毛利 + AI 办公；yfinance 显示 TTM PE 28.7、ROE 26.9%、利润率 58.2%、营收增速 24%。2025 年报/公告显示 WPS AI、协作、国际化是主线。 | 前十大股东中多方减持/询价转让需要跟踪；AI 付费转化仍需财报验证。 |
| 3 | 中微公司 `688012.SH` | WATCH+ | 72 | SEMI 设备支出和中国晶圆厂 capex 支撑强；yfinance 显示营收增速 34.1%、利润增速 194%、利润率 20.8%。 | TTM PE 91.5、forward PE 53.7，估值已经不低；需要订单和新品放量继续兑现。 |
| 4 | 中科曙光 `603019.SH` | WATCH | 68 | AI4S、算力基础设施、国产算力链条受益；yfinance 显示 TTM PE 51.7、forward PE 31.2，近 60 日回撤约 11%，相对不过热。 | ROE 9.9% 不算强；需要更多订单和利润弹性验证。 |
| 5 | 浪潮信息 `000977.SZ` | WATCH | 66 | AI 服务器弹性大，forward PE 17.8；估值比多数 AI 硬件票温和。 | yfinance 显示最近营收增速为负，利润率仅 1.7%；需确认 AI 服务器放量是否真正改善利润。 |

未入选但继续观察：

- 沪电股份 `002463.SZ`：基本面很强，但近 60 日涨幅约 +78.7%，当前价 137 元已高于 yfinance 目标均价 110.37 元，暂不追。
- 北方华创 `002371.SZ`：设备主线强，但估值较高，盈利增速代理不如中微。

---

## 4. 全市场推荐 / 非纯 AI 主线

| 排名 | 股票 | 判断 | 总分 | 核心理由 | 主要风险 |
|---:|---|---|---:|---|---|
| 1 | 宁德时代 `300750.SZ` | BUY | 82 | 供需、财务、机构代理三轴最完整。Q1 收入同比 +52.45%、归母净利同比 +48.52%；yfinance 显示 TTM PE 22.4、forward PE 16.3、ROE 25.4%。23 个 analyst opinions，recommendation 为 strong_buy，目标均价较现价约 +41.6%。 | 国内车市需求分化、价格战、海外政策/贸易风险。 |
| 2 | 思源电气 `002028.SZ` | BUY | 80 | 电网设备、数据中心供电、海外电力建设共振；yfinance 显示 TTM PE 42.9、forward PE 28.4、ROE 22.7%、营收增速 41.6%。10 个 analyst opinions，strong_buy，目标均价较现价约 +36.5%。2025 Q3 报显示全国社保基金六零一组合在前十大无限售股东中。 | 估值不低；项目交付和海外订单节奏会影响短期表现。 |
| 3 | 阳光电源 `300274.SZ` | BUY/WATCH | 72 | 储能 PCS/逆变器龙头；yfinance 显示 TTM PE 25.3、forward PE 17.4、ROE 25.0%。16 个 analyst opinions，recommendation 为 buy，目标均价较现价约 +17%。 | yfinance 最近营收/利润增速代理为负，说明光伏链价格战和周期压力仍在；需要储能占比持续提升。 |
| 4 | 药明康德 `603259.SH` | WATCH+ | 70 | 估值和财务代理很好：TTM PE 13.9、forward PE 13.5、ROE 25.7%、利润率 43.6%、营收增速 28.8%。 | CXO 地缘政策风险仍是硬红旗；没有接入完整海外法案/客户订单数据库前，不升为高置信 BUY。 |
| 5 | 当升科技 `300073.SZ` | WATCH | 66 | 正极材料周期修复代理信号强：yfinance 显示营收增速 137.2%、利润增速 132.9%，目标均价较现价约 +51%。 | ROE 5.6%、利润率 6.1%，行业仍可能供给过剩；更像周期反弹，不是高质量复利。 |

---

## 5. 过热不推荐

| 排名 | 股票 | 判断 | 红旗 | 证据 |
|---:|---|---|---|---|
| 1 | 寒武纪 `688256.SH` | AVOID | 估值极端 + 题材拥挤 | yfinance 显示 TTM PE 291.5、PB 61.0、近 60 日约 +62.4%。AI 芯片需求真，但价格已提前反映太多。 |
| 2 | 中际旭创 `300308.SZ` | AVOID / 不追高 | 涨幅过热 + 目标价倒挂 | yfinance 显示近 60 日约 +111.1%、TTM PE 85.9、PB 36.1；当前价 1154.99 元高于目标均价 914.43 元。 |
| 3 | 新易盛 `300502.SZ` | AVOID / 不追高 | 涨幅过热 + 估值拥挤 | yfinance 显示近 60 日约 +82.5%、TTM PE 71.3、PB 35.4；当前价 725 元高于目标均价 625.98 元。 |
| 4 | 光库科技 `300620.SZ` | AVOID | 估值极端 | yfinance 显示近 60 日约 +83.8%、TTM PE 361.0、forward PE 599.3；1 个 analyst target 为 177 元，显著低于现价 299.67 元。 |
| 5 | 绿的谐波 `688017.SH` | AVOID | 机器人题材拥挤 + 盈利质量不足以支撑估值 | yfinance 显示近 60 日约 +98.4%、TTM PE 571、forward PE 315，ROE 3.9%。 |

备选回避：

- 中国卫星 `600118.SH`：TTM PE 8220、forward PE 576，利润率和 ROE 很低。虽然近 60 日未明显过热，但估值与盈利质量明显不匹配。
- 沪电股份 `002463.SZ`：业务质量强，但短线涨幅和目标价倒挂使其更适合等待回撤，而不是当前追入。

---

## 6. 三轴证据评分摘要

| 股票 | 基本面 | 机构评测代理 | 聪明钱代理 | 供需 | 估值 | 结论 |
|---|---:|---:|---:|---:|---:|---|
| 宁德时代 | 19/20 | 14/15 | 11/15 | 22/25 | 9/10 | BUY |
| 思源电气 | 18 | 14 | 10 | 21 | 7 | BUY |
| 工业富联 | 18 | 8 | 7 | 24 | 8 | BUY |
| 金山办公 | 18 | 8 | 5 | 18 | 8 | BUY/WATCH |
| 中微公司 | 15 | 7 | 6 | 23 | 4 | WATCH+ |
| 阳光电源 | 16 | 12 | 8 | 19 | 8 | BUY/WATCH |
| 药明康德 | 18 | 6 | 5 | 16 | 10 | WATCH+ |
| 中际旭创 | 20 | 9 | 8 | 24 | 1 | AVOID/不追 |
| 寒武纪 | 16 | 5 | 5 | 20 | 0 | AVOID |
| 绿的谐波 | 8 | 4 | 4 | 18 | 0 | AVOID |

---

## 7. 下一步建议

要把这版 dry-run 升级成正式 `/picks`，需要先补三件事：

1. 接入或半自动解析基金季报、前十大流通股东、社保/QFII/保险/公募持仓变化，替代 yfinance 的机构持股比例代理。
2. 把 `templates/picks_card.yaml` 升级为 `institutional_view`、`smart_money`、`supply_demand`、`gpt_scorecard` 四块。
3. 改 `lock_picks.py`，没有供需硬证据和红旗反证就不能锁定。

---

## 8. 主要来源

- NVIDIA FY2027 Q1 results: https://investor.nvidia.com/news/press-release-details/2026/NVIDIA-Announces-Financial-Results-for-First-Quarter-Fiscal-2027/default.aspx
- Microsoft FY2026 Q2 results: https://www.microsoft.com/en-us/Investor/earnings/FY-2026-Q2/press-release-webcast
- SEMI World Fab Forecast 2Q26: https://www.semi.org/ko/products-services/market-data/world-fab-forecast
- WSTS Spring 2026 forecast entry: https://wsts.tsia.org.tw/index.aspx
- NBS PMI May 2026: https://www.stats.gov.cn/english/PressRelease/202606/t20260601_1963851.html
- NBS Industrial Production April 2026: https://www.stats.gov.cn/english/PressRelease/202605/t20260519_1963760.html
- Xinhua / CAAM NEV April 2026: https://english.news.cn/20260511/0dcff9a7e6b248a5957d0d2da0b3fbd6/c.html
- CATL 2025 annual report news: https://www.catl.com/en/news/6773.html
- CATL 2026 Q1 report: https://static.cninfo.com.cn/finalpage/2026-04-16/1225107946.PDF
- CATL 2026 investor record: https://static.cninfo.com.cn/finalpage/2026-04-16/1225109217.PDF
- 工业富联 2025 年度业绩预增公告: https://static.cninfo.com.cn/finalpage/2026-01-29/1224953921.PDF
- 工业富联 2025 年年度报告: https://static.cninfo.com.cn/finalpage/2026-03-11/1225004420.PDF
- 阳光电源 2025 年年度报告摘要: https://static.cninfo.com.cn/finalpage/2026-04-01/1225066677.PDF
- 金山办公 2025 年年度报告相关公告: https://money.finance.sina.com.cn/corp/view/vCB_AllBulletinDetail.php?id=12019049&stockid=688111
- 思源电气 2025 Q3 report: https://static.cninfo.com.cn/finalpage/2025-10-18/1224719649.PDF
- SEC Form 13F FAQ, used for smart-money lag caveat: https://www.sec.gov/rules-regulations/staff-guidance/frequently-asked-questions-about-form-13f
