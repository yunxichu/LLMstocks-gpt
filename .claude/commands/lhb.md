---
description: 龙虎榜分析（V1 deprecated — defer to V2）
---

# /lhb is DEPRECATED in v0.5

LHB (龙虎榜) data is sourced from China-mainland-only APIs (东财 / AKShare)
which are not accessible from overseas environments.

## What to do instead

- For long-term analysis: use `/analyze <ticker>` (works in v0.5)
- For short-term flow signals: defer to V2

## When will this return?

V2 will add a境内 MCP proxy (deployed on a Chinese cloud server) that lets
Claude Code reach Tushare / AKShare from overseas via a thin remote MCP layer.
At that point, `/lhb` (and short-term `/analyze`) become active again.

See `PLAN.md` V2 roadmap section.

## If user really wants something now

Suggest WebFetch to 同花顺 / 东方财富 网页版的"今日龙虎榜"页面（虽然境外
访问也可能不稳，但作为最后手段）—— 不要 lock 为正式预测，只作 informal note。

---

**This command should reply to the user with the above explanation and exit.
Do not attempt to fetch LHB data via the deprecated `data.ashare.lhb` module
in v0.5.**
