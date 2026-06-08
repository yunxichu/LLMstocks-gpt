"""Render a self-contained interactive HTML report from a locked picks YAML.

Usage:
    python tools/render_picks_html.py predictions/picks/<YYYY-MM-DD>/picks_<HHMMSS>.yaml

Produces: <same dir>/picks_<HHMMSS>.html

Features:
- Self-contained single file (inline CSS, zero JS — uses HTML5 <details>)
- 3 sections: AI 推荐 / 全市场推荐 / 过热不推荐
- Each pick card: ticker + name + verdict + thesis summary, click to expand
- Expandable sub-sections per pick: 详细分析 / 证据链 / 红旗扫描
- Color-coded by verdict + evidence type + red flag severity
"""

from __future__ import annotations

import html
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent


CSS = """
<style>
  * { box-sizing: border-box; }
  body {
    font-family: -apple-system, BlinkMacSystemFont, "PingFang SC",
                 "Microsoft YaHei", "Segoe UI", Helvetica, Arial, sans-serif;
    max-width: 1100px;
    margin: 2em auto;
    padding: 0 1.2em;
    line-height: 1.6;
    color: #1a1a1a;
    background: #fafafa;
  }
  h1 {
    color: #0066cc;
    border-bottom: 3px solid #0066cc;
    padding-bottom: 0.3em;
    margin-bottom: 0.2em;
  }
  h2 {
    margin-top: 2.5em;
    padding: 0.3em 0.5em;
    border-radius: 4px;
    color: #fff;
  }
  h2.ai     { background: linear-gradient(90deg, #5e35b1 0%, #3949ab 100%); }
  h2.market { background: linear-gradient(90deg, #2e7d32 0%, #388e3c 100%); }
  h2.avoid  { background: linear-gradient(90deg, #c62828 0%, #d32f2f 100%); }
  h2.misc   { background: linear-gradient(90deg, #455a64 0%, #546e7a 100%); }

  .meta {
    color: #666;
    font-size: 0.88em;
    margin: 0.6em 0 1em;
  }
  .market-context {
    background: #fff;
    border-left: 4px solid #5e35b1;
    padding: 1em 1.2em;
    margin: 1.5em 0;
    border-radius: 0 6px 6px 0;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
  }
  .market-context strong { color: #5e35b1; }

  .pick {
    background: #fff;
    border: 1px solid #e0e0e0;
    border-radius: 8px;
    padding: 1em 1.2em;
    margin: 1em 0;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    transition: box-shadow 0.2s;
  }
  .pick:hover { box-shadow: 0 2px 8px rgba(0,0,0,0.08); }
  .pick.ai     { border-left: 5px solid #5e35b1; }
  .pick.market { border-left: 5px solid #2e7d32; }
  .pick.avoid  { border-left: 5px solid #c62828; }

  .pick-header {
    display: flex;
    flex-wrap: wrap;
    justify-content: space-between;
    align-items: baseline;
    gap: 0.5em;
  }
  .pick-title {
    font-size: 1.25em;
    font-weight: 600;
  }
  .pick-rank {
    background: #f5f5f5;
    color: #666;
    padding: 0.1em 0.5em;
    border-radius: 12px;
    font-size: 0.8em;
    margin-right: 0.5em;
  }
  .pick-ticker { color: #0066cc; }
  .pick-name { color: #333; margin-left: 0.4em; }

  .pick-tags {
    margin: 0.4em 0;
    display: flex;
    flex-wrap: wrap;
    gap: 0.5em;
  }
  .tag {
    display: inline-block;
    padding: 0.15em 0.6em;
    border-radius: 4px;
    font-size: 0.82em;
    font-weight: 500;
  }
  .tag-strategy { background: #ede7f6; color: #5e35b1; }
  .tag-strategy.market { background: #e8f5e9; color: #2e7d32; }
  .tag-concern  { background: #ffebee; color: #c62828; }
  .tag-theme    { background: #f5f5f5; color: #555; }
  .tag-conf     { background: #fff; border: 1px solid #ddd; color: #666; font-family: ui-monospace, "SF Mono", Menlo, monospace; }

  .pick-thesis {
    margin: 0.6em 0;
    font-size: 1.02em;
    color: #333;
  }
  .pick-thesis em { color: #5e35b1; font-style: normal; font-weight: 500; }

  details {
    margin-top: 0.7em;
    border-top: 1px dashed #e0e0e0;
    padding-top: 0.4em;
  }
  details summary {
    cursor: pointer;
    color: #0066cc;
    padding: 0.4em 0;
    font-weight: 500;
    list-style: none;
    user-select: none;
  }
  details summary::before {
    content: "▶";
    display: inline-block;
    margin-right: 0.4em;
    transition: transform 0.15s;
    font-size: 0.7em;
    color: #999;
  }
  details[open] summary::before { transform: rotate(90deg); }
  details summary:hover { color: #ff6600; }
  details > div, details > table { margin: 0.5em 0; }

  .field { margin: 0.4em 0; }
  .field-label {
    color: #666;
    font-size: 0.9em;
    margin-right: 0.4em;
    font-weight: 500;
  }
  .field-value { color: #333; }
  .field-value.num { font-family: ui-monospace, "SF Mono", Menlo, monospace; color: #0066cc; }

  table.evidence {
    width: 100%;
    border-collapse: collapse;
    font-size: 0.88em;
    margin-top: 0.5em;
  }
  table.evidence th, table.evidence td {
    border: 1px solid #e0e0e0;
    padding: 0.4em 0.6em;
    text-align: left;
    vertical-align: top;
  }
  table.evidence th {
    background: #f8f8f8;
    color: #555;
    font-weight: 500;
    font-size: 0.85em;
  }
  td.ev-type {
    width: 70px;
    text-align: center;
    font-weight: 500;
    font-size: 0.85em;
  }
  td.ev-type.hard { background: #e8f5e9; color: #2e7d32; }
  td.ev-type.soft { background: #fff3e0; color: #e65100; }
  td.ev-type.pending_verify { background: #f5f5f5; color: #666; }
  td.ev-source {
    font-family: ui-monospace, "SF Mono", Menlo, monospace;
    font-size: 0.82em;
    color: #555;
    word-break: break-all;
    max-width: 280px;
  }
  td.ev-used { width: 120px; font-size: 0.82em; color: #666; }

  .red-flag {
    background: #fafafa;
    padding: 0.5em 0.8em;
    border-left: 3px solid #999;
    margin: 0.4em 0;
    font-size: 0.92em;
    border-radius: 0 4px 4px 0;
  }
  .red-flag.HIGH   { border-color: #c62828; background: #ffebee; }
  .red-flag.MEDIUM { border-color: #ef6c00; background: #fff3e0; }
  .red-flag.LOW    { border-color: #fbc02d; background: #fffde7; }
  .red-flag .severity {
    display: inline-block;
    padding: 0.05em 0.4em;
    border-radius: 3px;
    font-size: 0.78em;
    font-weight: 600;
    margin-right: 0.4em;
  }
  .red-flag.HIGH .severity   { background: #c62828; color: #fff; }
  .red-flag.MEDIUM .severity { background: #ef6c00; color: #fff; }
  .red-flag.LOW .severity    { background: #fbc02d; color: #333; }
  .red-flag .cat { font-weight: 500; color: #333; }
  .red-flag .ev  { color: #555; margin-top: 0.3em; font-size: 0.9em; }
  .red-flag .src { color: #999; font-size: 0.82em; font-family: ui-monospace, monospace; }

  .summary-stats {
    display: flex;
    flex-wrap: wrap;
    gap: 0.6em;
    margin: 0.3em 0;
  }
  .stat {
    background: #f8f8f8;
    padding: 0.2em 0.6em;
    border-radius: 3px;
    font-size: 0.82em;
    color: #666;
  }
  .stat.hard { background: #e8f5e9; color: #2e7d32; }
  .stat.soft { background: #fff3e0; color: #e65100; }
  .stat.pending { background: #f5f5f5; color: #666; }
  .stat.flag-high   { background: #ffebee; color: #c62828; }
  .stat.flag-medium { background: #fff3e0; color: #ef6c00; }
  .stat.flag-low    { background: #fffde7; color: #f9a825; }

  .footer {
    margin-top: 4em;
    padding-top: 1.5em;
    border-top: 1px solid #ddd;
    color: #888;
    font-size: 0.85em;
  }
  .badge {
    background: #1a1a1a;
    color: #fff;
    padding: 0.2em 0.5em;
    border-radius: 3px;
    font-size: 0.75em;
    font-family: ui-monospace, monospace;
  }
  .empty {
    color: #999;
    font-style: italic;
    padding: 1em;
    text-align: center;
    background: #f8f8f8;
    border-radius: 4px;
  }

  @media (max-width: 700px) {
    body { padding: 0 0.6em; }
    .pick-header { flex-direction: column; align-items: flex-start; }
  }
</style>
"""


def h(s) -> str:
    """Safe HTML escape (handles None)."""
    if s is None:
        return ""
    return html.escape(str(s))


def render_evidence_log(entries: list) -> str:
    if not entries:
        return '<div class="empty">无 evidence_log entries</div>'
    n_hard = sum(1 for e in entries if isinstance(e, dict) and e.get("type") == "hard")
    n_soft = sum(1 for e in entries if isinstance(e, dict) and e.get("type") == "soft")
    n_pending = sum(1 for e in entries if isinstance(e, dict) and e.get("type") == "pending_verify")
    rows_html = []
    for e in entries:
        if not isinstance(e, dict):
            continue
        etype = e.get("type", "")
        rows_html.append(
            f'<tr>'
            f'<td class="ev-type {h(etype)}">{h(etype.upper() if etype else "?")}</td>'
            f'<td class="ev-source">{h(e.get("source", ""))}</td>'
            f'<td>{h(e.get("content", ""))}</td>'
            f'<td class="ev-used">{h(", ".join(e.get("used_in", []) or []))}</td>'
            f'</tr>'
        )
    summary = (
        f'<div class="summary-stats">'
        f'<span class="stat hard">{n_hard} HARD</span>'
        f'<span class="stat soft">{n_soft} SOFT</span>'
        f'<span class="stat pending">{n_pending} PENDING</span>'
        f'</div>'
    )
    table = (
        '<table class="evidence">'
        '<thead><tr><th>类型</th><th>来源</th><th>内容</th><th>用在</th></tr></thead>'
        f'<tbody>{"".join(rows_html)}</tbody></table>'
    )
    return summary + table


def render_red_flags(triggered: list) -> str:
    if not triggered:
        return '<div class="empty">无 red flag 触发 ✓ (此 BUY 候选通过 18 类全扫描)</div>'
    n_high = sum(1 for t in triggered if isinstance(t, dict) and (t.get("severity", "").upper() == "HIGH"))
    n_med = sum(1 for t in triggered if isinstance(t, dict) and (t.get("severity", "").upper() == "MEDIUM"))
    n_low = sum(1 for t in triggered if isinstance(t, dict) and (t.get("severity", "").upper() == "LOW"))
    items_html = []
    for t in triggered:
        if not isinstance(t, dict):
            continue
        sev = (t.get("severity") or "").upper()
        items_html.append(
            f'<div class="red-flag {h(sev)}">'
            f'<span class="severity">{h(sev or "?")}</span>'
            f'<span class="cat">{h(t.get("category", ""))}</span>'
            f'<div class="ev">{h(t.get("evidence", ""))}</div>'
            f'<div class="src">检测方式: {h(t.get("detection_method", ""))}</div>'
            f'</div>'
        )
    summary = (
        f'<div class="summary-stats">'
        f'<span class="stat flag-high">{n_high} HIGH</span>'
        f'<span class="stat flag-medium">{n_med} MEDIUM</span>'
        f'<span class="stat flag-low">{n_low} LOW</span>'
        f'</div>'
    )
    return summary + "".join(items_html)


def render_buy_pick(pick: dict, kind: str) -> str:
    """kind: 'ai' or 'market'"""
    css_class = "ai" if kind == "ai" else "market"
    strategy_tag_class = "tag-strategy" if kind == "ai" else "tag-strategy market"

    rank = pick.get("rank", "?")
    ticker = h(pick.get("ticker", ""))
    name = h(pick.get("name", ""))
    theme = h(pick.get("theme", ""))
    strategy = h(pick.get("strategy", ""))
    pattern = h(pick.get("pattern_matched", ""))
    thesis = h(pick.get("thesis", ""))
    why_now = h(pick.get("why_now", ""))
    entry_close = pick.get("entry_close", "")
    key_track = h(pick.get("key_tracking_indicator", ""))
    main_risk = h(pick.get("main_risk", ""))
    confidence = pick.get("confidence", "")
    rubric = pick.get("rubric_score")

    rubric_field = (
        f'<div class="field"><span class="field-label">Rubric:</span>'
        f'<span class="field-value num">{rubric}/80</span></div>'
        if rubric is not None else ""
    )

    return f'''
<div class="pick {css_class}">
  <div class="pick-header">
    <div class="pick-title">
      <span class="pick-rank">#{rank}</span>
      <span class="pick-ticker">{ticker}</span>
      <span class="pick-name">{name}</span>
    </div>
    <div>
      <span class="tag tag-conf">conf {confidence}</span>
    </div>
  </div>

  <div class="pick-tags">
    <span class="tag {strategy_tag_class}">{strategy}</span>
    {f'<span class="tag tag-theme">theme: {theme}</span>' if theme else ""}
    {f'<span class="tag tag-theme">{pattern}</span>' if pattern else ""}
  </div>

  <div class="pick-thesis"><em>Thesis:</em> {thesis}</div>

  <details>
    <summary>📋 详细分析</summary>
    <div>
      <div class="field"><span class="field-label">Why now:</span><span class="field-value">{why_now}</span></div>
      <div class="field"><span class="field-label">关键跟踪指标:</span><span class="field-value">{key_track}</span></div>
      <div class="field"><span class="field-label">主要风险:</span><span class="field-value">{main_risk}</span></div>
      <div class="field"><span class="field-label">入场价:</span><span class="field-value num">{entry_close}</span></div>
      {rubric_field}
    </div>
  </details>

  <details>
    <summary>🔍 证据链 (evidence_log)</summary>
    <div>{render_evidence_log(pick.get("evidence_log") or [])}</div>
  </details>

  <details>
    <summary>🚩 Red flag 扫描结果</summary>
    <div>{render_red_flags(pick.get("red_flags_triggered") or [])}</div>
  </details>
</div>
'''


def render_avoid_pick(pick: dict) -> str:
    rank = pick.get("rank", "?")
    ticker = h(pick.get("ticker", ""))
    name = h(pick.get("name", ""))
    theme = h(pick.get("theme", ""))
    primary = h(pick.get("primary_concern", ""))
    concern_summary = h(pick.get("concern_summary", ""))
    evidence_str = h(pick.get("evidence", ""))
    retail = h(pick.get("why_retail_temptation", ""))
    reverse_signal = h(pick.get("what_would_reverse", ""))
    entry_close = pick.get("entry_close", "")
    confidence = pick.get("confidence", "")

    return f'''
<div class="pick avoid">
  <div class="pick-header">
    <div class="pick-title">
      <span class="pick-rank">#{rank}</span>
      <span class="pick-ticker">{ticker}</span>
      <span class="pick-name">{name}</span>
    </div>
    <div>
      <span class="tag tag-conf">conf {confidence}</span>
    </div>
  </div>

  <div class="pick-tags">
    <span class="tag tag-concern">{primary}</span>
    {f'<span class="tag tag-theme">theme: {theme}</span>' if theme else ""}
  </div>

  <div class="pick-thesis"><em>Concern:</em> {concern_summary}</div>

  <details>
    <summary>📋 详细分析</summary>
    <div>
      <div class="field"><span class="field-label">主要证据:</span><span class="field-value">{evidence_str}</span></div>
      <div class="field"><span class="field-label">散户为何容易追:</span><span class="field-value">{retail}</span></div>
      <div class="field"><span class="field-label">什么信号说明 AVOID 错了:</span><span class="field-value">{reverse_signal}</span></div>
      <div class="field"><span class="field-label">入场参考价:</span><span class="field-value num">{entry_close}</span></div>
    </div>
  </details>

  <details>
    <summary>🔍 证据链 (evidence_log)</summary>
    <div>{render_evidence_log(pick.get("evidence_log") or [])}</div>
  </details>

  <details open>
    <summary>🚩 触发的 red flag</summary>
    <div>{render_red_flags(pick.get("red_flags_triggered") or [])}</div>
  </details>
</div>
'''


def render_section(title: str, kind: str, picks: list, emoji: str, render_fn) -> str:
    """kind: ai | market | avoid"""
    n = len(picks) if picks else 0
    if not picks:
        body = '<div class="empty">本期无符合条件的 picks (诚实输出)</div>'
    else:
        body = "".join(render_fn(p) for p in picks)
    return f'<h2 class="{kind}">{emoji} {title} ({n} 支)</h2>\n{body}'


def render_market_context(ctx: dict) -> str:
    one_line = h(ctx.get("one_line", ""))
    active_themes = ctx.get("active_themes") or []
    events = ctx.get("recent_significant_events") or []
    us_leaders = ctx.get("us_leaders_observed") or []

    extras = []
    if active_themes:
        extras.append(f'<div class="field"><span class="field-label">活跃主题:</span><span class="field-value">{h(", ".join(str(t) for t in active_themes))}</span></div>')
    if events:
        events_html = "".join(f'<li>{h(e)}</li>' for e in events)
        extras.append(f'<div class="field"><span class="field-label">关键事件:</span><ul style="margin:0.2em 0 0 1.5em">{events_html}</ul></div>')
    if us_leaders:
        extras.append(
            f'<div class="field"><span class="field-label">美股龙头对照:</span><span class="field-value">观察 {len(us_leaders)} 个</span></div>'
        )

    return f'''
<div class="market-context">
  <strong>📈 市场背景</strong>
  <div style="margin-top:0.5em">{one_line}</div>
  {"".join(extras)}
</div>
'''


def render_selection_process(card: dict, lock: dict) -> str:
    sel = card.get("selection_process") or {}
    sources = sel.get("candidate_pool_sources") or []
    rationale = h(sel.get("short_list_rationale", ""))
    order = h(sel.get("selection_order", ""))

    src_items = []
    for s in sources:
        if isinstance(s, dict):
            for k, v in s.items():
                src_items.append(f'<li>{h(k)}: {h(v)}</li>')

    body = f'''
<div class="field"><span class="field-label">候选池规模:</span><span class="field-value num">{lock.get("candidate_pool_size", "?")}</span></div>
<div class="field"><span class="field-label">短列表规模:</span><span class="field-value num">{lock.get("short_list_size", "?")}</span></div>
{f'<div class="field"><span class="field-label">选择顺序:</span><span class="field-value">{order}</span></div>' if order else ""}
{f'<div class="field"><span class="field-label">候选池来源:</span><ul style="margin:0.2em 0 0 1.5em">{"".join(src_items)}</ul></div>' if src_items else ""}
{f'<div class="field"><span class="field-label">短列表逻辑:</span><span class="field-value">{rationale}</span></div>' if rationale else ""}
'''
    return body


def render_lock_meta(lock: dict) -> str:
    pid = h(lock.get("picks_id", ""))
    at = h(lock.get("analyzed_at", ""))
    pb = h(lock.get("playbook", ""))
    pb_ver = lock.get("playbook_version", "")
    pb_short = pb_ver[:8] if isinstance(pb_ver, str) and len(pb_ver) >= 8 else h(pb_ver)
    bm = h(lock.get("benchmark", ""))
    bm_close = lock.get("benchmark_entry_close", "")
    edate = h(lock.get("entry_close_date", ""))
    horizon = lock.get("prediction_horizon_days", "")
    hash_short = (lock.get("claude_output_hash") or "")[:16]

    return f'''
<div class="meta">
  <span class="badge">{pid}</span> &nbsp;
  analyzed_at: <b>{at}</b> &nbsp; | &nbsp;
  benchmark: <b>{bm} @ {bm_close}</b> &nbsp; | &nbsp;
  entry_date: <b>{edate}</b> &nbsp; | &nbsp;
  horizon: <b>T+{horizon}</b> &nbsp; | &nbsp;
  playbook: <b>{pb}@{pb_short}</b> &nbsp; | &nbsp;
  hash: <code>{hash_short}...</code>
</div>
'''


def render_open_checks(card: dict) -> str:
    checks = card.get("open_checks") or []
    if not checks:
        return ""
    items = "".join(f"<li>{h(c)}</li>" for c in checks)
    return f'''
<details>
  <summary>📌 Open Checks (未核实事项)</summary>
  <div><ul style="margin:0.5em 0 0 1.5em">{items}</ul></div>
</details>
'''


def render_html(card: dict) -> str:
    lock = card.get("lock") or {}
    market_ctx = card.get("market_context") or {}
    ai_picks = card.get("ai_picks") or []
    market_picks = card.get("market_picks") or []
    avoid_picks = card.get("avoid_picks") or []
    # legacy backward compat (v0.6 / v0.7 buy_picks)
    legacy_buy = card.get("buy_picks") or []

    pid = h(lock.get("picks_id", "unknown"))
    edate = h(lock.get("entry_close_date", ""))

    legacy_section = ""
    if legacy_buy and not (ai_picks or market_picks):
        # File uses old buy_picks schema; render under legacy section
        legacy_section = render_section(
            "BUY (legacy v0.6/v0.7 schema)", "misc", legacy_buy, "📦",
            lambda p: render_buy_pick(p, "market")
        )

    sections_html = ""
    if ai_picks or market_picks:
        sections_html += render_section(
            "AI 相关推荐", "ai", ai_picks, "🚀",
            lambda p: render_buy_pick(p, "ai")
        )
        sections_html += render_section(
            "全市场推荐 (非 AI)", "market", market_picks, "💎",
            lambda p: render_buy_pick(p, "market")
        )

    sections_html += render_section(
        "过热不推荐 (AVOID)", "avoid", avoid_picks, "⚠️",
        render_avoid_pick
    )

    if legacy_section:
        sections_html += legacy_section

    body = f'''
<h1>📊 Weekly Picks — {edate}</h1>
{render_lock_meta(lock)}
{render_market_context(market_ctx)}
{sections_html}

<h2 class="misc">🔬 流水线透明度</h2>
<details>
  <summary>候选池 → 短列表 → 3 list 选择</summary>
  <div>{render_selection_process(card, lock)}</div>
</details>
{render_open_checks(card)}

<div class="footer">
  <p><strong>Trade Disclosure</strong>: thesis_only — 个人研究工具，不持仓不下单。
  本报告所有结论为研究信号，不构成投资建议。</p>
  <p><strong>Evidence discipline</strong>: 每个 claim 在 evidence_log 中标记
  <span style="background:#e8f5e9;color:#2e7d32;padding:1px 6px;border-radius:3px">HARD</span> /
  <span style="background:#fff3e0;color:#e65100;padding:1px 6px;border-radius:3px">SOFT</span> /
  <span style="background:#f5f5f5;color:#666;padding:1px 6px;border-radius:3px">PENDING_VERIFY</span>。
  AVOID 类红旗触发都有具体证据 + URL + 日期。</p>
  <p>Generated by <code>tools/render_picks_html.py</code> from
  <code>{pid}</code>. 项目仓库:
  <a href="https://github.com/yunxichu/LLMstocks">github.com/yunxichu/LLMstocks</a></p>
</div>
'''

    return f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Weekly Picks {pid}</title>
{CSS}
</head>
<body>
{body}
</body>
</html>
'''


def main(yaml_path_str: str) -> int:
    yaml_path = Path(yaml_path_str).resolve()
    if not yaml_path.exists():
        print(f"File not found: {yaml_path}", file=sys.stderr)
        return 1

    with yaml_path.open(encoding="utf-8") as f:
        card = yaml.safe_load(f)

    html_text = render_html(card)
    out_path = yaml_path.with_suffix(".html")
    with out_path.open("w", encoding="utf-8") as f:
        f.write(html_text)

    print(f"Wrote: {out_path}")
    print(f"  ai_picks: {len(card.get('ai_picks') or [])}")
    print(f"  market_picks: {len(card.get('market_picks') or [])}")
    print(f"  avoid_picks: {len(card.get('avoid_picks') or [])}")
    if card.get("buy_picks"):
        print(f"  buy_picks (legacy): {len(card['buy_picks'])}")
    return 0


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python tools/render_picks_html.py <yaml_path>", file=sys.stderr)
        sys.exit(1)
    sys.exit(main(sys.argv[1]))
