# LLMstocks 安装与配置指南 (v0.5)

本项目是 A 股研究的轻量工作流，Claude Code 驱动。v0.5 起完全使用境外可访问的
数据源（yfinance + Claude WebFetch），不依赖中国大陆 API，从任何网络环境都
能跑通。

---

## 1. 环境要求

- Python 3.10+
- Claude Code 已安装
- 任何能访问 Yahoo Finance 的网络环境（国内开 VPN / 海外 / 公司网）

---

## 2. 安装依赖

```powershell
# 在 E:\LLMstocks 下
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e .
```

只需要主依赖。**不需要** Tushare token，**不需要** AKShare（v0.5 已切换到
yfinance）。

可选依赖（默认不装）：
```powershell
pip install -e ".[dev]"             # 测试 + 静态检查
pip install -e ".[ashare-legacy]"   # V2 才需要的 AKShare（境内访问）
pip install -e ".[tushare]"         # V2 才需要的 Tushare Python 客户端
```

---

## 3. 环境变量

```powershell
Copy-Item .env.example .env
notepad .env
```

v0.5 关键变量：
- `YF_REQUEST_INTERVAL`：yfinance 单次调用间隔（秒），默认 0.5

不再需要 Tushare token、不再需要 AKShare 限流环境变量。

---

## 4. 验证数据接入

跑一行 Python 测试 yfinance：

```powershell
python -c "from data.web import a_share; info = a_share.stock_info('600519.SH'); print(info.get('shortName'), info.get('marketCap'))"
```

应该输出 `KWEICHOW MOUTAI ...` 加一个大数。如果失败，检查 VPN / 网络。

测试基准指数：
```powershell
python -c "from data.web import benchmark; df = benchmark.benchmark_history('000300.SH'); print('rows:', len(df), '| last:', df.tail(1))"
```

测试交易日历：
```powershell
python -c "from data.web import calendar; print('last 3 trading days:', calendar.trading_calendar()[-3:])"
```

---

## 5. 配置 watchlist

```powershell
Copy-Item watchlist\watchlist.yaml.example watchlist\watchlist.yaml
notepad watchlist\watchlist.yaml
```

按需添加你想长期追踪的票（ticker 格式：`600519.SH` / `000001.SZ`），然后：

```powershell
python tools/refresh_universe.py
```

这会校验所有 watchlist 条目并生成 `watchlist/universe.csv`。

---

## 6. 启动分析

在 Claude Code 内：

```text
/analyze 600519
/screen
/review
```

`/lhb` 和短期 `/analyze` 在 v0.5 deprecated（依赖中国大陆专有数据），等 V2。

---

## 7. 故障排查

| 现象 | 可能原因 | 处理 |
|---|---|---|
| `requests.exceptions.ConnectionError` 访问 query2.finance.yahoo.com | 网络不通 Yahoo Finance | 在国内开 VPN，或换网络 |
| `yfinance` 返回空 DataFrame / 部分 | yfinance vendor 数据有空白 (常见于小盘股或非交易日) | 多查几次，或换 ticker |
| `/analyze` 输出格式不一致 | LLM 或 playbook 漂移 | 检查 `playbooks/long_term.md` 是否被改动 |
| `predictions/locked/` 文件被修改 | 违反不可变约定 | `python tools/verify_locks.py` 检查 |
| `add_trading_days out of range` | 交易日历未覆盖目标日期 | 重启 Python（lru_cache 刷新） |
| `北交所 (.BJ) 暂不支持` | yfinance 不覆盖北交所 | 暂不分析北交所，等 V2 |

---

## 8. V1 (v0.5) vs V2 路线图

| 能力 | V1 (v0.5, 现在) | V2 (未来) |
|---|---|---|
| 个股中长期分析 | ✅ yfinance + WebFetch | ✅ + 公募季报 + 研报评级 |
| 短期分析 (/analyze short) | ❌ deferred | ✅ + 龙虎榜 + 主力资金流 |
| 龙虎榜 (/lhb) | ❌ deferred | ✅ |
| 周筛 (/screen) | ✅ watchlist-based | ✅ + 全市场扫描 |
| 复盘 (/review) | ✅ long-term only | ✅ + short-term |
| 主题/赛道扫描 (/theme) | 设计就绪未实现 | ✅ |

V2 关键依赖：**部署一台境内云服务器（阿里云轻量 ¥10/月）** 跑 Tushare + AKShare
MCP，让 Claude Code 用 remote MCP 调用。这是未来的 1-2 小时一次性工作。

---

## 9. 合规与免责

- 系统产出为**研究信号**，不构成投资建议
- 不存储或分发研报全文
- 任何对外形式使用前必须重新评估合规
- 实盘决策与风险由使用者自行承担

---

## 10. 相关文档

- `PLAN.md` — 工作计划与方法论（v0.5）
- `playbooks/long_term.md` — 中长期分析工作流
- `playbooks/references/research-rubric.md` — 16 维评分体系
- `playbooks/references/pattern-library.md` — 14 类可复用模式
- `playbooks/references/a-share-data-sources.md` — 数据源优先级
- `templates/stock_card.yaml` — 输出模板
