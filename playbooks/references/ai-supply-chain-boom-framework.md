# AI Supply-Chain Boom Framework

> Use this reference for AI-related `/picks`, `/theme`, and `/analyze` work.
> The goal is to avoid a classic valuation mistake: treating a multi-year AI
> infrastructure buildout like a normal one-year earnings cycle.

---

## 1. Why This Framework Exists

The AI chain is no longer just a "theme". As of 2026-06-09, current public
evidence points to a capex arms race with real bottlenecks:

- NVIDIA FY2027 Q1 revenue was $81.6bn, up 85% YoY; Data Center revenue was
  $75.2bn, up 92% YoY; FY2027 Q2 revenue guidance was $91.0bn.
- Microsoft FY2026 Q3 disclosed AI annual revenue run rate above $37bn, up
  123% YoY.
- Alphabet said AI demand is exceeding available supply, guided 2026 capex to
  $180-190bn, and said 2027 capex should increase significantly versus 2026.
- Meta raised 2026 capex guidance to $125-145bn, citing higher component
  pricing and additional data center costs.
- TrendForce says AI demand has caused bottlenecks in 3nm-2nm wafers and
  2.5D/3D advanced packaging; the CoWoS shortage has extended upstream to
  equipment and downstream to substrates, packaging materials and other parts.
- TrendForce forecasts 2026 AI server shipments to grow more than 20%, AI
  server revenue to grow more than 30%, and HBM usage to rise more than 70%.
- IEA projects global data-center electricity consumption to roughly double
  to about 945 TWh by 2030; accelerated-server electricity consumption grows
  around 30% annually in its base case.
- Uptime Institute expects developers will not outrun power shortages; it
  frames power availability as a constraint on 2026 data-center deployment.

Implication: **AI valuation must separate ordinary expensive stocks from
strategically scarce bottleneck assets.** A high PE is not automatically a
sell if the company controls a bottleneck that is being pulled by multi-year
capex and booked capacity. But a high PE is still dangerous if the company has
no proven node, no customer/capacity evidence, or no financial translation.

---

## 2. Future-Backcast First

Do not begin with today's ticker list. Begin with the AI world 3-5 years out,
then work backward.

### 2.1 Base Future State: 2028-2030 AI World

Use this as the default prior unless current evidence changes:

```text
AI moves from model training as the center of gravity
-> to always-on inference, reasoning, agents, video, robotics and enterprise workflow automation
-> AI factories become power-dense, rack-scale industrial infrastructure
-> chip design moves toward GPU + custom ASIC + HBM + advanced packaging
-> cluster performance depends on memory bandwidth, packaging, networking, PCB/substrate, power and cooling
-> national AI stacks increase demand for domestic substitutes in China
```

The future world is therefore not just "more GPUs". It is:

- more accelerated servers and custom ASICs;
- more HBM and memory bandwidth;
- more 2.5D/3D packaging and substrate area;
- more high-speed PCB, connectors, optics and switching;
- more data-center power, cooling, grid equipment and energy storage;
- more domestic AI infrastructure where export controls limit direct access;
- more software that embeds AI into real workflow distribution.

### 2.2 Future-Backcast Questions

For every AI candidate, answer in this order:

1. What must be much larger in the 2028-2030 AI world?
2. Which physical or software node becomes constrained if that future arrives?
3. Is the constraint scarce, qualified, capacity-limited, power-limited or
   architecture-locked?
4. Does this company own capacity, know-how, customer qualification, or
   domestic substitution value at that node?
5. Can the future node become revenue, margin, EPS and cash flow for this
   company, not just market narrative?
6. Is today's price still below the future-backed base case, or already near
   the future bull case?

### 2.3 Future-Backcast Score

Each AI candidate can receive a 0-100 `future_backcast_score`.

| Dimension | Points | What To Prove |
|---|---:|---|
| Future demand inevitability | 15 | The node must expand materially if AI inference/agents/data centers scale. |
| Node criticality in future AI architecture | 20 | The node is structurally required, not optional or easily designed out. |
| Company positioning and qualification path | 15 | Current products, capex, customers, validation or technical capability map to the future node. |
| Financial translation path | 15 | There is a credible bridge to revenue, margin, EPS, cash flow and ROIC. |
| Scarcity and pricing power | 10 | Supply cannot catch up easily; switching/qualification/lead time protects returns. |
| Domestic strategic value | 10 | China localization, export controls or strategic customers make the node more valuable. |
| Balance-sheet and capex survivability | 5 | The company can fund the transition without excessive dilution or financial stress. |
| Current pricing gap | 10 | The market is not already pricing the future bull case. |

Interpretation:

| Score | Future-Backcast View |
|---:|---|
| 85-100 | Core future infrastructure candidate; staged BUY can be justified even if 12M upside is modest. |
| 70-84 | Strong candidate; BUY on pullback or proof, WATCH+ if already near 12M fair value. |
| 55-69 | Real option, but execution proof is required before treating it as core. |
| <55 | Theme exposure only; do not use the future story to override valuation. |

---

## 3. The New Mental Model

### 3.1 Two Time Scales

Every AI pick now has two separate views:

```text
12M target price
-> near-term earnings, consensus, valuation discipline, downside control

3-5Y structural option
-> capacity scarcity, architecture lock-in, customer pull, capex cycle, strategic value
```

Do not collapse them into one number. A stock can be:

- `near_term_buy + structural_buy`: best setup.
- `near_term_watch + structural_buy`: not cheap today, but too important to
  discard; size carefully or wait for pullbacks.
- `near_term_avoid + structural_watch`: good story, price already in bull case.
- `near_term_avoid + structural_avoid`: theme-only or overbuilt.

### 3.2 Bottleneck First, Ticker Second

Start with the supply-chain node, not the stock:

```text
AI model demand
-> GPU / ASIC / accelerator rack
-> HBM + advanced packaging + substrate + PCB + optical + power + cooling
-> capacity reservation, lead time, qualification, pricing
-> company revenue, margin, cash flow, dilution
```

The correct question is:

> If AI capex doubles again, which exact physical or technical constraint gets
> paid first, and does this company own that constraint?

---

## 4. AI Bottleneck Score

Each AI candidate must receive a 0-100 `ai_bottleneck_score`.

| Dimension | Points | What To Prove |
|---|---:|---|
| End-market capex intensity | 10 | CSP/sovereign/cloud/server capex or order pull is rising. |
| Node bottleneck strength | 20 | Capacity is scarce, qualification is long, switching cost is high, or supply is pre-booked. |
| Architecture lock-in | 15 | New platforms such as GB/Rubin racks, ASIC clusters, HBM4, CoWoS/SoIC, 1.6T/3.2T optical, liquid cooling, HVDC power change supplier economics. |
| Customer/order/capacity evidence | 15 | Company filing, IR, customer disclosure, backlog, capex, utilization, or qualification evidence. |
| Financial translation | 15 | Revenue, gross margin, EPS, cash flow, utilization, or ASP bridge is visible. |
| Supply expansion and dilution risk | 10 | Competitor capacity, own capex, depreciation, debt, or equity issuance risk is bounded. |
| Capital validation | 5 | Institutional ownership, strategic shareholder, high-quality fund, or customer capital validation. |
| Re-rating optionality | 10 | Market still prices the company as old economy / normal cycle, not as an AI bottleneck. |

Interpretation:

| Score | Structural View |
|---:|---|
| 85-100 | Strategic bottleneck; scarcity premium can be large if financial translation is proven. |
| 70-84 | Strong AI node; BUY/WATCH depends on current price and evidence quality. |
| 55-69 | Plausible beneficiary; no valuation override unless new hard evidence appears. |
| <55 | Theme exposure only; normal valuation discipline applies. |

---

## 5. Scarcity Premium Rules

Traditional valuation:

```text
target_price = forecast_EPS × justified_PE
```

AI scarcity valuation:

```text
target_price =
  normalized_earnings_value
  + probability_of_bottleneck_success × structural_option_value
  - probability_of_execution_failure × capex_dilution_penalty
```

### 5.1 When A Multiple Override Is Allowed

Allow an AI scarcity premium only when all are true:

- `ai_bottleneck_score >= 70`.
- At least 2 hard evidence items prove supply-chain role and customer/capacity
  pull.
- Latest financials show revenue or margin translation, or management gives
  specific capacity/utilization/qualification milestones.
- No HIGH red flag.
- Bull case does not require impossible margin, market share, or terminal
  growth assumptions.

Suggested PE/PB premium guardrails:

| Bottleneck Score | Allowed Premium To Normal Multiple |
|---:|---:|
| 85-100 | +30% to +60% |
| 70-84 | +15% to +30% |
| 55-69 | 0% to +15%, only if near-term numbers are also improving |
| <55 | 0% |

Apply discounts for:

- customer concentration;
- heavy capex / depreciation;
- equity issuance and dilution;
- capacity coming online across peers;
- weak cash conversion;
- export controls or geopolitics;
- management credibility gaps.

### 5.2 When High PE Is Still A Red Flag

High PE remains dangerous when:

- the chain role is generic or unproven;
- the company only says "AI-related" without product, customer, capacity or
  margin detail;
- the stock price already exceeds the structural bull case;
- earnings growth comes mainly from one-off gains;
- new capacity requires large debt/equity financing before orders are proven;
- the bottleneck is migrating to a different architecture.

---

## 6. Required Output Field

Every AI pick must include:

```yaml
ai_supply_chain_review:
  status: complete | partial | unavailable
  structural_horizon_years: 3-5
  chain_node: hbm | advanced-packaging | substrate | pcb | optical | server | power | cooling | semiconductor-equipment | software | robotics | other
  ai_demand_evidence: []
  bottleneck_evidence: []
  customer_capacity_evidence: []
  financial_translation:
    revenue_bridge: ""
    margin_bridge: ""
    capex_or_depreciation: ""
    utilization_or_backlog: ""
    evidence_grade: hard | soft | pending_verify
  bottleneck_score:
    end_market_capex: 0
    node_bottleneck: 0
    architecture_lock_in: 0
    customer_capacity: 0
    financial_translation: 0
    supply_expansion_risk: 0
    capital_validation: 0
    rerating_optionality: 0
  bottleneck_score_total: 0
  future_backcast_score:
    future_demand_inevitability: 0
    node_criticality: 0
    company_positioning: 0
    financial_translation_path: 0
    scarcity_pricing_power: 0
    domestic_strategic_value: 0
    capex_survivability: 0
    current_pricing_gap: 0
  future_backcast_score_total: 0
  scarcity_premium:
    multiple_override_allowed: false
    allowed_premium_to_normal_multiple: "0%"
    conditions: []
  structural_verdict: structural_buy | watch | avoid
  thesis_breakers: []
  open_checks: []
```

---

## 7. Decision Upgrade Rules

Use both valuation and AI structural score:

| Near-Term Valuation | AI Bottleneck Score | Result |
|---|---:|---|
| Upside >= 15%, no HIGH red flag | >=70 | BUY |
| Upside 0-15%, no HIGH red flag | >=85 and option value not overpaid | BUY / high-risk or WATCH, depending on liquidity and evidence |
| Downside to base target, but structural bull case above current | >=80 | WATCH / wait for pullback or EPS upgrade |
| Downside to base target and current already near bull case | any | AVOID / not chase |
| No financial translation | <70 | AVOID if expensive; otherwise WATCH only |

This is the key change from the previous framework: **a high-quality AI
bottleneck can prevent a stock from being mechanically labeled AVOID just
because 12M PE is high.** It cannot, however, turn an unproven theme stock into
a BUY.

Future-backcast override:

- If `future_backcast_score >= 85`, 12M target upside is allowed to be modest
  if the current price is far below the 3-5Y base case.
- If `future_backcast_score` is 70-84, do not chase price above the 12M fair
  range unless fresh hard evidence raises the financial translation path.
- If `future_backcast_score` is 55-69, treat the stock as an option, not a
  core holding.
- If current price already approaches the 3-5Y bull case, downgrade to WATCH
  or AVOID regardless of the future story.

---

## 8. Source Anchors

- NVIDIA FY2027 Q1 results: https://investor.nvidia.com/news/press-release-details/2026/NVIDIA-Announces-Financial-Results-for-First-Quarter-Fiscal-2027/default.aspx
- Microsoft FY2026 Q3 results: https://www.microsoft.com/en-us/investor/earnings/fy-2026-q3/press-release-webcast
- Alphabet 2026 equity/capex press release: https://s206.q4cdn.com/479360582/files/doc_news/2026/Jun/01/attachments/2026-June-Alphabet-Equity-Capital-Raise-Press-Release-PDF.pdf
- Meta Q1 2026 results: https://investor.atmeta.com/investor-news/press-release-details/2026/Meta-Reports-First-Quarter-2026-Results/
- TrendForce 2026-04-30 AI supply chain arms race: https://www.trendforce.com/presscenter/news/20260430-13028.html
- TrendForce 2025-10-30 AI server outlook: https://www.trendforce.com/presscenter/news/20251030-12762.html
- IEA Energy and AI: https://www.iea.org/reports/energy-and-ai/energy-demand-from-ai
- Uptime Institute 2026 data center predictions: https://uptimeinstitute.com/about-ui/press-releases/uptime-institute-announces-five-data-center-predictions-report-for-2026
