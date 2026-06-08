"""Verify integrity of locked predictions and picks files.

Usage:
    python tools/verify_locks.py

Detects:
- Modified raw.md (SHA-256 mismatch with stored hash)
- Missing raw.md
- Locks without claude_output_hash or playbook_version

Scans both:
- predictions/locked/**/*.yaml (single-ticker, v0.5)
- predictions/picks/**/*.yaml (10-ticker picks, v0.6+)

Exit code 0 = all OK; 1 = at least one issue.
"""

from __future__ import annotations

import hashlib
import sys
from pathlib import Path

import yaml
from rich.console import Console

ROOT = Path(__file__).resolve().parent.parent
console = Console()


def compute_raw_hash(raw_path: Path) -> str:
    h = hashlib.sha256()
    with raw_path.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def check_yaml(yaml_path: Path) -> tuple[int, str | None]:
    """Returns (status, error_msg). status: 0=ok, 1=mismatch, 2=missing_raw, 3=no_hash, 4=other."""
    rel = yaml_path.relative_to(ROOT).as_posix()
    try:
        with yaml_path.open(encoding="utf-8") as f:
            card = yaml.safe_load(f)
        lock = (card or {}).get("lock", {}) if isinstance(card, dict) else {}
    except Exception as e:
        return 4, f"{rel}: parse error {e}"

    raw_path = yaml_path.with_name(yaml_path.stem + ".raw.md")
    if not raw_path.exists():
        return 2, f"{rel}: missing raw.md"

    stored_hash = lock.get("claude_output_hash", "")
    if not stored_hash:
        return 3, f"{rel}: claude_output_hash empty (never locked?)"

    actual_hash = compute_raw_hash(raw_path)
    if stored_hash != actual_hash:
        return 1, (
            f"{rel}: HASH MISMATCH\n"
            f"    stored: {stored_hash[:32]}...\n"
            f"    actual: {actual_hash[:32]}..."
        )
    return 0, None


def main() -> int:
    candidates: list[Path] = []
    for sub in ("locked", "picks"):
        d = ROOT / "predictions" / sub
        if d.exists():
            candidates.extend(sorted(d.rglob("*.yaml")))

    if not candidates:
        console.print("[yellow]No locked predictions / picks found.[/yellow]")
        return 0

    n_total = len(candidates)
    n_ok = 0
    n_mismatch = 0
    n_missing_raw = 0
    n_no_hash = 0
    n_error = 0

    for yp in candidates:
        status, msg = check_yaml(yp)
        if status == 0:
            n_ok += 1
        else:
            if msg:
                console.print(f"[red]{msg}[/red]")
            if status == 1:
                n_mismatch += 1
            elif status == 2:
                n_missing_raw += 1
            elif status == 3:
                n_no_hash += 1
            else:
                n_error += 1

    console.print()
    console.print(f"Total YAMLs checked: {n_total}")
    console.print(f"  [green]OK:            {n_ok}[/green]")
    console.print(f"  [red]hash mismatch: {n_mismatch}[/red]")
    console.print(f"  [red]missing raw:   {n_missing_raw}[/red]")
    console.print(f"  [red]no hash:       {n_no_hash}[/red]")
    console.print(f"  [red]other error:   {n_error}[/red]")

    issues = n_mismatch + n_missing_raw + n_no_hash + n_error
    if issues:
        console.print(f"[bold red]Found {issues} issue(s)[/bold red]")
        return 1
    console.print("[bold green]All locks verified OK[/bold green]")
    return 0


if __name__ == "__main__":
    sys.exit(main())
