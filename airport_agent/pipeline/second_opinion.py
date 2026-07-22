"""Second opinion (independent FAA-NPIAS expert), presented BESIDE the score.

The deterministic score answers "how do our congestion/growth/volume metrics rank
this airport". This layer answers a different question -- "what does the FAA itself
say" -- from two cached NPIAS 2025-2029 signals (reference/npias.csv):

  * the FAA's five-year development-cost estimate (Appendix A), and
  * the FAA's forward runway-capacity outlook for 2028 and 2033 (Narrative Fig. 1).

Every number is looked up deterministically here; a dedicated "FAA analyst" LLM
call only phrases them and states how the FAA view RELATES to our score -- whether
it corroborates it, diverges from it, or fills a gap we could not measure (a Tier-2
airport has no FAA capacity profile, so we have no congestion number for it). The
relationship itself is decided in code, not by the model. Without an API key a
template renders the same facts. This block never changes a score or a ranking.
"""

from __future__ import annotations

import json
from bisect import bisect_right

from .. import config, reference
from .compute import Result

_CAP = {0: "not flagged", 1: "congested", 2: "capacity constrained",
        3: "severe capacity constraints"}

_REL_NOTE = {
    "corroborate": "FAA's forward capacity outlook corroborates the high congestion "
                   "the team's score already flags.",
    "faa_more_concerned": "FAA's forward outlook flags a runway constraint the team's "
                          "current-snapshot congestion score does not emphasise.",
    "we_more_concerned": "The team's congestion score runs hotter than the FAA outlook, "
                         "which marks the airport congested but stops short of a hard "
                         "capacity constraint.",
    "faa_notes_congestion": "The FAA marks it congested in its outlook (a watch signal, "
                            "short of a hard capacity constraint), broadly in line with "
                            "the team's moderate congestion score.",
    "both_quiet": "Neither the team's congestion score nor the FAA outlook flags any "
                  "congestion or capacity constraint.",
    "fills_gap": "Tier 2 has no FAA capacity profile, so the team has no congestion "
                 "number here; the FAA outlook supplies an independent congestion signal.",
    "both_quiet_t2": "Tier 2 (no congestion measure), and the FAA capacity outlook "
                     "does not flag it either.",
}

_FOOTNOTE = ("_Source: FAA NPIAS 2025-2029 (Appendix A development costs; Narrative "
             "Figure 1 capacity outlook). This view sits beside the deterministic "
             "score and never changes it. \"Not flagged\" means an airport is not on "
             "the FAA's constrained list -- not proof it is unconstrained (small hubs "
             "may not have been evaluated)._")

_SYSTEM = (
    "You are a senior FAA-infrastructure analyst giving a SECOND OPINION to an airport "
    "investment team. For each airport you get the team's own deterministic score and "
    "independent FAA NPIAS 2025-2029 facts: a five-year development-cost estimate and a "
    "forward runway-capacity outlook for 2028 and 2033. Write a tight expert view, about "
    "one to two sentences per airport.\n"
    "RULES:\n"
    "- Use ONLY the numbers provided; never invent or alter a figure.\n"
    "- The user's question is context only. Do NOT answer or restate it, and do NOT "
    "apologise for any metric (passengers, growth, long-haul, etc.) you were not given -- "
    "comment solely on the FAA facts for these airports.\n"
    "- For each airport, state the FAA development-need figure with its percentile and the "
    "capacity outlook (2028 -> 2033), then explain how the FAA view relates to the team's "
    "score: corroborates it, diverges from it, or fills a gap the team could not measure "
    "(a Tier-2 airport has no FAA capacity profile, so the team has no congestion number). "
    "Let the provided 'relationship' guide your framing, but write natural prose -- never "
    "quote it or any other internal field name.\n"
    "- Be honest: 'not flagged' means the airport is not on the FAA's constrained list, NOT "
    "that it is proven fine. Do NOT re-rank the airports or alter any score.\n"
    "- Lead each airport with '**<name> (<IATA>)**'."
)


def second_opinion(result: Result) -> str | None:
    """An FAA-NPIAS second-opinion block for the airports in `result`, or None."""
    subjects = _subjects(result)
    if not subjects:
        return None
    df = reference.load_npias()
    sorted_costs = sorted(int(x) for x in df["dev_cost_2025_2029"].dropna())

    facts = []
    for s in subjects:
        row = df.loc[df["iata"] == s["iata"]]
        if len(row):
            facts.append(_facts_for(s, row.iloc[0], sorted_costs))
    if not facts:
        return None

    body = None
    if config.llm_available():
        try:
            body = _llm_view(facts, result.question)
        except Exception:
            body = None
    if not body:
        body = _template_view(facts)
    return f"### 🏛️ FAA NPIAS -- independent second opinion\n\n{body}\n\n{_FOOTNOTE}"


def _subjects(result: Result, cap: int = 6) -> list[dict]:
    """Uniform (iata, name, tier, our_score, congestion_norm) for each resolved
    airport, drawn from either a single/compare answer or a ranking's top entries."""
    rows: list[dict] = []
    if result.ranking:
        for e in result.ranking["tier1"][:3] + result.ranking["tier2"][:3]:
            rows.append({"iata": e["iata"], "name": e["name"], "tier": e["tier"],
                         "our_score": e["score"], "congestion_norm": _cong(e)})
    else:
        for a in result.airports:
            if a.get("error"):
                continue
            tier = a["tier"]
            our = a.get("investment_score") if tier == 1 else a.get("demand_score")
            rows.append({"iata": a["iata"], "name": a["name"], "tier": tier,
                         "our_score": our, "congestion_norm": a.get("congestion_norm")})
    seen, uniq = set(), []
    for r in rows:
        if r["iata"] not in seen:
            seen.add(r["iata"])
            uniq.append(r)
    return uniq[:cap]


def _cong(entry: dict):
    """Tier-1 congestion sub-score (0-100) from an airport or ranking entry, else None."""
    if "congestion_norm" in entry:
        return entry["congestion_norm"]
    for c in (entry.get("score_breakdown") or {}).get("components", []):
        if c["metric"] == "congestion":
            return c["sub_score_0_100"]
    return None


def _relationship(tier: int, cong, faa_flag: int) -> str:
    if tier == 2:
        return "fills_gap" if faa_flag >= 1 else "both_quiet_t2"
    hot = cong is not None and cong >= 55
    if faa_flag >= 2:                       # FAA: capacity constrained / severe
        return "corroborate" if hot else "faa_more_concerned"
    if faa_flag == 1:                       # FAA: congested (a watch signal, not a constraint)
        return "we_more_concerned" if hot else "faa_notes_congestion"
    return "both_quiet"                     # FAA: not flagged at all


def _facts_for(subject: dict, row, sorted_costs: list[int]) -> dict:
    cost = int(row["dev_cost_2025_2029"])
    c28, c33 = int(row["capacity_2028"]), int(row["capacity_2033"])
    faa_flag = max(c28, c33)
    rel = _relationship(subject["tier"], subject["congestion_norm"], faa_flag)
    pctile = round(100 * bisect_right(sorted_costs, cost) / len(sorted_costs))
    return {
        "iata": subject["iata"], "name": subject["name"], "tier": subject["tier"],
        "our_score": subject["our_score"],
        "our_congestion_norm": subject["congestion_norm"],
        "faa_dev_cost": _usd(cost),
        "faa_dev_cost_percentile": pctile,
        "faa_capacity_2028": _CAP[c28],
        "faa_capacity_2033": _CAP[c33],
        "worsening": c33 > c28,
        "relationship": rel,
        "relationship_note": _REL_NOTE[rel],
    }


def _usd(n: int) -> str:
    return f"${n / 1e9:.2f}B" if n >= 1e9 else f"${n / 1e6:.1f}M"


def _ordinal(n: int) -> str:
    suffix = "th" if 10 <= n % 100 <= 20 else {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
    return f"{n}{suffix}"


def _llm_view(facts: list[dict], question: str) -> str:
    from .. import llm

    msg = (f"Question: {question}\n\n"
           f"AIRPORTS (JSON):\n{json.dumps(facts, ensure_ascii=False)}")
    resp = llm.get_client().messages.create(
        model=config.SECOND_OPINION_MODEL, max_tokens=550, system=_SYSTEM,
        messages=[{"role": "user", "content": msg}],
    )
    return "".join(b.text for b in resp.content if b.type == "text").strip()


def _template_view(facts: list[dict]) -> str:
    blocks = []
    for f in facts:
        head = (f"**{f['name']} ({f['iata']})** -- FAA dev-need 2025-29: "
                f"{f['faa_dev_cost']} ({_ordinal(f['faa_dev_cost_percentile'])} pct) - "
                f"outlook: {f['faa_capacity_2028']} -> {f['faa_capacity_2033']}"
                + (" (worsening)" if f["worsening"] else ""))
        blocks.append(f"{head}\n\n> {f['relationship_note']}")
    return "\n\n".join(blocks)
