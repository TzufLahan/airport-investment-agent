# Autonomous agent -- validation report

Model: **claude-sonnet-5**  ·  10 cases + a consistency check.


**Hard-check pass rate: 10/10  ·  consistency: STABLE**


**Consistency (3x, LAX/SNA scores identical every run): STABLE**  ·  [{'LAX.investment_score': True, 'SNA.investment_score': True}, {'LAX.investment_score': True, 'SNA.investment_score': True}, {'LAX.investment_score': True, 'SNA.investment_score': True}]


## [PASS] compare-tier1

**Q:** Compare LA and Santa Ana on our investment score.

- no_crash: True · tools_ok: True (saw ['compare_airports', 'resolve_airport']) · substr_ok: True · steps: 3
- grounding LAX.investment_score: [OK] expected one of ['62.9']
- grounding SNA.investment_score: [OK] expected one of ['32.3']

**Answer:**

**Both are Tier 1**, so their investment_scores are directly comparable.

| Metric | LAX (Los Angeles Intl) | SNA (John Wayne–Orange County) |
|---|---|---|
| **Investment score** | **62.9** | **32.3** |
| Congestion norm | 55.0 (ratio 2412 ops/declared cap 172/hr) | 32.7 (ratio 1623 ops/declared cap 58/hr) |
| Growth norm (CAGR) | 57.4 (3.59%/yr) | 33.2 (-1.70%/yr, shrinking) |
| Volume norm | 89.9 (37.76M pax, 413.6k ops) | 29.9 (5.37M pax, 95k ops) |

**Takeaway:** LAX scores nearly double SNA (62.9 vs 32.3) — driven by much larger volume, positive growth, and higher congestion pressure (all of which signal stronger capacity-expansion investment case).

One important caveat for SNA: it carries a note that its commercial operations/passengers are **capped by a community Settlement Agreement (amended 2003)**, so its practical commercial capacity sits below the physical runway capacity — this structurally suppresses its volume, growth, and congestion sub-scores versus what raw infrastructure might otherwise support. That's a real-world constraint reflected in the deterministic data, not an error.

Want me to pull FAA NPIAS profiles for both to see funding/capacity outlook alongside these scores?

**Tool trace:** resolve_airport -> resolve_airport -> compare_airports


## [PASS] metric-congestion

**Q:** How congested is JFK?

- no_crash: True · tools_ok: True (saw ['get_airport_score', 'get_npias', 'resolve_airport']) · substr_ok: True · steps: 3
- grounding JFK.congestion_norm: [OK] expected one of ['68.4']

**Answer:**

**JFK congestion snapshot (from our deterministic scoring model):**

- **Congestion sub-score: 68.4 / 100** (a fairly high reading, reflecting real operational strain)
- **Congestion ratio: 2,886** (annual ops relative to declared hourly capacity of 88 ops/hr) — this is the raw driver behind the sub-score
- Annual operations: 255,441; annual passengers (CY24): ~31.5M
- This feeds into JFK's overall Tier‑1 **investment_score of 60.3** (which also factors growth_norm 40.1 and volume_norm 84.3 — note growth CAGR is actually slightly negative at -0.18%, so the score is being pulled up mainly by volume and congestion, not growth)

**FAA NPIAS second opinion (independent of our score):**
- Capacity outlook 2028: **"capacity constrained"**
- Capacity outlook 2033: **"severe capacity constraints"**
- 5-year planned development cost: ~$257M (49th percentile among the 65 airports — mid-pack spending relative to peers)

**Bottom line:** JFK is genuinely congested today (congestion_norm 68.4) and the FAA's independent outlook agrees the situation gets worse, not better — from "capacity constrained" in 2028 to "severe capacity constraints" by 2033. Passenger growth has been flat-to-slightly-negative recently, so the congestion pressure is coming from volume/operations bumping against a tight declared capacity ceiling (88 ops/hr) rather than from rapid demand growth.

**Tool trace:** resolve_airport -> get_airport_score -> get_npias


## [PASS] rank-region

**Q:** Rank the New England airports as expansion candidates.

- no_crash: True · tools_ok: True (saw ['get_npias', 'list_scope', 'rank_airports']) · substr_ok: True · steps: 3
- grounding BOS.investment_score: [OK] expected one of ['70.8']

**Answer:**

## New England Expansion Candidates

Our in-scope dataset covers only **two** New England airports: **BOS** (Tier 1) and **BDL** (Tier 2). Note these are different scoring regimes — BOS has a full investment_score (with congestion factored in), while BDL only has a demand_score (no congestion data available), so they aren't strictly apples-to-apples.

| Rank | Airport | Tier | Score | Congestion | Growth | Volume |
|------|---------|------|-------|------------|--------|--------|
| 1 | **BOS** – Boston Logan Intl | 1 (investment_score) | **70.8** | 64.0 | 76.9 | 72.0 |
| 2 | **BDL** – Bradley Intl (Hartford) | 2 (demand_score) | **54.1** | n/a | 73.7 | 14.8 |

**FAA NPIAS cross-check (2025-2029):**
- **BOS**: $906M planned development (82nd percentile among the 65 airports — high-priority capital need), and flagged as **capacity constrained by 2028**, worsening to **severe capacity constraints by 2033**. This reinforces BOS as the stronger expansion case — high growth/volume score plus an independent FAA signal of looming capacity crunch.
- **BDL**: $175M planned development (only 29th percentile), **not flagged** for capacity constraints in 2028 or 2033 — consistent with its much lower volume_norm (14.8) and no congestion pressure.

**Takeaway:** BOS is the clear top candidate — strong deterministic score (70.8) reinforced by FAA data showing severe forecasted capacity constraints and a large committed development budget, making a strong case for capacity-adding investment (terminal/gate/runway efficiency projects). BDL scores respectably on growth (73.7) but its low volume and lack of any flagged congestion suggest it's a lower-urgency, more demand-driven (not congestion-driven) opportunity — the FAA data doesn't show near-term capacity strain there.

**Caveat:** Only 2 New England airports are in our 65-airport scope, so this "ranking" is really just a two-way comparison — there's no broader regional field to rank against.

**Tool trace:** list_scope -> rank_airports -> get_npias -> get_npias


## [PASS] npias

**Q:** What does the FAA NPIAS say about SFO's development cost and capacity outlook?

- no_crash: True · tools_ok: True (saw ['get_npias', 'resolve_airport']) · substr_ok: True · steps: 3
- grounding SFO.dev_cost_percentile: [OK] expected one of ['78']

**Answer:**

## SFO — FAA NPIAS 2025–2029 Findings

**Development Cost:**
- 5-year planned development cost: **$683,792,071**
- This ranks at the **78th percentile** across the 65 airports in scope — i.e., SFO's planned investment is higher than roughly three-quarters of its peers.

**Runway Capacity Outlook:**
- **2028:** "Capacity constrained"
- **2033:** "Severe capacity constraints"

**Interpretation:** The FAA's independent capacity outlook shows a worsening trajectory — SFO is already constrained by 2028 and is projected to face severe constraints by 2033, despite a substantial (top-quartile) development spend already planned. This NPIAS data is separate from our deterministic investment_score for SFO; if you'd like, I can pull SFO's full score breakdown (congestion/growth/volume sub-scores) via `get_airport_score` to compare the two "second opinions" side by side.

**Tool trace:** resolve_airport -> get_npias


## [PASS] custom-weights

**Q:** If growth matters twice as much as congestion and volume is minor, who are the top 3 Tier-1 airports?

- no_crash: True · tools_ok: True (saw ['set_weights']) · substr_ok: True · steps: 2

**Answer:**

## Top 3 Tier-1 Airports (Growth weighted 2x Congestion, Volume Minor)

**Weights used:** Growth 57.1% | Congestion 28.6% | Volume 14.3%

| Rank | Airport | Custom Score | Growth | Congestion | Volume |
|------|---------|-------------|--------|------------|--------|
| 1 | **CLT** – Charlotte Douglas Intl | 82.1 | 89.6 | 67.7 | 81.2 |
| 2 | **LGA** – LaGuardia (New York) | 79.6 | 75.3 | 95.4 | 64.8 |
| 3 | **DFW** – Dallas/Fort Worth Intl | 77.3 | 81.6 | 60.8 | 93.4 |

**Read:** CLT tops the list on the strength of a high growth sub-score (89.6) even with only moderate congestion pressure — exactly what this weighting rewards. LGA stays competitive mainly via its very high congestion score (95.4), despite lower growth than CLT/DFW. DFW's strong growth and volume offset its comparatively low congestion score.

Note: these are Tier-1 airports, so all three have full investment_scores including a measured congestion dimension — the comparison is apples-to-apples. Let me know if you'd like the NPIAS development-cost/capacity outlook for any of these three as a second opinion, or want this saved as a standing preference.

**Tool trace:** set_weights


## [PASS] tier2-demand

**Q:** What is the demand score for Nashville?

- no_crash: True · tools_ok: True (saw ['get_airport_score', 'resolve_airport']) · substr_ok: True · steps: 3
- grounding BNA.demand_score: [OK] expected one of ['77.1']

**Answer:**

**Nashville International (BNA) — Demand Score: 77.1** (Tier 2)

Key underlying metrics:
- Growth CAGR: 10.36% → growth_norm 88.3
- Annual passengers (CY24): ~12.06M → volume_norm 54.8
- Long-haul share: 0.0%
- Hub classification: Large (L)

**Important caveat:** BNA is a **Tier 2** airport — it has no FAA capacity/congestion profile in our data, so this is a *demand_score*, not a full investment_score. It reflects growth and volume only, and is **not directly comparable** to Tier 1 airports' investment_scores, which also factor in congestion. If you want, I can pull NPIAS development-cost data for BNA as a secondary/qualitative check, or compare it against other Tier 2 airports in its region.

**Tool trace:** resolve_airport -> get_airport_score


## [PASS] messy-typo

**Q:** How congested is Chicagoo?

- no_crash: True · tools_ok: True (saw ['get_airport_score', 'resolve_airport']) · substr_ok: True · steps: 3
- grounding ORD.congestion_norm: [OK] expected one of ['71.4']

**Answer:**

**Chicago → O'Hare International (ORD)**, Tier 1, East North Central region.

**Congestion metrics (from our deterministic model):**
- Congestion sub-score: **71.4 / 100** (higher = more congested relative to declared capacity)
- Congestion ratio: **2,994** (annual ops relative to declared hourly capacity of 220 ops/hr)
- Annual operations: 657,133; Annual passengers (CY24): ~38.6M
- This feeds into an overall **investment_score of 76.0** (congestion 71.4, growth_norm 73.3, volume_norm 90.5)

**Important caveat:** The tool flags **staleness = true** — the congestion profile is based on a 2014-era declared capacity baseline. A note in the data states: *"New runway 9C/27C opened Nov 2020 plus reconfiguration; airfield capacity higher than 2014 profile."* This means the 71.4 congestion score likely **overstates current congestion**, since ORD's actual airfield capacity has increased since the baseline was set.

Would you like me to:
1. Pull the FAA NPIAS runway-capacity outlook for ORD (2028/2033) as a second opinion, and/or
2. Also check Chicago Midway (MDW), since "Chicago" could refer to either airport?

**Tool trace:** resolve_airport -> get_airport_score


## [PASS] descriptive

**Q:** What is the passenger growth of the main airport serving Silicon Valley?

- no_crash: True · tools_ok: True (saw ['get_airport_score', 'resolve_airport']) · substr_ok: True · steps: 4
- grounding SJC.growth_cagr_pct: [OK] expected one of ['1.45', '1.4']

**Answer:**

**Norman Y. Mineta San Jose International Airport (SJC)** — the main airport serving Silicon Valley — is our matched in-scope airport (note: my initial generic query for "the airport serving Silicon Valley" didn't resolve, but searching directly by name found it).

**Passenger growth data (Tier 2 — demand-side metrics only, no FAA congestion profile):**
- **Growth CAGR: 1.45%** (passenger growth compound annual growth rate)
- Growth sub-score (normalized): 47.6 / 100
- Annual passengers (CY2024): 5,822,019
- Annual operations: 104,106
- Overall demand_score: 42.5

**Important caveat:** SJC is a **Tier 2** airport in our dataset, meaning it has a demand_score built from growth, volume, and demand normalization — but **no FAA runway-capacity/congestion profile**, unlike Tier 1 airports. So while I can give you its growth rate confidently, it isn't directly comparable to a Tier 1 airport's full investment_score (which also weighs congestion).

Want me to pull NPIAS development-cost data for SJC, or compare its growth against other Bay Area/Pacific region airports (e.g., SFO, OAK) for context?

**Tool trace:** resolve_airport -> resolve_airport -> get_airport_score


## [PASS] out-of-scope

**Q:** How congested is Fresno?

- no_crash: True · tools_ok: True (saw ['resolve_airport']) · substr_ok: True · steps: 2

**Answer:**

Fresno Yosemite International Airport (FAT) is **out of scope** — it's not among the 65 airports in our deterministic dataset, so I have no computed congestion score, investment/demand score, or ranking for it.

I can search the web for qualitative external context if you'd like (e.g., recent news on delays or capacity), but that would be general information — not comparable to our scored airports, and I won't fabricate a score for it.

Would you like me to run that web search, or would you like a comparison using a similarly-sized in-scope airport instead?

**Tool trace:** resolve_airport


## [PASS] compositional

**Q:** Which Tier-1 airports does the FAA flag as capacity-constrained by 2033 while our congestion score is under 65? Rank those by growth.

- no_crash: True · tools_ok: True (saw ['get_npias', 'list_scope', 'rank_airports']) · substr_ok: True · steps: 4

**Answer:**

## Tier‑1 Airports: FAA-Flagged Capacity-Constrained by 2033 AND Congestion Score < 65

**Method:** Started from all 33 Tier‑1 airports, pulled each `congestion_norm` from the deterministic ranking, kept those <65, then checked FAA NPIAS `capacity_2033` outlook for each. Any 2033 status other than "not flagged" (i.e., "congested," "capacity constrained," or "severe capacity constraints") counts as FAA-flagged. Final list ranked by `growth_norm`.

| Rank | Airport | Congestion Score | FAA 2033 Outlook | Growth Score |
|---|---|---|---|---|
| 1 | **PHL** – Philadelphia | 46.4 | congested | **87.0** |
| 2 | **IAD** – Washington Dulles | 18.2 | congested | **84.6** |
| 3 | **DFW** – Dallas/Fort Worth | 60.8 | congested | **81.6** |
| 4 | **DEN** – Denver | 51.8 | congested | **79.2** |
| 5 | **BOS** – Boston Logan | 64.0 | severe capacity constraints | **76.9** |
| 6 | **SFO** – San Francisco | 61.4 | severe capacity constraints | **69.8** |
| 7 | **FLL** – Fort Lauderdale | 57.3 | congested | **66.0** |
| 8 | **MDW** – Chicago Midway | 47.3 | congested | **58.2** |
| 9 | **LAX** – Los Angeles | 55.0 | capacity constrained | **57.4** |
| 10 | **MIA** – Miami | 33.9 | capacity constrained | **53.3** |
| 11 | **SNA** – John Wayne (Orange County) | 32.7 | congested | **33.2** |

**Key takeaway:** These 11 airports represent a mismatch pattern worth flagging to investors — our congestion sub-score (a normalized, relative measure) rates them as only moderately congested today, but the FAA's independent NPIAS outlook already sees them hitting capacity limits by 2033. This is exactly the kind of gap an infrastructure investor would want to front-run: growth is strong (PHL 87.0, IAD 84.6, DFW 81.6, DEN 79.2 lead) while our own congestion metric hasn't yet caught up to the FAA's forward-looking capacity call — suggesting these could be underpriced relative to future bottleneck risk.

**Caveats:**
- BOS and SFO stand out as the most severe (FAA says "severe capacity constraints" by 2033) despite congestion scores in the low-60s — the largest score/outlook divergence in the set.
- IAD has the lowest congestion score (18.2) of any airport on this list yet is still FAA-flagged as "congested" by 2033 — likely reflects runway/terminal capacity limits not fully captured in the congestion sub-score's current-year framing.
- This ranking is by growth only, not overall investment score — CLT, ATL, LGA, SEA, SAN, ORD, PHX, LAS, BWI were excluded solely because their congestion scores are already ≥65 (i.e., already flagged as congested today), not because they lack 2033 risk.
- FAA capacity outlook and our congestion score are two independent sources by design (per your standing methodology) — I did not let one adjust the other, only used the FAA read as a qualitative/independent filter.

Want me to pull NPIAS development-cost percentiles for these 11 as a rough proxy for capital intensity, or re-run with custom weights emphasizing growth over congestion for a blended investment view?

**Tool trace:** list_scope -> rank_airports -> get_npias -> get_npias -> get_npias -> get_npias -> get_npias -> get_npias -> get_npias -> get_npias -> get_npias -> get_npias -> get_npias -> get_npias -> get_npias -> get_npias -> get_npias -> get_npias -> get_npias -> get_npias -> get_npias -> get_npias -> get_npias
