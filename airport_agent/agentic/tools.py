"""Deterministic tools -- thin wrappers over the scoring core, exposed to the LLM.

Each function returns a JSON-serialisable dict; the model decides WHICH to call.
The numbers are still computed by the same deterministic code the workflow uses
(scoring/, reference/, compute), so nothing here is invented by the LLM. Every
tool has a matching JSON schema in SCHEMAS and an entry in DISPATCH.
"""

from __future__ import annotations

from bisect import bisect_right

from .. import reference
from ..pipeline import resolve as _resolve
from ..pipeline.compute import _facts, _num
from ..scoring import score

_CAP = {0: "not flagged", 1: "congested", 2: "capacity constrained",
        3: "severe capacity constraints"}


def _scored():
    """The full scored frame (65 airports, all sub-scores + composites)."""
    return score.score_airports()


# --- tool implementations -----------------------------------------------------

def resolve_airport(name: str) -> dict:
    """A natural name/description -> the in-scope IATA code (deterministic)."""
    res = _resolve.resolve([name])
    iata = res.resolved.get(name)
    if not iata:
        return {"query": name, "resolved": None, "note": "not an in-scope airport"}
    row = reference.get_airport(iata)
    return {"query": name, "iata": iata, "name": row["name"], "tier": int(row["tier"])}


def get_airport_score(iata: str) -> dict:
    """Full deterministic score + raw metrics for one airport."""
    f = _facts(_scored(), iata.strip().upper())
    f.pop("score_breakdown", None)
    f.pop("requested_metric", None)
    return f


def compare_airports(iatas: list[str]) -> dict:
    """Side-by-side scores for two or more airports."""
    return {"airports": [get_airport_score(i) for i in iatas]}


def rank_airports(region: str | None = None, tier: int | None = None, top: int = 6) -> dict:
    """Top expansion candidates, ranked by the deterministic score. Tier 1 by
    investment_score, Tier 2 by demand_score -- returned separately, never merged."""
    df = _scored()
    if region:
        df = df[df["region"].str.lower() == region.strip().lower()]

    def entries(sub, score_col):
        sub = sub.sort_values(score_col, ascending=False).head(top)
        return [{"iata": r["iata"], "name": r["name"], "tier": int(r["tier"]),
                 "score": _num(r[score_col]),
                 "congestion_norm": _num(r["congestion_norm"]),
                 "growth_norm": _num(r["growth_norm"]),
                 "volume_norm": _num(r["volume_norm"])}
                for _, r in sub.iterrows()]

    out: dict = {"region": region}
    if tier in (None, 1):
        out["tier1_by_investment_score"] = entries(df[df["tier"] == 1], "investment_score")
    if tier in (None, 2):
        out["tier2_by_demand_score"] = entries(df[df["tier"] == 2], "demand_score")
    return out


def get_npias(iata: str) -> dict:
    """FAA NPIAS 'second opinion' facts: 5-year dev cost + capacity outlook."""
    df = reference.load_npias()
    hit = df.loc[df["iata"] == iata.strip().upper()]
    if not len(hit):
        return {"iata": iata, "note": "no NPIAS data"}
    r = hit.iloc[0]
    costs = sorted(int(x) for x in df["dev_cost_2025_2029"].dropna())
    cost = int(r["dev_cost_2025_2029"])
    return {
        "iata": iata.strip().upper(),
        "dev_cost_2025_2029": cost,
        "dev_cost_percentile": round(100 * bisect_right(costs, cost) / len(costs)),
        "capacity_2028": _CAP[int(r["capacity_2028"])],
        "capacity_2033": _CAP[int(r["capacity_2033"])],
    }


def list_scope(region: str | None = None, tier: int | None = None) -> dict:
    """The in-scope airports (optionally filtered by region/tier) -- for grounding."""
    df = reference.load_airports()
    if region:
        df = df[df["region"].str.lower() == region.strip().lower()]
    if tier is not None:
        df = df[df["tier"] == int(tier)]
    return {"count": int(len(df)),
            "airports": [{"iata": r["iata"], "name": r["name"], "tier": int(r["tier"]),
                          "region": r["region"], "hub": r["hub"]}
                         for _, r in df.iterrows()]}


def set_weights(congestion: float, growth: float, volume: float,
                region: str | None = None, top: int = 6) -> dict:
    """Re-rank Tier-1 airports with CUSTOM weights (normalised to sum 1). Use when
    the analyst wants to weight the sub-scores differently than the 0.4/0.4/0.2 default."""
    w = {"congestion": float(congestion), "growth": float(growth), "volume": float(volume)}
    total = sum(w.values())
    if total <= 0:
        return {"error": "weights must sum to a positive number"}
    w = {k: v / total for k, v in w.items()}
    df = _scored()
    df = df[df["tier"] == 1].copy()
    if region:
        df = df[df["region"].str.lower() == region.strip().lower()]
    df["custom_score"] = (w["congestion"] * df["congestion_norm"]
                          + w["growth"] * df["growth_norm"]
                          + w["volume"] * df["volume_norm"])
    df = df.sort_values("custom_score", ascending=False).head(top)
    return {"weights_used": {k: round(v, 3) for k, v in w.items()},
            "note": "Tier-1 re-ranked with custom weights (normalised to sum 1).",
            "ranking": [{"iata": r["iata"], "name": r["name"],
                         "custom_score": _num(r["custom_score"]),
                         "congestion_norm": _num(r["congestion_norm"]),
                         "growth_norm": _num(r["growth_norm"]),
                         "volume_norm": _num(r["volume_norm"])}
                        for _, r in df.iterrows()]}


# --- schemas + dispatch -------------------------------------------------------

SCHEMAS = [
    {"name": "resolve_airport",
     "description": "Resolve a natural airport name, city, or description (e.g. "
                    "'Santa Ana', 'the airport serving Silicon Valley') to its in-scope "
                    "IATA code. Returns resolved:null if the airport is out of scope.",
     "input_schema": {"type": "object",
                      "properties": {"name": {"type": "string"}},
                      "required": ["name"]}},
    {"name": "get_airport_score",
     "description": "Full deterministic score and raw metrics for one airport, by IATA "
                    "code: congestion/growth/volume sub-scores, investment_score (Tier 1) "
                    "or demand_score (Tier 2), enplanements, growth CAGR, long-haul share.",
     "input_schema": {"type": "object",
                      "properties": {"iata": {"type": "string"}},
                      "required": ["iata"]}},
    {"name": "compare_airports",
     "description": "Side-by-side deterministic scores for two or more airports (IATA codes).",
     "input_schema": {"type": "object",
                      "properties": {"iatas": {"type": "array", "items": {"type": "string"}}},
                      "required": ["iatas"]}},
    {"name": "rank_airports",
     "description": "Rank in-scope airports by the deterministic investment/demand score. "
                    "Optionally filter by US region (e.g. 'New England') and/or tier (1 or 2). "
                    "Tier 1 and Tier 2 are returned in separate lists.",
     "input_schema": {"type": "object",
                      "properties": {"region": {"type": "string"},
                                     "tier": {"type": "integer", "enum": [1, 2]},
                                     "top": {"type": "integer"}}}},
    {"name": "get_npias",
     "description": "FAA NPIAS 2025-2029 facts for one airport (IATA): 5-year development "
                    "cost, its percentile across the 65, and the runway-capacity outlook "
                    "for 2028 and 2033. Independent of our score; use for a second opinion.",
     "input_schema": {"type": "object",
                      "properties": {"iata": {"type": "string"}},
                      "required": ["iata"]}},
    {"name": "list_scope",
     "description": "List the in-scope airports (optionally by region/tier). Use to see "
                    "what exists before ranking or to answer 'which airports are covered'.",
     "input_schema": {"type": "object",
                      "properties": {"region": {"type": "string"},
                                     "tier": {"type": "integer", "enum": [1, 2]}}}},
    {"name": "set_weights",
     "description": "Re-rank Tier-1 airports with CUSTOM sub-score weights (they are "
                    "normalised to sum to 1). Use when the analyst wants to emphasise one "
                    "dimension, e.g. 'weight growth more than congestion'.",
     "input_schema": {"type": "object",
                      "properties": {"congestion": {"type": "number"},
                                     "growth": {"type": "number"},
                                     "volume": {"type": "number"},
                                     "region": {"type": "string"},
                                     "top": {"type": "integer"}},
                      "required": ["congestion", "growth", "volume"]}},
]

DISPATCH = {
    "resolve_airport": resolve_airport,
    "get_airport_score": get_airport_score,
    "compare_airports": compare_airports,
    "rank_airports": rank_airports,
    "get_npias": get_npias,
    "list_scope": list_scope,
    "set_weights": set_weights,
}
