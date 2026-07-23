# Design & Architecture — Airport Investment Intelligence Agent

An agent that helps analysts identify **US airports where expansion would be most
profitable**, based on flight/passenger capacity pressure and demand growth. It
ranks and compares airports on a **deterministic KPI** (never LLM-invented numbers),
explains its reasoning, and supports conversational follow-ups.

---

## 1. Guiding principle: reliability over coverage

The hard part of an investment tool is not producing a number , it is producing a
number an analyst can trust. Three commitments follow:

1. **Deterministic where it counts.** Every score, ranking, mapping, and comparison
   is pure Python. The LLM only reads the question and phrases the answer; it never
   touches a figure.
2. **Depth over breadth.** We cover a well-instrumented set of major airports with
   dense, authoritative data rather than all ~500 commercial airports thinly.
3. **Honest about uncertainty.** Every answer states its confidence and limitations
   (data tier, staleness, what the metric does and does not capture).

---

## 2. Architecture — a routing workflow, LLM at the edges

This is a **workflow** (predefined code path), not an autonomous agent , a
deliberate choice: the LLM must never be in a position to invent an investment
number. It sits only at the edges , understanding the question, phrasing the answer,
and an independent second-opinion commentary , never on the scoring path itself.

```
user question
  -> understand (LLM)   : natural language -> {intent, airports, region, metric}
  -> resolve   (code)   : natural name -> IATA code  (poka-yoke; never LLM-guessed)
  -> route     (code)   : Tier 1 (has FAA capacity) / Tier 2
  -> compute   (code)   : congestion / growth / volume -> weighted score
  -> respond   (LLM)    : computed numbers -> natural language + confidence/caveats
  -> second_opinion (LLM): an independent FAA NPIAS view beside the score (never alters it)
```

- **understand** (`pipeline/understand.py`) — Claude extracts a structured `Query`
  via the structured-output API. Handles fuzzy language ("Santa Ana", "the Anchorage
  airport", regions).
- **resolve** (`pipeline/resolve.py`) — a deterministic alias map turns a name into
  an IATA code. This is the guardrail against a hallucinated `SAN` vs `SNA`. A light
  fuzzy pass tolerates typos; unresolvable names are reported, not guessed.
- **route** (`pipeline/route.py`) — reads each airport's tier from the reference table.
- **compute** (`pipeline/compute.py`) — dispatches on intent (`metric` / `compare` /
  `rank` / `explain`) and assembles the answer's **facts** from the scoring core.
- **respond** (`pipeline/respond.py`) — Claude phrases those facts, weaving in the
  confidence/limitation statements. It is instructed to use only the numbers given.
  A fifth intent, `meta`, bypasses the data path entirely — see §2.1.
- **second_opinion** (`pipeline/second_opinion.py`) — appended after `respond`: an
  independent FAA-NPIAS read presented beside the score, never feeding it.

**No API key? The agent still runs.** `understand` degrades to a keyword parser and
`respond` to a template formatter, so the entire deterministic core is demonstrable
without any LLM or network. This is the architecture claim made literal: unplug the
edges and the numbers are unchanged.

### 2.1 Conversation memory

`agent.ask()` returns an opaque `context` dict that the caller (CLI or Streamlit)
hands back on the next turn. It carries two different things, because a follow-up
needs both:

- **the subject** — `airports` / `region` / `metric`. A question that names none of
  its own inherits the previous turn's, so *"and why?"* or *"what about its growth?"*
  resolve against what was just discussed.
- **the transcript** — the last few question/answer pairs, passed to `respond` as
  context. Subject alone is not enough: a *ranking* question names no airport, so
  after one the subject is empty and only the transcript remembers what was shown.
  `context["iatas"]` therefore also records the codes the answer actually displayed,
  and a follow-up falls back to those.

A message **about the conversation** rather than about the data — *"summarize the
previous answers"*, *"what did you just say?"*, *"repeat that in Hebrew"* — is
classified `meta` and skips `resolve → compute` entirely: `respond_meta` answers from
the transcript alone. This is a correctness property, not a convenience. The old
behaviour ran such a message down the data path, computed an empty fact set, and let
the model improvise ("this appears to be the start of our conversation"). A `meta`
turn is forbidden to recompute: it reuses the figures **and their labels** exactly as
already shown, so a summary can never disagree with the answer it summarizes.

Two safety rails: the transcript is capped (`MAX_HISTORY_TURNS`, and each stored
answer truncated) so a long chat cannot grow the prompt without bound; and if a
non-`meta` turn computes an empty result while a conversation exists, it falls back
to the transcript rather than reporting that no airport was found.

---

## 3. Scope — an authoritative, non-arbitrary boundary

Scope is not "top N by size" (arbitrary). It is defined by two external, authoritative
FAA boundaries, unioned:

```
scope = (FAA Large + Medium hubs)  ∪  (airports with an FAA Airport Capacity Profile)
```

- **FAA hub classification** (from the FAA CY2024 enplanement report) gives the
  breadth: all Large (≥1% of national enplanements) and Medium (0.25–1%) hubs.
- **FAA Airport Capacity Profiles** give the depth: the ~33 airports with an official
  declared runway capacity.

The union is 65 airports. It keeps a couple of capacity-profile airports that are now
Small hubs (LGB, MEM) because their authoritative capacity data is valuable.

### Two tiers (a data-coverage property of the airport, not the question)

- **Tier 1 (33 airports)** — has an FAA capacity profile → **true congestion** is
  computable (measured load ÷ declared capacity). Full investment score.
- **Tier 2 (32 airports)** — no capacity profile (e.g. Anchorage, a cargo hub; Nashville
  and Austin, large hubs FAA never profiled) → demand/growth/volume only; congestion
  is not computable and we say so.

---

## 4. Data sources & acquisition

| Metric | Source | Nature |
|--------|--------|--------|
| Declared runway capacity | FAA Airport Capacity Profiles (2014) | PDF, extracted once into `reference/faa_capacity.csv` |
| Hub class + volume | FAA CY2024 enplanements | PDF, parsed into `reference/airports.csv` |
| Passengers, growth, long-haul | BTS T-100 Domestic Market | TranStats form download (2022 + 2024), one-time |
| Operations (dep+arr) | BTS T-100 (ArcGIS REST API) | Live REST query, 2024 |

**Acquisition strategy: fetch once, commit a small snapshot.** `scripts/fetch_data.py`
pulls the BTS data, filters to the 65-airport scope, and writes a committed
per-airport metrics file (`data/processed/airport_metrics.csv`). At runtime the agent
reads that snapshot and never touches a live endpoint — for an investment tool, a flaky
endpoint that quietly breaks analysis mid-session is the worst outcome. Re-fetching is
a single documented command.

**Identifier normalization.** FAA and BTS use different code systems; every identifier
is normalized to **IATA** before any join, and a validation guard fails loudly if a
join leaves a hole (a wrong-but-quiet result is worse than a crash).

---

## 5. Scoring methodology (the KPI)

A weighted blend of three sub-scores, exposed so an analyst sees *why* an airport ranks
where it does. Weights are tunable constants at the top of `scoring/weights.py`.

| Sub-score | Definition | Normalization | Weight |
|-----------|-----------|---------------|--------|
| **Congestion** | annual operations ÷ declared hourly capacity (Visual-condition midpoint) | linear min-max | **0.40** |
| **Growth** | passenger CAGR 2022→2024 | linear min-max | **0.40** |
| **Volume** | annual enplanements (CY2024) | **log** min-max | **0.20** |

```
investment_score = 0.40·congestion_norm + 0.40·growth_norm + 0.20·volume_norm   (Tier 1)
```

**Why these choices**

- **Congestion is a measurement, not an estimate.** We cross real FAA declared capacity
  with real BTS operations. Validation check: ranking Tier-1 airports by this metric puts
  DCA, LGA, SAN, EWR, JFK at the top — exactly the airports the FAA restricts by Order or
  that are famously single-runway-constrained. A simple metric that reproduces the
  regulator's own congestion list is a strong signal it is right. Independently, the FAA's
  own forward capacity outlook is built from the same ratio and flags an overlapping set of
  airports (§7) — a second confirmation the KPI measures the right thing.
- **Normalization is chosen per feature by its distribution.** Congestion and growth are
  bounded, well-behaved → linear min-max stays explainable. Volume is heavy-tailed (ATL/LAX
  dwarf everyone) → log min-max, so a real mid-size airport like SNA isn't crushed to ~0.
  This directly serves the "LA vs Santa Ana" comparison.
- **Delays are a confidence signal, not a fourth sub-score.** Delays overlap with congestion
  (both measure pressure); a separate weight would double-count. (On-time data lives behind a
  separate BTS table; the metric is deferred — see limitations — and the fetch mechanism
  generalizes to it.)

### Tier-2 handling — two rankings, never a false comparison

Tier-2 airports lack congestion (40% of the score) **because of missing data, not because
they are uncongested.** Forcing them into one ranking would either punish them for a data
gap or fabricate the missing value. Instead:

- **Tier 1** ranks on the full `investment_score`.
- **Tier 2** ranks on a `demand_score` (growth + volume, re-normalized), always presented
  separately and labelled "congestion not measured".

A cross-tier question (e.g. "New England candidates") returns BOS (Tier 1, full score)
**and** BDL (Tier 2, demand only) with the distinction stated explicitly.

---

## 6. Where and how AI is used

| Stage | LLM? | Role |
|-------|------|------|
| understand | yes (Claude Haiku 4.5) | NL → structured `{intent, airports, region, metric}` via structured output |
| resolve, route, compute | **no** | deterministic mapping, tiering, scoring |
| respond | yes (Claude Haiku 4.5) | numbers → prose, weaving in confidence/caveats |
| respond_meta | yes (Claude Sonnet 5) | summarize/restate the conversation; *reads a transcript*, never computes (§2.1) |
| second_opinion | yes (Claude Sonnet 5) | independent FAA NPIAS view beside the score; *reasons* over cached facts, never alters a number (§7) |

**Model choice:** the edges are light work (extract a few fields from a sentence; phrase a
handful of computed numbers). Haiku 4.5 does this accurately, fast, and at ~half a cent per
question — a deliberate cost/latency/quality call; a larger model would add cost and latency
with no quality gain for this task. Two stages are the deliberate exceptions, both for the same
reason — they *reason* over a body of material rather than phrasing one fact block, so both run
on the stronger Claude Sonnet 5: the second-opinion layer (§7), which relates two datasets, and
`respond_meta` (§2.1), which reads a whole transcript and must preserve every figure, label and
unit while often answering in the analyst's own language. Every LLM stage falls back to
deterministic code if the call fails or no key is present.

---

## 7. Second opinion — an independent FAA NPIAS view

Beside every scored answer, the agent adds a **second opinion**: an independent read from
the FAA's *National Plan of Integrated Airport Systems* (NPIAS 2025–2029). Where the score
says "how do our congestion/growth/volume metrics rank this airport", the second opinion
says "what does the FAA itself say" — and whether the two **agree, diverge, or fill each
other's gaps**. It is presented in its own block and **never changes a score or a ranking**.

Two independent FAA signals, cached per airport in `reference/npias.csv`
(built once by `scripts/fetch_npias.py`):

| Signal | Source | Nature |
|--------|--------|--------|
| **5-year development cost** | NPIAS Appendix A | the FAA's own $ estimate of each airport's 2025–2029 development need (all 65 airports) |
| **Forward capacity outlook** | NPIAS Narrative, Figure 1 | the FAA's projected runway-capacity status for 2028 and 2033 (ordinal: not flagged / congested / capacity-constrained / severe) |

**The relationship is decided in code, not by the model.** For each airport, deterministic
logic compares the FAA capacity flag to our congestion sub-score and classifies the pair as
*corroborates* (both flag pressure), *diverges* (one runs hotter than the other), or *fills a
gap* (a Tier-2 airport we cannot measure but the FAA does). A dedicated LLM call then phrases
that classification — using only the supplied figures — as a short expert note.

**External validation — the FAA measures congestion the way we do.** The NPIAS capacity
evaluation defines its status from *"the ratio of hourly operational demand to available
runway capacity"* (congested >60% of the time, capacity-constrained >80%, severe >90%) and
explicitly excludes gate/terminal constraints. That is, independently, our exact congestion
metric and our exact airside-not-landside caveat (§9). Its forward list of constrained
airports overlaps our top-ranked congested airports — a second, independent confirmation the
congestion KPI is measuring the right thing. It also **fills a real gap**: for Tier-2 airports
with no FAA capacity profile (SJC, DAL, HOU, SAT), the FAA outlook supplies a congestion
signal our own data cannot compute.

**A stronger model for a harder job.** Unlike the edges (which extract fields or phrase
numbers), this analyst *reasons* over two datasets and relates them, so it runs on Claude
Sonnet 5, not Haiku. It still reads only deterministically-computed figures — it never invents
a number — and falls back to a deterministic template if the call fails.

**Honest framing, enforced.** "Not flagged" means an airport is absent from the FAA's
constrained list, not that it is proven fine (the evaluation covers large/medium hubs). The
development cost is *total* identified development (runway, terminal, safety), not expansion
alone. Figure 1 is a graphic, so its 27 airports were transcribed manually and cross-checked
against the FAA's published totals (11 constrained by 2028, 14 by 2033, 13 more at risk) — a
check enforced both in the build script and in the test suite.

---

## 8. Key tradeoffs

- **Depth vs breadth** — 65 well-instrumented airports over 500 thin ones. The scope boundary
  is authoritative (FAA hub + capacity), so it is defensible rather than arbitrary.
- **Rejected real-time data (FAA SWIM/live status).** Infrastructure investment is driven by
  multi-year structural trends, not today's snapshot. Real-time would add complexity and risk
  with no analytical value.
- **Congestion methodology.** Annual ops ÷ hourly capacity is a utilization proxy, uniform
  across airports, so the *ranking* is meaningful even though the absolute % is not a peak-hour
  reading. Validated against FAA slot-controlled airports (§5).
- **Cached snapshot vs live fetch.** Reliability and reproducibility over freshness; re-fetch is
  one command.

---

## 9. Data limitations & assumptions (stated honestly)

1. **Airside, not landside.** Congestion measures *runway* pressure. The assignment often asks
   about *terminal* expansion; terminal/gate pressure is inferred only indirectly via passenger
   growth. We have no direct landside-capacity metric.
2. **Capacity staleness (2014).** FAA capacity data is from 2014. We assume it still holds except
   where a runway changed; airports with known post-2014 airfield changes (ORD, FLL, CLT) carry a
   `staleness_flag` and are flagged in output.
3. **Scope staleness.** The FAA boundary reflects recent hub data, but airports that grew rapidly
   are Tier 2 until FAA profiles them (e.g. Austin, Nashville).
4. **Long-haul is domestic, passenger-based.** Computed from T-100 Domestic Market as the share of
   departing passengers on >3,000-mile markets. International traffic is excluded (this matters most
   for Anchorage's Asia cargo, which is not passenger traffic anyway). "Flights" is approximated by
   "passengers".
5. **Growth window & COVID.** Growth is a 2022→2024 CAGR (recent post-recovery momentum). A short
   window can flatter airports still rebounding from COVID; flagged where relevant.
6. **Volume source.** Volume uses FAA CY2024 enplanements (authoritative total incl. international);
   growth/long-haul use BTS domestic passengers. Each metric uses its best source.
7. **Delays deferred.** The confidence-multiplier from on-time performance is not yet wired in.
8. **NPIAS second opinion is commentary, not a score input.** The FAA development cost is *total*
   identified development (not expansion alone), and the capacity outlook covers large/medium hubs;
   both sit beside the score and never feed it (§7).

---

## 10. Reliability features built in

- **Silent-join guards.** The reference loader fails loudly if `tier` and capacity-presence
  disagree; the dataset loader fails loudly if any in-scope airport lacks passengers or ops, or a
  Tier-1 airport lacks capacity.
- **Deterministic, reproducible core.** Same input → same output, locked by `tests/`
  (17 unit tests over normalization, sub-scores, weighted total, tier handling, and the NPIAS
  overlay — including a guard that the capacity-outlook transcription reproduces the FAA's totals).
- **Graceful degradation.** No API key, an LLM failure, an unresolvable airport name, a bad chat
  turn — none crash the tool; each degrades to an honest fallback.

---

## 11. Run & verify

```bash
pip install -r requirements.txt
cp .env.example .env          # optional: add ANTHROPIC_API_KEY for the LLM edges
python -m airport_agent.cli   # chat; works with or without a key

python -m pytest              # 17 tests (scoring core + NPIAS overlay)
python scripts/fetch_data.py  # re-build the BTS metrics snapshot (one-time)
python scripts/fetch_npias.py # re-build the NPIAS second-opinion snapshot (one-time)
```

The four assignment questions, end-to-end:

- *Which airports in New England are strong candidates for terminal expansion?* → BOS (Tier 1,
  score) + BDL (Tier 2, demand only), tiers distinguished.
- *Compare LA and Santa Ana congestion levels.* → LAX vs SNA congestion, with log-volume so SNA
  isn't crushed.
- *What is the percentage of long-haul flights out of Anchorage?* → domestic long-haul share, with
  the domestic-only caveat.
- *What is the unmet demand at SFO and why?* → sub-score breakdown (high congestion + growth).
