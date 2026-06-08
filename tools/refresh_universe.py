"""Validate watchlist tickers against yfinance + emit universe.csv.

v0.5 change: this no longer does a full-market screen (yfinance has no
batch endpoint for the entire A-share market, and full-market scans are
over-engineered for personal research).

Behavior:
1. Loads `watchlist/watchlist.yaml`
2. Validates each ticker is reachable via yfinance
3. Outputs `watchlist/universe.csv` for compatibility / quick reference
4. Reports failed tickers (e.g., delisted, 北交所 not supported by yfinance)

Run after:
- Adding new tickers to watchlist.yaml
- Periodically (e.g., monthly) to catch delisted / renamed tickers

For finding NEW candidates (beyond what's in watchlist), use the /screen
playbook — it's watchlist-based + theme-driven, not full-market scan.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import yaml
from rich.console import Console

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from data.web import a_share  # noqa: E402

console = Console()


def load_watchlist() -> list[dict]:
    """Load watchlist.yaml. Returns list of {ticker, ...} dicts."""
    p = ROOT / "watchlist" / "watchlist.yaml"
    if not p.exists():
        return []
    with p.open(encoding="utf-8") as f:
        data = yaml.safe_load(f) or []
    if not isinstance(data, list):
        raise ValueError(
            f"watchlist.yaml must be a list of entries; got {type(data).__name__}"
        )
    return data


def normalize_entry(entry) -> dict:
    """Accept either a bare ticker string or a full dict entry."""
    if isinstance(entry, str):
        return {"ticker": entry}
    if isinstance(entry, dict) and "ticker" in entry:
        return entry
    raise ValueError(f"Bad watchlist entry: {entry!r}")


def validate_one(ticker: str) -> dict:
    """Fetch basic info; return {ok, ticker, name, ...} or {ok: False, error}."""
    try:
        info = a_share.stock_info(ticker)
        name = info.get("shortName") or info.get("longName") or ""
        return {
            "ok": True,
            "ticker": ticker,
            "name": name,
            "industry": info.get("industry") or "",
            "sector": info.get("sector") or "",
            "market_cap": info.get("marketCap"),
            "pe_ttm": info.get("trailingPE"),
            "pb": info.get("priceToBook"),
            "currency": info.get("currency"),
            "is_st": "ST" in str(name).upper(),
            "market_segment": a_share.market_segment(ticker),
        }
    except Exception as e:
        return {"ok": False, "ticker": ticker, "error": str(e)}


def main() -> None:
    entries = load_watchlist()
    if not entries:
        console.print("[yellow]Watchlist is empty.[/yellow]")
        console.print("Start by either:")
        console.print(
            "  1) [bold]cp watchlist/watchlist.yaml.example watchlist/watchlist.yaml[/bold]"
        )
        console.print(
            "  2) Manually add tickers to watchlist/watchlist.yaml, then re-run"
        )
        console.print(
            "  3) Run /screen in Claude Code to surface new candidates"
        )
        return

    console.print(f"[blue]Validating {len(entries)} watchlist entries...[/blue]")

    rows = []
    for raw in entries:
        try:
            entry = normalize_entry(raw)
        except ValueError as e:
            console.print(f"[red]Skipping bad entry: {e}[/red]")
            continue
        ticker = entry["ticker"]
        console.print(f"  {ticker}...")
        result = validate_one(ticker)
        # Carry forward extra metadata from the yaml entry
        for k in ("theme", "rationale", "status", "added_on", "added_by"):
            if k in entry and entry[k] is not None:
                result[k] = entry[k]
        rows.append(result)

    n_ok = sum(1 for r in rows if r["ok"])
    n_failed = len(rows) - n_ok
    console.print(f"[green]OK: {n_ok}[/green] / [red]Failed: {n_failed}[/red]")

    if n_failed:
        console.print("[red]Failed tickers:[/red]")
        for r in rows:
            if not r["ok"]:
                console.print(f"  {r['ticker']}: {r.get('error', 'unknown')}")
        console.print(
            "Causes: delisted, 北交所 ('.BJ' not supported by yfinance), "
            "or transient yfinance outage. Retry, or remove if delisted."
        )

    # Emit universe.csv (only validated rows)
    ok_rows = [r for r in rows if r["ok"]]
    if not ok_rows:
        console.print("[yellow]No validated tickers; nothing to write.[/yellow]")
        return

    output_path = ROOT / "watchlist" / "universe.csv"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    cols = [
        "ticker", "name", "sector", "industry", "market_cap", "pe_ttm", "pb",
        "currency", "is_st", "market_segment",
        "theme", "rationale", "status", "added_on", "added_by",
    ]
    out = pd.DataFrame(ok_rows)
    for c in cols:
        if c not in out.columns:
            out[c] = None
    out = out[cols].sort_values(
        "market_cap", ascending=False, na_position="last"
    ).reset_index(drop=True)
    out.to_csv(output_path, index=False, encoding="utf-8-sig")
    console.print(f"[bold green]Wrote {len(out)} rows to {output_path}[/bold green]")


if __name__ == "__main__":
    main()
