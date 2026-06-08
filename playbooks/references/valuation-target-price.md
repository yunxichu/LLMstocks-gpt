# Target Price Valuation Standard

> Use this reference whenever `/picks` or `/analyze` assigns a target price, fair-value range, or overvaluation warning. A target price is not acceptable unless it explains the earnings forecast, valuation method, research-report context, and revision triggers.

---

## 1. Minimum Bar

A target price must include all of the following:

1. **Latest financial anchor**
   - Latest annual report, quarterly report, profit alert, earnings forecast, or investor-relations record.
   - Revenue, net profit, operating cash flow, gross margin / net margin, share count or dilution assumption.

2. **Research-report matrix**
   - Prefer 3-5 recent institutional reports or consensus records from the last 90 days.
   - If the reports are paywalled, record only metadata: institution, date, rating, target price, EPS forecast, valuation method, and short paraphrased thesis. Do not store copyrighted report text or charts.
   - If fewer than 3 credible reports are available, set `research_coverage_status: partial` or `unavailable`.

3. **EPS / profit forecast bridge**
   - FY2025 actual or latest trailing EPS.
   - FY2026 / FY2027 EPS or net-profit forecast.
   - The bridge from financials to forecast: volume, ASP, gross margin, operating leverage, share count, tax, minority interest, dilution.

4. **Valuation method**
   - At least one primary method and one cross-check.
   - Explain why the method fits the industry.
   - Show the formula.

5. **Target-price dispersion**
   - External high / median / mean / low target price when available.
   - Own base / bull / bear target price.
   - Explain why our base differs from consensus.

6. **Revision triggers**
   - Upward triggers: which financial or industry evidence raises EPS or multiple.
   - Downward triggers: which evidence lowers EPS, multiple, or conviction.

7. **Evidence grade**
   - `hard`: filings, official reports, audited financials, regulator/industry official data, authorized consensus database.
   - `soft`: broker research view, management tone, media interview, market consensus.
   - `pending_verify`: metadata found but original document not read, paywalled report not available, unconfirmed customer relationship.

---

## 2. Research-Report Matrix

Each target-price section must contain a matrix like this:

```yaml
research_report_matrix:
  status: complete | partial | unavailable
  lookback_days: 90
  reports:
    - institution: ""
      analyst: ""
      date: ""
      rating: buy | outperform | hold | underperform | sell | unavailable
      rating_action: upgrade | downgrade | initiate | maintain | suspend | unavailable
      target_price: null
      fy2026_eps: null
      fy2027_eps: null
      fy2026_net_profit: null
      fy2027_net_profit: null
      valuation_method: PE | PEG | PB_ROE | EV_EBITDA | EV_Sales | DCF | SOTP | NAV | other
      core_assumptions: []
      access: authorized_full | public_summary | paywalled_metadata | unavailable
      evidence_type: hard | soft | pending_verify
      source: ""
```

Rules:

- A broker report is **soft evidence** unless the full report is accessible through an authorized subscription or the report is officially published by the institution.
- A consensus database such as Wind, Choice, FactSet, LSEG I/B/E/S, Bloomberg, or Refinitiv is **hard evidence** only when accessed through an authorized account and the exact snapshot date is recorded.
- Reposted report PDFs from document-sharing sites are not acceptable evidence.

---

## 3. EPS Forecast Bridge

Every BUY/WATCH target price must show how earnings are estimated.

```yaml
eps_forecast_bridge:
  latest_actual:
    fiscal_period: ""
    revenue: null
    net_profit_parent: null
    eps: null
    operating_cash_flow: null
    source: ""
  fy2026_forecast:
    revenue: null
    net_profit_parent: null
    eps: null
    gross_margin: null
    key_drivers: []
  fy2027_forecast:
    revenue: null
    net_profit_parent: null
    eps: null
    gross_margin: null
    key_drivers: []
  bridge_logic:
    volume: ""
    asp: ""
    margin: ""
    opex: ""
    share_count_or_dilution: ""
    tax_or_minority_interest: ""
  confidence: high | medium | low
```

Minimum rule:

- Do not use `current_price / forward_PE` as the only EPS source.
- If no institutional EPS forecast is available, build a conservative internal EPS forecast from company filings and mark it `internal_model`.
- If neither external nor internal EPS is reliable, do not issue a precise target price; issue a broad fair-value range and downgrade confidence.

---

## 4. Valuation Method by Business Type

| Business type | Primary method | Cross-check | Notes |
|---|---|---|---|
| Quality software / SaaS | PE on normalized EPS, DCF | EV/Sales, PEG | Use subscription growth, retention, margin expansion. |
| AI server / electronics manufacturing | PE, EV/EBITDA | ROE / FCF, peer comps | Apply customer concentration and margin discount. |
| Semiconductor equipment | PE, EV/Sales / EV/EBITDA | backlog, order growth | High multiples require order visibility. |
| Optical modules / CPO | forward PE, PEG | customer capex, inventory | Apply cycle and price-pressure discount after sharp rallies. |
| Batteries / energy storage | PE, EV/EBITDA | DCF, commodity sensitivity | Model ASP, utilization, raw-material cost, overseas policy. |
| Power equipment / grid | PE, EV/EBITDA | order backlog, overseas mix | Stable order visibility can support higher PE. |
| CXO / biotech services | PE, EV/EBITDA | FCF yield | Apply geopolitical and customer-concentration discount. |
| Early-stage / loss-making tech | EV/Sales, scenario DCF | SOTP | Do not use PE when earnings are too volatile. |
| Banks / insurers | PB-ROE | dividend yield | PE alone is insufficient. |
| Asset-heavy cyclicals | EV/EBITDA, PB | replacement cost | Use cycle trough / peak scenario. |

---

## 5. Formulas

### PE

```text
target_price = forecast_EPS × justified_PE
```

Justified PE inputs:

- Sector PE range.
- Company growth, ROE, FCF quality.
- Earnings visibility.
- Policy, cycle, customer-concentration, governance, and red-flag discounts.

### PEG

```text
PEG = PE / expected_EPS_growth_rate
```

Use only when EPS growth is positive and not purely from a one-off recovery.

### EV/EBITDA

```text
enterprise_value = forecast_EBITDA × target_EV_EBITDA
equity_value = enterprise_value - net_debt + excess_cash - minority_interest
target_price = equity_value / diluted_shares
```

Use for capital-intensive or cross-capital-structure comparisons.

### DCF

```text
firm_value = PV(FCFF years 1..N) + PV(terminal_value)
equity_value = firm_value - net_debt + excess_cash - minority_interest
target_price = equity_value / diluted_shares
```

Required DCF assumptions:

- Forecast period.
- WACC / discount rate.
- Terminal growth or exit multiple.
- Capex, working capital, tax, share dilution.
- Sensitivity table.

### SOTP

```text
target_price = sum(segment_value_i) - net_debt + excess_cash - minority_interest
```

Use when segments have clearly different economics, such as hardware + software, battery + storage, CRO + CDMO.

---

## 6. Target-Price Construction

Use base / bull / bear:

```yaml
target_price_review:
  status: research_grade | provisional | unavailable
  horizon_months: 12
  current_price: null
  base_target: null
  target_range: [null, null]
  upside_pct: null
  bear_case:
    target: null
    assumptions: []
  base_case:
    target: null
    assumptions: []
  bull_case:
    target: null
    assumptions: []
  consensus_cross_check:
    target_mean: null
    target_median: null
    target_high: null
    target_low: null
    analyst_count: null
    source: ""
    snapshot_date: ""
  selected_method:
    primary: ""
    cross_checks: []
    justification: ""
  eps_forecast_bridge: {}
  research_report_matrix: {}
  revision_triggers:
    upward: []
    downward: []
  evidence_grade:
    financials: hard | soft | pending_verify
    research_reports: hard | soft | pending_verify | unavailable
    industry_data: hard | soft | pending_verify
    consensus: hard | soft | pending_verify | unavailable
  open_checks: []
```

`status` rules:

- `research_grade`: latest filings read, at least 3 credible recent research/consensus inputs, EPS bridge built, primary + cross-check valuation shown, revision triggers listed.
- `provisional`: latest filings read and model shown, but fewer than 3 research/consensus inputs or incomplete smart-money data.
- `unavailable`: data gaps are too large; no target price should be published.

---

## 7. AVOID Valuation

AVOID names still need valuation work. Use:

```yaml
valuation_red_flag:
  fair_value_or_risk_range: [null, null]
  current_price: null
  overvaluation_reason: ""
  method: ""
  reversal_conditions: []
  evidence_grade: {}
```

Examples:

- `current_price` above consensus high target.
- `forward_PE` requires unrealistic EPS growth.
- `EV/Sales` implies margins far above sector leaders.
- `DCF` only works with aggressive terminal growth or low discount rate.

---

## 8. Hard Rejection Rules

Reject or downgrade target-price confidence when:

- No latest filing or official financial source is used.
- No EPS/profit forecast bridge exists.
- Only yfinance target price is cited.
- The target price is copied from one broker without explanation.
- The report stores paywalled research text, charts, or tables beyond short metadata.
- Valuation method is mismatched to the business model.
- BUY target upside is below 15% and evidence quality is not high.
- AVOID has no fair-value/risk range.

---

## 9. Sources and Methodology References

- CFA Institute equity valuation process: https://www.cfainstitute.org/insights/professional-learning/refresher-readings/2026/equity-valuation-applications-and-processes
- CFA Institute valuation concepts and basic tools: https://www.cfainstitute.org/insights/professional-learning/refresher-readings/2025/equity-valuation-concepts-basic-tools
- LSEG I/B/E/S Estimates overview: https://www.lseg.com/en/data-analytics/financial-data/company-data/ibes-estimates
- FactSet point-in-time consensus overview: https://insight.factset.com/resources/at-a-glance-factset-estimates-point-in-time-consensus
- Morningstar equity methodology overview: https://indexes.morningstar.com/docs/calculation-and-methodology/morningstar-equity-research-methodology
