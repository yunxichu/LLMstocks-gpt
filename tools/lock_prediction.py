"""Lock a stock card prediction after Claude writes it.

Usage:
    python tools/lock_prediction.py predictions/locked/<date>/<prediction_id>.yaml

What it does:
1. Validates the LOCK area (all required fields present, prediction_id format,
   invalidation_conditions >= 3, etc.)
2. Looks for the accompanying raw markdown at <yaml_path>.raw.md (or
   <prediction_id>.raw.md in the same dir if `.yaml` is replaced)
3. Computes SHA-256 of the raw markdown -> lock.claude_output_hash
4. Records the playbook's current git SHA -> lock.playbook_version
5. Writes back the YAML
6. Appends a row to predictions/index.csv

After locking, the YAML and raw.md must NOT be edited. Use verify_locks.py
to detect tampering.
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

REQUIRED_LOCK_FIELDS = [
    "prediction_id",
    "analyzed_at",
    "ticker",
    "name",
    "playbook",
    "prediction_horizon_days",
    "benchmark",
    "entry_close",
    "entry_close_date",
    "benchmark_entry_close",
    "success_criteria",
    "failure_criteria",
    "invalidation_conditions",
]

PREDICTION_ID_PATTERN = re.compile(r"^\d{6}-\d{8}-\d{6}-(lt|st)$")


def git_sha_for(path: Path) -> str:
    """Get the current git SHA for a file. Fall back to HEAD if no per-file history."""
    try:
        if path.exists():
            result = subprocess.run(
                ["git", "log", "-n", "1", "--format=%H", "--", str(path)],
                capture_output=True, text=True, cwd=ROOT, timeout=10,
            )
            sha = result.stdout.strip()
            if sha:
                return sha
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            capture_output=True, text=True, cwd=ROOT, timeout=10,
        )
        sha = result.stdout.strip()
        return sha or "no-git"
    except Exception:
        return "no-git"


def compute_raw_hash(raw_path: Path) -> str:
    h = hashlib.sha256()
    with raw_path.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def validate_lock(lock: dict) -> list[str]:
    errors: list[str] = []
    for field in REQUIRED_LOCK_FIELDS:
        value = lock.get(field)
        if value is None or value == "" or (isinstance(value, (list, tuple)) and not value):
            errors.append(f"missing or empty: {field}")

    pid = lock.get("prediction_id", "")
    if pid and not PREDICTION_ID_PATTERN.match(pid):
        errors.append(
            f"prediction_id format invalid: '{pid}' "
            f"(expected <6digit>-<yyyymmdd>-<HHMMSS>-<lt|st>)"
        )

    if len(lock.get("invalidation_conditions") or []) < 3:
        errors.append("invalidation_conditions must have >= 3 entries")

    horizon = lock.get("prediction_horizon_days", 0)
    try:
        h = int(horizon)
        if h <= 0:
            errors.append(f"prediction_horizon_days must be > 0; got {horizon}")
    except Exception:
        errors.append(f"prediction_horizon_days must be int; got {horizon!r}")

    # entry_close and benchmark_entry_close must be positive floats
    for field in ("entry_close", "benchmark_entry_close"):
        try:
            v = float(lock.get(field, 0))
            if v <= 0:
                errors.append(f"{field} must be > 0; got {v}")
        except Exception:
            errors.append(f"{field} must be numeric; got {lock.get(field)!r}")

    return errors


def append_to_index(lock: dict, yaml_path: Path) -> None:
    index_path = ROOT / "predictions" / "index.csv"
    index_path.parent.mkdir(parents=True, exist_ok=True)
    is_new = not index_path.exists()
    rel = yaml_path.relative_to(ROOT).as_posix()
    with index_path.open("a", encoding="utf-8") as f:
        if is_new:
            f.write(
                "prediction_id,analyzed_at,ticker,name,playbook,"
                "horizon_days,benchmark,entry_close,entry_close_date,yaml_path\n"
            )
        f.write(
            f"{lock['prediction_id']},{lock['analyzed_at']},{lock['ticker']},"
            f"{lock['name']},{lock['playbook']},{lock['prediction_horizon_days']},"
            f"{lock['benchmark']},{lock['entry_close']},"
            f"{lock['entry_close_date']},{rel}\n"
        )


def main(yaml_path_str: str) -> int:
    yaml_path = Path(yaml_path_str).resolve()
    if not yaml_path.exists():
        console.print(f"[red]File not found: {yaml_path}[/red]")
        return 1

    # raw markdown lives at <id>.raw.md (replace .yaml with .raw.md)
    raw_path = yaml_path.with_name(yaml_path.stem + ".raw.md")
    if not raw_path.exists():
        console.print(f"[red]Raw markdown not found: {raw_path}[/red]")
        console.print(
            "  Claude must write <prediction_id>.raw.md alongside the YAML."
        )
        return 1

    with yaml_path.open(encoding="utf-8") as f:
        card = yaml.safe_load(f)

    if not isinstance(card, dict) or "lock" not in card:
        console.print("[red]Invalid card structure: missing top-level `lock`[/red]")
        return 1

    lock = card["lock"]

    errors = validate_lock(lock)
    if errors:
        console.print("[red]Lock validation failed:[/red]")
        for e in errors:
            console.print(f"  - {e}")
        return 1

    # Verify entry_close_date is a real trading day
    try:
        entry_date = datetime.strptime(lock["entry_close_date"], "%Y-%m-%d").date()
        if not cal_data.is_trading_day(entry_date):
            console.print(
                f"[yellow]Warning: entry_close_date {entry_date} is not a "
                f"trading day[/yellow]"
            )
    except Exception as e:
        console.print(f"[yellow]Could not verify entry_close_date: {e}[/yellow]")

    # Compute raw hash and playbook git sha
    raw_hash = compute_raw_hash(raw_path)
    playbook_name = lock["playbook"]
    playbook_path = ROOT / "playbooks" / playbook_name
    pb_sha = git_sha_for(playbook_path)

    lock["claude_output_hash"] = raw_hash
    lock["playbook_version"] = pb_sha
    card["lock"] = lock

    # Write back
    with yaml_path.open("w", encoding="utf-8") as f:
        yaml.safe_dump(
            card, f, allow_unicode=True, sort_keys=False, default_flow_style=False
        )

    append_to_index(lock, yaml_path)

    console.print(f"[bold green]Locked: {lock['prediction_id']}[/bold green]")
    console.print(f"  ticker:   {lock['ticker']} ({lock['name']})")
    console.print(f"  playbook: {playbook_name}@{pb_sha[:8]}")
    console.print(f"  horizon:  T+{lock['prediction_horizon_days']} vs {lock['benchmark']}")
    console.print(f"  hash:     {raw_hash[:16]}...")
    return 0


if __name__ == "__main__":
    if len(sys.argv) < 2:
        console.print("Usage: python tools/lock_prediction.py <yaml_path>")
        sys.exit(1)
    sys.exit(main(sys.argv[1]))
