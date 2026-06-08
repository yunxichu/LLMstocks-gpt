"""Update tracking records for all open locked predictions (single + picks).

Usage:
    python tools/update_tracking.py

What it does:
1. Scans both:
   - predictions/locked/**/*.yaml  — single-ticker stock cards (v0.5)
   - predictions/picks/**/*.yaml   — weekly picks cards (v0.6+)
2. Expands each card into "tracking units" (one per ticker)
3. For each unit, determines today's d_index and writes any new checkpoint(s)
4. Per-unit tracking lives at predictions/tracking/<tracking_id>/d<N>.json
   where tracking_id = prediction_id (single) or <picks_id>--<ticker> (picks)
"""

from __future__ import annotations

import json
import sys
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from typing import Iterable

import yaml
from rich.console import Console

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from data.web import a_share as price_data  # noqa: E402
from data.web import benchmark as bm_data  # noqa: E402
from data.web import calendar as cal_data  # noqa: E402

console = Console()

STANDARD_CHECKPOINTS = [1, 5, 10, 15, 20, 30, 60]


@dataclass
class TrackingUnit:
    tracking_id: str
    ticker: str
    entry_close: float
    entry_close_date: date
    benchmark: str
    benchmark_entry_close: float
    horizon_days: int
    source_kind: str  # "single" or "picks_buy" or "picks_avoid"
    source_path: str  # for diagnostics


def _parse_date(s: str) -> date:
    return datetime.strptime(s, "%Y-%m-%d").date()


def units_from_single_yaml(yaml_path: Path) -> list[TrackingUnit]:
    """Single-ticker stock_card.yaml (v0.5 /analyze output)."""
    with yaml_path.open(encoding="utf-8") as f:
        card = yaml.safe_load(f)
    if not isinstance(card, dict) or "lock" not in card:
        return []
    lock = card["lock"]
    try:
        return [TrackingUnit(
            tracking_id=lock["prediction_id"],
            ticker=lock["ticker"],
            entry_close=float(lock["entry_close"]),
            entry_close_date=_parse_date(lock["entry_close_date"]),
            benchmark=lock["benchmark"],
            benchmark_entry_close=float(lock["benchmark_entry_close"]),
            horizon_days=int(lock["prediction_horizon_days"]),
            source_kind="single",
            source_path=yaml_path.relative_to(ROOT).as_posix(),
        )]
    except (KeyError, ValueError, TypeError) as e:
        console.print(f"[yellow]{yaml_path.name}: malformed single lock: {e}[/yellow]")
        return []


def units_from_picks_yaml(yaml_path: Path) -> list[TrackingUnit]:
    """10-ticker picks_card.yaml (v0.6 /picks output)."""
    with yaml_path.open(encoding="utf-8") as f:
        card = yaml.safe_load(f)
    if not isinstance(card, dict) or "lock" not in card:
        return []
    lock = card["lock"]
    try:
        picks_id = lock["picks_id"]
        entry_date = _parse_date(lock["entry_close_date"])
        benchmark = lock["benchmark"]
        bm_close = float(lock["benchmark_entry_close"])
        horizon = int(lock["prediction_horizon_days"])
    except (KeyError, ValueError, TypeError) as e:
        console.print(f"[yellow]{yaml_path.name}: malformed picks lock: {e}[/yellow]")
        return []

    units: list[TrackingUnit] = []
    # v0.8: 3 lists (ai_picks + market_picks + avoid_picks)
    # Legacy v0.6/v0.7: buy_picks (kept for backward compat with picks_192556)
    section_kinds = [
        ("picks_ai", "ai_picks"),           # v0.8 NEW
        ("picks_market", "market_picks"),   # v0.8 NEW
        ("picks_avoid", "avoid_picks"),
        ("picks_buy", "buy_picks"),         # legacy v0.6/v0.7
    ]
    for kind, key in section_kinds:
        for e in card.get(key) or []:
            try:
                units.append(TrackingUnit(
                    tracking_id=f"{picks_id}--{e['ticker']}",
                    ticker=e["ticker"],
                    entry_close=float(e["entry_close"]),
                    entry_close_date=entry_date,
                    benchmark=benchmark,
                    benchmark_entry_close=bm_close,
                    horizon_days=horizon,
                    source_kind=kind,
                    source_path=yaml_path.relative_to(ROOT).as_posix(),
                ))
            except (KeyError, ValueError, TypeError) as err:
                console.print(
                    f"[yellow]{yaml_path.name} {key} entry: {err}[/yellow]"
                )
    return units


def collect_all_units() -> list[TrackingUnit]:
    units: list[TrackingUnit] = []
    locked_dir = ROOT / "predictions" / "locked"
    picks_dir = ROOT / "predictions" / "picks"
    if locked_dir.exists():
        for yp in sorted(locked_dir.rglob("*.yaml")):
            units.extend(units_from_single_yaml(yp))
    if picks_dir.exists():
        for yp in sorted(picks_dir.rglob("*.yaml")):
            units.extend(units_from_picks_yaml(yp))
    return units


def already_tracked(tracking_id: str) -> set[int]:
    tracking_dir = ROOT / "predictions" / "tracking" / tracking_id
    if not tracking_dir.exists():
        return set()
    tracked: set[int] = set()
    for p in tracking_dir.glob("d*.json"):
        try:
            tracked.add(int(p.stem[1:]))
        except ValueError:
            continue
    return tracked


def is_invalidated(tracking_id: str) -> bool:
    tracking_dir = ROOT / "predictions" / "tracking" / tracking_id
    if not tracking_dir.exists():
        return False
    for p in tracking_dir.glob("d*.json"):
        try:
            with p.open(encoding="utf-8") as f:
                rec = json.load(f)
            if rec.get("invalidated"):
                return True
        except Exception:
            continue
    return False


def update_unit(unit: TrackingUnit, today: date) -> int:
    """Update tracking for one unit. Returns count of new records."""
    if is_invalidated(unit.tracking_id):
        return 0

    checkpoints = sorted({d for d in STANDARD_CHECKPOINTS if d <= unit.horizon_days} | {unit.horizon_days})
    already = already_tracked(unit.tracking_id)
    pending = [d for d in checkpoints if d not in already]
    if not pending:
        return 0

    n_written = 0
    for d in pending:
        try:
            trade_date = cal_data.add_trading_days(unit.entry_close_date, d)
        except Exception as e:
            console.print(f"[yellow]{unit.tracking_id} d{d}: cannot resolve trade date ({e})[/yellow]")
            continue
        if trade_date > today:
            continue

        try:
            stock_close = price_data.stock_close_on(unit.ticker, trade_date, adjust="qfq")
            bm_close = bm_data.benchmark_close_on(unit.benchmark, trade_date)
        except Exception as e:
            console.print(
                f"[yellow]{unit.tracking_id} d{d} ({trade_date}): "
                f"data fetch failed: {e}[/yellow]"
            )
            continue

        stock_ret = (stock_close - unit.entry_close) / unit.entry_close
        bm_ret = (bm_close - unit.benchmark_entry_close) / unit.benchmark_entry_close
        excess = stock_ret - bm_ret

        record = {
            "tracking_id": unit.tracking_id,
            "ticker": unit.ticker,
            "source_kind": unit.source_kind,
            "d_index": d,
            "trade_date": trade_date.isoformat(),
            "stock_close": round(stock_close, 4),
            "stock_return_cum": round(stock_ret, 4),
            "benchmark": unit.benchmark,
            "benchmark_close": round(bm_close, 4),
            "benchmark_return_cum": round(bm_ret, 4),
            "excess_return_cum": round(excess, 4),
            "events": [],
            "invalidated": False,
        }

        out_dir = ROOT / "predictions" / "tracking" / unit.tracking_id
        out_dir.mkdir(parents=True, exist_ok=True)
        out_path = out_dir / f"d{d}.json"
        with out_path.open("w", encoding="utf-8") as f:
            json.dump(record, f, ensure_ascii=False, indent=2)
        n_written += 1
        kind_tag = unit.source_kind.upper()
        console.print(
            f"  [green]{unit.tracking_id} d{d} ({trade_date}) [{kind_tag}]: "
            f"excess={excess:+.2%} (stk={stock_ret:+.2%}, bm={bm_ret:+.2%})[/green]"
        )

    return n_written


def main() -> None:
    today = cal_data.today_or_previous_trading_day()
    console.print(f"[blue]Updating tracking for date = {today}[/blue]")

    units = collect_all_units()
    if not units:
        console.print("[yellow]No predictions / picks found.[/yellow]")
        return

    n_single = sum(1 for u in units if u.source_kind == "single")
    n_ai = sum(1 for u in units if u.source_kind == "picks_ai")
    n_market = sum(1 for u in units if u.source_kind == "picks_market")
    n_buy_legacy = sum(1 for u in units if u.source_kind == "picks_buy")
    n_avoid = sum(1 for u in units if u.source_kind == "picks_avoid")
    console.print(
        f"  found {len(units)} tracking units "
        f"(single={n_single}, ai={n_ai}, market={n_market}, "
        f"avoid={n_avoid}, legacy_buy={n_buy_legacy})"
    )

    bm_data.refresh_cache()

    total_written = 0
    for unit in units:
        try:
            total_written += update_unit(unit, today)
        except Exception as e:
            console.print(f"[red]{unit.tracking_id}: error {e}[/red]")

    if total_written == 0:
        console.print("[yellow]No new tracking records written.[/yellow]")
    else:
        console.print(
            f"[bold green]Wrote {total_written} new tracking records[/bold green]"
        )


if __name__ == "__main__":
    main()
