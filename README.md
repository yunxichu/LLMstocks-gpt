# LLMstocks-gpt

> 基于 [yunxichu/LLMstocks](https://github.com/yunxichu/LLMstocks) 复制并升级的 A 股研究工作流。当前仓库先保留原项目的 Claude Code 选股 SOP、锁定/跟踪工具和 HTML 报告能力；新增升级方向是把**主流机构评测、顶级投资人持仓、产业链供需分析**纳入每只股票的证据链和评分规则。详见 [`docs/UPGRADE_PLAN.md`](docs/UPGRADE_PLAN.md)。

---

# LLMstocks 原始基线

> A 股研究轻量工作流，由 Claude / Claude Code 驱动。每周产出 **3 类 × 5 = 15
> 支 picks**（AI 推荐 / 全市场推荐 / 过热不推荐），每只标的经过 **18 类暴雷
> 信号扫描** + **evidence_log 强制溯源**，输出**交互式 HTML 报告**。所有预测
> SHA-256 锁定不可改，按真实时间流逝做前瞻测试（相对沪深 300 超额）。

[![Version](https://img.shields.io/badge/version-v0.8-blue.svg)](PLAN.md)
[![License](https://img.shields.io/badge/license-personal_research-lightgrey.svg)](#合规与免责)
[![Data](https://img.shields.io/badge/data-yfinance%20+%20WebFetch-green.svg)](docs/SETUP.md)

---

## 这是什么

LLMstocks 不是一个跑在固定 agent 框架里的多智能体系统，也不是量化回测平台。
它是一套**让 Claude 自主选股的 SOP**：

- **工具层** (`data/web/`)：境外可访问的数据接口（yfinance + Claude WebFetch
  到 巨潮/新浪/财联社/SEC EDGAR）
- **Playbook 层** (`playbooks/`)：Markdown 工作流，让 Claude 按 6-stage 选股
- **入口层** (`.claude/commands/`)：Claude Code slash commands
  (`/picks` 主力，`/analyze` 辅助)
- **预测锁定 + 跟踪** (`predictions/` + `tools/`)：每条 picks 落盘不可改，
  每个交易日自动跟踪 T+1/5/10/20 相对沪深 300 超额

完全可从**境外环境**运行（开 VPN 即可），不依赖中国大陆专有 API。

---

## 核心特点

### 🎯 3 类 picks 主输出（v0.8）

| 类别 | 数量 | 选择规则 |
|---|---|---|
| 🚀 **AI 相关推荐** | 5 支 | theme ∈ {ai-compute, optical-cpo, semi-equipment, robotics, domestic-software} |
| 💎 **全市场推荐** | 5 支 | theme ∉ AI_THEMES（含 watchlist 单独名） |
| ⚠️ **过热不推荐** | 5 支 | 任意主题，≥1 HIGH 或 ≥2 MEDIUM 红旗 |

选择顺序: **AVOID 先 → AI → 全市场**（3 类 ticker 不重叠）

### 🚩 18 类暴雷信号强制扫描（v0.6）

每只候选必须跑全 18 类 red flag scan（业绩雷 / 现金流背离 / 应收存货异常 / 商
誉雷 / 大股东减持 / 解禁 / 质押 / 关联交易 / 审计 / 监管 / 高管异常 / 稀释 /
ST / 政策 / 海外 / 题材熄火 / 估值过热 / 散户狂热），详见
[`playbooks/references/red-flags.md`](playbooks/references/red-flags.md)。

- BUY: 0 HIGH + ≤1 MEDIUM
- AVOID: ≥1 HIGH 或 ≥2 MEDIUM（每条带 evidence + URL + 日期）

### 🔍 Evidence_log 强制溯源（v0.7）

每只 pick 必须有 `evidence_log` ≥ 3 个 `type='hard'` entries（yfinance 字段
值 / WebFetch URL + 公告标题 / 公开文件引用）。任何非 hard claim（市场共识 /
行业常识 / 定性判断）**必须显式标 `type: soft` 或 `pending_verify`**。

防止 thesis 用"Tesla 供应链"、"NVIDIA 代工"这种未核实市场共识当事实证据。
lock 工具强制校验，不达标拒收。

### 🖱️ 交互式 HTML 报告（v0.8）

`tools/render_picks_html.py` 生成 **self-contained HTML**（inline CSS + 零 JS
+ HTML5 `<details>` 折叠），浏览器打开即可点击展开每只 pick 的：
- 📋 详细分析（why_now / 跟踪指标 / 主要风险 / 入场价 / rubric）
- 🔍 证据链（evidence_log 全表，颜色区分 HARD / SOFT / PENDING_VERIFY）
- 🚩 Red flag 扫描（HIGH / MEDIUM / LOW 染色 + 具体证据 + 来源）

可发邮件、可手机打开、可打印。

### 🔒 预测锁定 + 前瞻测试

每条 picks 写入时立即 SHA-256 锁定（`lock_picks.py`），事后不可改。每个交易
日盘后跑 `update_tracking.py` 自动拉收盘 + 沪深 300 收盘，计算 T+1/5/10/20
相对超额。T+20 后跑 `/review` 出客观胜率 + 规避率 + 综合 alpha 统计。

不做历史回测（用户的量化在别处）。这是**真实时间流逝**的 paper trading。

---

## 当前状态

**v0.8** — 阶段 0/1/2 已完成；首份 v0.6 baseline picks（`picks_192556`，5 BUY
legacy + 5 AVOID）已锁定且开始跟踪；v0.8 schema 升级完成，**下一份 /picks 起
正式输出 15-name 3-class 报告**。

详见 [PLAN.md](PLAN.md) 的进度速览 + 阶段路线图。

---

## 快速开始

### 1. 环境要求

- Python 3.10+
- Windows / macOS / Linux 均可（项目以 Windows + PowerShell 为开发环境）
- 网络能访问 query2.finance.yahoo.com（国内开 VPN 即可，海外直连）
- Claude Code (CLI)

### 2. 装依赖

```powershell
cd E:\LLMstocks    # 或你的实际项目路径
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e .
```

### 3. 配 watchlist

```powershell
Copy-Item watchlist\watchlist.yaml.example watchlist\watchlist.yaml
notepad watchlist\watchlist.yaml    # 加你想跟踪的票
python tools/refresh_universe.py
```

### 4. 第一次 /picks（在 Claude Code 内）

```
/picks
```

Claude 会自动跑 6-stage 流水线（候选池 → 初评 → 短列表 → WebFetch + 18 类
红旗 → 选 5+5+5 → 锁定 + 生成 HTML），约 30-45 分钟。

输出：
- `predictions/picks/<date>/picks_<HHMMSS>.yaml` — 结构化数据
- `predictions/picks/<date>/picks_<HHMMSS>.raw.md` — Markdown 报告
- `predictions/picks/<date>/picks_<HHMMSS>.html` — **交互式 HTML（双击打开）**

### 5. 每个交易日盘后

```powershell
python tools/update_tracking.py
```

自动跟踪所有 locked picks 的 T+1/5/10/20 表现。

### 6. 月末复盘

```
/review
```

按 AI / 全市场 / AVOID 三轨分别统计胜率 + 规避率 + 综合 alpha。

---

## 主要 slash commands

| 命令 | 用途 | 频率 |
|---|---|---|
| **`/picks`** | **PRIMARY** — 产出 15 支 picks（3 类 × 5）+ HTML 报告 | 周日 / 手动 |
| `/analyze <ticker>` | 单股长期深度分析（16 维 rubric） | 想深入某只时 |
| `/review` | 客观复盘（基于真实跟踪数据，4 轨分别统计） | 月度 / T+20 后 |
| `/lhb` | 龙虎榜分析 | ⚠️ V2 deferred (数据需境内 API) |
| `/screen` | 周筛 | ⚠️ v0.6 已合并入 `/picks` |

---

## 项目结构

```
LLMstocks/
├── PLAN.md                              # 工作计划 (v0.8) — 路线图、决策、变更日志
├── README.md                            # 本文件
├── pyproject.toml / .env.example
├── docs/SETUP.md                        # 详细安装 + 故障排查
│
├── config/
│   ├── themes.yaml                      # 10 个 A 股主题 + ~50 代表股
│   └── filters.yaml
│
├── data/web/                            # 主数据层 (境外可访问)
│   ├── a_share.py / benchmark.py / calendar.py / us_stocks.py
│   ├── announcement.py (WebFetch URL helpers)
│   └── ...
├── data/ashare/                         # V2 deferred (境内 API)
│
├── playbooks/                           # Claude 工作流
│   ├── weekly_picks.md                  # ⭐ PRIMARY (6-stage)
│   ├── long_term.md                     # 辅助 single-stock
│   ├── review.md                        # 月度复盘
│   ├── short_term.md / lhb.md           # V2 deferred
│   └── references/
│       ├── red-flags.md                 # ⭐ 18 类暴雷信号
│       ├── research-rubric.md           # 16 维评分
│       ├── pattern-library.md           # 14 类模式
│       └── a-share-data-sources.md
│
├── templates/
│   └── picks_card.yaml                  # 3-list schema (v0.8)
│
├── predictions/
│   ├── picks/<date>/                    # ⭐ 主输出 (yaml + raw.md + html)
│   ├── picks_index.csv                  # 每只 ticker 一行索引
│   ├── locked/                          # v0.5 legacy 单股 lock
│   └── tracking/                        # per-ticker T+N 跟踪 JSON
│
├── watchlist/
│   ├── watchlist.yaml(.example)
│   └── universe.csv                     # refresh_universe 生成
│
├── tools/
│   ├── refresh_universe.py
│   ├── lock_picks.py                    # ⭐ Schema 校验 + SHA-256 锁定
│   ├── render_picks_html.py             # ⭐ HTML 报告生成
│   ├── update_tracking.py               # 自动跟踪
│   ├── verify_locks.py                  # 防篡改检测
│   ├── lock_prediction.py               # v0.5 单股 lock 工具
│   └── _picks_stage12.py                # v0.6 Stage 1+2 scratch (保留作 audit)
│
└── .claude/commands/                    # Claude Code 入口
    ├── picks.md / analyze.md / review.md
    └── lhb.md (deprecated notice)
```

---

## 数据来源与境外可用性

| 数据 | 接口 | 境外可用 |
|---|---|---|
| A 股 OHLCV / 财务 / 估值 | `data.web.a_share.*` (yfinance) | ✅ |
| 沪深 300 基准 | `data.web.benchmark.benchmark_close_on('000300.SH')` | ✅ |
| 交易日历 | `data.web.calendar.*` | ✅ |
| 公司公告 | Claude WebFetch → 新浪财经公告页 | ✅ |
| 行业新闻 / 政策 | Claude WebFetch → 财联社 / 第一财经 / 发改委 | ✅ |
| 美股龙头对照 | `data.web.us_stocks.*` (yfinance) | ✅ |
| 美股 13F | Claude WebFetch → SEC EDGAR | ✅ |
| 龙虎榜 / 公募季报 / 主力资金流 | ⚠️ V2 deferred | ❌ |

⚠️ **巨潮资讯网 (cninfo.com.cn) 是 JS SPA**，WebFetch 静态 HTML 拿不到内容；
已统一改用新浪财经 (`https://vip.stock.finance.sina.com.cn/...`)，验证可用。

⚠️ **北向资金实时数据自 2024-08-19 改季度披露**，不再用作短期信号。

⚠️ **yfinance 对中证 800/1000 历史数据缺失**（只有最近 1 天），已切换沪深 300
作为默认基准（v0.5 hotfix）。

详见 [docs/SETUP.md](docs/SETUP.md) + [playbooks/references/a-share-data-sources.md](playbooks/references/a-share-data-sources.md)。

---

## 设计原则

1. **轻量优先** — 不造多智能体框架（Claude 即调度者），不引 Celery/Redis/FastAPI
2. **境外可访问** — 完全可从美国/欧洲/中国+VPN 环境运行
3. **证据强制溯源** — 每个 claim 必须 HARD / SOFT / PENDING_VERIFY 标记
4. **预测不可改** — SHA-256 锁定 + git 历史 + 跟踪记录，防事后马后炮
5. **诚实输出** — 候选不够 5 个就输出 fewer + 说明原因；不凑数
6. **18 类红旗硬扫** — 防业绩雷 / 减持 / 解禁 / 关联交易 / 商誉雷等暴雷信号漏检

---

## 合规与免责

- **本项目产出为研究信号，不构成投资建议**
- 不做实盘自动下单
- 不输出精确买入价 / 目标价 / 止损价 / 仓位百分比
- 不存储 / 分发研报全文（版权约束）
- 不对外分发（定位个人研究工具）
- 实盘决策与风险由使用者自行承担
- 数据源遵循各 API 提供商 ToS（Tushare 商用授权、东财系限流等）

---

## 设计致谢

借鉴的开源方法论（不 fork 代码，仅借鉴设计）：

- **[Serenity.SKILL](https://github.com/xvhaoran778-cyber/Serenity.SKILL)** — chokepoint 投资法、Bayesian 证据更新、18 维评分体系
- **super-detective** (个人前作) — 变局卡片 YAML 格式、影响链上中下游、五大维度（政策/技术/产业/资本/叙事）
- **AI Hedge Fund** (`virattt/ai-hedge-fund`) — 多智能体设计参考（最终未采用，转为 playbook 模式）

---

## 文档导航

| 文档 | 内容 |
|---|---|
| [PLAN.md](PLAN.md) | **总规划** — 路线图、阶段、决策、变更日志、风险登记 |
| [docs/SETUP.md](docs/SETUP.md) | 详细安装 + 故障排查 |
| [playbooks/weekly_picks.md](playbooks/weekly_picks.md) | 主流水线 6-stage 工作流 |
| [playbooks/references/red-flags.md](playbooks/references/red-flags.md) | 18 类暴雷信号清单 + 检测方法 |
| [playbooks/references/research-rubric.md](playbooks/references/research-rubric.md) | 16 维单股评分体系 |
| [playbooks/references/pattern-library.md](playbooks/references/pattern-library.md) | 14 类可复用模式 |
| [playbooks/references/a-share-data-sources.md](playbooks/references/a-share-data-sources.md) | 数据源优先级 |
| [templates/picks_card.yaml](templates/picks_card.yaml) | 输出 schema |

---

## 仓库

https://github.com/yunxichu/LLMstocks
