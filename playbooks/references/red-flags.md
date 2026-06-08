# A-Share Red Flag Scanner

Systematic checklist of暴雷 signals for A-share stocks. Every candidate in the
`/picks` pipeline MUST be scanned against this list (Stage 4 of `weekly_picks.md`).

Two roles:
- **BUY candidates** — must PASS all HIGH-severity checks (any hit → eject)
- **AVOID candidates** — must TRIGGER at least one HIGH or MEDIUM-severity flag

**Source priority** for evidence:
1. 公司公告 (via WebFetch 新浪财经公告页 `vip.stock.finance.sina.com.cn`)
2. 财务数据 (via `data.web.a_share` yfinance wrapper)
3. 监管 / 行业新闻 (via WebFetch 财联社 / 第一财经)

**Severity legend**:
- **HIGH**: 单条命中即应进入 AVOID 池，BUY 候选直接剔除
- **MEDIUM**: 单条不致命，但 ≥2 个 MEDIUM 累积 → AVOID 池；BUY 候选要 lower confidence
- **LOW**: 信息记录，不主动剔除，但写入 `concerns`

---

## Quick checklist (18 categories)

| # | Category | Severity |
|---|---|---|
| 1 | 业绩雷 (Earnings shock) | HIGH |
| 2 | 现金流-净利严重背离 | HIGH |
| 3 | 应收账款 / 存货异常激增 | MEDIUM |
| 4 | 商誉雷 (Goodwill bomb) | HIGH |
| 5 | 大股东 / 高管减持 | MEDIUM-HIGH |
| 6 | 大额解禁压力 | MEDIUM |
| 7 | 股权质押过高 | HIGH if >80% & 跌 |
| 8 | 关联交易 / 资金占用 | MEDIUM-HIGH |
| 9 | 审计问题 / 审计师变更 | HIGH |
| 10 | 监管处罚 / 立案调查 | HIGH |
| 11 | 关键管理层异常变动 | MEDIUM-HIGH |
| 12 | 可转债 / 定增稀释 | MEDIUM |
| 13 | ST / 退市风险警示 | HIGH |
| 14 | 行业政策风险 | MEDIUM |
| 15 | 海外 / 地缘风险 (制裁 / 出口管制) | MEDIUM-HIGH |
| 16 | 题材熄火（板块龙头回落 + 跟涨股仍高位） | MEDIUM |
| 17 | 估值过热（PE 历史 80+ 分位 + 涨幅过大） | MEDIUM |
| 18 | 散户狂热 (社交媒体讨论爆炸 + 龙虎榜散户主导) | LOW-MEDIUM |

---

## 1. 业绩雷 (Earnings shock) — HIGH

**Signal**: 业绩预告 / 业绩快报与最终披露大幅偏差；或近期突发业绩下修。

**Detection**:
- WebFetch `https://vip.stock.finance.sina.com.cn/corp/go.php/vCB_AllBulletin/stockid/<6digit>.phtml`
- 搜公告标题含 "业绩预告" / "业绩快报" / "业绩修正"
- 重点：业绩预告下修方向、扣非净利同比下滑 > 30%
- 同时拉 yfinance quarterly_financials 看最近季度 Net Income 是否突然恶化

**Thresholds**:
- 业绩预告下修 / 业绩预告与正式披露偏差 > 30% → HIGH
- 最近 2 季度净利同比 < -30% → HIGH
- 最近 1 季度净利同比 -10% 到 -30% → MEDIUM

**BUY impact**: HIGH 命中直接剔除。
**AVOID trigger**: 单条 HIGH 即可触发。

**False positive caveat**: 周期股低谷不算业绩雷（看是否伴随基本面恶化）；季节性波动（如教培公司暑期 Q2 弱）也要排除。

---

## 2. 现金流-净利严重背离 — HIGH

**Signal**: 经营性现金流 / 净利润 (OCF / NI) 长期 < 70%，或 FCF 持续为负但净利为正。

**Detection** (yfinance only, fast):
```python
from data.web import a_share
ai = a_share.stock_financials(ticker)
acf = a_share.stock_cashflow(ticker)
years = sorted(ai.columns)[-4:]  # last 4 years
ratios = []
for y in years:
    ni = ai.loc['Net Income', y]
    ocf = acf.loc['Operating Cash Flow', y]
    if ni and ni > 0:
        ratios.append(ocf / ni)
# OCF/NI 中位数 < 0.7 或连续 3 年 < 0.7 → 警讯
```

**Thresholds**:
- OCF/NI 4 年均 < 50% → HIGH（财务造假高度怀疑）
- OCF/NI 4 年均 < 70% → MEDIUM
- FCF 连续 3+ 年为负但净利为正 → HIGH

**BUY impact**: HIGH 剔除；MEDIUM lower confidence。
**AVOID trigger**: HIGH 触发；MEDIUM 配合其他 flag 触发。

**False positive caveat**: 早期/高增长公司大量资本开支可能压低 FCF（如新能源车企）；周期性收账款波动正常。看的是**长期趋势**不是单年。

---

## 3. 应收账款 / 存货异常激增 — MEDIUM

**Signal**: 应收账款 / 存货增速明显超过营收增速，提示销售质量下降或渠道压货。

**Detection** (yfinance):
```python
abs_ = a_share.stock_balance_sheet(ticker)
ai = a_share.stock_financials(ticker)
# 应收账款 / 营收 (DSO proxy)
for y in years:
    ar = abs_.loc.get('Accounts Receivable', {}).get(y)
    rev = ai.loc['Total Revenue', y]
    if ar and rev:
        print(y, ar/rev)
# 比值持续上升 > 30% 是警讯
```

**Thresholds**:
- 应收账款 / 营收 比值 3 年内上升 > 50% → MEDIUM
- 存货 / 营收 比值 3 年内上升 > 50% → MEDIUM
- 应收增速持续 > 营收增速 × 2 → MEDIUM

**BUY impact**: lower confidence + 写入 concerns。
**AVOID trigger**: 配合其他 flag。

**False positive caveat**: 业务模式转型（如从直销到经销）会暂时拉高应收；季节性 (Q4 高存货为春节备货) 也常见。

---

## 4. 商誉雷 (Goodwill bomb) — HIGH

**Signal**: 商誉 / 净资产比例过高，并购标的若业绩不达预期会引发大额减值。

**Detection** (yfinance):
```python
abs_ = a_share.stock_balance_sheet(ticker)
y = abs_.columns[0]  # most recent
goodwill = abs_.loc.get('Goodwill', {}).get(y, 0) or 0
equity = abs_.loc['Stockholders Equity', y]
ratio = goodwill / equity if equity else 0
```

**Thresholds**:
- 商誉 / 净资产 > 50% → HIGH
- 商誉 / 净资产 30-50% → MEDIUM
- 已有商誉减值历史 + 新并购标的 → HIGH

**BUY impact**: HIGH 剔除。
**AVOID trigger**: HIGH 触发。

**False positive caveat**: 部分行业（医药 / 软件）商誉天然较高，需结合并购标的业绩承诺兑现情况判断。

---

## 5. 大股东 / 高管减持 — MEDIUM-HIGH

**Signal**: 近 6 个月大股东 / 高管 / 实控人发布减持公告。

**Detection** (WebFetch):
- URL: `https://vip.stock.finance.sina.com.cn/corp/go.php/vCB_AllBulletin/stockid/<6digit>.phtml`
- 搜公告标题含 "减持" / "股份减持计划" / "减持股份进展"
- 关注：减持比例（占总股本 %）、减持人身份（控股股东 / 实控人 / 董监高）

**Thresholds**:
- 控股股东 / 实控人减持 > 1% 总股本 → HIGH
- 多位董监高同时减持 → HIGH
- 单一董监高减持 → MEDIUM
- 减持计划已披露但未执行（窗口期内）→ MEDIUM

**BUY impact**: HIGH 剔除；MEDIUM 仅 lower confidence。
**AVOID trigger**: HIGH 单条触发。

**False positive caveat**: 部分股权激励行权后小幅减持是正常的；定期换届导致董事会调整需结合时点判断。

---

## 6. 大额解禁压力 — MEDIUM

**Signal**: 未来 30-90 天有大额限售股上市（占流通股 > 10%）。

**Detection** (WebFetch):
- 搜 "限售股上市流通" / "解禁"
- 注意解禁规模 vs 流通股本，以及解禁对象（战投 / 定增 / 股权激励）

**Thresholds**:
- 解禁规模 > 流通股本 20% → MEDIUM-HIGH
- 解禁规模 5-20% → MEDIUM
- 解禁对象是高位定增的机构（可能高位套现）→ 加重

**BUY impact**: 30 日内有 > 20% 解禁 → 剔除；其他 lower confidence。
**AVOID trigger**: 配合估值过热使用。

**False positive caveat**: 解禁不必然导致下跌；优质公司大解禁后反而见底是常事。看的是组合效应。

---

## 7. 股权质押过高 — HIGH (if >80% + 股价跌)

**Signal**: 控股股东股权质押比例过高，叠加股价下跌，存在强平风险。

**Detection** (WebFetch):
- 搜 "股权质押" / "股份质押"
- 注意：质押比例（占其持股 %）、被质押股份是否冻结、平仓线

**Thresholds**:
- 控股股东质押 > 80% + 近 60 日股价 < -15% → HIGH（强平风险）
- 控股股东质押 > 80% + 股价平稳 → MEDIUM
- 控股股东质押 60-80% → LOW-MEDIUM

**BUY impact**: HIGH 剔除。
**AVOID trigger**: HIGH 触发。

**False positive caveat**: 部分大股东质押用于扩大产业投资，不必然是负面；但需结合股价走势综合判断。

---

## 8. 关联交易 / 资金占用 — MEDIUM-HIGH

**Signal**: 大额关联交易转移利润，或控股股东占用上市公司资金。

**Detection** (WebFetch):
- 年报 / 半年报中"关联交易"专章
- 公告搜 "关联交易" / "对外担保" / "资金占用"
- 重点：关联交易占营收比例、是否公允定价、对外担保是否给关联方

**Thresholds**:
- 关联交易占营收 > 30% 且持续上升 → HIGH
- 上市公司大额对外担保（占净资产 > 50%）给关联方 → HIGH
- 资金占用历史记录 → HIGH（即使已归还）
- 关联交易占营收 10-30% → MEDIUM

**BUY impact**: HIGH 剔除。
**AVOID trigger**: HIGH 触发。

---

## 9. 审计问题 / 审计师变更 — HIGH

**Signal**: 审计师出具保留 / 拒绝 / 否定意见；或频繁更换审计师。

**Detection** (WebFetch):
- 年报中"审计报告"段，看审计意见类型
- 搜公告 "会计师事务所变更" / "审计意见"
- 注意：非"标准无保留意见"都是警讯

**Thresholds**:
- 保留意见 / 拒绝表示意见 / 否定意见 → HIGH
- 2 年内更换审计师 ≥ 2 次 → HIGH
- 重大事项段提示 → MEDIUM

**BUY impact**: HIGH 直接剔除。
**AVOID trigger**: HIGH 触发。

---

## 10. 监管处罚 / 立案调查 — HIGH

**Signal**: 证监会立案 / 警告 / 处罚；或公司被监管问询函要求重大整改。

**Detection** (WebFetch):
- 搜 "证监会" / "立案调查" / "处罚决定" / "问询函"
- 检查 csrc.gov.cn 处罚公示

**Thresholds**:
- 证监会立案调查 → HIGH（极严重）
- 行政处罚（罚款 + 高管警告）→ HIGH
- 多次问询函（>2 个）→ MEDIUM-HIGH

**BUY impact**: HIGH 剔除。
**AVOID trigger**: HIGH 触发。

---

## 11. 关键管理层异常变动 — MEDIUM-HIGH

**Signal**: 董事长 / 总经理 / CFO / 独董异常离任，尤其是任职不满 1 年的离任。

**Detection** (WebFetch):
- 搜 "辞职" / "任免" / "选举"
- 关注离任原因（"个人原因" 警讯比"工作调整"严重）
- 多名董事 / 高管同期离任 = 红灯

**Thresholds**:
- CFO 异常离任 → HIGH
- 董事长 + 总经理同期离任 → HIGH
- 独董抗议性离任（披露反对意见）→ HIGH
- 单人非定期离任 + 原因模糊 → MEDIUM
- 定期换届（任期到）→ LOW（中性）

**BUY impact**: HIGH 剔除。
**AVOID trigger**: HIGH 触发。

**False positive caveat**: 定期换届导致大面积变动是中性；区分关键在于"是否符合既定任期"。

---

## 12. 可转债 / 定增稀释 — MEDIUM

**Signal**: 近期发行可转债或定增（非公开发行），稀释影响。

**Detection** (WebFetch):
- 搜 "非公开发行" / "可转债" / "定向增发" / "配股"
- 关注：发行规模 vs 总股本、发行价 vs 现价、用途

**Thresholds**:
- 大额定增（> 总股本 20%）+ 发行价远低于现价 → MEDIUM-HIGH
- 频繁定增（2 年内 2 次以上）→ MEDIUM-HIGH
- 可转债占总股本 > 10% → MEDIUM

**BUY impact**: lower confidence；配合估值高时剔除。
**AVOID trigger**: 触发条件之一。

**False positive caveat**: 高质量公司定增扩产是正面（如比亚迪历史 H 股定增）；判断关键是"用途 + 时点"。

---

## 13. ST / 退市风险警示 — HIGH

**Signal**: 已被 ST / *ST / 退市风险警示。

**Detection** (yfinance + WebFetch):
```python
info = a_share.stock_info(ticker)
name = info.get('shortName', '')
is_st = 'ST' in name.upper() or '*ST' in name.upper()
```
也搜公告 "退市风险警示" / "其他风险警示"

**Thresholds**:
- 任何形式 ST 标记 → HIGH（直接 AVOID 池）
- 连续 2 年净利为负 → HIGH（即将 ST）
- 净资产为负 → HIGH

**BUY impact**: HIGH 直接剔除（永不进 BUY）。
**AVOID trigger**: HIGH 触发。

---

## 14. 行业政策风险 — MEDIUM

**Signal**: 行业突发监管收紧（教培整顿 / 反垄断 / 出口管制等）。

**Detection** (WebFetch):
- 财联社 / 第一财经搜行业关键词 + "监管" / "整顿" / "规范"
- 国务院 / 发改委 / 工信部新发文件

**Thresholds**:
- 已发布明确收紧文件 → MEDIUM-HIGH
- 传闻 / 征求意见 → MEDIUM
- 长期方向性收紧（无明确事件）→ LOW

**BUY impact**: 关联行业 BUY 候选 lower confidence。
**AVOID trigger**: 短期受冲击大的标的进 AVOID。

---

## 15. 海外 / 地缘风险 — MEDIUM-HIGH

**Signal**: 公司被列入实体清单 / 美国 SDN / 海外资产风险 / 出口受限。

**Detection** (WebFetch):
- 搜公司名 + "制裁" / "实体清单" / "出口管制"
- 美国 BIS Entity List 网站搜索
- 关注海外营收占比（财报披露）

**Thresholds**:
- 已列入实体清单 → HIGH（业务直接受冲击）
- 主要海外市场（>20% 营收）面临关税或限制 → MEDIUM-HIGH

**BUY impact**: 关联标的 lower confidence 或剔除。
**AVOID trigger**: HIGH 触发。

---

## 16. 题材熄火 — MEDIUM

**Signal**: 板块龙头开始连续回落，跟涨股估值仍高位，资金切换信号明显。

**Detection** (yfinance):
- 选定板块龙头股，看近 30 日是否从高点回撤 > 15%
- 跟涨股是否仍维持高 PE / 高换手
- 板块整体涨幅榜是否落后大盘

**Thresholds**:
- 板块龙头从高位 -15% + 跟涨股 PE 历史 80+ 分位 → MEDIUM
- 板块整体回撤 > 20% + 仍有 "题材股" 高位 → MEDIUM-HIGH

**BUY impact**: 题材类 BUY 候选 lower confidence。
**AVOID trigger**: 配合估值过热使用，触发 AVOID。

---

## 17. 估值过热 — MEDIUM

**Signal**: 当前 PE 在 5 年历史 80+ 分位 + 近 60-90 日累计涨幅过大。

**Detection** (yfinance):
```python
info = a_share.stock_info(ticker)
pe_now = info.get('trailingPE')
hist = a_share.stock_history(ticker, period='5y')
# 自算 EPS 历史分位 (粗略)
# 或简化: 近 60 日涨幅
hist_60d = hist.tail(60)
ret_60d = hist_60d['Close'].iloc[-1] / hist_60d['Close'].iloc[0] - 1
```

**Thresholds**:
- PE 历史 80+ 分位 + 近 60 日涨幅 > 50% → MEDIUM-HIGH
- 近 30 日涨幅 > 50% + 无对应业绩催化 → MEDIUM-HIGH
- 近 60 日涨幅 30-50% → LOW-MEDIUM

**BUY impact**: lower confidence；与"题材熄火"叠加时剔除。
**AVOID trigger**: 主要触发条件。

**False positive caveat**: 短期上涨可能因业绩超预期是合理的；要看 forward PE 是否仍合理。

---

## 18. 散户狂热 — LOW-MEDIUM

**Signal**: 雪球 / 股吧 / 微博讨论量短期爆炸性增长；龙虎榜散户营业部主导（V2 才能精确测）。

**Detection** (WebFetch):
- 雪球热度榜 (xueqiu.com/hots)
- 股吧帖子热度
- v0.5 没有精确量化指标，主要靠定性观察

**Thresholds**:
- 雪球热度排名进入前 30 + 30 日涨幅 > 30% → LOW-MEDIUM
- 出现在多个财经短视频 / 公众号 → LOW

**BUY impact**: 配合其他 flag 使用。
**AVOID trigger**: 配合估值过热 + 题材熄火。

**False positive caveat**: 散户讨论本身不是 sell signal；用作 contrarian 反向指标时要小心。

---

## Aggregate Decision Logic

After scanning all 18 categories for a candidate:

```
high_count = 命中 HIGH severity 的 flag 数
medium_count = 命中 MEDIUM severity 的 flag 数

if high_count >= 1:
    → AVOID 池
    → BUY 候选直接剔除
elif medium_count >= 2:
    → AVOID 池候选（综合判断）
    → BUY 候选 confidence × 0.7
elif medium_count == 1:
    → BUY 候选 confidence × 0.85，写入 concerns
else:
    → 通过 red flag scan，可进 BUY 评分阶段
```

**输出到 picks_card.yaml 必填**:
```yaml
red_flags_checked: [list of all 18 categories scanned]  # 永远是 1-18 全列
red_flags_triggered:  # 触发的 flag
  - category: <number + name>
    severity: HIGH | MEDIUM | LOW
    evidence: "<concrete fact + source URL + date>"
    detection_method: yfinance | WebFetch:<source>
```

BUY 类要求 `red_flags_triggered = []` 或仅含 LOW。
AVOID 类要求 `red_flags_triggered` 至少含 1 个 HIGH 或 2 个 MEDIUM。

---

## Honest Limitations (v0.5)

无法精确检测的（V2 deferred）:
- 龙虎榜营业部细节（散户 vs 机构）
- 公募季报重仓变化
- 实时资金流入流出
- 内幕消息 / 知情人交易

仍能高质量检测的（v0.5）:
- 财务数据驱动的所有 flag（OCF/NI, 商誉, 应收, ST 等）
- 公告驱动的所有 flag（减持, 解禁, 质押, 关联交易等）via 新浪财经
- 公开新闻驱动的 flag（监管处罚, 政策, 地缘 etc.）via 财联社

v0.5 的覆盖估计能抓 80%+ 真正的"暴雷"，剩余 < 20% 主要在游资博弈和内幕信息层面。
