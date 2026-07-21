"""Edge 4 (deterministic): dispatch on intent and assemble the answer's FACTS.

Pure numbers from the scoring core -- no phrasing. Every figure here is computed,
never produced by an LLM. respond.py turns this structure into natural language.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field

from .. import config
from ..scoring import score
from ..scoring.weights import WEIGHTS
from .understand import Query


# Authoritative one-line definitions (what each metric means + how it is computed).
# Written here so the LLM explains them accurately instead of inventing definitions.
_DEFINITIONS = {
    "congestion": "annual aircraft operations (takeoffs + landings) divided by the FAA "
                  "declared hourly runway capacity; higher = the runways work harder "
                  "relative to their rated throughput. A measured constraint (Tier 1 only).",
    "growth": "compound annual growth rate (CAGR) of departing passengers from 2022 to "
              "2024 -- the forward-looking demand signal.",
    "volume": "annual passengers (FAA CY2024 enplanements), taken on a log scale so a few "
              "giant hubs do not crush mid-size airports. A size multiplier.",
    "long_haul": "share of departing DOMESTIC passengers on markets longer than 3,000 "
                 "miles (international traffic excluded).",
    "normalization": "each sub-score is scaled to 0-100 across the scored airports "
                     "(min-max; volume on a log scale) before the weights are applied.",
    "investment_score": "Tier-1 composite = 0.4×congestion + 0.4×growth + 0.2×volume.",
    "demand_score": "Tier-2 composite = growth + volume renormalized to 0-100 "
                    "(congestion excluded -- no FAA capacity profile).",
}
_DEF_ORDER = ["congestion", "growth", "volume", "long_haul", "normalization",
              "investment_score", "demand_score"]


def _num(x, nd=1):
    if x is None:
        return None
    try:
        f = float(x)
    except (TypeError, ValueError):
        return None
    return None if math.isnan(f) else round(f, nd)


@dataclass
class Result:
    intent: str
    question: str = ""
    airports: list[dict] = field(default_factory=list)
    ranking: dict | None = None
    unresolved: list[str] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)
    definitions: dict = field(default_factory=dict)


def compute(query: Query, resolved: dict[str, str], unresolved: list[str] | None = None) -> Result:
    df = score.score_airports()
    iatas = list(dict.fromkeys(resolved.values()))  # unique, order preserved
    res = Result(intent=query.intent, question=query.raw, unresolved=list(unresolved or []))

    if query.intent == "rank":
        res.ranking = _rank(df, query.region)
        if query.region:
            res.notes.append(f"Ranked within region: {query.region}.")
    else:
        res.airports = [_facts(df, code, query.metric) for code in iatas]

    res.definitions = _relevant_definitions(res, query)
    _add_caveats(res, query)
    return res


def _relevant_definitions(res: Result, query: Query) -> dict:
    """Only the metrics that actually appear in this answer, in a stable order."""
    tiers = {a.get("tier") for a in res.airports}
    if res.ranking:
        tiers |= {e["tier"] for e in res.ranking["tier1"] + res.ranking["tier2"]}
    keys = {"growth", "volume", "normalization"}
    if 1 in tiers:
        keys |= {"congestion", "investment_score"}
    if 2 in tiers:
        keys.add("demand_score")
    if query.metric == "long_haul":
        keys.add("long_haul")
    return {k: _DEFINITIONS[k] for k in _DEF_ORDER if k in keys}


def _rank(df, region, top=6) -> dict:
    d = df if not region else df[df["region"] == region]
    t1 = d[d["tier"] == 1].sort_values("investment_score", ascending=False).head(top)
    t2 = d[d["tier"] == 2].sort_values("demand_score", ascending=False).head(top)
    return {"region": region,
            "tier1": [_rank_entry(r) for _, r in t1.iterrows()],
            "tier2": [_rank_entry(r) for _, r in t2.iterrows()]}


def _rank_entry(r) -> dict:
    tier = int(r["tier"])
    score = r["investment_score"] if tier == 1 else r["demand_score"]
    return {"iata": r["iata"], "name": r["name"], "tier": tier,
            "region": r["region"], "score": _num(score),
            "score_breakdown": _breakdown(r)}


def _breakdown(r) -> dict:
    """Deterministic derivation of the composite score from its weighted sub-scores.

    Contributions (sub_score * weight) are computed HERE so the LLM only formats
    them and never does the arithmetic itself (which it can garble).
    """
    tier = int(r["tier"])
    if tier == 1:
        parts = [("congestion", _num(r["congestion_norm"]), WEIGHTS["congestion"]),
                 ("growth", _num(r["growth_norm"]), WEIGHTS["growth"]),
                 ("volume", _num(r["volume_norm"]), WEIGHTS["volume"])]
        total = _num(r["investment_score"])
        formula = "0.4×congestion + 0.4×growth + 0.2×volume"
    else:
        weight_sum = WEIGHTS["growth"] + WEIGHTS["volume"]
        parts = [("growth", _num(r["growth_norm"]), round(WEIGHTS["growth"] / weight_sum, 3)),
                 ("volume", _num(r["volume_norm"]), round(WEIGHTS["volume"] / weight_sum, 3))]
        total = _num(r["demand_score"])
        formula = "(0.4×growth + 0.2×volume) / 0.6   [congestion excluded: no FAA capacity]"
    components = [
        {"metric": name, "sub_score_0_100": sub, "weight": w,
         "contribution": None if sub is None else round(sub * w, 1)}
        for name, sub, w in parts
    ]
    return {"formula": formula, "components": components, "total": total}


def _facts(df, iata, metric=None) -> dict:
    hit = df[df["iata"] == iata]
    if not len(hit):
        return {"iata": iata, "error": "not in scope"}
    r = hit.iloc[0]
    f = {
        "iata": iata, "name": r["name"], "tier": int(r.tier), "region": r.region,
        "hub": r.hub, "requested_metric": metric,
        "growth_cagr_pct": _num(r.growth_cagr_pct, 2),
        "longhaul_share_pct": _num(r.longhaul_share_pct, 1),
        "annual_passengers_cy24": int(r.enplanements_cy24),
        "annual_ops": None if _num(r.ops) is None else int(r.ops),
        "growth_norm": _num(r.growth_norm), "volume_norm": _num(r.volume_norm),
        "demand_score": _num(r.demand_score),
        "staleness": bool(r.staleness_flag),
        "note": (r.notes or None),
    }
    if r.tier == 1:
        f.update({
            "congestion_ratio": _num(r.congestion_raw, 0),
            "declared_capacity_ops_hr": _num(r.declared_capacity, 0),
            "congestion_norm": _num(r.congestion_norm),
            "investment_score": _num(r.investment_score),
        })
    f["score_breakdown"] = _breakdown(r)
    return f


def _add_caveats(res: Result, query: Query) -> None:
    tier2_present = any(a.get("tier") == 2 for a in res.airports) or (
        res.ranking and res.ranking["tier2"]
    )
    if query.metric == "long_haul":
        res.notes.append(
            f"Long-haul = share of departing DOMESTIC passengers on markets over "
            f"{config.LONG_HAUL_MILES} miles; international traffic is excluded."
        )
    if tier2_present:
        res.notes.append(
            "Tier 2 airports have no FAA capacity profile: demand signal only, "
            "congestion is not measured and is not comparable to Tier 1 scores."
        )
    if any(a.get("staleness") for a in res.airports):
        res.notes.append(
            "A flagged airport has known post-2014 capacity changes; its congestion "
            "may be understated relative to today."
        )
