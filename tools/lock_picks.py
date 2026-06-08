"""Lock a weekly picks card (v0.8: 3 lists × 5 each = 15 picks).

Usage:
    python tools/lock_picks.py predictions/picks/<YYYY-MM-DD>/picks_<HHMMSS>.yaml

What it does:
1. Validates the top-level LOCK area + every entry in:
   - ai_picks       (5 max, BUY semantics, theme ∈ AI_THEMES)
   - market_picks   (5 max, BUY semantics, theme ∉ AI_THEMES)
   - avoid_picks    (5 max, AVOID semantics)
2. Enforces:
   - red_flag scan completeness (all 18 categories) per entry
   - BUY 类: 0 HIGH + ≤1 MEDIUM
   - AVOID 类: ≥1 HIGH or ≥2 MEDIUM with evidence
   - evidence_log: ≥3 type='hard' entries per pick
   - target_price_review for AI / market picks
   - valuation_red_flag for AVOID picks
   - ai_picks ∩ market_picks ticker set = ∅
3. Computes SHA-256 of accompanying raw.md
4. Records playbook_version (git sha of weekly_picks.md)
5. Appends one row per ticker (15 total) to predictions/picks_index.csv
"""

from __future__ import annotations

import hashlib
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

import yaml
from rich.console import Console

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from data.web import calendar as cal_data  # noqa: E402

console = Console()

REQUIRED_TOP_LOCK_FIELDS = [
    "picks_id",
    "analyzed_at",
    "playbook",
    "prediction_horizon_days",
    "benchmark",
    "benchmark_entry_close",
    "entry_close_date",
    "candidate_pool_size",
    "short_list_size",
    "red_flag_categories_scanned",
    "ai_themes_used",
    "success_criteria",
    "failure_criteria",
    "invalidation_conditions",
]

REQUIRED_BUY_FIELDS = [
    "rank", "ticker", "name", "theme", "strategy", "thesis", "why_now",
    "entry_close", "confidence",
    "key_tracking_indicator", "main_risk",
    "red_flags_checked", "red_flags_triggered",
    "evidence_log",
    "target_price_review",
]

REQUIRED_AVOID_FIELDS = [
    "rank", "ticker", "name", "primary_concern", "concern_summary",
    "evidence", "why_retail_temptation", "what_would_reverse",
    "entry_close", "confidence",
    "red_flags_checked", "red_flags_triggered",
    "evidence_log",
    "valuation_red_flag",
]

PICKS_ID_PATTERN = re.compile(r"^picks-\d{8}-\d{6}$")
ALL_RED_FLAG_CATEGORIES = list(range(1, 19))  # 1..18

# v0.8: AI themes for ai_picks vs market_picks validation
AI_THEMES = {"ai-compute", "optical-cpo", "semi-equipment", "robotics", "domestic-software"}

EVIDENCE_VALID_TYPES = {"hard", "soft", "pending_verify"}
MIN_HARD_EVIDENCE_PER_PICK = 3
MAX_PICKS_PER_LIST = 5
TARGET_PRICE_STATUSES = {"research_grade", "provisional", "unavailable"}
RESEARCH_MATRIX_STATUSES = {"complete", "partial", "unavailable"}


def git_sha_for(path: Path) -> str:
    try:
        if path.exists():
            r = subprocess.run(
                ["git", "log", "-n", "1", "--format=%H", "--", str(path)],
                capture_output=True, text=True, cwd=ROOT, timeout=10,
            )
            if r.stdout.strip():
                return r.stdout.strip()
        r = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            capture_output=True, text=True, cwd=ROOT, timeout=10,
        )
        return r.stdout.strip() or "no-git"
    except Exception:
        return "no-git"


def compute_raw_hash(raw_path: Path) -> str:
    h = hashlib.sha256()
    with raw_path.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def validate_top_lock(lock: dict) -> list[str]:
    errors: list[str] = []
    for k in REQUIRED_TOP_LOCK_FIELDS:
        v = lock.get(k)
        if v is None or v == "" or (isinstance(v, (list, tuple)) and not v):
            errors.append(f"lock.{k} missing or empty")

    pid = lock.get("picks_id", "")
    if pid and not PICKS_ID_PATTERN.match(pid):
        errors.append(
            f"picks_id format invalid: '{pid}' (expected 'picks-yyyymmdd-HHMMSS')"
        )

    scanned = lock.get("red_flag_categories_scanned", [])
    if sorted(scanned) != ALL_RED_FLAG_CATEGORIES:
        errors.append(
            f"red_flag_categories_scanned must be [1..18]; got {scanned}"
        )

    # v0.8: ai_themes_used must match AI_THEMES exactly
    declared_ai = set(lock.get("ai_themes_used") or [])
    if declared_ai != AI_THEMES:
        errors.append(
            f"lock.ai_themes_used must equal AI_THEMES = {sorted(AI_THEMES)}; "
            f"got {sorted(declared_ai)}"
        )

    if len(lock.get("invalidation_conditions") or []) < 3:
        errors.append("invalidation_conditions must have >= 3 entries")

    try:
        if float(lock.get("benchmark_entry_close", 0)) <= 0:
            errors.append("benchmark_entry_close must be > 0")
    except Exception:
        errors.append("benchmark_entry_close must be numeric")

    return errors


def validate_evidence_log(evidence_log, label: str) -> list[str]:
    """v0.7 evidence_log validation."""
    errors = []
    if evidence_log is None or not isinstance(evidence_log, list) or not evidence_log:
        return [
            f"{label}.evidence_log missing or empty "
            f"(v0.7 requires evidence_log with ≥{MIN_HARD_EVIDENCE_PER_PICK} hard entries)"
        ]
    n_hard = 0
    for ei, e in enumerate(evidence_log):
        if not isinstance(e, dict):
            errors.append(f"{label}.evidence_log[{ei}] must be a dict")
            continue
        etype = (e.get("type") or "").lower()
        if etype not in EVIDENCE_VALID_TYPES:
            errors.append(
                f"{label}.evidence_log[{ei}].type must be one of "
                f"{sorted(EVIDENCE_VALID_TYPES)}; got '{etype}'"
            )
            continue
        if not (e.get("source") or "").strip():
            errors.append(f"{label}.evidence_log[{ei}].source missing")
        content = e.get("content")
        if content is None or (isinstance(content, str) and not content.strip()):
            errors.append(f"{label}.evidence_log[{ei}].content missing")
        if etype == "hard":
            n_hard += 1
    if n_hard < MIN_HARD_EVIDENCE_PER_PICK:
        errors.append(
            f"{label}.evidence_log has only {n_hard} hard entries; "
            f"v0.7 requires ≥{MIN_HARD_EVIDENCE_PER_PICK} type='hard' "
            f"(yfinance fields / WebFetch URLs / public docs)"
        )
    return errors


def _positive_number(value) -> bool:
    try:
        return float(value) > 0
    except Exception:
        return False


def validate_target_price_review(review, label: str) -> list[str]:
    """v1.0 target-price validation for AI / market BUY entries."""
    errors: list[str] = []
    if not isinstance(review, dict) or not review:
        return [f"{label}.target_price_review missing or not a dict"]

    status = review.get("status")
    if status not in TARGET_PRICE_STATUSES:
        errors.append(
            f"{label}.target_price_review.status must be one of "
            f"{sorted(TARGET_PRICE_STATUSES)}; got {status!r}"
        )
    if status == "unavailable":
        errors.append(
            f"{label}.target_price_review.status cannot be unavailable for "
            f"AI / market picks; use provisional if research reports are incomplete"
        )

    for k in ["current_price", "base_target"]:
        if not _positive_number(review.get(k)):
            errors.append(f"{label}.target_price_review.{k} must be > 0")

    target_range = review.get("target_range")
    if (
        not isinstance(target_range, list)
        or len(target_range) != 2
        or not all(_positive_number(x) for x in target_range)
    ):
        errors.append(
            f"{label}.target_price_review.target_range must be two positive numbers"
        )

    method = review.get("selected_method")
    if not isinstance(method, dict) or not (method.get("primary") or "").strip():
        errors.append(
            f"{label}.target_price_review.selected_method.primary missing"
        )

    eps_bridge = review.get("eps_forecast_bridge")
    if not isinstance(eps_bridge, dict) or not eps_bridge:
        errors.append(f"{label}.target_price_review.eps_forecast_bridge missing")
    else:
        if not isinstance(eps_bridge.get("latest_actual"), dict):
            errors.append(
                f"{label}.target_price_review.eps_forecast_bridge.latest_actual missing"
            )
        if not (
            isinstance(eps_bridge.get("fy2026_forecast"), dict)
            or isinstance(eps_bridge.get("fy2027_forecast"), dict)
        ):
            errors.append(
                f"{label}.target_price_review.eps_forecast_bridge needs "
                f"fy2026_forecast or fy2027_forecast"
            )

    matrix = review.get("research_report_matrix")
    report_count = 0
    if not isinstance(matrix, dict) or not matrix:
        errors.append(f"{label}.target_price_review.research_report_matrix missing")
    else:
        mstatus = matrix.get("status")
        if mstatus not in RESEARCH_MATRIX_STATUSES:
            errors.append(
                f"{label}.target_price_review.research_report_matrix.status must be "
                f"one of {sorted(RESEARCH_MATRIX_STATUSES)}; got {mstatus!r}"
            )
        reports = matrix.get("reports") or []
        if isinstance(reports, list):
            report_count = len(reports)
        else:
            errors.append(
                f"{label}.target_price_review.research_report_matrix.reports "
                f"must be a list"
            )
        if status == "research_grade":
            if mstatus != "complete":
                errors.append(
                    f"{label}.target_price_review is research_grade but "
                    f"research_report_matrix.status is {mstatus!r}"
                )
            if report_count < 3:
                errors.append(
                    f"{label}.target_price_review is research_grade but has "
                    f"only {report_count} report(s); requires >= 3"
                )

    triggers = review.get("revision_triggers")
    if not isinstance(triggers, dict):
        errors.append(f"{label}.target_price_review.revision_triggers missing")
    else:
        if not isinstance(triggers.get("upward"), list):
            errors.append(
                f"{label}.target_price_review.revision_triggers.upward must be a list"
            )
        if not isinstance(triggers.get("downward"), list):
            errors.append(
                f"{label}.target_price_review.revision_triggers.downward must be a list"
            )

    if not isinstance(review.get("evidence_grade"), dict) or not review.get("evidence_grade"):
        errors.append(f"{label}.target_price_review.evidence_grade missing")

    return errors


def validate_valuation_red_flag(red_flag, label: str) -> list[str]:
    """v1.0 fair-value / overvaluation validation for AVOID entries."""
    errors: list[str] = []
    if not isinstance(red_flag, dict) or not red_flag:
        return [f"{label}.valuation_red_flag missing or not a dict"]

    fair_range = red_flag.get("fair_value_or_risk_range")
    if (
        not isinstance(fair_range, list)
        or len(fair_range) != 2
        or not all(_positive_number(x) for x in fair_range)
    ):
        errors.append(
            f"{label}.valuation_red_flag.fair_value_or_risk_range must be "
            f"two positive numbers"
        )
    if not _positive_number(red_flag.get("current_price")):
        errors.append(f"{label}.valuation_red_flag.current_price must be > 0")
    if not (red_flag.get("overvaluation_reason") or "").strip():
        errors.append(f"{label}.valuation_red_flag.overvaluation_reason missing")
    if not (red_flag.get("method") or "").strip():
        errors.append(f"{label}.valuation_red_flag.method missing")
    if not isinstance(red_flag.get("reversal_conditions"), list) or not red_flag.get("reversal_conditions"):
        errors.append(
            f"{label}.valuation_red_flag.reversal_conditions must have >= 1 entry"
        )
    if not isinstance(red_flag.get("evidence_grade"), dict) or not red_flag.get("evidence_grade"):
        errors.append(f"{label}.valuation_red_flag.evidence_grade missing")

    return errors


def validate_pick_entry(entry: dict, verdict: str, idx: int) -> list[str]:
    """Validate one pick entry. verdict ∈ {'ai', 'market', 'avoid'}."""
    errors: list[str] = []
    is_buy = verdict in ("ai", "market")
    required = REQUIRED_BUY_FIELDS if is_buy else REQUIRED_AVOID_FIELDS
    label = f"{verdict}_picks[{idx}]"

    for k in required:
        v = entry.get(k)
        if v is None or v == "":
            # special: red_flags_triggered can be empty list for BUY
            if k == "red_flags_triggered" and isinstance(v, list):
                continue
            # evidence_log validated separately
            if k == "evidence_log":
                continue
            errors.append(f"{label}.{k} missing or empty")

    scanned = entry.get("red_flags_checked", []) or []
    if sorted(scanned) != ALL_RED_FLAG_CATEGORIES:
        errors.append(f"{label}.red_flags_checked must be [1..18]; got {scanned}")

    triggered = entry.get("red_flags_triggered", []) or []

    if is_buy:
        n_high = 0
        n_medium = 0
        for ti, t in enumerate(triggered):
            if not isinstance(t, dict):
                errors.append(f"{label}.red_flags_triggered[{ti}] must be a dict")
                continue
            sev = (t.get("severity") or "").upper()
            if sev == "HIGH":
                n_high += 1
            elif sev == "MEDIUM":
                n_medium += 1
            if not (t.get("evidence") or "").strip():
                errors.append(f"{label}.red_flags_triggered[{ti}] missing evidence")
        if n_high > 0:
            errors.append(
                f"{label} BUY has {n_high} HIGH red flag(s); BUY allows 0 HIGH"
            )
        if n_medium > 1:
            errors.append(
                f"{label} BUY has {n_medium} MEDIUM red flag(s); "
                f"BUY allows ≤1 MEDIUM"
            )
    else:
        # AVOID
        n_high = sum(
            1 for t in triggered
            if isinstance(t, dict) and (t.get("severity") or "").upper() == "HIGH"
        )
        n_medium = sum(
            1 for t in triggered
            if isinstance(t, dict) and (t.get("severity") or "").upper() == "MEDIUM"
        )
        if n_high < 1 and n_medium < 2:
            errors.append(
                f"{label} AVOID must have ≥1 HIGH or ≥2 MEDIUM red_flags_triggered; "
                f"got HIGH={n_high}, MEDIUM={n_medium}"
            )
        for ti, t in enumerate(triggered):
            if isinstance(t, dict) and not (t.get("evidence") or "").strip():
                errors.append(
                    f"{label}.red_flags_triggered[{ti}] missing evidence string"
                )

    try:
        if float(entry.get("entry_close", 0)) <= 0:
            errors.append(f"{label}.entry_close must be > 0")
    except Exception:
        errors.append(f"{label}.entry_close must be numeric")

    # v0.7: evidence_log
    errors.extend(validate_evidence_log(entry.get("evidence_log"), label))

    # v1.0: valuation discipline
    if is_buy:
        errors.extend(
            validate_target_price_review(entry.get("target_price_review"), label)
        )
    else:
        errors.extend(
            validate_valuation_red_flag(entry.get("valuation_red_flag"), label)
        )

    # v0.8: theme validation for BUY entries
    if is_buy:
        theme = (entry.get("theme") or "").strip()
        if verdict == "ai":
            if theme not in AI_THEMES:
                errors.append(
                    f"{label}.theme '{theme}' MUST be in AI_THEMES "
                    f"({sorted(AI_THEMES)})"
                )
        elif verdict == "market":
            if theme in AI_THEMES:
                errors.append(
                    f"{label}.theme '{theme}' is in AI_THEMES; "
                    f"market_picks must use non-AI theme or empty (watchlist)"
                )

    return errors


def append_to_picks_index(card: dict, yaml_path: Path) -> None:
    """One row per ticker in the picks file."""
    index_path = ROOT / "predictions" / "picks_index.csv"
    index_path.parent.mkdir(parents=True, exist_ok=True)
    is_new = not index_path.exists()
    rel = yaml_path.relative_to(ROOT).as_posix()
    lock = card["lock"]

    rows = []
    for e in card.get("ai_picks") or []:
        rows.append(("AI_BUY", e, e.get("strategy", "")))
    for e in card.get("market_picks") or []:
        rows.append(("MARKET_BUY", e, e.get("strategy", "")))
    for e in card.get("avoid_picks") or []:
        rows.append(("AVOID", e, e.get("primary_concern", "")))

    with index_path.open("a", encoding="utf-8") as f:
        if is_new:
            f.write(
                "picks_id,analyzed_at,verdict,rank,ticker,name,theme,"
                "strategy_or_concern,entry_close,horizon_days,benchmark,"
                "benchmark_entry_close,entry_close_date,confidence,yaml_path\n"
            )
        for verdict, e, tag in rows:
            theme = e.get("theme", "") or ""
            f.write(
                f"{lock['picks_id']},{lock['analyzed_at']},{verdict},"
                f"{e.get('rank')},{e.get('ticker')},{e.get('name')},{theme},{tag},"
                f"{e.get('entry_close')},{lock['prediction_horizon_days']},"
                f"{lock['benchmark']},{lock['benchmark_entry_close']},"
                f"{lock['entry_close_date']},{e.get('confidence')},{rel}\n"
            )


def main(yaml_path_str: str) -> int:
    yaml_path = Path(yaml_path_str).resolve()
    if not yaml_path.exists():
        console.print(f"[red]File not found: {yaml_path}[/red]")
        return 1

    raw_path = yaml_path.with_name(yaml_path.stem + ".raw.md")
    if not raw_path.exists():
        console.print(f"[red]Raw markdown not found: {raw_path}[/red]")
        return 1

    with yaml_path.open(encoding="utf-8") as f:
        card = yaml.safe_load(f)

    if not isinstance(card, dict) or "lock" not in card:
        console.print("[red]Invalid picks card: missing top-level `lock`[/red]")
        return 1

    # Reject legacy buy_picks schema (v0.6/v0.7)
    if "buy_picks" in card:
        console.print(
            "[red]This file uses legacy `buy_picks` field (v0.6/v0.7). "
            "v0.8 requires ai_picks + market_picks. Update the YAML and retry.[/red]"
        )
        return 1

    errors = validate_top_lock(card["lock"])

    ai_picks = card.get("ai_picks") or []
    market_picks = card.get("market_picks") or []
    avoid_picks = card.get("avoid_picks") or []

    for name, lst in [("ai_picks", ai_picks), ("market_picks", market_picks),
                       ("avoid_picks", avoid_picks)]:
        if len(lst) > MAX_PICKS_PER_LIST:
            errors.append(f"{name} has {len(lst)} entries; max {MAX_PICKS_PER_LIST}")

    for i, e in enumerate(ai_picks):
        errors.extend(validate_pick_entry(e, "ai", i))
    for i, e in enumerate(market_picks):
        errors.extend(validate_pick_entry(e, "market", i))
    for i, e in enumerate(avoid_picks):
        errors.extend(validate_pick_entry(e, "avoid", i))

    # v0.8: ai_picks ∩ market_picks tickers must be empty
    ai_tickers = {e.get("ticker") for e in ai_picks if e.get("ticker")}
    market_tickers = {e.get("ticker") for e in market_picks if e.get("ticker")}
    overlap = ai_tickers & market_tickers
    if overlap:
        errors.append(
            f"ai_picks and market_picks tickers overlap: {sorted(overlap)} — "
            f"v0.8 requires disjoint lists"
        )

    try:
        entry_date = datetime.strptime(
            card["lock"]["entry_close_date"], "%Y-%m-%d"
        ).date()
        if not cal_data.is_trading_day(entry_date):
            console.print(
                f"[yellow]Warning: entry_close_date {entry_date} is not a "
                f"trading day[/yellow]"
            )
    except Exception as e:
        console.print(f"[yellow]Could not verify entry_close_date: {e}[/yellow]")

    if errors:
        console.print("[red]Picks validation failed:[/red]")
        for e in errors:
            console.print(f"  - {e}")
        return 1

    raw_hash = compute_raw_hash(raw_path)
    playbook_path = ROOT / "playbooks" / card["lock"]["playbook"]
    pb_sha = git_sha_for(playbook_path)

    card["lock"]["claude_output_hash"] = raw_hash
    card["lock"]["playbook_version"] = pb_sha

    with yaml_path.open("w", encoding="utf-8") as f:
        yaml.safe_dump(
            card, f, allow_unicode=True, sort_keys=False, default_flow_style=False
        )

    append_to_picks_index(card, yaml_path)

    pid = card["lock"]["picks_id"]
    console.print(f"[bold green]Locked picks: {pid}[/bold green]")
    console.print(f"  AI picks:     {len(ai_picks)} entries")
    console.print(f"  Market picks: {len(market_picks)} entries")
    console.print(f"  Avoid picks:  {len(avoid_picks)} entries")
    console.print(f"  playbook:     {card['lock']['playbook']}@{pb_sha[:8]}")
    console.print(f"  hash:         {raw_hash[:16]}...")
    console.print()
    console.print(
        f"[yellow]Next step:[/yellow] render HTML report:\n"
        f"  python tools/render_picks_html.py {yaml_path.relative_to(ROOT)}"
    )
    return 0


if __name__ == "__main__":
    if len(sys.argv) < 2:
        console.print("Usage: python tools/lock_picks.py <yaml_path>")
        sys.exit(1)
    sys.exit(main(sys.argv[1]))
