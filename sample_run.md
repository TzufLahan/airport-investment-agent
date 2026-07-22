# Sample run - Airport Investment Intelligence Agent

Mode: **Claude (LLM edges)**


## A. Assignment questions

**Q:** Which airports in New England are strong candidates for terminal expansion?

# New England Terminal Expansion Candidates

## Top Ranking

**Boston Logan International (BOS)** is the strongest candidate for terminal expansion in New England.

| Metric | Sub-Score | Weight | Contribution |
|--------|-----------|--------|--------------|
| Congestion | 64.0 | 0.4 | 25.6 |
| Growth | 76.9 | 0.4 | 30.8 |
| Volume | 72.0 | 0.2 | 14.4 |
| **Investment Score** | — | — | **70.8** |

BOS shows strong fundamentals across all dimensions: moderate-to-high congestion (64.0), robust growth trajectory (76.9), and substantial passenger volume (72.0). The growth signal is particularly compelling for terminal investment planning.

---

## Secondary Candidate

**Bradley International—Hartford (BDL)** ranks second at 54.1, but with important caveats.

| Metric | Sub-Score | Weight | Contribution |
|--------|-----------|--------|--------------|
| Growth | 73.7 | 0.667 | 49.2 |
| Volume | 14.8 | 0.333 | 4.9 |
| **Demand Score** | — | — | **54.1** |

⚠️ **Limitation:** BDL is Tier 2 (no FAA capacity profile). Its score reflects demand signals only—growth momentum is solid (73.7), but absolute volume is low (14.8). Congestion is unmeasured and not comparable to BOS. Terminal expansion viability depends on demand validation beyond this metric.

---

## Summary

**BOS is the clear priority.** It combines elevated congestion, strong growth, and high volume—the full investment case. **BDL merits secondary consideration** if demand forecasts justify it, but its low volume and lack of capacity data require deeper due diligence.

---

### 🏛️ FAA NPIAS -- independent second opinion

**Boston Logan International (BOS)** — FAA pegs development need at $906.3M (82nd percentile), with capacity constrained by 2028 and worsening to severe constraints by 2033; this trajectory reinforces the team's already-elevated congestion score, making BOS a well-supported case for terminal expansion.

**Bradley International (BDL)** — FAA development cost sits at $175.0M (29th percentile), and the capacity outlook is not flagged for either 2028 or 2033; since BDL is a Tier-2 airport, the team's score carries no congestion metric here, so this simply means BDL isn't on the FAA's constrained radar, not that terminal capacity is confirmed adequate.

_Source: FAA NPIAS 2025-2029 (Appendix A development costs; Narrative Figure 1 capacity outlook). This view sits beside the deterministic score and never changes it. "Not flagged" means an airport is not on the FAA's constrained list -- not proof it is unconstrained (small hubs may not have been evaluated)._

---

**Q:** Compare LA and Santa Ana airport congestion levels.

# Congestion Comparison: LAX vs. Santa Ana (SNA)

## Congestion Metrics

| Airport | IATA | Congestion Ratio | Declared Capacity (ops/hr) | Congestion Norm (0–100) |
|---------|------|------------------|----------------------------|-------------------------|
| Los Angeles International | LAX | 2412.0 | 172.0 | 55.0 |
| John Wayne-Orange County | SNA | 1623.0 | 58.0 | 32.7 |

**LAX is significantly more congested than Santa Ana.** LAX's congestion ratio of 2412.0 annual operations per declared hourly slot is 48% higher than SNA's 1623.0. On the normalized 0–100 scale, LAX scores 55.0 versus SNA's 32.7.

## Context

- **LAX** handles 37.76 million annual passengers (CY 2024) with 413,641 annual operations across a 172-slot declared capacity.  
- **SNA** handles 5.37 million annual passengers with 94,965 annual operations across a 58-slot capacity.

**Important caveat:** SNA operates under a Community Settlement Agreement (amended 2003) that caps commercial operations and passengers below its runway capacity. The practical commercial limit is therefore lower than the declared 58 ops/hr, making the raw ratio less directly comparable to LAX's unconstrained operations. This regulatory ceiling means SNA's congestion is artificially suppressed—expansion there faces legal and community constraints beyond typical operational measures.

---

### 🏛️ FAA NPIAS -- independent second opinion

**Los Angeles International (LAX)** — FAA development need sits at $572.7M (69th percentile), with the runway outlook showing capacity constrained status in both 2028 and 2033, reinforcing the team's already-high congestion read at 62.9 (congestion norm 55.0) — the outlook and score are pointing the same direction.

**John Wayne-Orange County (SNA)** — FAA development need is $114.8M (15th percentile), and the outlook flags it as congested (not the more severe capacity-constrained tier) in both 2028 and 2033; this watch-level signal lines up reasonably well with the team's moderate score of 32.3 (congestion norm 32.7), though "congested" should be read as a caution flag rather than confirmation the airport is unconstrained.

_Source: FAA NPIAS 2025-2029 (Appendix A development costs; Narrative Figure 1 capacity outlook). This view sits beside the deterministic score and never changes it. "Not flagged" means an airport is not on the FAA's constrained list -- not proof it is unconstrained (small hubs may not have been evaluated)._

---

**Q:** What is the percentage of long-haul flights out of Anchorage airport?

# Long-Haul Share at Ted Stevens Anchorage International (ANC)

**5.0%** of departing domestic passengers at Anchorage are on long-haul markets (over 3,000 miles).

## Context

- **Airport:** Ted Stevens Anchorage International (ANC) – Tier 2, Pacific region
- **Annual passengers (CY24):** 2,767,856
- **Note:** Long-haul share is calculated from *domestic* passenger departures only; international traffic is excluded.

Anchorage is a major cargo hub with diverse operations; the relatively low long-haul domestic share reflects its role serving Alaska intrastate and regional markets alongside significant cargo activity.

---

### 🏛️ FAA NPIAS -- independent second opinion

**Ted Stevens Anchorage International (ANC)** — FAA development need sits at $319.0M (55th percentile), with no capacity constraint flagged for either 2028 or 2033. As a Tier-2 airport, the team's score has no congestion component to compare against, so this quiet FAA capacity outlook doesn't corroborate or contradict anything—it simply confirms there's no flagged runway pressure through the forecast window, though this isn't proof the airport is free of other issues.

_Source: FAA NPIAS 2025-2029 (Appendix A development costs; Narrative Figure 1 capacity outlook). This view sits beside the deterministic score and never changes it. "Not flagged" means an airport is not on the FAA's constrained list -- not proof it is unconstrained (small hubs may not have been evaluated)._

---

**Q:** What is the unmet flight demand in SFO airport and why?

# Unmet Flight Demand at SFO

## Summary
SFO exhibits **significant unmet demand**, evidenced by a high congestion ratio and strong growth trajectory. The airport is operationally constrained relative to passenger volume and growth trends.

## Key Indicators

| Metric | Value | Interpretation |
|--------|-------|-----------------|
| **Congestion Ratio** | 2,639.0 ops/slot | Annual operations are 2,639× the declared hourly capacity (105 ops/hr), indicating severe scheduling compression |
| **Annual Operations** | 277,099 | High absolute volume on constrained infrastructure |
| **Growth CAGR** | 6.3% | Strong year-over-year expansion |
| **Annual Passengers (CY24)** | 25,078,968 | Major hub-level traffic |

## Why Unmet Demand Exists

**Capacity Constraint:** SFO's declared capacity of 105 operations per hour cannot accommodate the 277,099 annual operations, forcing extensive slot rationing. The 2,639 congestion ratio—among the highest for US airports—reflects demand far exceeding declared hourly throughput.

**Growth Pressure:** At 6.3% CAGR, passenger and flight demand is expanding faster than infrastructure can absorb. The growth normalization score of 69.8 (out of 100) confirms this is a material growth driver.

**Structural Mismatch:** The airport serves a major metropolitan area with strong domestic and international connectivity needs, yet physical runway and terminal constraints limit frequency expansion.

## Investment Signal

SFO's **investment_score of 67.9** reflects this tension:

| Component | Sub-Score | Weight | Contribution |
|-----------|-----------|--------|--------------|
| Congestion | 61.4 | 0.4 | 24.6 |
| Growth | 69.8 | 0.4 | 27.9 |
| Volume | 77.3 | 0.2 | 15.5 |
| **Total** | — | — | **67.9** |

Both congestion and growth are material drivers of investment opportunity, signaling that demand-supply misalignment is acute.

**Limitation:** Declared capacity (105 ops/hr) is from FAA data; actual operational practices may differ. The 2014 baseline has no staleness flag for SFO, so this estimate is current.

---

### 🏛️ FAA NPIAS -- independent second opinion

**San Francisco International (SFO)** FAA development-need is pegged at $683.8M, in the 78th percentile nationally, with a capacity outlook moving from constrained in 2028 to severe constraints by 2033. This trajectory corroborates the team's already-elevated congestion score (61.4), reinforcing that SFO's capacity pressure is a well-supported, worsening structural issue rather than a modeling artifact.

_Source: FAA NPIAS 2025-2029 (Appendix A development costs; Narrative Figure 1 capacity outlook). This view sits beside the deterministic score and never changes it. "Not flagged" means an airport is not on the FAA's constrained list -- not proof it is unconstrained (small hubs may not have been evaluated)._

---


## B. Single metrics

**Q:** How congested is JFK?

# JFK Congestion Assessment

**JFK is moderately congested** with a congestion ratio of **2886.0** — meaning the airport handles approximately 2,886 annual operations per declared hourly runway slot.

For context:
- **Declared capacity:** 88.0 operations/hour
- **Annual operations:** 255,441
- **Congestion normalized score (0–100):** 68.4

This normalized score of 68.4 reflects JFK's position in the middle-to-upper range of US airport congestion. The airport is a major international hub with substantial traffic, but it is not at the extreme congestion levels of the most constrained US facilities.

## Investment Score Breakdown

JFK's overall investment score of **60.3** incorporates congestion alongside growth and volume factors:

| Metric | Sub-score | Weight | Contribution |
|--------|-----------|--------|--------------|
| Congestion | 68.4 | 0.4 | 27.4 |
| Growth (CAGR) | 40.1 | 0.4 | 16.0 |
| Volume | 84.3 | 0.2 | 16.9 |
| **Total** | | | **60.3** |

**Key observations:**
- JFK's congestion score is its strongest component (27.4 contribution).
- Growth is modest (−0.18% CAGR), pulling the investment score down.
- Long-haul international traffic (1.1% of annual passengers) reflects its role as a major gateway.

---

### 🏛️ FAA NPIAS -- independent second opinion

**John F. Kennedy International (JFK)** – FAA five-year development-need is pegged at $257.3M (49th percentile), and the runway-capacity outlook moves from "capacity constrained" in 2028 to "severe capacity constraints" by 2033. This trajectory corroborates the team's own congestion read (67th percentile in their model), reinforcing that JFK's tight capacity is a well-flagged, worsening issue rather than a one-off metric quirk.

_Source: FAA NPIAS 2025-2029 (Appendix A development costs; Narrative Figure 1 capacity outlook). This view sits beside the deterministic score and never changes it. "Not flagged" means an airport is not on the FAA's constrained list -- not proof it is unconstrained (small hubs may not have been evaluated)._

---

**Q:** What is the passenger growth at Nashville?

# Passenger Growth at Nashville International (BNA)

**Growth Rate (CAGR):** 10.36%

Nashville International is experiencing strong passenger growth at a compound annual growth rate of **10.36%**, with current annual passengers at **12,058,688** (CY24).

## Demand Score Breakdown

Since Nashville is a **Tier 2 airport**, it has no FAA capacity profile. The demand score reflects growth and volume only—congestion is not measured.

| Metric | Sub-Score | Weight | Contribution |
|--------|-----------|--------|--------------|
| Growth | 88.3 | 0.667 | 58.9 |
| Volume | 54.8 | 0.333 | 18.2 |
| **Demand Score** | — | — | **77.1** |

The high growth sub-score (88.3) reflects BNA's above-average expansion trajectory, positioning it as a strong growth market among US airports.

## Confidence & Limitations

- **Tier 2 status:** No FAA capacity profile means demand and growth are observable, but **congestion is not measured** and scores are **not directly comparable to Tier 1 airports**.
- **Staleness:** Data is current (no staleness flag).
- **Long-haul share:** 0.0% (domestic-passenger-based metric).

---

### 🏛️ FAA NPIAS -- independent second opinion

**Nashville International (BNA)** — FAA data show a $1.39B five-year development-need estimate, placing it in the 91st percentile nationally, with capacity outlooks for both 2028 and 2033 not flagged as constrained; since BNA is a Tier-2 airport, the team's model carries no congestion metric here, so this FAA data point simply fills that gap rather than confirming or conflicting with the team's 77.1 score — the high investment percentile signals substantial planned capital work, but "not flagged" should not be read as a clean bill of health on future capacity.

_Source: FAA NPIAS 2025-2029 (Appendix A development costs; Narrative Figure 1 capacity outlook). This view sits beside the deterministic score and never changes it. "Not flagged" means an airport is not on the FAA's constrained list -- not proof it is unconstrained (small hubs may not have been evaluated)._

---

**Q:** How many passengers does Denver handle?

## Denver International (DEN) – Passenger Volume

**Denver handled 40,012,895 passengers in calendar year 2024.**

### Context

- **Growth trajectory:** Denver is expanding at a 8.37% compound annual growth rate (CAGR), positioning it among faster-growing major US airports.
- **Hub status:** Large hub (L), reflecting its role as a major connecting point.
- **Tier 1 airport:** Full capacity and demand data available; comparable to other major US airports.

### Investment Score Breakdown

Denver's **investment_score of 70.7** combines three metrics:

| Metric | Sub-Score (0–100) | Weight | Contribution |
|--------|---|--------|---|
| Congestion | 51.8 | 0.4 | 20.7 |
| Growth | 79.2 | 0.4 | 31.7 |
| Volume | 91.6 | 0.2 | 18.3 |
| **Total** | — | — | **70.7** |

The relatively modest investment score (despite high growth and volume) reflects moderate congestion (2,300 annual ops per declared hourly slot), suggesting headroom remains before expansion becomes urgent on pure congestion grounds. However, strong growth momentum is a positive indicator for long-term demand.

---

### 🏛️ FAA NPIAS -- independent second opinion

**Denver International (DEN)** — FAA earmarks $1.06B in development need, the 88th percentile nationally, and flags the airport as congested in both the 2028 and 2033 outlook. That sustained congestion signal aligns with the team's moderate congestion score of 51.8, corroborating rather than contradicting the internal assessment, though it's worth noting "congested" here is a watch-level designation, not confirmation of a hard capacity bottleneck.

_Source: FAA NPIAS 2025-2029 (Appendix A development costs; Narrative Figure 1 capacity outlook). This view sits beside the deterministic score and never changes it. "Not flagged" means an airport is not on the FAA's constrained list -- not proof it is unconstrained (small hubs may not have been evaluated)._

---

**Q:** What share of flights out of Honolulu are long-haul?

# Long-Haul Share at Honolulu (HNL)

**13.6%** of flights out of Honolulu are long-haul.

This represents the share of departing domestic passengers on markets over 3,000 miles. Note that international traffic is excluded from this metric.

---

### 🏛️ FAA NPIAS -- independent second opinion

**Daniel K. Inouye International (HNL)** — The FAA pegs a five-year development need of $582.2M, placing HNL at the 71st percentile nationally, yet its capacity outlook is not flagged for either 2028 or 2033. This absence of a forward capacity constraint aligns with the team's own congestion score of 26.8, which is comparatively modest and contributes to the overall score of 43.9 — both signals point in the same quiet direction, though "not flagged" simply means HNL isn't on the FAA's constrained list, not that future capacity pressure is ruled out.

_Source: FAA NPIAS 2025-2029 (Appendix A development costs; Narrative Figure 1 capacity outlook). This view sits beside the deterministic score and never changes it. "Not flagged" means an airport is not on the FAA's constrained list -- not proof it is unconstrained (small hubs may not have been evaluated)._

---


## C. Ranking (overall and by region)

**Q:** Which airports are the best expansion candidates overall?

# Best Expansion Candidates Overall

Based on investment scores, the top candidates rank as follows:

## **Tier 1 Airports** (Congestion + Growth + Volume measured)

| Rank | Airport | Score | Congestion | Growth | Volume |
|------|---------|-------|-----------|--------|--------|
| 1 | **LGA** (LaGuardia, NY) | **81.3** | 95.4 (38.2) | 75.3 (30.1) | 64.8 (13.0) |
| 2 | **CLT** (Charlotte Douglas, NC) | **79.2** | 67.7 (27.1) | 89.6 (35.8) | 81.2 (16.2) |
| 3 | **SEA** (Seattle-Tacoma, WA) | **77.3** | 88.8 (35.5) | 65.7 (26.3) | 77.7 (15.5) |
| 4 | **ATL** (Hartsfield-Jackson, GA) | **77.1** | 75.1 (30.0) | 67.6 (27.0) | 100.0 (20.0) |
| 5 | **SAN** (San Diego, CA) | **76.6** | 92.1 (36.8) | 71.2 (28.5) | 56.5 (11.3) |
| 6 | **DCA** (Reagan National, DC) | **76.1** | 100.0 (40.0) | 62.0 (24.8) | 56.5 (11.3) |

**LGA leads decisively** with exceptional congestion (95.4) and solid growth momentum. **CLT is the strongest growth story**, combining the highest growth score (89.6) with substantial volume (81.2). **DCA is maximally congested** (100.0) but shows weaker growth, signaling capacity constraints without robust demand expansion.

---

## **Tier 2 Airports** (Growth + Volume only; no FAA capacity data)

| Rank | Airport | Score | Growth | Volume |
|------|---------|-------|--------|--------|
| 1 | **RDU** (Raleigh-Durham, NC) | **80.2** | 100.0 (66.7) | 40.5 (13.5) |
| 2 | **BNA** (Nashville, TN) | **77.1** | 88.3 (58.9) | 54.8 (18.2) |
| 3 | **SJU** (San Juan, PR) | **73.8** | 92.8 (61.9) | 35.7 (11.9) |
| 4 | **PBI** (Palm Beach

---

### 🏛️ FAA NPIAS -- independent second opinion

**LaGuardia (LGA)** FAA pegs development need at $110.1M (14th percentile) while the capacity outlook stays capacity constrained through both 2028 and 2033 — this squarely corroborates the team's already-high congestion reading, confirming LGA's constraint is a durable structural issue rather than a scoring artifact.

**Charlotte Douglas International (CLT)** FAA development need is $1.03B (85th percentile), with the capacity outlook moving from not flagged in 2028 to congested by 2033; this is softer than the team's own congestion score suggests, meaning the team may be more concerned about near-term crowding than FAA's forward projections currently support.

**Seattle-Tacoma International (SEA)** FAA development need sits at $539.2M (68th percentile), and the capacity outlook worsens from capacity constrained in 2028 to severe capacity constraints by 2033 — a strong corroboration of the team's high congestion score and a signal that the constraint is intensifying, not static.

**Raleigh-Durham International (RDU)** carries a $384.6M FAA development need (62nd percentile), but as a Tier-2 airport it has no FAA capacity flag in either 2028 or 2033, so this fills a gap the team's score couldn't measure directly — the FAA view is quiet, but that reflects absence of a congestion metric rather than a clean bill of health.

**Nashville International (BNA)** shows the largest FAA development need in the set at $1.39B (91st percentile), yet again with no capacity constraint flagged for 2028 or 2033; the size of the investment figure stands out even though FAA's forward-looking capacity l

_Source: FAA NPIAS 2025-2029 (Appendix A development costs; Narrative Figure 1 capacity outlook). This view sits beside the deterministic score and never changes it. "Not flagged" means an airport is not on the FAA's constrained list -- not proof it is unconstrained (small hubs may not have been evaluated)._

---

**Q:** Which Mountain region airports are the best candidates?

# Mountain Region Airport Candidates

## Top-Ranked Airports (Tier 1 – with FAA capacity data)

**1. Phoenix Sky Harbor International (PHX) – Score: 74.2**

| Metric | Sub-Score | Weight | Contribution |
|--------|-----------|--------|--------------|
| Congestion | 70.1 | 0.4 | 28.0 |
| Growth | 76.4 | 0.4 | 30.6 |
| Volume | 77.9 | 0.2 | 15.6 |
| **Total** | | | **74.2** |

PHX is the strongest candidate, driven by robust growth (76.4) and high passenger volume (77.9), paired with meaningful congestion pressure (70.1) signaling capacity constraints that expansion could relieve.

---

**2. Harry Reid International, Las Vegas (LAS) – Score: 72.2**

| Metric | Sub-Score | Weight | Contribution |
|--------|-----------|--------|--------------|
| Congestion | 78.4 | 0.4 | 31.4 |
| Growth | 61.7 | 0.4 | 24.7 |
| Volume | 80.9 | 0.2 | 16.2 |
| **Total** | | | **72.2** |

LAS ranks second with the *highest congestion score (78.4)* among Mountain airports, indicating near-term capacity strain. High volume (80.9) supports the case for expansion, though growth trails PHX.

---

**3. Denver International (DEN) – Score: 70.7**

| Metric | Sub-Score | Weight | Contribution |
|--------|-----------|--------|--------------|
| Congestion | 51.8 | 0.4 | 20.7 |
| Growth | 79.2 | 0.4 | 31.7 |
| Volume | 91.6 | 0.2 | 18.3 |
| **Total** | | | **70.7** |

DEN shows *highest volume (91.6)* and *highest growth (79.2)* in the region, but lower congestion (51.8) suggests current capacity is managing demand. Strong fundamentals, but immediate expansion urgency is lower than PHX/LAS.

---

**4. Salt Lake City International (SLC) – Score: 48.7**

| Metric | Sub-Score | Weight | Contribution |
|--------|-----------|--------|--------------|
| Congestion | 31.7 | 0.4 | 12.7 |
| Growth | 60.8 | 0.4 | 24.3 |
| Volume | 58.3 | 0.2 | 11.7 |
| **Total** | | | **48.7** |

SLC lags meaningfully

---

### 🏛️ FAA NPIAS -- independent second opinion

**PHX (Phoenix Sky Harbor International)** FAA pegs development need at $203.4M (37th percentile) with a capacity outlook of congested->congested through 2033. The FAA view is more measured than the team's score, which reads hotter on congestion than a hard capacity constraint would suggest — worth reconciling before treating PHX as a top-tier bottleneck case.

**LAS (Harry Reid International)** FAA development need sits at $135.8M (22nd percentile), but the capacity trajectory is the standout: capacity constrained in 2028 sliding to severe capacity constraints by 2033. That forward path corroborates the team's already-elevated congestion score, reinforcing LAS as a genuine capacity-risk candidate despite the relatively modest spend percentile.

**DEN (Denver International)** carries by far the largest development need at $1.06B (88th percentile), with a steady congested->congested outlook through 2033. This is a watch-level signal rather than a hard constraint, and it lines up reasonably with the team's moderate congestion score — the capital need is large, but the FAA isn't yet calling it capacity-constrained.

**ABQ (Albuquerque International Sunport)** As a Tier-2 field the team has no congestion figure to work with; FAA shows a modest $50.4M need (6th percentile) and no capacity flags in either 2028 or 2033, filling that gap with a quiet signal rather than confirmation of adequacy.

**BOI (Boise Airport/Gowen Field)** Similarly untracked for congestion by the team, FAA data shows an $87.7M need (9th percentile) and no capacity constraints fl

_Source: FAA NPIAS 2025-2029 (Appendix A development costs; Narrative Figure 1 capacity outlook). This view sits beside the deterministic score and never changes it. "Not flagged" means an airport is not on the FAA's constrained list -- not proof it is unconstrained (small hubs may not have been evaluated)._

---

**Q:** Rank the New England airports.

# New England Airports Ranking

## Tier 1

**1. Boston Logan International (BOS) – Score: 70.8**

| Metric | Sub-Score | Weight | Contribution |
|--------|-----------|--------|--------------|
| Congestion | 64.0 | 0.4 | 25.6 |
| Growth | 76.9 | 0.4 | 30.8 |
| Volume | 72.0 | 0.2 | 14.4 |
| **Total** | | | **70.8** |

Formula: 0.4×congestion + 0.4×growth + 0.2×volume

Boston Logan leads the region with balanced strength across all dimensions. Growth (76.9) is the strongest component, followed by volume (72.0), while congestion (64.0) reflects moderate operational pressure.

---

## Tier 2

**2. Bradley International—Hartford (BDL) – Score: 54.1**

| Metric | Sub-Score | Weight | Contribution |
|--------|-----------|--------|--------------|
| Growth | 73.7 | 0.667 | 49.2 |
| Volume | 14.8 | 0.333 | 4.9 |
| **Total** | | | **54.1** |

Formula: (0.4×growth + 0.2×volume) / 0.6 [congestion excluded: no FAA capacity profile]

Bradley shows strong growth (73.7) but significantly lower volume (14.8). **Important:** As a Tier 2 airport, BDL has no FAA capacity data, so congestion is unmeasured and its score is not directly comparable to BOS. The ranking reflects demand signal only.

---

## Key Limitation

Tier 2 airports lack FAA hourly runway slot declarations, making congestion assessment impossible and their scores incomparable to Tier 1 facilities on a congestion basis.

---

### 🏛️ FAA NPIAS -- independent second opinion

**Boston Logan International (BOS)** — FAA pegs development need at $906.3M (82nd percentile), with the runway outlook worsening from capacity constrained in 2028 to severe capacity constraints by 2033; this trajectory corroborates the team's already-elevated congestion norm of 64.0, reinforcing that Logan's high score is well-founded and likely to intensify.

**Bradley International (BDL)** — FAA development need sits at $175.0M (29th percentile), and the capacity outlook is not flagged for either 2028 or 2033. As a Tier-2 airport the team's score carries no congestion measure here, so this simply fills that gap with a quiet signal rather than confirming the airport is problem-free.

_Source: FAA NPIAS 2025-2029 (Appendix A development costs; Narrative Figure 1 capacity outlook). This view sits beside the deterministic score and never changes it. "Not flagged" means an airport is not on the FAA's constrained list -- not proof it is unconstrained (small hubs may not have been evaluated)._

---


## D. Comparisons (same-tier, cross-tier, multi-airport metros)

**Q:** Compare Denver and Salt Lake City.

# Denver vs. Salt Lake City: Investment Profile Comparison

Both airports are **Tier 1** Mountain-region facilities with large hub operations, but **Denver substantially outperforms Salt Lake City** on investment metrics and demand signals.

## Key Metrics Summary

| Metric | Denver (DEN) | Salt Lake City (SLC) |
|--------|--------------|---------------------|
| **CY24 Passengers** | 40.0M | 13.5M |
| **Annual Operations** | 643,935 | 237,051 |
| **Growth CAGR** | 8.37% | 4.35% |
| **Long-haul Share** | 1.1% | 0.0% |
| **Investment Score** | **70.7** | **48.7** |
| **Demand Score** | **83.4** | **60.0** |

## Investment Score Breakdown

**Denver (70.7):**

| Metric | Sub-score | Weight | Contribution |
|--------|-----------|--------|--------------|
| Congestion | 51.8 | 0.4 | 20.7 |
| Growth | 79.2 | 0.4 | 31.7 |
| Volume | 91.6 | 0.2 | 18.3 |
| **Total** | — | — | **70.7** |

**Salt Lake City (48.7):**

| Metric | Sub-score | Weight | Contribution |
|--------|-----------|--------|--------------|
| Congestion | 31.7 | 0.4 | 12.7 |
| Growth | 60.8 | 0.4 | 24.3 |
| Volume | 58.3 | 0.2 | 11.7 |
| **Total** | — | — | **48.7** |

## Key Differences

- **Demand:** Denver's demand score (83.4) reflects nearly 3× the passenger volume (40M vs. 13.5M), stronger growth momentum (8.37% vs. 4.35%), and measurable long-haul connectivity (1.1% of domestic passengers). Salt Lake City shows only domestic traffic (0.0% long-haul share).

- **Congestion:** Denver operates at a higher congestion ratio (2,300 ops per runway slot-hour vs. 1,591), signaling tighter capacity utilization and urgency for expansion; Salt Lake City has more slack capacity.

- **Growth Contribution:** Denver's 79.2 growth sub-score drives 31.7 points of its investment score; Salt Lake City's 60.8 contributes only 24.3 points—a significant gap reflecting Denver's trajectory.

## Investment Recommendation Signal

**Denver is the stronger investment candidate** on this data: higher absolute demand, faster growth, and more acute congestion pressure. Salt Lake City presents a secondary-tier opportunity with lower near-term urgency but

---

### 🏛️ FAA NPIAS -- independent second opinion

**Denver International (DEN)** – FAA pegs a five-year development need of $1.06B (88th percentile) with a capacity outlook of congested in both 2028 and 2033; this watch-level congestion signal aligns reasonably well with the team's moderate congestion score of 51.8, corroborating rather than contradicting the internal read.

**Salt Lake City International (SLC)** – FAA development need is much lower at $173.6M (28th percentile), and the capacity outlook is not flagged for either 2028 or 2033, consistent with the team's lower congestion score of 31.7; both signals point to a quieter capacity picture, though the absence of a flag confirms no current constraint rather than proving future headroom.

_Source: FAA NPIAS 2025-2029 (Appendix A development costs; Narrative Figure 1 capacity outlook). This view sits beside the deterministic score and never changes it. "Not flagged" means an airport is not on the FAA's constrained list -- not proof it is unconstrained (small hubs may not have been evaluated)._

---

**Q:** Compare Boston and Bradley.

## Boston vs. Bradley: Investment Comparison

### Volume & Demand
**Boston Logan (BOS)** is substantially larger, handling **21.1M passengers** annually versus Bradley's **3.3M**—a 6.4× difference. Both airports show similar growth momentum (**BOS: 7.87% CAGR; BDL: 7.17% CAGR**), but Boston's long-haul presence (0.3% of domestic passengers) gives it greater network diversity; Bradley has no measurable long-haul traffic.

---

### Investment & Congestion Scores

| **Metric** | **BOS** | **BDL** |
|---|---|---|
| **Investment Score** | 70.8 | 54.1 |
| **Demand Score** | 75.3 | 54.1 |

**Boston's score breakdown** (Tier 1 formula: 0.4×congestion + 0.4×growth + 0.2×volume):

| Component | Sub-Score | Weight | Contribution |
|---|---|---|---|
| Congestion | 64.0 | 0.4 | 25.6 |
| Growth | 76.9 | 0.4 | 30.8 |
| Volume | 72.0 | 0.2 | 14.4 |
| **Total** | — | — | **70.8** |

**Bradley's score breakdown** (Tier 2 formula: (0.4×growth + 0.2×volume) / 0.6; no FAA capacity):

| Component | Sub-Score | Weight | Contribution |
|---|---|---|---|
| Growth | 73.7 | 0.667 | 49.2 |
| Volume | 14.8 | 0.333 | 4.9 |
| **Total** | — | — | **54.1** |

---

### Key Difference
Boston operates at **2,730 annual ops per declared hourly slot** (congestion_ratio), indicating measurable capacity stress. Bradley has no FAA capacity profile, so congestion cannot be assessed—its score reflects demand signals (growth and volume) only. **The 16.7-point gap reflects Boston's larger scale, higher volume normalization, and quantified congestion.**

### Investment Implication
Boston presents both stronger demand signals and documented capacity constraints, making it a clearer expansion candidate if capacity relief is the goal. Bradley's smaller footprint and lack of capacity data limit direct comparability but signal room for organic growth without immediate infrastructure pressure.

---

### 🏛️ FAA NPIAS -- independent second opinion

**Boston Logan International (BOS)** — FAA pegs development need at $906.3M (82nd percentile), with a capacity outlook that moves from constrained in 2028 to severe constraints by 2033; this trajectory reinforces the team's already-elevated congestion score, confirming Boston as a genuine, worsening bottleneck rather than a modeling artifact.

**Bradley International (BDL)** — FAA development need is $175.0M (29th percentile), and it carries no capacity-constraint flag in either 2028 or 2033. Since Bradley is a Tier-2 airport the team's score had no congestion metric to draw on, and the FAA data here fills that gap quietly rather than raising a concern — absence of a flag isn't proof of adequate capacity, just an absence of documented strain.

_Source: FAA NPIAS 2025-2029 (Appendix A development costs; Narrative Figure 1 capacity outlook). This view sits beside the deterministic score and never changes it. "Not flagged" means an airport is not on the FAA's constrained list -- not proof it is unconstrained (small hubs may not have been evaluated)._

---

**Q:** Compare Nashville and Austin.

# Nashville vs. Austin: Demand Score Comparison

Both are Tier 2 airports without FAA capacity profiles, so scores reflect **demand/growth/volume signals only**—congestion is not measured.

## Demand Scores

| Airport | Score | Growth CAGR | Annual Passengers (CY24) | Annual Ops |
|---------|-------|-------------|--------------------------|------------|
| **Nashville (BNA)** | **77.1** | 10.36% | 12,058,688 | 208,149 |
| **Austin (AUS)** | **47.7** | 1.11% | 10,678,073 | 179,873 |

Nashville's **demand_score of 77.1 significantly exceeds Austin's 47.7**—a 29.4-point gap.

### Score Breakdown

**Nashville (BNA):**

| Metric | Sub-Score | Weight | Contribution |
|--------|-----------|--------|--------------|
| Growth | 88.3 | 0.667 | 58.9 |
| Volume | 54.8 | 0.333 | 18.2 |
| **Total** | — | — | **77.1** |

**Austin (AUS):**

| Metric | Sub-Score | Weight | Contribution |
|--------|-----------|--------|--------------|
| Growth | 46.0 | 0.667 | 30.7 |
| Volume | 51.0 | 0.333 | 17.0 |
| **Total** | — | — | **47.7** |

## Key Differences

- **Growth dominates the gap:** Nashville's 10.36% CAGR (growth_norm: 88.3) far outpaces Austin's 1.11% (growth_norm: 46.0).
- **Volume is comparable:** Both carry ~51–55M passengers per the normalized scores; Nashville edges Austin in absolute passengers (12.1M vs. 10.7M annually).
- **Long-haul:** Austin shows 0.4% long-haul share (limited); Nashville reports 0.0%.

## Investment Context

**Nashville signals stronger demand expansion**, making it a more attractive expansion candidate if growth trajectory and operational efficiency can be sustained. **Austin shows stability but lacks growth momentum**, which may limit near-term expansion ROI.

⚠️ **Limitation:** Both are Tier 2 with no FAA capacity constraints measured—cannot assess actual congestion or runway slot scarcity, which would be critical to expansion justification.

---

### 🏛️ FAA NPIAS -- independent second opinion

**Nashville International (BNA)** — FAA pegs development needs at $1.39B, 91st percentile, with a capacity outlook of not flagged in both 2028 and 2033. As a Tier-2 airport, the team's score of 77.1 carries no congestion metric, and the FAA's clean capacity outlook fills that gap without contradicting the score, though "not flagged" only means it's absent from the constrained list, not that congestion risk is disproven.

**Austin-Bergstrom International (AUS)** — FAA development need is $1.05B, 86th percentile, again with a not-flagged capacity profile for both 2028 and 2033. This heavy investment figure sits alongside a lower team score of 47.7 with no congestion input, so the FAA data neither confirms nor undermines the ranking—it simply supplies infrastructure-cost context the team's model couldn't capture, and the absence of a flag should not be read as a clean bill of health.

_Source: FAA NPIAS 2025-2029 (Appendix A development costs; Narrative Figure 1 capacity outlook). This view sits beside the deterministic score and never changes it. "Not flagged" means an airport is not on the FAA's constrained list -- not proof it is unconstrained (small hubs may not have been evaluated)._

---

**Q:** Compare O'Hare and Midway.

# O'Hare vs. Midway: Investment Comparison

## Summary
**O'Hare (ORD)** is the substantially larger and more congested facility, with a stronger investment case. **Midway (MDW)** is a secondary airport with lower growth and demand signals.

---

## Investment Scores

| Airport | Investment Score | Demand Score | Annual Passengers (CY24) |
|---------|------------------|--------------|--------------------------|
| **O'Hare** | 76.0 | 79.0 | 38,575,693 |
| **Midway** | 52.2 | 55.5 | 10,360,093 |

### O'Hare Score Breakdown
| Metric | Sub-Score | Weight | Contribution |
|--------|-----------|--------|--------------|
| Congestion | 71.4 | 0.4 | 28.6 |
| Growth | 73.3 | 0.4 | 29.3 |
| Volume | 90.5 | 0.2 | 18.1 |
| **Total** | — | — | **76.0** |

### Midway Score Breakdown
| Metric | Sub-Score | Weight | Contribution |
|--------|-----------|--------|--------------|
| Congestion | 47.3 | 0.4 | 18.9 |
| Growth | 58.2 | 0.4 | 23.3 |
| Volume | 50.1 | 0.2 | 10.0 |
| **Total** | — | — | **52.2** |

---

## Key Differences

| Metric | O'Hare | Midway |
|--------|--------|--------|
| **Growth (CAGR)** | 7.07% | 3.78% |
| **Long-Haul Share** | 0.4% | 0.0% |
| **Congestion Ratio** | 2,994 ops/slot-hour | 2,142 ops/slot-hour |
| **Declared Capacity** | 220 ops/hour | 74 ops/hour |
| **Hub Status** | Large (L) | Large (L) |

---

## Investment Insights

**O'Hare's advantage:**
- 3.7× larger passenger base
- 87% higher growth rate
- Significantly higher congestion (2,994 vs. 2,142), indicating acute capacity pressure
- Strong volume foundation (90.5 vs. 50.1 normalized)
- **Caveat:** Capacity profile was updated post-2014 (new runway 9C/27C, Nov 2020); declared capacity of 220 ops/hour may now understate true congestion relative to peak demand

**Midway's constraints:**
- Much smaller volume and lower growth
- No long-haul service (0

---

### 🏛️ FAA NPIAS -- independent second opinion

**Chicago O'Hare International (ORD)** — FAA pegs development need at $2.04B (97th percentile) with a capacity outlook of constrained in both 2028 and 2033; this strongly corroborates the team's already-high congestion reading (71.4 norm, 76.0 score), confirming O'Hare's capacity pressure is structural and persistent, not a modeling artifact.

**Chicago Midway International (MDW)** — FAA development need sits at $326.4M (57th percentile), with capacity not flagged for 2028 but shifting to congested by 2033, a worsening trajectory that aligns reasonably with the team's moderate congestion score (47.3 norm, 52.2 overall); it's a watch-level signal rather than a hard constraint, so treat the current "not flagged" status as unconfirmed rather than a clean bill of health.

_Source: FAA NPIAS 2025-2029 (Appendix A development costs; Narrative Figure 1 capacity outlook). This view sits beside the deterministic score and never changes it. "Not flagged" means an airport is not on the FAA's constrained list -- not proof it is unconstrained (small hubs may not have been evaluated)._

---

**Q:** Compare Dallas and Houston.

# Dallas/Fort Worth vs. Houston Comparison

## Overview
Both airports are Tier 1 hubs in the West South Central region, but **Dallas/Fort Worth (DFW) is significantly larger and scores higher on investment attractiveness**.

| Metric | DFW | IAH (Houston) |
|--------|-----|---------------|
| Annual Passengers (CY24) | 42,351,316 | 23,349,157 |
| Annual Operations | 641,095 | 341,827 |
| Growth CAGR | 8.88% | 7.27% |
| Long-Haul Share | 0.8% | 0.9% |

---

## Investment Scores

**Dallas/Fort Worth: 75.6 / 100**

| Metric | Sub-Score | Weight | Contribution |
|--------|-----------|--------|--------------|
| Congestion | 60.8 | 0.4 | 24.3 |
| Growth | 81.6 | 0.4 | 32.6 |
| Volume | 93.4 | 0.2 | 18.7 |
| **Total** | — | — | **75.6** |

**Houston (IAH): 60.2 / 100**

| Metric | Sub-Score | Weight | Contribution |
|--------|-----------|--------|--------------|
| Congestion | 38.9 | 0.4 | 15.6 |
| Growth | 74.2 | 0.4 | 29.7 |
| Volume | 75.1 | 0.2 | 15.0 |
| **Total** | — | — | **60.2** |

---

## Key Differences

- **Demand Score**: DFW (85.5) outpaces IAH (74.5) — stronger passenger growth and volume trajectory
- **Congestion**: DFW is notably more congested (ratio 2617.0 ops/slot vs. 1843.0), reflecting its larger scale; this drives the higher investment score (the formula weights congestion at 40%)
- **Growth**: DFW grows faster (8.88% CAGR vs. 7.27%), scoring 81.6 vs. 74.2 on the growth metric
- **Long-haul**: IAH has slightly higher international/long-haul exposure (0.9% vs. 0.8%), consistent with a major hub role

---

## Investment Perspective

**DFW is the stronger expansion candidate** by a margin of 15.4 points (75.6 vs. 60.2). It combines higher absolute volume, faster growth, and more acute congestion pressure—all signals of near-term capacity constraints that make expansion economically justified. Houston has slower growth and looser capacity, reducing urgency and return potential.

---

### 🏛️ FAA NPIAS -- independent second opinion

**Dallas/Fort Worth International (DFW)** — FAA pegs development need at $2.34B, the 98th percentile nationally, with capacity outlook running congested in both 2028 and 2033; the team's congestion score is actually more alarmed than the FAA's designation, which flags congestion but not a hard capacity constraint, so the team's caution here is directionally supported but somewhat ahead of the FAA's own severity read.

**George Bush Intercontinental (IAH)** — FAA development need is modest at $51.7M (8th percentile) with capacity not flagged for either 2028 or 2033, aligning with the team's comparatively low congestion score; both signals are quiet, though absence of a flag simply means IAH isn't on the constrained list, not a clean bill of health.

_Source: FAA NPIAS 2025-2029 (Appendix A development costs; Narrative Figure 1 capacity outlook). This view sits beside the deterministic score and never changes it. "Not flagged" means an airport is not on the FAA's constrained list -- not proof it is unconstrained (small hubs may not have been evaluated)._

---


## E. Explanations

**Q:** Why is Charlotte a strong investment candidate?

# Why Charlotte Douglas International (CLT) Is a Strong Investment Candidate

Charlotte Douglas is a compelling investment opportunity driven by **robust demand growth, significant current congestion, and planned capacity expansion**. Here's the breakdown:

## Investment Score: 79.2 / 100

| Metric | Sub-Score | Weight | Contribution |
|--------|-----------|--------|--------------|
| Congestion | 67.7 | 0.4 | 27.1 |
| Growth | 89.6 | 0.4 | 35.8 |
| Volume | 81.2 | 0.2 | 16.2 |
| **Total** | — | — | **79.2** |

## Key Strengths

1. **Exceptional Growth (89.6/100):** CLT is expanding at a 10.64% compound annual growth rate—well above typical airport performance. This signals strong regional economic momentum and airline network expansion.

2. **High Current Congestion (67.7/100):** The airport operates at a 2,860:1 congestion ratio (annual operations per declared hourly runway slot), indicating meaningful capacity constraints. This creates both operational stress and a strong business case for expansion investment.

3. **Substantial Volume (81.2/100):** With 28.5 million annual passengers and 511,933 annual operations, CLT is a major hub serving the South Atlantic region—providing stable, high-traffic demand.

4. **Planned Capacity Relief:** A fourth parallel runway is planned for ~2027, offering a concrete expansion project aligned with demonstrated demand pressure.

## Important Caveat

**Staleness flag:** CLT's declared capacity is based on 2014 data. The fourth parallel runway project (post-2014) means current congestion may actually be *worse* than the 2,860 ratio suggests, making expansion even more urgent. The 2014 baseline does not yet reflect this infrastructure improvement, so today's actual operational stress is not fully captured in our metrics.

**Long-haul share:** 0.0% is domestic-passenger-based and reflects CLT's hub role in connecting regional/domestic traffic rather than international long-haul dominance.

---

### 🏛️ FAA NPIAS -- independent second opinion

**Charlotte Douglas International (CLT)** The FAA pegs a five-year development need of $1.03B, landing in the 85th percentile nationally, with a capacity outlook that's not flagged for 2028 but shifts to congested by 2033. This trajectory validates the team's congestion score of 67.7 directionally, though notably the team's internal read runs hotter than the FAA's own timeline suggests — the team is flagging risk sooner than the federal data currently substantiates, which is worth reconciling before treating the 79.2 score as fully corroborated by regulatory evidence.

_Source: FAA NPIAS 2025-2029 (Appendix A development costs; Narrative Figure 1 capacity outlook). This view sits beside the deterministic score and never changes it. "Not flagged" means an airport is not on the FAA's constrained list -- not proof it is unconstrained (small hubs may not have been evaluated)._

---

**Q:** Why is LaGuardia congested?

# Why LaGuardia is Congested

LaGuardia operates at **3,841 annual operations per declared hourly runway slot**—nearly 46× the ideal capacity of one flight per slot per hour. This extreme congestion ratio (95.4 out of 100) is the primary driver of its high investment urgency.

## The Congestion Picture

| Metric | Sub-Score | Weight | Contribution |
|--------|-----------|--------|--------------|
| **Congestion** | 95.4 | 0.4 | **38.2** |
| Growth | 75.3 | 0.4 | 30.1 |
| Volume | 64.8 | 0.2 | 13.0 |
| | | | **Investment Score: 81.3** |

## Root Causes

1. **Constrained Physical Capacity**  
   LaGuardia's declared capacity is only **83 operations per hour**, severely limiting throughput despite strong demand.

2. **Strong Passenger Demand**  
   16.7 million annual passengers (CY24) with **7.52% growth (CAGR)** drive sustained pressure on fixed runway slots.

3. **Structural Mismatch**  
   The airport sits in a dense urban region with limited room for expansion, so current infrastructure cannot accommodate growth.

## Context

- LaGuardia is a **Tier 1 airport** (capacity-constrained and FAA-profiled), making this congestion quantifiable and directly comparable.
- The **0.0% long-haul share** indicates LaGuardia is primarily a domestic and short-haul hub, concentrating regional demand that cannot easily shift to alternatives.
- No staleness flag applies—2014 capacity baseline is current.

This combination of high growth, large passenger base, and severely limited runway slots makes LaGuardia one of the most congested US airports, justifying its **81.3 investment score**.

---

### 🏛️ FAA NPIAS -- independent second opinion

**LaGuardia (LGA)**: FAA pegs a five-year development need of $110.1M (14th percentile) while its runway-capacity outlook stays "capacity constrained" in both 2028 and 2033, reinforcing rather than adding new weight to the team's own steep 95.4 congestion norm and 81.3 overall score — the federal forecast simply confirms the constraint the team already identified, with no sign of near-term relief.

_Source: FAA NPIAS 2025-2029 (Appendix A development costs; Narrative Figure 1 capacity outlook). This view sits beside the deterministic score and never changes it. "Not flagged" means an airport is not on the FAA's constrained list -- not proof it is unconstrained (small hubs may not have been evaluated)._

---


## F. Out-of-scope airports (not among the 65)

**Q:** How congested is Fresno?

# Fresno Congestion Status

**Fresno is unresolved.** We do not have congestion data for this airport in our current dataset.

## Why

Fresno Yosemite International Airport (FAT) is a **Tier 2 airport** in our framework. Tier 2 airports lack a FAA capacity profile—meaning we have no declared hourly runway slots or historical operations data needed to compute a congestion_ratio. Without these capacity benchmarks, congestion cannot be measured or compared to other airports.

## Next steps

If you need to evaluate Fresno for investment, we can provide:
- **Demand signals** (if available): passenger trends, route diversity, long-haul share
- **Context**: Tier 2 status means it is a smaller regional hub without formal FAA slot constraints

Would you like demand-side analysis for Fresno instead, or do you want to compare it to a Tier 1 airport where congestion data *is* available?

---

**Q:** Compare Boise and Spokane.

## Comparison: Boise vs. Spokane

**Result:** Only Boise is available in the current dataset. **Spokane is unresolved/out of scope** and cannot be compared at this time.

---

### Boise Airport (BOI) – Summary

| Metric | Value |
|--------|-------|
| **Tier** | 2 (Regional) |
| **Region** | Mountain |
| **Hub Status** | M (Minor) |
| **Annual Passengers (CY24)** | 2,475,370 |
| **Growth (CAGR %)** | 5.34 |
| **Long-Haul Share (%)** | 0.0 |
| **Annual Operations** | 58,608 |
| **Demand Score** | 45.6 |

#### Demand Score Breakdown

| Metric | Sub-Score (0–100) | Weight | Contribution |
|--------|------|--------|-----|
| Growth | 65.4 | 0.667 | 43.6 |
| Volume | 6.1 | 0.333 | 2.0 |
| **Total Demand Score** | — | — | **45.6** |

**Note:** Boise is a Tier 2 airport with no FAA capacity profile. Its demand score reflects growth and passenger volume only; **congestion is not measured and is not comparable to Tier 1 facilities**. The staleness flag is clear (data is current).

---

**To compare with Spokane, please verify that Spokane data is available in your dataset or request it separately.**

---

### 🏛️ FAA NPIAS -- independent second opinion

**Boise Airport (Gowen Field) (BOI)** – FAA five-year development-need is estimated at $87.7M, placing it at just the 9th percentile nationally, and the capacity outlook is unflagged for both 2028 and 2033. This is a Tier-2 airport, so the team's own score carries no congestion metric here; the FAA data doesn't fill that gap with a warning, but a low-cost, unconstrained profile is consistent with a quiet, low-pressure facility rather than pointing to any hidden strain the score might be missing.

No FAA figures for Spokane were provided in the data set, so no second-opinion comparison can be made for that airport.

_Source: FAA NPIAS 2025-2029 (Appendix A development costs; Narrative Figure 1 capacity outlook). This view sits beside the deterministic score and never changes it. "Not flagged" means an airport is not on the FAA's constrained list -- not proof it is unconstrained (small hubs may not have been evaluated)._

---

**Q:** How is Tucson doing?

**Tucson International Airport (TUS) – Status: Unresolved**

Tucson is not in scope for this analysis. The system was unable to resolve it against the investable airport database.

This could mean:
- TUS does not meet the current investment criteria (e.g., it may be classified as Tier 3 or below, or outside the focus set).
- Data is not yet loaded for this airport.

To assess Tucson's investment potential, you would need to:
1. Confirm whether it is included in your firm's target list.
2. If it should be, request that TUS be added to the analytic database.
3. Once available, metrics like demand_score (passenger growth, market share) and investment_score (capacity constraints, expansion feasibility) can be computed.

Is there a different airport you'd like me to analyze, or would you like to add Tucson to the scope?

---

**Q:** What about El Paso and Reno?

Both **El Paso** and **Reno** are **unresolved** – they fall outside the scope of this analysis.

This investment tool focuses on **Tier 1 airports** (major US hubs with FAA capacity profiles and congestion data) and a curated set of **Tier 2 airports** (medium-size hubs with demand signals but no FAA capacity measurement). El Paso and Reno do not appear in either tier's dataset.

If your firm is evaluating these markets, you would need to:
- Source capacity and operations data directly from each airport's master plan or FAA records
- Gather passenger demand, route diversity, and long-haul connectivity from airline and TSA data
- Assess local economic drivers and regional competition independently

Feel free to ask about any **Tier 1 or Tier 2 airports** that are in scope, and I can provide detailed investment and demand scores with full breakdowns.

---

**Q:** Rank the airports in Wichita and Tulsa.

# Ranking Result: Wichita and Tulsa

**Status: Unresolved**

Neither Wichita nor Tulsa resolved to a specific airport code in the system. 

**Possible airports:**
- **Wichita** likely refers to **MHK** (Wichita Dwight D. Eisenhower National Airport)
- **Tulsa** likely refers to **TUL** (Tulsa International Airport)

To complete the ranking, please clarify:
1. Should I analyze MHK and TUL specifically?
2. Are there other airports in these cities you'd like included?

Once confirmed, I can provide a full comparative analysis with investment scores, demand metrics, congestion profiles, and a clear ranking.

---


## G. Messy input (typos, descriptions, a factual trap)

**Q:** How congested is Chicagoo?

# Chicago O'Hare (ORD) Congestion Assessment

**Chicago O'Hare is moderately congested**, with a congestion ratio of **2,994.0** annual operations per declared hourly runway slot.

## Congestion Metric Detail

| Metric | Value |
|--------|-------|
| Annual Operations | 657,133 |
| Declared Capacity (ops/hr) | 220.0 |
| **Congestion Ratio** | **2,994.0** |
| Congestion Normalized Score (0–100) | 71.4 |

## Important Caveats

**⚠️ Capacity Profile Staleness:** ORD is flagged as having post-2014 capacity changes. A new runway (9C/27C) opened in November 2020, plus airfield reconfiguration. The 2014 FAA profile underlying this congestion ratio may **understate current capacity**, meaning today's actual congestion could be **lower** than this figure suggests. The declared capacity of 220 ops/hr may not fully reflect the expanded runway system.

## Context: Investment Score

ORD's overall **investment score is 76.0**, driven by:

| Component | Sub-Score | Weight | Contribution |
|-----------|-----------|--------|--------------|
| Congestion | 71.4 | 0.4 | 28.6 |
| Growth (CAGR) | 73.3 | 0.4 | 29.3 |
| Volume (passengers CY24) | 90.5 | 0.2 | 18.1 |
| | | | **76.0** |

ORD's congestion and growth rates are both solid investment signals, paired with very high passenger volume (38.6M annually), making it an attractive expansion candidate despite the capacity uncertainty.

---

### 🏛️ FAA NPIAS -- independent second opinion

**Chicago O'Hare International (ORD)** FAA pegs development need at $2.04B, the 97th percentile nationally, with runway capacity outlook flagged as constrained for both 2028 and 2033. This aligns with the team's own high congestion reading (71.4 norm, 76.0 overall score) — the FAA's forward-looking data corroborates rather than contradicts the internal assessment, reinforcing that ORD's capacity pressure is a persistent, structural issue rather than a temporary spike.

_Source: FAA NPIAS 2025-2029 (Appendix A development costs; Narrative Figure 1 capacity outlook). This view sits beside the deterministic score and never changes it. "Not flagged" means an airport is not on the FAA's constrained list -- not proof it is unconstrained (small hubs may not have been evaluated)._

---

**Q:** What is the main airport serving Silicon Valley?

# Main Airport Serving Silicon Valley

**Norman Y. Mineta San Jose International (SJC)** is the main airport serving Silicon Valley.

## Airport Profile

| Metric | Value |
|--------|-------|
| IATA Code | SJC |
| Tier | 2 |
| Region | Pacific |
| Hub Status | Medium |
| Annual Passengers (CY24) | 5,822,019 |
| Annual Operations | 104,106 |

## Demand Score Breakdown

SJC has a **demand_score of 42.5** (0–100 scale), calculated as follows:

| Metric | Sub-Score | Weight | Contribution |
|--------|-----------|--------|--------------|
| Growth (CAGR) | 47.6 | 0.667 | 31.7 |
| Volume (Passengers) | 32.4 | 0.333 | 10.8 |
| **Total** | — | — | **42.5** |

**Growth CAGR:** 1.45%  
**Long-haul Share:** 0.0%

## Important Limitation

⚠ **Tier 2 Airport:** SJC has no FAA capacity profile, so congestion is not measured. The demand_score reflects growth and volume signals only and is **not comparable to Tier 1 airport scores**, which include congestion data. The staleness flag is false, indicating the airport data is current.

---

### 🏛️ FAA NPIAS -- independent second opinion

**San Jose International (SJC)** — FAA data show a five-year development need of $278.3M (51st percentile) with a capacity outlook that remains congested from 2028 through 2033. Since this is a Tier-2 airport, the team's model carries no congestion metric here, so this FAA-sourced constrained outlook fills that gap, adding an independent signal of persistent capacity pressure that the internal score of 42.5 could not capture on its own.

_Source: FAA NPIAS 2025-2029 (Appendix A development costs; Narrative Figure 1 capacity outlook). This view sits beside the deterministic score and never changes it. "Not flagged" means an airport is not on the FAA's constrained list -- not proof it is unconstrained (small hubs may not have been evaluated)._

---

**Q:** What's the airport in the capital of Alaska?

The airport in the capital of Alaska is **Juneau International Airport (JNU)**, located in Juneau.

However, this airport is **out of scope** for the investment analysis covered by this system. Juneau is a Tier 2 regional airport and does not appear in the available dataset of airports evaluated for US expansion investment metrics.

If you're interested in evaluating Alaska airports for expansion potential, you may want to inquire about larger regional hubs in the state that fall within the coverage scope.

---


## H. Follow-ups (conversation memory in one thread)

**Q:** Compare LA and Santa Ana congestion.

# Congestion Comparison: LAX vs. Santa Ana (SNA)

## Summary
**LAX is significantly more congested than Santa Ana.** LAX's congestion ratio is **2412.0** operations per declared hourly runway slot, compared to Santa Ana's **1623.0**—a difference of 789 operations per slot (49% higher congestion at LAX).

## Detailed Metrics

| Metric | LAX | Santa Ana |
|--------|-----|-----------|
| **Congestion Ratio** | 2412.0 | 1623.0 |
| **Declared Capacity (ops/hr)** | 172.0 | 58.0 |
| **Annual Operations** | 413,641 | 94,965 |
| **Congestion Norm (0–100 score)** | 55.0 | 32.7 |

## Context

- **LAX (Tier 1):** Operates at ~2,400 ops per hourly slot. High absolute volume (413k+ ops/year) and elevated growth (3.59% CAGR) drive persistent congestion, despite significant declared capacity.

- **Santa Ana (Tier 1):** Lower congestion ratio (1,623 ops/slot) and much smaller scale (~95k ops/year). However, its note flags a material constraint: *"Commercial ops/passengers capped by a community Settlement Agreement (amended 2003); practical commercial capacity below runway capacity."* This means the declared capacity (58 ops/hr) overstates what is actually available for growth, and the congestion metric reflects operational reality under that cap—not runway scarcity.

## Confidence Note
Both are Tier 1 airports with current FAA capacity profiles. LAX's congestion is demand-driven at a major international hub. Santa Ana's congestion is lower in absolute terms, but its growth is flat (−1.7% CAGR) and constrained by agreement, making it a limited expansion candidate despite lower current stress.

---

### 🏛️ FAA NPIAS -- independent second opinion

**Los Angeles International (LAX)** — FAA development need sits at $572.7M (69th percentile), with the capacity outlook holding at capacity constrained for both 2028 and 2033; this reinforces the team's already-elevated congestion score, confirming LAX faces sustained, unrelieved runway pressure through the forecast horizon.

**John Wayne–Orange County (SNA)** — FAA development need is $114.8M (15th percentile), with a 2028->2033 outlook of congested (not the more severe capacity-constrained tier); this watch-level signal aligns reasonably well with the team's moderate congestion score, though it's a softer flag than LAX's and shouldn't be read as evidence of a hard capacity bottleneck.

_Source: FAA NPIAS 2025-2029 (Appendix A development costs; Narrative Figure 1 capacity outlook). This view sits beside the deterministic score and never changes it. "Not flagged" means an airport is not on the FAA's constrained list -- not proof it is unconstrained (small hubs may not have been evaluated)._

---

**Q:** What about their growth?

# Growth Analysis

Both airports show very different growth trajectories:

## LAX (Los Angeles International)
**Growth CAGR: 3.59%**  
LAX is expanding steadily, with 37.8M passengers in CY24. Its growth contributes meaningfully to its investment score:

| Metric | Sub-Score (0–100) | Weight | Contribution |
|--------|-------------------|--------|--------------|
| Congestion | 55.0 | 0.4 | 22.0 |
| **Growth** | **57.4** | **0.4** | **23.0** |
| Volume | 89.9 | 0.2 | 18.0 |
| **Investment Score** | | | **62.9** |

At 3.59% annual growth, LAX is posting moderate gains—a healthy expansion signal for a major hub airport.

## SNA (John Wayne–Orange County)
**Growth CAGR: −1.7%**  
SNA is contracting, declining at 1.7% annually despite serving 5.4M passengers in CY24. This negative growth significantly constrains its investment profile:

| Metric | Sub-Score (0–100) | Weight | Contribution |
|--------|-------------------|--------|--------------|
| Congestion | 32.7 | 0.4 | 13.1 |
| **Growth** | **33.2** | **0.4** | **13.3** |
| Volume | 29.9 | 0.2 | 6.0 |
| **Investment Score** | | | **32.3** |

**Key constraint:** SNA operates under a 2003 Community Settlement Agreement that caps commercial operations and passengers below runway capacity. This regulatory ceiling explains both the weak growth and the investment score's lower ranking.

**Bottom line:** LAX shows positive growth momentum and a stronger investment case; SNA faces structural headwinds from its settlement cap that limit expansion potential.

---

### 🏛️ FAA NPIAS -- independent second opinion

**Los Angeles International (LAX)** — FAA development need is pegged at $572.7M (69th percentile), and the capacity outlook stays "capacity constrained" through both 2028 and 2033, reinforcing the team's own elevated congestion reading rather than pointing to any imminent easing of pressure that might support additional growth.

**John Wayne-Orange County (SNA)** — At $114.8M (15th percentile), development need is modest, and the FAA's "congested" tag holds steady from 2028 to 2033 — a watch-level signal, not a hard constraint — which lines up with the team's moderate congestion score and suggests capacity is unlikely to be the swing factor for growth trajectory here.

_Source: FAA NPIAS 2025-2029 (Appendix A development costs; Narrative Figure 1 capacity outlook). This view sits beside the deterministic score and never changes it. "Not flagged" means an airport is not on the FAA's constrained list -- not proof it is unconstrained (small hubs may not have been evaluated)._

---

**Q:** And volume?

# Volume Assessment

You asked about **volume**. Here are the two airports ranked by their volume normalization score:

| Airport | IATA | Annual Passengers (CY24) | Annual Ops | Volume Score (0–100) |
|---------|------|--------------------------|------------|----------------------|
| Los Angeles International | LAX | 37,760,834 | 413,641 | 89.9 |
| John Wayne–Orange County | SNA | 5,370,273 | 94,965 | 29.9 |

**LAX** dominates on raw scale (37.8M passengers, 413.6K operations) and achieves a volume normalization score of **89.9**, reflecting its position as a major hub. **SNA** is much smaller (5.4M passengers, 95K operations) with a volume score of **29.9**.

Note: Volume contributes only **20% of the investment score** (the formula is 0.4×congestion + 0.4×growth + 0.2×volume). LAX's high volume score (18.0 contribution points) is tempered by moderate congestion and growth signals, yielding an overall investment_score of **62.9**. SNA's lower volume (6.0 contribution) reflects both smaller passenger base and operational constraints from its 2003 Community Settlement Agreement, resulting in an investment_score of **32.3**.

---

### 🏛️ FAA NPIAS -- independent second opinion

**Los Angeles International (LAX)** — FAA pegs a $572.7M five-year development need (69th percentile) with a capacity outlook that stays "capacity constrained" from 2028 through 2033; this reinforces the team's already-elevated congestion read (55.0) and score (62.9), confirming LAX's tightness is a durable, not transient, condition.

**John Wayne-Orange County (SNA)** — FAA estimates $114.8M in development need (15th percentile) and flags SNA as "congested" in both 2028 and 2033 — a watch-level signal rather than a hard constraint — which lines up reasonably well with the team's moderate congestion figure (32.7) and overall score (32.3).

_Source: FAA NPIAS 2025-2029 (Appendix A development costs; Narrative Figure 1 capacity outlook). This view sits beside the deterministic score and never changes it. "Not flagged" means an airport is not on the FAA's constrained list -- not proof it is unconstrained (small hubs may not have been evaluated)._

---

**Q:** Why is LAX more congested?

# Why LAX Shows Higher Congestion

LAX operates at a **congestion ratio of 2,412**, meaning it handles approximately 2,412 annual operations per declared hourly runway slot. This ratio reflects the airport's annual operations (413,641) divided by its declared capacity of 172 operations per hour, indicating substantial pressure on runway infrastructure.

## Investment Score Breakdown

LAX's overall **investment score of 62.9** reflects this congestion alongside growth and volume factors:

| Metric | Sub-Score (0–100) | Weight | Contribution |
|--------|---|---|---|
| Congestion | 55.0 | 0.4 | 22.0 |
| Growth | 57.4 | 0.4 | 23.0 |
| Volume | 89.9 | 0.2 | 18.0 |
| **Total** | — | — | **62.9** |

The congestion sub-score of 55.0 (normalized to a 0–100 scale) is weighted at 40%, making it a significant contributor. LAX's high absolute volume (37.8 million annual passengers) combined with moderate declared capacity creates the operational squeeze.

## Key Drivers

1. **Large passenger base** (89.9 volume normalized score) concentrated on limited runway capacity (172 ops/hour declared)
2. **Sustained growth** (3.59% CAGR, 57.4 growth norm) adding pressure over time
3. **Runway slot constraints** typical of major coastal hubs

**Note:** The 2014 FAA capacity declaration is flagged as current (staleness: false), so the 172 ops/hour reflects recent data. Long-haul share shows 0.0%, indicating the metric is based on domestic passenger mix only.

---

### 🏛️ FAA NPIAS -- independent second opinion

**Los Angeles International (LAX)** FAA data show a five-year development-need estimate of $572.7M, placing LAX at the 69th percentile nationally, with a capacity outlook that remains "capacity constrained" in both 2028 and 2033 — a persistent, non-worsening bottleneck. This corroborates the team's own congestion read (55.0 norm, 62.9 overall score): the FAA's independent forward-looking capacity view lines up with what the team's score already flags, reinforcing rather than contradicting the internal assessment.

_Source: FAA NPIAS 2025-2029 (Appendix A development costs; Narrative Figure 1 capacity outlook). This view sits beside the deterministic score and never changes it. "Not flagged" means an airport is not on the FAA's constrained list -- not proof it is unconstrained (small hubs may not have been evaluated)._

---


## Deterministic ground truth (verify the numbers above)

```
iata  tier hub             region  growth_cagr_pct  longhaul_share_pct    ops  congestion_raw  congestion_norm  investment_score  demand_score  dev_cost_2025_2029  capacity_2028  capacity_2033
 ATL     1   L     South Atlantic              5.8                 0.3 690292          3123.5             75.1              77.1          78.4          1502965252              1              2
 BOS     1   L        New England              7.9                 0.3 328953          2729.9             64.0              70.8          75.3           906303854              2              3
 BWI     1   L     South Atlantic              9.1                 0.0 207349          2802.0             66.0              71.0          74.3           635439726              1              2
 CLT     1   L     South Atlantic             10.6                 0.0 511933          2860.0             67.7              79.2          86.8          1034776873              0              1
 DCA     1   L     South Atlantic              4.6                 0.0 282173          4002.5            100.0              76.1          60.1          1274679136              2              2
 DEN     1   L           Mountain              8.4                 1.1 643935          2299.8             51.8              70.7          83.4          1063036000              1              1
 DFW     1   L West South Central              8.9                 0.8 641095          2616.7             60.8              75.6          85.5          2343113489              1              1
 DTW     1   L East North Central              6.7                 0.5 269677          1489.9             28.9              52.9          68.9           371694229              0              0
 EWR     1   L    Middle Atlantic              4.2                 0.2 294541          3036.5             72.7              68.4          65.6            94400000              2              3
 FLL     1   L     South Atlantic              5.5                 0.0 194650          2495.5             57.3              62.4          65.8          1021368126              0              1
 HNL     1   L            Pacific              3.7                13.6 167715          1415.3             26.8              43.9          55.3           582223120              0              0
 IAD     1   L     South Atlantic              9.6                 0.4 174530          1111.7             18.2              52.5          75.4           603893103              0              1
 IAH     1   L West South Central              7.3                 0.9 341827          1842.7             38.9              60.2          74.5            51718665              0              0
 JFK     1   L    Middle Atlantic             -0.2                 1.1 255441          2886.3             68.4              60.3          54.8           257289334              2              3
 LAS     1   L           Mountain              4.5                 0.0 405106          3240.8             78.4              72.2          68.1           135766667              2              3
 LAX     1   L            Pacific              3.6                 0.0 413641          2411.9             55.0              62.9          68.2           572656460              2              2
 LGA     1   L    Middle Atlantic              7.5                 0.0 318783          3840.8             95.4              81.3          71.8           110066871              2              2
 MCO     1   L     South Atlantic              5.1                 0.0 334039          2018.4             43.8              59.3          69.6           214898588              0              0
 MDW     1   L East North Central              3.8                 0.0 158514          2142.1             47.3              52.2          55.5           326396067              0              1
 MEM     1   S East South Central              6.2                 0.0 162536          1069.3             17.0              35.6          48.0           182789359              0              0
 MIA     1   L     South Atlantic              2.7                 0.0 235187          1668.0             33.9              50.7          61.9          1826314254              1              2
 MSP     1   L West North Central              7.3                 0.5 292058          1808.4             37.9              58.3          71.9           653905319              0              0
 ORD     1   L East North Central              7.1                 0.4 657133          2993.8             71.4              76.0          79.0          2042331509              2              2
 PHL     1   L    Middle Atlantic             10.1                 0.0 259478          2109.6             46.4              65.7          78.5           377310630              0              1
 PHX     1   L           Mountain              7.8                 0.0 417075          2947.5             70.1              74.2          76.9           203396468              1              1
 SAN     1   L            Pacific              6.6                 0.0 195545          3724.7             92.1              76.6          66.3          2405797784              2              3
 SEA     1   L            Pacific              5.4                 0.0 382147          3605.2             88.8              77.3          69.7           539206029              2              3
 SFO     1   L            Pacific              6.3                 0.0 277099          2639.0             61.4              67.9          72.3           683792071              2              3
 SLC     1   L           Mountain              4.4                 0.0 237051          1590.9             31.7              48.7          60.0           173627159              0              0
 TPA     1   L     South Atlantic              5.9                 0.0 172645          1514.4             29.6              50.0          63.6           233836969              0              0
 SNA     1   M            Pacific             -1.7                 0.0  94965          1623.3             32.7              32.3          32.1           114810954              1              1
 OAK     1   M            Pacific             -3.3                 0.0 108547           893.4             12.0              21.0          27.1           843610420              0              0
 LGB     1   S            Pacific             12.7                 0.0  35915           469.5              0.0              39.6          65.9           209761682              0              0
 ANC     2   M            Pacific              3.3                 5.0 136925             NaN              NaN               NaN          40.5           319008800              0              0
 BDL     2   M        New England              7.2                 0.0  59880             NaN              NaN               NaN          54.1           174957175              0              0
 BNA     2   L East South Central             10.4                 0.0 208149             NaN              NaN               NaN          77.1          1394034035              0              0
 AUS     2   L West South Central              1.1                 0.4 179873             NaN              NaN               NaN          47.7          1047269147              0              0
 DAL     2   M West South Central              5.2                 0.0 150296             NaN              NaN               NaN          57.9           152345517              1              1
 PDX     2   M            Pacific              8.6                 0.0 162640             NaN              NaN               NaN          68.5           247709640              0              0
 STL     2   M West North Central              7.8                 0.0 144256             NaN              NaN               NaN          64.8          1639905443              0              0
 RDU     2   M     South Atlantic             12.9                 0.0 134027             NaN              NaN               NaN          80.2           384556600              0              0
 HOU     2   M West South Central              5.1                 0.0 116161             NaN              NaN               NaN          55.8           307491696              1              1
 SMF     2   M            Pacific              5.0                 0.0 118962             NaN              NaN               NaN          54.9           200019806              0              0
 MSY     2   M West South Central              4.7                 0.0 106246             NaN              NaN               NaN          53.7           281820751              0              0
 SJU     2   M        Puerto Rico             11.3                 0.0 102916             NaN              NaN               NaN          73.8           160349606              0              0
 MCI     2   M West North Central             10.6                 0.0 110153             NaN              NaN               NaN          70.5           227147166              0              0
 SJC     2   M            Pacific              1.4                 0.0 104106             NaN              NaN               NaN          42.5           278271918              1              1
 SAT     2   M West South Central              6.9                 0.0  91449             NaN              NaN               NaN          58.4           502211804              1              1
 RSW     2   M     South Atlantic              2.4                 0.0  76601             NaN              NaN               NaN          44.6           589676600              0              0
 IND     2   M East North Central             10.9                 0.0 121316             NaN              NaN               NaN          70.1           511926366              0              0
 CLE     2   M East North Central              7.7                 0.0  89137             NaN              NaN               NaN          60.0           215122803              0              0
 PIT     2   M    Middle Atlantic             10.8                 0.0 103104             NaN              NaN               NaN          69.1           109344597              0              0
 CVG     2   M East South Central              9.3                 0.0 128959             NaN              NaN               NaN          63.7           495521108              0              0
 CMH     2   M East North Central             10.1                 0.0  89032             NaN              NaN               NaN          66.0           250756089              0              0
 PBI     2   M     South Atlantic             12.4                 0.0  63280             NaN              NaN               NaN          72.3           192692537              0              0
 JAX     2   M     South Atlantic              8.6                 0.0  66281             NaN              NaN               NaN          59.8            44000600              0              0
 ONT     2   M            Pacific              9.2                 0.0  84500             NaN              NaN               NaN          61.1           145494434              0              0
 OGG     2   M            Pacific             -9.0                 6.8  73865             NaN              NaN               NaN           5.3           193762995              0              0
 BUR     2   M            Pacific              5.4                 0.0  77383             NaN              NaN               NaN          49.0           117003896              0              0
 CHS     2   M     South Atlantic              9.1                 0.0  60351             NaN              NaN               NaN          59.4            36516492              0              0
 MKE     2   M East North Central              7.7                 0.0  66822             NaN              NaN               NaN          55.0           131799951              0              0
 ABQ     2   M           Mountain              7.7                 0.0  60207             NaN              NaN               NaN          53.8            50402686              0              0
 OMA     2   M West North Central              8.2                 0.0  53719             NaN              NaN               NaN          54.7           130763713              0              0
 BUF     2   M    Middle Atlantic             11.5                 0.0  51137             NaN              NaN               NaN          64.5            32923575              0              0
 BOI     2   M           Mountain              5.3                 0.0  58608             NaN              NaN               NaN          45.6            87690224              0              0
```
