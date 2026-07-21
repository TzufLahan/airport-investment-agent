"""Edge 5 (LLM): computed facts -> natural-language answer with caveats.

The LLM only phrases; every number comes from compute.py. Without a key, a
deterministic template renders the same facts. Confidence and limitations
(tier, staleness, domestic-only long-haul) are always surfaced either way.
"""

from __future__ import annotations

import json

from .. import config
from .compute import Result


def respond(result: Result) -> str:
    if config.llm_available():
        try:
            return _llm_respond(result)
        except Exception:
            pass
    return _template_respond(result)


def _as_dict(result: Result) -> dict:
    return {
        "intent": result.intent, "question": result.question,
        "airports": result.airports, "ranking": result.ranking,
        "unresolved": result.unresolved, "notes": result.notes,
    }


_SYSTEM = (
    "You assist an analyst at a firm that invests in US airport expansion. You are given "
    "the user's question and FACTS that were already computed deterministically. Write a "
    "clear, concise answer.\n"
    "RULES: use ONLY the numbers in FACTS -- never invent or alter a figure. Reproduce "
    "each value EXACTLY as given, including decimals and sign (a long-haul share of 0.4 "
    "is 0.4%, never 40%; do not rescale or round away a leading zero). Each airport "
    "includes a 'score_breakdown' (the formula, each sub-score 0-100, its weight, and "
    "its contribution = sub_score x weight, summing to the total). When you state a "
    "composite score (investment_score or demand_score), SHOW this breakdown -- ideally "
    "a small table with columns metric / sub-score / weight / contribution -- so the "
    "reader sees exactly how the number was built. Use the contribution values as given; "
    "never recompute them. Do NOT output a standalone metric glossary/definitions list -- "
    "the app shows metric definitions separately; keep the answer about THIS question. "
    "Surface "
    "confidence and limitations honestly: Tier 2 airports have no FAA capacity profile "
    "(demand signal only; congestion not measured and not comparable to Tier 1); a "
    "'staleness' flag means the 2014 capacity may understate today's; long-haul share is "
    "domestic-passenger-based. congestion_ratio is annual operations per declared hourly "
    "runway slot (higher = more congested); investment_score and demand_score are 0-100. "
    "If an airport is unresolved/out of scope, say so plainly."
)


def _llm_respond(result: Result) -> str:
    from .. import llm

    msg = (f"Question: {result.question}\n\n"
           f"FACTS (JSON):\n{json.dumps(_as_dict(result), ensure_ascii=False)}")
    resp = llm.get_client().messages.create(
        model=llm.MODEL, max_tokens=700, system=_SYSTEM,
        messages=[{"role": "user", "content": msg}],
    )
    return "".join(b.text for b in resp.content if b.type == "text").strip()


# --- deterministic template (renders as clean markdown, like the LLM path) ----

def _template_respond(result: Result) -> str:
    blocks: list[str] = []
    if result.intent == "rank" and result.ranking:
        blocks.append(_rank_md(result.ranking))
    else:
        blocks.extend(_airport_md(a) for a in result.airports)
    for name in result.unresolved:
        blocks.append(f"**{name}** could not be identified among the in-scope airports "
                      "(out of scope).")
    if result.notes:
        blocks.append("\n".join(f"> {note}" for note in result.notes))
    blocks = [b for b in blocks if b]
    return "\n\n".join(blocks) if blocks else "No airports identified in the question."


def _rank_md(rk: dict) -> str:
    scope = rk["region"] or "all in-scope airports"
    out = [f"### Top expansion candidates — {scope}"]
    if rk["tier1"]:
        out.append("**Tier 1 — FAA capacity measured (full score)**")
        out += [_ranked_md(i, a) for i, a in enumerate(rk["tier1"], 1)]
    if rk["tier2"]:
        out.append("**Tier 2 — demand signal only (congestion not measured)**")
        out += [_ranked_md(i, a) for i, a in enumerate(rk["tier2"], 1)]
    return "\n\n".join(out)


def _ranked_md(i: int, a: dict) -> str:
    label = "investment score" if a["tier"] == 1 else "demand score"
    head = f"**{i}. {a['iata']} — {a['name']}**  ·  {label} **{a['score']}/100**"
    return head + "\n\n" + _score_table(a["score_breakdown"])


def _airport_md(a: dict) -> str:
    if "error" in a:
        return f"**{a['iata']}**: {a['error']}."
    label = "investment score" if a["tier"] == 1 else "demand score"
    score = a.get("investment_score") if a["tier"] == 1 else a.get("demand_score")
    parts = [f"**{a['iata']} — {a['name']} (Tier {a['tier']})**  ·  {label} **{score}/100**"]
    highlight = _metric_highlight(a)
    if highlight:
        parts.append(highlight)
    parts.append(_score_table(a["score_breakdown"]))
    if a.get("note"):
        parts.append(f"_{a['note']}_")
    return "\n\n".join(parts)


def _metric_highlight(a: dict) -> str | None:
    """A one-line lead for a specifically-requested metric."""
    metric = a.get("requested_metric")
    if metric == "long_haul":
        return f"**Long-haul share: {a['longhaul_share_pct']}%** of departing domestic passengers."
    if metric == "congestion" and a["tier"] == 1:
        return (f"**Congestion: {a['congestion_ratio']}** annual ops per declared hourly slot "
                f"(declared capacity {a['declared_capacity_ops_hr']} ops/hr).")
    if metric == "growth":
        return f"**Growth (2022-2024 CAGR): {a['growth_cagr_pct']}%**."
    if metric == "volume":
        return f"**Annual passengers (CY24): {a['annual_passengers_cy24']:,}**."
    return None


def _score_table(bd: dict) -> str:
    rows = ["| Metric | Sub-score (0-100) | Weight | Contribution |",
            "|---|---|---|---|"]
    for c in bd["components"]:
        rows.append(f"| {c['metric'].title()} | {c['sub_score_0_100']} | "
                    f"{c['weight']} | {c['contribution']} |")
    rows.append(f"| **Total** |  |  | **{bd['total']}** |")
    return "\n".join(rows)
