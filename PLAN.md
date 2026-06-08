# A股 LLM 选股助手 — 工作计划文档

> 版本：v0.8（主输出拆 3 类 × 5 = 15 picks: AI 推荐 + 全市场推荐 + 过热不推荐；新增交互式 HTML 报告输出）
> 创建：2026-06-08
> 最近更新：2026-06-08

> LLMstocks-gpt 说明：本仓库已复制原 LLMstocks 基线，并在 [`docs/UPGRADE_PLAN.md`](docs/UPGRADE_PLAN.md) 中新增 v1.0 升级路线。升级重点是将主流机构评测、顶级投资人持仓、产业链供需分析并入证据链、评分和锁定规则。

本文档是项目从立项到长期迭代的总纲。每次重大设计变更、Playbook 修改、新数据源接入、决策变化，都回到本文档对应章节做记录。Playbook 内容单独成文件，本文档只做指引。

---

## 0. 项目愿景与边界

### 0.1 目标

构建一套 A 股研究的**轻量选股助手**，**完全可从境外环境运行**（USA / EU / CN+VPN），**主输出明确的"看好 + 警惕"清单**：

**核心 deliverable（v0.8）**:
- 每周一份 **15-name picks**（via `/picks`），分 3 类：
  - **AI 相关推荐** (`ai_picks`, 5 支) — 限 AI_THEMES (ai-compute / optical-cpo / semi-equipment / robotics / domestic-software)
  - **全市场推荐** (`market_picks`, 5 支) — 非 AI 主题（含 watchlist 单独名）
  - **过热不推荐** (`avoid_picks`, 5 支) — 任意主题
- 每只 pick 必须经过 **18 类暴雷信号扫描**，每条触发记录有具体 evidence
- 每只 pick 必须有 `evidence_log` ≥ 3 hard entries（v0.7）
- BUY (AI + market) 强制 strategy；AVOID 强制 primary_concern
- **v0.8 新增**：交互式 HTML 报告（`render_picks_html.py` 生成 self-contained
  HTML 含 inline CSS + HTML5 `<details>` 折叠，用户点击展开每只 pick 的
  详细分析 / 证据链 / 红旗扫描）

**辅助 deliverable**:
- 单股深度分析（via `/analyze <ticker>`）— 用户对清单中某只想深入了解时触发
- 月度复盘（via `/review`）— picks 胜率 + 规避率统计
- watchlist 校验（via `tools/refresh_universe.py`）

**架构**:
- **工具层**: yfinance + Claude WebFetch（无中国大陆 API 依赖）
- **Playbook 层**: weekly_picks.md（主流水线）+ long_term.md（deep dive）+ red-flags.md（必查）
- **入口层**: Claude Code slash commands（`/picks` 主，`/analyze` 辅）
- **预测锁定 + 跟踪层**: 每条 picks 锁定不可变，自动跟踪 T+1/5/10/20

**核心理念**：LLM 是分析引擎；项目准备好"原料"+"清单"+"暴雷红线"+"评估纪律"；预测一旦输出立即锁定，靠真实时间流逝来检验。

### 0.2 不做什么（明确边界）
- 不做实盘自动下单
- 不输出精确买入价 / 目标价 / 止损价 / 仓位百分比
- 不做对外分发（定位个人研究工具）
- 不存储或分发研报全文（版权约束）
- 不做历史回测（量化在其他地方做；本项目只做前瞻测试）
- 不修改已锁定的预测
- **v0.6 不做短期分析**（V2 配境内 MCP 后恢复）
- 不允许 "watchlist only / neutral" 输出 —— 必须给 BUY 或 AVOID verdict
- 不允许 BUY 候选有 HIGH / MEDIUM 严重的暴雷信号
- 不允许 AVOID 候选无具体 evidence

### 0.3 合规与免责
- 系统产出为研究信号，不构成投资建议
- WebFetch 内容仅供研究，不复制原文
- 实盘决策与风险由使用者自行承担

### 0.4 项目环境
- 路径：`E:\LLMstocks`
- 平台：Windows 11 / PowerShell
- 主入口：Claude Code slash commands
- 主要 LLM：Claude

### 0.5 项目进度速览 (snapshot @ 2026-06-08)

#### 已完成 ✅

| Phase | 状态 | 关键产物 |
|---|---|---|
| 阶段 0 工具就绪 | ✅ | `data/web/` 8 模块 (yfinance + WebFetch verified) |
| 阶段 1 单股流水线 | ✅ | `long_term.md` + `lock_prediction.py` + `update_tracking.py` |
| 阶段 2 picks 主流水线 v0.6 | ✅ | 5 BUY + 5 AVOID + 18 类红旗扫描 |
| v0.7 evidence_log | ✅ | 每只 pick ≥3 hard entries + 显式 soft 标记 |
| v0.8 3 类 + HTML | ✅ | AI 5 + 全市场 5 + 过热 5 + 交互式 HTML 报告 |

#### 进行中 🟡

| Phase | 状态 | 关键信息 |
|---|---|---|
| 阶段 3 前瞻测试 第 1 期 | 🟡 跟踪中 | `picks-20260608-192556` (v0.6 legacy) 已 lock, 等待 T+20 (~2026-07-06) |

#### 待启动 ⏸️

| Phase | 状态 | 触发条件 |
|---|---|---|
| 阶段 4 客观复盘 | ⏸️ | T+20 后跑 `/review` |
| 阶段 5 V2 境内 MCP (可选) | ⏸️ | 阶段 4 反馈后决定 |

#### 当前用户可用能力

| 命令 / 工具 | 状态 | 用途 |
|---|---|---|
| `/picks` | ✅ ready | 产出 v0.8 3 类 × 5 = 15 支 picks + HTML |
| `/analyze <ticker>` | ✅ ready | 单股 16 维深度分析 |
| `/review` | ✅ ready (待跟踪数据) | 4 轨复盘（AI / 市场 / AVOID / legacy 单股） |
| `python tools/refresh_universe.py` | ✅ ready | 校验 watchlist + 生成 universe.csv |
| `python tools/update_tracking.py` | ✅ ready | 每个交易日盘后跑 |
| `python tools/render_picks_html.py <yaml>` | ✅ ready | 渲染 HTML 报告 |
| `python tools/verify_locks.py` | ✅ ready | 防篡改检测 |
| `/lhb` | ❌ V2 deferred | 龙虎榜需要境内 API |

#### 已有的真实预测档案

| ID | 类型 | 状态 | 关键内容 |
|---|---|---|---|
| `picks-20260608-192556` | v0.6 legacy picks | T+1/5/10/15/20 跟踪中 | 5 BUY (阳光电源/工业富联/金山办公/拓普集团/思源电气) + 5 AVOID (寒武纪/中际旭创/中国卫星/中国软件/中天科技) |
| `600519-20260608-173105-lt` | v0.5 single-stock | 跟踪中 | 茅台 long_term, watchlist confidence 0.42 |

#### 下一步（按优先级）

1. **看 HTML 输出**: 用浏览器打开 `predictions/picks/2026-06-08/picks_192556.html` 验证交互效果
2. **每天跑跟踪**: 盘后 `python tools/update_tracking.py`（可挂 Windows Task Scheduler）
3. **下周日跑首次 v0.8 /picks**: 得到第一份正式 3 类 × 5 报告
4. **T+20 后跑 /review**（约 2026-07-06）: 第一份客观复盘

---

## 1. 阶段路线图

### 阶段 0 + 1：已完成（v0.5 落地）
工具层 + 单股 Playbook + 锁定/跟踪基础设施。

### 阶段 2：v0.6 升级（已完成，今日）
- 5 BUY + 5 AVOID 主流水线就位
- 18 类暴雷信号扫描器（red-flags.md）
- picks_card.yaml 模板 + lock_picks.py
- update_tracking.py / verify_locks.py 兼容 picks
- 单股 long_term.md 重定位为辅助

### 阶段 3：前瞻测试启动（next）
- 用户运行第一次 `/picks` 产出 5+5 清单
- 自动 lock
- 每个交易日 `python tools/update_tracking.py` 跟踪 10 只标的的 T+1/5/10/20 表现
- 第 15-20 个交易日（约 2026-06-26 至 2026-07-03）运行 `/review`

### 阶段 4：客观复盘 + 调优
- 基于真实跟踪数据计算 BUY 胜率 + AVOID 规避率
- 综合 alpha 判断
- 改 playbook（必须在评估期外）

### 阶段 5：V2 — 境内 MCP 代理（可选）
当用户想要恢复短期 / 龙虎榜 / 公募季报 / 研报评级时启动：
- 部署 Tushare + AKShare MCP 在境内云
- Claude Code remote MCP 调用
- 解锁 short_term, lhb 维度 + smart_money 评分维度

### 阶段 6：持续迭代
每周 picks + 每月 review + 每季度方向反思。

---

## 2. 数据层 (v0.5 数据，v0.6 用法不变)

主路径：yfinance + Claude WebFetch（详见 `playbooks/references/a-share-data-sources.md`）。

| 数据 | 接口 |
|---|---|
| 个股 OHLCV / 财务 / 估值 | `data.web.a_share.*` (yfinance) |
| 基准指数（沪深 300 默认）| `data.web.benchmark.*` |
| 交易日历 | `data.web.calendar.*` |
| 美股龙头对照 | `data.web.us_stocks.*` |
| 公司公告 | Claude WebFetch → 新浪财经 (`vip.stock.finance.sina.com.cn`) |
| 行业新闻 / 政策 | Claude WebFetch → 财联社 / 第一财经 / 发改委 |
| 美股 13F | Claude WebFetch → SEC EDGAR |

**Deprecated (V2 路径)**: Tushare API / AKShare 东财接口 / 龙虎榜 / 公募季报 / 主力资金流 / 涨停板梯队 / 研报评级数据库 / 两融 / 大宗交易。

**北向资金降级（不变）**: 2024-08-19 起改季度披露，不用作短期信号。

---

## 3. Playbooks（v0.6 重新组织）

### 3.1 Active Playbooks
| Playbook | 角色 | 触发 |
|---|---|---|
| `weekly_picks.md` | **PRIMARY**: 5 BUY + 5 AVOID 主流水线 | `/picks`（每周日 / 手动） |
| `long_term.md` | **AUXILIARY**: 单股 deep dive | `/analyze <ticker>` |
| `review.md` | 月度客观复盘（picks + single-stock 分轨） | `/review` |

### 3.2 V2 Deferred
- `short_term.md` — 短期分析
- `lhb.md` — 龙虎榜分析

### 3.3 Legacy (v0.5)
- `screen.md` — 已被 weekly_picks 吸收

### 3.4 References (必查)
- **`red-flags.md`** — **18 类暴雷信号 + 检测方法**（强制流水线步骤）
- `research-rubric.md` — 16 维单股评分（用于 BUY 内部排序）
- `pattern-library.md` — 14 类模式（用于 strategy 分类）
- `a-share-data-sources.md` — yfinance + WebFetch 来源优先级

---

## 4. 主输出：5 BUY + 5 AVOID 清单

### 4.1 数据流（`/picks` 运行时）

```
Stage 1: 候选池构建 (30-80 tickers)
  来源: watchlist + themes 代表股 + 美股龙头映射 + 财联社热点
Stage 2: 批量初评 (yfinance only, 快)
Stage 3: 短列表 (15-20 tickers, 含 BUY 候选 + AVOID 候选)
Stage 4: 深度扫描 (WebFetch each — 强制 18 类暴雷扫描)
Stage 5: 选 5 BUY + 5 AVOID
Stage 6: 输出 + Lock
```

### 4.2 强制约束 (lock_picks.py 强制校验, 不满足拒收)
- 3 类 (ai/market/avoid) 各 ≤ 5 支
- BUY 类 (ai + market): `red_flags_triggered` 0 HIGH + ≤1 MEDIUM
- AVOID: `red_flags_triggered ≥ 1 HIGH 或 ≥ 2 MEDIUM`，每条带具体 evidence
- 每只候选 `red_flags_checked = [1..18]`（全 18 类都要扫）
- BUY 5 只之间 strategy + sector 不能过度集中
- 不允许"watchlist only / neutral"
- **v0.7**: 每只 pick 必须有 `evidence_log` ≥ 3 个 type='hard' entries
  (yfinance 字段 / WebFetch URL + 公告 / 公开文件)；所有非 hard claim 显式
  标 `type: soft` 或 `pending_verify`，附 source + content
- **★ v0.8**: 
  - `ai_picks` 中每只 `theme` ∈ AI_THEMES = {ai-compute, optical-cpo, semi-equipment, robotics, domestic-software}
  - `market_picks` 中每只 `theme` ∉ AI_THEMES (或为空表示 watchlist)
  - `ai_picks` ∩ `market_picks` ticker 不重叠
  - Selection 顺序: AVOID 5 → AI 5 → market 5
  - 必须生成 HTML 报告 (`python tools/render_picks_html.py <yaml>`)

### 4.3 失败模式（lock 工具会拒绝）
- 任何 BUY 触发 HIGH/MEDIUM red flag → 拒收 lock
- 任何 AVOID red_flags_triggered 不达 1 HIGH 或 2 MEDIUM → 拒收
- 任何 evidence 字段为空 → 拒收
- red_flags_checked 缺少任一类别 → 拒收

### 4.4 文件结构
```
predictions/
├── picks/                          # v0.6 主输出
│   └── 2026-06-XX/
│       ├── picks_<HHMMSS>.yaml     # 10 ticker structured
│       └── picks_<HHMMSS>.raw.md   # 人读
├── picks_index.csv                 # 一行一 ticker（10 行 per picks）
├── tracking/<picks_id>--<ticker>/  # per-ticker tracking
│   ├── d1.json / d5.json / d10.json / d20.json
├── locked/                         # v0.5 legacy 单股 lock
│   └── 2026-06-08/...              # 茅台 v0.5 lock 保留
└── index.csv                       # v0.5 single-ticker index
```

---

## 5. 单股深度分析（辅助）

通过 `/analyze <ticker>` 触发 `long_term.md` playbook：
- 16 维 rubric
- 完整 chokepoint + Bayesian 工作流
- 输出 `predictions/locked/<date>/<id>.yaml`

**用法场景**:
- 用户看完 picks 想深入某只
- 用户对自己 watchlist 中某只独立评估
- 与 picks 流水线**独立统计**（不混入 picks 平均胜率）

---

## 6. 跟踪 + 复盘 (v0.6 双轨制)

### 6.1 跟踪 (`update_tracking.py`)
- 扫描 `predictions/locked/` (v0.5 single) + `predictions/picks/` (v0.6)
- 展开为 tracking units
- 每个 unit per checkpoint (d1/5/10/15/20) 拉 yfinance close + 沪深 300 close
- 写 `predictions/tracking/<tracking_id>/d<N>.json`

### 6.2 复盘 (`/review`)
**Picks track (PRIMARY)**:
- 胜率_BUY = T+20 超额 > 0 的 BUY 比例
- 规避率_AVOID = T+20 超额 < 0 的 AVOID 比例
- 综合 alpha = 胜率_BUY + 规避率_AVOID - 1

**Single-stock track (LEGACY)**:
- v0.5 老 long_term lock 单独评估
- 不混入 picks 平均

### 6.3 验收阈值
- 综合 alpha > 0: picks 有 alpha → 阶段 4 微调
- 胜率_BUY > 55% AND 规避率_AVOID > 55%: 强信号
- 综合 alpha < -0.1: 反向更准 → 严重 bug，停下来分析

---

## 7. 维护机制

### 7.1 日常使用
- 用户每周日触发 `/picks`
- 每个交易日盘后跑 `python tools/update_tracking.py`（可挂 Windows Task Scheduler）
- 每月初触发 `/review`

### 7.2 前瞻测试纪律
**评估期间禁止修改 playbook**。改动必须在 review 之后 + 记入 §9.4 + 重新启动评估窗口。

---

## 8. 风险登记册

### 8.1 已识别风险
| 风险 | 影响 | 缓解 |
|---|---|---|
| Red flag scan 漏检 | 暴雷未识别 → AVOID 漏报 / BUY 错放 | 强制 18 类全扫；lock 工具校验 |
| 巨潮 SPA WebFetch 失败 | 公告类 red flag 漏检 | 用新浪财经替代（已验证 work） |
| 候选池过窄 | picks 同质化、缺多样性 | watchlist + themes + news + US leaders 多源 |
| BUY confidence 偏低导致 < 5 | picks 不足 5 BUY | 诚实输出 fewer，说明原因 |
| AVOID 候选都是小盘冷门 | 警告价值低 | 排序考虑投资者关注度 |
| yfinance vendor 数据滞后 | 公告类 red flag 时点不准 | WebFetch 巨潮交叉验证 |
| 中证 800/1000 yfinance 缺失 | 已 hotfix 用沪深 300 | 已解决 |
| yfinance 不支持北交所 | BJ 标的不可分析 | 暂排除，等 V2 |
| 前瞻测试样本量小 | 单次 picks 只有 10 个 sample | 多周累积 |
| Playbook 漂移 | Claude 越来越不按 playbook 走 | 定期审计 + git diff |
| 个人时间投入不可持续 | 项目搁置 | 周生成节奏 sustainable |

### 8.2 未知风险探测
- 月度 review 强制问"过去一月最大的意外"
- 季度新增风险登记

---

## 9. 待办与决策记录（活文档）

### 9.1 当前 TODO
- [x] 阶段 0-1：基础设施 + 单股 playbook (v0.5)
- [x] 阶段 2 v0.6：5+5 picks 主流水线 + red-flags.md + lock_picks.py
- [x] v0.7：evidence_log 强制
- [x] v0.8：3 类 (AI/全市场/AVOID) + 交互式 HTML 报告
- [x] picks-20260608-192556 (v0.6 baseline) 已 lock, 进入跟踪
- [x] README.md 项目入口文档
- [ ] **下一步**：用户跑首次 v0.8 `/picks`（首份 3 类 × 5 = 15 支正式报告）
- [ ] **持续**：每个交易日盘后跑 `python tools/update_tracking.py`
- [ ] **里程碑**：T+20 (~2026-07-06) 跑 `/review` 客观复盘
- [ ] 阶段 4 决策（基于 review 结果，决定 playbook 是否调优）
- [ ] 阶段 5 决策：V2 境内 MCP 是否启动（恢复 LHB / 公募季报 / 研报评级数据）

### 9.2 待决策事项
- [ ] LLM 主力模型：Claude Sonnet vs Opus（picks 工作流可能需要更强模型）
- [ ] Windows Task Scheduler 自动跑 `update_tracking.py`？
- [ ] V2 启动时间（取决于 picks 长期 alpha 是否够用）
- [ ] 每周 picks 是否启用 routine 自动跑（vs manual）
- [ ] 是否扩展 themes.yaml 加更多主题 + 代表股

### 9.3 已决策事项
| 日期 | 决策 | 原因 |
|---|---|---|
| 2026-06-08 | A 股为主，美股仅作主题/宏观参考 | 用户目标 |
| 2026-06-08 | 不做实盘下单 | 合规 |
| 2026-06-08 | 不做历史回测 | 用户：量化在他处 |
| 2026-06-08 | 入口：Claude Code slash commands | 用户决策 |
| 2026-06-08 | v0.5 完全外网模式（yfinance + WebFetch）| 用户在国内 + VPN |
| 2026-06-08 | v0.5 hotfix: 基准从中证 800 改沪深 300 | yfinance vendor 覆盖不足 |
| 2026-06-08 | **v0.6: 主输出改为 5 BUY + 5 AVOID 清单** | **用户：选股助手要给"看好 + 警惕"决策** |
| 2026-06-08 | **v0.6: 强制 18 类 red flag 扫描每只候选** | **用户："不能忽略暴雷细节"** |
| 2026-06-08 | **v0.6: BUY 必须无 HIGH/MEDIUM red flag；AVOID 必须 ≥1 HIGH 或 ≥2 MEDIUM** | **lock 工具校验，纪律不可松** |
| 2026-06-08 | **v0.6: long_term.md 降为辅助；screen.md 被 weekly_picks 吸收** | 流水线重构 |
| 2026-06-08 | **v0.6: 茅台 v0.5 lock 保留作 archive，与 picks 分轨统计** | forward-test 纪律 |
| 2026-06-08 | **v0.7: 每只 pick 强制 evidence_log（≥3 hard entries + 显式标 soft）** | **用户：每个结论都需要对应的证据/来源/报告。第一份 picks 发现 BUY thesis 大量依赖未核实的市场共识（如 Tesla 供应链 / NVIDIA 代工 / HVDC 跨界）** |
| 2026-06-08 | **v0.7: 当前 picks_192556 保留作 baseline，附 evidence.md 公开 gap；下一份 picks 起执行 v0.7 schema** | 透明 + 不违反 lock 不可改原则 |
| 2026-06-08 | **v0.8: 主输出拆 3 类（AI 推荐 5 + 全市场推荐 5 + 过热不推荐 5）+ 交互式 HTML 报告** | **用户：分 3 类关注 (AI / 全市场 / 过热不推荐)，HTML 点击查看详细解析** |
| 2026-06-08 | **v0.8: AI_THEMES 集合 = {ai-compute, optical-cpo, semi-equipment, robotics, domestic-software}**；ai_picks 必须 ∈ AI_THEMES, market_picks 必须 ∉ AI_THEMES, ticker 不重叠 | 明确分类边界 |
| 2026-06-08 | **v0.8: Selection 顺序 AVOID 先 → AI → market** | 保证 3 list 不重叠 + 最严重信号先固定 |

### 9.4 变更日志
| 日期 | 类型 | 内容 | 影响 |
|---|---|---|---|
| 2026-06-08 | doc | v0.1 初稿（多智能体方案）| - |
| 2026-06-08 | doc | v0.2: Playbook + 工具 + Claude Code 驱动 | 架构方向转变 |
| 2026-06-08 | doc | v0.3: 验证方式改实盘前瞻测试 | 验证哲学变化 |
| 2026-06-08 | code | v0.4: 阶段 0-1 代码就绪（AKShare/Tushare）| 代码就绪 |
| 2026-06-08 | code | v0.5: 完全外网模式（yfinance + WebFetch）| 数据架构转变 |
| 2026-06-08 | hotfix | v0.5: 基准切沪深 300（yfinance 覆盖）| 真实数据 issue 修复 |
| 2026-06-08 | code | v0.5: 第一个 lock 预测（茅台 long-term）| 端到端 workflow 验证 |
| **2026-06-08** | **code + doc** | **v0.6: 主输出改 5 BUY + 5 AVOID picks；新增 red-flags.md 18 类暴雷扫描；weekly_picks.md 主流水线；picks_card.yaml + lock_picks.py + 升级 update_tracking/verify_locks 支持 picks；long_term.md 降辅助；screen.md 标 deprecated；review.md 加 picks 评估；themes.yaml 加 representative tickers** | **产品定位重大转变：从研究档案到选股助手** |
| 2026-06-08 | code | v0.6 第一次 /picks 实施：picks-20260608-192556（5 BUY 阳光电源/工业富联/金山办公/拓普集团/思源电气 + 5 AVOID 寒武纪/中际旭创/中国卫星/中国软件/中天科技）；候选池 49 → 短列表 14 → 5+5；WebFetch 新浪财经 14/14 成功 | 端到端 workflow 验证通过 |
| 2026-06-08 | fix | lock_picks BUY 规则与 weekly_picks.md §3 对齐（允许 ≤1 MEDIUM）| 第一次 lock 时发现 |
| **2026-06-08** | **code + doc** | **v0.7: 每只 pick 强制 evidence_log（≥3 hard + 显式标 soft/pending_verify）；picks_card.yaml schema 升级；weekly_picks.md 加 Stage 4b "Evidence collection"；lock_picks.py 加 evidence_log 校验；picks.md command 提示更新；当前 picks_192556 附加 evidence.md 公开 gap (lock 不动)** | **用户反馈：每个结论需对应证据/来源；防止 thesis 用未核实市场共识充当事实** |
| **2026-06-08** | **code + doc** | **v0.8: buy_picks (5) → ai_picks (5) + market_picks (5)，avoid_picks (5) 保留；新增 `tools/render_picks_html.py` 生成 self-contained interactive HTML 报告；lock_picks.py 强制校验 3-list 不重叠 + AI_THEMES 一致；weekly_picks.md Stage 5 重写为 5a(AVOID)→5b(AI)→5c(market)；update_tracking.py 兼容 3 list；picks_card.yaml schema 升级；review.md 改 4 轨评估** | **用户：分 3 类 (AI / 全市场 / 过热不推荐) × 5 支 + HTML 点击查看详细解析** |

---

## 10. 附录

### 10.1 关键术语
- **Playbook**: Markdown 形式的分析工作流
- **Picks Card**: 5 BUY + 5 AVOID 的单文件 YAML（v0.6 主输出）
- **Stock Card**: 单股深度分析 YAML（辅助）
- **LOCK 区**: 预测时点固化字段，不可变（SHA-256 校验）
- **Red Flag**: 18 类暴雷信号之一
- **Tracking Unit**: 每条 prediction 对应的跟踪单元（per ticker）
- **Strategy** (BUY): CHOKEPOINT / QUALITY_COMPOUNDER / VALUE / SPECIAL_SITUATION
- **Primary Concern** (AVOID): OVERHEATED / EARNINGS_RISK / DILUTION / MANAGEMENT / 等

### 10.2 关键参考资源
- Serenity.SKILL（设计参考）: https://github.com/xvhaoran778-cyber/Serenity.SKILL
- super-detective（设计参考）: `E:\super-detective`
- yfinance: https://github.com/ranaroussi/yfinance
- 巨潮资讯（v0.5 SPA 不可用）/ 新浪财经（v0.5 可用）/ SSE / SZSE
- SEC EDGAR: https://www.sec.gov/edgar

### 10.3 目录结构 (v0.6)
```
E:\LLMstocks\
├── PLAN.md
├── pyproject.toml / .gitignore / .env.example
├── docs/SETUP.md
│
├── config/
│   ├── filters.yaml
│   └── themes.yaml                  # 10 主题 + 代表股
│
├── data/
│   ├── web/                         # v0.5+ 主数据层
│   │   ├── yf_client.py / a_share.py / benchmark.py / calendar.py
│   │   ├── us_stocks.py / announcement.py / universe.py
│   └── ashare/                      # V2 deferred
│
├── playbooks/                       # Claude 工作流
│   ├── weekly_picks.md              # v0.6 PRIMARY ✨
│   ├── long_term.md                 # 辅助 deep dive
│   ├── review.md                    # 月度复盘
│   ├── short_term.md / lhb.md       # V2 deferred
│   ├── screen.md                    # v0.6 legacy (吸收入 picks)
│   └── references/
│       ├── red-flags.md             # v0.6 NEW ✨ 18 类暴雷
│       ├── research-rubric.md       # 16 维（v0.5）
│       ├── pattern-library.md       # 14 模式
│       └── a-share-data-sources.md
│
├── templates/
│   ├── picks_card.yaml              # v0.6 NEW ✨
│   └── stock_card.yaml              # 单股
│
├── predictions/
│   ├── picks/<date>/                # v0.6 PRIMARY ✨
│   │   ├── picks_<HHMMSS>.yaml
│   │   └── picks_<HHMMSS>.raw.md
│   ├── picks_index.csv              # per-ticker index
│   ├── locked/<date>/               # v0.5 legacy 单股
│   ├── index.csv                    # v0.5 index
│   └── tracking/                    # per-tracking-unit
│       └── <tracking_id>/d{1,5,10,15,20}.json
│
├── watchlist/
│   ├── watchlist.yaml / .example
│   ├── universe.csv
│   └── history/
│
├── tools/
│   ├── lock_picks.py                # v0.6 NEW ✨
│   ├── lock_prediction.py           # v0.5 单股
│   ├── update_tracking.py           # v0.6 升级，支持两者
│   ├── verify_locks.py              # v0.6 升级，支持两者
│   └── refresh_universe.py
│
└── .claude/commands/
    ├── picks.md                     # v0.6 PRIMARY ✨
    ├── analyze.md                   # 辅助
    ├── review.md / screen.md
    └── lhb.md                       # V2 deferred notice
```

---

## 维护说明

- 本文档是**活文档**
- Playbook 修改、新数据源接入、决策变化，都回到对应章节更新
- 每次更新顶部"最近更新"日期 + §9.4 变更日志
- **前瞻测试期间 playbook 修改必须记入 §9.4 并标注"样本污染"**
- 待决策事项由用户拍板后转入 §9.3
- 项目终止时写明终止原因，归档保留
