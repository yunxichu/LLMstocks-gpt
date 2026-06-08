---
description: Objective review of locked predictions based on tracking data
---

You are about to produce an **objective forward-test review report** based on actually-tracked predictions.

## Hard discipline (read first)

- **Read-only**: this command never modifies locked predictions or tracking records
- **No cherry-picking**: all closed predictions enter the statistics
- **No retroactive justification**: don't explain away losses with "but it would have worked if..."
- **Pre-defined metrics only**: use the formulas in `playbooks/review.md`, don't invent new ones mid-report

## Required reading

1. `playbooks/review.md` — full workflow + decision rules
2. `playbooks/references/research-rubric.md` — for rubric calibration check

## Pre-flight check

Run integrity check first:

```powershell
python tools/verify_locks.py
```

If any HASH MISMATCH or missing files reported, **stop the review and report the integrity issue to the user**. Tampered predictions break forward-test validity.

## Required data

1. Load all locked cards: `predictions/locked/**/*.yaml`
2. Load all tracking records: `predictions/tracking/**/d*.json`
3. Load `predictions/index.csv` for quick scan

## Determine which predictions are "closed"

A prediction is **closed** when ANY of:
- `predictions/tracking/<id>/d<horizon>.json` exists (horizon reached)
- ANY tracking record has `invalidated: true` (early invalidation)

Open predictions (horizon not yet reached, not invalidated): include in "In-Flight" section but exclude from statistics.

## Workflow

Follow `playbooks/review.md` Step 1 through Step 8.

## Output

Save the report to `watchlist/history/<YYYY-MM-DD>/review.md` and print to user. Structure:

```markdown
# Forward-Test Review — <YYYY-MM-DD>

## Coverage
- Period: <range of analyzed_at>
- Long-term predictions: N_total (N_closed evaluated, N_in_flight open, N_invalidated invalidated)
- Short-term predictions: ...

## Aggregate Metrics — Long-Term (T+20 vs 沪深 300)
| Metric | Value |
|---|---|
| 胜率                  | X% |
| 平均超额收益          | X% |
| 中位超额收益          | X% |
| 最大单笔回撤          | X% |
| 标准差                | X% |
| IR (annualized proxy) | X  |

## Aggregate Metrics — Short-Term (T+5 vs 中证 1000)
...

## Decision per `playbooks/review.md` Step 4
**Long-term**: <信号有效 / 方向对幅度小 / 信号无效 / 严重 bug>
**Short-term**: ...

## Failure Case Clustering
...

## Success Case Clustering
...

## Playbook Improvement Proposals (待用户决策)
1. ...
2. ...

## Next Steps
- (推荐) ...
```

## What this command does NOT do

- Apply playbook changes. Proposals are listed; user decides.
- Re-evaluate invalidated predictions with hindsight.
- Modify any data file.

## After the report

If the user approves any improvement proposals:
1. Update `PLAN.md` §9.4 变更日志
2. Update the relevant playbook
3. Commit with a clear message
4. Start next forward-test window with new playbook version
