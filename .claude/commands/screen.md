---
description: Weekly A-share screen — propose 5-10 long-term candidates worth deeper /analyze
---

You are about to run the **weekly screen** to generate 5-10 candidates for long-term analysis.

## Required reading

1. `playbooks/screen.md` — full workflow
2. `playbooks/references/pattern-library.md` — for chokepoint pattern matching (Category A) and A-share specific patterns (Category B)
3. `playbooks/references/a-share-data-sources.md` — news triage rules
4. `config/themes.yaml` — current theme registry

## Required data

Before reasoning:

1. Load `watchlist/universe.csv`. If missing or stale (> 7 days old), tell the user to run:
   ```powershell
   python tools/refresh_universe.py
   ```
   and stop.

2. Pull recent (last 7 days) market data via AKShare:
   - Sector fund flow ranks: `data.ashare.fund_flow.sector_fund_flow()`
   - LHB summary: `data.ashare.lhb.lhb_range(today - 7, today)`

3. Pull recent (last 7-30 days) disclosures via Tushare MCP:
   - Earnings pre-announcements (`forecast`, `express`)
   - Major insider sells, share unlocks, dilutions
   - Major contracts

## Workflow

Follow `playbooks/screen.md` Step 1 through Step 8.

## Output

1. Print the screen list to the user (per Step 7 markdown template).

2. Save a copy at `watchlist/history/<YYYY-MM-DD>/screen.md`.

3. Append candidates to `watchlist/watchlist.yaml` (create if missing). Each entry:
   ```yaml
   - ticker: 600519.SH
     added_on: <YYYY-MM-DD>
     added_by: weekly_screen
     rationale: <1 sentence>
     status: candidate
   ```

## What this command does NOT do

- Lock predictions. Locking happens only via `/analyze <ticker>` per candidate.
- Mass-analyze every candidate. Output is a curated list; user picks which to deep-analyze.

## Hard constraints

- Maximum 10 candidates. Less is better than more.
- Apply A-share hard risk filters (减持 / 解禁 / 商誉 / 质押 / ST) — any hit excludes the candidate from the list.
- Do not include candidates already on `watchlist/watchlist.yaml` unless their signal strengthened materially this week (re-list with `status: re-confirmed` and note).
